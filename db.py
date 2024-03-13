from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String, Boolean
from settings import REAL_DATABASE_URL


engine = create_engine(REAL_DATABASE_URL, echo=True)


class Base(DeclarativeBase): pass
class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    send_time = Column(String, nullable=False)
    product_article = Column(Integer, nullable=False)
    

Base.metadata.create_all(bind=engine)


class DataManipulation:
    '''Класс манипуляции данными'''
    def write_data(user_id, send_time, product_article):
        with Session(autoflush=False, bind=engine) as db:
            new_data = Data(user_id=user_id, send_time=send_time, product_article=product_article)
            db.add(new_data)
            db.commit()
            return new_data
        

    def get_last_requests(user_id, many):
        with Session(autoflush=False, bind=engine) as db:
            return db.query(Data).filter(Data.user_id == user_id,).order_by(Data.id.desc()).limit(many).all()