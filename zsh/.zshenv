# =========================================
# ~/.zshenv
# Variables d’environnement UNIQUEMENT
# =========================================

echo "DEBUG : .zshenv loaded"
# Chemin du repo dotfiles
ZSHENV_DIR="${0:A:h}"
export DOTFILES="${ZSHENV_DIR:h}"

# Évite de charger la conf interactive dans les scripts
export ZDOTDIR="$HOME"

# PATH de base (minimal)
export PATH="$HOME/bin:$PATH"
