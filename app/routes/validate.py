import pydantic
from pydantic import BaseModel, validator


class UserValidator(BaseModel):
    name: str
    password: str
    repeat_password: str
    email: str
    @validator('password')
    def password_strengtht(cls, value):
        if len(value) < 6:
            raise ValueError('Password os too short')
        return value

    @validator('repeat_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Password and repeat password do not match')
        return v

class RouteValidator(BaseModel):
    coordinates: list
    name: str
    userid: int
    @validator('coordinates')
    def is_list(cls, v):
        if len(v) == 0:
            raise ValueError('Coordinates not entered')
        return v