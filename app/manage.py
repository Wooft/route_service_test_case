from flask import Flask
from app.routes.urls import hello_url

app = Flask('app')

app.add_url_rule(rule=hello_url['rule'],
                 view_func=hello_url['view_func'],
                 methods=hello_url['methods'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)