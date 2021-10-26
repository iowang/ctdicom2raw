# nbitconvert
# Convert CT DICOM to RAW File with CT Parameters Output
# https://github.com/z0gSh1u/ctdicom2raw
# by z0gSh1u


def convertToNBytes(inPath, sourceBytes: int, outPath, targetBytes: int=4, littleEndian=True):
    '''
        Convert a `sourceBytes` bytes per pixel image to a `targetBytes` per pixel one.
    '''
    fin = open(inPath, 'rb')
    fout = open(outPath, 'wb')

    assert targetBytes > sourceBytes
    paddingBytes = bytes([0] * (4 - sourceBytes))

    bytes_ = fin.read(sourceBytes)
    while True:
        if not littleEndian:
            fout.write(paddingBytes)
            fout.write(bytes_)
        else:
            fout.write(bytes_)
            fout.write(paddingBytes)
        bytes_ = fin.read(sourceBytes)
        if not bytes_:
            break

    fin.close()
    fout.close()
    return