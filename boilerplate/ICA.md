# boilerplate for ICA

taken from the [COBIDAS blog](https://cobidas.wordpress.com/2016/05/23/cobidas-easter-egg/)

## Single-Modality ICA

Methods for ICA analyses are not as consolidated as mass univariate linear modelling, but we provide short summaries of some typical analyses in GIFT and MELODIC (alphabetical order), based on versions GIFTv3.0a and FSL 5.0.8, respectively. [Optional aspects, depending on particular variants used, indicated in brackets.]

### GIFT

GIFT, single-subject fMRI with ICASSO stability: Spatial ICA estimated with infomax where scaling of original data, spatial components and time courses constrained to unit norm, resulting best-run selected from 10 runs; post-ICA Z statistics produced for maps, between temporal component correlation (Functional Network Correlation), time courses, spectra, tested within a GLM framework.

GIFT, multi-subject PCA-based back-reconstruction with ICASSO stability: Single-subject PCA followed by temporal concatenation, group-level PCA and then spatial ICA with infomax; calculation of single subject maps using PCA-based back-reconstruction, resulting best-run selected from 10 runs; post-ICA Z statistics produced for maps, time courses, spectra, and between temporal component correlation (Functional Network Correlation) tested within a GLM framework. [Time-varying states computed using moving window between temporal components (Dynamic Functional Network Correlation).]

GIFT, spatio-temporal (dual) regression of new data: Using provided component maps calculates per-subject components from new data using regression-based back-reconstruction; produces component maps, time courses and spectra and between temporal component correlation (Functional Network Correlation) tested within a GLM framework.

GIFT, spatial ICA with reference: Spatial ICA using one or more provided seed or component maps. Components found by joint maximization of non-Gaussianity and similarity to spatial maps resulting in subject specific component maps and timecourses for each subject, scaled to Z-scores, following by testing voxelwise (within network connectivity), between temporal component correlation (Functional Network Correlation), spectra, tested within a GLM framework.

GIFT, source based morphometry of gray matter maps: Spatial ICA of multi-subject gray matter segmentation maps (from SPM, FSL, etc) resulting in spatial components and subject-loading parameters tested within a GLM framework.

### MELODIC

MELODIC, single-subject ICA: Spatial ICA estimated by maximising non-Gaussian sources, using robust voxel-wise variance-normalisation of data, automatic model-order selection and Gaussian/Gamma mixture-model based inference on component maps.

MELODIC, group level (concat ICA): Temporally concatenation of fMRI data, followed by spatial ICA estimated by maximising non-Gaussian sources, using using robust voxel-wise variance-normalisation of data, automatic model order selection and Gaussian/Gamma mixture-model based inference on component maps

MELODIC, group-level (tensor-ICA): Higher-dimensional decomposition of all fMRI data sets into spatial, temporal and subject modes; automatic model order selection and Gaussian/Gamma mixture-model based inference on component maps

MELODIC dual regression: Estimation of subject-specific temporal and spatial modes from group-level ICA maps or template maps using spatial followed by temporal regression.

## Multi-Modalitiy ICA

Available multi-modality ICA methods include FIT and FSL-FLICA (alphabetical order), based on versions FITv2.0c and flica_2013-01-15, respectively.

### FIT

FIT, joint ICA, two-group, fMRI + EEG fusion: Joint spatial ICA of GLM contrast maps and temporal ICA of single or multi-electrode event-related potential time course data (can be non-concurrent) with infomax ICA; produces joint component maps (each with an fMRI component map and ERP component timecourse(s)) and subject loading parameters which are then tested for group differences with a GLM framework.

FIT, N-way fusion using multiset CCA+joint ICA: Multiset canonical correlation analysis applied to several spatial maps to extract components, then submitted to spatial ICA with infomax ICA; produces multi-modal component maps and subject-specific loading parameters which are tested within a GLM framework.

FIT, parallel ICA, fusion of gray matter maps and genetic polymorphism array data: Joint spatial ICA of gray matter segmentation maps and genetic ICA of single nucleotide polymorphism data performed through a maximization of independence among gray matter components, genetic components, and subject-wise correlation among one or more gray matter and genetic components. Produces linked and unlinked gray matter and genetic components and subject loading parameters which are then tested within a GLM framework.

### FSL

FSL-FLICA multi-subject/multi-modality (Linked-ICA): ICA-based estimation of common components across multiple image modalities, linked through a shared subject-courses.
