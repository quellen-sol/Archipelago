from ThemeContents import ThemeContents

adventure_theme = ThemeContents(0x00)
adventure_theme.set_chest_name("Chest")
adventure_theme.set_key_name("Key")

adventure_theme.add_junk_item("Meat Scraps")
adventure_theme.add_goal_item("Magic Crystal")

adventure_theme.validate()
