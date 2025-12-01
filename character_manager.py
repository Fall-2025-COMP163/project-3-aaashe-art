"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)
SAVE_DIR = "saves"
# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    base_stats = {
        'Warrior': {'health': 120, 'strength': 15, 'magic': 5},
        'Mage': {'health': 80, 'strength': 8, 'magic': 20},
        'Rogue': {'health': 90, 'strength': 12, 'magic': 10},
        'Cleric': {'health': 100, 'strength': 10, 'magic': 15}
    }

    if character_class not in base_stats:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    stats = base_stats[character_class]

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
        "equipped_weapon": None,
        "equipped_armor": None
    }
    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w") as f:
        f.write(f"name:{character['name']}\n")
        f.write(f"class:{character['class']}\n")
        f.write(f"level:{character['level']}\n")
        f.write(f"health:{character['health']}\n")
        f.write(f"max_health:{character['max_health']}\n")
        f.write(f"strength:{character['strength']}\n")
        f.write(f"magic:{character['magic']}\n")
        f.write(f"experience:{character['experience']}\n")
        f.write(f"gold:{character['gold']}\n")
        f.write(f"inventory:{','.join(character['inventory'])}\n")
        f.write(f"active_quests:{','.join(character['active_quests'])}\n")
        f.write(f"completed_quests:{','.join(character['completed_quests'])}\n")
        f.write(f"equipped_weapon:{character.get('equipped_weapon')}\n")
        f.write(f"equipped_armor:{character.get('equipped_armor')}\n")

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save found for character '{character_name}'")

    character = {}
    with open(filepath, "r") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            if key in ["inventory", "active_quests", "completed_quests"]:
                if value:
                    character[key] = value.split(",")
                else:
                    character[key] = []
            elif key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
                character[key] = int(value)
            else:
                character[key] = value

    return character
def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(SAVE_DIR):
        return []

    files = os.listdir(SAVE_DIR)
    saved_characters = []
    for file in files:
        if file.endswith("_save.txt"):
            saved_characters.append(file.replace("_save.txt", ""))
    return saved_characters

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(SAVE_DIR, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save found for character '{character_name}'")

    os.remove(filepath)

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if character["health"] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead.")

    character["experience"] += xp_amount

    level_up_xp = character["level"] * 100
    while character["experience"] >= level_up_xp:
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        level_up_xp = character["level"] * 100
    
def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError("Not enough gold.")
    character["gold"] = new_gold
    return character["gold"]

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    if character["health"] <= 0:
        return 0
    old_health = character["health"]
    character["health"] += amount
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]
    return character["health"] - old_health

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    return character["health"] <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if character["health"] > 0:
        return False
    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_keys = ["name", "class", "level", "health", "max_health",
                     "strength", "magic", "experience", "gold",
                     "inventory", "active_quests", "completed_quests"]

    for rk in required_keys:
        if rk not in character:
            raise InvalidSaveDataError(f"Missing field: {rk}")

    for key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        if type(character[key]) != int:
            raise InvalidSaveDataError(f"Field {key} must be an integer.")

    for key in ["inventory", "active_quests", "completed_quests"]:
        if type(character[key]) != list:
            raise InvalidSaveDataError(f"Field {key} must be a list.")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    #Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
    
    #Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    #Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")

