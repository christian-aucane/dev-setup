# =========================================
# ~/.zshenv
# Variables d’environnement UNIQUEMENT
# =========================================

# Chemin du repo
ZSHENV_DIR="${0:A:h}"
export DOTFILES="${ZSHENV_DIR:h}"

# Évite de charger la conf interactive dans les scripts
export ZDOTDIR="$HOME"

# User specific environment
if ! [[ ":$PATH:" == *":$HOME/.local/bin:$HOME/bin:"* ]]; then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH
