"""Repository base con operaciones CRUD comunes"""

from typing import Generic, List, Optional, TypeVar

from sqlalchemy.orm import Session

from app.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Repository base genérico"""

    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def create(self, obj_in: dict) -> T:
        """Crear un nuevo registro"""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def get_by_id(self, obj_id: int) -> Optional[T]:
        """Obtener por ID"""
        return self.session.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtener todos los registros"""
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def update(self, obj_id: int, obj_in: dict) -> Optional[T]:
        """Actualizar un registro"""
        db_obj = self.get_by_id(obj_id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.session.commit()
            self.session.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: int) -> bool:
        """Eliminar un registro"""
        db_obj = self.get_by_id(obj_id)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
            return True
        return False
