
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
	@cd docs && make clean && make html

doc_pdf:
	@cd docs && make clean && make latexpdf

doc_epub:
	@cd docs && make clean && make epub

fasttests:
	pytest tests/test_dot.py --junitxml=junit/test_dot-results.xml --cov-report=html

longtests:
	pytest tests/ --doctest-modules --junitxml=junit/test-results.xml --cov-report=html

tests: longtests

coverage:
	@echo "\nCode coverage"
    coverage run -m pytest
	python -m coverage report -m