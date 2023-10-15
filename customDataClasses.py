from dataclasses import dataclass
from enum import Enum
from datetime import date
from pprint import pprint

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


class Goal(Enum):
    cut = 1
    maintain = 2
    bulk = 3


class Sex(Enum):
    male = 1
    female = 2


class PA(Enum):  # Physical Activity
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
