import requests
import random
import json
api_key = '9352cf695fe2426f89998c232f7fc973'

def get_menu_items(query, calorie_limit):
    # Replace 'your_endpoint' with the actual endpoint from the Spoonacular API
    url = 'https://api.spoonacular.com/food/menuItems/search'
    url_with_params = f'{url}?query={query}&apiKey={api_key}&maxCalories={calorie_limit}'


    response = requests.get(url_with_params)

    if response.status_code == 200:
        menu_items = response.json()
        return menu_items
    else:
        print(f'Failed to retrieve menu items: {response.status_code}')
        return None

def get_recipe(minCalories, minProtein, minCarbs, minFat, maxCalories, number):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    offset = int(random.random() * 100)
    url_with_params = f'{url}?apiKey={api_key}&minCalories={minCalories}&minProtein={minProtein}&minCarbs={minCarbs}&minFat={minFat}&maxCalories={maxCalories}&intstructionsRequired=TRUE&number={number}&offset={offset}'


    response = requests.get(url_with_params)
    if response.status_code == 200:
        recipe = response.json()
    else:
        print(f'Failed to retrieve menu items: {response.status_code}')
        return None
    if recipe:
        id = recipe["results"][0]["id"]
    else:
        return None
    url = f'https://api.spoonacular.com/recipes/{id}/ingredientWidget.json?apiKey={api_key}'
    url2 = f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey={api_key}'
    url3 = f'https://api.spoonacular.com/food/menuItems/{id}/nutritionLabel.png?apiKey={api_key}'
    response = requests.get(url)
    response2 = requests.get(url2)
    nutLabel = requests.get(url3)
    if (response.status_code == 200) and (response2.status_code == 200):
        recipe_ingredients = response.json()
        recipe_instructions = response2.json()

        if recipe_ingredients and recipe_instructions:
            print()
            print(f'{recipe["results"][0]["title"]}')
            #print(nutLabel)
            print()
            print("ingredients:")
            for item in recipe_ingredients["ingredients"]:
                print(f'{item["name"]}, {item["amount"]["us"]["value"]} {item["amount"]["us"]["unit"]}')

            print()
            print("instructions:")
            for item in recipe_instructions[0]["steps"]:
                print()
                print(f'{item["number"]}. {item["step"]}')

    else:
        print(f'Failed to retrieve menu items: {response.status_code}')
        return None
        
# Usage:

minCalories = 300  # For example, to find menu items under 500 calories
minProtein = 20
minCarbs = 20
minFat = 15
maxCalories = 1000
#location = 'St. Louis, MO'
menu_items = get_recipe(minCalories, minProtein, minCarbs, minFat, maxCalories, 1)

