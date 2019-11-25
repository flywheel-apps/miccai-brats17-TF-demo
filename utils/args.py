import os, os.path as op
import subprocess as sp
import shutil

def build(context):
    pass

def validate(context):
    """
    Input: gear context with parameters in context.custom_dict['params']
    Attempts to correct any violations
    Logs warning on what may cause problems
    """
    # "context.config" must be invoked to populate the context object.
    config = context.config
    inputs = context._invocation['inputs']
    required_files = ['t1','t1ce','t2','flair']
    missing = []
    for fl in required_files:
        if not fl in inputs.keys():
            missing.append(fl)
    
    if len(missing)>0:
        raise Exception('The following file(s) are required: {}'.format(missing))

def exec_command(context,command,shell=False):
    environ = context.custom_dict['environ']
    context.log.info('Executing command: \n' + ' '.join(command)+'\n\n')
    if not context.custom_dict['dry-run']:
        # The 'shell' parameter is needed for bash redirects
        if shell:
            command = ' '.join(command)
        result = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE,
                        universal_newlines=True, env=environ, shell=shell)

        stdout, stderr = result.communicate()
        context.log.info(result.returncode)
        context.log.info(stdout)

        if result.returncode != 0:
            context.log.error('The command:\n ' +
                              ' '.join(command) +
                              '\nfailed.')
            raise Exception(stderr)

def execute(context):
    FLYWHEEL_BASE = '/flywheel/v0/'
    # Setup the directory structure expected by brats17/test.py for a 
    # single subject (e.g. /flywheel/v0/input/{subject}/{fl})
    
    subject = context.config["Subject"]

    os.makedirs(FLYWHEEL_BASE+'/input/'+subject, exist_ok=True)

    inputs = context._invocation['inputs']
    # Make symbolic links between the flywheel file structure and the file 
    # structure expected by brats/test.py
    for fl in inputs:
        if "location" in inputs[fl]:
            path=inputs[fl]["location"]["path"]
            command = ["ln","-s",path,FLYWHEEL_BASE+"/input/"+subject+"/"]
            exec_command(context,command) 

    # Create the test_names.txt file needed by taigw/brats2017 code...
    # with the subject that is downloaded. 
    f = open('test_names.txt','w')
    f.write(subject)
    f.close()

    # change to the model execution directory
    os.chdir("/opt/brats17/")

    command = ["python","test.py","/flywheel/v0/test_all_class.txt"]
    exec_command(context,command)    