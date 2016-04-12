import json
import subprocess
import re
import pdb


print "This is testing code"
print "type in the IDL file you'd like to try"
#file_name = raw_input("Name: " )
file_name = "lotsofstuff.idl"

json_as_text = subprocess.check_output(["./idl_to_json", file_name])
idl_contents = json.loads(json_as_text)
#print idl_contents
#pdb.set_trace()

functions = idl_contents["functions"]
types = idl_contents["types"]

def fix_names(str):
	return str.replace("[", "_").replace(']', "_")

def generate_serialize_headers(type_name, type_desc):
	if type_desc["type_of_type"] == "builtin":
		pass
	if type_desc["type_of_type"] == "array":
		fixed_type = fix_names(type_name)
		return "string serialize_" + fixed_type + "(" + type_name[2:] + " val);\n"
	if type_desc["type_of_type"] == "struct":
		fixed_type = fix_names(type_name)
		return "string serialize_" + fixed_type + "(" + fixed_type + " val);\n"





def generate_serialize(type_name, type_desc):
	# for i in type_desc:
	# 	print i
	# 	print type_desc[i]
	output = ""


	#case 1: simple builtins, just copy what we've written
	if type_desc["type_of_type"] == "builtin":
		#print "builtin: " + type_name
		pass

	#case 2: arrays, iterate over all elements and serialize them
	if type_desc["type_of_type"] == "array":
		tmp = fix_names(type_desc['member_type'])
		fixed_type = fix_names(type_name)
		tester = re.search('(?<=_)[0-9]+(?=_)', fixed_type)
		num_elem = tester.group(0)
		output =   "string serialize_" + fixed_type + "(" + type_name[2:] + " val){\n"
		output +=  "    string output;\n"
		output += ('    output.append("{' + fixed_type + ':");\n')
		output += ("    for(int i = 0; i < " + num_elem + "; i++){\n")
		output += ("        output.append(serialize_" + tmp + "(val[i]));\n")
		output += "    }\n"
		output += '     output.append("}");\n'
		output += "    return output;\n"
		output += "}\n"
		# print output
		return output

	#case 3: loop over all members and serialize them
	if type_desc["type_of_type"] == "struct":
		fixed_type = fix_names(type_name)
		output =  "string serialize_" + fixed_type + "(" + fixed_type + " val){\n"
		output += "    string output;\n"
		output += ('    output.append("{' + fixed_type + ':");\n')
		for i in type_desc["members"]:
			output += ("    output.append(serialize_" + fix_names(i["type"]) + "(val." + i["name"] + "));\n")
		output += '    output.append("}");\n'
		output += '    return output;\n'
		output += '}\n'
		# print output
		return output

def generate_deserialize(type_name, type_desc):
	if type_desc["type_of_type"] == "builtin":
		pass
	if type_desc["type_of_type"] == "array":
		output = ""
	if type_desc["type_of_type"] == "struct":
		pass


def fix_names(str):
	return str.replace("[", "_").replace(']', "_")

for i in types:
	# generate_serialize( i, types[i] )
	print generate_serialize_headers(i, types[i])