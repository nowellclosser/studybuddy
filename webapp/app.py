import logging

import bottle

import common

@bottle.get('/')
def home():
    return '<b>Studybuddy api running</b>!'

@bottle.get('/fake-news-by-nowell')
def fake_page():
    return static_file('fake_page.html', root='static')

# For Trello to validate our callback URL
@bottle.get('/process_card_update/<card_type>/<card_id>')
def process_card_update(card_type, card_id):
    return 'Valid card update url'

@bottle.post('/process_card_update/<card_type>/<card_id>')
def process_card_update(card_type, card_id):
    action_data = bottle.request.json["action"]
    if (action_data["type"] == "updateCard" and
            action_data["data"].get("listBefore") and
            action_data["data"].get("listBefore") != action_data["data"].get("listAfter") and
            action_data["data"]["listAfter"]["id"] == common.DONE_LIST_ID):
        common.mark_task_completed(card_type, card_id)

if __name__ == "__main__":
    bottle.run(host='localhost', port=8000)
else:
    app = bottle.default_app()


