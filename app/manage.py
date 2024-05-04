from flask import Flask
from urls import urls
from api import api
from users.views import ns
from routes.views import ns_routes
from analytics.views import analytics_namespace

app = Flask('app')


api.init_app(app)
api.add_namespace(ns)
api.add_namespace(ns_routes)
api.add_namespace(analytics_namespace)


for url in urls:
    app.add_url_rule(rule=url['rule'],
                     view_func=url['view_func'],
                     methods=url['methods'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)