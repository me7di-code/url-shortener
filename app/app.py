from pydantic import functional_serializers
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from typing import Annotated, Literal
from pydantic import BaseModel, Field
import secrets
import string


app = FastAPI()
Base = declarative_base()
engine = create_engine("sqlite+pysqlite:///./urls.db", echo=True)

class Data(BaseModel):
    url:str
class Shortener(Base):
    __tablename__ = "URLs shortener"
    url = Column(String(250), nullable=False,primary_key=True)
    code = Column(String(250), nullable=False,unique=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session= Session()


@app.post("/short")
def shorten(url:Data):
    existing = session.query(Shortener).filter_by(url=url.url).first()
    if existing != None:
        return "This link is already assigned"
    new_url = Shortener(url=url.url, code="".join(secrets.choice("0123456789") for _ in range(6)))
    session.add(new_url)
    session.commit()
    return session.query(Shortener).filter_by(url=url.url).first()

@app.post("/update/{code}")
def update_link(code:str):
    existing = session.query(Shortener).filter_by(code=code).first()
    if existing == None:
        return "This URL doesnt exist"
    new_link = session.query(Shortener).filter_by(code=code).first()
    new_link.code = "".join(secrets.choice("0123456789") for _ in range(6))
    session.commit()
    return session.query(Shortener).filter_by(code=new_link.code).first()


@app.get("/all")
def fetch():
    users = session.query(Shortener).all()
    return users


# @app.get("/{code}")
# def redirect(code :str):
#     existing= session.query(Shortener).filter_by(code=code).first()
#     if existing == None:
#         return "This link doesnt exist"
#     return RedirectResponse(f"https://{url}")

@app.delete("/delete/{code}")
def delete_link(code: str):
    existing = session.query(Shortener).filter_by(code=code).first()
    if existing == None:
        return "This code doesnt exist"
    url = session.query(Shortener).filter_by(code=code).first()
    session.delete(url)
    session.commit()
    return "URL deleted"




    

