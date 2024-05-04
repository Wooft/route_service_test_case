from users.views import Register
from routes.views import RouteView, SetEndTime
from analytics.views import AnalyticsView

urls = [
        {
            'rule': '/register',
            'view_func': Register.as_view('register'),
            'methods': ['POST', 'GET']
        },
        {
            'rule': '/routes',
            'view_func': RouteView.as_view('routes'),
            'methods': ['GET', 'POST']
        },
        {
            'rule': '/set_end_time',
            'view_func': SetEndTime.as_view('end_time'),
            'methods': ['PATCH',]
        },
        {
            'rule': '/analytics',
            'view_func': AnalyticsView.as_view('analytics'),
            'methods': ['GET', ]
        }
]