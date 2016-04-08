import json
import subprocess
import pdb


print "This is testing code"
print "type in the IDL file you'd like to try"
#file_name = raw_input("Name: " )
file_name = "testfunction.idl"

json_as_text = subprocess.check_output(["./idl_to_json", file_name])
idl_contents = json.loads(json_as_text)
#print idl_contents
#pdb.set_trace()

functions = idl_contents["functions"]
types = idl_contents["types"]


def generate_function_proxies(functions):
	output = ""
	for k,i in functions.iteritems():
		proxy = ""
		proxy += i["return_type"]
		proxy += " "
		proxy += k
		proxy += " ( "

		temp = []
		for j in i["arguments"]:
			temp.append(j["type"] + " " + j["name"])

		proxy += ', '.join(temp)

		proxy += ") { \n"
		
		#setup a datastructure to hold message to server
		proxy += '    char readBuffer[20];\n'
		proxy += '    string server_call = "";\n'
		proxy += ('    server_call.append( "' + k + '-" );\n')
		for j in i["arguments"]:
			proxy += ('    server_call.append(serialize_' + j["type"] + '( ' + j["name"] + '));\n')
		proxy += "    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);\n"
		proxy += "    RPCPROXYSOCKET->read(readBuffer, sizeof(readBuffer));\n"
		proxy +=   """    if (strncmp(readBuffer,"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }\n"""
	  	if(i["return_type"] != "void"):
		  	proxy += ('    return deserialize_' + i["return_type"] + '(std::string str(readBuffer));\n')
	  	proxy += "}\n\n"
	  	output += proxy
	return output

# print generate_function_proxies(functions)

def generate_function_stubs(functions):
	output = ""
	for k,i in functions.iteritems():
		stub = "void __"
		stub += k
		if len(i["arguments"]) == 0:
			stub += "(){\n"
		else:
			stub += "( string arguments ){\n"
			for j in i["arguments"]:
				stub += "    "
				stub += j["type"]
				stub += ' '
				stub += j["name"]
				stub += " = deserialize_"
				stub += j["type"]
				stub += "(arguments);\n"
				stub += "    arguments = eat_value(arguments);\n"
		if i["return_type"] == "void":
			#just return done
			stub += ("    " +k + '(') 
			temp = []
			for j in i["arguments"]:
				temp.append(j["name"])
			stub += ", ".join(temp)	
			stub += ');\n'
			stub += '    string output = "Done";\n'
		else:
			stub += ('    string output = serialize_' + i["return_type"] + '(' + k + '(') 
			temp = []
			for j in i["arguments"]:
				temp.append(j["name"])
			stub += ", ".join(temp)	
			stub += '));\n'
		stub += '    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);\n'
		stub += '}\n\n'
		output += stub
	return output

def generate_dispatch_code(functions):
	output ="""
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

"""
	if_block = []
	for k,i in functions.iteritems():
		temp = 'if(strcmp( name, "'
		temp += k
		temp += '") == 0){\n'
		temp += '        __'
		temp += k
		temp += "(args);\n"
		temp += "}"
		if_block.append(temp)

	output += " else ".join(if_block)
	output += "\n}\n"

	return output





def generate_proxy_file(functions, name):
	output = '#include "' + name + '"'
	output += """
#include "rpcproxyhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
"""
	output += generate_function_proxies(functions)
	return output


def generate_stub_file(functions, name):
	output = '#include "' + name + '"'
	output += """
#include "rpcstubhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
"""
	output += generate_function_stubs(functions)
	output += generate_dispatch_code(functions)
	return output


def prepare_rpc(file_name):
	json_as_text = subprocess.check_output(["./idl_to_json", file_name])
	idl_contents = json.loads(json_as_text)

	stub_file = open((file_name[:-3] + "stub.cpp"), "w")
	stub_file.write(generate_stub_file(idl_contents["functions"], file_name))
	stub_file.close()

	proxy_file = open((file_name[:-3] + "proxy.cpp"), "w")
	proxy_file.write(generate_proxy_file(idl_contents["functions"], file_name))
	proxy_file.close()
	print "success!"

prepare_rpc("testfunction.idl")