import os

import db

TRELLO_TOKEN = os.environ['TRELLO_TOKEN']
TRELLO_API_KEY = '05f785ea84a94d962177813ad467dba0'
TRELLO_AUTH_STRING = f'key={TRELLO_API_KEY}&token={TRELLO_TOKEN}'
STUDY_BOARD_ID = '5c9b032e34978643340a72aa'
TO_DO_LIST_ID = '5c9b032e6e6f3c185318da3c'
DONE_LIST_ID = '5c9b032ef2f2f717ab525e9e'

STUDYBUDDY_DB = 'studybuddy.db'

STRANG_LA = 'strang_la'
PINTER_AA = 'pinter_aa'
BOOKS = {
    STRANG_LA: 'Linear Algebra - Strang',
    PINTER_AA: 'A Book of Abstract Algebra - Pinter'
}

READING = 'reading'
NOTES = 'notes'
EXERCISES = 'exercises'
study_card_types = [READING, NOTES, EXERCISES]


def get_book_section(book_id, chapter, section, fields=None):
    connection = db.get_connection()

    fetch = """
    SELECT * FROM book_sections
    WHERE book_id = :book_id
        AND chapter = :chapter
        AND (section IS NULL OR section = :section)
    """

    return connection.execute(
        fetch,
        {'book_id': book_id, 'chapter': chapter, 'section': section}
    ).fetchone()


def get_section_range(book_id, start_chapter, start_section, end_chapter, end_section):
    connection = db.get_connection()

    fetch = """
    SELECT * FROM book_sections
    WHERE book_id = :book_id
        AND ((chapter > :start_chapter AND chapter < :end_chapter)
            OR (chapter = :start_chapter AND COALESCE(section, 1000000) >= :start_section)
            OR (chapter = :end_chapter AND COALESCE(section, -1) <= :end_section))
    ORDER BY chapter, section
    """

    return connection.execute(
        fetch,
        {
            'book_id': book_id,
            'start_chapter': start_chapter,
            'start_section': start_section or 1,
            'end_chapter': end_chapter,
            'end_section': end_section or 1_000_000
        }
    ).fetchall()


def book_division_name(book_id, chapter, section):
    if section:
        return f'{BOOKS[book_id]}, Section {chapter}-{section}'
    return f'{BOOKS[book_id]}, Chapter {chapter}'


def list_sections_with_notes():
    connection = db.get_connection()

    fetch = """
    SELECT book_id, chapter, section
    FROM book_sections
    WHERE notes_completed = 1
        AND exclude_from_review = 0
    """

    return [
        book_division_name(row['book_id'], row['chapter'], row['section'])
        for row in connection.execute(fetch)
    ]


def update_section_card_id(book_id, chapter, section, card_type, id_value):
    connection = db.get_connection()

    update = f"""
    UPDATE book_sections
    SET {card_type}_card_id = :id
    WHERE book_id = :book_id
        AND chapter = :chapter
        AND (section IS NULL OR section = :section)
    """

    params = {
        'book_id': book_id,
        'chapter': chapter,
        'section': section,
        'id': id_value
    }
    connection.execute(update, params)
    connection.commit()


def mark_task_completed(task_type, card_id):
    connection = db.get_connection()

    update = f"""
    UPDATE book_sections
    SET {task_type}_completed = 1
    WHERE {task_type}_card_id = :card_id
    """

    params = {
        'card_id': card_id
    }
    connection.execute(update, params)
    connection.commit()


