# Name: Joshua Venable
# Date: 12/26/2022
# Description: After giving the student's classes, and what days of the week they are held, this program will export the dates of the classes to a .csv file.
# Notes:
# v.1.0.0

import pandas as pd

valid_days = ["M", "T", "W", "R", "F", "S", "U"]  # Valid days of the week


def main():
    """Main function."""
    class_ser = get_student_classes()
    correct_days = False

    while (not correct_days):
        class_dict = get_student_class_days(class_ser)

        pretty_print(class_dict)

        correct_days = confirm_days()

    export_to_csv(class_dict)

    get_semester_start_end()


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
                day in valid_days for day in answer) and answer != "n" and answer != ""):
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


def export_to_csv(class_days: dict):
    """Export the class days to a csv file.

    Args:
        class_days (dict): A dictionary of the student's classes and the days of the week that they are held.
    """

    class_days_df = pd.DataFrame(
        index=valid_days, columns=class_days.keys(), dtype=bool)

    # Check if the class is held on a day and set the value to True
    for (class_, days) in class_days.items():
        class_days_df[class_] = False
        for day in days:
            class_days_df.loc[day, class_] = True

    class_days_df.to_csv("class_days.csv", index_label="Day")
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
        print(f"Invalid date: {start_date}" if pd.to_datetime("start_date", errors="coerce") is pd.NaT else f"Invalid date: {end_date}")
        return get_semester_start_end()

    return (start_date, end_date)
