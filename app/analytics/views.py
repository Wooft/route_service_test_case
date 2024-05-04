from flask.views import MethodView
from flask import jsonify, request
from database import Session, Routes
from sqlalchemy.sql import func
from flask_restx import Namespace
from api import analytic_model

analytics_namespace = Namespace('analytics', description='Получение аналитики пользователя')

@analytics_namespace.route('/analytics')
class AnalyticsView(MethodView):

    @analytics_namespace.expect(analytic_model)
    @analytics_namespace.doc(params={'userid': {'description': 'ID пользователя', 'in': 'query', 'type': 'integer'},
                                     'day_of_week': {'description': 'число от 0 до 6, где 0 — воскресенье, 6 — суббота', 'in': 'query', 'type': 'integer'}})
    def get(self):

        """
        Получает статистику маршрутов для пользователя с заданным user_id.

        Эта функция обрабатывает GET-запросы и возвращает среднее отклонение
        фактического времени прохождения маршрута от запланированного и
        общее пройденное расстояние по всем маршрутам пользователя.
        Опционально может принимать параметр 'day_of_week' в теле запроса,
        чтобы ограничить статистику маршрутами, совершенными в определенный день недели.

        Параметры:
        - user_id (int): идентификатор пользователя в системе
        - day_of_week (int, optional): число от 0 до 6, где 0 — воскресенье, 6 — суббота
        """
        try:
            with Session() as session:
                user_id = request.json['userid']
                query = session.query(Routes).filter(Routes.user_id == user_id)
                day_of_week = request.json.get('day_of_week')
                if day_of_week is not None:
                    query = query.filter(func.extract('dow', Routes.start_time) == day_of_week)
                average_deviation = query.with_entities(
                    func.avg(func.extract('epoch', Routes.end_time) - func.extract('epoch', Routes.start_time) - Routes.duration)).filter(Routes.user_id == user_id).scalar()
                total_distance = query.with_entities(func.sum(Routes.distance)).filter(
                    Routes.user_id == user_id).scalar()
                return jsonify({
                    'average_deviation': average_deviation,
                    'total_distance': total_distance
                })
        except Exception as exc:
            return jsonify({'error': 'Unexpected error', 'details': str(exc)}), 500
        return jsonify()