from routes.views import Hello

hello_url = {
    'rule': '/hello',
    'view_func': Hello.as_view('Hello'),
    'methods': ['GET', 'POST']
}