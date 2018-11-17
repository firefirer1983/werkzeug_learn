# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-15


import os
import traceback
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request,Response
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from jinja2 import Environment, FileSystemLoader
from redis import Redis


class Shortly:
	
	def __init__(self, redis_config):
		self._redis = Redis(
			redis_config["host"],
			redis_config["port"]
		)
		self.jinja_env = Environment(
			loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
			autoescape=True,
			auto_reload=True
		)
		
		self.url_map = Map([
			Rule("/", endpoint="new_url"),
			Rule("/<short_id>", endpoint="follow_short_link"),
			Rule("/<short_id>+", endpoint="short_link_details")
		])
	
	def render_template(self, template_name, **context):
		t = self.jinja_env.get_template(template_name)
		render_ret = t.render(context)
		print("render ret:", render_ret)
		return Response(render_ret, mimetype="text/html")

	@staticmethod
	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
		except HTTPException as e:
			return e
		else:
			func = getattr(self , "on_" + endpoint)
			return func(request, **values)
	
	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request=request)
		return response(environ, start_response)
	
	def __call__(self, environ, start_response):
		print(os.getpid())
		return self.wsgi_app(environ, start_response)

	def on_new_url(self, request, **value):
		print("on_new_url")
	
	def on_new_url(self, request, **value):
		print("on_new_url")
	
	def on_new_url(self, request, **value):
		print("on_new_url")


def create_app(static_serving=True):
	
	app = Shortly(dict(
		host="localhost",
		port=6379))
	
	if static_serving:
		app.wsgi_app = SharedDataMiddleware(
			app=app.wsgi_app,
			exports={
				"/static": os.path.join(os.path.dirname(__file__), "static")
			}
		)
		
	return app


app = create_app(static_serving=True)

if __name__ == '__main__':
	app = create_app(static_serving=True)
	run_simple("localhost", 5000, app, use_debugger=True, use_reloader=True)
