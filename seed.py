
from faker import Faker
from random import randint
from datetime import datetime, timedelta

from engine import session
from models import Students, Groups, Teachers, Subjects, Grades

NUMBER_STUDENTS = 40
NUMBER_SUBJECTS = 8
NUMBER_GROUPS = 3
NUMBER_TEACHERS = 6
NUMBER_GRADES = 30


def generate_fake_data(number_students, number_subjects, number_groups, number_teachers, number_grades):
    fake = Faker()


    fake_groups = [('Group A',), ('Group B',), ('Group C',)]

    for group in fake_groups:
        new_group = Groups(name = group)
        session.add(new_group)

    for _ in range(number_students):
        new_student = Students(name = fake.name(), group_id = randint(1, number_groups))
        session.add(new_student)

    for _ in range(number_subjects):
        new_subject = Subjects(name = fake.word(), group_id = randint(1, number_groups), teacher_id = randint(1, number_teachers))
        session.add(new_subject)

    for _ in range(number_teachers):
        new_teacher = Teachers(name = fake.name())
        session.add(new_teacher)

    for _ in range(number_grades):
        new_grade = Grades(grade = randint(1, 6), date_issued = (datetime.now() - timedelta(days=randint(1, 365))).strftime('%Y-%m-%d'), student_id = randint(1, number_students), subject_id = randint(1, number_subjects))
        session.add(new_grade)


    session.commit()
    session.close()


if __name__ == '__main__':
    generate_fake_data(NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_GROUPS, NUMBER_TEACHERS, NUMBER_GRADES)
