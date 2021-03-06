// This autogenerated skeleton file illustrates how to build a server.
// You should copy it to another filename to avoid overwriting it.

#include "save_server/Save.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <vector>
#include <iostream>

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using namespace  ::save_service;
using namespace std;

class SaveHandler : virtual public SaveIf {
 public:
  SaveHandler() {
    // Your initialization goes here
  }

  /**
   * * username: myserver的名称
   *      * password: myserver的密码的md5sum的前8位
   *           * 用户名密码验证成功会返回0，验证失败会返回1
   *                * 验证成功后，结果会被保存到myserver:homework/lesson_6/result.txt中
   * 
   * @param username
   * @param password
   * @param player1_id
   * @param player2_id
   */
  int32_t save_data(const std::string& username, const std::string& password, const int32_t player1_id, const int32_t player2_id) {
    // Your implementation goes here
    printf("save_data\n");
    cout << username << " " << password << " " << player1_id << " " << player2_id << endl;

    return 0;
  }

};

int main(int argc, char **argv) {
  int port = 9091;// 9090 已经被 match_server 占用
  ::std::shared_ptr<SaveHandler> handler(new SaveHandler());
  ::std::shared_ptr<TProcessor> processor(new SaveProcessor(handler));
  ::std::shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  ::std::shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  ::std::shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}

