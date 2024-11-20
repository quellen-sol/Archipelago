from BaseClasses import Item
from .themes.all_themes import all_themes


class ArchipelaPalItem(Item):
    game = "ArchipelaPal"


item_names_table = {}
item_codes_table = {}

for theme in all_themes:
    theme.write_to_items_tables(item_names_table, item_codes_table)
