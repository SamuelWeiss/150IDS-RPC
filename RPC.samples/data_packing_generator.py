import json
import subprocess
import re

def fix_array_name(str):
	return str.replace("[", "_").replace(']', "_")

def generate_serialize_headers(type_name, type_desc):
	if type_desc["type_of_type"] == "builtin":
		return ""
	if type_desc["type_of_type"] == "array":
		fixed_type = fix_array_name(type_name)
		base_type = type_name[2:type_name.index('[')]
		input_type = base_type
		input_type += ('* ' * type_name.count('['))
		return "string serialize_" + fixed_type + "(" + input_type + " val);\n"
	if type_desc["type_of_type"] == "struct":
		return "string serialize_" + type_name + "(" + type_name + " val);\n"


def generate_deserialize_headers(type_name, type_desc):
	if type_desc["type_of_type"] == "builtin":
		return ""
	if type_desc["type_of_type"] == "array":
		fixed_type = fix_array_name(type_name)
		base_type = type_name[2:type_name.index('[')]
		input_type = base_type
		input_type += ('* ' * type_name.count('['))
		return input_type + " deserialize_" + fixed_type + "(string args);\n"
	if type_desc["type_of_type"] == "struct":
		return type_name + "* deserialize_" + type_name + "(string args);\n"


def generate_serialize(type_name, type_desc):
	output = ""

	#case 1: simple builtins, just copy what we've written
	if type_desc["type_of_type"] == "builtin":
		#print "builtin: " + type_name
		return ""

	#case 2: arrays, iterate over all elements and serialize them
	if type_desc["type_of_type"] == "array":
		fixed_type = fix_array_name(type_name)
		first_num_re = re.search('(?<=_)[0-9]+(?=_)', fixed_type)
		num_elem = first_num_re.group(0)
		base_type = type_name[2:type_name.index('[')]
		input_type = base_type
		input_type += ('* ' * type_name.count('['))

		output =   "string serialize_" + fixed_type + "(" + input_type + " val){\n"
		output +=  "    string output;\n"
		output += ('    output.append("{' + fixed_type + ':");\n')
		output += ("    for(int i = 0; i < " + num_elem + "; i++){\n")
		output += ("        output.append(serialize_" + fix_array_name(type_desc['member_type']) + "(val[i]));\n")
		output += "    }\n"
		output += '     output.append("}");\n'
		output += "    return output;\n"
		output += "}\n"
		return output

	#case 3: loop over all members and serialize them
	if type_desc["type_of_type"] == "struct":
		fixed_type = fix_array_name(type_name)
		output =  "string serialize_" + fixed_type + "(" + fixed_type + " val){\n"
		output += "    string output;\n"
		output += ('    output.append("{' + fixed_type + ':");\n')
		for i in type_desc["members"]:
			output += ("    output.append(serialize_" + fix_array_name(i["type"]) + "(val." + i["name"] + "));\n")
		output += '    output.append("}");\n'
		output += '    return output;\n'
		output += '}\n'
		return output

def generate_deserialize(type_name, type_desc, types):
	if type_desc["type_of_type"] == "builtin":
		return ""
	if type_desc["type_of_type"] == "array":
		fixed_type = fix_array_name(type_name)
		first_num_re = re.search('(?<=_)[0-9]+(?=_)', fixed_type)
		num_elem = first_num_re.group(0)
		base_type = type_name[2:type_name.index('[')]
		return_type = base_type
		return_type += ('* ' * type_name.count('['))
		output = return_type
		output += " deserialize_"
		output += fixed_type
		output += "( string args ) {\n"

		output += "    args = args.substr("
		output += str(2 + len(fixed_type))
		output += ", args.length());\n    "
		output += return_type
		output += "retval = ("
		output += return_type
		output += ")malloc(sizeof("
		output += return_type[0:-2]
		output += ") * " 
		output += str(num_elem)
		output += ");\n"
		output += ("    for(int i = 0; i < " + str(num_elem) + "; i++){\n")
		if types[type_desc["member_type"]]["type_of_type"] == "struct":
			output += ("        retval[i] = *deserialize_" + fix_array_name(type_desc['member_type']) + "(get_var_string(args));\n" )
		else:
			output += ("        retval[i] = deserialize_" + fix_array_name(type_desc['member_type']) + "(get_var_string(args));\n" )
		output += ("        args = eat_value(args);\n")
		output += "    }\n"
		output += "    return retval;\n"
		output += "}\n"
		return output

	if type_desc["type_of_type"] == "struct":
		return_type = type_name + "* "

		output = type_name
		output += ("* deserialize_" + type_name + "(string args){\n")
		output += ("    args = args.substr(" + str(2 + len(type_name)) + ", args.length());\n    ")
		output += (return_type + "retval = (" + return_type + ")malloc(sizeof(" + type_name + "));\n")
		temp_arr_counter = 97
		for i in type_desc["members"]:
			if "[" in i["type"]:
				output += (i["type"][2:i["type"].index('[')] + '* ' + " temp_arr = ")
				output += "deserialize_" + fix_array_name(i["type"]) + "(get_var_string(args));\n"
				num_elems = types[i["type"]]["element_count"]

				output += ("for (int z=0; z <" + str(num_elems) + "; z++) {\n" )
				if types[i["type"]]["member_type"] == "struct":
					output += ("retval->" + i["name"] + "[z] = *temp_arr[z];\n")
				else:
					output += ("retval->" + i["name"] + "[z] = temp_arr[z];\n")
				output += "}\n"
			else:
				output += ("    retval->" + i["name"] + " = deserialize_" + fix_array_name(i["type"]) + "(get_var_string(args));\n")
			output += ("    args = eat_value(args);\n")
		output += "    return retval;\n"
		output += "}\n"

		return output

def generate_data_packing_header(types, name):
	output = """
#include <string>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <sstream>

#define OPEN_DELIM "{"
#define CLOSE_DELIM "}"
#define VAR_START ":"
#define INT 1
#define FLOAT 2
#define BOOL 3
#define STRING 4
#define CHAR 5

using namespace std;
"""
	output += '#include "' + name + '"\n'

	output += """
void myReplace(std::string& str, const std::string& oldStr, const std::string& newStr);
string get_var_string(string str);
string chop_string(string str, int len);
string eat_value(string str);
string serialize_int(int val);
int deserialize_int(string str);
string serialize_float(float val);
float deserialize_float(string str);
string serialize_string(string val);
string deserialize_string(string str);
void deserialize_void(string str);
"""
	for i in types:
		output += generate_serialize_headers(i, types[i])
		output += generate_deserialize_headers(i, types[i])

	return output;

def generate_data_packing_cpp(types, name):

	output = ('#include "' + name[:-4] + '_data_packing.h"' )

	output += """
#include "data_packing.h"
#include <string>
#include <cstring>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <sstream>

using namespace std;

void myReplace(std::string& str, const std::string& oldStr, const std::string& newStr){
  size_t pos = 0;
  while((pos = str.find(oldStr, pos)) != std::string::npos){
     str.replace(pos, oldStr.length(), newStr);
     pos += newStr.length();
  }
}

string get_var_string(string str){
	//pulls out the first val
	int curly_count = 1;
	for(unsigned i = 1; i < str.length(); i++){
		if(str.at(i) == '}'){
			if(str.at(i-1) == '\\\\'){
				continue;
			} else {
				curly_count--;
			}
		} else if(str.at(i) == '{'){
			if(str.at(i-1) == '\\\\'){
				continue;
			} else {
				curly_count++;
			}
		}

		if(curly_count == 0) {
			return str.substr(0, i + 1);
		}
	}
	cerr << "something bad happened" << endl;
	exit(1);
	return "";
}


string eat_value(string str){
	int curly_count = 1;
	for(unsigned i = 1; i < str.length(); i++){
		if(str.at(i) == '}'){
			if(str.at(i-1) == '\\\\'){
				continue;
			} else {
				curly_count--;
			}
		} else if(str.at(i) == '{'){
			if(str.at(i-1) == '\\\\'){
				continue;
			} else {
				curly_count++;
			}
		}

		if(curly_count == 0) {
			return str.substr(i+1, str.length() - (i + 1));
		}
	}
	cerr << "something bad happened" << endl;
	exit(1);
	return "";
}

string serialize_int(int val){
	string output;
	output.append(OPEN_DELIM);
	output.append("int");
	output.append(VAR_START);
	stringstream ss;
	ss << val;
	output.append(ss.str());
	output.append(CLOSE_DELIM);
	return output;
}

int deserialize_int(string str){
	string conv_buff = str.substr(5, str.length() - (1 + 5));
	return atoi(conv_buff.c_str());
}

string serialize_float(float val){
	string output;
	output.append(OPEN_DELIM);
	output.append("float");
	output.append(VAR_START);
	stringstream ss;
	ss << val;
	output.append(ss.str());
	output.append(CLOSE_DELIM);
	return output;
}

float deserialize_float(string str){
	string conv_buff = str.substr(7, str.length() - (1 + 7));
	return atof(conv_buff.c_str());
}

string serialize_string(string val){
	string output;
	output.append(OPEN_DELIM);
	output.append("string");
	output.append(VAR_START);

	//need to escape close curly braces
	myReplace(val, CLOSE_DELIM, "\\\\}");
	myReplace(val, OPEN_DELIM,  "\\\\{");
	output.append(val);
	output.append(CLOSE_DELIM);
	return output;
}

string deserialize_string(string str){
	myReplace(str, "\\\\}", "}");
	myReplace(str, "\\\\{", "{");
	return str.substr(8, str.length() - (1 + 8));
}

void deserialize_void(string str){
  if(strcmp(str.c_str(), "Done") == 0){
	  cerr << "got a bad void value, exiting" << endl;
	  exit(1);
	}
}
"""
	for i in types:
		output += generate_serialize(i, types[i])
		output += generate_deserialize(i, types[i], types)

	return output;


def fix_array_name(str):
	return str.replace("[", "_").replace(']', "_")

