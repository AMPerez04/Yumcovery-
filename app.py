from datetime import date

from flask import Flask, request
from customDataClasses import Sex, Goal, User

from mongoHandler import store_user

app = Flask(__name__)


@app.route('/createUser', methods=['POST'])
def create_user():
    name = request.form['name']
    dob = date.fromisoformat(request.form['dob'])
    sex = Sex[request.form['sex']]
    height = int(request.form['height'])
    weight = int(request.form['weight'])
    goal = Goal[request.form['goal']]
    # get form data
    store_user(User(name, dob, sex, height, weight, goal))
    # response showing success
    return 'User created successfully'


if __name__ == '__main__':
    app.run()
