
all: stls

stls:
	python -m cad export

install: install-cad

install-cad:
	pip install --upgrade pip
	pip install --editable .${if $(dev),[dev],}

format: format-cad

format-cad:
	isort $(if $(check),--check,) . && black $(if $(check),--check,) .

test: test-cad

test-cad:
	pytest tests/cad

clean:
	git clean -Xdf
