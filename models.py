from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    PrimaryKeyConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# table for many-to-many relationship between groups and subjects
groups_m2m_students = Table(
    "groups_m2m_students",
    Base.metadata,
    Column("group_id", ForeignKey("group.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column(
        "student_id", ForeignKey("student.id", ondelete="CASCADE", onupdate="CASCADE")
    ),
    PrimaryKeyConstraint("group_id", "student_id"),
)

# table for many-to-many relationship between students and subjects
students_m2m_subjects = Table(
    "students_m2m_subjects",
    Base.metadata,
    Column(
        "student_id", ForeignKey("student.id", ondelete="CASCADE", onupdate="CASCADE")
    ),
    Column(
        "subject_id", ForeignKey("subject.id", ondelete="CASCADE", onupdate="CASCADE")
    ),
    PrimaryKeyConstraint("student_id", "subject_id"),
)


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    groups: Mapped[list["Group"]] = relationship(
        secondary=groups_m2m_students, back_populates="students"
    )
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=students_m2m_subjects, back_populates="students"
    )
    marks: Mapped[list["Mark"]] = relationship(back_populates="student")


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    students: Mapped[list["Student"]] = relationship(
        secondary=groups_m2m_students, back_populates="groups"
    )


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    subjects: Mapped[list["Subject"]] = relationship(
        back_populates="teacher", cascade="all, delete"
    )


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teacher.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    marks: Mapped[list["Mark"]] = relationship(back_populates="subject")
    students: Mapped[list["Student"]] = relationship(
        secondary=students_m2m_subjects, back_populates="subjects"
    )


class Mark(Base):
    __tablename__ = "mark"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[int] = mapped_column(Integer)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("student.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subject.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    obtained_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    student: Mapped["Student"] = relationship(back_populates="marks")
    subject: Mapped["Subject"] = relationship(back_populates="marks")
