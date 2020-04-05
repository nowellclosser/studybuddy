import random
from datetime import datetime, timezone

import arrow
import requests

import common


def main():
    url = f'https://api.trello.com/1/cards/?{common.TRELLO_AUTH_STRING}'
    query = {
        'idList': common.TO_DO_LIST_ID,
        'name': f'Review notes for {random.choice(common.list_sections())}',
        'due': arrow.now().replace(hour=23, minute=59)
    }

    result = requests.post(url, params=query)


if __name__ == '__main__':
    main()
