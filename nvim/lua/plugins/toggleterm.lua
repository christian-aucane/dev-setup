local shell_path = "/usr/bin/zsh"
if vim.fn.executable("zsh") == 0 then
    shell_path = vim.o.shell  -- fallback si Zsh non installé
end

return {
	"akinsho/toggleterm.nvim",
	version = "*",
	config = function()
		local toggleterm = require("toggleterm")
		toggleterm.setup({
			size = 15,
			open_mapping = [[<C-t>]],
			hide_numbers = true,
			shade_terminals = true,
			start_in_insert = true,
			insert_mappings = true,
			terminal_mappings = true,
			persist_size = true,
			direction = "float",
			close_on_exit = true,
			shell = shell_path,
		})

		-- ----------- NORMAL MODE MAPPINGS -----------
		local keymap = vim.keymap.set
		local opts = { noremap = true, silent = true }

		keymap(
			"n",
			"<leader>tt",
			"<cmd>ToggleTerm direction=float<CR>",
			vim.tbl_extend("force", opts, { desc = "Floating terminal" })
		)
		keymap(
			"n",
			"<leader>th",
			"<cmd>ToggleTerm size=15 direction=horizontal<CR>",
			vim.tbl_extend("force", opts, { desc = "Horizontal terminal" })
		)
		keymap(
			"n",
			"<leader>tv",
			"<cmd>ToggleTerm size=50 direction=vertical<CR>",
			vim.tbl_extend("force", opts, { desc = "Vertical terminal" })
		)
	end,
}
