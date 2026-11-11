# Jasreet — Week 5: Pattern Hunters
# 24 tips written as plain sentences. There is no | to split on this week,
# so instead I describe the SHAPE of what I want and let regex go find it.

import re                              # bring in the regex tool so I can search by shape


# ---- The extractors: one function, one pattern, one job ----

def extract_phones(text):              # make a tool called extract_phones that takes some text
    """Find phone numbers like (214) 555-1234 and 214-555-1234."""   # one line saying what it does
    # \(? maybe a (   \d{3} three digits   \)? maybe a )   [ -] a space or a dash
    return re.findall(r"\(?\d{3}\)?[ -]\d{3}-\d{4}", text)   # search the text, hand back a list of phones


def extract_case_refs(text):            # make a tool that takes some text
    """Find case references like CC-14589."""
    # CC- is plain text to match exactly, then \d{5} is five digits
    return re.findall(r"CC-\d{5}", text)        # hand back a list of case refs, or [] if none


def extract_beats(text):                # make a tool that takes some text
    """Find the beat number from 'beat 341' or 'Beat 341'."""
    # [Bb] = a big B or a small b. The ( ) says keep ONLY that part.
    return re.findall(r"[Bb]eat (\d{3})", text)   # hand back just the numbers, like ['341']


def extract_iso_dates(text):            # make a tool that takes some text
    """Find dates written as 2019-02-19."""
    # \d{4} four digits, a dash, \d{2} two digits, a dash, \d{2} two digits
    return re.findall(r"\d{4}-\d{2}-\d{2}", text)   # hand back a list of dash dates


def extract_us_dates(text):             # make a tool that takes some text
    """Find dates written as 4/7/2019."""
    # \d{1,2} means one OR two digits, so 4/7 and 12/25 both work
    return re.findall(r"\d{1,2}/\d{1,2}/\d{4}", text)   # hand back a list of slash dates


def summarize_tip(number, text):        # make a tool that takes a tip number AND the tip
    """Build one summary line for a single tip."""
    phones = extract_phones(text)       # run my phone tool, keep the list it gives back
    refs = extract_case_refs(text)      # run my case ref tool, keep that list
    beats = extract_beats(text)         # run my beat tool, keep that list
    dates = extract_iso_dates(text) + extract_us_dates(text)   # run both date tools, join the lists
    return f"TIP {number}: phone={phones} date={dates} case={refs} beat={beats}"   # hand back one line of text


# ---- Read the tips into a list ----

tips = []                              # make an empty list to hold the tips

with open("data/wk05_data_tipline.txt") as tip_file:   # open the tip file and call it tip_file
    for line in tip_file:              # take the lines one at a time, call each one "line"
        tips.append(line.strip())      # cut off the newline, then add the tip to my list

# ---- One line per tip, then the callback count ----

with_callback = 0                      # start a counter at zero, before the loop

print("TIP LINE EXTRACTION")           # print a heading

for i, tip in enumerate(tips, start=1):   # go through the tips, counting from 1, number is i
    print(summarize_tip(i, tip))       # build this tip's summary line and print it
    if extract_phones(tip):            # if the phone list came back with something in it
        with_callback += 1             # add 1 to the counter

print()                                # print a blank line

print(f"{'Tips processed:':<23}{len(tips)}")              # print the label, then how many tips
print(f"{'Tips with a callback:':<23}{with_callback}")    # print the label, then the counter
print(f"{'Tips with NO callback:':<23}{len(tips) - with_callback}  <- these leads die without follow-up")   # 24 take away 15
