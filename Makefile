IDU := $(shell id -u)
IDG := $(shell id -g)

.PHONY: install-base
install-base:
	./install.sh

.PHONY: install-poetry
install-poetry:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry install' \;

.PHONY: install
install: install-base install-poetry add-envrc allow-envrc

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

.PHONY: del-test-output
del-test-output:
	find . -name test_output.txt | xargs rm

.PHONY: own-repo
own-repo:
	@sudo chown $(IDU):$(IDG) -R .
