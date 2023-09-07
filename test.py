import re
import pandas as pd

class StudentWeeklyResult:
    def __init__(self, username):
        self.username = username
        self.weekly_result =        [999, 999, 999, 999, 999, 999, 999, 999, 999]
        self.weekly_correct_ratio = [999, 999, 999, 999, 999, 999, 999, 999, 999]

df_grades = pd.read_excel("FIT9136_S2_2022 Grades.xlsx")
df_student_answer_quiz = pd.read_csv("student_answer_quiz_result.csv", delimiter=";")
df_quiz_set_link = pd.read_csv("quiz_set_link.csv", delimiter=";")
df_quiz = pd.read_csv("quiz.csv", delimiter=";")

print(df_grades.head())
print(df_student_answer_quiz.head())
print(df_quiz_set_link.head())

quiz_correct_answer_dict = dict(zip(list(df_quiz["id"]), list(df_quiz["correct_option_num"])))
quiz_set_link_dict = dict()

for index, row in df_quiz_set_link.iterrows():
    quiz_set_link_dict[row["id"]] = (row["quiz_set_id"], row["quiz_set_title"])

print(quiz_set_link_dict)
print(quiz_correct_answer_dict)

print(df_grades[["Username", "First name", "Surname", "Email address",
                 "Assignment: Assignment 1 - Programming Project I (15%) (Real)",
                 "Assignment: Assignment 2 - Programming Project II (30%) (Real)",
                 "Moodle Quiz - (20%) (Real)",
                 "Assignment: Assignment 3 - Programming Project III (35%) (Real)",
                 "Unit total (Real)"]])
count_username_dict = dict()
count = 0
print("valid_comment;id;student_id;username;fullname;quiz_id;correct_answer_num;selected_answer_num;quiz_set_link_id;quiz_set_desc;create_time")

student_weekly_data_dict = dict()

for index, row in df_student_answer_quiz.iterrows():
    # print(row["username"], row["fullname"])

    itemid = row["id"]
    student_id = row["student_id"]
    username = row["username"]
    fullname = row["fullname"]
    quiz_id = row["quiz_id"]
    selected_answer_num = row["selected_answer_num"]
    quiz_set_link_id = row["quiz_set_link_id"]
    create_time = row["create_time"]

    my_key = username.lower() + "_____" + str(quiz_set_link_id)

    if my_key not in count_username_dict.keys():
        count_username_dict[my_key] = 1
    else:
        count_username_dict[my_key] += 1

    if username not in student_weekly_data_dict.keys():
        student_weekly_data_dict[username] = StudentWeeklyResult(username)

    # if username.lower() in list(df_grades["Email address"]):
    #     print("---------------valid----------------------------------------", itemid, student_id, username, fullname, quiz_id, quiz_correct_answer_dict[int(quiz_id)], selected_answer_num, quiz_set_link_id, quiz_set_link_dict[int(quiz_set_link_id)], create_time, sep=";")
    # else:
    #     print("***************possible drop-not in list********************", itemid, student_id, username, fullname, quiz_id, quiz_correct_answer_dict[int(quiz_id)], selected_answer_num, quiz_set_link_id, quiz_set_link_dict[int(quiz_set_link_id)], create_time, sep=";")

    temp_week_id = quiz_set_link_dict[int(quiz_set_link_id)][0]

    if (student_weekly_data_dict[username].weekly_result[temp_week_id - 8] == 999):
        if quiz_correct_answer_dict[int(quiz_id)] == selected_answer_num:
            student_weekly_data_dict[username].weekly_result[temp_week_id - 8] = 1
        else:
            student_weekly_data_dict[username].weekly_result[temp_week_id - 8] = 0
    else:
        if quiz_correct_answer_dict[int(quiz_id)] == selected_answer_num:
            if temp_week_id - 8 == 1 and student_weekly_data_dict[username].weekly_result[temp_week_id - 8] == 6:
                student_weekly_data_dict[username].weekly_result[temp_week_id - 8] = 0
            if temp_week_id - 8 != 1 and student_weekly_data_dict[username].weekly_result[temp_week_id - 8] == 5:
                student_weekly_data_dict[username].weekly_result[temp_week_id - 8] = 0

            student_weekly_data_dict[username].weekly_result[temp_week_id - 8] += 1




    count += 1

# for key, value in count_username_dict.items():
#     if value > 6:
#         print(key)

for key, value in student_weekly_data_dict.items():

    if value.weekly_result[0] != 999:
        value.weekly_correct_ratio[0] = value.weekly_result[0] / 5
    if value.weekly_result[1] != 999:
        value.weekly_correct_ratio[1] = value.weekly_result[1] / 6
    if value.weekly_result[2] != 999:
        value.weekly_correct_ratio[2] = value.weekly_result[2] / 5
    if value.weekly_result[3] != 999:
        value.weekly_correct_ratio[3] = value.weekly_result[3] / 5
    if value.weekly_result[4] != 999:
        value.weekly_correct_ratio[4] = value.weekly_result[4] / 5
    if value.weekly_result[5] != 999:
        value.weekly_correct_ratio[5] = value.weekly_result[5] / 5
    if value.weekly_result[6] != 999:
        value.weekly_correct_ratio[6] = value.weekly_result[6] / 5
    if value.weekly_result[7] != 999:
        value.weekly_correct_ratio[7] = value.weekly_result[7] / 5
    if value.weekly_result[8] != 999:
        value.weekly_correct_ratio[8] = value.weekly_result[8] / 5





# print("valid_comment;id;student_id;username;fullname;quiz_id;correct_answer_num;selected_answer_num;quiz_set_link_id;quiz_set_desc;create_time")
# for key, value in student_weekly_data_dict.items():
#     print()


print("Username;ID number;First name;Surname;Email address;A1;A2;moodle quiz;A3;Unit total (Real);Unit total (Letter);week3;week4;week5;week6;week7;week8;week9;week10;week11")
for index, row in df_grades.iterrows():
    email = row["Email address"]

    if email in student_weekly_data_dict.keys():

        print(row["Username"], row["ID number"], row["First name"], row["Surname"], row["Email address"],
              row["Assignment: Assignment 1 - Programming Project I (15%) (Real)"],
              row["Assignment: Assignment 2 - Programming Project II (30%) (Real)"],
              row["Moodle Quiz - (20%) (Real)"],
              row["Assignment: Assignment 3 - Programming Project III (35%) (Real)"],
              row["Unit total (Real)"],
              row["Unit total (Letter)"],
              student_weekly_data_dict[email].weekly_correct_ratio[0],student_weekly_data_dict[email].weekly_correct_ratio[1],student_weekly_data_dict[email].weekly_correct_ratio[2],
              student_weekly_data_dict[email].weekly_correct_ratio[3],student_weekly_data_dict[email].weekly_correct_ratio[4],student_weekly_data_dict[email].weekly_correct_ratio[5],
              student_weekly_data_dict[email].weekly_correct_ratio[6],student_weekly_data_dict[email].weekly_correct_ratio[7],student_weekly_data_dict[email].weekly_correct_ratio[8],
              sep=";")
    else:
        print(row["Username"], row["ID number"], row["First name"], row["Surname"], row["Email address"],
              row["Assignment: Assignment 1 - Programming Project I (15%) (Real)"],
              row["Assignment: Assignment 2 - Programming Project II (30%) (Real)"],
              row["Moodle Quiz - (20%) (Real)"],
              row["Assignment: Assignment 3 - Programming Project III (35%) (Real)"],
              row["Unit total (Real)"],
              row["Unit total (Letter)"],
              999,
              999,
              999,
              999,
              999,
              999,
              999,
              999,
              999,
              sep=";")


for email in student_weekly_data_dict.keys():
    if email.lower() not in list(df_grades["Email address"]):
        print("null", "null", "null", "null", email,
              "null",
              "null",
              "null",
              "null",
              "null",
              "null",
              student_weekly_data_dict[email].weekly_correct_ratio[0],
              student_weekly_data_dict[email].weekly_correct_ratio[1],
              student_weekly_data_dict[email].weekly_correct_ratio[2],
              student_weekly_data_dict[email].weekly_correct_ratio[3],
              student_weekly_data_dict[email].weekly_correct_ratio[4],
              student_weekly_data_dict[email].weekly_correct_ratio[5],
              student_weekly_data_dict[email].weekly_correct_ratio[6],
              student_weekly_data_dict[email].weekly_correct_ratio[7],
              student_weekly_data_dict[email].weekly_correct_ratio[8],
              sep=";")


