# boilerplate for fMRI preprocessing

<!-- TOC -->
<!-- lint disable -->
- [boilerplate for fMRI preprocessing](#boilerplate-for-fmri-preprocessing)
  - [CPP SPM12 pipeline](#cpp-spm12-pipeline)
  - [fMRIprep](#fmriprep)
  - [SPM references](#spm-references)
    - [spm_realign](#spm_realign)
    - [spm_coreg](#spm_coreg)
    - [spm_normalize](#spm_normalize)
    - [spm_spm](#spm_spm)
<!-- lint enable -->
<!-- /TOC -->


## fMRIprep

Taken from this [page](https://fmriprep.org/en/stable/citing.html).

```
Results included in this manuscript come from preprocessing performed using
FMRIPREP version latest [1, 2, RRID:SCR_016216], a Nipype [3, 4,
RRID:SCR_002502] based tool. Each T1w (T1-weighted) volume was corrected for INU
(intensity non-uniformity) using N4BiasFieldCorrection v2.1.0 [5] and
skull-stripped using antsBrainExtraction.sh v2.1.0 (using the OASIS template).
Brain surfaces were reconstructed using recon-all from FreeSurfer v6.0.1 [6,
RRID:SCR_001847], and the brain mask estimated previously was refined with a
custom variation of the method to reconcile ANTs-derived and FreeSurfer-derived
segmentations of the cortical gray-matter of Mindboggle [21, RRID:SCR_002438].
Spatial normalization to the ICBM 152 Nonlinear Asymmetrical template version
2009c [7, RRID:SCR_008796] was performed through nonlinear registration with the
antsRegistration tool of ANTs v2.1.0 [8, RRID:SCR_004757], using brain-extracted
versions of both T1w volume and template. Brain tissue segmentation of
cerebrospinal fluid (CSF), white-matter (WM) and gray-matter (GM) was performed
on the brain-extracted T1w using fast [17] (FSL v5.0.9, RRID:SCR_002823).

Functional data was slice time corrected using 3dTshift from AFNI v16.2.07 [11,
RRID:SCR_005927] and motion corrected using mcflirt (FSL v5.0.9 [9]).
"Fieldmap-less" distortion correction was performed by co-registering the
functional image to the same-subject T1w image with intensity inverted [13,14]
constrained with an average fieldmap template [15], implemented with
antsRegistration (ANTs). This was followed by co-registration to the
corresponding T1w using boundary-based registration [16] with six degrees of
freedom, using bbregister (FreeSurfer v6.0.1). Motion correcting
transformations, field distortion correcting warp, BOLD-to-T1w transformation
and T1w-to-template (MNI) warp were concatenated and applied in a single step
using antsApplyTransforms (ANTs v2.1.0) using Lanczos interpolation.

Physiological noise regressors were extracted applying CompCor [18]. Principal
components were estimated for the two CompCor variants: temporal (tCompCor) and
anatomical (aCompCor). A mask to exclude signal with cortical origin was
obtained by eroding the brain mask, ensuring it only contained subcortical
structures. Six tCompCor components were then calculated including only the top
5% variable voxels within that subcortical mask. For aCompCor, six components
were calculated within the intersection of the subcortical mask and the union of
CSF and WM masks calculated in T1w space, after their projection to the native
space of each functional run. Frame-wise displacement [19] was calculated for
each functional run using the implementation of Nipype. ICA-based Automatic
Removal Of Motion Artifacts (AROMA) was used to generate aggressive noise
regressors as well as to create a variant of data that is non-aggressively
denoised [20].

Many internal operations of FMRIPREP use Nilearn [22, RRID:SCR_001362],
principally within the BOLD-processing workflow. For more details of the
pipeline see https://fmriprep.readthedocs.io/en/latest/workflows.html.
```

## CPP SPM

```
The fMRI data were pre-processed and analyzed using statistical parametric
mapping (SPM12 – v7487; Wellcome Center for Neuroimaging, London, UK;
www.fil.ion.ucl.ac.uk/spm) running on {octave 4.{??} / matlab 20{XX}
(Mathworks)}.

The preprocessing of the functional images was performed in the following order:
removing of dummy scans, {slice timing correction}, realignment, normalization
to MNI, smoothing.

{XX} dummy scans were removed to allow signal stabilization.

{Slice timing correction was then performed taking the {XX}th slice as a
reference (interpolation: sinc interpolation).}

Functional scans from each participant were realigned using the mean image as a
reference (SPM 2 passes ; number of degrees of freedom: 6 ; cost function: least
square) (Friston et al, 1995).

The mean image obtained from realignement was then co-registered to the
anatomical T1 image (number of degrees of freedom: 6 ; cost function: normalized
mutual information) (Friston et al, 1995). The transformation matrix from this
coregistration was then applied to all the functional images.

The anatomical T1 image was bias field corrected, segmented and normalized to
MNI space (target space resolution: 1 mm ; interpolation: 4th degree b-spline)
using a unified segmentation. The deformation field obtained from this step was
then applied to all the functional images (target space resolution equal that
used at acquisition ; interpolation: 4th degree b-spline)

Functional MNI normalized images were then spatially smoothed using a 3D
gaussian kernel (FWHM = {XX} mm).
```

## SPM references

### spm_realign

Friston KJ, Ashburner J, Frith CD, Poline J-B, Heather JD & Frackowiak RSJ
(1995) Spatial registration and normalization of images Hum. Brain Map.
2:165-189

### spm_coreg

```
% Mutual Information
% -------------------------------------------------------------------------
% Collignon, Maes, Delaere, Vandermeulen, Suetens & Marchal (1995).
% "Automated multi-modality image registration based on information theory".
% In Bizais, Barillot & Di Paola, editors, Proc. Information Processing
% in Medical Imaging, pages 263--274, Dordrecht, The Netherlands, 1995.
% Kluwer Academic Publishers.
%
% Wells III, Viola, Atsumi, Nakajima & Kikinis (1996).
% "Multi-modal volume registration by maximisation of mutual information".
% Medical Image Analysis, 1(1):35-51, 1996.
%
% Entropy Correlation Coefficient
% -------------------------------------------------------------------------
% Maes, Collignon, Vandermeulen, Marchal & Suetens (1997).
% "Multimodality image registration by maximisation of mutual
% information". IEEE Transactions on Medical Imaging 16(2):187-198
%
% Normalised Mutual Information
% -------------------------------------------------------------------------
% Studholme, Hill & Hawkes (1998).
% "A normalized entropy measure of 3-D medical image alignment".
% in Proc. Medical Imaging 1998, vol. 3338, San Diego, CA, pp. 132-143.
%
% Optimisation
% -------------------------------------------------------------------------
% Press, Teukolsky, Vetterling & Flannery (1992).
% "Numerical Recipes in C (Second Edition)".
% Published by Cambridge.
```

### spm_normalize

K.J. Friston, J. Ashburner, C.D. Frith, J.-B. Poline, J.D. Heather, and R.S.J.
Frackowiak Spatial Registration and Normalization of Images. Human Brain Mapping
2:165-189, 1995.

J. Ashburner, P. Neelin, D.L. Collins, A.C. Evans and K.J. Friston,
Incorporating Prior Knowledge into Image Registration. NeuroImage
6:344-352, 1997.

J. Ashburner and K.J. Friston. Nonlinear spatial normalization using basis
functions. Human Brain Mapping, 7(4):254-266, 1999.

### spm_spm

```
% References:
%
% Statistical Parametric Maps in Functional Imaging: A General Linear
% Approach. Friston KJ, Holmes AP, Worsley KJ, Poline JB, Frith CD,
% Frackowiak RSJ. (1995) Human Brain Mapping 2:189-210.
%
% Analysis of fMRI Time-Series Revisited - Again. Worsley KJ, Friston KJ.
% (1995) NeuroImage 2:173-181.
```
