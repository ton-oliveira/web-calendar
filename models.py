from sqlalchemy import MetaData, Table, create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime


engine = create_engine('sqlite:///calendar.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
meta = MetaData()
Base = declarative_base()
Base.query = db_session.query_property()


class WebCalendar(Base):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True)
    event = Column(String(80), nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return "<WebCalendar(event='%s', date='%s')>" % (
            self.name, self.date)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    calendar = Table(
        'calendar', meta,
        Column('id', Integer, primary_key=True),
        Column("event", String(80), nullable=False),
        Column('date', Date, nullable=False)
    )

    meta.create_all(engine)


if __name__ == '__main__':
    init_db()

session = sessionmaker()
session.configure(bind=engine)
S = session()
