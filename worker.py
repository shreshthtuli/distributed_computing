import rpyc
import time
import sys
from rpyc.utils.server import ThreadedServer

@rpyc.service
class TestService(rpyc.Service):
    @rpyc.exposed
    def run_code(self, code):
        loc = {}
        exec(code, globals(), loc)  
        return loc['result']

print('starting worker')
server = ThreadedServer(TestService, port=int(sys.argv[1]))
server.start()