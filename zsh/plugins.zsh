
# =========================================
# plugins.zsh
# Gestionnaire + plugins
# =========================================

# Installer zinit si absent
if [[ ! -f "$HOME/.zinit/bin/zinit.zsh" ]]; then
    mkdir -p "$HOME/.zinit"
    git clone https://github.com/zdharma-continuum/zinit.git "$HOME/.zinit/bin"
fi

source "$HOME/.zinit/bin/zinit.zsh"

# Plugins essentiels
zinit light zsh-users/zsh-autosuggestions
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-history-substring-search
zinit light zdharma-continuum/fast-syntax-highlighting
zinit light hlissner/zsh-autopair

# zoxide
zinit ice as"program" atclone"./install.sh" atpull"%atclone"
zinit light ajeetdsouza/zoxide

if (( $+commands[zoxide] )); then
    eval "$(zoxide init zsh)"
fi

