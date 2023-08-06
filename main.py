import discord
import os
import requests
import json
import random
from replit import db
from alive import keep_alive

my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

def update_q(command_message):
  if 'commands' in db.keys():
    commands = db['commands']
    commands.append(command_message)
    db['commands'] = commands
    
  else:
    db['commands'] = [command_message]

def delete_q(index):
  commands = db['commands']
  if len(commands) > index:
    del commands[index]
    db['commands'] = commands

client = discord.Client(intents=intents)

soccer_words = ['messi', 'ronaldo', 'neymar', 'barca', 'manche', 'man united' 'liverpool', 'man city', 'madrid', 'chelsea', 'arsenal', 'tot', 'atm', 'psg', 'bayern', 'dortmund', 'ajax', 'ucl', 'uel', 'wc', 'transfer window']

starter_q = ['Attention', 'Stop', 'Focus']

if 'responding' not in db.keys():
  db['responding'] = True

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  print('Message received:', message.content)
  if message.author == client.user:
    return 

  msg = message.content
  
  if msg.startswith('ronaldo'):
    quote = get_quote() 
    await message.channel.send(quote)

  if db['responding']:       
    options = starter_q
    if 'commands' in db.keys():
      options = options + list(db['commands'])
    
    if any(word in msg for word in soccer_words):
      await message.channel.send(random.choice(options))


  if msg.startswith('$new'):
    command_message = msg.split('$new ', 1)[1]
    update_q(command_message)
    await message.channel.send("New command message added.")

  if msg.startswith('$del'):
    commands = []
    if 'commands' in db.keys():
      index = int(msg.split('$del',1)[1])
      delete_q(index)
      commands = db['commands']
    await message.channel.send('\n'.join(commands))
  
  if msg.startswith('$list'):
    commands = []
    if 'commands' in db.keys():
      commands = db['commands']
    await message.channel.send('\n'.join(commands))


  if msg.startswith('$responding'):
    value = msg.split('responding ',1)[1]
    if value.lower() ==  'true':
      db['responding'] = True
      await message.channal.send('Responding is on.')


    else:
      db['responding'] = False
      await message.channal.send('Responding is off.')

keep_alive()
client.run(my_secret)
