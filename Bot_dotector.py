import amino
import threading
import heroku3
from time import sleep
client = amino.Client()
email='ravimourya40@gmail.com'
password ='ravioppp1234'
client.login(email=email, password=password)
comid=[17015136,14999388] # Time valley and Indias VIP community ID
mtype=[100,107,109,110,114,115]
me=['e8560276-7896-41ca-964e-3aa7358b0cb4','9eaa0323-4912-40d8-ab77-ee281ae44a55','d027476e-4058-499a-8d1f-2381919014fb']

heroku_conn = heroku3.from_key('2510e899-3f90-4907-aeb1-aaf1fa469bcf')
botapp= heroku_conn.apps()['botdetectoramino']


def search_bot(message,comid):
    if message.json['type'] in mtype and message.content is not None:
        if message.author.userId not in me:
            subclient = amino.SubClient(comId=comid, profile=client.profile)
            mes="<$"+message.author.nickname+"$> is sending the unknown messages"
            print(mes)
            subclient.send_message(message.chatId,mes,mentionUserIds=[message.author.userId])
            subclient.logout()
            # subclient.socket.close()
            
            
@client.callbacks.event("on_delete_message")
def on_delete_message(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()

@client.callbacks.event("on_voice_chat_start")
def on_voice_chat_start(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()

@client.callbacks.event("on_video_chat_start")
def on_video_chat_start(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()
        
@client.callbacks.event("on_voice_chat_end")
def on_voice_chat_end(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()

@client.callbacks.event("on_video_chat_end")
def on_video_chat_end(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()
        
@client.callbacks.event("on_screen_room_start")
def on_screen_room_start(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()
        
@client.callbacks.event("on_screen_room_end")
def on_screen_room_end(data):
    if data.comId in comid:
        mt=threading.Thread(target=search_bot,args=(data.message,data.comId,))
        mt.start()
        
        
def search(uid):
    global found
    if uid not in me:
        for com in comid:
            try:
                subclient = amino.SubClient(comId=com, profile=client.profile)
                u=subclient.get_from_id(uid,objectType=0,comId=com)
                if subclient.get_user_info(uid).status == 0:
                # print(uid)
                    found=1
                    # print(subclient.get_user_info(uid).nickname,com)
                    log=u.json['extensions']['linkInfo']['shareURLShortCode']+" is a bot in "+client.get_community_info(com).name
                    print(log)
                    client.send_message('54cd2fa2-20c1-46ba-9fe7-72ee5fade260',log)
                    subclient.logout()
            except:
                pass
                found=0
                
def stayalive():
    j=0
    while True:
       try:
        if j >= 60: #1 minute
            client.socket.close()
            client.socket.start()
            j = 0
            botapp.restart()
        u=client.get_from_deviceid("01B592EF5658F82E1339B39AA893FF661D7E8B8F1D16227E396EF4B1BF60F33D25566A35AB1514DAB5")
        found=0
        mm=threading.Thread(target=search,args=(u,))
        mm.start()
        if found==0:
            mm.join()
        j+=1
        sleep(1)
       except:
        pass
stayalive()
