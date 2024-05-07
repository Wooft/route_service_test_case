# Инструкция по развертыванию сервиса управления маршрутами

## Введение
Это руководство описывает процесс развертывания веб-сервиса для управления маршрутами. Сервис использует данные от https://openrouteservice.org и поддерживает управление через Docker-compose.

## Как начать
Прежде чем приступить к установке, вам понадобится:
- Учетная запись на https://openrouteservice.org для получения API-токена.
- Docker и Docker-compose, установленные на вашей машине.

## Шаги по установке

1. Клонирование проекта
   Откройте терминал и выполните команду:
      git clone https://github.com/Wooft/route_service_test_case.git


2. Настройка окружения
   В корневой директории проекта создайте файл .env с необходимыми настройками:  
   DB_USER=postgres  
   DB_PASSWORD=postgres  
   DB_NAME=routes  
   DB_HOST=db  
   API_TOKEN=Ваш_API_токен   
   
   Примечание: Замените Ваш_API_токен на токен, полученный от openrouteservice.org.

3. Запуск приложения
   Используйте Docker-compose для запуска приложения:  
      `docker-compose up`
   

## Доступ к сервису
После запуска приложение будет доступно по адресу:
- Главная страница: http://localhost
- Документация API: http://localhost/swagger
- Регистрация пользователей: http://localhost/register
- Создание маршрутов и получение списка маршрутов пользователя: http://localhost/routes
- Добавление времени окончания маршрута: http://localhost/set_end_time
- Получение данных аналитики пользователя: http://localhost/analytics