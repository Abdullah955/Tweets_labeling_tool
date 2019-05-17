from flask import Flask, flash, redirect, render_template, request, session, abort
import flask
import os
import tempfile
from flask import *
from jinja2 import Template
import csv
import pandas as pd
from sqlalchemy.orm import sessionmaker
from tabledef import *


user = 1
length = 0
engine = create_engine('sqlite:///users.db', echo=True)
# session = scoped_session(sessionmaker(bind = engine))


app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route('/', methods=['GET'])
def home():

    # check which user is logged in
    if not session.get('logged_in'):
        return render_template('login.html')

    else:

        df = pd.read_csv(str(userG()), encoding='utf-8', engine='python')
        count1 = df.iloc[0, 3]
        # tweet index to start from
        count = int(count1)
        # length of dataframe
        length = len(df)
        # display tweet in the page
        # df = pd.read_csv(file, encoding='utf-8', engine='python')
        count1 = df.iloc[0, 3]
        # tweet index to start from
        count = int(count1)
        # length of dataframe
        length = len(df)
        print (length)
        if count <= length - 2:
            return render_template('index.html', paragraph=df.iloc[count, 0], count=[count + 1])
        else:
            return render_template('index.html', paragraph="End of tweets", disabled="disabled")


@app.route('/', methods=['POST'])
def hello(name=None):
    if not session.get('logged_in'):
        return render_template('login.html')

    else:

        df = pd.read_csv(str(userG()), encoding='utf-8', engine='python')
        count1 = df.iloc[0, 3]
        count = int(count1)
        length = len(df)
        count1 = df.iloc[0, 3]
        count = int(count1)

        if request.form['submit'] == 'Positive':
            df.iloc[count, 1] = 1

        elif request.form['submit'] == 'Negative':
            df.iloc[count, 1] = 2

        elif request.form['submit'] == 'Neutral':
            df.iloc[count, 1] = 3

        elif request.form['submit'] == 'Spam':
            df.iloc[count, 1] = 0

    # df = pd.read_csv(str(userG()), encoding='utf-8', engine='python')

    # get context checkboxes as list
    choicesList = request.form.getlist('context')
    # seperate list by ,
    choicesString = ",".join(choicesList)
    # write context choice in df
    df.iloc[count, 2] = choicesString
    # increase and write count
    count += 1
    df.iloc[0, 3] = count
    # write to csv
    df.to_csv(str(userG()), index=False)

    # display tweet in the page
    if count <= length - 1:
        return render_template('index.html', paragraph=df.iloc[count, 0], count=[count + 1])
    else:
        return render_template('index.html', paragraph="End of tweets", disabled="disabled")


@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    # add the user to the session
    session['USERNAME'] = POST_USERNAME

    try:
        user = POST_USERNAME

    # failed to login, do something.
    except Exception as why:
        app.logger.critical('.....')

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]), User.id)
    result = query.first()
    print(result)
    if result:
        # user logged in correctly
        session['logged_in'] = True
    else:
        flash('Wrong username or password!')
    return redirect(url_for('home'))


# user file selection
def userG():
    print (session)
    if session['USERNAME'] == 'user1':
        file = 'S1.csv'
    elif session['USERNAME'] == 'user2':
        file = 'S2.csv'
    elif session['USERNAME'] == 'user3':
        file = 'S3.csv'
    elif session['USERNAME'] == 'user4':
        file = 'S4.csv'

    finalFile = file
    # read tweets from user's file
    # df = pd.read_csv(file, encoding='utf-8', engine='python')
    return finalFile


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.run(debug=True)
