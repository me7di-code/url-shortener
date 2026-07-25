from datetime import datetime
from enum import unique
from pydantic import functional_serializers
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import secrets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()
engine = create_engine("sqlite+pysqlite:///./urls.db", echo=True)

class Data(BaseModel):
    url:str
class Shortener(Base):
    __tablename__ = "URLs shortener"
    url = Column(String(250), nullable=False,primary_key=True)
    code = Column(String(6), nullable=False,unique=True)
    clickCount = Column(Integer())
    createdAt = Column(String(250),nullable=False)
    updatedAt = Column(String(250),nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session= Session()


@app.post("/shorten")
def shorten(url:Data):
    existing = session.query(Shortener).filter_by(url=url.url).first()
    if existing != None:
        return "This link is already assigned"
    new_url = Shortener(url=url.url, code="".join(secrets.choice("0123456789") for _ in range(6)),createdAt=datetime.now(),updatedAt=datetime.now(),clickCount=0)
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
    new_link.updatedAt = datetime.now()
    session.commit()
    return session.query(Shortener).filter_by(code=new_link.code).first()


@app.get("/all")
def fetch():
    users = session.query(Shortener).all()
    return users


@app.get("/{code}")
def redirect(code :str):
    existing= session.query(Shortener).filter_by(code=code).first()
    if existing == None:
        return "This link doesnt exist"
    url = session.query(Shortener).filter_by(code=code).first()
    url.clickCount += 1
    session.commit()
    
    target_url = url.url
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = f"https://{target_url}"
        
    return RedirectResponse(target_url)

@app.delete("/delete/{code}")
def delete_link(code: str):
    existing = session.query(Shortener).filter_by(code=code).first()
    if existing == None:
        return "This code doesnt exist"
    url = session.query(Shortener).filter_by(code=code).first()
    session.delete(url)
    session.commit()
    return "URL deleted"