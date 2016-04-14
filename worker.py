import boto.sqs
import boto.sns
from boto.sqs.message import Message
from alchemyapi import AlchemyAPI
import ast


conn = boto.sqs.connect_to_region("us-west-2", aws_access_key_id='*',aws_secret_access_key='*')
text={}
sns = boto.sns.connect_to_region("us-west-2", aws_access_key_id='*',aws_secret_access_key='*')
topics = sns.get_all_topics()
mytopics = topics["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
mytopic_arn = mytopics[0]["TopicArn"]
print mytopic_arn

alchemyapi = AlchemyAPI()
#p = 0
while True:
	try:
		my_queue = conn.get_queue('myqueue6')
		rs = my_queue.get_messages()
		#a = len(rs)
		#print a
		#while len(rs) != 0:
		m = rs[0]
		#m.get_body()
		text=ast.literal_eval(m.get_body())
		text1=text["text"]
		text2=text["coordinates"]
		print text1
		print text2
		res = alchemyapi.sentiment("text", text1, {'sentiment': 1})
		sentiment = res["docSentiment"]["type"]
		print sentiment
		#print "Sentiment: ", sentiment
		subj = "SNS message over boto"
		msg = "sentiment analysis is done."
		response = sns.publish(
			topic=mytopic_arn,
			message=text1,
			subject=str(text2[0])+","+str(text2[1])+","+str(sentiment)
			)
		#mytopic_arn, msg, [text1,text2,"sentiment"])
		my_queue.delete_message(m)
	except:
		pass
