from pydantic import BaseModel, validator


class RouteValidator(BaseModel):
    """
    Валидатор для проверки данных маршрута.

    Поля:
        coordinates (list): Список координат маршрута.
        name (str): Название маршрута.
        userid (int): Идентификатор пользователя, создающего маршрут.

    Методы:
        coordinates_not_empty(cls, v): Проверяет, что координаты были введены.
    """
    coordinates: list
    name: str
    userid: int
    @validator('coordinates')
    def coordinates_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Coordinates not entered')
        if len(v) == 1:
            raise ValueError('There must be at least two coordinates to calculate the route')
        return v

class EndTimeValidator(BaseModel):
    userid: int
    routeid: int