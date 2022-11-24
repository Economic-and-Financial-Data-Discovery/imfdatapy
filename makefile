
uninstall_imf:
	cd ..
	rm -fr IMF_data_discovery
	conda deactivate
	conda remove --name imf --all

install_imf:
	git clone https://github.com/Economic-and-Financial-Data-Discovery/imfdatapy.git
	cd imfdatapy
	git checkout develop
	conda env create --file environment.yml
	conda activate imfdatapy
	jupyter nbextensions_configurator enable --user
	python -m ipykernel install --user --name=imfdatapy
	pip install -e .

_uml:
	pyreverse -k src/imfdatapy/imf.py -o png
	mv classes.png docs/imfdatapy_classes.png
	pyreverse src/imfdatapy/imf.py -o png
	mv classes.png docs/imfdatapy_classes_members.png



doc_html:
	sphinx-build -b html doc doc/build

doc_pdf:
	sphinx-build -b latex doc doc/build -W --keep-going  2>/dev/null
	cd doc/build/
	latex doc/build/imfdatapy.tex
	cd ../..

tests:
	python -W ignore -m coverage run --append --source=./ -m unittest discover -s tests/ 1>/dev/null