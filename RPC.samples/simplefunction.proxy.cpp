#include "simplefunction.idl"
#include "rpcproxyhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
#include <string>
using namespace C150NETWORK;
void func3 ( ) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "func3-" );
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
}

void func2 ( ) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "func2-" );
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
}

int cur_time ( ) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "cur_time-" );
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_int(string(readBuffer));
}

void func1 ( ) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "func1-" );
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
}

