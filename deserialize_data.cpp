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

void myReplace(std::string& str, const std::string& oldStr, const std::string& newStr){
  size_t pos = 0;
  while((pos = str.find(oldStr, pos)) != std::string::npos){
     str.replace(pos, oldStr.length(), newStr);
     pos += newStr.length();
  }
}

string get_var_string(string str){
	//pulls out the first val and deletes it
	string output;
	for(int i = 0; i < str.length(); i++){
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
	for(int i = 0; i < str.length(); i++){
		if(str.at(i) == '}'){
			if(str.at(i-1) == '\\'){
				continue;
			} else {
				return substr(str(i+1, str.length() - (i + 2)));
			}
		}
	}
}

int deserialize_int(string str){
	string conv_buff = str.substr(5, str.length() - (1 + 5));
	return atoi(conv_buff.c_str());
}

bool deserialize_bool(string str){
	return str.at(6) == 'T';
}

float deserialize_float(string str){
	string conv_buff = str.substr(7, str.length() - (1 + 7));
	return atof(conv_buff.c_str());
}

string deserialize_string(string str){
	myReplace(str, "\\}", "}");
	cout << str << endl;
	int temp =  str.length();
	cout << temp << endl;
	return str.substr(8, str.length() - (1 + 8));
}

void* deserialize_array(string str){
	//chopping off the head

	//figure out type

	//loop through and deserialize by type
}


int main(int argc, char* argv[]){
	string str = "{string:This is a test \\} of things}{int:42}";
	string str2 = get_var_string(str);
	cout << str2 << endl;
	str = chop_string(str, str2.length());
	cout << str << endl;
	cout << deserialize_int("{int:42}")<< endl;
	cout << deserialize_string(str2)<< endl;
}



