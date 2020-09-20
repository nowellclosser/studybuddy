
import common
import db

connection = db.get_connection()

elim_algebra_1 = f"""
UPDATE book_sections
SET exclude_from_review=1
WHERE book_id = '{common.PINTER_AA}' AND chapter = 1
"""

update_pinter_read = f"""
UPDATE book_sections
SET reading_completed=1
WHERE book_id = '{common.PINTER_AA}' AND chapter <= 25
"""

update_pinter_exercises = f"""
UPDATE book_sections
SET exercises_completed=1
WHERE book_id = '{common.PINTER_AA}' AND chapter <= 24
"""

update_pinter_notes = f"""
UPDATE book_sections
SET notes_completed=1,
    scheduled=1
WHERE book_id = '{common.PINTER_AA}' AND chapter <= 22
"""

with connection:
    connection.execute(elim_algebra_1)
    connection.execute(update_pinter_read)
    connection.execute(update_pinter_exercises)
    connection.execute(update_pinter_notes)

connection.close()
