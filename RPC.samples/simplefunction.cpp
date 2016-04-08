// --------------------------------------------------------------
//
//                        simplefunction.cpp
//
//        Author: Noah Mendelsohn         
//   
//
//        Trivial implementations of the routines declared
//        in simplefunction.idl. These are for testing: they
//        just print messages.
//
//       Copyright: 2012 Noah Mendelsohn
//     
// --------------------------------------------------------------

// IMPORTANT! WE INCLUDE THE IDL FILE AS IT DEFINES THE INTERFACES
// TO THE FUNCTIONS WE'RE IMPLEMENTING. THIS MAKES SURE THE
// CODE HERE ACTUALLY MATCHES THE REMOTED INTERFACE

#include "simplefunction.idl"

#include <cstdio>
#include <ctime>
#include <iostream>
#include "c150debug.h"

using namespace C150NETWORK;  // for all the comp150 utilities 


void func1() {
  printf("func1() invoked\n");
  c150debug->printf(C150RPCDEBUG,"simplefunction.cpp: func1() invoked");
}

void func2() {
  printf("func2() invoked\n");				  
  c150debug->printf(C150RPCDEBUG,"simplefunction.cpp: func2() invoked");
}

void func3() {
  printf("func3() invoked\n");
  c150debug->printf(C150RPCDEBUG,"simplefunction.cpp: func3() invoked");
}

int cur_time(){
	std::time_t t = std::time(0);
	return (int)t;
}

bool is_prime(int val){
	for(int i = 2 ; i < val; i++){
		if (val % i == 0){
			return false;
		}
	}
	return true;
}

