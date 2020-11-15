
import common
import db

connection = db.get_connection()

update_pinter_read = f"""
UPDATE book_sections
SET reading_completed=1
WHERE book_id = '{common.PINTER_AA}' AND chapter <= 29
"""

update_pinter_exercises = f"""
UPDATE book_sections
SET exercises_completed=1
WHERE book_id = '{common.PINTER_AA}' AND chapter <= 26
"""

update_pinter_notes = f"""
UPDATE book_sections
SET notes_completed=1,
    scheduled=1
WHERE book_id = '{common.PINTER_AA}' AND chapter <= 26
"""

with connection:
    connection.execute(update_pinter_read)
    connection.execute(update_pinter_exercises)
    connection.execute(update_pinter_notes)

connection.close()
