nbdir = docs/demo_md/

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


_doc: #  gets run by docs/conf.py so we don't need to commit files in $(nbdir)
	# Remove and make directory
	@rm -r -f $(nbdir)
	@mkdir $(nbdir)
	@for f in demo/imfdatapy*.ipynb; do \
		echo "#\tConverting $$f"; \
		jupyter nbconvert --to markdown --output-dir='$(nbdir)' $$f 2>/dev/null; \
	done
	#jupyter nbconvert --to markdown --output-dir='$(nbdir)'  demo/imfdatapy_demo.ipynb
	#jupyter nbconvert --to markdown --output-dir='$(nbdir)'  demo/imfdatapy_IFS_GDP_example.ipynb

_doc_clean:
	@cd docs && make clean

doc_html:
	@cd docs && make html

doc_pdf:
	@cd docs && make latexpdf

doc_epub:
	@cd docs && make epub

docs: _doc_clean _doc _uml doc_html doc_pdf doc_epub

fasttests:
	coverage run -m pytest tests/test_dot.py

longtests:
	coverage run -m pytest

coverage:
	@echo "\nCode coverage"
	@rm -r -f htmlcov
	python -m coverage report -m
	coverage html

fasttests_cov: fasttests coverage


longtests_cov: longtests coverage