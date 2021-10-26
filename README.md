# ctdicom2raw

This is a Python tool that converts CT DICOM files into RAW files, with CT parameters retrieved from DICOM metadata output.

## Usage

### Install

**Via wheel**

Download `.whl` file from [Releases](https://github.com/z0gSh1u/ctdicom2raw/releases), and run:

```sh
pip install <path_to_whl_file>
```

**Via source**

Clone this repository, and run:

```sh
python setup.py install
```

### Use as a Library

```python
from ctdicom2raw import ctdicom2raw

ctdicom2raw(dicomFolder, outputFolder, renameFunc=DEFAULT_REANME_FUNC, outputParam='first', verbose=False)
```

- `dicomFolder`:  path to a folder full of DICOM files (.dcm / .IMA etc.)
- `outputFolder`: path to save .raw output files
- `renameFunc`: a function that receives the filename of DICOM file and return the filename of RAW file
- `outputParam`: 'first': CT parameters will be retrieved only once from the first slice; 'every': CT parameters will be retrieved for every slice
- `verbose`: True to show the progress bar of conversion

### Use as a CLI

Have it installed, and have `ctdicom2raw.sh` downloaded, and run:

```sh
ctdicom2raw.sh <dicomFolder> <outputFolder> [outputParam]
```

## Details

### CT Parameters

These parameters will be extracted from DICOM metadata as a JSON file in `outputFolder`:

| Tag                         | Example                | Remarks        |
| --------------------------- | ---------------------- | -------------- |
| Window Center               | [55, -600]             | as str         |
| Window Width                | [440, 1500]            | as str         |
| Manufacturer                | SIEMENS                |                |
| Manufacturer Model Name     | SOMATOM Definition AS+ |                |
| Body Part Examined          | ABDOMEN                |                |
| Patient Position            | FFS                    |                |
| KVP                         | 100.0                  | keV            |
| X Ray Tube Current          | 101.0                  | mA             |
| Exposure Time               | 500.0                  |                |
| Exposure                    | 84.0                   |                |
| Slice Thickness             | 1.0                    | mm             |
| Data Collection Diameter    | 500.0                  | mm             |
| Reconstruction Diameter     | 340.0                  | mm             |
| Rows                        | 512                    |                |
| Columns                     | 512                    |                |
| Pixel Spacing               | [0.6640625, 0.6640625] | mm             |
| Distance Source To Detector | 1085.6                 | SDD, mm        |
| Distance Source To Patient  | 595.0                  | SOD, mm        |
| Rotation Direction          | CW                     |                |
| Bits Allocated              | 16                     | must be 16     |
| Table Height                | 126.0                  |                |
| Table Speed                 | 46.0                   |                |
| Table Feed Per Rotation     | 23.0                   |                |
| Rescale Intercept           | -1024.0                |                |
| Rescale Slope               | 1.0                    |                |
| Rescale Type                | "HU"                   |                |
| Spiral Pitch Factor         | 0.6                    | for helical CT |

Refer to the source code to find the corresponding (Group, Element) pair.

### RAW File Format

- Pixel Value Type: 16-bit Unsigned
- Width, Height: same as Rows, Columns
- Byte Order: Little-endian
- Pixel Value Meaning: Detector received value before rescaling to HU using *kx+b*

A proper WW/WL should be set to get a similar view like DICOM file.

## Third-party Libraries

- [pydicom](https://github.com/pydicom/pydicom)
- tqdm

## License

MIT

