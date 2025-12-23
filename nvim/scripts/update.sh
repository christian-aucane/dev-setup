#!/usr/bin/env bash
set -e

# -------------------------------------------
# Minimal Neovim update script (user-only)
# -------------------------------------------

# Path to your repo
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"  # root of the repo

echo ">>> Updating Neovim config repo..."
git -C "$REPO_DIR" pull

echo ">>> Installing/updating plugins..."
nvim --headless +PlugInstall +qall

echo ">>> Done! Neovim config and plugins are up to date."

