from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import SelectField
from bson.objectid import ObjectId

def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
handle = connect()


class Form(FlaskForm):
    state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')]) 
    city = SelectField('city', choices=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.city.choices = [(city['_id'], city['cities']) for city in handle.location.find({"state":"CA"})]
    if request.method == 'POST':
        selected_city = form.city.data #returns the objectid of the selected city
        city = handle.location.find({"_id" : ObjectId(selected_city)})[0]
        #print(city)
        #city = City.query.filter_by(id=form.city.data).first()
        return '<h1>State: {}, City: {}</h1>'.format(form.state.data, city['cities'])
    return render_template('index.html', form=form)


@app.route('/city/<state>')
def city(state):
    cities = handle.location.find({"state":state})
    cityArray = []
    for city in cities:
        cityObj = {}
        see = str(city["_id"])
        cityObj['id'] = see
        cityObj['state'] = city['state']
        cityObj['city'] = city['cities']
        cityArray.append(cityObj)
        print(see)

    return jsonify({'cities' : cityArray})




if __name__ == '__main__':
    app.run(debug=True)
