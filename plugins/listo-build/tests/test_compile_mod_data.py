import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "listo-build", "scripts")
sys.path.insert(0, SCRIPTS)
import compile_mod_data as CMD  # noqa: E402


class StatsParser(unittest.TestCase):
    def test_stats_entries_preserve_source_fields_and_unknown_directives(self):
        records = list(
            CMD.parse_stats(
                '''new entry "Projectile_Test"
'''
                '''type "SpellData"
'''
                '''using "Projectile_Base"
'''
                '''data "SpellType" "Projectile"
'''
                '''data "RequirementConditions" "Tagged(\\"TEST\\")"
'''
                '''data "Repeated" "first"
'''
                '''data "Repeated" "second"
'''
                '''add object category "I_TEST",1,0,0,0,0,0,0,0
'''
            )
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.record_type, "SpellData")
        self.assertEqual(record.name, "Projectile_Test")
        self.assertEqual(record.using, "Projectile_Base")
        self.assertEqual(record.data["RequirementConditions"], 'Tagged("TEST")')
        self.assertEqual(record.data["Repeated"], ["first", "second"])
        self.assertEqual(record.data["_directives"][0]["command"], "add")

    def test_treasure_tables_become_their_own_type(self):
        record = next(CMD.parse_stats('new treasuretable "TT_Test"\nnew subtable "1,1"\n'))
        self.assertEqual(record.record_type, "TreasureTable")
        self.assertEqual(record.name, "TT_Test")
        self.assertIn("new subtable", record.raw)


class LsxParser(unittest.TestCase):
    def test_top_level_nodes_are_rows_and_nested_nodes_stay_attached(self):
        payload = b'''<?xml version="1.0"?>
<save><region id="ClassDescriptions"><node id="root"><children>
  <node id="ClassDescription">
    <attribute id="Name" type="FixedString" value="Inquisitor"/>
    <attribute id="UUID" type="guid" value="class-uuid"/>
    <attribute id="DisplayName" type="TranslatedString" handle="h123" version="1"/>
    <children><node id="SubClass"><attribute id="Object" value="subclass-uuid"/></node></children>
  </node>
</children></node></region></save>'''
        records = list(CMD.parse_lsx(payload))
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.record_type, "ClassDescription")
        self.assertEqual(record.name, "Inquisitor")
        self.assertEqual(record.uuid, "class-uuid")
        self.assertEqual(record.data["attributes"]["DisplayName"]["handle"], "h123")
        self.assertEqual(record.data["children"][0]["node_type"], "SubClass")

    def test_localization_is_keyed_by_content_handle(self):
        record = next(CMD.parse_localization(b'<contentList><content contentuid="h123" version="2">Name</content></contentList>'))
        self.assertEqual(record.record_type, "Localization")
        self.assertEqual(record.name, "h123")
        self.assertEqual(record.data, {"text": "Name", "version": "2"})

    def test_localization_accepts_loose_content_fragments(self):
        records = list(
            CMD.parse_localization(
                b'<content contentuid="h1">One</content>\n'
                b'<content contentuid="h2">Two</content>'
            )
        )
        self.assertEqual([(record.name, record.data["text"]) for record in records], [("h1", "One"), ("h2", "Two")])

    def test_localization_repairs_the_shipped_missing_entity_semicolon(self):
        payload = (
            b'<contentList><content contentuid="h123">'
            b'Gain &lt;LSTag Tooltip="Nature"&gt>Nature&lt;/LSTag&gt;. '
            b'Apply &lt;LSTag Tooltip="Vines"&gtVines&lt;/LSTag&gt;.'
            b"</content></contentList>"
        )
        record = next(CMD.parse_localization(payload))
        self.assertEqual(
            record.data["text"],
            'Gain <LSTag Tooltip="Nature">Nature</LSTag>. Apply <LSTag Tooltip="Vines">Vines</LSTag>.',
        )

    def test_legacy_version_six_lsf_retries_with_version_five_metadata(self):
        payload = bytearray(64)
        payload[:4] = b"LSOF"
        payload[4:8] = (6).to_bytes(4, "little")
        payload[48] = 2
        payload[56] = 15
        seen = []
        original = CMD._forge_parse_resource

        def fake_parser(data):
            version = int.from_bytes(data[4:8], "little")
            seen.append(version)
            if version == 6:
                raise ValueError("unknown compression method 15")
            return "parsed"

        try:
            CMD._forge_parse_resource = fake_parser
            self.assertEqual(CMD._parse_binary_document(bytes(payload)), "parsed")
        finally:
            CMD._forge_parse_resource = original
        self.assertEqual(seen, [6, 5])


class ProfileParser(unittest.TestCase):
    def test_enabled_profile_and_game_load_order_are_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "modlist.txt"
            settings = root / "modsettings.lsx"
            profile.write_text("# generated\n+Late Patch\n-Disabled\n+Base Mod\n", encoding="utf-8")
            settings.write_text(
                '''<save><region id="ModuleSettings"><node id="root"><children>
'''
                '''<node id="ModOrder"><children id="Module"><attribute id="UUID" value="base"/></children><children id="Module"><attribute id="UUID" value="patch"/></children></node>
'''
                '''<node id="Mods"><children><node id="ModuleShortDesc"><attribute id="UUID" value="base"/><attribute id="Name" value="Base"/><attribute id="Folder" value="BaseFolder"/></node><node id="ModuleShortDesc"><attribute id="UUID" value="patch"/><attribute id="Name" value="Patch"/><attribute id="Folder" value="PatchFolder"/></node></children></node>
'''
                '''</children></node></region></save>''',
                encoding="utf-8",
            )
            self.assertEqual(CMD.parse_profile(profile), [(2, "Late Patch"), (4, "Base Mod")])
            order, metadata = CMD.parse_modsettings(settings)
            by_uuid, by_folder = CMD._modules_from_settings(order, metadata, 6)
            self.assertEqual(order, ["base", "patch"])
            self.assertEqual(by_uuid["base"].load_order, 6)
            self.assertEqual(by_uuid["patch"].load_order, 7)
            self.assertEqual(by_folder["basefolder"].name, "Base")

    def test_base_discovery_excludes_media_archives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            localization = root / "Localization"
            localization.mkdir()
            for relative in (
                "Game.pak",
                "Shared.pak",
                "Patch9_HotFix1.pak",
                "Models.pak",
                "VirtualTextures.pak",
                "Localization/English.pak",
                "Localization/Voice.pak",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            discovered = {
                path.relative_to(root).as_posix()
                for path in CMD._base_pak_paths(root)
            }
            self.assertEqual(
                discovered,
                {
                    "Game.pak",
                    "Shared.pak",
                    "Patch9_HotFix1.pak",
                    "Localization/English.pak",
                },
            )


class SqliteSchema(unittest.TestCase):
    def test_each_record_type_gets_a_source_bearing_table(self):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        database = CMD.Database(connection)
        module = CMD.Module("module-uuid", "Example Module", "Example", 7)
        origin = CMD.Origin("Example MO2 Mod", "mod", 12, 7, 0, "Example/example.pak", module)
        database.insert_record(
            origin,
            "Public/Example/Feats/Feats.lsx",
            "lsx",
            CMD.Record("Feat", "Alert", "feat-uuid", None, {"attributes": {"Name": "Alert"}}),
        )
        table = connection.execute("SELECT table_name FROM data_types WHERE record_type = 'Feat'").fetchone()[0]
        columns = [row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')]
        row = connection.execute(
            f'SELECT source, source_kind, load_order, record_name, data FROM "{table}"'
        ).fetchone()
        self.assertIn("source", columns)
        self.assertIn("source_kind", columns)
        self.assertEqual(row[:4], ("Example MO2 Mod", "mod", 7, "Alert"))
        self.assertEqual(json.loads(row[4])["attributes"]["Name"], "Alert")


class EntryClassification(unittest.TestCase):
    def test_character_build_resources_are_extracted_and_assets_are_only_indexed(self):
        self.assertEqual(CMD.classify_entry("Public/Mod/Stats/Generated/Data/Spell_Target.txt"), "stats")
        self.assertEqual(CMD.classify_entry("Public/Mod/ClassDescriptions/ClassDescriptions.lsx"), "lsx")
        self.assertEqual(CMD.classify_entry("Mods/Mod/Localization/English/english.xml"), "localization")
        self.assertEqual(CMD.classify_entry("Public/Mod/RootTemplates/item.lsf"), "resource")
        self.assertEqual(CMD.classify_entry("Mods/Mod/Localization/English/english.loca"), "localization")
        self.assertEqual(CMD.classify_entry("Localization/English/english.loca"), "localization")
        self.assertEqual(CMD.classify_entry("Mods/Mod/GUI/icon.dds"), "indexed")


if __name__ == "__main__":
    unittest.main()
