
#include "rpcstubhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
#include "testfunction.idl"
void __halve( string arguments ){
    int x = deserialize_int(get_var_string(arguments));
    arguments = eat_value(arguments);
    string output = serialize_float(halve(x));
    output += (char)23;
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

void __replace( string arguments ){
    string base = deserialize_string(get_var_string(arguments));
    arguments = eat_value(arguments);
    string search = deserialize_string(get_var_string(arguments));
    arguments = eat_value(arguments);
    string replace_me = deserialize_string(get_var_string(arguments));
    arguments = eat_value(arguments);
    string output = serialize_string(replace(base, search, replace_me));
    output += (char)23;
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

void __silly(){
    silly();
    string output = "Done";
    output += (char)23;
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

void __pow( string arguments ){
    int x = deserialize_int(get_var_string(arguments));
    arguments = eat_value(arguments);
    int y = deserialize_int(get_var_string(arguments));
    arguments = eat_value(arguments);
    string output = serialize_int(pow(x, y));
    output += (char)23;
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}


string read_stream_to_string(){
	string output;
	char buffer[2];

	do{
		RPCSTUBSOCKET-> read(buffer, 1);
		output += buffer[0];
	}while(buffer[0] != (char)23 );

	return output;

}

string get_name_from_message(string message){
	for(unsigned i = 0; i < message.length(); i++){
		if(message.at(i) == '-'){
            if(message.at(0) == 0)
                return message.substr(1,i-1);
            else
    			return message.substr(0,i);
		}
	}
  cerr << "I unno, raise an error or soemthing"<< endl;
  exit(1);
  return "";
}

string get_arguments_from_message(string message){
	for(unsigned i = 0; i < message.length(); i++){
		if(message.at(i) == '-'){
			return message.substr(i+1, message.length() - (i+2));
		}
	}
  cerr << "I unno, raise an error or soemthing"<< endl;
  exit(1);
  return "";
}

void dispatchFunction() {
	string message = read_stream_to_string();
	string name = get_name_from_message(message);
	string args = get_arguments_from_message(message);

if(strcmp( name.c_str(), "halve") == 0){
        __halve(args);
} else if(strcmp( name.c_str(), "replace") == 0){
        __replace(args);
} else if(strcmp( name.c_str(), "silly") == 0){
        __silly();
} else if(strcmp( name.c_str(), "pow") == 0){
        __pow(args);
}else {
	cerr << "Unknown function called: " << name << endl;
}
}