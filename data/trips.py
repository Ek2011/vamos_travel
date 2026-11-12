import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Trip(SqlAlchemyBase):
    __tablename__ = 'trips'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('User')
    points = orm.relationship("TripPoint", back_populates='trip', cascade="all, delete-orphan")
