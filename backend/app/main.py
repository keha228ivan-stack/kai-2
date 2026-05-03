from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session

from .auth import create_access_token, get_current_user, hash_password, require_roles, verify_password
from .database import Base, engine, get_db
from .models import Course, CourseAssignment, CourseLibrary, Progress, Test, User
from .schemas import CourseAssignmentCreate, ProgressUpdate, Token, UserCreate

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Local HR Backend")


@app.post("/auth/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email exists")
    user = User(name=payload.name, email=payload.email, password_hash=hash_password(payload.password), role=payload.role, department=payload.department)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "role": user.role}


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(401, "Invalid login")
    return Token(access_token=create_access_token({"sub": user.email, "role": user.role}))


@app.post("/manager/assign", dependencies=[Depends(require_roles("manager"))])
def assign_course(payload: CourseAssignmentCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == payload.user_id, User.role == "employee").first():
        raise HTTPException(404, "Employee not found")
    if not db.query(Course).filter(Course.id == payload.course_id).first():
        raise HTTPException(404, "Course not found")
    existing = db.query(CourseAssignment).filter_by(user_id=payload.user_id, course_id=payload.course_id).first()
    if existing:
        return {"status": "already_assigned", "assignment_id": existing.id}
    assignment = CourseAssignment(user_id=payload.user_id, course_id=payload.course_id, status="in-progress")
    db.add(assignment)
    db.flush()
    db.add(Progress(assignment_id=assignment.id, completion_percentage=0.0))
    db.commit()
    return {"status": "assigned", "assignment_id": assignment.id}


@app.get("/employee/my_courses", dependencies=[Depends(require_roles("employee"))])
def my_courses(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(CourseAssignment).filter(CourseAssignment.user_id == user.id, CourseAssignment.status == "in-progress").all()


@app.get("/employee/my_courses/{course_id}", dependencies=[Depends(require_roles("employee"))])
def my_course_detail(course_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(CourseAssignment).filter_by(user_id=user.id, course_id=course_id).first()
    if not assignment:
        raise HTTPException(404, "Course not assigned")
    return assignment


@app.get("/employee/my_courses/{course_id}/progress", dependencies=[Depends(require_roles("employee"))])
def my_course_progress(course_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(CourseAssignment).filter_by(user_id=user.id, course_id=course_id).first()
    if not assignment or not assignment.progress:
        raise HTTPException(404, "Progress not found")
    return assignment.progress


@app.patch("/employee/my_courses/{course_id}/progress", dependencies=[Depends(require_roles("employee"))])
def update_progress(course_id: int, payload: ProgressUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(CourseAssignment).filter_by(user_id=user.id, course_id=course_id).first()
    if not assignment or not assignment.progress:
        raise HTTPException(404, "Progress not found")
    assignment.progress.completion_percentage = max(0.0, min(100.0, payload.completion_percentage))
    if assignment.progress.completion_percentage >= 100.0:
        assignment.status = "completed"
    db.commit()
    return {"status": assignment.status, "completion_percentage": assignment.progress.completion_percentage}


@app.get("/employee/my_courses/{course_id}/test", dependencies=[Depends(require_roles("employee"))])
def my_test(course_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(CourseAssignment).filter_by(user_id=user.id, course_id=course_id).first()
    if not assignment or assignment.status != "completed":
        raise HTTPException(403, "Test is available only after course completion")
    return db.query(Test).filter(Test.course_id == course_id).all()


@app.get("/manager/employee_courses/{user_id}", dependencies=[Depends(require_roles("manager"))])
def employee_courses(user_id: int, db: Session = Depends(get_db)):
    return {"user_id": user_id, "assigned_courses": db.query(CourseAssignment).filter_by(user_id=user_id).count()}


@app.get("/admin/stats", dependencies=[Depends(require_roles("admin"))])
def global_stats(db: Session = Depends(get_db)):
    return {
        "employees_total": db.query(User).filter(User.role == "employee").count(),
        "assignments_total": db.query(CourseAssignment).count(),
        "completed_assignments": db.query(CourseAssignment).filter(CourseAssignment.status == "completed").count(),
    }


@app.get("/admin/stats/{department}", dependencies=[Depends(require_roles("admin"))])
def department_stats(department: str, db: Session = Depends(get_db)):
    rows = db.query(User.department, func.count(User.id)).filter(User.department == department, User.role == "employee").group_by(User.department).all()
    total = rows[0][1] if rows else 0
    return {"department": department, "employees_total": total}


@app.get("/library/sync", dependencies=[Depends(require_roles("manager", "employee"))])
def sync_library(db: Session = Depends(get_db)):
    return db.query(CourseLibrary).all()
