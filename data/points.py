import sqlalchemy
from .db_session import SqlAlchemyBase


class TripPoint(SqlAlchemyBase):
    __tablename__ = 'trip_point'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    destination = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    arrival_time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    notes = sqlalchemy.Column(sqlalchemy.String, nullable=True)