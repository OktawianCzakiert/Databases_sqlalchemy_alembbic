from engine import session
from sqlalchemy import func, desc

from models import Students,  Groups, Teachers, Subjects, Grades


def select_1():
    # 1. Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.
    # SELECT students.id, students.name, AVG(grades.grade) as average_grade
    # FROM students
    # JOIN grades ON students.id = grades.student_id
    # GROUP BY students.id, students.name
    # ORDER BY average_grade DESC
    # LIMIT 5;

    with session:
        result = (
            session.query(Students.id, Students.name, func.round(func.avg(Grades.grade), 2).label('average_grade'))
            .select_from(Students)
            .join(Grades, Students.id == Grades.student_id)
            .group_by(Students.id, Students.name)
            .order_by(func.avg(Grades.grade).desc())
            .limit(5)
            .all()
        )

    print(f"\n5 students with the highest grades average:")
    for row in result:
        print(f"ID: {row.id}, Name: {row.name}, Average Grade: {row.average_grade}")


def select_2():
    # 2. Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu.
    # SELECT students.id, students.name, AVG(grades.grade) as average_grade
    # FROM students
    # JOIN grades ON students.id = grades.student_id
    # WHERE grades.subject_id = 3
    # GROUP BY students.id, students.name
    # ORDER BY average_grade DESC
    # LIMIT 1;

    sub_id = 3

    with session:
        result = (
            session.query(Students.id, Students.name, func.round(func.avg(Grades.grade), 2).label('average_grade'))
            .select_from(Students)
            .join(Grades, Students.id == Grades.student_id)
            .where(Grades.subject_id == sub_id)
            .group_by(Students.id, Students.name)
            .order_by(func.avg(Grades.grade).desc())
            .limit(1)
        )

    print(f"\nStudent with the highest grades average for subject_id == {sub_id}:")
    for row in result:
        print(f"ID: {row.id}, Name: {row.name}, Average Grade: {row.average_grade}")


def select_3():
    # 3. Znajdź średni wynik w grupach dla określonego przedmiotu.
    # SELECT groups.name AS group_name, AVG(grades.grade) AS average_grade
    # FROM groups
    # JOIN students ON groups.id = students.group_id
    # JOIN grades ON students.id = grades.student_id
    # JOIN subjects ON grades.subject_id = subjects.id
    # WHERE subjects.id = 3
    # GROUP BY group_name
    # ORDER BY average_grade DESC;

    sub_id = 3

    with session:
        result = (
            session.query(Groups.name.label('group_name'), func.round(func.avg(Grades.grade), 2).label('average_grade'))
            .select_from(Groups)
            .join(Students, Groups.id == Students.group_id)
            .join(Grades, Students.id == Grades.student_id)
            .join(Subjects, Grades.subject_id == Subjects.id)
            .where(Subjects.id == sub_id)
            .group_by('group_name')
            .order_by(desc('average_grade'))
        )

    print(f"\nAverage grade in groups for subject_id == {sub_id}:")
    for row in result:
        print(f"Average Grade: {row.average_grade}")


def select_4():
    # 4. Znajdź średni wynik w grupie (w całej tabeli ocen).
    # SELECT groups.name AS group_name, AVG(grades.grade) AS average_grade
    # FROM groups
    # JOIN students ON groups.id = students.group_id
    # JOIN grades ON students.id = grades.student_id
    # JOIN subjects ON grades.subject_id = subjects.id
    # GROUP BY group_name
    # ORDER BY average_grade DESC;

    with session:
        result = (
            session.query(Groups.name.label('group_name'), func.round(func.avg(Grades.grade), 2).label('average_grade'))
            .select_from(Groups)
            .join(Students, Groups.id == Students.group_id)
            .join(Grades, Students.id == Grades.student_id)
            .join(Subjects, Grades.subject_id == Subjects.id)
            .group_by('group_name')
            .order_by(desc('average_grade'))
        )

    print(f"\nAverage grade in groups:")
    for row in result:
        print(f"{row.group_name} - average grade: {row.average_grade}")


def select_5():
    # 5. Znajdź przedmioty, których uczy określony wykładowca.
    # SELECT subjects.name AS subject_name
    # FROM subjects
    # WHERE subjects.teacher_id = 1
    # GROUP BY subject_name

    teach_id = 1

    with session:
        result = (
            session.query(Subjects.name.label('subject_name'))
            .select_from(Subjects)
            .where(Subjects.teacher_id == teach_id)
            .group_by('subject_name')
        )

    print(f"\nSubjects taught by teacher with id {teach_id}:")
    for row in result:
        print(f"Subject name: {row.subject_name}")


def select_6():
    # 6. Znajdź listę studentów w określonej grupie.
    # SELECT students.name AS students_name
    # FROM students
    # WHERE students.group_id = 1

    gr_id = 1

    with session:
        result = (
            session.query(Students.name.label('students_name'))
            .select_from(Students)
            .where(Students.group_id == gr_id)
        )

    print(f"\nList of students from group with id {gr_id}:")
    for row in result:
        print(f"- {row.students_name}")


def select_7():
    # 7. Znajdź oceny studentów w określonej grupie z danego przedmiotu.
    # SELECT students.name, grades.grade
    # FROM students
    # JOIN grades ON students.id = grades.student_id
    # JOIN subjects ON grades.subject_id = subjects.id
    # WHERE students.group_id = 2 AND subjects.id = 5;

    gr_id = 2
    sub_id = 5

    with session:
        result = (
            session.query(Students.name.label('students_name'), Grades.grade)
            .select_from(Students)
            .join(Grades, Students.id == Grades.student_id)
            .join(Subjects, Grades.subject_id == Subjects.id)
            .where(Students.group_id == gr_id and Subjects.id == sub_id)
        )

    print(f"\nGrades of students from group with id {gr_id} and subject with id {sub_id}:")
    for row in result:
        print(f"- {row.students_name} - {row.grade}")


def select_8():
    # 8. Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.
    # SELECT AVG(grades.grade)
    # FROM grades
    # JOIN subjects ON subjects.id = grades.subject_id
    # JOIN teachers ON teachers.id = subjects.teacher_id
    # WHERE teachers.id = 2 AND subjects.id = 3;

    teach_id = 2
    sub_id = 3

    with session:
        result = (
            session.query(func.round(func.avg(Grades.grade), 2).label('average_grade'))
            .select_from(Grades)
            .join(Subjects, Subjects.id == Grades.subject_id)
            .join(Teachers, Teachers.id == Subjects.teacher_id)
            .where(Teachers.id == teach_id and Subjects.id == sub_id)
        )

    print(f"Average grades given by teacher with id {teach_id} in subject with id {sub_id}")
    for row in result:
        print(f"{row.average_grade}")


def select_9():
    # 9. Znajdź listę przedmiotów zaliczonych przez danego studenta.
    # SELECT subjects.name
    # FROM subjects
    # JOIN students ON students.group_id = groups.id
    # JOIN groups ON students.group_id = subjects.group_id
    # WHERE students.id = 1;

    stud_id = 13

    with session:
        result = (
            session.query(Subjects.name)
            .select_from(Subjects)
            .join(Students, Students.group_id == Subjects.group_id)
            .where(Students.id == stud_id)
        )

    print(f"List of subjects learned by student with id {stud_id}:")

    for row in result:
        print(f"- {row.name}")


def select_10():
    # 10. Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta.
    # SELECT subjects.name
    # FROM subjects
    # JOIN teachers ON subjects.teacher_id = teachers.id
    # JOIN students ON students.group_id = subjects.group_id
    # WHERE students.id = 3 AND teachers.id = 2;

    stud_id = 3
    teach_id = 2

    with session:
        result = (
            session.query(Subjects.name)
            .select_from(Subjects)
            .join(Teachers, Subjects.teacher_id == Teachers.id)
            .join(Students, Students.group_id == Subjects.group_id)
            .where(Students.id == stud_id and Teachers.id == teach_id)
        )

    print(f"List of subjects taught by teacher with id {teach_id} for student with id {stud_id}")

    for row in result:
        print(f"{row.name}")


func_dict = {
        "1": select_1,
        "2": select_2,
        "3": select_3,
        "4": select_4,
        "5": select_5,
        "6": select_6,
        "7": select_7,
        "8": select_8,
        "9": select_9,
        "10": select_10,
    }


def ask_for_query_no():

    valid_number = False

    while not valid_number:
        try:
            query_no = input("\nEnter 'exit' to stop or query no (1-10) to execute: ")

            if query_no.lower() == "exit":
                return False
            elif 1 <= int(query_no) <= 10:
                valid_number = True
                return query_no
            else:
                print("Please enter a number within specified range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def execute_query():

    function = ask_for_query_no()
    if not function:
        return False
    return function


if __name__ == '__main__':
    working = True
    while working:
        data = execute_query()
        if not data:
            working = False
            break
        print(func_dict[data]())
