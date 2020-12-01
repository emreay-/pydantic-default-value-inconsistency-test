
user_name:=$(shell echo `id -un $(USER)`)
user_id:=$(shell echo `id -u $(USER)`)
user_group:=$(shell echo `id -g $(USER)`)
PYDANTIC_VERSION*=

.PHONY: build
build:
	docker build \
		--build-arg UNAME=${user_name} \
		--build-arg UID=${user_id} \
		--build-arg GID=${user_group} \
		--build-arg PYDANTIC_VERSION=${PYDANTIC_VERSION} \
		-t pydantic_default_value_issue .


.PHONY: run
run: build
	docker run --rm -t pydantic_default_value_issue pytest -s --disable-pytest-warnings pydantic_default_value_issue.py
