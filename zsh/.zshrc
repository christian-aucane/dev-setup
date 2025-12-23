# =========================================
# ~/.zshrc
# Point d’entrée interactif
# =========================================

echo "DEBUG: .zshrc loaded"

ZSHRC_REALPATH="${${(%):-%N}:A}"
REPO_ZSH_DIR="$(dirname "$ZSHRC_REALPATH")"
# 1️⃣ Options Zsh (setopt, HISTFILE, etc.)
source "$REPO_ZSH_DIR/options.zsh"

# 2️⃣ Aliases
[[ -f "$REPO_ZSH_DIR/aliases.zsh" ]] && source "$REPO_ZSH_DIR/aliases.zsh"

# 3️⃣ Complétion (OBLIGATOIRE avant plugins)
autoload -Uz compinit
compinit

# 4️⃣ Options des plugins (variables AVANT chargement)
[[ -f "$REPO_ZSH_DIR/plugin_options.zsh" ]] && source "$REPO_ZSH_DIR/plugin_options.zsh"

# 5️⃣ Plugins
[[ -f "$REPO_ZSH_DIR/plugins.zsh" ]] && source "$REPO_ZSH_DIR/plugins.zsh"

# 6️⃣ Keymaps / bindkey (APRÈS plugins)
[[ -f "$REPO_ZSH_DIR/keymaps.zsh" ]] && source "$REPO_ZSH_DIR/keymaps.zsh"

# Prompt (doit être chargé en dernier)
[[ -f "$REPO_ZSH_DIR/prompt.zsh" ]] && source "$REPO_ZSH_DIR/prompt.zsh"
