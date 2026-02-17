from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Movies(Base):
        __tablename__ = 'Movies'
        
        id = Column(Integer, primary_key=True)
        titulo = Column(String(100), nullable=False)
        generos = Column(String(250))
        rate = Column(Numeric(precision=10, scale=2), nullable=False)
        year = Column(Integer)
        summary = Column(Text)
        director = Column(String(150))
        image = Column(Text)




def createDb(databaseName):
    engine = create_engine(f'sqlite:///{databaseName}', echo=True)

    Base.metadata.create_all(engine)

    return engine, Movies
