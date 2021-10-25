import pydicom
import os
from os import path
import json


def _CTPARAM(loc, type_):
    return {'loc': loc, 'type': type_}


CTPARAMS = {
    # For WC two values will be fetched. Usually they are the same.
    # If not, it means that the view is recommended to be displayed using to windows.
    # So as WD.
    'Window Center': _CTPARAM([0x0028, 0x1050], str),
    'Window Width': _CTPARAM([0x0028, 0x1051], str),

    # Manufacturer
    'Manufacturer': _CTPARAM([0x0008, 0x0070], str),
    'Manufacturer Model Name': _CTPARAM([0x0008, 0x1090], str),

    # Patient status
    'Body Part Examined': _CTPARAM([0x0018, 0x0015], str),
    'Patient Position': _CTPARAM([0x0018, 0x5100], str),  # (H/F)F(S/P)

    # X-Ray exposure
    'KVP': _CTPARAM([0x0018, 0x0060], float),  # kVpeak
    'X Ray Tube Current': _CTPARAM([0x0018, 0x1151], float),  # mA
    'Exposure Time': _CTPARAM([0x0018, 0x1150], float),
    'Exposure': _CTPARAM([0x0018, 0x1152], float),

    # CT Reconstruction
    'Slice Thickness': _CTPARAM([0x0018, 0x0050], float),
    'Data Collection Diameter': _CTPARAM([0x0018, 0x0090], float),
    'Reconstruction Diameter': _CTPARAM([0x0018, 0x1100], float),
    'Rows': _CTPARAM([0x0028, 0x0010], int),
    'Columns': _CTPARAM([0x0028, 0x0011], int),
    'Pixel Spacing': _CTPARAM([0x0028, 0x0030], str),  # u/v, mm
    'Distance Source To Detector': _CTPARAM([0x0018, 0x1110], float),  # SDD, mm
    'Distance Source To Patient': _CTPARAM([0x0018, 0x1111], float),  # SOD, mm
    'Rotation Direction': _CTPARAM([0x0018, 0x1140], str),  # CW/CCW
    'Bits Allocated': _CTPARAM([0x0028, 0x0100], int),

    # Table
    'Table Height': _CTPARAM([0x0018, 0x1130], float),
    'Table Speed': _CTPARAM([0x0018, 0x9309], float),
    'Table Feed Per Rotation': _CTPARAM([0x0018, 0x9310], float),

    # CT Value rescaling
    # e.g.  HU = 1X-1024
    'Rescale Intercept': _CTPARAM([0x0028, 0x1052], float),
    'Rescale Slope': _CTPARAM([0x0028, 0x1053], float),
    'Rescale Type': _CTPARAM([0x0028, 0x1054], str),

    # For helical CT
    'Spiral Pitch Factor': _CTPARAM([0x0018, 0x9311], float)
}

ExampleDcmFile = 'F:/MedRecon/AAPM-CT-Dataset/AAPM-Reconstructed/L067/' + \
    'L067_FD_1_1.CT.0001.0001.2015.12.22.18.09.40.840353.358074219.IMA'


def fetchCTParams(dicom):
    res = {}

    def _fetchCTParam(param):
        metaParam = CTPARAMS[param]
        if metaParam is None:
            return None
        value = metaParam['type'](dicom[metaParam['loc'][0], metaParam['loc'][1]].value)
        return value

    for key in CTPARAMS.keys():
        res[key] = _fetchCTParam(key)
    return res


def dumpCTParams(dicom, path_):
    json.dump(fetchCTParams(dicom), path_, indent=2)


DEFAULT_REANME_FUNC = lambda x: '.'.join(x.split('.')[:-1])


def ctdicom2raw(dicomFolder, outputFolder, renameFunc=DEFAULT_REANME_FUNC, outputParam='first'):
    dicomFiles = sorted(os.listdir(dicomFolder))
    dicomPaths = [path.join(dicomFolder, x) for x in dicomFiles]
    for idx, dicomPath in enumerate(dicomPaths):
        dcm = pydicom.dcmread(dicomPath)
        outputName = renameFunc(dicomFiles[idx])
        # output CT parameters
        if outputParam == 'every':
            paramOutputPath = path.join(outputFolder, outputName + '.param.json')
            json.dump(fetchCTParams(dcm), paramOutputPath, indent=2)
        # convert pixel data bytes to raw file
        rawOutputPath = path.join(outputFolder, outputName + '.raw')
        f = open(rawOutputPath, mode='wb')
        f.write(dcm.PixelData)
        f.close()
    if outputParam == 'first':
        dcm = pydicom.dcmread(dicomPath)
        outputName = renameFunc(dicomFiles[0])
        # output CT parameters
        dumpCTParams(dcm)
        paramOutputPath = path.join(outputFolder, outputName + '.param.json')
        json.dump(fetchCTParams(dcm), paramOutputPath, indent=2)


def _ctdicom2raw(dcmPath, rawOutputPath):
    dcm = pydicom.dcmread(ExampleDcmFile)
    # print(dcm[0x0028, 0x1050].value)
    print(fetchCTParams(dcm))
    # bytes_ = dcm.PixelData
    # f = open(rawOutputPath, mode='wb')
    # f.write(bytes_)
    # f.close()


_ctdicom2raw(None, None)
