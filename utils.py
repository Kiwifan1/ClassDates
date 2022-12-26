# Name: Joshua Venable
# Date: 12/26/2022
# Description: After giving the student's classes, and what days of the week they are held, this program will export the dates of the classes to a .csv file.
# Notes:
# v.1.0.0

import pandas as pd


def main():
    """Main function for the program.
    """
    print("Hello World!")
    return


def get_student_classes():
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


def get_student_class_days(classes: pd.Series):
    """Get the days of the week that the student's classes are held.

    Args:
        classes (pd.Series): The student's classes, as a pandas Series.

    Returns:
        dict: A dictionary of the student's classes and the days of the week that they are held.
    """
    class_days = {}

    print("\nEnter the days of the week in the format of M, T, W, R, F, S, U (ex. MWF)\n")

    valid_days = ["M", "T", "W", "R", "F", "S", "U"]

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

    # print the header
    for class_ in class_days:
        print(f"|{class_:^13}|", end="")

    print("\n" + "-" * (15 * len(class_days)))

    # print the days

    for i in range(7):
        for class_ in class_days:
            # print '|' around the days
            if (i < len(class_days[class_])):
                print(f"|{class_days[class_][i]:^13}|", end="")
            else:
                print(f"|{' ':^13}|", end="")
        print()
    return
