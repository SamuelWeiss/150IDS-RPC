
#include "rpcproxyhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
#include "testfunction.idl"
float halve ( int x) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "halve-" );
    server_call.append(serialize_int( x));
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_float(string(readBuffer));
}

string replace ( string base, string search, string replace_me) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "replace-" );
    server_call.append(serialize_string( base));
    server_call.append(serialize_string( search));
    server_call.append(serialize_string( replace_me));
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_string(string(readBuffer));
}

void silly ( ) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "silly-" );
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
}

int pow ( int x, int y) { 
    char readBuffer[20];
    string server_call = "";
    server_call.append( "pow-" );
    server_call.append(serialize_int( x));
    server_call.append(serialize_int( y));
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));
    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_int(string(readBuffer));
}

