from sqlmodel import Session, select
from app.models.user import User, UserReq
from app.core.security import get_password_hash, verify_password
import uuid

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def get_user_by_id(*, session: Session, id: str) -> User | None:
    statement = select(User).where(User.id == id)
    session_user = session.exec(statement).first()
    return session_user

def create_user(*, session: Session, user: UserReq) -> User:
    id = uuid.uuid4()
    password = get_password_hash(user.password)
    db_obj = User(id = id, email = user.email, password = password)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user