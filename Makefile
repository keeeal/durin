
all: stls

stls:
	python -m cad export

format-cad:
	isort $(if $(check),--check,) . && black $(if $(check),--check,) .

format: format-cad

test-cad:
	pytest tests/cad

test: test-cad

install-cad:
	pip install --upgrade pip
	pip install --editable .${if $(dev),[dev],}

clean:
	git clean -Xdf
