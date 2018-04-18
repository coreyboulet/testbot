import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen
#from groupy import attachments
#from groupy import post
#from groupy.client import Client
#client = Client.from_token(token)
from flask import Flask, request
import schedule
import time

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
    usrID= 0,0
    locid= [0, 0],[0, 0]

  # Ici je verifie que on est bien dans le code du channel de conversation
  #then I check the text and that I'm not talking to myself
  elif data['group_id']=='33797805' and mess=='hello' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Hello {}!'.format(data['name'])
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']=='33797805' and mess=='good night' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Sleep tight {}!'.format(data['name'])
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']=='33797805' and mess=='lol' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'lol'
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']=='33797805' and data['text']=='@Rare' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Rare pokemon mentionned. @Coreyboulet @Abhinay @Mitch @Sabre @Sam'
    usrID= 35632718,53626037,33632383,56662107,50236640
    locid= [24,28],[0,0],[0,0],[0,0],[0,0]
  elif data['group_id']=='33797805' and mess=='@Quest' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Quests were mentionned. @Coreyboulet @Abhinay @Mitch'
    usrID= 35632718,53626037,33632383
    locid= [23,28],[0,0],[0,0]
  elif data['group_id']=='33797805' and data['text']=='@Ditto' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Ditto was mentionned. @Rob, @Jackie'
    usrID= 18834490,45568857,0
    locid= [22,13],[0,0],[0,0]
  elif data['group_id']=='33797805' and data['text']=='@Ghost' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'A ghost was mentionned. @Rob'
    usrID= 18834490,0
    locid= [22,4],[0,0]
  elif data['group_id']=='33797805' and data['text']=='@Bot' and data['name'] != 'Secretary of Coreyboulet':
    msg = "Hello Everyone, I'm a bot, please use me to notify people that need things on this channel. Right now, you can type @Ditto: Rob and Jackie, @Ghost: Rob @Rare: Mitch, Corey, Abhinay, Sabre, Sam-B @Quest: Mitch, Corey, Abhinay. Contact Corey to be added or deleted from a list " 
    usrID= 0,0
    locid= [0, 0],[0, 0]

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


msg = "Hello Everyone, I'm a bot, please use me to notify people that need things on this channel. Right now, you can type @Ditto: Rob and Jackie, @Ghost: Rob @Rare: Mitch, Corey, Abhinay, Sabre, Sam-B @Quest: Mitch, Corey, Abhinay. Contact Corey to be added or deleted from a list " 
usrID= 0,0
locid= [0, 0],[0, 0]
schedule.every().day.at("10:55").do(send_message(msg, usrID, locid))
schedule.every().day.at("10:57").send_message(msg, usrID, locid)