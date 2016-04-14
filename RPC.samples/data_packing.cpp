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
	string output;
	for(unsigned i = 0; i < str.length(); i++){
		output += str.at(i);
		if(str.at(i) == '\\'){
			if(str.at(i+1) == CLOSE_DELIM[0]){
				output += str.at(i+1);
				i++;
			}
		} else if(str.at(i) == CLOSE_DELIM[0]){
			return output;
		}
	}
	cerr << "something bad happened" << endl;
	exit(1);
	return "";
}

string chop_string(string str, int len){
	str = str.substr(len, str.length());
	return str;
}

string eat_value(string str){
	// if we decide to adapt this for arrays, simply keep a counter
	// of how many open curly braces we have encountered and subtract
	// when we enctounter a close curly brace, when the counter is 0 we
	// are done
	for(unsigned i = 0; i < str.length(); i++){
		if(str.at(i) == '}'){
			if(str.at(i-1) == '\\'){
				continue;
			} else {
				return str.substr(i+1, str.length() - (i + 1));
			}
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
	cerr << "deserialize int " << str << endl;
	string conv_buff = str.substr(5, str.length() - (1 + 5));
		cerr << "deserialize int, conv_buff " << conv_buff << endl;

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
	myReplace(val, CLOSE_DELIM, "\\}");
	output.append(val);
	output.append(CLOSE_DELIM);
	return output;
}

string deserialize_string(string str){
	myReplace(str, "\\}", "}");
	return str.substr(8, str.length() - (1 + 8));
}

void deserialize_void(string str){
  if(strcmp(str.c_str(), "Done") == 0){
	  cerr << "got a bad void value, exiting" << endl;
	  exit(1);
	}
}

