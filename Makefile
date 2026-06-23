
all: stl

# usage: make view part=part-name
view:
	uv run --group vscode -m cad view $(if $(part),--part $(part),)

# usage: make stl part=part-name
stl:
	uv run -m cad export --format stl $(if $(part),--part $(part),)

format: format-cad

format-cad:
	uv run ruff format $(if $(check),--check,) src/cad tests/cad

lint: lint-cad

lint-cad:
	uv run ruff check $(if $(check),,--fix) src/cad tests/cad

test: test-cad

test-cad:
	uv run pytest tests/cad

clean:
	git clean -Xdf
