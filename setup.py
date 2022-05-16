from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Python Package for Storyboarding in osu!'
LONG_DESCRIPTION = 'file: readme.md'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="pystoryboard", 
        version=VERSION,
        author="indexerror",
        author_email="lkycst@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pillow'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'storyboard', 'osu'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
)