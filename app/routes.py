from app import app
from flask import render_template, request, redirect
from app.models import model
from flask_pymongo import PyMongo

from bson.objectid import ObjectId


mongodb_password = 'GL3evKMWcya1XEO8'
mongodb_user = 'debugger'
mongodb_url = f'mongodb+srv://{mongodb_user}:{mongodb_password}@cluster0-qjkuk.mongodb.net/debugger'

app.config['MONGO_DBNAME'] = 'debugger'
app.config['MONGO_URI'] = mongodb_url

mongo = PyMongo(app)

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
                    'tags':[x.lower() for x in request.form.getlist('tags')]
                    }
        collection.insert(document)
        return redirect('/')

@app.route('/tag/<tag>')
def tag_search(tag):
    collection = mongo.db.rules
    rules = collection.aggregate([{"$match":{"tags":{"$in":[tag]}}},{ "$addFields": 
            {"difficulty_average": 
                { "$avg": "$difficulty" }
            }
        }])
    return render_template('index.html', rules=rules)

@app.route('/difficulty/<int:difficulty>')
def difficulty_search(difficulty):
    collection = mongo.db.rules
    rules = collection.aggregate([{ 
        "$addFields":{
            "difficulty_average": { 
                "$avg": "$difficulty" 
            }
        }
        
    },
    {
        "$match":{
            "difficulty_average": { 
                "$gte": difficulty-0.5, 
                "$lt": difficulty+0.5
            }
        }
    }
    ])
    
    return render_template('index.html', rules=list(rules))

@app.route('/rule/<objectID>')
def rule_detail(objectID):
    collection = mongo.db.rules
    rule = collection.find_one({"_id": ObjectId(objectID)})
    return render_template('rule.html',rule=rule)

@app.route('/updaterule',methods=['GET','POST'])
def updaterule():
    if request.method == "POST":
        collection = mongo.db.rules
        collection.update(
            {"_id": ObjectId(request.form['_id'])}, 
            {'$push': {'difficulty':int(request.form['difficulty'])}}
            )
        return redirect('/rule/'+request.form['_id'])