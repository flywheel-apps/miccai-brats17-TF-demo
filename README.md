# flywheel/miccai-brats17-demo

[Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) that runs the [2nd place winner](https://github.com/taigw/brats17) of the [MICCAI 2017 BraTS (Brain Tumor Segmentation) Challenge](http://braintumorsegmentation.org/). We wrap their [TensorFlow](https://www.tensorflow.org/) and [NiftyNet](https://niftynet.io/) based [docker image](https://hub.docker.com/r/brats/brats_dc) in the Flywheel framework to enable ease of use.

## Important notes

* This uses the data produced for the 2017 BraTS challenge. These data must be acquired from the Center for [Biomedical Image Computing and Analytics](https://ipp.cbica.upenn.edu/) at the University of Pennsylvania. Attribution for use is required.
* User data is prepared by brain-extracting the required coregistered modalities. See the [BraTS Data Description Overview](https://www.med.upenn.edu/cbica/brats2019/data.html) for more information.

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

## GPU Execution
For GPU execution, please see the development branch dedicated to exploring this functionality.
