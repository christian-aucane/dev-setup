-- neovide.lua
if vim.g.neovide then
	-- Fullscreen mode
	vim.g.neovide_fullscreen = false -- valeurs: true/false, default: false

	-- Scale factor (zoom général)
	vim.g.neovide_scale_factor = 1.0 -- float >=0, default: 1.0

	-- Padding around Neovim content
	vim.g.neovide_padding_top = 12 -- default: 0
	vim.g_neovide_padding_bottom = 12
	vim.g_neovide_padding_left = 12
	vim.g_neovide_padding_right = 12

	-- Smooth scrolling
	vim.g.neovide_scroll_animation_length = 0.25 -- secondes, default: 0.3
	vim.g.neovide_scroll_animation_far_lines = 3 -- default: 1
	vim.g.neovide_no_idle = false -- force redraw continu, default: false

	-- Cursor animations
	vim.g.neovide_cursor_animation_length = 0.18 -- temps de l'animation du curseur, default: 0.150
	vim.g.neovide_cursor_trail_size = 0.7 -- 0.0 à 1.0, default 1.0
	vim.g.neovide_cursor_vfx_mode = "pixiedust" -- effets: "", "railgun", "torpedo", "pixiedust", "sonicboom", "ripple", "wireframe"
	vim.g.neovide_cursor_vfx_opacity = 200.0 -- opacity particules, default 200
	vim.g.neovide_cursor_vfx_particle_lifetime = 0.5 -- durée de vie particules (s)
	vim.g.neovide_cursor_vfx_particle_density = 0.8 -- nombre de particules, default 0.7
	vim.g.neovide_cursor_vfx_particle_speed = 12.0 -- pixels / sec, default 10

	-- IME input (East Asian languages)
	vim.g.neovide_input_ime = true -- default true

	-- Window transparency
	vim.g.neovide_opacity = 0.92 -- default 1.0
	vim.g.neovide_normal_opacity = 0.92 -- default 1.0
	vim.g.neovide_window_blurred = true

	-- Theme: mirror system theme
	vim.g.neovide_theme = "auto" -- valeurs: auto/light/dark/bg_color, default: auto

	-- Optional: smooth blink for cursor
	vim.g.neovide_cursor_smooth_blink = true -- default false
end
