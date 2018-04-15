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
    usrID= 0
    locid= [0, 0]

  # Ici je verifie que on est bien dans le code du channel de conversation
  #then I check the text and that I'm not talking to myself
  elif data['group_id']=='39961905' and mess=='hello' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Hello {}!'.format(data['name'])
    usrID= 0
    locid= [0, 0]
  elif data['group_id']=='39961905' and mess=='good night' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Sleep tight {}!'.format(data['name'])
    usrID= 53626037
    locid= [0, 0]
  elif data['group_id']=='39961905' and mess=='lol' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'lol this is cool, really'
    usrID= 53626037
    locid= 0, 0
  elif data['group_id']=='39961905' and data['text']=='@rare' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Hello, @Coreyboulet @Abhinay @Matt'
    usrID= 35632718,53626037,20366614
    locid= [1,2],[5,2],[9,2]


  send_message(msg, usrID, locid)
  return "ok", 200



def send_message(msg, usrID, locid):
  url  = 'https://api.groupme.com/v3/bots/post?token=' + os.getenv('ACCESS_TOKEN')

  data = {
          
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
          'attachments':
          [
          {
          'type':'mentions',
          'user_ids':usrID,
          'loci':locid  
          }
          ]
          
         }
  params = json.dumps(data).encode('utf8')
  request = Request(url, data=params, headers={'content-type': 'application/json'})
  response = urlopen(request).read().decode()
  #request = Request(url, urlencode(data).encode())
  #request.add_header('content-type', 'application/json')
  #json = urlopen(request).read().decode()