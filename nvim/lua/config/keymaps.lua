-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- [START] CUSTOM --

vim.keymap.set("i", ";;", "<Esc>", { desc = "Quit insertion mode" })
vim.keymap.set("i", ";;w", "<Esc><cmd>w<CR>", { desc = "Quit insertion mode and save file" })
-- [END] CUSTOM --
