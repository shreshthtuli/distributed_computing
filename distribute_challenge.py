import rpyc
import inspect

server_c = rpyc.connect('localhost', 18811)

class compute_this(object):
	def __init__(self, x):
		self.function_def = inspect.getsource(x).replace('@compute_this', '')
		self.function_name = str(x.__name__)

	def __call__(self, x):
		self.args = x
		return self
		
	def run(self):
		code = (self.function_def +
			'\nresult = ' + self.function_name +
			'(' + str(self.args) + ')')
		worker_port = -1
		while worker_port == -1:
			worker_port = server_c.root.find_free_worker()
		worker_c = rpyc.connect('localhost', worker_port)
		result = worker_c.root.run_code(code)
		server_c.root.free_worker(worker_port)
		return result
