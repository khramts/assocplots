import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "assocplots",
    version = "0.0.2",
    author = "Ekaterina",
    author_email = "eakhram@gmail.com",
    description = ("AssocPlots"),
    license = "MIT",
    keywords = "manhattan qqplot Quantile-Quantile plots",
    url = "https://github.com/khramts/assocplots",
    packages=['assocplots'],
    long_description=read('README.md'),
    install_requires=[
          'matplotlib', 'bokeh', 'numpy', 'scipy'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)