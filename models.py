from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="SET NULL"))
    grades = relationship('Grades', back_populates='student')


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subject = relationship("Subjects", back_populates="group")


class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subject = relationship("Subjects", back_populates="teacher")


class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="SET NULL"))
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="SET NULL"))
    teacher = relationship("Teachers", back_populates="subject")
    group = relationship("Groups", back_populates="subject")
    grade = relationship("Grades", back_populates="subject")


class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Integer)
    date_issued = Column(DateTime, default=datetime.now())
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"))
    student = relationship("Students", back_populates="grades")
    subject = relationship("Subjects", back_populates="grade")

