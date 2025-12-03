"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Abraheem ashe

AI Usage: Chat got was used periodically for logic errors and tips on how to write some lines of code simpiler

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    inventory.remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    inventory = character.get("inventory", [])
    return item_id in inventory


def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    inventory = character.get("inventory")
    if inventory is None:
        return 0

    return inventory.count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    inventory = character.get("inventory")
    if inventory is None:
        current_size = 0
    else:
        current_size = len(inventory)

    remaining = MAX_INVENTORY_SIZE - current_size
    if remaining < 0:
        remaining = 0

    return remaining

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        return []

    removed = list(inventory)
    character["inventory"] = []
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")

    item_def = item_data
    if "type" not in item_def:
        raise InvalidItemTypeError(f"Item '{item_id}' missing type information.")

    if item_def["type"] != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not consumable.")

    effect = item_def.get("effect", "")
    stat_name, value = parse_item_effect(effect)

    apply_stat_effect(character, stat_name, value)

    inventory.remove(item_id)

    return f"Used {item_def.get('name', item_id)}: {stat_name} +{value}"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    # Must have item
    if item_id not in inventory:
        raise ItemNotFoundError(f"Weapon '{item_id}' not in inventory.")

    # Must be correct type
    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon.")

    # Ensure equipped key exists
    current_weapon = character.get("equipped_weapon")

    # If a weapon is already equipped, unequip it properly
    if current_weapon is not None:
        # Get data for currently equipped weapon
        prev_weapon_data = item_data.get("all_items", {}).get(current_weapon)
        if prev_weapon_data:
            prev_stat, prev_val = parse_item_effect(prev_weapon_data["effect"])
            character[prev_stat] = character.get(prev_stat, 0) - prev_val

        # Ensure space in inventory
        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError("No inventory space to unequip current weapon.")

        # Put the old weapon back
        inventory.append(current_weapon)

    # Equip the new weapon
    effect_string = item_data.get("effect", "")
    stat_name, value = parse_item_effect(effect_string)

    # Apply new bonus
    character[stat_name] = character.get(stat_name, 0) + value

    # Save equipped weapon
    character["equipped_weapon"] = item_id

    # Remove weapon from inventory
    inventory.remove(item_id)

    return f"Equipped {item_data.get('name', item_id)} (+{value} {stat_name})"

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Armor '{item_id}' not in inventory.")

    if item_data.get("type") != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor.")

    if "equipped_armor" not in character:
        character["equipped_armor"] = None

    current_armor = character.get("equipped_armor")
    if current_armor is not None:
        space = get_inventory_space_remaining(character)
        if space <= 0:
            raise InventoryFullError("No inventory space to unequip current armor.")

        character["equipped_armor"] = None
        inventory.append(current_armor)

    effect_string = item_data.get("effect", "")
    stat_name, value = parse_item_effect(effect_string)
    if stat_name == "max_health":
        character["max_health"] = character.get("max_health", 0) + value
        # ensure current health does not exceed new max
        if character.get("health", 0) > character["max_health"]:
            character["health"] = character["max_health"]
    else:
        character[stat_name] = character.get(stat_name, 0) + value

    character["equipped_armor"] = item_id
    inventory.remove(item_id)

    return f"Equipped {item_data.get('name', item_id)} (+{value} {stat_name})"

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    equipped = character.get("equipped_weapon")
    if equipped is None:
        return None

    space = get_inventory_space_remaining(character)
    if space <= 0:
        raise InventoryFullError("Inventory full. Cannot unequip weapon.")
    
    character["equipped_weapon"] = None
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]
    inventory.append(equipped)
    return equipped

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    equipped = character.get("equipped_armor")
    if equipped is None:
        return None

    space = get_inventory_space_remaining(character)
    if space <= 0:
        raise InventoryFullError("Inventory full. Cannot unequip armor.")

    character["equipped_armor"] = None
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]
    inventory.append(equipped)
    return equipped

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    cost = item_data.get("cost", 0)
    gold = character.get("gold", 0)
    if gold < cost:
        raise InsufficientResourcesError("Not enough gold to purchase item.")

    space = get_inventory_space_remaining(character)
    if space <= 0:
        raise InventoryFullError("Inventory is full. Cannot purchase item.")

    character["gold"] = gold - cost
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    inventory.append(item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    inventory = character.get("inventory")
    if inventory is None:
        character["inventory"] = []
        inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    inventory.remove(item_id)

    cost = item_data.get("cost", 0)
    sell_value = cost // 2
    character["gold"] = character.get("gold", 0) + sell_value
    return sell_value

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    if not effect_string:
        raise InvalidItemTypeError("Item effect string is empty.")

    if ":" not in effect_string:
        raise InvalidItemTypeError(f"Invalid effect format: '{effect_string}'")

    parts = effect_string.split(":", 1)
    stat_name = parts[0].strip()
    value_str = parts[1].strip()

    try:
        value = int(value_str)
    except Exception:
        raise InvalidItemTypeError(f"Invalid effect value: '{value_str}'")

    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    character[stat_name] = character.get(stat_name, 0) + value

    if stat_name == "health" and character["health"] > character.get("max_health", 0):
        character["health"] = character["max_health"]

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character["inventory"]

    if len(inventory) == 0:
        print("Inventory is empty.")
        return

    # Count items
    counts = {}
    for item_id in inventory:
        if item_id in counts:
            counts[item_id] += 1
        else:
            counts[item_id] = 1

    print("\n=== INVENTORY ===")
    for item_id in counts:
        item_info = item_data_dict[item_id]
        name = item_info["name"]
        itype = item_info["type"]
        qty = counts[item_id]
        

        print(f"{name} (id: {item_id}) | type: {itype} | qty: {qty}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    # 
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

