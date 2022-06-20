.PHONY: install
install: install-poetry allow-envrc

.PHONY: install-poetry
install-poetry:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry install' \;

.PHONY: format
format:
	find . -name pyproject.toml -exec sh -c 'cd $$(exec dirname {}) && make format' \;

.PHONY: test
test:
	find . -name pyproject.toml -exec sh -c 'cd $$(exec dirname {}) && make test' \;

.PHONY: update
update:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry update' \;

.PHONY: add-envrc
add-envrc:
	find . -name pyproject.toml -exec sh -c 'echo "layout poetry" > "$$(exec dirname {})/.envrc"' \;

.PHONY: allow-envrc
allow-envrc:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && direnv allow .' \;
