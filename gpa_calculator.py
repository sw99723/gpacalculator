import streamlit as st
import json

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

def input_grades(username):
    st.write("Enter your course information:")
    st.write("Format: Course Name: Score")
    st.write("Example: ANT102H5: 66")
    st.write("Leave a blank line to finish entering grades.")

    taken_courses = {}

    courses = st.text_area("Enter your courses and scores (e.g., MAT135H5: 73, MAT136H5: 76)")
    courses = courses.strip()
    course_list = courses.split(',')

    if courses:
        course_list = courses.strip().split('\n')

        for course in course_list:
            courses = course.split(':')
            if len(courses) == 2:  # Check if the course info is correctly formatted
                course_name = courses[0].strip()
                score = courses[1].strip()
                taken_courses[course_name] = int(score)

    # Save the taken_courses to user's data file
    save_user_data(username, taken_courses)

    return taken_courses

def load_user_data(username):
    # Load the user's data from JSON file
    try:
        with open(f"{username}_data.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}

def save_user_data(username, data):
    # Save the user's data to JSON file
    with open(f"{username}_data.json", "w") as file:
        json.dump(data, file)
        
def register_user(username, password):
    # Check if the username is available
    if not is_username_taken(username):
        # Create a new user with the given username and password
        user_data = {"password": password}
        save_user_data(username, user_data)
        return True
    else:
        return False

def is_username_taken(username):
    # Check if the username is already taken
    # For example, check if the user's data file exists
    return os.path.isfile(f"{username}_data.json")

def authenticate(username, password):
    # Authenticate the user based on the provided username and password
    # For example, compare the password with the stored password in the user's data file
    user_data = load_user_data(username)
    if user_data and user_data.get("password") == password:
        return True
    else:
        return False
    

def get_grades(username):
    # Load the user's data
    data = load_user_data(username)

    updated_courses = {}

    for course_name, score in data.items():
        if isinstance(score, int):
            for grade_value, info in grade_scheme.items():
                percentage_range = info["Percentage"]
                if int(percentage_range[0]) <= score <= int(percentage_range[1]):
                    grade_point = info["Grade Point"]
            updated_courses[course_name] = (score, grade_point)

    return updated_courses

def get_grades_point_completed_credit(username):
    updated_courses = get_grades(username)
    completed_credit = 0.0
    sum_grade_point = 0.0

    for course, course_info in updated_courses.items():
        period_sign = course[6:7]
        if period_sign == 'H':
            if isinstance(course_info[1], float):
                completed_credit += 0.5
                sum_grade_point += course_info[1] * 0.5
        elif period_sign == 'Y':
            if isinstance(course_info[1], float):
                completed_credit += 1.0
                sum_grade_point += course_info[1] * 1.0

    return (sum_grade_point, completed_credit)

def get_cgpa(username):
    sum_grade_point = get_grades_point_completed_credit(username)[0]
    completed_credit = get_grades_point_completed_credit(username)[1]
    current_cgpa = round(sum_grade_point / completed_credit, 2)
    st.write(f'Current CGPA is {current_cgpa}')

def main():
    st.title("GPA Calculator")
    st.write("Welcome to the GPA calculator!")

    # Get the username and password from the user
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if the user is registering for the first time
    if not is_username_taken(username):
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already taken. Please choose a different username.")
        return

    # Perform authentication (e.g., check if username and password match)
    if authenticate(username, password):
        # If authentication succeeds, continue
        if st.button("Calculate GPA"):
            get_cgpa(username)

        # ... Rest of the code

    # If authentication fails, show an error message
    else:
        st.error("Invalid username or password")

if __name__ == "__main__":
    main()
