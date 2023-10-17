from collections import defaultdict
from datetime import datetime, date, timedelta

from flask import Flask, request, render_template
from customDataClasses import Sex, Goal, User, cumulative_calorie_expenditure_over_time
from spoonacularAPI import get_menu_items

from mongoHandler import *

app = Flask(__name__)

queue_cache = defaultdict(dict)


@app.route("/createUser", methods=["GET"])
def create_user_form():
    return render_template("createUser.html")


@app.route("/dashboard", methods=["GET"])
def create_dashboard():
    return render_template("dashboard.html")


@app.route("/createUser", methods=["POST"])
def create_user():
    name = request.form["name"]
    # need a floor function of DOB
    dob = date.fromisoformat(request.form["dob"])
    sex = Sex[request.form["sex"]]
    height_inches = int(request.form["height"])  # needs to be in inches
    weight_in_lbs = int(request.form["pounds"])  # needs to be in kilos
    goal = Goal[request.form["goal"]]
    # get form data
    store_user(User(name, dob, sex, height_inches, weight_in_lbs, goal))
    # response showing success
    return "User created successfully"


@app.route("/meal")
def get_meal():
    user_id = request.args.get("user_id")

    nutritionists_suggestions(user_id)  # we will return from here


def nutritionists_suggestions(user_id):
    """
    :param user_id: the user id of the user


    """
    queue_cache[user_id]["user_data"] = get_user(user_id)
    queue_cache[user_id]["activity"] = get_activity(user_id)

    caloric_goal = calc_calorie_intake_target(user_id)
    level = physical_activity_level(user_id)

    kilos_per_pound = 0.453592
    weight_kilos = queue_cache[user_id]["user_data"]["weight"] * kilos_per_pound
    protein, fat, carbs = get_macros(caloric_goal, weight_kilos, level)

    user_goal = queue_cache[user_id]["user_data"].goal  # user goal
    # no print statements
    if user_goal == Goal.cut:
        meals = get_menu_items(max_protein=protein, max_fat=fat, max_carbs=carbs, max_calories=caloric_goal)
    elif user_goal == Goal.maintain:
        meals = get_menu_items(protein - 5, protein + 5, fat - 3, fat + 3, carbs - 10, carbs + 10, caloric_goal - 100,
                               caloric_goal + 100)
    else:
        meals = get_menu_items(min_protein=protein, min_fat=fat, min_carbs=carbs, min_calories=caloric_goal)

    print(protein, fat, carbs)
    del queue_cache[user_id]


def physical_activity_level(user_id):
    # intense excersing minutes
    intense_excercising_seconds = queue_cache[user_id]["activity"][
        "data"][0]["active_durations_data"]["activity_seconds"]
    intense_excercising_minutes = intense_excercising_seconds / 60

    if intense_excercising_minutes == 0:
        return 1
    elif 0 < intense_excercising_minutes <= 15:
        return 2
    elif 15 < intense_excercising_minutes <= 30:
        return 3
    elif 30 < intense_excercising_minutes <= 45:
        return 4
    else:
        return 5


def get_macros(calorie_goal: float, weight_in_kg, physical_acticvity):
    """
    :param calorie_goal: the calorie goal of the user
    :param weight_in_kg: the weight of the user in kilograms
    :param physical_acticvity: the physical activity level of the user

    :return: a tuple of the macros in grams
    """
    calories_per_gram = {"fat": 9, "protein": 4, "carbs": 4}
    # the physical_activity_ratio is calculated with 0.8 grams of protein per kilo

    physical_activity_ratio = 0.8 + ((physical_acticvity - 1) * 0.2)

    protein = physical_activity_ratio * weight_in_kg * 4
    fat = 0.2 * calorie_goal
    carbs = calorie_goal - (protein + fat)

    return (
        protein / calories_per_gram["protein"],
        fat / calories_per_gram["fat"],
        carbs / calories_per_gram["carbs"],
    )


def calc_calorie_intake_target(user_id: str):
    CALORIE_ADJUSTMENT = 500

    user_data = queue_cache[user_id]["user_data"]
    activity = queue_cache[user_id]["activity"]

    data = activity["data"][0]
    meta = data["metadata"]
    datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    calories_burned = data["calories_data"]["total_burned_calories"]

    start_time = datetime.strptime(meta["start_time"], datetime_format)
    end_time = datetime.strptime(meta["end_time"], datetime_format)

    total_calories = timed_calories_to_total(
        calories_burned, start_time, end_time)

    if user_data["goal"] == Goal.cut:
        return total_calories - CALORIE_ADJUSTMENT
    elif user_data["goal"] == Goal.bulk:
        return total_calories + CALORIE_ADJUSTMENT
    else:
        return total_calories


def timed_calories_to_total(calories, start_time: datetime, end_time: datetime):
    total = 0.0
    current_time = start_time

    while current_time < end_time:
        next_hour_start = (current_time + timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0
        )

        if next_hour_start > end_time:  # if fractional hour, calculate fraction of hour
            fraction_of_hour = (end_time - current_time).seconds / 3600
            total += (
                    fraction_of_hour
                    * cumulative_calorie_expenditure_over_time[current_time.hour]
            )
            break

        # before next hour, calculate fraction of hour
        fraction_of_hour = (next_hour_start - current_time).seconds / 3600
        total += (
                fraction_of_hour
                * cumulative_calorie_expenditure_over_time[current_time.hour]
        )

        current_time = next_hour_start

    return calories / total


if __name__ == "__main__":
    app.run(debug=True, port=3031)
