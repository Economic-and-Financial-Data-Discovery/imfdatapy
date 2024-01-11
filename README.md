# imfdatapy
[![DOI](https://zenodo.org/badge/565568140.svg)](https://zenodo.org/badge/latestdoi/565568140)

A package for data discovery and extraction from the International Monetary Fund (IMF)!
This repository contains Python source code and Jupyter notebooks with examples on how to extract data from the IMF.

For a comprehensive overview of the project, including its objectives, design, and examples, you can refer to the following manuscript and online documentation:

- [IMFDataPy: A Python Package for IMF Data Discovery and Extraction](https://github.com/Economic-and-Financial-Data-Discovery/imfdatapy/blob/master/docs/imfdatapy.pdf)

- [IMFDataPy Documentation](https://imfdatapy.readthedocs.io/)


## Installation

```bash
    $ pip install imfdatapy
```

## Usage

`imfdatapy` can be used to search through and extract data as follows. The examples below show how to search through the IFS (International Financial Statistics) and BOP (Balance of Payments) using ```serach_terms``` and download all the data with matching economic indicator names.

```python
from imfdatapy.imf import *
ifs = IFS(search_terms=["gross domestic product, real"], countries=["US"], period='Q',
start_date="2000", end_date="2022")
df = ifs.download_data()

bop = BOP(search_terms=["current account, total, credit"], countries=["US"], period='Q',
start_date="2000", end_date="2022")
df = bop.download_data()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a [Code of Conduct](conduct.md). By contributing to this project, you agree to abide by its terms.

## License

`imfdatapy` was created by Sou-Cheng T. Choi and Irina Klein, Illinois Institute of Technology. It is licensed under the terms of the Apache License, v2.0.

With regard to the terms for using IMF data, please refer to IMF's [Copyright and Usage](https://www.imf.org/external/terms.htm) and pay special attention to the 
section _SPECIAL TERMS AND CONDITIONS PERTAINING TO THE USE OF DATA_.  


## Credits

`imfdatapy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
