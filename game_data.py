"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Abraheem ashe

AI Usage: Chat got was used periodically for logic errors and tips on how to write some lines of code simpiler

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file '{filename}' not found.")

    quests = {}
    try:
        with open(filename, "r") as file:
            block = []
            for line in file:
                line = line.strip()
                if line == "":
                    if block:
                        quest = parse_quest_block(block)
                        quest_id = quest["quest_id"]
                        quests[quest_id] = quest
                        block = []
                else:
                    block.append(line)
            if block:
                quest = parse_quest_block(block)
                quest_id = quest["quest_id"]
                quests[quest_id] = quest
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading quest file: {e}")

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file '{filename}' not found.")
    
    items = {}
    try:
        with open(filename, "r") as file:
            block = []
            for line in file:
                line = line.strip()
                if line == "":
                    if block:
                        item = parse_item_block(block)
                        items[item["item_id"]] = item
                        block = []
                else:
                    block.append(line)
            if block:
                item = parse_item_block(block)
                items[item["item_id"]] = item
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading item file: {e}")
    
    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_keys = ["quest_id", "title", "description", "reward_xp",
                     "reward_gold", "required_level", "prerequisite"]
    for key in required_keys:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing key in quest: {key}")
    try:
        quest_dict["reward_xp"] = int(quest_dict["reward_xp"])
        quest_dict["reward_gold"] = int(quest_dict["reward_gold"])
        quest_dict["required_level"] = int(quest_dict["required_level"])
    except Exception:
        raise InvalidDataFormatError("Quest numeric fields must be integers.")
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
    for key in required_keys:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing key in item: {key}")
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    try:
        item_dict["cost"] = int(item_dict["cost"])
    except Exception:
        raise InvalidDataFormatError("Item cost must be an integer.")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    if not os.path.exists("data"):
        os.mkdir("data")
    
    quest_file = "data/quests.txt"
    if not os.path.exists(quest_file):
        with open(quest_file, "w") as f:
            f.write("QUEST_ID: first_quest\n")
            f.write("TITLE: The First Adventure\n")
            f.write("DESCRIPTION: Begin your journey.\n")
            f.write("REWARD_XP: 100\n")
            f.write("REWARD_GOLD: 50\n")
            f.write("REQUIRED_LEVEL: 1\n")
            f.write("PREREQUISITE: NONE\n\n")
    
    item_file = "data/items.txt"
    if not os.path.exists(item_file):
        with open(item_file, "w") as f:
            f.write("ITEM_ID: iron_sword\n")
            f.write("NAME: Iron Sword\n")
            f.write("TYPE: weapon\n")
            f.write("EFFECT: strength:5\n")
            f.write("COST: 100\n")
            f.write("DESCRIPTION: A basic sword for beginners.\n")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid quest line: {line}")
        key, value = line.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "quest_id":
            quest["quest_id"] = value
        elif key == "title":
            quest["title"] = value
        elif key == "description":
            quest["description"] = value
        elif key == "reward_xp":
            quest["reward_xp"] = value
        elif key == "reward_gold":
            quest["reward_gold"] = value
        elif key == "required_level":
            quest["required_level"] = value
        elif key == "prerequisite":
            quest["prerequisite"] = value
    validate_quest_data(quest)
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid item line: {line}")
        key, value = line.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "item_id":
            item["item_id"] = value
        elif key == "name":
            item["name"] = value
        elif key == "type":
            item["type"] = value
        elif key == "effect":
            item["effect"] = value
        elif key == "cost":
            item["cost"] = value
        elif key == "description":
            item["description"] = value
    validate_item_data(item)
    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    #Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

