import requests
import random
import json
import sys

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

def get_recipe(minProtein = 0, maxProtein = sys.maxsize, minFat = 0, maxFat = sys.maxsize, minCarbs = 0, maxCarbs = sys.maxsize, minCalories = 0, maxCalories = sys.maxsize):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    offset = int(random.random() * 100)
    url_with_params = f'{url}?apiKey={api_key}&minCalories={minCalories}&maxProtein={maxProtein}&minProtein={minProtein}&maxCarbs={maxCarbs}&minCarbs={minCarbs}&maxFat={maxFat}&minFat={minFat}&maxCalories={maxCalories}&intstructionsRequired=TRUE&offset={offset}&number=1'

    name = requests.get(url_with_params)
    if name.status_code == 200:
        recipe = name.json()
    else:
        # print(f'Failed to retrieve menu items: {response.status_code}')
        return None
    if recipe:
        id = recipe["results"][0]["id"]
    else:
        return None
    url = f'https://api.spoonacular.com/recipes/{id}/ingredientWidget.json?apiKey={api_key}'
    url2 = f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey={api_key}'
    url3 = f'https://api.spoonacular.com/food/menuItems/{id}/nutritionLabel.png?apiKey={api_key}'
    ingredients = requests.get(url)
    instructions = requests.get(url2)
    nutLabel = requests.get(url3)
    if (ingredients.status_code == 200) and (instructions.status_code == 200):
        recipe_ingredients = ingredients.json()
        recipe_instructions = instructions.json()

        # if recipe_ingredients and recipe_instructions:
        #     print()
        #     print(f'{recipe["results"][0]["title"]}')
        #     #print(nutLabel)
        #     print()
        #     print("ingredients:")
        #     for item in recipe_ingredients["ingredients"]:
        #         print(f'{item["name"]}, {item["amount"]["us"]["value"]} {item["amount"]["us"]["unit"]}')

        #     print()
        #     print("instructions:")
        #     for item in recipe_instructions[0]["steps"]:
        #         print()
        #         print(f'{item["number"]}. {item["step"]}')

    response_dict = {
        'name': name,
        'ingredients': ingredients,
        'instructions': instructions
    }

    return response_dict
        
# Usage:
# menu_items = get_recipe(minProtein = 0, maxProtein = 20, minFat = 0, maxFat = 20, minCarbs = 0, maxCarbs = 20, minCalories = 0, maxCalories = 700)

