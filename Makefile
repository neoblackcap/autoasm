.PHONY: install-dev docs docs-deploy

install-dev:
	pip install -r requirement.txt

docs: install-dev
	python setup.py build_sphinx

