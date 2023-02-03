# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmos_noise_map', 'cmos_noise_map.tests', 'cmos_noise_map.utils']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.2.1',
 'click>=8.1.3',
 'glob2>=0.7',
 'ipython>=8.9.0',
 'matplotlib>=3.6.3',
 'myst-parser>=0.18.1',
 'nbsphinx>=0.8.12',
 'numpy>=1.24.1',
 'pandas>=1.5.3',
 'pandoc>=2.3',
 'pytest>=7.2.1',
 'scikit-learn>=1.2.1',
 'scipy>=1.10.0']

extras_require = \
{':docs': ['sphinx>=4,<6']}

entry_points = \
{'console_scripts': ['rts-maker = cmos_noise_map.main:cli']}

setup_kwargs = {
    'name': 'cmos-noise-map',
    'version': '0.1.0',
    'description': "A tool to create a read noise map for CMOS detectors by modelling Random Telegraph Signal. This was originally created for use by LCOGT's BANZAI pipeline.",
    'long_description': "# CMOS Noise Map\n[![Python application](https://github.com/LCOGT/cmos-noise-map/actions/workflows/python-app.yml/badge.svg)](https://github.com/LCOGT/cmos-noise-map/actions/workflows/python-app.yml)\n\nCode to model random telegraph noise in a CMOS detector. Originally designed for the Las Cumbres Observatory BANZAI pipeline.\nAuthors: Prerana Kottapalli, Matt Daily, Curtis McCully\n\nRead the docs: https://cmos-noise-map.readthedocs.io/en/latest/index.html\n\n## Installation\n### From PyPi\n¯\\_(ツ)_/¯ Not on Pypi yet\n\n### From Github\nTo install the tool, clone this repository and run:\n\n```\npip install poetry\ncd cmos-noise-map\npoetry install\n```\n## Tests\nTo run the unit tests, simply run:\n\n`poetry run pytest`\n\n## Usage\nOnce you've installed the tool, it can be run simply by:\n`rts-maker <path> <options> <write filename>`\n\n```\nUsage: rts-maker [OPTIONS] PATH FILENAME [METHOD]\n\n  This script builds a noise map with the chosen method.\n\n  path: Path to input without the .fits at the end\n\n  filename: Path to write file, including the filename ending in .fits\n\n  method: Default method is std. Available methods are std, rts, and param.\n  See docs for more information about each method.\n\nOptions:\n  -r, --data_ext INTEGER          Extension of fits file that contains the\n                                  image data\n  -uq, --upper_quantile FLOAT     Standard deviation cutoff for pixel noise\n                                  evaluation\n  -t, --tolerance FLOAT           The minimum difference between silhouette\n                                  scores. See docs for more information.\n  -m, --min_peak_separation FLOAT\n                                  Minimum difference between pixel value\n                                  cluster centers to be considered separate\n                                  clusters\n  -o, --out_hdu_name TEXT         Name for the header in which the data will\n                                  be stored\n  --help                          Show this message and exit.\n\n```\n",
    'author': 'Prerana Kottapalli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

