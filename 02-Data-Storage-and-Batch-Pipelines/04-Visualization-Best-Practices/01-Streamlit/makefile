include ../../../make.inc

.PHONY: docs install test supertest

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := poetry run python -c "$$BROWSER_PYSCRIPT"

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/app.rst
	rm -f docs/modules.rst
	poetry run sphinx-apidoc -o docs/ app
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/build/html/index.html

test-f1transforms:
	poetry run pytest -v -k TestF1Transforms

test: pytest
