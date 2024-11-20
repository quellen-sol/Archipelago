from .ThemeContents import ThemeContents

adventure_theme = ThemeContents(0x00)

adventure_theme.set_hub_name("Castle Town")
adventure_theme.set_chest_name("Chest")
adventure_theme.set_key_name("Key")

adventure_theme.add_junk_item("Meat Scraps")
adventure_theme.add_junk_item("Old Boot")

adventure_theme.add_goal_item("Magic Crystal")
adventure_theme.add_goal_item("Odd Rune")

adventure_theme.add_speed_boost_item("Cape of the Winds")
adventure_theme.add_speed_boost_item("Boots of Hermes")

adventure_theme.validate()
