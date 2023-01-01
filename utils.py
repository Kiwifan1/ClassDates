# Name: Joshua Venable
# Date: 12/26/2022
# Description: After giving the student's classes, and what days of the week they are held, this program will export the dates of the classes to a .csv file.
# Notes:
# v.1.0.0

import pandas as pd

valid_days = {"M": "Mon", "T": "Tue", "W": "Wed", "R": "Thu",
              "F": "Fri", "S": "Sat", "U": "Sun"}  # Valid days of the week


def main():
    """Main function."""
    class_ser = get_student_classes()
    correct_days = False

    while (not correct_days):
        class_dict = get_student_class_days(class_ser)

        pretty_print(class_dict)

        correct_days = confirm_days()

    export_class_days(class_dict)

    class_dates = get_dates_of_classes(class_dict)

    export_class_dates(class_dates)


def get_student_classes() -> pd.Series:
    """Get the student's classes.

    Returns:
        pandas.Series: The student's classes, as a pandas Series.
    """
    answer = "\0"
    classes = []
    while (answer != "q" and answer != ""):
        answer = input("Enter a class name (q or hit enter to quit): ")
        if (answer != "q" and answer != ""):
            classes.append(answer)

    return pd.Series(classes, dtype=str)


def get_student_class_days(classes: pd.Series) -> dict:
    """Get the days of the week that the student's classes are held.

    Args:
        classes (pd.Series): The student's classes, as a pandas Series.

    Returns:
        dict: A dictionary of the student's classes and the days of the week that they are held.
    """
    class_days = {}

    print("\nEnter the days of the week in the format of M, T, W, R, F, S, U (ex. MWF)\n")

    for class_ in classes:
        answer = "\0"
        days = []
        answer = input(
            f"Enter the days of the week that {class_} is held (n or hit enter to quit): ")

        # Check if all the days are valid
        while (not all(
                day in valid_days.keys() for day in answer) and answer != "n" and answer != ""):
            answer = input(
                f"Invalid Input. Enter the days of the week that {class_} is held (n or hit enter to quit): ")

        if (answer != "n" and answer != ""):
            days = [*answer]  # Unpack the string into a list
        class_days[class_] = days
    return class_days


def pretty_print(class_days: dict):
    """Print the class days in a table format.

    Args:
        class_days (dict): A dictionary of the student's classes and the days of the week that they are held.
    """
    print("\nClass Days")

    if (len(class_days) == 0):
        print("No classes")
        return

    # print the header
    for class_ in class_days:
        print(f"|{class_:^13}|", end="")

    print("\n" + "-" * (15 * len(class_days)))

    # print the days
    for i in range(7):
        for class_ in class_days:
            if (i < len(class_days[class_])):
                print(f"|{class_days[class_][i]:^13}|", end="")
            else:
                print(f"|{' ':^13}|", end="")
        print()
    return


def confirm_days() -> bool:
    """Confirm the days of the week that the student's classes are held.

    Returns:
        bool: True if the days are confirmed, False otherwise.
    """
    answer = input("Are the days correct? (y/n): ")
    if (answer == "y"):
        return True
    return False


def export_class_days(class_days: dict, filename: str = "class_days.csv"):
    """Export the class days to a csv file.

    Args:
        class_days (dict): A dictionary of the student's classes and the days of the week that they are held.
    """

    class_days_df = pd.DataFrame(
        index=valid_days.keys(), columns=class_days.keys(), dtype=str)

    # Check if the class is held on a day and set the value to True
    for (class_, days) in class_days.items():
        class_days_df[class_] = ""
        for day in days:
            class_days_df.loc[day, class_] = "X"

    class_days_df.to_csv(filename, index_label="Day")
    return


def export_class_dates(class_dates: dict, filename: str = "class_dates.csv"):
    """Export the class dates to a csv file.

    Args:
        class_dates (dict): A dictionary of the student's classes and the dates that they are held.
    """
    # make a dataframe where the columns are the classes and the series are the dates

    max_len = max(len(class_dates[class_]) for class_ in class_dates)

    class_dates_df = pd.DataFrame(index=range(
        max_len), columns=class_dates.keys(), dtype=str)

    class_dates_df.fillna(pd.NA, inplace=True)
    
    for (class_, dates) in class_dates.items():
        dates = [date.strftime("%m/%d/%Y") for date in dates]
        if (len(dates) < len(class_dates_df)):
            class_dates_df[class_] = dates + [""] * (len(class_dates_df) - len(dates))
        else:
            class_dates_df[class_] = dates  

    class_dates_df.to_csv(filename, index_label="Index")
    return


def get_semester_start_end() -> tuple:
    """Get the start and end dates of the semester.

    Returns:
        tuple: A tuple of the start and end dates of the semester.
    """
    start_date = input("Enter the start date of the semester (mm/dd/yyyy): ")
    end_date = input("Enter the end date of the semester (mm/dd/yyyy): ")

    # check if dates are valid

    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except ValueError:
        print(f"Invalid date: {start_date}" if pd.to_datetime(
            "start_date", errors="coerce") is pd.NaT else f"Invalid date: {end_date}")
        return get_semester_start_end()

    return (start_date, end_date)


def convert_days_to_weekmask(days: list) -> str:
    """Convert the days of the week to a weekmask.

    Args:
        days (list): A list of the days of the week.

    Returns:
        str: A string of the days of the week in a weekmask format.
    """
    weekmask = ""
    for day in days:
        weekmask += valid_days[day] + " "
    return weekmask.strip()


def get_dates_of_classes(class_days: dict) -> dict:
    """Get the dates of the student's classes.

    Args:
        class_days (dict): A dictionary of the student's classes and the days of the week that they are held.

    Returns:
        dict: A dictionary of the student's classes and the dates of the classes.
    """
    class_dates = {}

    start_date, end_date = get_semester_start_end()

    for (class_, days) in class_days.items():
        weekmask = convert_days_to_weekmask(days)
        class_date = pd.offsets.CustomBusinessDay(weekmask=weekmask)
        dates = pd.date_range(start_date, end_date,
                              freq=class_date, inclusive='both')
        class_dates[class_] = dates

    return class_dates