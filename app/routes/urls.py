from routes.views import RouteView, Register

urls = [{
            'rule': '/routes',
            'view_func': RouteView.as_view('routes'),
            'methods': ['GET', 'POST']
        },
        {
            'rule': '/register',
            'view_func': Register.as_view('register'),
            'methods': ['POST', 'GET']
        }]