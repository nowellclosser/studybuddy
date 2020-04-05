import os

TRELLO_TOKEN = os.environ['TRELLO_TOKEN']
TRELLO_API_KEY = '05f785ea84a94d962177813ad467dba0'
TRELLO_AUTH_STRING = f'key={TRELLO_API_KEY}&token={TRELLO_TOKEN}'
STUDY_BOARD_ID = '5c9b032e34978643340a72aa'
TO_DO_LIST_ID = '5c9b032e6e6f3c185318da3c'

SECTIONS = {
    'Linear Algebra - Strang': {
        1: list(range(1,4)),
        2: list(range(1,8)),
        3: list(range(1,6)),
        4: list(range(1,5)),
        5: list(range(1,4)),
        6: list(range(1,6)),
    },
    'A Book of Abstract Algebra - Pinter': {
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
    }
}


def list_sections():
    result = []
    for book, divisions in SECTIONS.items():
        for chapter, sections in divisions.items():
            if sections:
                for section in sections:
                    result.append(f'{book}: Section {chapter}-{section}')
            else:
                result.append(f'{book}: Chapter {chapter}')
    return result
