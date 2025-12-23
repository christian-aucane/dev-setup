# =========================================
# options.zsh
# Configuration Zsh de base (starter)
# =========================================

echo "DEBUG: options.zsh loaded"

# -------------------
# Historique (CRITIQUE)
# -------------------
HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000

setopt APPEND_HISTORY          # ajoute à l’historique existant
setopt SHARE_HISTORY           # partage entre shells
setopt INC_APPEND_HISTORY      # écrit immédiatement
setopt HIST_IGNORE_DUPS        # ignore doublons
setopt HIST_IGNORE_SPACE       # ignore commandes avec espace devant
setopt HIST_REDUCE_BLANKS      # nettoie espaces
setopt HIST_VERIFY             # édite avant exécution

# -------------------
# Navigation
# -------------------
setopt AUTO_CD                 # entrer dans un dossier en tapant son nom
setopt AUTO_PUSHD              # cd empilé
setopt PUSHD_IGNORE_DUPS

# -------------------
# Complétion & édition
# -------------------
setopt COMPLETE_IN_WORD
setopt ALWAYS_TO_END
setopt AUTO_LIST

# -------------------
# Interaction
# -------------------
unsetopt BEEP                  # pas de bip
setopt INTERACTIVE_COMMENTS    # # en interactif

# -------------------
# Globbing
# -------------------
setopt EXTENDED_GLOB

# -------------------
# Sécurité
# -------------------
unsetopt CLOBBER               # évite > d’écraser
