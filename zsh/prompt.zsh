# =========================================
# prompt.zsh
# Prompt Zsh lisible, moderne et efficace
# =========================================

# Permet l'expansion de variables dans le prompt
setopt PROMPT_SUBST

# Couleurs
autoload -Uz colors
colors

# -----------------------------------------
# OS (lisible au lieu d'un UUID)
# -----------------------------------------
if [[ -f /etc/os-release ]]; then
  source /etc/os-release
  OS_NAME=$ID
else
  OS_NAME=$(uname -s)
fi

# -----------------------------------------
# Git / VCS
# -----------------------------------------
autoload -Uz vcs_info
setopt PROMPT_SUBST

# Format : (branch)
zstyle ':vcs_info:git:*' formats '(%b)'
zstyle ':vcs_info:*' enable git

# Met à jour vcs_info avant chaque prompt
precmd() {
  vcs_info
}

# -----------------------------------------
# Statut dernière commande
# -----------------------------------------
# ✔ vert si succès, ✘ rouge si erreur
local exit_status='%(?.%F{green}✔.%F{red}✘)%f'

# -----------------------------------------
# User@OS + canard 🐤
# -----------------------------------------
local user_os="%F{blue}%n@%F{cyan}${OS_NAME} %F{yellow}🐤%f"

# -----------------------------------------
# Répertoire courant
# -----------------------------------------
# Vert vif pour bien contraster
local cwd="%F{green}%~%f"

# -----------------------------------------
# Branche Git
# -----------------------------------------
# Violet pour bien ressortir
local git_branch='%F{magenta}${vcs_info_msg_0_}%f'

# -----------------------------------------
# Symbole de prompt
# -----------------------------------------
local prompt_char="%F{magenta}»%f"

# -----------------------------------------
# Prompt final
# -----------------------------------------
PROMPT=" ${exit_status} ${user_os} ${cwd} ${git_branch} ${prompt_char} "
