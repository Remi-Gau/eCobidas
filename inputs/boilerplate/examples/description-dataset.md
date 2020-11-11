# boilerplate for MRI dataset description

<!-- TOC -->
<!-- lint disable -->

-   [boilerplate for MRI dataset description](#boilerplate-for-mri-dataset-description)
    -   [from pybids and bids-matlab](#from-pybids-and-bids-matlab) -
        [anat](#anat) - [func](#func) - [fmap](#fmap) - [dwi](#dwi) -
        [eeg](#meeg)
        <!-- lint enable -->
        <!-- /TOC -->

## General

### pybids

```python
    out_str = ('MR data were acquired using a {tesla}-Tesla {manu} {model} '
               'MRI scanner.')
    out_str = out_str.format(tesla=metadata.get('MagneticFieldStrength',
                                                'UNKNOWN'),
                             manu=metadata.get('Manufacturer', 'MANUFACTURER'),
                             model=metadata.get('ManufacturersModelName',
                                                'MODEL'))
```


```python
desc = '''
        Dicoms were converted to NIfTI-1 format{software_str}.
        This section was (in part) generated
        automatically using pybids ({meth_vers}).
        '''.format(software_str=software_str,
                    meth_vers=__version__)
```

## anat

### pybids

```python
    desc = '''
{suffix} {variants} {seqs} structural MRI data were collected
({n_slices} slices; repetition time, TR={tr}ms;
echo time, TE={te}ms; flip angle, FA={fa}<deg>;
field of view, FOV={fov}mm; matrix size={ms}; voxel size={vs}mm).
'''.format(suffix=suffix,
            variants=variants,
            seqs=seqs,
            n_slices=n_slices,
            tr=num_to_str(metadata['RepetitionTime']*1000),
            te=te,
            fa=metadata.get('FlipAngle', 'UNKNOWN'),
            vs=vs_str,
            fov=fov_str,
            ms=ms_str,
            )
```

### bids-matlab

```matlab
anat_text = cat(2, ...
    '%s %s %s structural MRI data were collected (%s slices; \n', ...
    'repetition time, TR= %s ms; echo time, TE= %s ms; flip angle, FA=%s deg; \n', ...
    'field of view, FOV= %s mm; matrix size= %s; voxel size= %s mm) \n\n');

fprintf(anat_text,...
    acq_param.type, acq_param.variants, acq_param.seqs, ...
    acq_param.n_slices, acq_param.tr, ...
    acq_param.te, acq_param.fa, ...
    acq_param.fov, acq_param.ms, acq_param.vs);
```

## func

### pybids

```python
desc = '''
        {run_str} of {task} {variants} {seqs} {me_str} fMRI data were
        collected ({n_slices} slices{so_str}; repetition time, TR={tr}ms;
        echo time, TE={te}ms; flip angle, FA={fa}<deg>;
        field of view, FOV={fov}mm; matrix size={ms};
        voxel size={vs}mm{mb_str}{pr_str}).
        Each run was {length} minutes in length, during which
        {n_vols} functional volumes were acquired.
        '''.format(run_str=run_str,
                    task=task_name,
                    variants=variants,
                    seqs=seqs,
                    me_str=me_str,
                    n_slices=n_slices,
                    so_str=so_str,
                    tr=num_to_str(tr*1000),
                    te=te,
                    fa=metadata.get('FlipAngle', 'UNKNOWN'),
                    vs=vs_str,
                    fov=fov_str,
                    ms=ms_str,
                    length=length,
                    n_vols=n_tps,
                    mb_str=mb_str,
                    pr_str=pr_str
                    )
```                     

### bids-matlab

```
'%s run(s) of %s %s %s fMRI data were collected (%s slices acquired in a %s fashion; repetition time, TR= %s ms; \n', ...
'echo time, TE= %s ms; flip angle, FA= %s deg; field of view, FOV= %s mm; matrix size= %s; \n', ...
'voxel size= %s mm; multiband factor= %s; in-plane acceleration factor= %s). Each run was %s minutes in length, during which \n', ...
'%s functional volumes were acquired. \n\n');

fprintf(func_text,...
    acq_param.run_str, acq_param.task, acq_param.variants, acq_param.seqs, ...
    acq_param.n_slices, acq_param.so_str, acq_param.tr, ...
    acq_param.te, acq_param.fa, ...
    acq_param.fov, acq_param.ms, ...
    acq_param.vs, acq_param.mb_str, acq_param.pr_str, ...
    acq_param.length, ...
    acq_param.n_vols);
```

## fmap

### pybids

```python
desc = '''
        A {variants} {seqs} field map (phase encoding:
        {dir_}; {n_slices} slices; repetition time, TR={tr}ms;
        echo time, TE={te}ms; flip angle, FA={fa}<deg>;
        field of view, FOV={fov}mm; matrix size={ms};
        voxel size={vs}mm) was acquired{for_str}.
        '''.format(variants=variants,
                    seqs=seqs,
                    dir_=dir_,
                    for_str=for_str,
                    n_slices=n_slices,
                    tr=num_to_str(metadata['RepetitionTime']*1000),
                    te=te,
                    fa=metadata.get('FlipAngle', 'UNKNOWN'),
                    vs=vs_str,
                    fov=fov_str,
                    ms=ms_str)
```

### bids-matlab

```matlab
fmap_text = cat(2, ... 
'A %s %s field map (phase encoding: %s; %s slices; repetition time, TR= %s ms; \n',... 
'echo time 1 / 2, TE 1/2= %s ms; flip angle, FA= %s deg; field of view, FOV= %s mm; matrix size= %s; \n',... 
'voxel size= %s mm) was acquired %s. \n\n');

fprintf(fmap_text,... 
acq_param.variants, acq_param.seqs, acq_param.phs_enc_dir, acq_param.n_slices, acq_param.tr, ... 
acq_param.te, acq_param.fa, acq_param.fov, acq_param.ms, ... 
acq_param.vs, acq_param.for);

```

## dwi

```python
desc = '''
        One run of {variants} {seqs} diffusion-weighted (dMRI) data were collected
        ({n_slices} slices{so_str}; repetition time, TR={tr}ms;
        echo time, TE={te}ms; flip angle, FA={fa}<deg>;
        field of view, FOV={fov}mm; matrix size={ms}; voxel size={vs}mm;
        b-values of {bval_str} acquired;
        {n_vecs} diffusion directions{mb_str}).
        '''.format(variants=variants,
                    seqs=seqs,
                    n_slices=n_slices,
                    so_str=so_str,
                    tr=num_to_str(metadata['RepetitionTime']*1000),
                    te=te,
                    fa=metadata.get('FlipAngle', 'UNKNOWN'),
                    vs=vs_str,
                    fov=fov_str,
                    ms=ms_str,
                    bval_str=bval_str,
                    n_vecs=n_vecs,
                    mb_str=mb_str
                    )
```

### bids-matlab

```matlab
fmap_text = cat(2, ...
'One run of %s %s diffusion-weighted (dMRI) data were collected (%s slices %s ; repetition time, TR= %s ms \n', ...
'echo time, TE= %s ms; flip angle, FA= %s deg; field of view, FOV= %s mm; matrix size= %s ; voxel size= %s mm \n', ...
'b-values of %s acquired; %s diffusion directions; multiband factor= %s ). \n\n');

fprintf(fmap_text,...
acq_param.variants, acq_param.seqs, acq_param.n_slices, acq_param.so_str, acq_param.tr,...
acq_param.te, acq_param.fa, acq_param.fov, acq_param.ms, acq_param.vs, ...
acq_param.bval_str, acq_param.n_vecs, acq_param.mb_str);
```

## meeg

See this [repository](https://github.com/guiomar/Armitage_BIDS_NLG) started
by Guiomar Niso to start creating method section for MEG data sets.

MNE also generates some level of dataset description at the end of the BIDS
conversion. See for example:

```
Summarizing participants.tsv /Users/hoechenberger/mne_data/eegmmidb_bids_group_conversion/participants.tsv...
Summarizing scans.tsv files [PosixPath('/Users/hoechenberger/mne_data/eegmmidb_bids_group_conversion/sub-002/ses-01/sub-002_ses-01_scans.tsv'), PosixPath('/Users/hoechenberger/mne_data/eegmmidb_bids_group_conversion/sub-001/ses-01/sub-001_ses-01_scans.tsv')]...
The participant template found: sex were all unknown;
handedness were all unknown; ages all unknown
This dataset was created with BIDS version 1.4.0 by Please cite MNE-BIDS in your
publication before removing this (citations in README). This report was
generated with MNE-BIDS (https://doi.org/10.21105/joss.01896). The dataset
consists of 2 participants (sex were all unknown; handedness were all unknown;
ages all unknown)and 1 recording sessions: 01. Data was recorded using a EEG
system sampled at 160.0 Hz with line noise at 50 Hz. There were 6 scans in
total. Recording durations ranged from 122.99 to 124.99 seconds (mean = 123.99,
std = 1.0), for a total of 743.96 seconds of data recorded over all scans. For
each dataset, there were on average 64.0 (std = 0.0) recording channels per
scan, out of which 64.0 (std = 0.0) were used in analysis (0.0 +/- 0.0 were
removed from analysis).
```

See
[here for example](https://mne.tools/mne-bids/stable/auto_examples/convert_group_studies.html#sphx-glr-auto-examples-convert-group-studies-py)

Implemented by [`report.py`](https://github.com/mne-tools/mne-bids/blob/master/mne_bids/report.py).






