#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import codecs
import glob
import json
import re
import os
import boto.sqs
from boto.sqs.message import Message
#from thread import *
#os.chdir("data/")

#alchemyapi = AlchemyAPI('*')

#Variables that contains the user credentials to access Twitter API
access_token = "*"
access_token_secret = "*"
consumer_key = "*"
consumer_secret = "*"

#conn = boto.sqs.connect_to_region("us-west-2", aws_access_key_id='*',aws_secret_access_key='*')
#conn = boto.sqs.connect_to_region("us-west-2")
conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='*', 
                                          aws_secret_access_key='*')
q = conn.create_queue('myqueue9')
#Hide the end point
#doc_service = boto.cloudsearch2.document.DocumentServiceConnection(domain=None, endpoint='*')



def append_record(record):
    with open('data1.json', 'a') as f:
        json.dump(record, f)
        f.write(os.linesep)

class StdOutListener(StreamListener):
    def on_data(self, data):
        json_load = json.loads(data)
        try:
            coordinates = json_load['coordinates']
            place = json_load['place']
            lang = json_load['lang']
            text = json_load['text']
            #response = alchemyapi.sentiment("text", text)
            #print "Sentiment: ", response["docSentiment"]["type"]
            if coordinates['coordinates'] != None:
                if lang == "en":
                    m = Message()
                    text1 = {}
                    text1["coordinates"]=coordinates['coordinates']
                    text1["text"]=text
                    print text1
                    m.set_body(str(text1))
                    q.write(m)
                    #append_record(json_load)
            """elif place != None:
                if lang == "en":
                    m = Message()
                    text1 = {}
                    text1["coordinates"]=coordinates
                    text1["text"]=text
                    m.set_body(text1)
                    q.write(m)"""
                    #append_record(json_load)
        except:
            pass
        #print coordinates
        return True
    
    def on_error(self, status):
        print(status)


class MyMessage(object):
    """docstring for My"""
    def __init__(self, arg):
        super(My, self).__init__()
        self.arg = arg
        


def start_stream(auth, l):
    while True:
        try:
            stream = Stream(auth, l)
            stream.sample()
        except:
            continue


if __name__ == '__main__':
    
    #for file in glob.glob("*_saved.txt"):
    #    shutil.copyfile(file, file.replace("_saved", ""))
    
    #This handles Twitter authetification and the connection to Twitter Streaming API
    
    #start_new_thread(StdOutListener,(conn,))
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    start_stream(auth, l)





