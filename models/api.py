from pydantic import BaseModel


class UpdateAccount(BaseModel):
    name: str
    age: int
    email: str
    password: str
    address: str
    phone: str
