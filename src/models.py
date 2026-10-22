# src/models.py — Week 7: the Case class (slides 4–6), placed in src/ for week 8
# A dict is a bag of facts. A class is facts + the questions you ask of them.


# "class" makes a new type, the same way str and list are types. Case is the
# blueprint; each actual case built from it is one object.
class Case:
    """One case file: its facts, plus the questions it can answer about itself."""

    # __init__ runs automatically the moment a Case is created — the booking.
    # "self" is "this particular case"; Python hands it in for me.
    def __init__(self, case_id, name, age, year, status):
        # self.case_id = case_id copies the value onto THIS case, so it sticks
        # around after __init__ ends. A plain "case_id" would vanish.
        self.case_id = case_id
        # Same move for each fact: store it on the object.
        self.name = name
        # An int, so math works on it later.
        self.age = age
        # The year the case opened, also an int — years_unsolved does math on it.
        self.year = year
        # 'OPEN' or 'CLOSED', already uppercased by from_row.
        self.status = status

    # @property lets me ask c.years_unsolved with NO parentheses, like a fact,
    # even though it's calculated fresh each time it's asked.
    @property
    def years_unsolved(self):
        """How many years since the case opened."""
        # Same subtraction as week 2's intake script, now living in one place.
        return 2026 - self.year

    # The 5-year rule lives HERE and nowhere else. Change the 5 once and every
    # report that asks c.is_stale updates with it.
    @property
    def is_stale(self):
        """True if the case is still open and 5 or more years old."""
        # "and" needs BOTH sides true. A closed case is never stale, however old.
        # The outer parentheses just let the expression wrap onto two lines.
        return (self.status == "OPEN"
                and self.years_unsolved >= 5)

    # @classmethod means this is called on the CLASS, not on one case:
    # Case.from_row(row). "cls" is Case itself, so cls(...) builds a new Case.
    # This is week 6's parse_row, turned into a constructor.
    @classmethod
    def from_row(cls, row):
        """One CSV row in, one Case out. Raises ValueError if the row is damaged."""
        # Truncated rows: check the length FIRST, before reaching for row[7].
        if len(row) != 8:
            # Raise on purpose, with a reason, so the quarantine log can say why.
            raise ValueError("truncated")
        # int('unknown') raises ValueError all by itself — no check needed.
        age = int(row[3])
        # cls(...) calls __init__ with these five values, in __init__'s order.
        # row[4][0:4] slices the first 4 characters of '2018-03-22' -> '2018',
        # and int() makes it 2018. An empty date gives int('') -> ValueError.
        return cls(row[0].strip(),
                   row[1].strip().title(),
                   age, int(row[4][0:4]),
                   row[7].strip().upper())
