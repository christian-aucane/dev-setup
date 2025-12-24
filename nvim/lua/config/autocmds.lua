-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")

-- [START] CUSTOM --

-- Disable autoformat for c files (formated by 42norm)
vim.api.nvim_create_autocmd({ "FileType" }, {
	pattern = { "c", "h" },
	callback = function()
		vim.b.autoformat = false
	end,
})

-- Smart <Esc> behavior: first press exits insert mode, second press closes the terminal
vim.api.nvim_create_autocmd("TermOpen", {
	pattern = "term://*",
	callback = function(ev)
		local buf = ev.buf

		-- First ESC: exit terminal insert mode
		vim.keymap.set("t", "<Esc>", function()
			vim.cmd("stopinsert")
		end, {
			buffer = buf,
			noremap = true,
			silent = true,
			desc = "Exit insert mode (terminal)",
		})

		-- Second ESC: close terminal buffer
		vim.keymap.set("n", "<Esc>", function()
			vim.cmd("bd!")
		end, {
			buffer = buf,
			noremap = true,
			silent = true,
			desc = "Close terminal buffer",
		})
	end,
})
-- [END] CUSTOM --
