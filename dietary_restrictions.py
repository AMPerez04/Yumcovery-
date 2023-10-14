from datetime import date
from enum import Enum
from flask import Flask, request
from customDataClasses import Sex, Goal, User

from mongoHandler import store_user

#Dietary Retrictions for the user


class Allergies(Enum):
    peanuts = 1
    tree_nuts =2
    milk =3
    egg =4
    wheat =5
    soy =6
    fish =7
    shellfish =8
    sesame =9
    mustard =10
    celery =11
    lupin =12
    sulphites =13
    kiwi =14
    sunflower_seeds =15
    poppy_seeds =16
    buckwheat =17
    mango =18
    garlic = 19
    onion = 20
    fava_beans =21
    pineapple =22
    mushrooms = 23
    strawberries = 24
    corn = 25
    triticale = 26
    carrot = 27
    avocado = 28
    bell_pepper = 29
    potato = 30
    pumpkin = 31
    
    

@app.route('/diet_restrict', methods=['POST'])
def dietary_restrictions():
    #a person can have multiple allergies
    #everything in the dietary restrictions will prevent those categoriey(s) of food from being suggested by the algorithm in the final
    #suggestions. 
    allergy = request.form('allergy')
    if allergy not in Allergies._member_names_:
        return {"error": "Invalid allergy provided."}, 400
    store_user_allergy(allergy)
    