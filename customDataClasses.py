from dataclasses import dataclass
from enum import Enum
from datetime import date
from pprint import pprint

<<<<<<< Updated upstream
cumulative_calorie_expenditure_over_time = [0.038,
                                            0.037,
                                            0.038,
                                            0.037,
                                            0.038,
                                            0.037,
                                            0.038,
                                            0.038,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.042,
                                            0.04,
                                            0.037,
                                            0.038,
                                            0.038]
=======


cumulative_calorie_expenditure_over_time = [
    0.038,
    0.075,
    0.113,
    0.150,
    0.188,
    0.225,
    0.263,
    0.301,
    0.343,
    0.385,
    0.427,
    0.469,
    0.511,
    0.553,
    0.595,
    0.637,
    0.679,
    0.721,
    0.763,
    0.805,
    0.847,
    0.887,
    0.924,
    0.962,
    1.000
]
>>>>>>> Stashed changes


class Goal(Enum):
    cut = 1
    maintain = 2
    bulk = 3


class Sex(Enum):
    male = 1
    female = 2


class PA(Enum): #Physical Activity
    Sedentary = 1
    Lightly_active = 2
    Moderately_active = 3
    Very_active = 4
    Incredibly_active = 5


@dataclass
class User:
    name: str
    dob: date
    sex: Sex
    height: int  # inches
    weight: int
    goal: Goal


@dataclass
class Activity:
    total_calories: int
    total_time: int
