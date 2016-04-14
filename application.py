from flask import Flask
application = Flask(__name__)
from flask import request, url_for
from flask import render_template
import urllib
import json
from elasticsearch import Elasticsearch
es = Elasticsearch(host='*.us-east-1.es.amazonaws.com', port=80)

import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
from flask import Flask, json, Response, render_template


def coordinate(word):
    dic = es.search(index='posts', doc_type='tweet', q='text:"'+str(word)+'"')
    output_coord = []
    p = 0
    n = 0
    ne = 0
    for line in dic['hits']['hits']:
        k = line['_source']
        if k['sentiment'] == 'negative':
            coord = [k['coordinates'], k['text'], 'http://maps.google.com/mapfiles/ms/icons/red-dot.png']
            ne += 1
            output_coord.append(coord)
        elif k['sentiment'] == 'positive':
            coord = [k['coordinates'], k['text'], 'http://maps.google.com/mapfiles/ms/icons/green-dot.png']
            p += 1
            output_coord.append(coord)
        elif k['sentiment'] == 'neutral':
            coord = [k['coordinates'], k['text'], 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png']
            n += 1
            output_coord.append(coord)
    return [output_coord,p,n,ne]

from flask import session

@application.route('/search')
def search():
    return render_template('ent.html')

@application.route('/sns', methods=['GET','POST'], strict_slashes=False)
def sns():
    try:
        temp = json.loads(request.data)
        #print temp
        msg = temp['Message']
        print msg
        content = temp['Subject']
        content_split = content.split(",")
        es.index(index='posts', doc_type='tweet', body={
            'text' : msg,
            'coordinates' : [float(content_split[0]),float(content_split[1])],
            'sentiment' : content_split[2]
            })
        global msg
    except:
        temp = json.loads(request.data)
        print temp
    return "success", 200





@application.route('/result', methods=['POST'])
def result():
    q1 = request.form['word']
    asd = coordinate(q1)
    print asd
    counter = len(asd[0])
    return render_template('search2.html',word = q1, counter = counter, posts=asd[0],p=asd[1],
        n=asd[2],ne=asd[3])



def event():
    while True:
        yield 'data: ' + msg + '\n\n'
        gevent.sleep(0.2)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/stream/', methods=['GET', 'POST'])
def stream():
    return Response(event(), mimetype="text/event-stream")

@application.route('/projects/')
def projects():
    return 'The project page'

@application.route('/about')
def about():
    return 'The about page'



@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
	#application.run(host='0.0.0.0', debug=True)
    WSGIServer(('', 5000), application).serve_forever()
