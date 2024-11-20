# Junk Item
# LE Byte 0 = Unique Name Index
# LE Byte 1 = Theme
# LE Byte 2 = Offset
JUNK_ID_OFFSET = 0x000001 # +1 since ID = 0 appears reserved/invalid

# Goal Item
# LE Byte 0 = Unique Name Index
# LE Byte 1 = Theme
# LE Byte 2 = Offset
GOAL_ID_OFFSET = 0x010000

# Key Item
# LE Byte 0 = Region
# LE Byte 1 = Theme
# LE Byte 2 = Offset
KEY_ID_OFFSET = 0x020000

# Chest ID offset
# LE Byte 0 = Chest Number
# LE Byte 1 = Theme
# LE Byte 2 = Region
# LE Byte 3 = Offset
CHEST_ID_OFFSET = 0x03000000

# Game-affecting Items
# LE Byte 0 = Unique Name Index
# LE Byte 1 = Theme
# LE Byte 2 = Affect Type
# LE Byte 3 = Offset
GAME_AFFECTOR_ID_OFFSET = 0x04000000
