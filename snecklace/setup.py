"""
Developer install
-----------------
Run following command in Anaconda prompt/terminal:
    pip install -e .
"""
from setuptools import setup


setup(name='nlacestats', #name of package on import
      version='0.1',  # package version
      description='Small scripts for collecting and collating statistics',  # brief description
      url='https://github.com/sarahhp/snlace.git',  # git repo url
      author='Sarah Hazell Pickering',  # author(s)
      author_email='sarah.pickering@anu.edu.au',  # email
      license='MIT',  # licensing
      packages=['stats_scripts'], #main package
      install_requires=[  # dependencies
        'numpy', 
        'pandas',  # manage tabular data in dataframes
        #'bicopython'
      ],
zip_safe=True) # package can be installed from zip file
