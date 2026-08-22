# Tests

Stdlib `unittest`, no third-party runner — the tree has no dependency file and adding one to run
four assertions is not a trade worth making. From the repository root:

```sh
python -m unittest discover -s plugins/listo-build/tests
```

Each test file puts the script directory it needs on `sys.path` itself, so the runner needs no
packaging and the tests directory needs no `__init__.py`.

## Rules

Fixtures are **copies**, written into a `tempfile` directory by the test that needs them. No test
reads, and certainly no test writes, `assets/ledger-vN.json`, `assets/chassis-seeds.json`,
`assets/subclass-bases.json` or `assets/dip-catalogue.json`. A test that mutates a published asset
is a test that can destroy a scoring run, and the pipeline's caches are keyed on exactly those
files' digests.

Reading a published asset to *derive a fixture* is fine, and one test does it: the comma-bearing
subclass keys must come from the real inventory or the test stops proving anything about it.
