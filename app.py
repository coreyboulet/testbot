import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen
#from groupy import attachments
#from groupy import post
#from groupy.client import Client
#client = Client.from_token(token)
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
  elif data['group_id']=='39961905' and mess=='lol' and data['name'] != 'Secretary of Coreyboulet':
  	msg = 'lol'
  elif data['group_id']=='39961905' and data['text']=='@Rare' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Hello, @Abhinay Tirupati'
    #atch = 
   #message = 39961905.post(text='hi')
    #mtn = [{:loci=[[0, 17]], :type="mentions", :user_ids=["35632718"]}]

  send_message(msg)
  return "ok", 200



def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post?token=MLNAWV0kDn62viD3ClwUzmOyO7Ru87BGjKKYLlFG'

  data = {
          
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
          'attachments': [{'loci':[[7, 16]], 'type':'mentions', 'user_ids':["35632718"]}],
          #'type':"mentions",
          #'user_ids':[35632718],
          #"loci":[[0,17]]
          
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()