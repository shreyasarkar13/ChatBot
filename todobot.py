import time
import json
import requests
import urllib
from dbhelper import DBHelper

db= DBHelper()

token= "466465110:AAH6uhlrE0oe0lNC5O-rf0QN3jSCQI6eRtE"
URL= "https://api.telegram.org/bot{}/".format(token)

def get_url(url):
        response=requests.get(url)
        content=response.content.decode("utf8")
        return content
        
def get_json(url):
        content=get_url(url)
        js=json.loads(content)
        return js
        
def get_updates(offset=None):
        url=URL+"getUpdates?timeout=100"
        if offset:
            url=url+"&offset={}".format(offset)
        js = get_json(url)
        return js
        
def handle_updates(updates):
        for update in updates["result"]:
                    text=update["message"]["text"]
                    chat=update["message"]["chat"]["id"] 
                    items=db.get_items(chat)
                    if text=="/start":
                        send_msg("Welcome to your To Do List. Send me any text and I'll save it as an item to the list. Send me the same item again and I'll delete it from the list.",chat)
                    elif text.startswith("/"):
                        continue
                    elif text in items:
                        db.delete_item(text,chat)
                        items=db.get_items(chat)
                    else:
                         db.add_item(text,chat)
                         items=db.get_items(chat)
                    message="\n".join(items)
                    send_msg(message,chat)
                    print(message," ",chat)
         
                
def get_last_chat_id_and_text(updates):
        num_updates=len(updates["result"])
        last_update=num_updates-1
        text= updates["result"][last_update]["message"]["text"]
        chat_id=updates["result"][last_update]["message"]["chat"]["id"]
        print(last_update,text,chat_id)
        return(text,chat_id)
        
def get_last_update_id(updates):
        update_ids=[]
        for update in updates["result"]:
                update_ids.append(int(update["update_id"]))
        return max(update_ids)
        
        
def send_msg(text,chat_id):
        text=urllib.quote_plus(text)
        url=URL+"sendMessage?text={}&chat_id={}".format(text, chat_id)
        get_url(url)
        
     
text,chat=get_last_chat_id_and_text(get_updates())
send_msg(text,chat)

def main():
        db.setup()
        last_update_id=None
        while True:
            updates= get_updates(last_update_id)
            if len(updates["result"])>0:
                last_update_id=get_last_update_id(updates)+1
                handle_updates(updates)
                time.sleep(0.5)
        
if __name__=='__main__':
        main()
