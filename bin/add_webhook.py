import requests
import json

import common

def main():
    url = f"https://api.trello.com/1/webhooks/?{common.TRELLO_AUTH_STRING}"

    query = {
       'callbackURL': 'http://8a1e38d3.ngrok.io/process_card_update/notes/5e8d97e2064b3c5f05e1b910',
       'idModel': '5e8d97e2064b3c5f05e1b910'
    }

    response = requests.post(url, params=query)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


if __name__ == '__main__':
    main()
