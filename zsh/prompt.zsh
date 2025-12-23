
# =========================================
# prompt.zsh
# Prompt Zsh minimal, lisible et efficace
# =========================================

echo "DEBUG: prompt.zsh loaded"

# Permet l'expansion de variables dans le prompt
setopt PROMPT_SUBST

# Couleurs
autoload -Uz colors
colors

# Indique le statut de la dernière commande
# ✔ vert si succès, ✘ rouge si erreur
local exit_status='%(?.%F{green}✔.%F{red}✘)'

# User@host (en bleu)
local user_host='%F{blue}%n@%m%f'

# Répertoire courant (chemin abrégé)
local cwd='%F{yellow}%~%f'

# Symbole de prompt
local prompt_char='%F{magenta}%#%f'

# Prompt final
PROMPT="${exit_status} ${user_host} ${cwd} ${prompt_char} "
