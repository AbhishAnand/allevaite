import numpy as np
import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
import html2text

from flask import Flask,Blueprint, render_template,redirect,request,jsonify
from flask_login import login_required,current_user

model = Blueprint('model', __name__)

@model.route('/text')
@login_required
def text():
    return render_template('textinp.html')


@model.route("/predict",methods=['POST'])
def predict():
    dataset=pd.read_csv('project/data/final_confessions.csv')
    X= dataset.iloc[:,0]
    y= dataset.iloc[:,1]

    corpus= []
    for i in range(0,626):
        conf = re.sub('[^a-zA-Z]',' ',dataset['Confession'][i])#a-zA-Z will be kept only 
        conf = conf.lower()#all the review words will be converted in lower case    
        conf = conf.split() #the words are split and stored in a list
        ps =PorterStemmer() #PorterStemmer is used to stem the past or some other tense word into root terms
        conf = [ps.stem(word) for word in conf if not word in set(stopwords.words('english'))]
        conf =' '.join(conf)
        corpus.append(conf)

    cv = CountVectorizer(max_features =100)
    cv.fit(corpus)

    model_mlp = open('Allevaite_model_mlp.pkl','rb')
    clf = joblib.load(model_mlp)

    if request.method == 'POST':
        message = request.form['editordata']
        cleantext = html2text.html2text(message).strip()
        title = request.form.get('title')
         
        # save the data in th database
        from . import db
        from .models import User,Post

        post = Post(title=title, author=current_user.name , content = cleantext )        
        db.session.add(post)
        db.session.commit()

        data = [message]
        vect = cv.transform(data).toarray()
        my_pred = str(clf.predict(vect)[0])

    return "Your emotion is : {}".format(my_pred)