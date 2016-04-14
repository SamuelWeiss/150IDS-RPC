import json
import subprocess
import sys

builtins = ['int', 'string', 'float', 'void']

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
		  	proxy += ('    return deserialize_' + i["return_type"] + '(string(readBuffer));\n')
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
				#if your type is not a builtin, then add a star, you're a pointer
				#TODO: remember to free later
				#TODO: clean up type names
				if j["type"] not in builtins:
					if '[' in j["type"]:
						cleaned_name = j["type"][0:j["type"].index('[')]
						stub += cleaned_name
						for useless in range(j["type"].count('[')):
							stub += '* '
					else:
						stub += j["type"]
						stub += '* '
				else:
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
		#Todo: free stuff
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
		readlen = RPCSTUBSOCKET-> read(buffer, 1);
		output += buffer[0];
	}while(readlen > 0);

	return output;

}

string get_name_from_message(string message){
	if(message.at(0) != '{'){
		cerr << "I unno, raise an error or soemthing"<< endl;
		exit(1);
	}
	for(unsigned i = 1; i < message.length(); i++){
		if(message.at(i) == '-'){
			return message.substr(1, i - 1);
		}
	}
       	cerr << "I unno, raise an error or soemthing"<< endl;
        exit(1);
        return "";
}

string get_arguments_from_message(string message){
	if(message.at(0) != '{'){
		cerr << "I unno, raise an error or soemthing"<< endl;
		exit(1);
	}
	for(unsigned i = 1; i < message.length(); i++){
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

"""
	if_block = []
	for k,i in functions.iteritems():
		temp = 'if(strcmp( name.c_str(), "'
		temp += k
		temp += '") == 0){\n'
		temp += '        __'
		temp += k
		if not i["arguments"]:
			temp += "();\n"
		else:
			temp += "(args);\n"
		temp += "}"
		if_block.append(temp)

	output += " else ".join(if_block)
	output += "\n}\n"

	return output





def generate_proxy_file(functions, name):
	output = """
#include "rpcproxyhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
"""
	output += '#include "' + name + '"\n'
	output += generate_function_proxies(functions)
	return output


def generate_stub_file(functions, name):
	output = """
#include "rpcstubhelper.h"
#include "data_packing.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
"""
	output += '#include "' + name + '"\n'
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

if len(sys.argv) != 2:
	print "There was an unsupported number of arguments!"
	print "Usage is : python rpcgenerate.py <idl_name>"
	sys.exit(1)
elif sys.argv[1][-3:] != "idl":
	print "RPCgenerate called on inappropriate file, use only with .idl files"
	sys.exit()

prepare_rpc(sys.argv[1])



