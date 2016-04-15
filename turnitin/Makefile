# Makefile for COMP 150IDS RPC Samples
#
#    Sam Weiss and Rachel Hogue
#
#
# Useful targets, assuming you have some idl file named xxxx.idl:
#
#    make xxx.proxy.o
#    make xxx.stub.o
#    make xxxserver 
#    make xxxclient
#
#

# Do all C++ compies with g++
CPP = g++

# change following line if your rpgenerate is not in current directory
#RPCGEN = ./rpcgenerate
RPCGEN = rpcgenerate.py

# Where the COMP 150 shared utilities live, including c150ids.a and userports.csv
# Note that environment variable COMP150IDS must be set for this to work!

C150LIB = $(COMP150IDS)/files/c150Utils/
C150AR = $(C150LIB)c150ids.a

# RPC framework is shared archive
C150IDSRPC = $(COMP150IDS)/files/RPC.framework/
C150IDSRPCAR = $(C150IDSRPC)c150idsrpc.a

CPPFLAGS = -g -Wall -Werror -I$(C150IDSRPC) -I$(C150LIB)
# CPPFLAGS = -g -Wall -Werror  -I$(C150LIB)


LDFLAGS = 
INCLUDES = $(C150LIB)c150streamsocket.h $(C150LIB)c150network.h $(C150LIB)c150exceptions.h $(C150LIB)c150debug.h $(C150LIB)c150utility.h $(C150LIB)c150grading.h $(C150IDSRPC)IDLToken.h $(C150IDSRPC)tokenizeddeclarations.h  $(C150IDSRPC)tokenizeddeclaration.h $(C150IDSRPC)declarations.h $(C150IDSRPC)declaration.h $(C150IDSRPC)functiondeclaration.h $(C150IDSRPC)typedeclaration.h $(C150IDSRPC)arg_or_member_declaration.h rpcproxyhelper.h rpcstubhelper.h simplefunction.idl arithmetic.idl floatarithmetic.idl 

########################################################################
#
#          General rules for building any client and server
#
#     Given any xxx.idl, these rules will build xxxclient and xxxserver
#
########################################################################

# Compile / link any client executable: 
%client: %.o %.proxy.o rpcserver.o rpcproxyhelper.o %client.o %_data_packing.o
	$(CPP) -o $@ $@.o rpcproxyhelper.o $*.proxy.o $*_data_packing.o $(C150AR) $(C150IDSRPCAR) 

# Compile / link any server executable:
%server: %.o %.stub.o rpcserver.o rpcstubhelper.o %.stub.o %_data_packing.o
	$(CPP) -o $@ rpcserver.o $*.stub.o $*.o rpcstubhelper.o $*_data_packing.o $(C150AR) $(C150IDSRPCAR) 



########################################################################
#
#          Generate C++ source from IDL files
#
########################################################################

%.proxy.cpp %.stub.cpp:%.idl $(RPCGEN)
	python $(RPCGEN) $<

########################################################################
#
#                   idldeclarationtst
#
#     When you write rpcgenerate, you'll want to use the idl
#     parser that's provided for you. This is a demo program
#     you can read and try to see how the parser works.
#
#     NOTE: This program became more or less obsolete in 2016.
#     Prior to then, all  RPC generators were written in C++,
#     there was no idl_to_json program, and this was the main example program
#     students used to learn the IDL parser. It is still maintained
#     in case anyone finds it useful.
#
########################################################################

idldeclarationtst: idldeclarationtst.o $(C150AR) $(C150IDSRPCAR)  $(INCLUDES)
	$(CPP) -o idldeclarationtst idldeclarationtst.o $(C150AR) $(C150IDSRPCAR) 

########################################################################
#
#                   idl_to_json
#
#     This program servers two purposes:
#
#     1) If you are writing your rpc generator in Python or Ruby,
#        this utility will convert .idl files to JSON for you.
#     2) Especially if you are writing rpcgenerate in C++, the
#        source code of idl_to_json.cpp is the best way to learn use
#        the provided .idl parser.
#
########################################################################

idl_to_json: idl_to_json.o $(C150AR) $(C150IDSRPCAR)  $(INCLUDES)
	$(CPP) -o idl_to_json idl_to_json.o $(C150AR) $(C150IDSRPCAR) 

########################################################################
#
#          Generate .json files from .idl files
#
#     This rule allows you to say:
#
#              make demo.json
#
#     if you already have demo.idl
#
########################################################################

%.json:%.idl idl_to_json
	     idl_to_json $< > $@

########################################################################
#
#                   Housekeeping
#
########################################################################


# make .o from .cpp

%.o:%.cpp  $(INCLUDES)
	$(CPP) -c  $(CPPFLAGS) $< 


