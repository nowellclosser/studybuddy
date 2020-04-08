
import common
import db

connection = db.get_connection()

drop = """
DROP TABLE IF EXISTS book_sections;
"""
connection.execute(drop)

create = """
CREATE TABLE IF NOT EXISTS book_sections (
    book TEXT NOT NULL,
    chapter INT NOT NULL,
    section INT,
    scheduled BOOLEAN DEFAULT 0,
    reading_completed BOOLEAN DEFAULT 0,
    notes_completed BOOLEAN DEFAULT 0,
    exercises_completed BOOLEAN DEFAULT 0,
    exclude_from_review BOOLEAN DEFAULT 0,
    PRIMARY KEY(book, chapter, section)
);
"""

connection.execute(create)

sections = {
    common.LA_STRANG: {
        1: list(range(1,4)),
        2: list(range(1,8)),
        3: list(range(1,6)),
        4: list(range(1,5)),
        5: list(range(1,4)),
        6: list(range(1,6)),
        7: list(range(1,5)),
        8: list(range(1,4)),
        9: list(range(1,4)),
        10: list(range(1,8)),
        11: list(range(1,4)),
        12: list(range(1,4)),

    },
    common.AA_PINTER: {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
        11: None,
        12: None,
        13: None,
        14: None,
        15: None,
        16: None,
        17: None,
        18: None,
        19: None,
        20: None,
        21: None,
        22: None,
        23: None,
        24: None,
        25: None,
        26: None,
        27: None,
        28: None,
        29: None,
        30: None,
        31: None,
        32: None,
        33: None,
    }
}

section_values = []
for book, divisions in sections.items():
    for chapter, sections in divisions.items():
        if sections:
            for section in sections:
                section_values.append((book, chapter, section))
        else:
            section_values.append((book, chapter, None))

with connection:
    connection.executemany(
        'INSERT INTO book_sections (book, chapter, section) VALUES (?,?,?)',
        section_values
    )

update_strang = f"""
UPDATE book_sections
SET reading_completed=1,
    notes_completed=1,
    exercises_completed=1,
    scheduled=1
WHERE book = '{common.LA_STRANG}' AND chapter <= 6
"""

update_pinter_read = f"""
UPDATE book_sections
SET reading_completed=1
WHERE book = '{common.AA_PINTER}' AND chapter <= 13
"""

update_pinter_exercises = f"""
UPDATE book_sections
SET exercises_completed=1
WHERE book = '{common.AA_PINTER}' AND chapter <= 12
"""

update_pinter_notes = f"""
UPDATE book_sections
SET notes_completed=1,
    scheduled=1
WHERE book = '{common.AA_PINTER}' AND chapter <= 9
"""
with connection:
    connection.execute(update_strang)
    connection.execute(update_pinter_read)
    connection.execute(update_pinter_exercises)
    connection.execute(update_pinter_notes)

connection.close()
