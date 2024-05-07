from flask.views import MethodView
from flask import jsonify, request
from database import Session, Routes
from sqlalchemy.sql import func, case
from flask_restx import Namespace
from api import analytic_model
from sqlalchemy.sql import text

analytics_namespace = Namespace('/analytics', description='Получение аналитики пользователя')

@analytics_namespace.route('/analytics')
class AnalyticsView(MethodView):

    @analytics_namespace.expect(analytic_model)
    @analytics_namespace.doc(params={'userid': {'description': 'ID пользователя', 'in': 'query', 'type': 'integer'},
                                     'day_of_week': {'description': 'число от 0 до 6, где 0 — воскресенье, 6 — суббота', 'in': 'query', 'type': 'integer'}})
    @analytics_namespace.response(200, 'Получение данных')
    @analytics_namespace.response(500, 'Непредвиденные ошибки')
    def get(self):
        """
        Получает данные о маршрутах пользователя из базы данных и вычисляет статистическую информацию.

        Функция выполняет следующие действия:
        - Извлекает из запроса идентификатор пользователя и, если указан, день недели.
        - Формирует SQL-запрос для получения маршрутов пользователя.
        - Если день недели указан, фильтрует маршруты по этому критерию.
        - Вычисляет среднее отклонение между фактическим временем маршрута и заявленной продолжительностью.
        - Подсчитывает общее пройденное расстояние и общее время в пути.
        - Рассчитывает среднюю скорость передвижения.
        - Возвращает JSON-объект со статистической информацией: среднее отклонение, общее расстояние, общее время и средняя скорость.

        В случае возникновения ошибки возвращает JSON с описанием ошибки и HTTP-статус 500.

        :return: JSON-объект со статистикой или описанием ошибки.
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
                total_distance = query.with_entities(func.sum(Routes.distance)).filter(Routes.user_id == user_id).scalar()
                total_time = session.query(func.sum(case((Routes.end_time is not None,
                                                          func.extract('epoch', Routes.end_time) - func.extract('epoch', Routes.start_time)),
                                                          else_=Routes.duration)
                    )).filter(Routes.user_id == user_id).scalar()
                avg_speed = total_distance / total_time

                return jsonify({
                    'average_deviation': average_deviation,
                    'total_distance': total_distance,
                    'total_time': total_time,
                    'avg_speed': avg_speed
                })
        except Exception as exc:
            return jsonify({'error': 'Unexpected error', 'details': str(exc)}), 500
        return jsonify()