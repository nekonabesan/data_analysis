SHELL := /usr/bin/env bash

SCRIPT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT_ROOT := $(abspath $(SCRIPT_DIR)/..)
WORK_DIR := $(PROJECT_ROOT)/work
JUPYTER_TOKEN ?= vscode-jupyter-token
DOCKER_COMPOSE ?= docker compose
SERVICE_NAME ?= stock_and_finance
IMAGE_NAME ?= ferm-finance-jupyter:latest
UV_PROJECT_DIR ?= /tmp/env
UV_ENV_PYTHON ?= /tmp/prophet-venv/bin/python
UV_ENV_DIR ?= /tmp/prophet-venv

.PHONY: start build stop logs sync lock install innstall

# Allows: make install numpy
ifneq ($(filter install innstall,$(MAKECMDGOALS)),)
  MODULE_FROM_GOAL := $(word 2,$(MAKECMDGOALS))
  ifneq ($(MODULE_FROM_GOAL),)
    $(eval $(MODULE_FROM_GOAL):;@:)
  endif
endif

start:
	@mkdir -p "$(WORK_DIR)"
	@if ! docker image inspect "$(IMAGE_NAME)" >/dev/null 2>&1; then \
		echo "Image $(IMAGE_NAME) not found. Running make build..."; \
		$(MAKE) build; \
	fi
	@cd "$(SCRIPT_DIR)" && JUPYTER_TOKEN="$(JUPYTER_TOKEN)" $(DOCKER_COMPOSE) up -d
	@echo "Jupyter URL for VS Code: http://127.0.0.1:8888/?token=$(JUPYTER_TOKEN)"

build:
	@cd "$(SCRIPT_DIR)"; \
	if docker image inspect "$(IMAGE_NAME)" >/dev/null 2>&1; then \
		echo "Removing existing image $(IMAGE_NAME)..."; \
		$(DOCKER_COMPOSE) down >/dev/null 2>&1 || true; \
		docker rmi -f "$(IMAGE_NAME)" >/dev/null; \
	fi; \
	echo "Building image $(IMAGE_NAME)..."; \
	$(DOCKER_COMPOSE) build $(SERVICE_NAME)

stop:
	@cd "$(SCRIPT_DIR)" && $(DOCKER_COMPOSE) down

logs:
	@cd "$(SCRIPT_DIR)" && $(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

sync:
	@cd "$(SCRIPT_DIR)"; \
	if ! $(DOCKER_COMPOSE) ps --status running --services | grep -q "^$(SERVICE_NAME)$$"; then \
		echo "Service $(SERVICE_NAME) is not running. Run 'make start' first."; \
		exit 1; \
	fi; \
	$(DOCKER_COMPOSE) exec -T $(SERVICE_NAME) env UV_PROJECT_ENVIRONMENT="$(UV_ENV_DIR)" uv sync --project "$(UV_PROJECT_DIR)" --no-dev

lock:
	@cd "$(SCRIPT_DIR)" && uv lock

install:
	@module="$(or $(MODULE),$(MODULE_FROM_GOAL))"; \
	if [ -z "$$module" ]; then \
		echo "Usage: make install <module_name>"; \
		exit 1; \
	fi; \
	cd "$(SCRIPT_DIR)"; \
	if ! $(DOCKER_COMPOSE) ps --status running --services | grep -q "^$(SERVICE_NAME)$$"; then \
		echo "Service $(SERVICE_NAME) is not running. Run 'make start' first."; \
		exit 1; \
	fi; \
	$(DOCKER_COMPOSE) exec -T $(SERVICE_NAME) uv pip install --python "$(UV_ENV_PYTHON)" "$$module"

innstall: install