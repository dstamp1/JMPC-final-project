from app import app
from flask import render_template, request, redirect
from app.models import model
from flask_pymongo import PyMongo
import statistics

mongodb_password = 'GL3evKMWcya1XEO8'
mongodb_user = 'debugger'
mongodb_url = f'mongodb+srv://{mongodb_user}:{mongodb_password}@cluster0-qjkuk.mongodb.net/debugger'

app.config['MONGO_DBNAME'] = 'debugger'
app.config['MONGO_URI'] = mongodb_url

mongo = PyMongo(app)

def average(d):
    return {'rule':d['rule'],'difficulty':sum(d['difficulty'])/len(d['difficulty'])}

@app.route('/')
@app.route('/index')
def index():
    collection = mongo.db.rules
    rules = collection.aggregate([{ "$addFields": 
        {"difficulty_average": 
            { "$avg": "$difficulty" }
        }
    }])

    return render_template('index.html', rules=rules)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        collection = mongo.db.rules
        print(request.form)
        document = {'rule':request.form['rule'],
                    'agerange':request.form['agerange'],
                    'difficulty':[int(request.form['difficulty'])],
                    'tags':request.form.getlist('tags')
                    }
        collection.insert(document)
        return redirect('/')
