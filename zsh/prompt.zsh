# =========================================
# prompt.zsh
# Prompt Zsh lisible, moderne et informatif
# =========================================

setopt PROMPT_SUBST

autoload -Uz colors
colors

# -----------------------------------------
# OS lisible
# -----------------------------------------
if [[ -f /etc/os-release ]]; then
  source /etc/os-release
  OS_NAME=$ID
else
  OS_NAME=$(uname -s)
fi

# -----------------------------------------
# vcs_info (Git)
# -----------------------------------------
autoload -Uz vcs_info
setopt prompt_subst

# Affiché AVANT chaque prompt
precmd() {
  vcs_info
}

# Activer Git
zstyle ':vcs_info:*' enable git

# Format de base (sans couleur ici)
zstyle ':vcs_info:git:*' formats '(%b)'
zstyle ':vcs_info:git:*' actionformats '(%b|%a)'

# -----------------------------------------
# Statut dernière commande
# -----------------------------------------
local exit_status='%(?.%F{green}✔.%F{red}✘)%f'

# -----------------------------------------
# User@OS + poussin
# -----------------------------------------
local user_os="%F{blue}%n@%F{cyan}${OS_NAME} %F{yellow}🐤%f"

# -----------------------------------------
# Couleur dynamique de la branche Git
# -----------------------------------------
git_prompt() {
  [[ -z "$vcs_info_msg_0_" ]] && return

  local branch="$vcs_info_msg_0_"
  local color="%F{green}"   # clean par défaut
  local suffix=""

  # état critique : merge / rebase / etc
  if [[ -n "$vcs_info_msg_1_" ]]; then
    color="%F{red}"
    suffix="!"
  # repo dirty
  elif ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    color="%F{yellow}"
    suffix="*"
  fi

  echo " ${color}${branch}${suffix}%f"
}

# -----------------------------------------
# Répertoire courant
# -----------------------------------------
local cwd="%F{green}%~%f"

# -----------------------------------------
# Symbole de prompt
# -----------------------------------------
local prompt_char="%F{magenta}%#%f"

# -----------------------------------------
# Prompt final
# -----------------------------------------
PROMPT=' ${exit_status} ${user_os} $(git_prompt) ${cwd} ${prompt_char} '
