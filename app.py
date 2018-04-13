import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  #Here I'm putting the message coming from the channel in lower so I dont care about caps
  mess = data['text']
  mess= mess.lower()

  # We don't want to reply to ourselves!
  # In this line I check that this message come from the alert channel so it starts the message telling 
  #us about the raid happening. 
  if data['group_id']==	'36731470' and data['name'] != 'Secretary of Coreyboulet':
    msg = '{}, announced :"{}".... Who is in ?'.format(data['name'], data['text'])

  # Ici je verifie que on est bien dans le code du channel de conversation
  #then I check the text and that I'm not talking to myself
  elif data['group_id']=='33797805' and mess=='hello' and data['name'] != 'Secretary of Coreyboulet':
  	msg = 'Hello {}!'.format(data['name'])
  elif data['group_id']=='33797805' and mess=='good night' and data['name'] != 'Secretary of Coreyboulet':
  	msg = 'Sleep tight {}!'.format(data['name'])
  elif data['group_id']=='33797805' and mess=='lol' and data['name'] != 'Secretary of Coreyboulet':
  	msg = 'lol'
  elif data['group_id']=='33797805' and mess=='@rare' and data['name'] != 'Secretary of Coreyboulet':
	msg = '@Abhinay | Lv39 | Instinct @Mitch (Rayquaza50) | Level 38 | Mystic'


  
  send_message(msg)
  return "ok", 200



def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()