# Standard library
from datetime import datetime
from typing import Dict, List

# Internal modules
from app import db


class BaseModel():
    id: int = db.Column(db.Integer, primary_key=True)
    created_at: datetime = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
        )
    updated_at: datetime = db.Column(
        db.DateTime,
        onupdate=datetime.utcnow
        )

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def to_dict(self) -> Dict:
        attribute_list = self._get_class_attributes_as_list()
        attribute_dict = dict()
        for item in attribute_list:
            attribute_dict.update(item)
        return attribute_dict

    def __repr__(self) -> str:
        attribute_dict = self.to_dict()
        repr_str: str = f"{self.__class__.__name__}("
        for i, (key, value) in enumerate(attribute_dict.items()):
            repr_str += f"{key}={value}"
            if i < len(attribute_dict) - 1:
                repr_str += ", "
        repr_str += ")"
        return repr_str

    def _get_class_attributes_as_list(self) -> List:
        valid_types = [str, int, bool, datetime, type(None)]
        return [{key: self.__getattribute__(key)}
                for key in dir(self)
                if not key.startswith('_')
                and not key.startswith('password')
                and type(self.__getattribute__(key)) in valid_types]


if __name__ == "__main__":
    pass
