-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

-- Show deprecation warnings
vim.g.deprecation_warnings = true

local opt = vim.opt

opt.spelllang = { "en" }
opt.tabstop = 4 -- Number of spaces tabs count for
opt.termguicolors = true -- True color support

opt.timeoutlen = vim.g.vscode and 1000 or 300 -- Lower than default (1000) to quickly trigger which-key
opt.wrap = true -- Enable line wrap

-- Fix markdown indentation settings
-- vim.g.markdown_recommended_style = 0
