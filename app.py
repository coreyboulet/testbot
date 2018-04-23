import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import schedule
import time

#import test for the googlespreadsheet
import gspread
from oauth2client.client import ServiceAccountCredentials


scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#sheet=client.open('GroupMeBot')
#testresult= sheet.cell(2,3).value





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
  if data['group_id']==	'36731470' and data['name'] != 'Secretary of Coreyboulet'and 'to the group.' not in mess and 'changed name'not in mess :
    msg = '{}, announced :"{}".... Who is in ?'.format(data['name'], data['text'])
    usrID= 0,0
    locid= [0, 0],[0, 0]

  # Ici je verifie que on est bien dans le code du channel de conversation
  #then I check the text and that I'm not talking to myself
  elif data['group_id']==os.getenv('GROUP_ID') and 'hello' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Hello {}!'.format(data['name'])
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']==os.getenv('GROUP_ID') and mess=='good night' and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Sleep tight {}!'.format(data['name'])
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']==os.getenv('GROUP_ID') and 'lol' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'lol'
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@rare' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Rare pokemon mentionned. @Coreyboulet @Abhinay @Mitch @Sabre @Sam @Harold @Allan'
    usrID= 35632718,53626037,33632383,56662107,50236640,58375075 ,33612373
    locid= [24,55],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@quest' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Quests were mentionned. @Coreyboulet @Abhinay @Mitch'
    usrID= 35632718,53626037,33632383
    locid= [23,28],[0,0],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@ditto' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Ditto was mentionned. @Rob, @Jackie'
    usrID= 18834490,45568857,0
    locid= [22,13],[0,0],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@ghost'in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'A ghost was mentionned. @Rob @Clare'
    usrID= 18834490,27457002
    locid= [23,11],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@bot' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = "Hello Everyone, I'm a bot, please use me to notify people that need things on this channel. Right now, you can type @Ditto: Rob and Jackie, @Ghost: Rob, Clare @Rare: Mitch, Corey, Abhinay, Sabre, Sam-B, Harold, Allan @Quest: Mitch, Corey, Abhinay. Contact Corey to be added or deleted from a list " 
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



#def daily_message():
  #msg = "Hello Everyone, I'm a bot, please use me to notify people that need things on this channel. Right now, you can type @Ditto: Rob and Jackie, @Ghost: Rob @Rare: Mitch, Corey, Abhinay, Sabre, Sam-B @Quest: Mitch, Corey, Abhinay. Contact Corey to be added or deleted from a list " 
  #usrID= 0,0
  #locid= [0, 0],[0, 0]
  #send_message(msg, usrID, locid)


#schedule.every().day.at("07:21").do(daily_message)
#schedule.every(10).seconds.do(daily_message)
#schedule.every().day.at("20:04").send_message(daily_message)


#while True:
  #schedule.run_pending()
  #time.sleep(1)