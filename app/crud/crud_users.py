from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session


from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, user: UserCreate) -> User:
        db_obj = User(
            username=user.username,
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            _user = db.query(User).filter(User.email == db_obj.email).first()
            _user.password_hash = hashed_password
            if update_data.get("is_authenticated") is not None:
                _user.is_authenticated = update_data["is_authenticated"]
            db.commit()
            db.refresh(_user)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        # authenticate user
        user.is_authenticated = True
        db.commit()
        db.refresh(user)
        return user

    def is_authenticated(self, user: User) -> bool:
        return user.is_authenticated

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)

# def create(db: Session, user: UserCreate):
#     db_user = User(username=user.username,
#                    email=user.email,
#                    password_hash=get_password_hash(user.password),
#                    )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# Implementa el resto de las operaciones CRUD (read, update, delete) según tus necesidades
