#!/usr/local/bin/python
import json
import logging
import os
import os.path as op
import sys
import subprocess as sp
import flywheel
from utils.custom_logger import get_custom_logger, log_config
from utils import args

if __name__ == '__main__':
    context = flywheel.GearContext()
    context.custom_dict={}
    # Create a 'dry run' flag for debugging
    context.custom_dict['dry-run'] = False

    context.log = get_custom_logger('[flywheel:taigw/brats17]')

    # grab environment for gear
    with open('/tmp/gear_environ.json', 'r') as f:
        environ = json.load(f)
    context.custom_dict['environ'] = environ
    
    try:
        # Report inputs and configuration
        log_config(context)

        # build parameters needed...Nothing to build here
        # args.build(context)

        # validate parameters required
        args.validate(context)

        # execute algorithm on parameters
        args.execute(context)

        context.log.info("Commands successfully executed!")
        os.sys.exit(0)

    except Exception as e:
        context.log.error(e)
        context.log.error(
            'Cannot execute https://github.com/taigw/brats17 commands.'
        )
        os.sys.exit(1)

    finally:
        pass
