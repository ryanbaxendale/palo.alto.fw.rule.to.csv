from os import curdir, sep, getcwd
import sys, getopt

def get_start_of(input, searchfor):
    if isinstance(input, str):
        input = input.splitlines()
    for index, item in enumerate(input):
        if searchfor in item:
            return index

def list_to_str(input):
    output = ""
    for line in input:
        output += line
    return output

def get_sub_from_line(num, data):
    startline = num
    i = 0
    subs = 1
    track = False
    item = []
    while i<len(data):
        if track:
            item.append( data[i] )
            if " {" in data[i]:
                subs += 1
            if "}" in data[i]:
                subs -= 1
                if subs == 0:
                    track = False
                    break
        if i == startline:
            item = [data[i]]
            track = True
        i += 1
    return item

def get_item_new(searchfor, data):
    startline = get_start_of(data, searchfor)
    i = 0
    subs = 1
    track = False
    item = []
    while i<len(data):
        if track:
            item.append( data[i] )
            if " {" in data[i]:
                subs += 1
            if "}" in data[i]:
                subs -= 1
                if subs == 0:
                    track = False
                    break
        if i == startline:
            item = [data[i]]
            track = True
        i += 1
    return item

def get_subs(data):
    i = 0
    subs = 1
    track = False
    item = []
    while i<len(data):
        #print track,"data[i]",data[i].rstrip()
        if track:
            if " {" in data[i]:
                subs += 1
            if "}" in data[i]:
                subs -= 1
                if subs == 0:
                    track = False
                    subs = 1
        if " {" in data[i] and not track:
            track = True
            #print i
            item.append(i)
        i += 1
    return item

def process(f, out):
	content = f.readlines()

	security_section = get_item_new( "security {", content)
	rules_section = get_item_new("rules {", security_section )

	out.write("name,from,to,action,description,source,destination,source_user,category,application,service,hip_profiles,log_start,log_end,negate_source,negate_destination" + '\n')

	print "Output rule: ",

	del rules_section[0]
	for num in get_subs(rules_section):
	    try:
		rule = list_to_str( get_sub_from_line(num, rules_section) ).rstrip().lstrip()
		rule_option = list_to_str( get_item_new("option {", get_sub_from_line(num, rules_section) )).rstrip().lstrip()
		rule_profile_setting = list_to_str( get_item_new("profile-setting {", get_sub_from_line(num, rules_section) )).rstrip().lstrip()
		rule_profile_setting_profiles = list_to_str( get_item_new("profiles {", get_sub_from_line(num, rules_section) )).rstrip().lstrip()
		rule_name = ""
		rule_from = ""
		rule_to = ""
		rule_description = ""
		rule_source = ""
		rule_destination = ""
		rule_source_user = ""
		rule_category = ""
		rule_application = ""
		rule_service = ""
		rule_hip_profiles = ""
		rule_log_start = ""
		rule_log_end = ""
		rule_negate_source = ""
		rule_negate_destination = ""
		rule_action = ""
		
		rule_name = rule[0:rule.index(" {")]
		if "from " in rule:
		    rule_from = rule[rule.index("from ")+5:rule.index(";", rule.index("from "))]
		if "to " in rule:
		    rule_to = rule[rule.index("to ")+3:rule.index(";", rule.index("to "))]
		if "source " in rule:
		    rule_source = rule[rule.index("source ")+7:rule.index(";", rule.index("source "))]
		if "destination " in rule:
		    rule_destination = rule[rule.index("destination ")+12:rule.index(";", rule.index("destination "))]
		if "source-user " in rule:
		    rule_source_user = rule[rule.index("source-user ")+12:rule.index(";", rule.index("source-user "))]
		if "category " in rule:
		    rule_category = rule[rule.index("category ")+9:rule.index(";", rule.index("category "))]
		if "application " in rule:
		    rule_application = rule[rule.index("application ")+12:rule.index(";", rule.index("application "))]
		if "service " in rule:
		    rule_service = rule[rule.index("service ")+8:rule.index(";", rule.index("service "))]
		if "hip-profiles " in rule:
		    rule_hip_profiles = rule[rule.index("hip-profiles ")+13:rule.index(";", rule.index("hip-profiles "))]
		if "log-start " in rule:
		    rule_log_start = rule[rule.index("log-start ")+10:rule.index(";", rule.index("log-start "))]
		if "log-end " in rule:
		    rule_log_end = rule[rule.index("log-end ")+8:rule.index(";", rule.index("log-end "))]
		if "description " in rule:
		    rule_description = rule[rule.index("description ")+12:rule.index(";", rule.index("description "))]
		if "negate-source " in rule:
		    rule_negate_source = rule[rule.index("negate-source ")+14:rule.index(";", rule.index("negate-source "))]
		if "negate-destination " in rule:
		    rule_negate_destination = rule[rule.index("negate-destination ")+19:rule.index(";", rule.index("negate-destination "))]
		if "action " in rule:
		    rule_action = rule[rule.index("action ")+7:rule.index(";", rule.index("action "))]

		out.write( \
		    rule_name \
		    + "," + \
		    rule_from \
		    + "," + \
		    rule_to \
		    + "," + \
		    rule_action \
		    + "," + \
		    rule_description \
		    + "," + \
		    rule_source \
		    + "," + \
		    rule_destination \
		    + "," + \
		    rule_source_user \
		    + "," + \
		    rule_category \
		    + "," + \
		    rule_application \
		    + "," + \
		    rule_service \
		    + "," + \
		    rule_hip_profiles \
		    + "," + \
		    rule_log_start \
		    + "," + \
		    rule_log_end \
		    + "," + \
		    rule_negate_source \
		    + "," + \
		    rule_negate_destination \
		    + '\n')

		print rule_name,
		
		#print rule_name,":",rule_from,"--->",rule_to
		#print "action:",rule_action
		#print "description:",rule_description
		#print "source:",rule_source
		#print "destination:",rule_destination
		#print "source-user:",rule_source_user
		#print "category:",rule_category
		#print "application:",rule_application
		#print "service:",rule_service
		#print "hip-profiles:",rule_hip_profiles
		#print "log-start:",rule_log_start
		#print "log-end:",rule_log_end
		#print "negate-source:",rule_negate_source
		#print "negate-destination:",rule_negate_destination
		
	    except Exception as e:
		print e

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
	opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print sys.argv[0], '-i <extracted-fw-config-in-txt> -o <csv-output-file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0], '-i <extracted-fw-config-in-txt> -o <csv-output-file>'
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
    print 'Reading in firewall config file [ ', inputfile, ' ]'
    f = open(getcwd() + sep + inputfile, 'r')
    print 'CSV Output to file [ ', outputfile, ' ]'
    out = open(getcwd() + sep + outputfile, "a")
    process(f, out)

if __name__ == "__main__":
    main(sys.argv[1:])

