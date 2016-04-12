#include "simplefunction.idl"
#include "rpcstubhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
void __func3(){
    func3();
    string output = "Done";
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

void __func2(){
    func2();
    string output = "Done";
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

void __cur_time(){
    string output = serialize_int(cur_time());
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

void __func1(){
    func1();
    string output = "Done";
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}


string read_stream_to_string(){
	string output;
	char buffer[2];
	ssize_t readlen;

	do{
		readlen = readlen = RPCSTUBSOCKET-> read(buffer, 1);
		output += buffer[0];
	}while(readlen > 0);

	return output;

}

string get_name_from_message(string message){
	if(message.at(0) != '{'){
		cerr << "I unno, raise an error or soemthing"<< endl;
		exit(1);
	}
	for(int i = 1; i < message.length(); i++){
		if(message.at(i) == '-'){
			return message.substr(1, i - 1);
		}
	}
}

string get_arguments_from_message(string message){
	if(message.at(0) != '{'){
		cerr << "I unno, raise an error or soemthing"<< endl;
		exit(1);
	}
	for(int i = 1; i < message.length(); i++){
		if(message.at(i) == '-'){
			return message.substr(i+1, message.length() - (i+2));
		}
	}
}

void dispatchFunction() {
	string message = read_stream_to_string();
	string name = get_name_from_message(message);
	string args = get_arguments_from_message(message);

if(strcmp( name, "func3") == 0){
        __func3(args);
} else if(strcmp( name, "func2") == 0){
        __func2(args);
} else if(strcmp( name, "cur_time") == 0){
        __cur_time(args);
} else if(strcmp( name, "func1") == 0){
        __func1(args);
}
}
