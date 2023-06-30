import streamlit as st
from queue import Queue

math_major = ['MAT102H5', 'MAT132H5', 'MAT134H5', 'MAT135H5', 'MAT136H5', 'MAT134Y5',
              'MAT135Y5', 'MAT137Y5', 'MAT157Y5', 'MAT223H5', 'MAT240H5', 'MAT202H5',
              'MAT244H5', 'MAT232H5', 'MAT233H5', 'MAT257Y5', 'MAT236H5', 'MAT224H5',
              'MAT247H5', 'MAT301H5', 'MAT334H5', 'MAT354H5', 'MAT337H5', 'MAT378H5',
              'MAT392H5', 'MAT405H5', 'MAT305H5', 'MAT315H5', 'MAT344H5', 'STA256H5']

stat_major = ['CSC108H5', 'MAT102H5', 'MAT132H5', 'MAT134H5', 'MAT135H5', 'MAT136H5',
              'MAT134Y5', 'MAT135Y5', 'MAT137Y5', 'MAT157Y5', 'MAT223H5', 'MAT240H5',
              'MAT232H5', 'MAT233H5', 'MAT257Y5', 'STA256H5', 'STA258H5', 'STA260H5',
              'STA302H5', 'STA304H5', 'STA305H5', 'CSC322H5', 'CSC311H5', 'CSC411H5',
              'MAT302H5', 'MAT311H5', 'MAT332H5', 'MAT334H5', 'MAT344H5', 'MAT337H5',
              'MAT378H5']

grade_scheme = {"A+": {"Grade Point": 4.0, "Percentage": (90, 100)},
                "A": {"Grade Point": 4.0, "Percentage": (85, 89)},
                "A-": {"Grade Point": 3.7, "Percentage": (80, 84)},
                "B+": {"Grade Point": 3.3, "Percentage": (77, 79)},
                "B": {"Grade Point": 3.0, "Percentage": (73, 76)},
                "B-": {"Grade Point": 2.7, "Percentage": (70, 72)},
                "C+": {"Grade Point": 2.3, "Percentage": (67, 69)},
                "C": {"Grade Point": 2.0, "Percentage": (63, 66)},
                "C-": {"Grade Point": 1.7, "Percentage": (60, 62)},
                "D+": {"Grade Point": 1.3, "Percentage": (57, 59)},
                "D": {"Grade Point": 1.0, "Percentage": (53, 56)},
                "D-": {"Grade Point": 0.7, "Percentage": (50, 52)},
                "F": {"Grade Point": 0.0, "Percentage": (0, 49)}}

taken_courses = {'ANT102H5': 66, 'MAT102H5': 56, 'ANT101H5': 69, 'CSC108H5': 77,
                 'SOC100H5': 53, 'MAT135H5': 73, 'MAT136H5': 76, 'MAT223H5': 68,
                 'MAT232H5': 75, 'STA256H5': 68, 'RLG203H5': 78}

def get_grades(courses: dict) -> dict:
    """
    현재 가지고 있는 taken_courses를 코스 이름을 키로 하고
    밸류를 점수와 grade point로 하는 딕셔너리로 바꿈
    """
    for course_name, score in courses.items():
        if isinstance(score, int):
            for grade_value, info in grade_scheme.items():
                percentage_range = info["Percentage"]
                if int(percentage_range[0]) <= score <= int(percentage_range[1]):
                    grade_point = info["Grade Point"]
            taken_courses[course_name] = (courses[course_name], grade_point)
    return taken_courses

def get_grades_point_completed_credit(courses: dict) -> (float, float):
    """
    gpa에 계산되는 grade point와 complete credits 구하기
    """
    updated_dict = get_grades(taken_courses)
    completed_credit = 0.0
    sum_grade_point = 0.0
    for course in updated_dict:
        period_sign = course[6:7]
        if period_sign == 'H':
            if isinstance(updated_dict[course][1], float):
                completed_credit += 0.5
                sum_grade_point += updated_dict[course][1] * 0.5
        elif period_sign == 'Y':
            if isinstance(updated_dict[course][1], float):
                completed_credit += 1.0
                sum_grade_point += updated_dict[course][1] * 1.0
    return (sum_grade_point, completed_credit)


def get_cgpa(courses: dict):
    """
    현재 CGPA 구하기

    Grade Point * Credit (0.5 or 1.0) / Total Credit (Except CR/NCR)
    """
    sum_grade_point = get_grades_point_completed_credit(courses)[0]
    completed_credit = get_grades_point_completed_credit(courses)[1]
    current_cgpa = round(sum_grade_point / completed_credit, 2)
    st.write(f'Current CPGA is {current_cgpa}')


def calculate_remaining_credit(courses: dict) -> (float, float):
    """
    20개 크레딧 중 몇 크레딧을 더 들어야 하는지

    (remaining credit, completed credit)
    """
    completed_credit = 0.0
    updated = get_grades(courses)
    for course in updated:
        if course[6:7] == 'H':
            if isinstance(updated[course][0], int):
                if updated[course][0] >= 50:
                    completed_credit += 0.5
            elif updated[course] == 'CR':
                completed_credit += 0.5
            elif updated[course] == 'NCR':
                completed_credit += 0.0
        elif course[6:7] == 'Y':
            if isinstance(updated[course][0], int):
                if updated[course][0] >= 50:
                    completed_credit += 1.0
            elif updated[course] == 'CR':
                completed_credit += 1.0
            elif courses[course] == 'NCR':
                completed_credit += 0.0
    remaining_credit = 20.0 - completed_credit
    return (remaining_credit, completed_credit)


def print_calculate_remaining_credit(courses: dict):
    remaining_credit = calculate_remaining_credit(courses)[0]
    completed_credit = calculate_remaining_credit(courses)[1]
    st.write(f'Remaining credit is {remaining_credit} \nComplete credit is {completed_credit}')


def remaining_cr(courses: dict):
    """
    2개의 CR/NCR 중 몇 개 사용했는지/몇 개 남았는지
    """
    total = 2.0
    lst = []
    for course in courses:
        if courses[course] == 'CR' or courses[course] == 'NCR':
            if course[6:7] == 'H':
                total -= 0.5
                lst.append(course)
            elif course[6:7] == 'Y':
                total -= 1.0
                lst.append(course)
    st.write(f'Remaining Credit/No Credit option is {total} \nYou used for Credit/No Credit option for {lst}')


def main():
    st.title("GPA Calculator")
    st.write("Welcome to the GPA calculator!")
    st.write("Enter your course information to calculate your GPA.")

    courses = st.text_area("Enter your courses and scores (e.g., MAT135H5: 73, MAT136H5: 76)")
    courses = courses.strip()
    course_list = courses.split(',')

    taken_courses = {}
    for course in course_list:
        course_info = course.split(':')
        course_name = course_info[0].strip()
        score = course_info[1].strip()
        taken_courses[course_name] = int(score)

    if st.button("Calculate GPA"):
        get_cgpa(taken_courses)

    if st.button("Calculate Remaining Credit"):
        print_calculate_remaining_credit(taken_courses)

    if st.button("Calculate Remaining CR/NCR"):
        remaining_cr(taken_courses)


if __name__ == "__main__":
    main()