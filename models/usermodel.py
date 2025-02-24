from sqlalchemy import Column,BigInteger,Integer,ForeignKey,String
from database import  Base



class User(Base):
    __tablename__="usersb"
    
    username=Column(String,unique=True,primary_key=True)
    password= Column(String)