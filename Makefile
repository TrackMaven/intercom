.DEFAULT_GOAL := tests

clean:
	git clean -Xdf
	rm -rf build/ dist/

setup:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	py.test
