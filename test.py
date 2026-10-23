# Supplied checks for your program.
#
# Run from this folder:
#
#     python3 test.py -v
#
# (On Windows use: py -3 test.py -v)
#
# This file runs the following checks against Card.py:
#
# 1. Direct checks of transaction_history, including an empty list.
# 2. The three worked examples from brief.md, as whole-program runs.
# 3. Your own tests in tests.txt: every function check under "# Function
#    checks" and every program case under "# Program cases".
#
# It also checks that the five given functions are still there
# with their names and parameters unchanged, because the hidden tests call
# them by name.
#
# Passing these checks is not your test mark. Designing your own tests in
# tests.txt is a separate, graded part of the assignment: see "Testing your
# program" in brief.md. Work out every expected value by hand before you run
# anything. A test of yours that fails may mean your program is wrong, or that
# your expected value is wrong. Find out which.
#
# What you should see:
#
# - ALL checks passing ends with:
#
#       ----------------------------------------------------------------------
#       Ran N tests in ...s
#
#       OK
#
# - If SOME checks fail, each failed one is listed under "FAIL:" with what
#   your program gave and what was expected; the run ends with
#   "FAILED (failures=N)". With the untouched template the output checks fail,
#   because the functions return None and main() prints nothing.
#
# Fix the first failing check and re-run; repeat until you get "OK".
#
# Do not change this file.

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROGRAM = HERE / "Card.py"
TESTS_FILE = HERE / "tests.txt"

TIMEOUT = 30

# The names and parameters given in the template. They must not change.
GIVEN_FUNCTIONS = {
    "ride_fare": ["card_type", "full_fare", "follows_ride"],
    "can_ride": ["balance", "fare"],
    "can_top_up": ["balance", "amount"],
    "transaction_history": ["transactions"],
    "main": [],
}
CHECKABLE = ["ride_fare", "can_ride", "can_top_up"]

# The prompts the program prints. input() echoes each one into stdout, so they
# are removed before the program's own lines are compared.
PROMPTS = [
    "Card type (1 adult, 2 student, 3 elder): ",
    "Transaction (1 ride, 2 top-up, 0 stop): ",
    "Starting balance: ",
    "Amount: ",
]

MAX_FUNCTION_CHECKS = 15
MAX_PROGRAM_CASES = 8


# ---- The worked examples from brief.md ----

EXAMPLE_1_INPUT = "2\n20\n1\n12\n1\n9\n2\n100\n1\n5\n0\n"
EXAMPLE_1_OUTPUT = [
    "Card type: student",
    "Rides taken: 3",
    "Top-ups: 1",
    "Fares paid: 12.00",
    "Lowest balance: 10.50",
    "Final balance: 108.00",
    "Refused: 0",
    '1: Ride accepted. Balance: 14.00',
    '2: Ride accepted. Balance: 10.50',
    '3: Top-up accepted. Balance: 110.50',
    '4: Ride accepted. Balance: 108.00',
]

EXAMPLE_2_INPUT = "1\n10\n1\n30\n1\n14\n2\n70\n2\n50\n1\n20\n1\n50\n0\n"
EXAMPLE_2_OUTPUT = [
    "Card type: adult",
    "Rides taken: 2",
    "Top-ups: 1",
    "Fares paid: 50.00",
    "Lowest balance: -20.00",
    "Final balance: 10.00",
    "Refused: 3",
    '1: Ride accepted. Balance: -20.00',
    '2: Ride refused. Balance: -20.00',
    '3: Top-up refused. Balance: -20.00',
    '4: Top-up accepted. Balance: 30.00',
    '5: Ride accepted. Balance: 10.00',
    '6: Ride refused. Balance: 10.00',
]

EXAMPLE_3_INPUT = "3\n2950\n2\n100\n2\n50\n1\n1\n1\n8\n1\n1\n0\n"
EXAMPLE_3_OUTPUT = [
    "Card type: elder",
    "Rides taken: 3",
    "Top-ups: 1",
    "Fares paid: 2.00",
    "Lowest balance: 2950.00",
    "Final balance: 2998.00",
    "Refused: 1",
    '1: Top-up refused. Balance: 2950.00',
    '2: Top-up accepted. Balance: 3000.00',
    '3: Ride accepted. Balance: 2999.00',
    '4: Ride accepted. Balance: 2998.00',
    '5: Ride accepted. Balance: 2998.00',
]


# ---- Running the program ----

def run_program(stdin_text):
    """Run Card.py with the given input. Return (printed lines, error text)."""
    result = subprocess.run(
        [sys.executable, str(PROGRAM)],
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    if result.returncode != 0:
        return None, result.stderr
    printed = result.stdout
    for prompt in PROMPTS:
        printed = printed.replace(prompt, "")
    return printed.splitlines(), None


# Calling one function. Card.py ends with main(), which reads input, so the
# function is called from a copy of Card.py with that last call left out. The
# copy runs in a separate Python process, with no input available.
FUNCTION_RUNNER = r"""
import ast, contextlib, io, json, sys
path, name, args_json = sys.argv[1], sys.argv[2], sys.argv[3]
source = open(path, encoding="utf-8").read()
tree = ast.parse(source, filename=path)
tree.body = [
    node for node in tree.body
    if not (isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "main")
]
namespace = {"__name__": "card_under_test"}
exec(compile(tree, path, "exec"), namespace)
args = json.loads(args_json)
if name == "transaction_history":
    args[0] = [tuple(record) for record in args[0]]
output = io.StringIO()
with contextlib.redirect_stdout(output):
    value = namespace[name](*args)
answer = {"repr": repr(value), "value": value} if isinstance(value, (bool, int, float, type(None))) else {"repr": repr(value), "value": None, "odd": True}
answer.update({"stdout": output.getvalue(), "args_after": args})
print(json.dumps(answer))
"""


def call_function(name, args):
    """Call one of the given functions in Card.py. Return (value, repr, error)."""
    result = subprocess.run(
        [sys.executable, "-c", FUNCTION_RUNNER, str(PROGRAM), name, json.dumps(args)],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    if result.returncode != 0:
        return None, None, result.stderr
    lines = result.stdout.strip().splitlines()
    if not lines:
        return None, None, "the call printed nothing back"
    try:
        answer = json.loads(lines[-1])
    except ValueError:
        return None, None, "could not read the result:\n" + result.stdout
    if answer.get("odd"):
        return object(), answer["repr"], None
    return answer["value"], answer["repr"], None


# ---- Reading tests.txt ----

class TestsFileError(Exception):
    pass


def parse_function_check(line):
    """Turn 'ride_fare(1, 12, False) == 12' into ('ride_fare', [1, 12, False], 12)."""
    try:
        tree = ast.parse(line, mode="eval")
    except SyntaxError:
        raise TestsFileError("this is not a valid Python expression")
    expr = tree.body
    if not (isinstance(expr, ast.Compare)
            and len(expr.ops) == 1
            and isinstance(expr.ops[0], ast.Eq)):
        raise TestsFileError("a function check must be a call, then ==, then the expected value")
    call = expr.left
    if not (isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id in CHECKABLE
            and not call.keywords):
        raise TestsFileError(
            "the left side must call one of " + ", ".join(CHECKABLE)
            + ", with plain values in the brackets"
        )
    try:
        args = [ast.literal_eval(arg) for arg in call.args]
        expected = ast.literal_eval(expr.comparators[0])
    except ValueError:
        raise TestsFileError("use plain numbers, True or False, not variables or sums")
    return call.func.id, args, expected


def is_int_line(text):
    text = text.strip()
    if text.startswith("-"):
        text = text[1:]
    return text.isdigit()


def parse_program_case(block):
    """Split a block of lines into (input text, expected output lines)."""
    split = 0
    while split < len(block) and is_int_line(block[split]):
        split += 1
    inputs, outputs = block[:split], block[split:]
    if not inputs:
        raise TestsFileError("the case has no input lines (one whole number per line)")
    if not outputs:
        raise TestsFileError("the case has no expected output after its input")
    if inputs[-1].strip() != "0":
        raise TestsFileError("the input must end with 0")
    return "\n".join(line.strip() for line in inputs) + "\n", [line.rstrip() for line in outputs]


def read_tests_file():
    """Return (function checks, program cases, problems), each with its line number."""
    if not TESTS_FILE.exists():
        return [], [], [(0, "tests.txt not found next to test.py")]
    lines = TESTS_FILE.read_text(encoding="utf-8").splitlines()
    section = None
    checks, cases, problems = [], [], []
    block, block_start = [], 0

    def close_block():
        if block:
            try:
                cases.append((block_start, parse_program_case(block)))
            except TestsFileError as error:
                problems.append((block_start, str(error)))

    for number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if line.lower() == "# function checks":
            close_block()
            block = []
            section = "functions"
            continue
        if line.lower() == "# program cases":
            close_block()
            block = []
            section = "programs"
            continue
        if section == "functions":
            if not line:
                continue
            try:
                checks.append((number, line, parse_function_check(line)))
            except TestsFileError as error:
                problems.append((number, str(error)))
        elif section == "programs":
            if not line:
                close_block()
                block = []
                continue
            if not block:
                block_start = number
            block.append(raw)
        elif line:
            problems.append((number, "this line is above both section headings"))
    close_block()
    if section is None:
        problems.append((0, 'tests.txt needs the lines "# Function checks" and "# Program cases"'))
    return checks, cases, problems


# ---- The checks ----

class GivenFunctionTests(unittest.TestCase):
    def test_given_functions_unchanged(self):
        if not PROGRAM.exists():
            self.fail(f"Card.py not found next to test.py (looked at {PROGRAM})")
        try:
            tree = ast.parse(PROGRAM.read_text(encoding="utf-8"))
        except SyntaxError as error:
            self.fail(f"Card.py is not valid Python: {error}")
        definitions = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        self.assertEqual(
            len(definitions), len(GIVEN_FUNCTIONS),
            "Define only the five supplied functions. Do not add helper functions, nested functions or duplicate definitions",
        )
        found = {
            node.name: [arg.arg for arg in node.args.args]
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }
        for name, params in GIVEN_FUNCTIONS.items():
            with self.subTest(function=name):
                self.assertIn(name, found, f"{name}() is missing from Card.py. Do not rename the given functions")
                self.assertEqual(
                    found[name], params,
                    f"{name}() must keep its parameters exactly: {name}({', '.join(params)})",
                )


class TransactionHistoryTests(unittest.TestCase):
    def check_history(self, records, expected_lines):
        result = subprocess.run(
            [sys.executable, "-c", FUNCTION_RUNNER, str(PROGRAM),
             "transaction_history", json.dumps([records])],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=TIMEOUT,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        try:
            answer = json.loads(result.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            self.fail("Could not read transaction_history's result: " + result.stdout)
        self.assertEqual(answer["stdout"], "".join(line + "\n" for line in expected_lines))
        self.assertEqual(answer["repr"], "None", "transaction_history must return nothing")
        self.assertEqual(answer["args_after"], [records], "Do not change the supplied history")

    def test_empty_history(self):
        self.check_history([], [])

    def test_single_record(self):
        self.check_history([[1, True, -20]], ["1: Ride accepted. Balance: -20.00"])

    def test_all_kinds_and_outcomes_in_order(self):
        self.check_history(
            [[1, True, 14], [2, False, 14], [1, False, 14], [2, True, 64]],
            ["1: Ride accepted. Balance: 14.00", "2: Top-up refused. Balance: 14.00",
             "3: Ride refused. Balance: 14.00", "4: Top-up accepted. Balance: 64.00"],
        )

    def test_fractional_and_zero_balances(self):
        self.check_history([[1, True, 0.5], [1, True, 0]],
                           ["1: Ride accepted. Balance: 0.50", "2: Ride accepted. Balance: 0.00"])


class WorkedExampleTests(unittest.TestCase):
    def check(self, stdin_text, expected_lines):
        if not PROGRAM.exists():
            self.fail(f"Card.py not found next to test.py (looked at {PROGRAM})")
        printed, error = run_program(stdin_text)
        if printed is None:
            self.fail("Card.py crashed before finishing.\nstderr was:\n" + error)
        if not printed:
            self.fail("Card.py printed nothing. Is main() still empty?")
        self.assertEqual(
            printed,
            expected_lines,
            "Output did not match exactly (labels, spaces, decimals and line order count)",
        )

    def test_example_1_student_interchange_broken_by_top_up(self):
        self.check(EXAMPLE_1_INPUT, EXAMPLE_1_OUTPUT)

    def test_example_2_adult_refusals(self):
        self.check(EXAMPLE_2_INPUT, EXAMPLE_2_OUTPUT)

    def test_no_transactions(self):
        self.check("1\n20\n0\n", ["Card type: adult", "Rides taken: 0", "Top-ups: 0",
                   "Fares paid: 0.00", "Lowest balance: 20.00", "Final balance: 20.00", "Refused: 0"])

    def test_example_3_elder(self):
        self.check(EXAMPLE_3_INPUT, EXAMPLE_3_OUTPUT)


class YourTestsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checks, cls.cases, cls.problems = read_tests_file()

    def test_tests_file_layout(self):
        for line_number, message in self.problems:
            where = f"line {line_number}" if line_number else "tests.txt"
            with self.subTest(where=where):
                self.fail(f"tests.txt, {where}: {message}")
        if len(self.checks) > MAX_FUNCTION_CHECKS:
            self.fail(f"tests.txt has {len(self.checks)} function checks; the brief allows up to {MAX_FUNCTION_CHECKS}")
        if len(self.cases) > MAX_PROGRAM_CASES:
            self.fail(f"tests.txt has {len(self.cases)} program cases; the brief allows up to {MAX_PROGRAM_CASES}")

    def test_your_function_checks(self):
        if not self.checks:
            self.skipTest("no function checks in tests.txt yet")
        for line_number, text, (name, args, expected) in self.checks:
            with self.subTest(line=line_number, check=text):
                value, shown, error = call_function(name, args)
                if error is not None:
                    self.fail(f"tests.txt line {line_number}: {text}\n{name}() crashed:\n{error}")
                if not value == expected:
                    self.fail(
                        f"tests.txt line {line_number}: {text}\n"
                        f"{name}() returned {shown}, you expected {expected!r}"
                    )

    def test_your_program_cases(self):
        if not self.cases:
            self.skipTest("no program cases in tests.txt yet")
        for line_number, (stdin_text, expected_lines) in self.cases:
            with self.subTest(case_starting_at_line=line_number):
                printed, error = run_program(stdin_text)
                if printed is None:
                    self.fail(f"tests.txt case at line {line_number}: Card.py crashed.\nstderr was:\n{error}")
                self.assertEqual(
                    printed,
                    expected_lines,
                    f"tests.txt case at line {line_number}: output did not match your expected output",
                )


if __name__ == "__main__":
    unittest.main()
