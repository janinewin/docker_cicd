install:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry install' \;

update:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry update' \;

add-envrc:
	find . -name pyproject.toml -exec sh -c 'echo "layout poetry" > "$$(exec dirname {})/.envrc"' \;
