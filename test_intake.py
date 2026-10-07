# Jasreet — Week 6: tests that prove the parser works
# Run it with:  python3 -m pytest test_intake.py

import pytest                         # pytest.raises lives in here
from intake_safe import parse_row     # import the tool I am testing


def test_good_row_parses():
    # A clean row should come back as a dict with converted fields.
    row = ["CC-1", " carter, d ", "m", "36",
           "2018-03-22", "412 larkmoor", "352", "open"]
    case = parse_row(row)
    # assert means: this must be true, or the test fails
    assert case["age"] == 36           # 36 the number, not "36" the text
    assert case["name"] == "Carter, D"  # stripped and title cased


def test_bad_age_rejected():
    # An age of "unknown" should raise ValueError, not crash the program.
    row = ["CC-1", " carter, d ", "m", "unknown",
           "2018-03-22", "412 larkmoor", "352", "open"]
    # This one is backwards: I EXPECT it to fail.
    # The test passes if parse_row raises, and fails if it quietly works.
    with pytest.raises(ValueError):
        parse_row(row)


def test_truncated_row_rejected():
    # A row missing its last two fields should raise ValueError.
    row = ["CC-1", " carter, d ", "m", "36",
           "2018-03-22", "412 larkmoor"]     # 6 fields, not 8
    with pytest.raises(ValueError):
        parse_row(row)
