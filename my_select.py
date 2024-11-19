from connect import session
from models import (
    Student,
    Group,
    Subject,
    Teacher,
    Mark,
    groups_m2m_students,
    students_m2m_subjects,
)
from sqlalchemy import and_, func
from tabulate import tabulate

OKGREEN = "\033[92m"
ENDC = "\033[0m"


# select top-5 students with the highest average mark
def select_1():
    # round average mark to 2 decimal places
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")

    # select top-5 students with the highest average mark
    query = (
        session.query(Mark.student_id, Student.name, avg_mark)
        .join(Student, Mark.student_id == Student.id)
        .group_by(Mark.student_id, Student.name)
        .order_by(avg_mark.desc())
        .limit(5)
        .all()
    )

    # prepare data for the table
    table_data = [
        (student_id, name, average_mark) for student_id, name, average_mark in query
    ]
    headers = ["Student ID", "Student Name", "Average Mark"]

    # print the table
    print(OKGREEN + "Task 1: Top-5 students with the highest average mark" + ENDC)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# to find the student with the highest average mark for a specific subject
def select_2(subject_name="English"):
    # round average mark to 2 decimal places
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")

    query = (
        session.query(Mark.student_id, Student.name, Subject.name, avg_mark)
        .join(Student, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Mark.student_id, Student.name, Subject.name)
        .order_by(avg_mark.desc())
        .first()
    )

    # prepare data for the table
    table_data = [(query.student_id, query[1], query.name, query.average_mark)]
    headers = ["Student ID", "Student Name", "Subject", "Average Mark"]

    # print the table
    print(
        OKGREEN
        + "Task 2: The student with the highest average mark for a specific subject"
        + ENDC
    )
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# get average mark in each group from some subject
def select_3(subject_name="English"):
    # round average mark to 2 decimal places
    avg_mark = func.round(func.avg(Mark.mark).label("average_mark"))

    query = (
        session.query(Group.name, Subject.name, avg_mark)
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .join(Mark, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name, Subject.name)
        .all()
    )

    # prepare data for the table
    table_data = [
        (group_name, subject, average_mark)
        for group_name, subject, average_mark in query
    ]
    headers = ["Group Name", "Subject", "Average Mark"]

    # print the table
    print(OKGREEN + "Task 3: Average mark in each group from some subject" + ENDC)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# find general average mark
def select_4():
    # round average mark to 2 decimal places
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")

    # select top-5 students with the highest average mark
    query = session.query(avg_mark).scalar()

    # print the result
    print(f"{OKGREEN}Task 4: Average mark: {query}{ENDC}")

    session.close()


# get which subjects a specific teacher teaches
def select_5():
    query = (
        session.query(
            Teacher.name, func.string_agg(Subject.name, ", ").label("subjects")
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .group_by(Teacher.id)
        .all()
    )
    for teacher_name, subjects in query:
        print(f"Teacher: {teacher_name}, Subjects: {subjects}")
        # prepare data for the table
    table_data = [(teacher_name, subjects) for teacher_name, subjects in query]
    headers = [
        "Teacher Name",
        "Subjects",
    ]

    # print the table
    print(OKGREEN + "Task 5: Subjects that a specific teacher teaches" + ENDC)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# get students list for each group
def select_6():
    query = (
        session.query(Group.name, func.string_agg(Student.name, ", ").label("students"))
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .group_by(Group.name)
        .all()
    )

    print(OKGREEN + "Task 6: Students list for each group" + ENDC)
    for group_name, students in query:
        print("-" * 150)
        print(f"Group: {group_name}, Students: {students}")

    session.close()


# get student marks in each group from some subject
def select_7(subject_name="English"):
    query = (
        session.query(
            Group.name,
            Student.name,
            Subject.name,
            func.array_agg(Mark.mark).label("marks"),
        )
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .join(Mark, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name, Student.name, Subject.name)
        .all()
    )

    table_data = [
        (group_name, student_name, subject_name, marks)
        for group_name, student_name, subject_name, marks in query
    ]
    headers = ["Group Name", "Student Name", "Subject", "Marks"]

    print(OKGREEN + "Task 7: Student marks in each group from some subject" + ENDC)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# get average mark that every teacher puts for each subject
def select_8():
    query = (
        session.query(
            Teacher.name,
            Subject.name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Mark, Mark.subject_id == Subject.id)
        .group_by(Teacher.name, Subject.name)
        .order_by(Teacher.name, Subject.name)
        .all()
    )

    table_data = [
        (teacher_name, subject_name, average_mark)
        for teacher_name, subject_name, average_mark in query
    ]
    headers = ["Teacher Name", "Subject", "Average Mark"]

    print(
        OKGREEN + "Task 8: Average mark that every teacher puts for each subject" + ENDC
    )
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# get subjects list that every student visits
def select_9():
    query = (
        session.query(Student.name, func.array_agg(Subject.name).label("subjects"))
        .join(students_m2m_subjects, Student.id == students_m2m_subjects.c.student_id)
        .join(Subject, Subject.id == students_m2m_subjects.c.subject_id)
        .group_by(Student.name)
        .all()
    )

    print(OKGREEN + "Subjects list that every student visits" + ENDC)
    for student_name, subjects in query:
        print(
            "-" * 150,
        )
        print("Student Name: ", student_name, ", ", "Subjects: ", subjects)

    session.close()


# get a list of subjects taught by a specific teacher to a specific student
def select_10():
    query = (
        session.query(
            Student.name, Teacher.name, func.array_agg(Subject.name).label("subjects")
        )
        .join(students_m2m_subjects, Student.id == students_m2m_subjects.c.student_id)
        .join(Subject, Subject.id == students_m2m_subjects.c.subject_id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .group_by(Student.name, Teacher.name)
        .order_by(Student.name, Teacher.name)
        .all()
    )

    table_data = [
        (student_name, teacher_name, subjects)
        for student_name, teacher_name, subjects in query
    ]
    headers = ["Student Name", "Teacher Name", "Subjects"]

    print(
        OKGREEN
        + "Task 10: A list of subjects taught by a specific teacher to a specific student"
        + ENDC
    )
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# get average mark that a specific teacher puts to a specific student
def select_11():
    query = (
        session.query(
            Student.name,
            Teacher.name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        # .join(students_m2m_subjects, Student.id == students_m2m_subjects.c.student_id)
        .join(Mark, Mark.student_id == Student.id)
        .join(Subject, Subject.id == Mark.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .group_by(Student.name, Teacher.name)
        .order_by(Student.name, Teacher.name)
        .all()
    )

    table_data = [
        (student_name, teacher_name, average_mark)
        for student_name, teacher_name, average_mark in query
    ]
    headers = ["Student Name", "Teacher Name", "Average Mark"]

    print(
        OKGREEN
        + "Task 11: Average mark that a specific teacher puts to a specific student"
        + ENDC
    )
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


# the marks of students in a specific group for a specific subject in the last class
def select_12(subject_name="English"):
    # Subquery to get the latest obtained_at date for each student in the subject
    subquery = (
        session.query(
            Mark.student_id, func.max(Mark.obtained_at).label("latest_obtained_at")
        )
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Mark.student_id)
        .subquery()
    )

    # Main query
    query = (
        session.query(
            Group.name.label("group_name"),
            Student.name.label("student_name"),
            Subject.name.label("subject_name"),
            Mark.mark.label("marks"),
            subquery.c.latest_obtained_at.label("last_obtained_at"),
        )
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .join(Mark, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .join(
            subquery,
            and_(
                Mark.student_id == subquery.c.student_id,
                Mark.obtained_at == subquery.c.latest_obtained_at,
            ),
        )
        .filter(Subject.name == subject_name)
        .order_by(Group.name, Student.name)
        .all()
    )

    # Prepare data for tabulation
    table_data = [
        (group_name, student_name, subject_name, marks, last_obtained_at)
        for group_name, student_name, subject_name, marks, last_obtained_at in query
    ]
    headers = ["Group Name", "Student Name", "Subject", "Marks", "Last Obtained At"]

    # Print the table
    print(
        OKGREEN
        + "Task 12: The marks of students in a specific group for a specific subject in the last class"
        + ENDC
    )
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    session.close()


if __name__ == "__main__":
    select_1()
    select_2("History")
    select_3("Computer Science")
    select_4()
    select_5()
    select_6()
    select_7("Chemistry")
    select_8()
    select_9()
    select_10()
    select_11()
    select_12()
