# flywheel/miccai-brats17-demo

[Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) that runs the [2nd place winner](https://github.com/taigw/brats17) of the [MICCAI 2017 BraTS (Brain Tumor Segmentation) Challenge](http://braintumorsegmentation.org/).

## Important notes

* This uses the data produced for the 2017 BraTS challenge. These data must be acquired from the Center for [Biomedical Image Computing and Analytics](https://ipp.cbica.upenn.edu/) at the University of Pennsylvania. Attribution for use is required.
* Data may be prepared by brain-extracting the coregistered required modalities below in the required resolution (1mm isotropic 240x240x155 centered at [0,239,0]).

## Required inputs

1. The name of the Subject (e.g. Brats17_TCIA_607_1) placed in the "Subject" field of the configuration tab.
2. The <code>flair</code> image of the session.
3. The <code>t1</code>-weighted image of the session.
4. The <code>t1ce</code> (Contrast Enhanced) image of the session.
5. The <code>t2</code>-weighted image of the session.

## Outputs

* \<subject\>\_nii.gz</code>: The gzipped nifti image of the algorithm-segmented tumor.
* test\_time.txt: A text file containing the time, in seconds, that the algorithm took to complete.

## Extra Files

* <code>test_all_class.txt</code> is a MICCAI BraTS 2017 configuration file containing the flywheel gear locations for input and output files. All other files are produced locally.
* <code>requirements.txt</code> is a pip requirements file that is used to install code dependencies when the Dockerfile is built. 
* <code>requirements-gpu.txt</code> and <code>Dockerfile.gpu</code> are GPU-enabled versions of the original files. See GPU Excecution Below

## GPU Execution

Interactive docker (and podman) sessions of this gear have been tested in a GPU environment with significant speedup in inference time (30 seconds vs. 8 minutes) on an NVIDIA GTX 1080 Ti.  The only difference (thus far) in gear instantiation is the docker/podman build command (e.g. 'podman build -t <Tag> -f Dockerfile.gpu .'). Other changes to the manifest may be necessary to provision the appropriate cloud resources. 

Local execution must be done with sample data, a valid configuration file (config.json), and the following nvidia container runtime command:
``nvidia-docker run --rm <image id> run.py``

See Host and Container Requirements below:

### Host Requirements
1. NVIDIA Driver 384.81 minimum (410.48 worked. See [Driver Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/#binary-compatibility))

### Guest Requirements
1. Cuda: v9.0
2. CuDNN: 7.1.4.18
3. tensorflow-gpu: 1.12.2 (minimum 1.4.0. See requirements-gpu.txt)
4. NiftyNet: 0.5.0 (minimum 0.2.0. See requirements-gpu.txt)
5. Python 3.5 (Python 3.6 max version)

The above versions of Cuda, CuDNN, tensorflow, and NiftyNet are required to execute the pretrained models created by [Guotai Wang](https://github.com/taigw/brats17). To use later versions of these libraries, retraining of the models would be required.