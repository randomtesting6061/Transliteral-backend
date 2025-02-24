from pydantic import BaseModel


class Userschemamodel(BaseModel):
    username:str
    password:str