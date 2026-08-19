"""Minimal LSPK v18 reader — list and extract entries from a BG3 .pak.

The installed modlist is the only authority on what a mod actually does; mod
pages and changelogs are frequently stale. Every .pak under the Mod Organizer
install is an LSPK archive, so its Progressions.lsx, Stats/Generated/Data/*.txt
and Lists/*.lsx can be read directly rather than inferred.

    python3 lspk.py <file.pak>                  # list every entry
    python3 lspk.py <file.pak> <entry> > out    # extract one entry

Install root (this machine): /mnt/mercury/Games/Listonomicon/mods

What to read for what:
  Progressions/Progressions.lsx        which level grants which passive
  Lists/SpellLists.lsx                 what a domain/subclass spell list holds
  Lists/PassiveLists.lsx               invocation tiers, in ascending order
  ActionResourceDefinitions/*.lsx      ReplenishType — Turn / ShortRest / Rest
  Stats/Generated/Data/Passive.txt     Boosts, Conditions, TooltipUseCosts
  Stats/Generated/Data/Status_BOOST.txt  what a status actually does, and StackId
  Stats/Generated/Data/Spell_*.txt     Shape, Range, SpellRoll, Cooldown, UseCosts

Requires the lz4 package. Base-game paks are NOT under the mods root, so
vanilla features cannot be confirmed this way.
"""
import struct, lz4.block, zlib, sys, io

HDR = struct.Struct("<4sIQIBB16sH")   # magic, version, listOffset, listSize, flags, prio, md5, numParts
ENT = struct.Struct("<256sIHBBII")    # name, off1, off2, part, flags, sizeOnDisk, uncompressed

def _decomp(buf, flags, usize):
    m = flags & 0x0F
    if m == 0: return buf
    if m == 1: return zlib.decompress(buf)
    if m == 2: return lz4.block.decompress(buf, uncompressed_size=usize)
    raise ValueError("method %d" % m)

class Pak:
    def __init__(self, path):
        self.path = path
        self.f = open(path, "rb")
        magic, ver, off, size, fl, pr, md5, parts = HDR.unpack(self.f.read(HDR.size))
        if magic != b"LSPK": raise ValueError("not LSPK")
        self.ver = ver
        self.f.seek(off)
        n, csize = struct.unpack("<II", self.f.read(8))
        raw = lz4.block.decompress(self.f.read(csize), uncompressed_size=n*ENT.size)
        self.entries = {}
        for i in range(n):
            name, o1, o2, part, flags, sod, us = ENT.unpack_from(raw, i*ENT.size)
            name = name.split(b"\0")[0].decode("utf-8", "replace")
            self.entries[name] = (o1 | (o2 << 32), flags, sod, us)

    def read(self, name):
        off, flags, sod, us = self.entries[name]
        self.f.seek(off)
        return _decomp(self.f.read(sod), flags, us)

    def names(self): return sorted(self.entries)

if __name__ == "__main__":
    p = Pak(sys.argv[1])
    if len(sys.argv) == 2:
        for n in p.names(): print(n)
    else:
        sys.stdout.buffer.write(p.read(sys.argv[2]))
