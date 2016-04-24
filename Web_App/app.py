'''Salesforce Strategy & Capacity
'''
from __future__ import print_function

import flask
import os 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import re
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from cStringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import psycopg2
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from plotly.offline import plot




app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
app._static_folder = os.path.dirname(os.path.realpath(__file__))
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf','doc'])
global relev
global top_soc
global data1
global data2
global map_graph


##h host and user info for posgresql database
host='ec2-23-21-166-138.compute-1.amazonaws.com'
database='dbc1rr04is5r4c'
User='pcvgfgscbezjmo'
Port=5432
Password='1-CPMPdxkaY-d7zzCPo8MONaG9'
Psql='heroku pg:psql --app heroku-postgres-69c58187 HEROKU_POSTGRESQL_OLIVE'

engine = create_engine(r'postgresql+psycopg2://'+User+':'+Password+'@'+host+':'+str(Port)+'/'+database)


soc_code='soc'

#make choropleth map for # of relevant jobs per state
def make_map(counts):
    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
                [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
    
    
    data = [ dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = counts['code'],            
            z = counts[soc_code].astype(float),    #number of relavent job postings per state
            locationmode = 'USA-states',
            #text = counts['counts'],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                )
            ),
        ) ]

    layout = dict(
            title = '# Related Jobs by State',
            width=600,height=600,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
            ),
        )

    fig = dict( data=data, layout=layout )

    url = plot( fig,filename='Relevant Jobs by State.html',output_type='div')   #output as html
    return(url)


#use pre-trained Multinomial Naive Bayes text classifier to classify resumes into top most relevant soc codes
def get_predictions(job_string):
    clf=joblib.load('model.pkl')  #load trained model
    preds=clf.predict_proba(job_string)
    prob_df=pd.DataFrame({soc_code:clf.classes_,'prob':preds[0]})
    return prob_df.sort_values('prob',ascending=0).head(11)[[soc_code]]    #classification plus 10 most related soc codes

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#remove stop words and other symbols from text
def clean_name(raw):
    letters=re.sub("[^a-zA-Z]", " ", raw)
    words=letters.lower().split()
    stops=set(stopwords.words("english"))   #get english stop words
    meaningful=[w for w in words if not w in stops]   #remove stop words
    return (" ".join( meaningful))		   


#find relevant jobs in the user-selected state
@app.route('/job_lookup', methods=['POST'])
def job_lookup():
    #g.db = connect_db()

    state=request.form.get('state')
    global relev
    
    jobs=relev[relev['state']==state]
    data2=jobs[['links','title']].to_html()
    return render_template('home.html', data=data1,data2=data2,data_map=map_graph)

@app.route("/")
def main():

    html = flask.render_template(
        'home.html'
    )
    return encode_utf8(html)


@app.route('/upload', methods=['POST'])
#read in file or text (must be .doc or .txt, no pdf)
def upload():
    global top_soc
    global data1
    global map_graph
    global relev


    file = request.files['file']       #read in file if one is uploaded
    text=None
    if (request.form['text']):             #get text if text input
        text = request.form['text']
    
    file_read=None
   
    if file and allowed_file(file.filename):
        filename = file.filename
        file_read=file.read()
        
    if ((text !=None) &(file_read !=None)):
        clean_txt=clean_name(str(file_read)+' '+str(text))
    elif (file):
        clean_txt=clean_name(file.read())
    else:
        clean_txt=clean_name(text)
    preds=get_predictions([clean_txt])
    
    titles = pd.read_sql("SELECT * FROM soc_occ_table_v2", con=engine)   #pull soc code mapping from posgres

    results=pd.merge(preds,titles,on=soc_code)[['soc','Title']]

    top_soc=results[soc_code]
    data1=results.to_html()
  

    #pull all Craigslist job postings from the posgres database
    relev=pd.read_sql("SELECT state,soc,title,links FROM craigslistdb_wsoc_v2 WHERE soc IN (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", con=engine,params=tuple(top_soc))
    state_code=pd.read_sql("SELECT * FROM state_code",con=engine)
    counts=relev[['state','soc']].groupby('state',as_index=False).count()
    counts=pd.merge(counts,state_code,on='state',how='inner')
    map_graph=make_map(counts)


    #print(results)
    html = flask.render_template(
    'home.html',data=data1,data_map=map_graph
	)
    return encode_utf8(html)
	
if __name__ == "__main__":

    print(__doc__)
    app.run(debug=True)
