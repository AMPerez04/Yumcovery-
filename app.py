from collections import defaultdict
from datetime import datetime, date, timedelta

from flask import Flask, request, render_template
from customDataClasses import Sex, Goal, User, cumulative_calorie_expenditure_over_time

from mongoHandler import store_user, get_activity, get_user

app = Flask(__name__)

queue_cache = defaultdict(dict)


@app.route("/createUser", methods=["GET"])
def create_user_form():
    return render_template("createUser.html")


@app.route("/createUser", methods=["POST"])
def create_user():
    name = request.form["name"]
    dob = date.fromisoformat(request.form["dob"])
    sex = Sex[request.form["sex"]]
    height = int(request.form["height"])
    weight = int(request.form["weight"])
    goal = Goal[request.form["goal"]]
    # get form data
    store_user(User(name, dob, sex, height, weight, goal))
    # response showing success
    return "User created successfully"


@app.route("/meal")
def get_meal():
    user_id = request.args.get("user_id")

    nutritionists_suggestions(user_id)  # we will return from here


def nutritionists_suggestions(user_id):
    queue_cache[user_id]["user_data"] = get_user(user_id)
    queue_cache[user_id]["activity"] = get_activity(user_id)
    caloric_goal = calc_calorie_intake_target(user_id)
    level = physical_activity_level(user_id)
    protein, fat, carbs = get_macros(caloric_goal, queue_cache[user_id]["user_data"]["weight"], level)
    # Create a funciton that takes into account of the user's goal and activity level and adjust accoridng
    # to their goal. Maintain: only suggested
    # bulk: at least
    # cut: at most
    print(protein, fat, carbs)
    del queue_cache[user_id]


def physical_activity_level(user_id):
    # intense excersing minutes
    intense_excercising_minutes = queue_cache[user_id]["activity"] # TODO: actually access intense excersing minutes
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


def get_macros(calorie_goal, weight_in_kg, pa):
    calories_per_gram = {"fat": 9, "protein": 4, "carbs": 4}

    physical_activity_ratio = 0.8 + ((pa - 1) * 0.2)

    protein = physical_activity_ratio * weight_in_kg * 4
    fat = 0.2 * calorie_goal
    carbs = calorie_goal - (protein + fat)

    return (
        protein / calories_per_gram["protein"],
        fat / calories_per_gram["fat"],
        carbs / calories_per_gram["carbs"],
    )  # returns the calories of protein, fat, and carbs


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
    app.run()
