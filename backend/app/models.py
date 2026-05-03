from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class CourseLibrary(Base):
    __tablename__ = "course_library"
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    channel = Column(String, primary_key=True)  # web | desktop


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # employee | manager | admin
    department = Column(String, nullable=False)

    assignments = relationship("CourseAssignment", back_populates="user", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    deadline = Column(Date)

    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    tests = relationship("Test", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("CourseAssignment", back_populates="course", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    attachment = Column(String)
    lesson_number = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="lessons")


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("course_assignments.id"), unique=True, nullable=False)
    completion_percentage = Column(Float, default=0.0)
    deadline = Column(Date)

    assignment = relationship("CourseAssignment", back_populates="progress")


class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    questions = Column(Text, nullable=False)

    course = relationship("Course", back_populates="tests")


class CourseAssignment(Base):
    __tablename__ = "course_assignments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status = Column(String, default="in-progress")

    user = relationship("User", back_populates="assignments")
    course = relationship("Course", back_populates="assignments")
    progress = relationship("Progress", back_populates="assignment", uselist=False, cascade="all, delete-orphan")
