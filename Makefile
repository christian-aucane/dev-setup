.PHONY: help link install update check

PYTHON := python3
COMMANDS_SCRIPT := make_commands.py

help:
	@echo "make link	-> create symlinks"
	@echo "make install	-> install full configuration"

link:
	$(PYTHON) $(COMMANDS_SCRIPT) link

install:
	$(PYTHON) $(COMMANDS_SCRIPT) install

update:
	$(PYTHON) $(COMMANDS_SCRIPT) update

check:
	$(PYTHON) $(COMMANDS_SCRIPT) check
