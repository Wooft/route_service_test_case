import json
from flask.views import MethodView
from flask import jsonify, request
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError

from database import Session, User, Routes
from decouple import config
from pprint import pprint
from routes.validate import UserValidator, RouteValidator
import requests

def get_route(coordinates):
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': config('API_TOKEN'),
        'Content-Type': 'application/json; charset=utf-8'
    }
    body = {"coordinates":[coordinate for coordinate in coordinates]}
    response = requests.post(url=f'https://api.openrouteservice.org/v2/directions/driving-car',
                             headers=headers,
                             json=body)
    return response.json()
class RouteView(MethodView):

    def get(self):
        with Session() as sesion:
            routes = [route.to_dict for route in sesion.query(Routes).all()]
            return jsonify({'data': routes})

    def post(self):
        '''
        Принимает координаты точек A и B
        Сохраняет занчения в Базу данных, соотнося по токену пользователя где чей маршрут
        Перенаправляет запрос https://openrouteservice.org/dev/#/api-docs/v2/
        Возвращает маршрут пользователю
        :return:
        '''
        try:
            route_data = RouteValidator(**request.json)
        except ValidationError as e:
            return jsonify({'error': e.errors()[0]['msg']}), 400
        new_route = Routes(json_data=get_route(route_data.coordinates),
                           user_id=route_data.userid)
        with Session() as session:
            session.add(new_route)
            try:
                session.commit()
            except IntegrityError as e:
                return jsonify({'error': e.orig.diag.message_detail})
            return jsonify(new_route.json_data)

class Register(MethodView):
    def get(self):
        with Session() as sesion:
            routes = [user.name for user in sesion.query(User).all()]
            return jsonify({'data': routes})
    def post(self):
        try:
            user_data = UserValidator(**request.json)
        except ValidationError as e:
            return jsonify({'error': e.errors()[0]['msg']}), 400
        print(user_data)
        with Session() as session:
            new_user = User(name=user_data.name,
                            password=user_data.password,
                            email=user_data.email)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError as e:
                return jsonify({'error': e.orig.diag.message_detail})
            return jsonify({'data': new_user.name})
