.DEFAULT_GOAL := tests

clean:
	git clean -Xdf
	rm -rf build/ dist/

setup:
	pip install --process-dependency-links -e .
	pip install -r requirements-dev.txt

test:
	py.test
