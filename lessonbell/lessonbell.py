from datetime import *
import schedule
import time
import tkinter
import json
from notifypy import *

startup_count = 0

monday = None
tuesday = None
wednesday = None
thursday = None
friday = None
saturday = None
sunday = None
print(datetime.now())
datedict = {
    "monday": schedule.every().monday,
    "tuesday": schedule.every().tuesday,
    "wednesday": schedule.every().wednesday,
    "thursday": schedule.every().thursday,
    "friday": schedule.every().friday,
    "saturday": schedule.every().saturday,
    "sunday": schedule.every().sunday,
}
def lesson_bell(lesson_date):
    bell = Notify()
    bell.title = f"Time for {lesson_date}'s lesson."
    bell.audio = "finalalarm.wav"
    bell.icon = "books.jpg"
    bell.message = "Wake up! Time for a lesson"
    bell.send()
    history_file_path = "lessonhistory.json"
    print(datetime.now())
    timenow = datetime.now()
    subject = input("What was this lesson's subject?: ")
    notes = input("Notes from lesson/things to remember: ")
    dict_to_append = {"Lesson Time": timenow.strftime("%Y-%m-%d %H:%M:%S"),
                      "Lesson Subject": subject,
                      "Lesson Notes": notes}
    history_thusfar = []
    with open(history_file_path, "r") as lesson_history:
        history_thusfar = json.load(lesson_history)
        history_thusfar.append(dict_to_append)
    with open(history_file_path, "w") as lesson_history:
        json.dump(history_thusfar, lesson_history, indent= 4)




def validate_time_format(timestr):
    if len(timestr) != 5 or timestr[2] != ':':
        return False
    hours, minutes = timestr.split(':')
    if not hours.isdigit() or not minutes.isdigit():
        return False
    hours, minutes = int(hours), int(minutes)
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return False
    return True


def write_new_lesson_to_json():
    while True:
        while True:
            raw_date_input = input("What day of the week is this lesson?")
            formatted_date_input = raw_date_input.lower()
            if formatted_date_input in datedict:
                break
            else:
                print("Unrecognised Date!")
        while True:
            raw_time_input = input("what time of day does this lesson begin? FORMAT: 15:00")
            if validate_time_format(raw_time_input):
                break
            else:
                print("Unrecognised time format!")

        dict_to_pass = {"Date":formatted_date_input,
                        "Time":raw_time_input}
        file_path = "addedlessons.json"
        existing_data = []
        with open(file_path, "r") as existing_json_data:
            existing_data = json.load(existing_json_data)
        existing_data.append(dict_to_pass)
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
            print("Successfully dumped lesson to json")
        break_prompt = input("Do you want to enter another lesson? Y/N")
        if break_prompt == "Y":
            pass
        if break_prompt == "N":
            break
    startup_menu()


def print_lesson_notes():
    history_file_path = "lessonhistory.json"
    with open(history_file_path, "r") as lessonhistory:
        loaded_lesson_history = json.load(lessonhistory)
        for iterated_dictionary in loaded_lesson_history:
            for key, value in iterated_dictionary.items():
                print(f"{key} : {value}")
            print("")
    startup_menu()



def read_json_for_scheduling():
    file_path = "addedlessons.json"
    with open(file_path, "r") as opened_json_for_reading:
        json_data = json.load(opened_json_for_reading)
        for iterated_dictionary in json_data:
            if "Date" in iterated_dictionary and "Time" in iterated_dictionary:
                iterated_date = iterated_dictionary["Date"]
                iterated_time = iterated_dictionary["Time"]
                datedict[iterated_date].at(iterated_time).do(lesson_bell, lesson_date=iterated_date)
                print(iterated_dictionary["Date"])
                print(iterated_dictionary["Time"])
    pass

def append_scheduled_lessons():

    pass


def startup_menu():
    menu_options = {"1":write_new_lesson_to_json,
                    "2":read_json_for_scheduling,
                    "3":print_lesson_notes}
    menu_prompt = input("What would you like to do? 1. Schedule new lessons  2. Wait for lessons 3. Check Lesson "
                        "notes  ")
    if menu_prompt not in menu_options:
        print("Unrecognised Command")
    menu_selection = menu_options.get(menu_prompt)
    menu_selection()


lesson_bell("monday")
startup_menu()

while True:
    schedule.run_pending()
    time.sleep(1)
