import argparse
import json

import arrow
import requests

import common

def add_webhook(card_type, card_id):
    url = f"https://api.trello.com/1/webhooks/?{common.TRELLO_AUTH_STRING}"

    query = {
       'callbackURL': f'http://pizzanet.sexy/process_card_update/{card_type}/{card_id}',
       'idModel': card_id
    }
    response = requests.post(url, params=query)
    if response.status_code != 200:
        raise Exception(response.text)


def schedule_range(
        book_id,
        start_chapter,
        end_chapter,
        start_section,
        end_section,
        start_date,
        reading_cadence_days,
        exercises_lag_days,
        notes_lag_days,
        clear_previous
):
    start_date = start_date.replace(hour=23, minute=59)

    put_url_template = f'https://api.trello.com/1/cards/{{id}}/?{common.TRELLO_AUTH_STRING}'
    post_url = f'https://api.trello.com/1/cards/?{common.TRELLO_AUTH_STRING}'
    delete_url = f'https://api.trello.com/1/cards/{{id}}/?{common.TRELLO_AUTH_STRING}'

    adjusted_cadence_days = reading_cadence_days - 1
    adjusted_exercises_lag_days = max(exercises_lag_days - 1, 0)
    adjusted_notes_lag_days = max(notes_lag_days - 1, 0)

    reading_task_count = 0
    days_with_reading_already_done = 0
    first_reading_task_scheduled = False
    for section in common.get_section_range(book_id, start_chapter, start_section, end_chapter, end_section):
        name = common.book_division_name(
            section['book_id'],
            section['chapter'],
            section['section']
        )

        should_increment_reading_task_count = False

        shift_base = (
            days_with_reading_already_done * adjusted_cadence_days +
            (reading_task_count - days_with_reading_already_done) * reading_cadence_days
        )

        # Upsert reading task
        if not section[f'{common.READING}_completed']:
            if not first_reading_task_scheduled:
                first_reading_task_scheduled = True

            should_increment_reading_task_count = True
            card_id = section[f'{common.READING}_card_id']

            if clear_previous and card_id:
                requests.delete(delete_url.format(id=card_id))
                common.update_section_card_id(book_id, section['chapter'], section['section'], common.READING, None)

            query = {
                'due': start_date.shift(days=shift_base)
            }

            if card_id and not clear_previous:
                requests.put(put_url_template.format(id=card_id), params=query)
            else:
                query['idList'] = common.TO_DO_LIST_ID
                query['name'] = f'Read {name}'
                card = requests.post(post_url, params=query).json()

                common.update_section_card_id(book_id, section['chapter'], section['section'], common.READING, card['id'])

            add_webhook(common.READING, card['id'])

        # Upsert exercises task
        if not section[f'{common.EXERCISES}_completed']:
            should_increment_reading_task_count = True
            card_id = section[f'{common.EXERCISES}_card_id']

            if clear_previous and card_id:
                requests.delete(delete_url.format(id=card_id))
                common.update_section_card_id(book_id, section['chapter'], section['section'], common.EXERCISES, None)
            card_id = section[f'{common.EXERCISES}_card_id']

            lag_days = exercises_lag_days
            if section[f'{common.READING}_completed']:
                lag_days = adjusted_exercises_lag_days

            query = {
                'due': start_date.shift(days=(shift_base + lag_days))
            }

            if card_id and not clear_previous:
                requests.put(put_url_template.format(id=card_id), params=query)
            else:
                query['idList'] = common.TO_DO_LIST_ID
                query['name'] = f'Do exercises for {name}'
                card =requests.post(post_url, params=query).json()

                common.update_section_card_id(book_id, section['chapter'], section['section'], common.EXERCISES, card['id'])

            add_webhook(common.EXERCISES, card['id'])

        # Upsert notes task
        if not section[f'{common.NOTES}_completed']:
            should_increment_reading_task_count = True
            card_id = section[f'{common.NOTES}_card_id']
            if clear_previous and card_id:
                requests.delete(delete_url.format(id=card_id))
                common.update_section_card_id(book_id, section['chapter'], section['section'], common.NOTES, None)
            card_id = section[f'{common.NOTES}_card_id']


            lag_days = notes_lag_days
            if section[f'{common.READING}_completed']:
                lag_days = adjusted_notes_lag_days
            query = {
                'due': start_date.shift(days=(shift_base + lag_days))
            }

            if card_id and not clear_previous:
                requests.put(put_url_template.format(id=card_id), params=query)
            else:
                query['idList'] = common.TO_DO_LIST_ID
                query['name'] = f'Write notes for {name}'
                card = requests.post(post_url, params=query).json()

                common.update_section_card_id(book_id, section['chapter'], section['section'], common.NOTES, card['id'])
            add_webhook(common.NOTES, card['id'])

        if should_increment_reading_task_count:
            reading_task_count += 1
            if not first_reading_task_scheduled:
                days_with_reading_already_done += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Specify a range of chapters or sections to schedule work for"
    )
    parser.add_argument('-b', '--book_id', choices=list(common.BOOKS.keys()), required=True)
    parser.add_argument('-s', '--start_chapter', type=int, required=True)
    parser.add_argument('-e', '--end_chapter', type=int, required=True)
    parser.add_argument('--reading_cadence_days', type=int, default=2)
    parser.add_argument('--exercises_lag_days', type=int, default=1)
    parser.add_argument('--notes_lag_days', type=int, default=1)
    parser.add_argument('--start_section', type=int, required=False, default=1)
    parser.add_argument('--end_section', type=int, required=False)
    parser.add_argument('--start_date', required=False)
    parser.add_argument('--clear_previous', action='store_true', default=True)

    args = parser.parse_args()

    schedule_range(
        args.book_id,
        args.start_chapter,
        args.end_chapter,
        args.start_section,
        args.end_section,
        arrow.get(args.start_date) if args.start_date else arrow.now(),
        args.reading_cadence_days,
        args.exercises_lag_days,
        args.notes_lag_days,
        args.clear_previous
    )


