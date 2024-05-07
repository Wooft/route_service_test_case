from flask.views import MethodView
from flask import jsonify, request
from users.validators import UserValidator
from pydantic_core._pydantic_core import ValidationError
from database import Session, User
from api import user_model
from flask_restx import Namespace
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


ns = Namespace('/register', description='Регистрация пользователей')


@ns.route('/authentication')
class Register(MethodView):
    @ns.expect(user_model)
    @ns.response(201, 'Пользователь создан')
    @ns.response(400, 'Ошибка проверки введенных данных')
    @ns.response(409, 'Ошибка создания пользователя, например такой пользователь уже зарегистрирован')
    @ns.response(500, 'Другие ошибки')
    def post(self):
        """
        Создает нового пользователя в системе.

        Этот метод принимает JSON-запрос с данными пользователя, проводит их валидацию
        и, если данные корректны, добавляет нового пользователя в базу данных. В случае
        успешного добавления возвращает имя пользователя и статус-код 201. Если происходят
        ошибки валидации или нарушения целостности данных (например, пользователь с таким же
        именем или email уже существует), возвращает соответствующее сообщение об ошибке
        и статус-код ошибки.

        Возвращает:
            - Response: Объект ответа Flask, содержащий JSON с данными о созданном
              пользователе или сообщением об ошибке.
        """
        try:
            user_data = UserValidator(**request.get_json())

            with Session() as session:
                new_user = User(
                    username=user_data.username,
                    password=user_data.password,
                    email=user_data.email
                )
                session.add(new_user)
                session.commit()

                return jsonify({'data': new_user.username, 'id': new_user.id}), 201

        except ValidationError as val_err:
            return jsonify({'error': 'Validation error', 'details': str(val_err.errors()[0]['msg'])}), 400

        except IntegrityError as int_err:
            session.rollback()
            return jsonify({'error': 'Integrity error', 'details': str(int_err.orig)}), 409

        except SQLAlchemyError as sql_err:
            session.rollback()
            return jsonify({'error': 'Database error', 'details': str(sql_err)}), 500

        except Exception as exc:
            return jsonify({'error': 'Unexpected error', 'details': str(exc)}), 500