import random

import requests

api_key = '9352cf695fe2426f89998c232f7fc973'  # privacy doesn't matter, this is a free api


def get_menu_items(min_protein=None, max_protein=None, min_fat=None, max_fat=None, min_carbs=None, max_carbs=None,
                   min_calories=None, max_calories=None):
    if ((min_protein is None and max_protein is None)
            or (min_fat is None and max_fat is None)
            or (min_carbs is None and max_carbs is None)
            or (min_calories is None and max_calories is None)):
        raise Exception("You must specify at least one min/max pair of macros")

    if min_protein is None or min_fat is None or min_carbs is None or min_calories is None:
        min_protein = max_protein * 0.7
        min_fat = max_fat * 0.7
        min_carbs = max_carbs * 0.7
        min_calories = max_calories * 0.7

    if max_protein is None or max_fat is None or max_carbs is None or max_calories is None:
        max_protein = min_protein * 1.4
        max_fat = min_fat * 1.4
        max_carbs = min_carbs * 1.4
        max_calories = min_calories * 1.4

    num_meals = 1
    endpoint = 'https://api.spoonacular.com/recipes/complexSearch'
    offset = int(random.random() * 100)
    url = f'''
    {endpoint}?apiKey={api_key}&minCalories={min_calories}&maxProtein={max_protein}&minProtein={min_protein}
    &maxCarbs={max_carbs}&minCarbs={min_carbs}&maxFat={max_fat}&minFat={min_fat}&maxCalories={max_calories}
    &intstructionsRequired=TRUE&offset={1}&number={num_meals}'''

    response = requests.get(url)
    if response.status_code == 200:
        meals = response.json()
    else:
        raise Exception(f'Failed to retrieve meal: {response.status_code}')

    meals_list = []
    for i, meal in enumerate(meals["results"]):
        recipe_id = meal["id"]

        ingredient_url = f'https://api.spoonacular.com/recipes/{recipe_id}/ingredientWidget.json?apiKey={api_key}'
        instruction_url = f'https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={api_key}'

        ingredients = requests.get(ingredient_url)
        instructions = requests.get(instruction_url)
        if (ingredients.status_code == 200) and (instructions.status_code == 200):
            recipe_ingredients = ingredients.json()["ingredients"]
            recipe_instructions = instructions.json()

        meals_list.append({
            'name': meals['results'][0]['title'],
            'ingredients': recipe_ingredients,
            'instructions': recipe_instructions
        })

    return meals_list
