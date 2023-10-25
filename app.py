import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id': False}))

    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    #sample_receive = request.form['sample_give']
    #print(sample_receive)
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']   
    filename = ''
    profile_name = '' 
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S') 

    if ('file_give' in request.files):
        file_receive = request.files['file_give']
        extension = file_receive.filename.split('.')[-1]
        filename = f'file-{mytime}.{extension}'
        file_receive.save(f'static/{filename}')
        print(filename)

    if ('profile_give' in request.files):
        profile_receive = request.files['profile_give']
        profile_extension = profile_receive.filename.split('.')[-1]   
        profile_name = f'profile-{mytime}.{profile_extension}' 
        profile_receive.save(f'static/{profile_name}')

    time = today.strftime('%Y.%m.%d')
    doc = {
        'file': filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive,
        'time' : time 
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST request complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)