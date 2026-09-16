from pydantic import BaseModel


class AskQuery(BaseModel):
    question:str

class AskResponse(BaseModel):
    
    answer:str