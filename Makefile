.PHONY: help link install update check

PYTHON := python3
COMMANDS_SCRIPT := make_commands.py

help:
	@echo "🛠️  Available commands:"
	@echo ""
	@echo "  make link      -> 🔗 Create symlinks for config files"
	@echo "  make install   -> 💾 Install full configuration (links, nvim, fonts, etc.)"
	@echo "  make update    -> ⬆️  Update repo, links, and nvim plugins"
	@echo "  make check     -> ✅  Check system and configuration status"
	@echo ""

link:
	$(PYTHON) $(COMMANDS_SCRIPT) link

install:
	$(PYTHON) $(COMMANDS_SCRIPT) install

update:
	$(PYTHON) $(COMMANDS_SCRIPT) update

check:
	$(PYTHON) $(COMMANDS_SCRIPT) check
