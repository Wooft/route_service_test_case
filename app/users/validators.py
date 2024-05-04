from pydantic import BaseModel, validator

class UserValidator(BaseModel):
    """
    Валидатор для проверки данных пользователя при регистрации.

    Поля:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.
        repeat_password (str): Подтверждение пароля пользователя.
        email (str): Электронная почта пользователя.

    Методы:
        password_strength(cls, value): Проверяет надежность пароля.
        passwords_match(cls, v, values): Проверяет, что пароль и повтор пароля совпадают.
    """
    username: str
    password: str
    repeat_password: str
    email: str
    @validator('password')
    def password_strengtht(cls, value):
        """
        Валидатор для проверки силы пароля.

        Проверяет, что пароль содержит не менее 6 символов. Если пароль слишком короткий,
        вызывается исключение ValueError.

        Args:
            value (str): Пароль для проверки.

        Returns:
            str: Исходный пароль, если он прошел проверку.

        Raises:
            ValueError: Если пароль содержит менее 6 символов.
        """
        if len(value) < 6:
            raise ValueError('Password os too short')
        return value

    @validator('repeat_password')
    def passwords_match(cls, v, values):
        """
        Валидатор для проверки совпадения пароля и подтверждения пароля.

        Проверяет, что значение 'repeat_password' совпадает со значением 'password'.
        Если значения не совпадают, вызывается исключение ValueError.

        Args:
            v (str): Подтверждение пароля для проверки.
            values (dict): Словарь всех полей, переданных в модель.

        Returns:
            str: Подтверждение пароля, если оно совпадает с паролем.

        Raises:
            ValueError: Если подтверждение пароля не совпадает с паролем.
        """
        if 'password' in values and v != values['password']:
            raise ValueError('Password and repeat password do not match')
        return v