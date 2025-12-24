.PHONY: help link install

PYTHON := python3
COMMANDS_SCRIPT := make_commands.py

help:
	@echo "make link	-> create symlinks"
	@echo "make install	-> install full configuration"

link:
	$(PYTHON) $(COMMANDS_SCRIPT) link

install:
	$(PYTHON) $(COMMANDS_SCRIPT) install
