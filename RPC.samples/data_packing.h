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
