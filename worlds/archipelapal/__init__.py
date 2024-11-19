from BaseClasses import Region, ItemClassification
from AutoWorld import World, WebWorld
from .Errors import ArchipelaPalError
from .Items import (
    ArchipelaPalItem,
    item_codes_table,
    item_names_table,
)
from .Locations import (
    ArchipelaPalLocation,
    loc_codes_table,
    loc_names_table,
)
from .Options import ArchipelaPalOptions
from .offsets import *
from .themes.all_themes import all_themes
from .utils import *


class ArchipelaPalWeb(WebWorld):
    tutorials = []
    theme = "ice"


class ArchipelaPal(World):
    """
    An automatic world-playing bot for Archipelago Randomizer
    """

    game = "ArchipelaPal"
    options_dataclass = ArchipelaPalOptions
    options: ArchipelaPalOptions
    web = ArchipelaPalWeb()

    item_name_to_id = item_names_table
    location_name_to_id = loc_names_table

    item_table = {}

    chests_per_region_result: list[int] = []

    # Might just do everything here?
    # Kinda wanna stay as far back as possible with this type of gen
    def generate_early(self) -> None:
        num_regions = self.options.num_regions

        min_chests_per_region = self.options.min_chests_per_region
        max_chests_per_region = self.options.max_chests_per_region

        min_time = self.options.min_time_between_checks
        max_time = self.options.max_time_between_checks

        num_sphere_0_chests = self.options.num_sphere_0_chests

        num_goal_items = self.options.num_goal_items

        pct_speed_boosts = self.options.pct_speed_boosts

        theme_choice = self.option.game_theme
        theme_obj = all_themes[theme_choice]

        min_expected_chests = num_regions * min_chests_per_region + num_sphere_0_chests

        if min_chests_per_region > max_chests_per_region:
            raise ArchipelaPalError(
                f"min_chests_per_region ({min_chests_per_region}) must be less than or equal to max_chests_per_region ({max_chests_per_region})"
            )

        if min_time > max_time:
            raise ArchipelaPalError(
                f"min_time_between_checks ({min_time}) must be less than or equal to max_time_between_checks ({max_time})"
            )

        if num_goal_items > min_expected_chests:
            raise ArchipelaPalError(
                f"num_goal_items ({num_goal_items}) must be less than or equal to the minimum expected number of chests ({min_expected_chests})"
            )

        itempool = []

        # Menu region
        menu = Region("Menu", self.player, self.multiworld)

        # Create Hub
        hub = Region("Hub", self.player, self.multiworld)

        # Create Hub Chests (Sphere 0)
        for chest_num in range(num_sphere_0_chests):
            real_chest = chest_num + 1
            chest_code = CHEST_ITEM_OFFSET + (theme_obj.offset_code << 8) + real_chest
            chest_name = loc_codes_table[chest_code]

            location = ArchipelaPalLocation(self.player, chest_name, chest_code, hub)
            hub.locations.append(location)
        self.chests_per_region_result.append(num_sphere_0_chests.value)

        total_junk_items = num_sphere_0_chests
        total_checks = num_sphere_0_chests
        for region_num in range(num_regions):
            region_display_num = region_num + 1
            # Create Region
            region_name = f"Region {region_display_num}"
            region_obj = Region(region_name, self.player, self.multiworld)

            # Create Key for this region
            key_code = (
                KEY_ITEM_OFFSET + (theme_obj.offset_code << 8) + region_display_num
            )
            key_name = item_codes_table[key_code]
            key_item = ArchipelaPalItem(
                key_name, ItemClassification.progression, key_code, self.player
            )
            itempool.append(key_item)
            self.item_table[key_name] = {
                "classification": ItemClassification.progression,
                "code": key_code,
            }

            num_chests = self.random.randint(
                min_chests_per_region, max_chests_per_region
            )
            total_checks += num_chests
            self.chests_per_region_result.append(num_chests)
            total_junk_items += num_chests - 1

            for chest_num in range(num_chests):
                real_chest = chest_num + 1
                chest_code = CHEST_ITEM_OFFSET + (region_display_num << 8) + real_chest
                chest_name = loc_codes_table[chest_code]

                location = ArchipelaPalLocation(
                    self.player, chest_name, chest_code, region_obj
                )
                region_obj.locations.append(location)

            self.multiworld.regions.append(region_obj)

            # Link this region to Hub &
            # Rule that the key is required to access the region
            # Wtf is this referencing bs, Python??? I have to use a default argument to hold on to the correct value????
            def rule(state, key_name=key_name):
                return state.has(key_name, self.player)

            hub.connect(region_obj, None, rule)

        total_junk_items -= num_goal_items

        # Add all goals from the theme to item_table
        for goal_item_name in theme_obj.goal_items:
            goal_item_code = item_names_table[goal_item_name]
            self.item_table[goal_item_name] = {
                "classification": ItemClassification.progression,
                "code": goal_item_code,
            }

        # for num_goal_items, pick a random one and add it to itempool
        for _ in range(num_goal_items):
            goal_item_name = theme_obj.choose_random_goal_item()
            goal_item = self.create_item(goal_item_name)
            itempool.append(goal_item)

        # new completion condition is that we have num_goal_items of any goal item
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has_from_list(
                theme_obj.goal_items, self.player, num_goal_items
            )
        )

        # Add Game-affecting Items
        pct_float = pct_speed_boosts / 100
        num_speed_boosts = int(total_checks * pct_float)
        # Clamp speed boosts to the number of junk items
        num_speed_boosts = min(num_speed_boosts, total_junk_items)

        # Add all speed boosts from the theme to item_table
        for speed_boost_name in theme_obj.speed_boost_items:
            speed_boost_code = item_names_table[speed_boost_name]
            self.item_table[speed_boost_name] = {
                "classification": ItemClassification.useful,
                "code": speed_boost_code,
            }

        for _ in range(num_speed_boosts):
            speed_boost_name = theme_obj.choose_random_speed_boost_item()
            speed_boost_item = self.create_item(speed_boost_name)
            itempool.append(speed_boost_item)

        total_junk_items -= num_speed_boosts

        # Add Junk items
        for junk_item_name in theme_obj.junk_items:
            junk_item_code = item_names_table[junk_item_name]
            self.item_table[junk_item_name] = {
                "classification": ItemClassification.filler,
                "code": junk_item_code,
            }

        for _ in range(total_junk_items):
            junk_item_name = theme_obj.choose_random_junk_item()
            junk_item = self.create_item(junk_item_name)
            itempool.append(junk_item)

        self.multiworld.regions.append(menu)
        self.multiworld.regions.append(hub)
        menu.connect(hub)

        # Debug prints
        # print(self.item_name_to_id)
        # print(self.location_name_to_id)
        # print(self.item_table)
        # print(itempool)
        # for r in self.multiworld.regions:
        #     print(f"{r.name} entrances:", [e for e in r.entrances])
        #     print(f"{r.name} exits:", [ex for ex in r.exits])
        #     print(f"{r.name} locations:", [loc for loc in r.locations])

        self.multiworld.itempool += itempool

    # Create Hub -> Regions entrances
    def create_regions(self) -> None:
        pass

    # Append `Item`s to self.multiworld.itempool
    def create_items(self) -> None:
        pass

    def create_item(self, name: str) -> ArchipelaPalItem:
        item = self.item_table[name]
        return ArchipelaPalItem(name, item.classification, item.code, self.player)

    def fill_slot_data(self):
        min_wait_time = self.options.min_time_between_checks.value
        max_wait_time = self.options.max_time_between_checks.value
        num_goal = self.options.num_goal_items.value
        slot_name = self.player_name
        num_regions = self.options.num_regions.value
        game_theme = self.options.game_theme.value
        chests_per_region_list = self.chests_per_region_result

        return {
            "min_wait_time": min_wait_time,
            "max_wait_time": max_wait_time,
            "num_goal": num_goal,
            "slot_name": slot_name,
            "num_regions": num_regions,
            "chests_per_region_list": chests_per_region_list,
            "game_theme": game_theme,
        }
