#include <iostream>
#include <string>
#include <sstream>

#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>

#include "match_client/Match.h"
#include "match_client/match_types.h"

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace match_service;

void operate(string op, int32_t user_id, string username, int32_t score) {

    std::shared_ptr<TTransport> socket(new TSocket("localhost", 9090));
    std::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
    std::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
    MatchClient client(protocol);

    try {
        transport->open();

        User user;
        user.__set_id(user_id);
        user.__set_name(username);
        user.__set_score(score);
        
        if (op == "add")
            client.add_user(user, "");
        else if (op == "remove")
            client.remove_user(user, "");

        transport->close();
    } catch (TException& tx) {
        cout << "ERROR: " << tx.what() << endl;
    }
}

int main(){
    string str;
    string op; int32_t user_id; string username; int32_t score;
    while(getline(cin, str)){
        stringstream ss(str);
        string a, b, c, d;
        ss >> a, ss >> b, ss >> c, ss >> d;
        op = a, user_id = stoi(b), username = c, score = stoi(d);
        operate(op, user_id, username, score);
    }
    return 0;
}
