# Creates docker container that runs the "Brain tumor segmentation for MICCAI 2017 BraTS challenge" from https://github.com/taigw/brats17
# Host System Requirements:
#   	NVidia driver 384.81 or above to be installed (e.g. 410.48 works).
#
# Container Requirements: 
#  	cuda 9.0
#	Python3 (3.5 to 3.6)
#	libcudnn7 (7.1.4.18)
#	tensorflow==1.12.2
#	numpy==1.14.5
#	niftynet==0.5.0

FROM nvidia/cuda:9.0-devel-ubuntu16.04

MAINTAINER Flywheel <support@flywheel.io>

# The taigw/brats17 DNN models depend on the following version of cudnn
ENV CUDNN_VERSION 7.1.4.18 

# Install the apt requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn7=$CUDNN_VERSION-1+cuda9.0 \
            libcudnn7-dev=$CUDNN_VERSION-1+cuda9.0 \
            bsdtar \
            zip \
            unzip \
            gzip \
            git \
            python3.5 \
            python3-pip && \
    apt-mark hold libcudnn7 && \
    rm -rf /var/lib/apt/lists/*

# Make a symbolic link for python 
RUN ln -s /usr/bin/python3 /usr/local/bin/python

# Add the source code for the tumor segmentation models
# Replace an obsolete tensorflow library import with an updated one
RUN git clone https://github.com/taigw/brats17.git /tmp/brats17/ && \
    perl -p -i -e 's/tensorflow\.contrib\.data/tensorflow\.data/g' /tmp/brats17/*.py    

RUN pip install --upgrade pip && \
    pip install flywheel-sdk


# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Install dependencies for tiagw/brats17
COPY requirements-gpu.txt $FLYWHEEL/requirements.txt
RUN pip3 install --upgrade pip && \
   	pip3.5 install setuptools && \
    pip3.5 install -r $FLYWHEEL/requirements.txt && \
    rm -rf /root/.cache/pip 

# Copy custom tiagw/brats17 configuration file to the $FLYWHEEL directory
# "test_names.txt" will be created on the fly from the subject name provided by the flywheel configuration
<<<<<<< HEAD
COPY test_all_class.txt $FLYWHEEL/

COPY manifest.json $FLYWHEEL/
COPY run.py $FLYWHEEL/
COPY utils $FLYWHEEL/utils

# Save docker environ
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'
=======
COPY test_all_class.txt ${FLYWHEEL}/
COPY manifest.json ${FLYWHEEL}/
COPY run.py ${FLYWHEEL}/
>>>>>>> josh-py-dev-w-gpu

# Configure entrypoint
RUN chmod +x ./run.py
ENTRYPOINT ["/flywheel/v0/run.py"]
