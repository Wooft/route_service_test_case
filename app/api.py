from flask_restx import Namespace, Resource, fields, Api


api = Api(version='1.0', title='Routes', description='WEB Сервис для управления маршрутами',  doc='/swagger/')

user_model = api.model('User', {
    'id': fields.Integer(required=True, description='ID пользователя'),
    'username': fields.String(required=True, description='Имя пользователя'),
    'email': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Username'),
    'created_at': fields.DateTime(autoincrement=True)
})

routes_model = api.model('Routes', {
    'id': fields.Integer(required=True, description='ID пользователя'),
    'start_time': fields.DateTime(required=False, description='Время начала маршрута'),
    'duration': fields.Float(required=False, description='Продолжительность маршрута (в секундах)'),
    'user_id': fields.Integer(required=False, description='ID пользователя, создавшего маршрут. Вторичный ключ модели User'),
    'name': fields.String(required=False, description='Название маршрута'),
    'route_points': fields.String(required=True, description='Список координат точек маршрута'),
    'end_time': fields.DateTime(required=True, description='Время окончания маршрута'),
})

analytic_model = api.model('Analytics', {
    'average_deviation': fields.Float(description='Среднее отклонение времени в пути'),
    'total_distance': fields.Float(description='Пройденное пользователем расстояние'),
})