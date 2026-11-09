# Adding and running your tests

Writing your own tests is a required part of the coursework. Use Python's built-in `unittest`; no extra package is needed.

## What to keep and what to add

- Keep `tests/test_public.py` unchanged. These supplied tests check basic interfaces, not all required behaviour. Do not remove, disable or weaken them to make a run pass.
- Add your own files named `test_*.py` under `tests/student/`. You may use one file or group related tests into several files.
- Retain both `tests/__init__.py` and `tests/student/__init__.py`. They allow recursive test discovery; you do not need to edit them.
- Keep supplied Stage 2 tests under `tests_stage2/` unchanged. Add your own Stage 2 tests under `tests/student/` after recording your Stage 1 tag.

## Try a neutral example

Create `tests/student/test_initial_state.py` and enter:

```python
import unittest

from bakery import Bakery


class InitialStateTests(unittest.TestCase):
    def test_custom_starting_cash(self):
        # Arrange: choose an explicit starting value, in pence.
        bakery = Bakery(duration=1, initial_cash=12345)

        # Assert: construction should retain the value we supplied.
        self.assertEqual(bakery.get_cash(), 12345)

    def test_negative_starting_cash_is_rejected(self):
        # Arrange: the constructor requires non-negative starting cash.
        invalid_cash = -1

        # Act and assert: this construction must raise ValueError.
        with self.assertRaises(ValueError):
            Bakery(duration=1, initial_cash=invalid_cash)
```

These tests check documented constructor behaviour. Both should already pass on the starter: they teach test structure and do not diagnose an assessed defect. Copying these examples alone does not provide evidence of your own test design.

The `with self.assertRaises(ValueError):` block sets up the exception check before running the indented operation. The test passes if that operation raises `ValueError`, fails if no exception is raised, and reports an error if a different exception is raised. Keep only the operation expected to fail inside the block; arrange valid supporting state beforehand. Do not write `self.assertRaises(ValueError, Bakery(...))`: that executes the constructor before the assertion can catch its exception.

Open a terminal in the coursework folder containing `main.py`. Run this one file with:

```sh
python3 -m unittest tests.student.test_initial_state -v
```

You should see both test methods reported as `ok`, followed by `Ran 2 tests` and `OK`. You do not need to run `main.py` first or register the test anywhere. Run tests through these commands rather than executing the test file directly.

Run the supplied Stage 1 tests and all your own tests together with:

```sh
python3 -m unittest discover -s tests -v
```

The example adds two tests to the three supplied tests. A passing run only establishes the behaviour checked by those tests.

## Add tests for your repairs

1. Create another file, such as `tests/student/test_accounting.py`, or add another test method to an existing file. Import `unittest` and the application classes you need.
2. Define a class inheriting from `unittest.TestCase`. Give every test method a distinct name starting with `test_` and a `self` parameter.
3. Set up a small, fresh bakery using the constructors in `API.md`. Choose concrete initial conditions and inputs, then calculate the expected result independently from the published rules.
4. Exercise the behaviour, for example by calling `Bakery.step(decision, demand)`. Assert the expected record values or state using methods such as `self.assertEqual(...)`. Use `self.assertRaises(ValueError)` when rejection is expected.
5. Run the test against the faulty code. For a regression test targeting a defect, check that its failure shows the intended behaviour is wrong, rather than a typo or import problem.
6. Repair the application and rerun the test and the full suite. Keep the test to guard against recurrence. Do not change a sound expected result merely to match faulty output.

Use the documented interfaces rather than private implementation details or exact terminal wording. Each test should set up its own state and should not depend on another test running first. Do not calculate expected results by calling the same application calculation you are testing. You usually do not need to simulate keyboard input: call the Python methods directly.

`FAIL` normally means an assertion did not hold; `ERROR` means an exception interrupted the test. Read the traceback in either case. An expected exception inside `assertRaises` passes. If your test is missing from the output, check the `test_` filename and method prefixes, the `TestCase` inheritance, and that both `__init__.py` files remain present. `Ran 0 tests` is not evidence that your code works.

## Record and extend your tests

Include your Stage 1 tests in the commit tagged `stage1-complete`. Continue in the same repository, preserving those tests while adding tests for Stage 2. Run the supplied Stage 2 tests separately after implementing the extension:

```sh
python3 -m unittest discover -s tests_stage2 -v
```

These supplied Stage 2 tests are expected not to pass on the unextended starter. See the “Testing Stage 2” section of the coursework document for required coverage and the component rubric for marking. The guidance above explains how to write and run the tests.

For v4, your own Stage 2 tests need to cover basic fulfilment, rejected-decision rollback and no-order replay compatibility. Retain your Stage 1 regression tests. Extra Stage 2 cases are optional; test counts do not independently earn marks.
