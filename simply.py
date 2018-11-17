# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-17


def wsgi_app(environ, start_response):
	body = b"<h1>Hello World!</h1>"
	status = "200 OK"
	print("env: ", environ)
	rsp_headers = [
		('Content-Type', 'text/html'),
		('Content-Length', str(len(body)))
	]
	start_response(status, rsp_headers)
	return [body]
