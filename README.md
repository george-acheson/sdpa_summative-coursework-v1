# Community bakery coursework starter

Read the coursework document first: it is the complete student brief. API.md and API_STAGE2.md specify technical interfaces. This program starts and passes its tests, but contains defects described by the reported issues. Repair the supplied code and add regression tests; passing the public tests is only a starting point.

Use Python 3.11 or later. No installation or external packages are required. Open this folder in your editor and run `main.py` as an ordinary Python script, or open a terminal in the folder containing `main.py` and use the commands below. Keep all the supplied Python files together beside `main.py`; they use ordinary imports such as `from bakery import Bakery`.

```sh
python3 main.py
python3 main.py --scenario data/example.json --decisions data/example_decisions.json --output output/run.json
python3 -m unittest discover -s tests -v
```

In the replay command, `--scenario` selects the scenario JSON file (simulation conditions), `--decisions` selects the decision JSON file (weekly choices), and `--output` selects the output JSON file (weekly results). See the brief for definitions and API.md for the exact formats.

The six-week example trades with one employee and replenishes its ingredients. It is an interface demonstration, not a complete oracle. Keep the supplied data unchanged and create separate small cases for your tests. Put tests under `tests/student/`; retain its `__init__.py` so discovery finds them.

See the coursework document for the development sequence, Stage 1 tag, required evidence and submission checklist. Replace this README with exact run/test commands and a short overview of the design and main responsibilities. Method details belong in docstrings. No separate diagnosis report is required.

Run `python3 -m unittest discover -s tests_stage2 -v` after implementing Stage 2. These extension tests intentionally do not pass against the Stage 1 starter.

## Writing your tests

Keep `tests/test_public.py` unchanged and add your own `test_*.py` files under `tests/student/`. Start with [Adding and running your tests](tests/README.md), which includes a neutral example and commands to run one file or the full suite.
