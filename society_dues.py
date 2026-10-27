"""Manage apartment society maintenance dues and payments."""

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE dues "
    "(flat TEXT, month TEXT, amount INTEGER, paid INTEGER)"
)


def add_due(flat, month, amount, history=None):
    """Add a due entry and record it in the history."""
    if history is None:
        history = []

    conn.execute(
        "INSERT INTO dues VALUES (?, ?, ?, 0)",
        (flat, month, amount)
    )
    history.append((flat, month))
    return history


def collect(flat, month):
    """Mark a flat's monthly dues as paid and return the amount."""
    row = conn.execute(
        "SELECT amount FROM dues WHERE flat = ? AND month = ?",
        (flat, month)
    ).fetchone()

    if row:
        conn.execute(
            "UPDATE dues SET paid = 1 WHERE flat = ? AND month = ?",
            (flat, month)
        )
        return row[0]

    return None


def penalty(amount, multiplier):
    """Calculate the late fee using the supplied multiplier."""
    return amount * multiplier


def pending():
    """Return a list of flats with unpaid dues."""
    rows = conn.execute(
        "SELECT flat FROM dues WHERE paid = 0"
    ).fetchall()
    return [row[0] for row in rows]


def main():
    """Run a demonstration of the dues ledger."""
    add_due("A-101", "Oct", 2500)
    add_due("A-102", "Oct", 2500)
    print(collect("A-101", "Oct"))
    print(penalty(50, 2))
    print(pending())


if __name__ == "__main__":
    main()
