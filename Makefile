.PHONY: docs start
.DEFAULT: help


help:
	@echo "Commands available: docs, start"

docs:
	@cd docs && python3 rmOld.py && sphinx-apidoc -o ./source ../ && make html

start:
	@cd .. && python3 -m quadratic_voting

install:
	python3 -m spacy download en_core_web_sm