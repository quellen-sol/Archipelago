from .adventure import adventure_theme
from .scifi import scifi_theme

all_themes = [adventure_theme, scifi_theme]

# Validate that all themes have distinct offset ids
offsets = set(theme.offset_code for theme in all_themes)
assert len(offsets) == len(all_themes), "All themes must have distinct offset ids"
