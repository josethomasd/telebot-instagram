import StringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
#import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

#time
from datetime import datetime, timedelta
import pytz
import time


TOKEN = '351697767:AAFV5Y2RewXLLXGbcGohE7reo3O1-lb0LpU'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


class Users(ndb.Model):
    user_id = ndb.StringProperty()
    name = ndb.StringProperty()
    user_name = ndb.StringProperty()

# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

def addUsers(chat_id, yes):
    es = addUsers.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

# ================================
class HelloWorld(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World')


class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self): 
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        try:
            message = body['message']
        except:
            message = body['edited_message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)
        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            elif text =='/nextround':
                italy_time =pytz.timezone('Europe/Rome')
                curr_time = datetime.now(italy_time)
                date_today = (datetime.today() + timedelta(1)).strftime('%Y%m%d')
                x = (datetime.today() + timedelta(1)).strftime('%Y%m%d')
                t = time.strptime(x,'%Y%m%d')
                newdate=datetime(t.tm_year,t.tm_mon,t.tm_mday)+timedelta(1)
                new_date = newdate.strftime('%d-%m-%Y')

                round_1 = 15
                round_2 = 18
                round_3 = 21

                time_now = curr_time.strftime('%d-%m-%Y %H:%M:%S')
                date_now = curr_time.strftime('%d-%m-%Y')
                hour_now = int(curr_time.strftime('%H'))
                min_now = int(curr_time.strftime('%M'))
                sec_now = int(curr_time.strftime('%S'))

                if(hour_now>=21):
                    hour_next = 15+23-hour_now
                    min_next = 60-min_now
                    sec_next = 60-sec_now
                    next_timer = hour_next+':'+min_next+':'+sec_next
                    next_date = "15:00:00"
                elif(hour_now<15):
                    hour_next = 14-hour_now
                    min_next = 60-min_now
                    sec_next = 60-sec_now
                    next_timer = hour_next+':'+min_next+':'+sec_next
                    next_date = "15:00:00"
                elif(hour_now>=15 and hour_now<18):
                    hour_next = 17-hour_now
                    min_next = 60-min_now
                    sec_next = 60-sec_now
                    next_timer = hour_next+':'+min_next+':'+sec_next
                    next_date = "18:00:00"
                else:
                    hour_next = 20-hour_now
                    if(hour_next)<10:
                        hour_next='0'+str(hour_next) 
                    min_next = 60-min_now
                    if(min_next)<10:
                        min_next='0'+str(min_next)
                    sec_next = 60-sec_now
                    if(sec_next)<10:
                        sec_next='0'+str(sec_next)
                    next_timer = str(hour_next)+':'+str(min_next)+':'+str(sec_next)
                    next_date = "21:00:00"
                reply('Group Time is: '+time_now+'\n Next Round Will Start in '+next_timer+'\n at: '+next_date+' (CET)')
        
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply('I am Igt Bot')
        elif 'what time' in text:
            reply('look at the corner of your screen!')
        else:
            if getEnabled(chat_id):
                reply('I got your message! (but I do not know how to answer)')
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/', HelloWorld),
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
