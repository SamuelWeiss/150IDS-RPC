#include <string>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <sstream>

using namespace std;

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
  //
  // We've read the function name, call the stub for the right one
  // The stub will invoke the function and send response.
  //

  // generated code
  if(strcmp(name, "the function name") == 0){

  } else if
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

int main(int argc, char* argv[]){
	cout << get_name_from_message("{dummy-{int:42}}") << endl;
	cout << get_arguments_from_message("{dummy-{int:42}{float:42.42}}") << endl;
}