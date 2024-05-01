from flask.views import MethodView
from flask import jsonify, request

class Hello(MethodView):

    def get(self):
        return jsonify({
            'hello': 'Hello World'
        })

    def post(self):
        '''
        Принимает координаты точек A и B
        Сохраняет занчения в Базу данных, соотнося по токену пользователя где чей маршрут
        Перенаправляет запрос https://openrouteservice.org/dev/#/api-docs/v2/
        Возвращает маршрут пользователю
        :return:
        '''
        print(request.json)
        return jsonify({
            'data': 'something'
        })