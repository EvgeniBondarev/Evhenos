#api_id - 11080576
#api_hash - 14079e73df3157b7d96ac12cf28d1d9c
from telethon import *


api_id = 11080576
api_hash = '14079e73df3157b7d96ac12cf28d1d9c'

client = TelegramClient('session_name', api_id, api_hash)
client.start()
directory = "C:/Users/Evgeni/Desktop/wd_bot/dow"
  
def kal():
    channels = []
    for dialog in client.iter_dialogs():
        if dialog.is_channel:
            channels.append(dialog.title)
    return channels

@client.on(events.NewMessage(chats=kal()))
async def normal_handler(event):        
    print(event)
    chat_from = event.chat if event.chat else (await event.get_chat()) 
    print(chat_from)
    if chat_from.username != None:
        await client.send_message('🌤WeatherPy🌤', f'https://t.me/{chat_from.username}/{event.message.id}')
    else:
        await client.send_message('🌤WeatherPy🌤', f'https://t.me/{chat_from.id}/{event.message.id}\n{event.message.message}')
    


client.run_until_disconnected()


        
       
          

               

            
        



