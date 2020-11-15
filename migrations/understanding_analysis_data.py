import common
import db

connection = db.get_connection()

sections = {
    common.ABBOTT_UA: {
        1: list(range(2,7)),
        2: list(range(2,9)),
        3: list(range(2,6)),
        4: list(range(2,7)),
        5: list(range(2,5)),
        6: list(range(2,8)),
        7: list(range(2,7)),
        8: list(range(2,7)),
    },
}

section_values = []
for book_id, divisions in sections.items():
    for chapter, sections in divisions.items():
        for section in sections:
            section_values.append((book_id, chapter, section))

with connection:
    connection.executemany(
        'INSERT INTO book_sections (book_id, chapter, section) VALUES (?,?,?)',
        section_values
    )
