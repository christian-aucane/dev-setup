.PHONY: help link

PYTHON := python3

help:
	@echo "make link	-> create symlinks"

link:
	$(PYTHON) scripts/dotfiles.py link
