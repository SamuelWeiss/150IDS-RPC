
#include "rpcproxyhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
#include "testfunction.idl"

string read_stream_to_string(){
	string output;
	char buffer[2];

	RPCPROXYSOCKET-> read(buffer, 1);
  if(buffer[0] != 0) {
    output += buffer[0];
  }

	do{
		RPCPROXYSOCKET-> read(buffer, 1);
		  if(buffer[0] != (char)23) {
        output += buffer[0];
      }
	}while(buffer[0] != (char)23 );

	return output;

}
float halve ( int x) { 
    string server_call = "";
    server_call.append( "halve-" );
    server_call.append(serialize_int( x));
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    string readBuffer = read_stream_to_string();
    if (strncmp(readBuffer.c_str(),"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_float(readBuffer);
}

string replace ( string base, string search, string replace_me) { 
    string server_call = "";
    server_call.append( "replace-" );
    server_call.append(serialize_string( base));
    server_call.append(serialize_string( search));
    server_call.append(serialize_string( replace_me));
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    string readBuffer = read_stream_to_string();
    if (strncmp(readBuffer.c_str(),"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_string(readBuffer);
}

void silly ( ) { 
    string server_call = "";
    server_call.append( "silly-" );
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    string readBuffer = read_stream_to_string();
    if (strncmp(readBuffer.c_str(),"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
}

int pow ( int x, int y) { 
    string server_call = "";
    server_call.append( "pow-" );
    server_call.append(serialize_int( x));
    server_call.append(serialize_int( y));
    server_call += (char)23;
    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);
    string readBuffer = read_stream_to_string();
    if (strncmp(readBuffer.c_str(),"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }
    return deserialize_int(readBuffer);
}

