# Name: Joshua Venable
# Date: 12/26/2022
# Description: After giving the student's classes, and what days of the week they are held, this program will export the dates of the classes to a .csv file.
# Notes:
# v.1.0.0

import utils

if __name__ == '__main__':
    class_ser = utils.get_student_classes()
    class_dict = utils.get_student_class_days(class_ser)
    utils.pretty_print(class_dict)
