'''
rpcgenerate.py
By Sam Weiss and Rachel Hogue

This is a file to be run on the command line with a single argument specifying
an idl file. This program uses an outsode tool to parse that idl file into
json, then generates a few c++ files. These c++ files that are generated
are as follows (where XXX indicates the idl file name):

XXX.stub.cpp
XXX.proxy.cpp
XXX_data_packing.h
XXX_data_packing.cpp

Explanation of files
(Here we will discuss what these files contain and how they will work.
We will do this here because attempting to document both the python
code that generates the c++ files and the c++ code itself is not
intelligible)

XXX.proxy.cpp:

This c++ should be compiled alongside the desired client that will use the
functions specified in the idl file. The purpose of this file is to hold
implementations of functions that, in a way that is opaque to the client,
do an RPC call on the specified server. The proxy file does this in three
steps. First, it calls a function that is generated in XXX_data_packing that
takes in the arguments to the function and converts them to a string that
can be sent to the RPC server. Second, it sends the name of the function being
called along with the string representations of all of the arguments. Lastly,
it  listens to the reponse from the RPC server and feeds it into a function
that converts the string from the socket into the appropriate return value.


XXX.stub.cpp:

This c++ file works in tandem with the proxy file, it works with server code
to allow the RPC system to work. Its main body is a loop that calls a dispatch
function forever. This dispatch function listens to the socket for any messages
sent to it by a client. It then parses the message to find the name of the
function being called, and calls a stub function that is generated in this file.
This stub function unpacks the appropriate arguments from the contents of the
message and calls the user supplied function that was included with the idl
file. The stub function then capture the output from the true function, packs
it to be sent back to the client, sends it, then exists. After that routine has
finished the server returns to the main dispatch calling while loop.

XXX_data_packing.h

This header file simply contains definitions used by the other files.

XXX_data_packing.cpp

This file deals with the serialization and deserialization of all of the data
types specified in the idl file. It works in a straightforward way. First, it 
defines a way to serialize and deserialize all of the builtin types that we 
were asked to implement. These types are int, float, string, and void. We 
crafted by hand functions to convert the builtins into and out of string
formats. We then generate code for arrays and structures that uses repeated
calls to these builtin type serialize and deserialize functions to gain
the ability to serialize and deserialize larger data members.

Note: data_packing generating code is located in data_packing_generator.py

Additional note about functionality:

When implementing this project we ran into a wall with arrays. We found that
our ideas about how they would work didn't quite match up with the way that 
they actually do, and this made it nearly impossible for us to make multi-
dimmensional arrays work. When we were writing our code we were under the 
impression that the arrays that were were working with would operate in the
same way as heap allocated multi dimmensional arrays. That is to say that they
are a pointer to an array of pointers to arrays. However, this is not how they
were defined and therefore not how they were used. Instead they were defined
as a pointer to an array of arrays, where all of the contents are in one 
contiguous block of memory. Because our deserialize functions are external
and therefore must return some value, and that value cannot be an array we 
returned pointers to arrays. This works fine for one dimensional arrays,
however when we attempted to test multi-dimmensional arrays we ran into trouble.
The internal structure of our multi-dimmensional array simply didn't line up
with what the routines were expecting and the solutions that we came up with 
either involved more code than we had time to create or throwing out our 
progress and starting from scratch.

'''





import json
import subprocess
import sys
from data_packing_generator import *

#we will define our builtins for easy access
builtins = ['int', 'string', 'float', 'void']

'''
function generate_function_proxies
takes a dictionary of functions and generates function proxies for them
They have the following form:


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

The c++ function has the same function signature as the function that it is
the proxy for.

First it makes a string called server_call that stores the string that will
be sent to the server.
Then the function name is appended to the string.
Then all of the arguments are serialized and appended to the server_call
Then the message is sent to the server.
Then the response from the server is read and deserialized and returned.

The below python code generates code of similar form to the above.

'''
def generate_function_proxies(functions):
	output = ""

	# we will iterate over all functions in our dictionary
	for k,i in functions.iteritems():
		proxy = ""
		proxy += i["return_type"]
		proxy += " "
		proxy += k
		proxy += " ( "
		temp = []

		#This for loop cycles through all the arguments and copies their
		# type into the function declaration
		# in order to accomplish this we make an array of temporary
		# strings then join them to get the commas right
		for j in i["arguments"]:
			if '[' in j["type"]:
				arr_arg = j["type"][2:j["type"].index('[')] + ('* ' * j["type"].count('[')) + j["name"]
				temp.append(arr_arg)
			else:
				temp.append(j["type"] + " " + j["name"])

		proxy += ', '.join(temp)

		proxy += ") { \n"
		
		#setup a datastructure to hold message to server
		proxy += '    string server_call = "";\n'
		proxy += ('    server_call.append( "' + k + '-" );\n')

		#this for loop again cycles through all the arguments to generate their serializer calls
		for j in i["arguments"]:
			proxy += ('    server_call.append(serialize_' + fix_array_name(j["type"]) + '( ' + j["name"] + '));\n')

		# we append ascii character 23 (the end transmission character) to the end of our messages
		# so that the server knows when tos top listening
		proxy += "    server_call += (char)23;\n"
		proxy += "    RPCPROXYSOCKET->write(server_call.c_str(), server_call.length()+1);\n"
		proxy += "    string readBuffer = read_stream_to_string();\n"
		proxy +=   """    if (strncmp(readBuffer.c_str(),"ERROR", sizeof(readBuffer))==0) {
	        throw C150Exception("simplefunction.proxy: func1() received invalid response from the server");
    }\n"""

        #if the function we're operating on has no return then we don't want to return anything
	  	if(i["return_type"] != "void"):
		  	proxy += ('    return deserialize_' + i["return_type"] + '(readBuffer);\n')
	  	proxy += "}\n\n"
	  	output += proxy
	return output

'''
function generate_function_stubs
takes a dictionary of functions and generates function stubs for them
They have the following form:


void __halve( string arguments ){
    int x = deserialize_int(get_var_string(arguments));
    arguments = eat_value(arguments);
    string output = serialize_float(halve(x));
    output += (char)23;
    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);
}

The c++ function has no return type and simply sends the response to the
client. This function takes a single argument, a string of arguments
that it then parses into all the arguments to the underlying function.

First this function declares local variables for all the arguments and parses
all of them from the arguments.
Second, the read variables that have been read are eaten from the string.
Third, the paresed areguments are passed to the function.
Last, the output is serialized and send back the client.

The below python code generates code of similar form to the above.

'''
def generate_function_stubs(functions):
	output = ""
	#Again we want to go through all the supplied functions
	for k,i in functions.iteritems():
		stub = "void __"
		stub += k

		# if there are no argument then we shouldn't pass in a string as it would be unused
		if len(i["arguments"]) == 0:
			stub += "(){\n"
		else:
			stub += "( string arguments ){\n"
			for j in i["arguments"]:
				stub += "    "
				# if the type is not a builtin then our deserialize function
				# will return a pointer
				# if the type is an array then we need multiple stars
				# (side note, this doesn't work, we don't need ***s we need *[][])
				if j["type"] not in builtins:
					if '[' in j["type"]:
						cleaned_name = j["type"][2:j["type"].index('[')]
						stub += cleaned_name
						stub += ('* ' * j["type"].count('['))
					else:
						stub += j["type"]
						stub += '* '
				else:
					stub += j["type"]
				stub += ' '
				stub += j["name"]
				stub += " = deserialize_"
				stub += fix_array_name(j["type"])
				stub += "(get_var_string(arguments));\n"
				stub += "    arguments = eat_value(arguments);\n"

		#figure out what to send back
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
				if j["type"] not in builtins and '[' not in j["type"]:
					temp.append("*" + j["name"])
				else:
					temp.append(j["name"])
			stub += ", ".join(temp)	
			stub += '));\n'
		stub += '    output += (char)23;\n'
		stub += '    RPCSTUBSOCKET->write(output.c_str(), output.length()+1);\n'
		#Todo: free stuff
		stub += '}\n\n'
		output += stub
	return output


#function generate_dispatch_code
# This adds some prebaked utility code to the stub file
# this code include the dispatch function which is generated
# it tests the name from a given messages against known function signatures
def generate_dispatch_code(functions):
	output ="""
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

"""
	# put in all the names of the function from the idl file
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

	output += "else {\n"
	output += '	cerr << "Unknown function called: " << name << endl;\n'
	output += '}\n'
	output += "}"

	return output


#function generate_proxy_files
#includes the required dependancies with the proxys that we generate
def generate_proxy_file(functions, name):
	output = '#include "' + name[:-4] + '_data_packing.h"\n'
	output += """
#include "rpcproxyhelper.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
"""

	output += """
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
"""

	output += generate_function_proxies(functions)
	return output

#function generate_stub_files
#includes the required dependancies with the stubs that we generate
def generate_stub_file(functions, name):
	output = '#include "' + name[:-4] + '_data_packing.h"\n'
	output += """
#include "rpcstubhelper.h"
#include <cstdio>
#include <cstring>
#include "c150debug.h"
using namespace C150NETWORK;
"""
	output += generate_function_stubs(functions)
	output += generate_dispatch_code(functions)
	return output

#function prepare_rpc
# read in the file name and create all the required files
def prepare_rpc(file_name):
	json_as_text = subprocess.check_output(["./idl_to_json", file_name])
	idl_contents = json.loads(json_as_text)

	stub_file = open((file_name[:-3] + "stub.cpp"), "w")
	stub_file.write(generate_stub_file(idl_contents["functions"], file_name))
	stub_file.close()

	proxy_file = open((file_name[:-3] + "proxy.cpp"), "w")
	proxy_file.write(generate_proxy_file(idl_contents["functions"], file_name))
	proxy_file.close()

	data_packing_cpp_file = open((file_name[:-4] + "_data_packing.cpp"), "w")
	data_packing_cpp_file.write(generate_data_packing_cpp(idl_contents["types"], file_name))
	data_packing_cpp_file.close()

	data_packing_header_file = open((file_name[:-4] + "_data_packing.h"), "w")
	data_packing_header_file.write(generate_data_packing_header(idl_contents["types"], file_name))
	data_packing_header_file.close()

if len(sys.argv) != 2:
	print "There was an unsupported number of arguments!"
	print "Usage is : python rpcgenerate.py <idl_name>"
	sys.exit(1)
elif sys.argv[1][-3:] != "idl":
	print "RPCgenerate called on inappropriate file, use only with .idl files"
	sys.exit()

prepare_rpc(sys.argv[1])



