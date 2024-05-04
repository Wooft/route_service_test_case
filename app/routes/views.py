from flask.views import MethodView
from flask import jsonify, request
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError
from database import Session, Routes
from decouple import config
from routes.validators import RouteValidator, EndTimeValidator
from datetime import datetime
from api import api, routes_model
from flask_restx import Namespace
import requests

ns_routes = Namespace('/routes', description='Создание, изменение, получение маршрутов')
set_routes = Namespace('/set_end_time', description='Установка времени окончания маршрута')


def get_route(coordinates):
    """
        Отправляет запрос к сервису OpenRouteService для получения данных маршрута пешеходного похода.

        Данная функция выполняет POST-запрос к API OpenRouteService, передавая координаты начальной и конечной точек маршрута.
        В ответ функция получает данные о маршруте, включая продолжительность пути, точки маршрута и время начала маршрута.

        Args:
            coordinates (list of list of float): Список координат, где каждая координата представлена списком из двух элементов [широта, долгота].

        Returns:
            dict: Словарь с информацией о маршруте, содержащий следующие ключи:
                'duration' (float): Продолжительность пути в секундах.
                'route_points' (list of list of float): Список координат точек маршрута.
                'start_at' (int): Временная метка начала маршрута.

        Пример:
            >>> get_route([[8.681495,49.41461], [8.687872,49.420318]])
            {
                'duration': 600.9,
                'route_points': [[8.681495, 49.41461], [8.68149, 49.41514], ...],
                'start_at': 1615464552
            }
        """
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': config('API_TOKEN'),
        'Content-Type': 'application/json; charset=utf-8'
    }
    body = {"coordinates":[coordinate for coordinate in coordinates]}
    response = requests.post(url=f'https://api.openrouteservice.org/v2/directions/foot-hiking/geojson',
                             headers=headers,
                             json=body)
    route_data = {
        'duration': response.json()['features'][0]['properties']['summary']['duration'],
        'route_points': response.json()['features'][0]['geometry']['coordinates'],
        'start_at': response.json()['metadata']['timestamp'],
        'distance': response.json()['features'][0]['properties']['summary']['distance'],
    }
    return route_data
@ns_routes.route('/routes')
class RouteView(MethodView):
    @ns_routes.expect(routes_model)
    @ns_routes.doc(params={'userid': {'description': 'ID пользователя', 'in': 'query', 'type': 'integer'}})
    @ns_routes.response(200, 'Возвращен список маршрутов')
    @ns_routes.response(500, 'Другие ошибки')
    def get(self):
        """
            Получает список маршрутов для заданного пользователя.

            Этот метод обрабатывает GET-запрос, извлекает из запроса идентификатор пользователя и возвращает список
            всех маршрутов, соответствующих этому пользователю, в формате JSON.

            Входные данные:
                - userid (int): Идентификатор пользователя, для которого нужно получить список маршрутов.
                                  Должен быть передан в теле запроса в формате JSON.

            Возвращает:
                - Response: Объект ответа Flask, содержащий JSON со списком маршрутов в случае успеха
                              или сообщение об ошибке в случае сбоя.
        """
        try:
            with Session() as sesion:
                routes = [route.to_dict for route in sesion.query(Routes).filter_by(user_id=request.json['userid'])]
                return jsonify({'data': routes})
        except Exception as exc:
            return jsonify({'error': 'Unexpected error', 'details': str(exc)}), 500

    @ns_routes.doc(responses={200: 'Success', 400: 'Error'},
             params={
                 'coordinates': {'description': 'Список координат (не менее 2)', 'in': 'query', 'type': 'list'},
                 'userid': {'description': 'ID пользователя', 'in': 'query', 'type': 'integer'},
                 'name': {'description': 'Название маршрута', 'in': 'query', 'type': 'string'}
             })
    @ns_routes.expect(routes_model)
    @ns_routes.response(201, 'Маршрут  создан')
    @ns_routes.response(500, 'Другие ошибки')
    def post(self):
        """
        Создает новый маршрут на основании предоставленных данных.

        Принимает JSON-запрос с данными маршрута, валидирует их, после чего выполняет запрос к
        внешнему сервису для получения дополнительной информации о маршруте. С полученными данными
        создает новую запись в базе данных и возвращает информацию о созданном маршруте.

        Входные данные JSON должны содержать:
            - userid (int): Идентификатор пользователя, создающего маршрут.
            - name (str): Название маршрута.
            - coordinates (list[list[float]]): Список координат маршрута в формате [[широта, долгота], ...].

        В случае успеха возвращает:
            - Response: Объект ответа Flask с JSON представлением созданного маршрута и статусом 201.
        """
        try:
            route_data = RouteValidator(**request.json)
            route = get_route(route_data.coordinates)
            print(route)
            new_route = Routes(user_id=route_data.userid,
                               name=route_data.name,
                               duration = route['duration'],
                               start_time=datetime.fromtimestamp(route['start_at'] / 1e3),
                               route_points={'route_points': route['route_points']},
                               distance = route['distance'])
            with Session() as session:
                session.add(new_route)
                session.commit()
                return jsonify(new_route.to_dict), 201
        except ValidationError as e:
            return jsonify({'error': 'Validation error', 'details': str(e.errors()[0]['msg'])}), 400
        except IntegrityError as e:
            session.rollback()
            return jsonify({'error': 'Integrity error', 'details': str(e.orig)}), 409
        except Exception as exc:
            return jsonify({'error': 'Unexpected error', 'details': str(exc)}), 500

@set_routes.route('/set_end_time')
class SetEndTime(MethodView):

    @ns_routes.expect(routes_model)
    @ns_routes.response(200, 'Время добавлено')
    @ns_routes.response(400, 'Ошибка валидации данных')
    @ns_routes.response(404, 'Маршрут с указанным ID не существует')
    @ns_routes.response(403, 'Пользователь с указанным ID не является владельцем маршрута')
    @ns_routes.response(500, 'Другие ошибки')
    @ns_routes.doc(params={'routeid': {'description': 'ID маршрута', 'in': 'query', 'type': 'integer'},
                           'userid': {'description': 'ID пользователя', 'in': 'query', 'type': 'integer'}})
    def patch(self):
        """
        Обновляет время окончания маршрута для заданного маршрута и пользователя.

        Этот метод принимает JSON-запрос с идентификатором маршрута и идентификатором пользователя,
        валидирует их, и, если данные корректны, обновляет время окончания маршрута в базе данных на текущее время.

        Входные данные JSON должны содержать:
            - routeid (int): Уникальный идентификатор маршрута.
            - userid (int): Идентификатор пользователя, который запрашивает обновление.

        В случае успеха возвращает:
            - Response: Объект ответа Flask с JSON, содержащим обновленное время окончания маршрута и статусом 200.
        """
        try:
            data = EndTimeValidator(**request.json)
            with Session() as session:
                route = session.query(Routes).filter_by(id=data.routeid).first()
                if not route:
                    return jsonify({'error': 'route does not exist'}), 404
                if route.user_id != data.userid:
                    return jsonify({'error': 'Access error'}), 403
                route.end_time = datetime.now().isoformat()
                session.add(route)
                session.commit()
                return jsonify({'end_time': route.end_time}), 200
        except ValidationError as val_err:
            return jsonify({'error': 'Validation error', 'details': str(val_err.errors()[0]['msg'])}), 400
        except Exception as exc:
            return jsonify({'error': 'Unexpected error', 'details': str(exc)}), 500
