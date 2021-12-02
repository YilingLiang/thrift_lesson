from match_server.match import Match
from save_client.save import Save
from match_server.match.ttypes import User

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from threading import Thread, Condition
from queue import Queue
import time

class Task:
    def __init__(self, user, ty):
        self.user = user
        self.ty = ty

class MessageQueue:
    def __init__(self):
        self.queue = Queue()
        self.cv = Condition()

mq = MessageQueue()

class Pool:
    def __init__(self):
        self.users = []
    
    def save_result(self, a, b):
        print("Match result:{} - {}".format(a, b))
        # Make socket
        transport = TSocket.TSocket('localhost', 9091) # 9090已被match服务端占用

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        client = Save.Client(protocol)

        # Connect!
        transport.open()

        client.save_data("acs_900", "passwd", a, b)
        # Close!
        transport.close()
    
    def match(self):
        while len(self.users) > 1:
            print(self.users)
            a = self.users[0]
            b = self.users[1]
            self.users.pop(0)
            self.users.pop(0)
            self.save_result(a.id, b.id)

    def add(self, user:User):
        self.users.append(user)

    def remove(self, user:User):
        for i in range(len(self.users)):
            if self.users[i].id == user.id:
                self.users.pop(i)
                break
pool = Pool()

class MatchHandler:
    def __init__(self):
        self.log = {}

    def add_user(self, user, info=""):
        print("add user")
        # print(mq.cv)
        mq.queue.put(Task(user, "add"))
        mq.cv.acquire()
        mq.cv.notify()
        mq.cv.release()
        # print(mq.cv)
        
        return 0

    def remove_user(self, user, info=""):
        print("remove user")
        mq.queue.put(Task(user, "remove"))
        mq.cv.acquire()
        mq.cv.notify()
        mq.cv.release()
        
        return 0

def consume_task():
    while True:
        # mq.queue.mutex.acquire() # 上锁
        if mq.queue.empty():
            # print("队列为空, 阻塞当前线程")
            time.sleep(3)
            mq.cv.acquire()
            mq.cv.wait()
        else:
            task = mq.queue.get()
            # mq.q.mutex.release() # 解锁
            # TODO TASK
            
            if task.ty == "add":
                pool.add(task.user)
            elif task.ty == "remove":
                pool.remove(task.user)
            pool.match();


if __name__ == '__main__':
    handler = MatchHandler()
    processor = Match.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)
    
    thread = Thread(target=consume_task)
    thread.start()

    print('Starting the server...')
    server.serve()
    print('done.')
