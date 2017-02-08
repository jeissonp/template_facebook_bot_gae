# -*- coding: utf-8 -*-
import webapp2
import logging
import json

from google.appengine.api import urlfetch

VERIFY_TOKEN = 'wxyz'

PAGE_ACCESS_TOKEN = 'abcd'

URL_FB = 'https://graph.facebook.com/v2.6/me/messages?access_token={access_token}'

class WebHookFacebookHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('hub.verify_token') == VERIFY_TOKEN:
            self.response.write(self.request.get('hub.challenge'))
        else:
            self.abort(403)

    def post(self):
        #  See: https://developers.facebook.com/docs/messenger-platform/webhook-reference
        data = json.loads(self.request.body)
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:
                    # someone sent us a message

                    # delivery confirmation
                    if messaging_event.get('delivery'):
                        pass

                    # optin confirmation
                    if messaging_event.get('optin'):
                        pass

                    # user clicked/tapped "postback" button in earlier message
                    if messaging_event.get('postback'):
                        pass

                    if messaging_event.get("message"):
                        # the facebook ID of the person sending you the message
                        sender_id = messaging_event['sender']['id']
                        self.send_message(sender_id, 'message')
        else:
            self.abort(403)

    def send_message(self, recipient_id, text):
        headers = {
            'Content-Type': 'application/json',
        }

        data = json.dumps({
            'recipient': {
                'id': recipient_id,
            },
            'message': {
                'text': text
            }
        })

        result = urlfetch.Fetch(url=URL_FB.format(access_token=PAGE_ACCESS_TOKEN), payload=data, method=urlfetch.POST, headers=headers)

        if result.status_code != 200:
            logging.info(data)
            logging.error(result.content)
        else:
            pass