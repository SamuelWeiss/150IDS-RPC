
#include "testfunction.idl"

#include <cstdio>
#include <string>
#include <ctime>
#include <iostream>
#include "c150debug.h"
#include <math.h>

using namespace C150NETWORK;  // for all the comp150 utilities 

void myReplace(std::string& str, const std::string& oldStr, const std::string& newStr){
  size_t pos = 0;
  while((pos = str.find(oldStr, pos)) != std::string::npos){
     str.replace(pos, oldStr.length(), newStr);
     pos += newStr.length();
  }
}

float halve(int x){
	return (x / 2.0);
}

int pow(int x, int y){
	int temp = 1;
	for(int i = 0; i < y; i++){
		temp *= x;
	}
	return temp;
}

std::string replace( string base, string search, string replace){
	myReplace(base, search, replace);
	return base;
}
