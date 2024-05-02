from flask import Flask
from app.routes.urls import urls
from flask_login import LoginManager

app = Flask('app')

for url in urls:
    app.add_url_rule(rule=url['rule'],
                     view_func=url['view_func'],
                     methods=url['methods'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)