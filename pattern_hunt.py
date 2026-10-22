# pattern_hunt.py — Week 5: Pattern Hunters
# Mines 24 free-text tips for phones, dates, case refs, and beats.

# Loads Python's regular-expression toolkit. The only thing I use out of it is
# re.findall(pattern, text), which returns a LIST of every match it finds.
# Found nothing at all? It hands back an empty list [].
import re


# "def" creates a function. "extract_phones" is the name I'll call it by.
# "text" in the parentheses is the PARAMETER — a placeholder for whatever
# string gets handed in at the moment the function is called.
def extract_phones(text):
    # Triple quotes on the first line inside a def make a DOCSTRING: one
    # sentence saying what this tool does. Slide 13 grades every extractor
    # for having one.
    """Every phone number in the text, both (214) 555-1234 and 214-555-1234."""
    # The r before the quote marks makes it a "raw string" — it tells Python to
    # leave the backslashes alone instead of reading them as escape codes.
    #
    # The | in the middle means OR, so this is really TWO patterns, and findall
    # takes whichever one fits. Sounding each out, left to right:
    #
    #   \(\d{3}\) \d{3}-\d{4}      the parenthesised format
    #     \(        a literal (     (the \ means a real paren, not regex magic)
    #     \d{3}     three digits    -> 214
    #     \)        a literal )
    #     (space)   one space
    #     \d{3}     three digits    -> 555
    #     -         a literal dash
    #     \d{4}     four digits     -> 1234
    #
    #   \d{3}-\d{3}-\d{4}          the all-dashes format -> 214-555-1234
    #
    # Why not one pattern with "maybe a paren" on each end, like \(?...\)? ?
    # Because the tips wrap numbers in sentence punctuation: "Witness
    # (784-550-8605) reports...". The optional-paren version grabs that opening
    # paren, then finds no closing one before the digits, and hands back
    # '(784-550-8605' with an unbalanced bracket. Demanding the parens come as
    # a matched pair — or not at all — is what keeps the output clean.
    # "return" hands the list back out to whoever called this function.
    return re.findall(r"\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4}", text)


# Second tool. Same shape as the first: one name, one parameter, one job.
def extract_case_refs(text):
    """Every case reference, like CC-14589."""
    # 'CC-' isn't regex magic, it's literal text — those exact characters.
    # Then \d{5} means exactly five digits after it.
    return re.findall(r"CC-\d{5}", text)


# Third tool.
def extract_beats(text):
    """Every beat number mentioned, like 341."""
    # [Bb] means one character from the set B or b, so this matches the word
    # whether the tip wrote "Beat" or "beat".
    # The parentheses around (\d{3}) are a CAPTURE GROUP. When a pattern has a
    # group, findall returns ONLY what's inside it — so I get '341' back,
    # not 'beat 341'. Drop the parens and the word comes along for the ride.
    return re.findall(r"[Bb]eat (\d{3})", text)


# Fourth tool.
def extract_iso_dates(text):
    """Every ISO-style date, like 2019-02-19."""
    # Four digits, a dash, two digits, a dash, two digits. Year-month-day.
    return re.findall(r"\d{4}-\d{2}-\d{2}", text)


# Fifth tool.
def extract_us_dates(text):
    """Every slash-style date, like 4/7/2019."""
    # {3} means EXACTLY three. {1,2} means one OR two, which matters here
    # because the tips write both "4/7/2019" and "7/20/2024" — single-digit
    # and double-digit months and days. Hard-code {2} and you'd miss half.
    return re.findall(r"\d{1,2}/\d{1,2}/\d{4}", text)


# This one takes TWO parameters, and does no regex of its own — it just calls
# the five tools above and arranges what they hand back. Small tools composing
# into a bigger one, instead of one giant extract_everything().
def summarize_tip(i, text):
    """One formatted summary line for a single tip."""
    # Call the phone tool. Whatever it returns gets stored in "phones" —
    # either a list of numbers, or an empty list [].
    phones = extract_phones(text)
    # Same for case refs.
    refs = extract_case_refs(text)
    # Same for beats.
    beats = extract_beats(text)
    # Call BOTH date tools and glue the results together. Adding two lists
    # with + joins them end to end into one list.
    dates = extract_iso_dates(text) + extract_us_dates(text)
    # Build the output line. The f lets me drop values into the text using
    # {curly braces}. This function doesn't print — it RETURNS the string and
    # lets the caller decide what to do with it.
    return f"TIP {i}: phone={phones} date={dates} case={refs} beat={beats}"


# open() finds and opens the file. .readlines() reads the whole thing and hands
# back a LIST of strings, one per line. 24 lines in the file = 24 items here.
tips = open("data/wk05_data_tipline.txt").readlines()

# A counter, starting at zero. It lives OUT here, before the loop — put it
# inside and it would reset to 0 on every tip, ending up at 1 or 0.
with_callback = 0

# A plain "for tip in tips:" would give me the tip only. enumerate() hands back
# TWO things each pass: a running number and the item. start=1 makes it count
# 1, 2, 3 instead of Python's usual 0, 1, 2.
for i, tip in enumerate(tips, start=1):
    # summarize_tip returns a string; print() puts it on the screen.
    # Runs once per tip, so this prints 24 lines.
    print(summarize_tip(i, tip))
    # Call the phone tool again, this time just to ask "did it find anything?"
    # In an if, Python treats an empty list [] as False and a list with
    # anything in it as True. So this reads: "if any phone was found".
    if extract_phones(tip):
        # += 1 means: take the current value, add one, store it back.
        with_callback += 1

# print() with nothing inside prints one blank line, to separate the report.
print()
# len() counts the items in the list — 24, with no loop needed.
print(f"Tips processed:       {len(tips)}")
# The counter the loop built up.
print(f"Tips with a callback: {with_callback}")
# No second counter needed: every tip is either one or the other, so the ones
# without a callback are just the total minus the ones with.
print(f"Tips with NO callback: {len(tips) - with_callback}  <- these leads die without follow-up")
