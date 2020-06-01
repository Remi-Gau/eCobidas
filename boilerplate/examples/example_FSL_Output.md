# Automatic text outputs from FSL

# For pre-processing with FEAT:

Analysis methods
FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version 6.00, part of FSL (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). Registration to high resolution structural and/or standard space images was carried out using FLIRT [Jenkinson 2001, 2002]. Registration from high resolution structural to standard space was then further refined using FNIRT nonlinear registration [Andersson 2007a, 2007b].

References
[Jenkinson 2001] M. Jenkinson and S.M. Smith. A Global Optimisation Method for Robust Affine Registration of Brain Images. Medical Image Analysis 5:2(143-156) 2001.
[Jenkinson 2002] M. Jenkinson, P. Bannister, M. Brady and S. Smith. Improved Optimisation for the Robust and Accurate Linear Registration and Motion Correction of Brain Images. NeuroImage 17:2(825-841) 2002.
[Andersson 2007a] J.L.R. Andersson, M. Jenkinson and S.M. Smith. Non-linear optimisation. FMRIB technical report TR07JA1, 2007.
[Andersson 2007b] J.L.R. Andersson, M. Jenkinson and S.M. Smith. Non-linear registration, aka Spatial normalisation. FMRIB technical report TR07JA2, 2007.

# For first-level GLM:

Analysis methods
FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version 6.00, part of FSL (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). Time-series statistical analysis was carried out using FILM with local autocorrelation correction [Woolrich 2001].

References
[Woolrich 2001] M.W. Woolrich, B.D. Ripley, J.M. Brady and S.M. Smith. Temporal Autocorrelation in Univariate Linear Modelling of FMRI Data. NeuroImage 14:6(1370-1386) 2001.

# For second-level GLM:

Analysis methods
FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version 6.00, part of FSL (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). Higher-level analysis was carried out using FLAME (FMRIB's Local Analysis of Mixed Effects) stage 1 [Beckmann 2003, Woolrich 2004, Woolrich 2008].

References
[Beckmann 2003] C. Beckmann, M. Jenkinson and S.M. Smith. General multi-level linear modelling for group analysis in FMRI. NeuroImage 20(1052-1063) 2003.
[Woolrich 2004] M.W. Woolrich, T.E.J Behrens, C.F. Beckmann, M. Jenkinson and S.M. Smith. Multi-level linear modelling for FMRI group analysis using Bayesian inference. NeuroImage 21:4(1732-1747) 2004
[Woolrich 2008] M.W. Woolrich. Robust Group Analysis Using Outlier Inference. NeuroImage 41:2(286-301) 2008

# Split up by me (Johannes) for which references belongs to which action:
fMRI data for each of the six blocks per participants were preprocessed using FSL 6.0.0 (Smith et al., 2004). Functional images were cleaned for non-brain tissue (BET; Smith, 2002), segmented, motion-corrected (MC-FLIRT; Jenkinson, Bannister, Brady, & Smith, 2002), and smoothed (FWHM 3 mm). Field maps were used for B0 unwarping and distortion correction in orbitofrontal areas. We used ICA-AROMA (Pruim et al., 2015) to automatically detect and reject independent components in the data that were associated with head motion. 
Before running GLMs, we performed high-pass filtering with a cutoff of 100 s and pre-whitening. Co-registrations to high-resolution anatomical images (linearly with FLIRT using Boundary-Based Registration) and to MNI152 2mm isotropic standard space (non-linearly with FNIRT using 12 DOF and 10 mm warp resolution; Andersson, Jenkinson, & Smith, 2007) were performed before fitting first-level GLMs.