from BaseClasses import Location
from themes.all_themes import all_themes


class ArchipelaPalLocation(Location):
    game = "ArchipelaPal"


loc_names_table = {}
loc_codes_table = {}

for theme in all_themes:
    theme.write_to_locations_table(loc_names_table, loc_codes_table)
