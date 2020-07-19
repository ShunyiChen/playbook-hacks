import sys, getopt, yaml, textwrap, os

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("usage: playbook.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("usage: playbook.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    if inputfile == '' or outputfile == '' :
        print("usage: playbook.py -i <inputfile> -o <outputfile>")
    else:
        print('The input file is '+inputfile)
        print('The output file is '+outputfile)
        parse_playbook(inputfile)
        generate_pythonfile(outputfile)
    

def parse_playbook(inputfile):
    with open(inputfile) as f:
        global x
        x = yaml.safe_load(f)
        print('%-50s' % 'Parsing playbook file ... ', '[OK]')

def generate_pythonfile(outputfile):
    code=""

    # sys.path.append('../')
    # import PocVerification.engine
    name = x[0]
    serial = 0
    handler_func = {}

    h_vars_area = ""
    h_function_area = ""
    h_call_area = ""
    handlers = name.get("handlers")
    if handlers is None:
        handlers = {}
    for handler in handlers:
        if 'register' in handler:
            var = handler.get("register")
            if str(var) in h_vars_area:
                h_vars_area += ''
            else: 
                h_vars_area += str(var) + " = ''\n"

        function_args = list(handler.values())[1]
        
        if function_args is not None:
            args_keys = list(function_args.keys())
            args_values = list(function_args.values())
        else: # non-parameter constructor
            args_keys = []
            args_values = []
        params = ""
        param_values = ""
        for param_name in args_keys:
            params += param_name+", "

        for param_value in args_values:
            if type(param_value) is str:
                param_values += "\'"+param_value+"\', "
            else:
                param_values += str(param_value)+", "

        function_when = ''
        if handler.get("when") is not None:
            function_when = "if "+ handler.get("when")+":\n"
            h_call_area += "".ljust(4, ' ')+function_when+"".ljust(8, ' ')+list(handler.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"
        else:
            h_call_area += "".ljust(4, ' ')+list(handler.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"

        function_comments = "# "+handler.get("name")
        function_name = "def "+ list(handler.keys())[1]+str(serial)+"("+params[:-2]+"):\n    print(\"Running handler: "+handler.get("name")+"\")\n"

        
        handler_func[handler.get("name")] = list(handler.keys())[1]+str(serial)+"("+param_values[:-2]+")"
        # print(handler_func.get(handler.get("name"))+"---------------------")

        if 'register' in handler:
            var = handler.get("register")
            function_body = str(var)+" = ssh_hack."+list(handler.keys())[1]+"("+params[0:-2:1]+")"
        else:   
            function_body = "ssh_hack."+list(handler.keys())[1]+"("+params[0:-2:1]+")"

        function_body = textwrap.indent(function_body, "".ljust(4, ' '))
        function_name += function_body
        h_function_area += function_comments+"\n"+str(function_name)+"" +"\n\n"
        params = ""


    t_import_area = "import sys\nsys.path.append('../')\nimport hacks.ssh_hack.SSH_Hack\n\n\n"
    t_hook_area = "def __init__(self):\n    print(\"__init__\")\n\nssh_hack = hacks.ssh_hack.SSH_Hack('10.22.2.2', 'ad', 'ad@Admn!23!23')\n\n"
    t_main_area = "if __name__ == '__main__':\n    print('================= Running procedure =================')\n"
    t_vars_area = ""
    t_function_area = ""
    t_call_area = ""
    # name = print(x[0])
    # print(x[0].get("tasks"))
    # print(type(x[0].get("tasks")))
    tasks = name.get("tasks")
    
    for task in tasks: 
        serial = serial + 1
        if 'register' in task:
            var = task.get("register")
            if str(var) in t_vars_area:
                t_vars_area += ''
            else: 
                t_vars_area += str(var) + " = ''\n"
        function_args = list(task.values())[1]
        
        if function_args is not None:
            args_keys = list(function_args.keys())
            args_values = list(function_args.values())
        else: # non-parameter constructor
            args_keys = []
            args_values = []
        params = ""
        param_values = ""
        for param_name in args_keys:
            params += param_name+", "

        for param_value in args_values:
            if type(param_value) is str:
                param_values += "\'"+param_value+"\', "
            else:
                param_values += str(param_value)+", "

        function_when = ''
        if task.get("when") is not None:
            function_when = "if "+ task.get("when")+":\n"
            t_call_area += "".ljust(4, ' ')+function_when+"".ljust(8, ' ')+list(task.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"
        else:
            t_call_area += "".ljust(4, ' ')+list(task.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"

        function_notify = ''
        if task.get("notify") is not None:
            notify_list = task.get("notify")
            for call_method in notify_list:
                function_notify += handler_func.get(call_method)+"\n"
        else:
            function_notify += ''
             
        function_comments = "# "+task.get("name")
        function_name = "def "+ list(task.keys())[1]+str(serial)+"("+params[:-2]+"):\n    print(\"Running task: "+task.get("name")+"\")\n"
        if 'register' in task:
            var = task.get("register")
            function_body = str(var)+" = ssh_hack."+list(task.keys())[1]+"("+params[0:-2:1]+")\n"
        else:   
            function_body = "ssh_hack."+list(task.keys())[1]+"("+params[0:-2:1]+")\n"
        
        function_body += function_notify

  
        function_body = textwrap.indent(function_body, "".ljust(4, ' '))
        function_name += function_body
        t_function_area += function_comments+"\n"+str(function_name)+"" +"\n\n"
        params = ""
 
    t_call_area += "    print('%-50s' % 'Run Success!', '[OK]')\n\n"
    
    t_main_area += h_call_area
    t_main_area += t_call_area
    code += t_import_area
    code += h_vars_area
    code += t_vars_area
    code += t_hook_area
    code += h_function_area
    code += t_function_area
    code += t_main_area
    # t_main_area = textwrap.indent(t_main_area, "".ljust(4, ' '))
    # t_main_area = t_main_area[4:]
    
    py_create(code, outputfile)
    
    # print(t_main_area)
    print('%-50s' % 'Creating python file ... ', '[OK]')
    os.system("python3 temp.py")



def py_create(code, output):
    f= open(output,"w+")
    f.write(code)
    f.close() 
 
def py_delete(path):
    os.remove(path)

if __name__ == "__main__":
    main(sys.argv[1:])
    
    