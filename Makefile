install:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry install' \;

add-envrc:
	find . -name pyproject.toml -exec sh -c 'echo "layout poetry" > "$$(exec dirname {})/.envrc"' \;
