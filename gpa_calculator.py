import streamlit as st

grade_scheme = {
    "A+": {"Grade Point": 4.0, "Percentage": (90, 100)},
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
    "F": {"Grade Point": 0.0, "Percentage": (0, 49)}
}

taken_courses = {}

def input_grades():
    st.write("Enter your course information:")
    st.write("Format: Course Name: Score")
    st.write("Leave a blank line to finish entering grades.")
    st.write("CR or NCR have to be all UPPER CASE")

    courses = st.text_area("Enter your courses and scores (e.g., MAT135H5: 73, MAT136H5: CR):")
    courses = courses.strip()
    course_list = courses.split(',')

    if courses:
        for course in course_list:
            course_info = course.split(':')
            if len(course_info) == 2:  # Check if the course info is correctly formatted
                course_name = course_info[0].strip()
                score = course_info[1].strip()
                if score.isdigit():
                    for grade_value, info in grade_scheme.items():
                        percentage_range = info["Percentage"]
                        if int(percentage_range[0]) <= int(score) <= int(percentage_range[1]):
                            grade_point = info["Grade Point"]
                            taken_courses[course_name] = (int(score), grade_point)
                elif score == 'CR' or score == 'NCR':
                    taken_courses[course_name] = (str(score), 0.0)

    return taken_courses


def get_cgpa(courses):
    """
    현재 CGPA 구하기

    Grade Point * Credit (0.5 or 1.0) / Total Credit (Except CR/NCR)
    """
    completed_credit = 0.0
    sum_grade_point = 0.0
    for course in courses:
        period_sign = course[6:7]
        if period_sign == 'H':
            if isinstance(courses[course][1], float):
                completed_credit += 0.5
                sum_grade_point += courses[course][1] * 0.5
        elif period_sign == 'Y':
            if isinstance(courses[course][1], float):
                completed_credit += 1.0
                sum_grade_point += courses[course][1] * 1.0
    current_cgpa = round(sum_grade_point / completed_credit, 2)
    st.write(f'Current CGPA is {current_cgpa}')


def calculate_remaining_credit(courses):
    """
    20개 크레딧 중 몇 크레딧을 더 들어야 하는지
    """
    completed_credit = 0.0
    for course in courses:
        if course[6:7] == 'H':
            if isinstance(courses[course][0], int):
                if courses[course][0] >= 50:
                    completed_credit += 0.5
        elif course[6:7] == 'Y':
            if isinstance(courses[course][0], int):
                if courses[course][0] >= 50:
                    completed_credit += 1.0
    remaining_credit = 20.0 - completed_credit
    st.write(f'Remaining credit is {remaining_credit}')
    st.write(f'Completed credit is {completed_credit}')


def remaining_cr(courses):
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
    st.write(f'Remaining Credit/No Credit option is {total}')
    st.write(f'You used Credit/No Credit option for {lst}')


def main():
    st.title("CGPA Calculator")
    st.write("Welcome to the CGPA Calculator!")

    option = st.selectbox("Select an option", ("Calculate CGPA", "Calculate Remaining Credit", "Check Credit/No Credit"))
    
    if option == "Calculate CGPA":
        courses = input_grades()
        get_cgpa(courses)
    
    elif option == "Calculate Remaining Credit":
        courses = input_grades()
        calculate_remaining_credit(courses)
    
    elif option == "Check Credit/No Credit":
        courses = input_grades()
        remaining_cr(courses)


if __name__ == "__main__":
    main()
