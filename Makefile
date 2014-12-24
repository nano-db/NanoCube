VERSION=$(shell grep __version__ server/__init__.py)
REQUIREMENTS="requirements.txt"
TAG="\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"


all: test

uninstall-nanodb:
	@echo $(TAG)Removing existing install$(END)
	- pip uninstall --yes nanodb >/dev/null
	! which nanodb
	@echo

uninstall-all: uninstall-nanodb
	- pip uninstall --yes -r $(REQUIREMENTS)

init: uninstall-nanodb
	@echo $(TAG)Install dev reqs$(END)
	pip install --upgrade -r $(REQUIREMENTS)
	@echo $(TAG)Install nanodb$(END)
	pip install --upgrade --editable .
	@echo

test: init
	@echo $(TAG)Running test$(END)
	nosetests
	@echo

test-sdist: uninstall-nanodb
	@echo $(TAG)Testing sdist build an installation$(END)
	python setup.py sdist
	pip install --force-reinstall --upgrade dist/*.gz
	which nanodb

test-all: uninstall-all clean init test

publish: test-all
	@echo $(TAG)Testing and publishing$(END)
	@echo "$(VERSION)"
	python setup.py register
	python setup.py sdist upload
	@echo

clean:
	@echo $(TAG)Clean up$(END)
	rm -rf .tox *.egg dist build .coverage
	@echo

