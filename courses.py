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
    current_cgpa = round(sum_grade_point/completed_credit, 2)
    print(f'Current CPGA is {current_cgpa}')

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
    print(f'Remaining credit is {remaining_credit} \nComplete credit is {completed_credit}')    
            
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
    print(f'Remaining Credit/No Credit option is {total} \nYou used for Credit/No Credit option for {lst}' )
    
'''def target_gpa(courses: dict):
    """
    목표 gpa를 맞추기 위해 몇 점을 받아야 하는지
    """
    goal_credit = input("Input your goal credits (.5 or .0 format): ")
    goal_credit = float(goal_credit)
    completed_credit = calculate_remaining_credit(courses)[1]
    additional_credit = goal_credit - completed_credit
    
    goal_gpa = input("Input your goal GPA: ")
    goal_gpa = float(goal_gpa)
    
    total_grade_points = get_grades_point_completed_credit(courses)[0]
    
    if goal_credit % 0.5 != 0:
        print('Invalid credit. It has to be either .5 or .0')
        return
    elif goal_credit <= calculate_remaining_credit(courses)[1]:
        print('Less or equal than completed credits')
        return
    else:
        total_credits = completed_credit + additional_credit
        goal_grade_point = goal_gpa * goal_credit
        gap = goal_grade_point - 
    print(gap)'''
    
     
def conflict_course(course_lst1: list, course_lst2: list) -> list:
    """
    통계학과와 수학학과에서 겹치는 코스 찾기
    """
    final_lst = []
    for item in course_lst1:
        if item in course_lst2:
            final_lst.append(item)
    return final_lst


# Math Major

def math_major_complete_condition():
    """
    수학 전공 요건 맞추기

    First Year:
    MAT102H5
    [( MAT132H5 or MAT135H5 or MAT137H5 or MAT157H5) and ( MAT134H5 or MAT136H5 or MAT139H5 or MAT159H5)] or MAT134Y5 or MAT135Y5 or MAT137Y5 or MAT157Y5
    MAT223H5 or MAT240H5

    Second Year:
    MAT202H5 and MAT244H5
    [( MAT232H5 or MAT233H5) and MAT236H5] or MAT257Y5
    MAT224H5 or MAT247H5
   
    Higher Years:
    MAT301H5 and ( MAT334H5 or MAT354H5)
    MAT337H5 or MAT378H5 or MAT392H5 or MAT405H5
    MAT305H5 or MAT311H5 or MAT332H5
    MAT302H5 or MAT315H5 or MAT344H5
    STA256H5 or 0.5 credit of MAT at the 300/ 400 level, except MAT322H5
    0.5 additional credits in MAT at the 400 level
    """
    condition_name1 = 'MAT102H5'
    condition_name2 = '[( MAT232H5 or MAT233H5) and MAT236H5] or MAT257Y5'
    condition_name3 = 'MAT224H5 or MAT247H5'
    condition_name4 = 'MAT301H5 and ( MAT334H5 or MAT354H5)'
    condition_name5 = 'MAT337H5 or MAT378H5 or MAT392H5 or MAT405H5'
    condition_name6 = 'MAT305H5 or MAT311H5 or MAT332H5'
    condition_name7 = 'MAT302H5 or MAT315H5 or MAT344H5'
    condition_name8 = 'STA256H5 or 0.5 credit of MAT at the 300/ 400 level, except MAT322H5'
    condition_name9 = '0.5 additional credits in MAT at the 400 level'
    
    condition1 = False # MAT102H5
    condition2 = False # [( MAT232H5 or MAT233H5) and MAT236H5] or MAT257Y5
    condition3 = False # MAT224H5 or MAT247H5
    condition4 = False # MAT301H5 and ( MAT334H5 or MAT354H5)
    condition5 = False # MAT337H5 or MAT378H5 or MAT392H5 or MAT405H5
    condition6 = False # MAT305H5 or MAT311H5 or MAT332H5
    condition7 = False # MAT302H5 or MAT315H5 or MAT344H5
    condition8 = False # STA256H5 or 0.5 credit of MAT at the 300/ 400 level, except MAT322H5
    condition9 = False # 0.5 additional credits in MAT at the 400 level

    for course in taken_courses:
        if course == 'MAT102H5':
            print(f'You passed first conditons out of 9. Condition 1 is {condition_name1}')
            condition1 = True
            break
    for course in taken_courses:
        if course in ['MAT232H5', 'MAT233H5']:
            for another_course in taken_courses:
                if another_course == 'MAT236H5':
                    # print(f'You passed second conditons out of 9. Condition 2 is {condition_name2}')
                    condition2 = True
                    break
                else:
                    print(f'You have to take MAT236H5 to meet {condition_name2}')
                    break
        elif course == 'MAT257Y5':
            print(f'You passed second conditons out of 9. Condition 2 is {condition_name2}')
            condition2 = True
            break
        else:
            pass
    for course in taken_courses:
        if course == ['MAT224H5', 'MAT247H5']:
            print(f'You passed second conditons out of 9. Condition 3 is {condition_name3}')
            condition3 = True
            break
        else:
            print(f'You have to take either MAT224H5 or MAT247H5 to meet {condition_name3}')
            break
    for course in taken_courses:
        if course == 'MAT301H5':
            for another_course in taken_courses:
                if another_course in ['MAT334H5', 'MAT354H5']:
                    print(f'You passed fourth conditons out of 9. Condition 4 is {condition_name4}')
                    condition4 = True
                    break
                else:
                    print(f'You have to take either MAT334H5 or MAT354H5 to meet {condition_name4}')
                    break
        else:
            print(f'You have to take MAT301H5 first followed by MAT334H5 or MAT354H5 (Condition 4: {condition_name4} )')
            break
    for course in taken_courses:
        if course in ['MAT337H5', 'MAT378H5', 'MAT392H5', 'MAT405H5']:
            print(f'You passed fifth conditons out of 9. Condition 5 is {condition_name5}')
            condition5 = True
            break
    for course in taken_courses:
        if course in ['MAT305H5', 'MAT311H5', 'MAT332H5']:
            print(f'You passed sixth conditons out of 9. Condition 6 is {condition_name6}')
            condition6 = True
            break
        else:
            print(f'You have to take one of MAT305H5, MAT311H5, MAT332H5 to satisfy condition 6 {condition_name6}')
            break
    for course in taken_courses:
        if course in ['MAT302H5', 'MAT315H5', 'MAT344H5']:
            print(f'You passed seventh conditons out of 9. Condition 7 is {condition_name7}')
            condition7= True
            break
        else:
            print(f'You have to take one of MAT302H5, MAT315H5, MAT344H5 to satisfy condition 7 {condition_name7}')
            break
    condition8_course = ''
    for course in taken_courses:
        if course == 'STA256H5':
            print(f'You passed eighth conditons out of 9. Condition 8 is {condition_name8}')
            condition8 = True
            break
        elif course[3:4] in ['3', '4']:
            if course[0:2] == 'MAT':
                if course != 'MAT322H5':
                    course = condition8_course
                    print(f'You passed eighth conditons out of 9. Condition 8 is {condition_name8}')
                    condition8 = True
                    break
        else:
            print(f'You have to take STA256H5 or 0.5 credit of MAT at the 300/ 400 level, except MAT322H5 to satisfy {condition_name8}')
            break
    for course in taken_courses:
        if course[3:4] == '4':
            if course[0:2] == 'MAT':
                if course != condition8_course:
                    print(f'You passed nineth conditons out of 9. Condition 9 is {condition_name9}')
                    condition9 = True
                    break
        else:
            print(f'You have to take one credit for 400 level to satisfy condition 9 {condition_name9}')
            break
    if condition1 and condition2 and condition3 and condition4 and condition5 and \
   condition6 and condition7 and condition8 and condition9:
       print("Congrat! You completed math major")
    else:
        false_conditions = sum([not condition1, not condition2, not condition3, not condition4, not condition5, 
                                not condition6, not condition7, not condition8, not condition9])
        print(f"You have {false_conditions} condition(s) that are not met ouf of 9.")
        
   

'''if __name__ == '__main__':
    print(target_gpa(taken_courses))
    # print(target_gpa(taken_courses))
    
    # print(get_grades(taken_courses))
    # print(get_cgpa(taken_courses))
    
    # print(calculate_remaining_credit(taken_courses))
    
    # print(remaining_cr(taken_courses))
    
    # print(math_major_complete_condition())'''
