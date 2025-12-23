if vim.g.neovide then
  -- transparence (0.0 = opaque, 1.0 = invisible)
  vim.g.neovide_opacity = 0.85  -- flouter l'arrière-plan
  vim.g.neovide_window_blurred = true  vim.g.neovide_cursor_vfx_mode = "pixiedust"
  vim.g.neovide_cursor_trail_size = 0.8  -- animations
  vim.g.neovide_scroll_animation_length = 0.3
  vim.g.neovide_floating_blur_amount_x = 2.0
  vim.g.neovide_floating_blur_amount_y = 2.0
end
