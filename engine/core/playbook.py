import sys, getopt, yaml, textwrap, os, subprocess

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
        print('================= PARAMETERS =================')
        print('The input file is '+inputfile)
        print('The output file is '+outputfile)
        parse_playbook(inputfile)
        generate_pythonfile(outputfile)
    
def parse_playbook(inputfile):
    with open(inputfile) as f:
        global x
        x = yaml.safe_load(f)
        print('%-50s' % 'Parsing playbook ... ', '[OK]')

def generate_pythonfile(outputfile):
    code=""
    timeout = 30 # second
    # sys.path.append('../')
    # import PocVerification.engine
    name = x[0]
    serial = 0
    handler_func = {}

    h_vars_area = ""
    h_function_area = ""
    # h_call_area = ""
    handlers = name.get("handlers")
    if handlers is None:
        handlers = {}
    for handler in handlers:
        serial = serial + 1
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

        decorator_timeout = ''
        if 'timeout' in handler:
            if handler.get("timeout") is not None:
                msg = ''
                if str(handler.get("timeout")) == 'timeout_continue':
                    msg = 'Skip '+list(handler.keys())[1]+' and continue running'
                else:
                    msg = 'Quit from '+list(handler.keys())[1]
                decorator_timeout = '@set_timeout('+str(timeout)+', \''+msg+'\', '+handler.get("timeout")+')\n'
            else: 
                decorator_timeout = ''

        function_comments = "# "+handler.get("name")
        function_name = "def "+ list(handler.keys())[1]+str(serial)+"("+params[:-2]+"):\n    print('%-50s' % 'NOTIFIED: ["+handler.get("name")+"]', '[OK]')\n"
     
        function_when = ''
        if 'when' in handler:
            if handler.get("when") is not None:
                function_when = "if "+ handler.get("when")+":\n"
                handler_func[handler.get("name")] = function_when+"".ljust(4, ' ')+list(handler.keys())[1]+str(serial)+"("+param_values[:-2]+")"
            else:
                handler_func[handler.get("name")] = list(handler.keys())[1]+str(serial)+"("+param_values[:-2]+")"
        else:
            handler_func[handler.get("name")] = list(handler.keys())[1]+str(serial)+"("+param_values[:-2]+")"
 
        if 'register' in handler:
            var = handler.get("register")
            function_body = "global "+str(var)+"\n"+str(var)+" = engine."+list(handler.keys())[1]+"("+params[0:-2:1]+")"
        else:   
            function_body = "engine."+list(handler.keys())[1]+"("+params[0:-2:1]+")"

        function_body = textwrap.indent(function_body, "".ljust(4, ' '))
        function_name += function_body
        h_function_area += function_comments+"\n"+decorator_timeout+""+str(function_name)+"" +"\n\n"
        params = ""


    t_import_area = "import sys\nfrom timeout_handle import set_timeout, timeout_quit, timeout_continue\nsys.path.append('../')\nimport hacks.facade\n\n\n"
    t_hook_area = "def __init__(self):\n    print(\"__init__\")\n\nengine = hacks.facade.Facade()\n\n"
    t_main_area = "if __name__ == '__main__':\n    print('')\n"
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
                if param_value in t_vars_area:
                   param_values += ""+param_value+", "
                else:
                    param_values += "\'"+param_value+"\', "
            else:
                param_values += str(param_value)+", "

        decorator_timeout = ''
        if 'timeout' in task:
            if task.get("timeout") is not None:
                msg = ''
                if str(task.get("timeout")) == 'timeout_continue':
                    msg = 'Skip '+list(task.keys())[1]+' and continue running'
                else:
                    msg = 'Quit from '+list(task.keys())[1]
                decorator_timeout = '@set_timeout('+str(timeout)+', \''+msg+'\', '+task.get("timeout")+')\n'
            else: 
                decorator_timeout = ''

        function_when = ''
        if 'when' in task:
            if task.get("when") is not None:
                function_when = "if "+ task.get("when")+":\n"
                t_call_area += "".ljust(4, ' ')+function_when+"".ljust(8, ' ')+list(task.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"
            else:
                t_call_area += "".ljust(4, ' ')+list(task.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"
        else:
            t_call_area += "".ljust(4, ' ')+list(task.keys())[1]+str(serial)+"("+param_values[:-2]+")\n"

        function_notify = ''
        if 'notify' in task:
            if task.get("notify") is not None:
                notify_list = task.get("notify")
                for call_method in notify_list:
                    if call_method in handler_func:
                        function_notify += handler_func.get(call_method)+"\n"
            else:
                function_notify += ''
             
        function_comments = "# "+task.get("name")
        function_name = "def "+ list(task.keys())[1]+str(serial)+"("+params[:-2]+"):\n    print('%-50s' % 'TASK: ["+task.get("name")+"]', '[OK]')\n"
        
        if 'register' in task:
            var = task.get("register")
            function_body = "global "+str(var)+"\n"+str(var)+" = engine."+list(task.keys())[1]+"("+params[0:-2:1]+")\n"
        else:   
            function_body = "engine."+list(task.keys())[1]+"("+params[0:-2:1]+")\n"
        
        function_body += function_notify

        function_body = textwrap.indent(function_body, "".ljust(4, ' '))
        function_name += function_body
        t_function_area += function_comments+"\n"+decorator_timeout+""+str(function_name)+"" +"\n\n"
        params = ""
 
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
    # Create new file
    py_create(code, outputfile)
    
    print('%-50s' % 'Generating python ... ', '[OK]')
    # os.system("python3 temp.py")
    # ret = subprocess.getoutput('python3 temp.py')
    subprocess.run(['python3', 'temp.py']) # official recommendation

def py_create(code, output):
    f= open(output,"w+")
    f.write(code)
    f.close() 
 
def py_delete(path):
    os.remove(path)

if __name__ == "__main__":
    main(sys.argv[1:])
    
    