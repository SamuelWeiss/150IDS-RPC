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


// string serialize_bool(bool val){
// 	string output;
// 	output.append(OPEN_DELIM);
// 	output.append("bool");
// 	output.append(VAR_START);
// 	if(val){
// 		output.append("T");
// 	} else {
// 		output.append("F");
// 	}
// 	output.append(CLOSE_DELIM);
// 	return output;
// }


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


// string serialize_char(char val){
// 	string output;
// 	output.append(OPEN_DELIM);
// 	output.append("char");
// 	output.append(VAR_START);

// 	if(val == CLOSE_DELIM[0]){
// 		output.append("\\");
// 	}
// 	output += val;
// 	output.append(CLOSE_DELIM);
// 	return output;
// }


	//terminating cvalue for size_array is -99
// string serialize_array(void* val, int type_indicator, int* size_array){
// 	string output;
// 	output.append(OPEN_DELIM);
// 	output.append("arr");
// 	output.append(VAR_START);
// 	output.append(size_array[0])
// 	if(size_array[1] != -99){
// 		void** ptr = (void**) val;
// 		for(int i = 0; i < size_array[0]; i++){
// 			output.append(serialize_array((void*)ptr[i], type_indicator, &size_array[1]));
// 		}
// 	} else if(type_indicator == INT){
// 		int* ptr = (int*) val;
// 		for(int i = 0; i < size_array[0]; i++){
// 			output.append(serialize_int(ptr[i]));
// 		}
// 	} else 	if(type_indicator == FLOAT){
// 		float* ptr = (float*) val;
// 		for(int i = 0; i < size_array[0]; i++){
// 			output.append(serialize_float(ptr[i]));
// 		}

// 	} else 	if(type_indicator == BOOL){
// 		bool* ptr = (bool*) val;
// 		for(int i = 0; i < size_array[0]; i++){
// 			output.append(serialize_bool(ptr[i]));
// 		}

// 	} else 	if(type_indicator == STRING){
// 		string* ptr = (string*) val;
// 		for(int i = 0; i < size_array[0]; i++){
// 			output.append(serialize_string(ptr[i]));
// 		}
// 	} else {
// 		char* ptr = (char*) val;
// 		for(int i = 0; i < size_array[0]; i++){
// 			output.append(serialize_char(ptr[i]));
// 		}
// 	}
// 	output.append(CLOSE_DELIM);
// 	return output;
	
// }

int main(int argc, char* argv[]){
	cout << serialize_int(42);
	cout << serialize_float(3.3333);
	cout << serialize_bool(true);
	cout << serialize_bool(false);
	cout << serialize_string("Somewhere over the rainbow");
	cout << serialize_string("Here is a thing: {int:42}");
	int array[8] = {1,2,3,4,5,6,7,8};
	int size_array[2] = {8,-99};
	cout << serialize_array((void*)array, INT, size_array);
	int* array2[3] = {array,array,array};
	int new_size_array[3] = {3,8,-99};
	cout << serialize_array((void*)array2, INT, new_size_array);
}








