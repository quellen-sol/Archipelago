from ..offsets import (
    JUNK_ID_OFFSET,
    GOAL_ID_OFFSET,
    CHEST_ID_OFFSET,
    GAME_AFFECTOR_ID_OFFSET,
    KEY_ID_OFFSET,
)
import random


class ThemeContents:
    def __init__(self, offset_code: int):
        self.offset_code = offset_code
        self.junk_items = []
        self.goal_items = []
        self.speed_boost_items = []
        self.chest_name = ""
        self.key_name = ""
        self.hub_name = ""

    def choose_random_goal_item(self) -> str:
        return random.choice(self.goal_items)

    def choose_random_speed_boost_item(self) -> str:
        return random.choice(self.speed_boost_items)

    def choose_random_junk_item(self) -> str:
        return random.choice(self.junk_items)

    def set_chest_name(self, chest_name: str):
        self.chest_name = chest_name

    def set_key_name(self, key_name: str):
        self.key_name = key_name

    def set_hub_name(self, hub_name: str):
        self.hub_name = hub_name

    def add_junk_item(self, item_name: str):
        self.junk_items.append(item_name)

    def add_goal_item(self, item_name: str):
        self.goal_items.append(item_name)

    def add_speed_boost_item(self, item_name: str):
        self.speed_boost_items.append(item_name)

    def write_to_items_tables(self, names_table: dict, codes_table: dict):
        shifted_offset = self.offset_code << 8
        # Write Junk items to names_table and codes_table
        for i, item_name in enumerate(self.junk_items):
            item_code = JUNK_ID_OFFSET + shifted_offset + i
            names_table[item_name] = item_code
            codes_table[item_code] = item_name
        # Write Goal items to names_table and codes_table
        for i, item_name in enumerate(self.goal_items):
            item_code = GOAL_ID_OFFSET + shifted_offset + i
            names_table[item_name] = item_code
            codes_table[item_code] = item_name
        # Write Speed boost items to names_table and codes_table
        for i, item_name in enumerate(self.speed_boost_items):
            item_code = GAME_AFFECTOR_ID_OFFSET + shifted_offset + i # + 0x00 << 16 for speed boost
            names_table[item_name] = item_code
            codes_table[item_code] = item_name
        # Write all Keys to names_table and codes_table
        for region_n in range(1, 256):
            key_code = KEY_ID_OFFSET + shifted_offset + region_n
            key_name = f"{self.key_name} {region_n}"
            names_table[key_name] = key_code
            codes_table[key_code] = key_name

    def write_to_locations_table(self, loc_table: dict, codes_table):
        shifted_offset = self.offset_code << 8
        for region_n in range(0, 256):
            for chest_n in range(1, 256):
                chest_code = (
                    CHEST_ID_OFFSET
                    + (region_n << 16)
                    + shifted_offset
                    + chest_n
                )
                if region_n == 0:
                    # Use Hub name
                    name = f"{self.hub_name} {self.chest_name} {chest_n}"
                else:
                    # Use Chest name
                    name = f"{self.chest_name} {region_n}-{chest_n}"
                loc_table[name] = chest_code
                codes_table[chest_code] = name

    def validate(self):
        # Ensure that the names is not empty
        assert self.chest_name != "", "Chest name cannot be empty"
        assert self.key_name != "", "Key name cannot be empty"
        assert self.hub_name != "", "Hub name cannot be empty"

        # Ensure that the junk items are unique
        assert len(self.junk_items) == len(
            set(self.junk_items)
        ), "Junk items must be unique"

        # Ensure that the goal items are unique
        assert len(self.goal_items) == len(
            set(self.goal_items)
        ), "Goal items must be unique"

        # Ensure that the speed boost items are unique
        assert len(self.speed_boost_items) == len(
            set(self.speed_boost_items)
        ), "Speed boost items must be unique"

        # Ensure that there is at least one junk item
        assert len(self.junk_items) > 0, "There must be at least one junk item"

        # Ensure that there is at least one goal item
        assert len(self.goal_items) > 0, "There must be at least one goal item"

        # Ensure that there is at least one speed boost item
        assert (
            len(self.speed_boost_items) > 0
        ), "There must be at least one speed boost item"
