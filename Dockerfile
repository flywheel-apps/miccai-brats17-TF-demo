# flywheel/miccai-brats17-demo
# Creates docker container that runs the "Brain tumor segmentation for MICCAI 2017 BraTS challenge" from https://github.com/taigw/brats17

# Use Latest Python 3.6 docker image
# niftynet==0.5.0 depends on tensorflow==1.12.2 which is available in python3.6 (and python 3.5).
FROM python:3.6

MAINTAINER Flywheel <support@flywheel.io>

# Install packages
RUN apt-get update \
    && apt-get install -y \
    bsdtar \
    zip \
    unzip \
    gzip 

# Add the source code for the tumor segmentation models
RUN git clone https://github.com/taigw/brats17.git /opt/brats17/

# Replace an obsolete tensorflow library import with an updated one
# tensorflow.contrib.data -> tensorflow.data
RUN perl -p -i -e 's/tensorflow\.contrib\.data/tensorflow\.data/g' /opt/brats17/*.py

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Install dependencies for tiagw/brats17
COPY requirements.txt $FLYWHEEL/requirements.txt
RUN pip install -r $FLYWHEEL/requirements.txt

# Save docker environ
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'

# Copy custom tiagw/brats17 configuration file to the $FLYWHEEL directory
# "test_names.txt" will be created on the fly from the subject name provided by the flywheel configuration
COPY test_all_class.txt ${FLYWHEEL}/
COPY manifest.json ${FLYWHEEL}/
COPY run.py ${FLYWHEEL}/
COPY utils ${FLYWHEEL}/utils

# Configure entrypoint
RUN chmod a+x ${FLYWHEEL}/run.py
ENTRYPOINT ["${FLYWHEEL}/run.py"]