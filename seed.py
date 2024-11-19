from connect import session
import random
from models import Student, Group, Subject, Teacher, Mark
from faker import Faker

fake = Faker()


def main():
    # create groups
    group_1 = Group(name="Group 1")
    group_2 = Group(name="Group 2")
    group_3 = Group(name="Group 3")

    # create teachers
    teachers = []
    for _ in range(1, 9):
        teachers.append(Teacher(name=fake.name()))

    # create subjects
    courses = [
        "Math",
        "Physics",
        "Chemistry",
        "Biology",
        "History",
        "Geography",
        "English",
        "French",
        "German",
        "Spanish",
        "Music",
        "Art",
        "Computer Science",
    ]
    subjects = []
    for course in courses:
        subjects.append(Subject(name=course, teacher=random.choice(teachers)))

    # create students
    students = []
    for i in range(1, 40):
        students.append(
            Student(
                name=fake.name(),
                age=random.randint(10, 20),
            )
        )
    for student in students:
        student.groups = random.sample(
            [group_1, group_2, group_3], k=random.randint(1, 2)
        )
        student.subjects = random.sample(subjects, k=random.randint(8, 10))

    # create marks
    marks = []
    for student in students:
        for _ in range(random.randint(12, 20)):
            marks.append(
                Mark(
                    mark=random.randint(1, 12),
                    student=student,
                    subject=random.choice(student.subjects),
                    obtained_at=fake.date_time_between(
                        start_date="-1y", end_date="now"
                    ),
                )
            )

    session.add_all([group_1, group_2, group_3])
    session.add_all(teachers)
    session.add_all(subjects)
    session.add_all(students)
    session.add_all(marks)
    session.commit()

    session.close()


if __name__ == "__main__":
    main()
