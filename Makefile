IDU := $(shell id -u)
IDG := $(shell id -g)

######## Initial setup #######

.PHONY: install-poetry
install-poetry:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry install' \;

.PHONY: allow-envrc
allow-envrc:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && direnv allow .' \;

.PHONY: own-repo
own-repo:
	@sudo chown $(IDU):$(IDG) -R .

.PHONY: install
install: install-poetry allow-envrc own-repo

######## Ongoing commands #######

.PHONY: format
format:
	find . -name pyproject.toml -exec sh -c 'cd $$(exec dirname {}) && make format' \;

.PHONY: test
test:
	find . -name pyproject.toml -exec sh -c 'cd $$(exec dirname {}) && make test' \;

.PHONY: update
update:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry update' \;

.PHONY: del-test-output
del-test-output:
	find . -name test_output.txt | xargs rm
