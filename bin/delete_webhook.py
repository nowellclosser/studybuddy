import json
import sys

import requests

import common

def main(webhook_id):
    url = f"https://api.trello.com/1/webhooks/{webhook_id}?{common.TRELLO_AUTH_STRING}"

    response = requests.delete(url)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


if __name__ == '__main__':
    main(sys.argv[1])
