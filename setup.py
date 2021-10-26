import setuptools

setuptools.setup(name="ctdicom2raw",
                 version="1.0",
                 author="z0gSh1u",
                 author_email="zx.cs@qq.coom",
                 description="Convert CT DICOM to RAW File with CT Parameters Output",
                 url="https://github.com/z0gSh1u/ctdicom2raw",
                 packages=setuptools.find_packages(),
                 install_requires=['pydicom', 'tqdm'])
