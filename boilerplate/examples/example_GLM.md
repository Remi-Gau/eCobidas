# boilerplate for fMRI GLM

taken from the [COBIDAS blog](https://cobidas.wordpress.com/2016/05/23/cobidas-easter-egg/)

Summaries for AFNI, Freesurfer, FSL, & SPM are based on versions AFNI_2011_12_21_1014, FreeSurfer 5.3, FSL 5.0.8 and SPM 12 revision 6470, respectively.


## AFNI

AFNI 1st level – 3dDeconvolve: Linear regression at each voxel, using ordinary least squares, drift fit with polynomial.

AFNI 1st level – 3dREMLfit: Linear regression at each voxel, using generalised least squares with a voxel-wise ARMA(1,1) autocorrelation model, drift fit with polynomial.

AFNI 2nd level – 3dTtest: Linear regression at each voxel, using ordinary least squares.

AFNI 2nd level – 3dMEMA: Linear mixed effects regression at each voxel, using generalized least squares with a local estimate of random effects variance.

AFNI 2nd level – 3dMVM: Multivariate ANOVA or ANCOVA at each voxel.

AFNI 2nd level – 3dLME: General linear mixed-effects modeling at each voxel, with separate specification of fixed and random variables.


## Freesurfer

Freesurfer 1st Level – selxavg3-sess: Linear regression at each surface element, using generalized least squares with a element-wise AR(1) autocorrelation model, drift fit with polynomial.

Freesurfer 2st Level – mri_glmfit: Linear regression at each surface element, using ordinary least squares.


## FSL

FSL 1st level: Linear regression at each voxel, using generalized least squares with a voxel-wise, temporally and spatially regularized autocorrelation model, drift fit with Gaussian-weighted running line smoother (100s FWHM).

FSL 2nd level – “OLS”: Linear regression at each voxel, using ordinary least squares.

FSL 2nd level – “FLAME1”: Linear mixed effects regression at each voxel, using generalized least squares with a local estimate of random effects variance.


## SPM

SPM 1st level: Linear regression at each voxel, using generalized least squares with a global approximate AR(1) autocorrelation model, drift fit with Discrete Cosine Transform basis (128s cut-off).

SPM 2nd level – no repeated measures: Linear regression at each voxel, using ordinary least squares.

SPM 2nd level – repeated measures: Linear regression at each voxel, using generalized least squares with a global repeated measures correlation model.
