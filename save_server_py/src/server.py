from save_server.save import Save

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import os

class SaveHandler:
    def __init__(self):
        self.log = {}

    def save_data(self, username, password, id1, id2):
        print(username, password, id1, id2)
        path = os.path.expanduser('~') + '/thrift_save/'
        if not os.path.exists(path): 
            os.mkdir(path)
        file = path + 'match.txt'
        with open(file, 'w') as f:
            match_result = str(id1) + ' - ' + str(id2) + '\n'
            f.write('Match Result:\n' + match_result)
        return 0



if __name__ == '__main__':
    handler = SaveHandler()
    processor = Save.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
