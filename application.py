# -*- coding: utf-8 -*-
import webapp2
from handlers import WebHookFacebookHandler

config = {}

app = webapp2.WSGIApplication([
    ('/web_hook/facebook', WebHookFacebookHandler),
    ], config=config, debug=True)
