# TwiFEx
TwiFEx is a Python package for feature extraction from tweets. It aims to facilitate feature extraction in Twitter-centric projects by incorporating a novel feature categorisation into the skeleton of the package. To this end, it uses five criteria (unit of analysis, level of resolution, configuration mode, time dependency, location dependency) to distil a broad range of features into 18 categories. In addition to feature extraction, TwiFEx offers a variety of functionalities to rapidly make sense of a collection of tweets. TwiFEx's emphasis is on the ease of use, extensibility, alignment with the machine learning pipeline, and API consistency. TwiFEx project comes with a BSD license which makes it open to adapt for commercial and non-commercial usage.


## Installation for developers

Prerequisites:

- Python 3.7 or 3.8
- Anaconda

Install datacube in a new virtual environment to avoid dependency issues:
```
git clone https://gitlab.tudelft.nl/steelelab/datacube.git
cd datacube
conda env create -f environment.yml
conda activate twifex
```