import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class TripPoint(SqlAlchemyBase):
    __tablename__ = 'trip_point'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    trip_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("trips.id"))
    destination = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    arrival_time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sequence_order = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    trip = orm.relationship('Trip', back_populates='points')