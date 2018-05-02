import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import schedule
import time
import re

#import test for the googlespreadsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#https://www.youtube.com/watch?v=vISRn5qFrkM&t=137s   and check the commentaries for the extra scope. 
#This basically opent the sheet in the excel sheet
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
gymsheet=client.open('GroupMeBot').worksheet("discordbot")
pokemonsheet=client.open('GroupMeBot').worksheet("pokemon")


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


  if data['group_id']==os.getenv('GROUP_ALERT') and data['name'] != 'Secretary of Coreyboulet'and 'to the group.' not in mess and 'changed name'not in mess :
  	strings=mess.split()
  	gym=""
  	time=""
  	pokemon=""
  	  #here i split the messages in string so we checked if they are names for raids in the dedicated sheet. this is the first part, looking for info on the raid
  	for string in strings:
  		try:
  			if gymsheet.find(string):
  				ref = gymsheet.find(string)
  				row = ref.row
  				output = gymsheet.cell(row,2).value
  			gym= gym + " " + output
  			#this is to avoid the formula to crash when the word is not in the excel list
  		except:
  			pass
  	#This is the second part to identify the pokemon
  	for string in strings:
  		try:
  			if pokemonsheet.find(string):
  				ref = pokemonsheet.find(string)
  				row = ref.row
  				output = pokemonsheet.cell(row,2).value
  			pokemon= pokemon + " " + output
  			#this is to avoid the formula to crash when the word is not in the excel list
  		except:
  			pass
  	#Here I'm looking for something that looks like a time xx:xx or x:xx
  	try:
  		searchtime=re.findall(r'\d{1,2}\S\d{1,2}', mess)
  		#I'm takin the first string with the time criteria, since there should be only one time in the message most of the time
  		time= " starting at "+ searchtime[0]
  	except:
  		try:
  			#if I dont find an hour, and there are 2 numbers this is probably a timer so we adress it another way
  		  	searchtime=re.findall(r'\d{1,2}\S', mess)
  		  	time=" with " +searchtime[0] +" mins left "		
  		except:
  			time=" (sorry I don't know when it is) "
  	if gym=="":
  		gym=" Somewhere... "
  	if pokemon=="":
  		pokemon=" Something... "  	
  	msg= " {} announced a ".format(data['name']) + pokemon + " at " + gym  + time +", who's in ?"
  	usrID= 0,0
  	locid= [0, 0],[0, 0]






  # Ici je verifie que on est bien dans le code du channel de conversation
  #then I check the text and that I'm not talking to myself
  elif data['group_id']==os.getenv('GROUP_ID') and 'hello' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Hello {}!'.format(data['name'])
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']==os.getenv('GROUP_ID') and 'good night' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Sleep tight {}!'.format(data['name'])
    usrID= 0,0
    locid= [0, 0],[0, 0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@rare' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Rare pokemon mentionned. @Coreyboulet @Abhinay @Mitch @Sabre @Sam @Allan, @Celine, @Sam M, @Max'
    usrID= 35632718,53626037,33632383,56662107,50236640,58375075 ,33612373,47762292,17045652
    locid= [24,71],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@quest' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Quests were mentionned. @Coreyboulet @Abhinay @Mitch @Andee @Max @Allan @Celine'
    usrID= 35632718,53626037,33632383,41943092,58375075,33612373
    locid= [23,55],[0,0],[0,0],[0,0],[0,0],[0,0]
#  elif data['group_id']==os.getenv('GROUP_ID') and sheet.cell(2,1).value in mess and data['name'] != 'Secretary of Coreyboulet':
#    msg = sheet.cell(2,2).value
#    usrID= sheet.cell(2,3).value,0
#    locid= [sheet.cell(2,4).value,sheet.cell(2,5).value],[0, 0]
#  elif data['group_id']==os.getenv('GROUP_ID') and sheet.cell(3,1).value in mess and data['name'] != 'Secretary of Coreyboulet':
#    msg = sheet.cell(3,2).value
#    usrID= sheet.cell(3,3).value,0
#    locid= [sheet.cell(3,4).value,sheet.cell(3,5).value],[3, 0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@ditto' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'Ditto was mentionned. @Rob @Clare @Izzy'
    usrID= 18834490,27457002,27100281
    locid= [22,17],[0,0],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@ghost'in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = 'A ghost was mentionned. @Rob'
    usrID= 18834490,0
    locid= [23,11],[0,0]
  elif data['group_id']==os.getenv('GROUP_ID') and '@bot' in mess and data['name'] != 'Secretary of Coreyboulet':
    msg = "Hello Everyone, I'm a bot, please use me to notify people that need things on this channel. Right now, you can type @Ditto: Rob, Clare, Izzy @Ghost: Rob @Rare: Mitch, Corey, Abhinay, Sabre, Sam-B, Allan, Celine, Sam M,Max @Quest: Mitch, Corey, Abhinay, Andee, Max, Allan, Celine. Contact Corey to be added or deleted from a list " 
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