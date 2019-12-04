#!/usr/local/bin/python
import json
import logging
import os
import os.path as op
import sys
import time
import subprocess as sp
import flywheel

def get_custom_logger(log_name):
    """Create a custom logger
    
    :param log_name: Name of Logger
    :type log_name: string
    :return: a logger
    :rtype: logger
    """
    # Initialize Custom Logging
    # Timestamps with logging assist debugging algorithms
    # With long execution times
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
                fmt='%(levelname)s - %(name)-8s - %(asctime)s -  %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger = logging.getLogger(log_name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

def exec_command(context,command,shell=False):
    """Used to execute shell commands
    
    :param context: Gear Context
    :type context: GearContext 
    :param command: A list of commands for subprocess
    :type command: list
    :param shell: Redirects (e.g. >>) only work with shell, defaults to False
    :type shell: bool, optional
    :raises Exception: On non-zero exit, we return the stderr for the shell command
    """
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

def main():
    context = flywheel.GearContext()
    context.custom_dict={}
    # Create a 'dry run' flag for debugging
    context.custom_dict['dry-run'] = False

    context.log = get_custom_logger('[flywheel:taigw/brats17]')

    # grab environment for gear
    with open('/tmp/gear_environ.json', 'r') as f:
        environ = json.load(f)
    context.custom_dict['environ'] = environ

    # Report inputs and configuration
    context.log_config()

    try:
        # verify required inputs are present 
        inputs = context._invocation['inputs']
        required_files = ['t1','t1ce','t2','flair']
        missing = []
        for fl in required_files:
            if not fl in inputs.keys():
                missing.append(fl)

        if len(missing)>0:
            raise Exception('The following file(s) are required: {}'.format(missing))

        # execute algorithm on parameters
        # Setup the directory structure expected by brats17/test.py for a 
        # single subject (e.g. /flywheel/v0/work/{subject}/{fl})
        subject = context.config["Subject"]
<<<<<<< HEAD
        os.makedirs(op.join(context.work_dir,subject), exist_ok=True)
=======
        os.makedirs(op.join(context.work_dir,subject))
>>>>>>> josh-py-dev-w-gpu

        inputs = context._invocation['inputs']
        # Make symbolic links between the flywheel file structure and the file 
        # structure expected by brats/test.py
        for fl in inputs:
            if "location" in inputs[fl]:
                src = inputs[fl]["location"]["path"]
<<<<<<< HEAD
                dest = op.join(context.work_dir,subject,"/")
=======
                dest = op.join(context.work_dir,subject,inputs[fl]["location"]["name"])
>>>>>>> josh-py-dev-w-gpu
                os.symlink(src, dest) 

        # Create the test_names.txt file needed by taigw/brats2017 code...
        # with the subject that is downloaded. 
        f = open('test_names.txt','w')
        f.write(subject)
        f.close()

        # change to the model execution directory
        os.chdir("/usr/src/app/")
        command = ["python","test.py","/flywheel/v0/test_all_class.txt"]
        exec_command(context,command)

    except Exception as e:
        context.log.exception(e)
        context.log.error(
            'Cannot execute https://github.com/taigw/brats17 commands.'
        )
        os.sys.exit(1)

    
    # On successful completion, notify and exit gracefully
    context.log.info("Commands successfully executed!")
    os.sys.exit(0)

if __name__ == '__main__':
    main()