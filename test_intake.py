# test_intake.py — Week 6: proof the parser works
# Run it with:  pytest test_intake.py

# pytest is the testing tool. I need it here for pytest.raises() below.
import pytest

# Pull in the one function I'm testing from my other file. Note I import
# parse_row only — the tests don't care about the file loading at all.
from intake_safe import parse_row


# pytest finds tests by name: any function starting with "test_" gets run.
# The name is the report — when it fails, this sentence is what you read.
def test_good_row_parses():
    """A clean row comes back as a dict with converted, tidied fields."""
    # A row I can check by eye: age "36" as text, name in sloppy lowercase
    # with padding spaces.
    row = ["CC-1", " carter, d ", "m", "36", "2018-03-22", "412 larkmoor", "352", "open"]
    # Call the real function.
    case = parse_row(row)
    # "assert" means: this must be true, or fail the test.
    # The text "36" must have become the NUMBER 36 — note no quotes.
    assert case["age"] == 36
    # And the name must have been stripped and title-cased.
    assert case["name"] == "Carter, D"


# Bad-row test number one. Each test gets its own fresh "row" variable —
# a variable made inside one function doesn't exist in any other, so I can't
# reuse the one from the test above.
def test_bad_age_rejected():
    """A row with age 'unknown' must be refused, not guessed at."""
    # Same row, but position 3 is the word 'unknown' instead of a number.
    row = ["CC-1", " carter, d ", "m", "unknown", "2018-03-22", "412 larkmoor", "352", "open"]
    # This flips the test upside down: instead of checking the answer, I'm
    # checking that it REFUSES. pytest.raises passes only if the code inside
    # raises that error — and fails if the code quietly succeeds.
    with pytest.raises(ValueError):
        # No "assert" needed. The pytest.raises above is doing the checking,
        # and the only job of this line is to trigger the error.
        parse_row(row)


# Bad-row test number two, covering the third trap in parse_row.
def test_missing_date_rejected():
    """A row with an empty date must be refused."""
    # Position 4 is the date, left blank here. Note the age is a valid "36",
    # so the ONLY thing wrong with this row is the date — that's what makes
    # the test prove the date check specifically, and not something else.
    row = ["CC-1", " carter, d ", "m", "36", "", "412 larkmoor", "352", "open"]
    # Same upside-down check: this passes only if parse_row raises.
    with pytest.raises(ValueError):
        # The call that should blow up.
        parse_row(row)
