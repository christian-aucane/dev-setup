# Linux Setup 🚀
![Neovim](https://img.shields.io/badge/Neovim-0.9+-green)
![Neovide](https://img.shields.io/badge/Neovide-GUI-blue)
![Zsh](https://img.shields.io/badge/Shell-Zsh-orange)
![Font](https://img.shields.io/badge/Font-FiraCode%20Nerd%20Font-purple)


Personal **Linux development environment setup**, focused on **Neovim**, **Neovide**, **Zsh**, and clean dotfile management.

This repository is designed to be:
- reproducible
- minimal
- safe to update
- fully symlink-based

---

## Features ✨

### 🧠 Neovim
- LazyVim-based configuration
- Modular Lua config
- Neovide-specific overrides
- No root / no sudo required

### 🖥️ Neovide
- GUI configuration via `config.toml`
- Smooth cursor animations
- Transparency & padding
- Box-drawing rendering fixes
- Optional visual effects (cursor, shadows)

### 🐚 Zsh
- Managed via dotfiles
- `.zshrc` and `.zshenv` symlinked
- Shell configuration versioned and reproducible
- No framework imposed (you stay in control)

### 🎨 Fonts
- **FiraCode Nerd Font**
- Ligatures, icons, box-drawing support
- Installed locally (user-level)

### 🔗 Dotfiles
- Safe symlink management
- Automatic backups if files already exist
- Idempotent setup (can be re-run safely)

---

## Installation 🛠️

Clone the repository:

```bash
git clone https://github.com/christian-aucane/setup-linux.git
cd ~/setup-linux
```

Run the setup:
```bash
make install
```

This will:

1. Create symlinks for
- Zsh config (.zshrc, .zshenv)
- Neovim config
2. Install fonts locally
3. Install Neovim-related Python tools
4. Apply Neovide configuration

---

## Updating 🔄
Update everything safely:

```bash
make update
```

What happens:

1. git pull (with safety checks)
2. Re-run symlink logic (in case files changed)
3. Update Neovim configuration

  ⚠️ Make sure your local changes are committed or stashed before updating.

---

## Checks ✅

Verify your environment:
```bash
make check
```
Checks include:
- Git repository status
- Dotfile symlinks validity
- Neovim availability
- Fonts installation
- Required tools presence

---

## Zsh 🐚

Zsh is configured via:

- `zsh/.zshenv`
- `zsh/.zshrc`

They are symlinked to:

```bash
~/.zshenv
~/.zshrc
```

An optional environment-specific file can be used:

- `zsh/env.zsh` (ignored by git)

It is automatically sourced by .zshrc and is meant for machine-specific tweaks (custom PATH, local binaries, school/work setup, etc.).

An example is provided:
```bash
zsh/env.zsh.example
```

To use it:
```bash
cp zsh/env.zsh.example zsh/env.zsh
```
and update it.

No external framework (Oh-My-Zsh, etc.) is required, but you can add one on top if you want.

---

## Fonts 🎨

Installed font:
- FiraCode Nerd Font
- Bold / Italic supported
- Box-drawing compatible
- Installed in:
```bash
~/.local/share/fonts
```

---

## Neovide 🖥️

Neovide configuration is split cleanly:

- `neovide/config.toml` → GUI / font / rendering

- `nvim/lua/neovide.lua` → runtime & UI behavior

Font is handled by **Neovide**, not Neovim.

---

Ignored Files ❌

The following files are intentionally not tracked:

- `lazy-lock.json`
- `lazyvim.json`

They are machine-specific and auto-generated.

- `env.zsh`
(This is environment-specific zsh configuration)
---

## Philosophy 🧘

- No sudo
- No magic
- Explicit configuration only
- Easy rollback
- One command setup

---

## License 📄

Personal configuration — provided **as is**.
Use it, fork it, or adapt it freely.


