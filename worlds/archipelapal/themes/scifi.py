from .ThemeContents import ThemeContents

scifi_theme = ThemeContents(0x01)

scifi_theme.set_hub_name("Space Station")
scifi_theme.set_chest_name("Storage Crate")
scifi_theme.set_key_name("Key Card")

scifi_theme.add_junk_item("Old Canister")
scifi_theme.add_junk_item("Rusty Bolt")

scifi_theme.add_goal_item("Strange Device")
scifi_theme.add_goal_item("Strange Orb")

scifi_theme.add_speed_boost_item("Ion Thruster")
scifi_theme.add_speed_boost_item("Photon Boosters")

scifi_theme.validate()
