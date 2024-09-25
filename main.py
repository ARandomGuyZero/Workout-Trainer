"""
Workout Trainer

Author: Alan
Date: September 25th 2024

Uses APIs to add a row to a worksheet in google Docs.
Nutritionix API: https://www.nutritionix.com/business/api
Sheety API: https://sheety.co/
"""
from requests import post
from os import environ
from datetime import datetime

# Uses the API nutritionix to get the data as json from a query
# For more info: https://docx.syndigo.com/developers/docs/nutritionix-api-guide
TRACKAPI_ENDPOINT = environ["TRACKAPI_ENDPOINT"]
NUTRITIONIX_APP_ID = environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_APP_KEY = environ["NUTRITIONIX_APP_KEY"]

# Uses the Sheety API to add a row
# For some info: https://sheety.co/docs
# User might not use AUTH_USER neither AUTH_PASSWORD
SHEETY_WORKSHEET_ENDPOINT = environ["SHEETY_WORKSHEET_ENDPOINT"]
AUTH_USER = environ["AUTH_USER"]
AUTH_PASSWORD = environ["AUTH_PASSWORD"]

def store_exercises():
    """
    Uses the Nutritionix API to get a json out of a query containing data about exercises
    :return: A dictionary with the lists of each of the exercises done with details
    """
    # Asks the user what exercises they did today
    query = input("Tell me which exercises you did: ")

    # Parameters for the json
    parameters = {
        "query": query,
    }

    # Headers with the API key
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
    }

    # Returns the json with the exercise data
    return post(url=TRACKAPI_ENDPOINT, json=parameters, headers=headers)

def add_row(data_list, workout_date, workout_time):
    """
    Adds a row to the worksheet we use using the data from the nutritionix API
    :param data_list: List of data
    :param workout_date: Date of the workout
    :param workout_time: Time of the workout
    :return:
    """
    # These parameters depend on the cells we will fill in our worksheet
    parameters = {
        "workout": {
            "date": workout_date,
            "time": workout_time,
            "exercise": data_list["name"].title(),
            "duration": data_list["duration_min"],
            "calories": data_list["nf_calories"]
        }
    }

    # Make a post method to add a row to our worksheet
    # User might not use AUTH_USER neither AUTH_PASSWORD
    response = post(
        url=SHEETY_WORKSHEET_ENDPOINT,
        json=parameters,
        auth=(
            AUTH_USER,
            AUTH_PASSWORD,
        )
    )

    print(response.text)

exercise_response = store_exercises().json()

date = datetime.now().strftime("%d%m%Y") # Gets the date formatted as DD/MM/YYYY, eg "12/01/2024"
time = datetime.now().strftime("%X") # Gets the date formatted as HH:MM:SS, eg "15:00:00"

for exercise_list in exercise_response["exercises"]:

    # Adds a row to the worksheet
    add_row(exercise_list, date, time)
