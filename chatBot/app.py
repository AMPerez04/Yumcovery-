import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_relevant_query(query):
    # List of keywords related to health, food, or nutrition
    keywords = ['health', 'food', 'nutrition', 'diet', 'exercise', 'vitamin', 'mineral', 'calorie']
    return any(keyword.lower() in query.lower() for keyword in keywords)


@app.route("/templates/chatBot", methods=("GET", "POST"))
def chatBot():
    if request.method == "POST":
        query = request.form["query"]
        if not is_relevant_query(query):
            response = "I would prefer to talk about food and nutrition."
            return redirect(url_for("chatBot", result=response))

        else:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f"You are a health and nutrition assistant, a dietitian, and a chef. {query}",
                temperature=0.4,
                max_tokens=50
            )
        return redirect(url_for("chatBot", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("chatBot.html", result=result)


# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )
