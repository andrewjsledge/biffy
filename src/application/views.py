from flask.views import View, MethodView
from flask import jsonify, render_template

from application.decorators import load_session
from application import app


class WebView(View):
    decorators = [load_session]

    def __init__(self, template_name=None, *args, **kwargs):
        self.template_name = template_name

    def dispatch_request(self, *args, **kwargs):
        return render_template(self.template_name)

class APIView(MethodView):
    decorators = [load_session]

    def __init__(self, *args, **kwargs):
        self.data = None

    def dispatch_request(self, *args, **kwargs):
        return jsonify(self.data)


