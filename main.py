# -*- coding: utf-8 -*-
import StringIO
import json
import logging
import random
import urllib
import urllib2

#db
import web
import string

from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

# for sending images
# import Image
# import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

#time
from datetime import datetime, timedelta
import pytz
import time

#for fixing emoji
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

TOKEN = ''

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
       web.ctx.orm.commit()
       raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # If the above alone doesn't work, uncomment 
        # the following line:
        #web.ctx.orm.expunge_all() 

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


class Users(ndb.Model):
    user_name = ndb.StringProperty()
    user_id = ndb.StringProperty()
    insta_id = ndb.StringProperty()


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

def addUsers(user_id, user_name, insta_id):
    sandy = Users()
    sandy.username = user_name
    sandy.user_id = user_id
    sandy.ins_id = ins_id
    sandy.put()
    return sandy

def getUsers(chat_id):
    sandy = Users.get_by_id(str(chat_id))
    if sandy:
        return sandy
    return False


# ================================
class HelloWorld(webapp2.RequestHandler):
    def get(self):
         u = User(insta_id='@jose'
                ,username='josethomasd'
                ,user_id='1234')
        web.ctx.orm.add(u)
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
        sender = message['from']
        sender_id = sender['id']
        sender_name = sender['username']
        chat_id = chat['id']
        chat_type = chat['type']

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

        def reply_group(msg=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-1001139451744',
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                })).read()
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)
        if chat_type=='supergroup':
            if text =='/nextround':
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
                    next_date = "15:00:00"
                elif(hour_now<15):
                    hour_next = 14-hour_now
                    next_date = "15:00:00"
                elif(hour_now>=15 and hour_now<18):
                    hour_next = 17-hour_now
                    next_date = "18:00:00"
                else:
                    hour_next = 20-hour_now
                    next_date = "21:00:00"
                
                min_next = 60-min_now
                sec_next = 60-sec_now
                
                if(hour_next)<10:
                    hour_next='0'+str(hour_next) 
                min_next = 60-min_now
                if(min_next)<10:
                    min_next='0'+str(min_next)
                sec_next = 60-sec_now
                if(sec_next)<10:
                    sec_next='0'+str(sec_next)
                
                next_timer = str(hour_next)+':'+str(min_next)+':'+str(sec_next)
                reply_group('Group Time is: '+time_now+'\n Next Round Will Start in '+next_timer+'\n at: '+next_date+' (CET)')  
            
            elif text.startswith('@'):
                italy_time =pytz.timezone('Europe/Rome')
                curr_time = datetime.now(italy_time)
                curr_hour = int(curr_time.strftime('%H'))
                curr_min = int(curr_time.strftime('%M'))
                if(curr_hour==14 or curr_hour==17 or curr_hour==20):
                    if(curr_min>=40):
                        ins_id = text.partition(' ')
                        insta_id = ins_id[0]
                        addUsers(user_id, user_name, insta_id)
                        reply('Username '+insta_id+' Received')

                    else:
                        reply('No active round')
                else:
                    reply('No active round')
            elif text.startswith('D'):
                italy_time =pytz.timezone('Europe/Rome')
                curr_time = datetime.now(italy_time)
                curr_hour = int(curr_time.strftime('%H'))
                curr_min = int(curr_time.strftime('%M'))
                
                ins_id = text.partition(' ')
                insta_id = ins_id[0]

                if(curr_hour==15 or curr_hour==18 or curr_hour==21):    
                    reply('Done '+insta_id)

                elif(curr_hour==16 or curr_hour==19 or curr_hour==22):
                    if(curr_time<=25):
                        reply('Done '+insta_id)
                else:
                    reply('No active round')

            else:
                if getEnabled(chat_id):
                    reply("Please Don't Speak Here! Join Our Discussion Chat'")
                else:
                    logging.info('not enabled for chat_id {}'.format(chat_id))

        elif text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            # elif text == '/image':
            #     img = Image.new('RGB', (512, 512))
            #     base = random.randint(0, 16777216)
            #     pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
            #     img.putdata(pixels)
            #     output = StringIO.StringIO()
            #     img.save(output, 'JPEG')
            #     reply(img=output.getvalue())
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply('I am Igt Bot')
        elif 'what time' in text:
            reply('look at the corner of your screen!')
        else:
            if getEnabled(chat_id):
                reply("I got your message.")
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


class NotifyHandler(webapp2.RequestHandler):
    def get(self): 
        msg = '❤ LIKE RECENT ROUND ❤\n D R O P \n Format : You can now drop like that \n@username'
  
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
            'chat_id': '-1001139451744',
            'text': msg.decode().encode('UTF-8'),
        })).read()
        self.response.write("ok")
class NewRoundHandler(webapp2.RequestHandler):
    def get(self): 
        msg = '😊 ROUND IS NOW CLOSED 😊 \n 90 MINUTES! \n LEECHING = BAN \n PM admins for any issues'
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
            'chat_id': '-1001139451744',
            'text': msg.decode().encode('UTF-8'),
        })).read()  
        self.response.write("ok")
app = webapp2.WSGIApplication([
    ('/', HelloWorld),
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/new_round', NewRoundHandler),
    ('/notify', NotifyHandler)
], debug=True)
app.add_processor(load_sqla)
