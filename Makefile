
all: stls

stls:
	python -m cad export

install: install-cad

install-cad:
	pip install --upgrade pip
	pip install --editable .${if $(dev),[dev],}

format: format-cad

format-cad:
	isort $(if $(check),--check,) src/cad tests/cad && \
	black $(if $(check),--check,) src/cad tests/cad

test: test-cad

test-cad:
	pytest tests/cad

clean:
	git clean -Xdf
