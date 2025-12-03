"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Abraheem Ashe

AI Usage: Chat got was used periodically for logic errors and tips on how to write some lines of code simpiler

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    while True:
        choice = input("Enter choice (1-3): ")
        try:
            num = int(choice)
            if 1 <= num <= 3:
                return num
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1-3).")
    

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("=== CREATE NEW CHARACTER ===")
    name = input("Enter character name: ")

    print("Choose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_choice = input("Select (1-4): ")

    try:
        class_num = int(class_choice)
    except ValueError:
        print("Please enter a valid number.")
        return new_game()

    if class_num not in (1, 2, 3, 4):
        print("Please enter a number between 1 and 4.")
        return new_game()

    class_map = {1: "Warrior", 2: "Mage", 3: "Rogue", 4: "Cleric"}
    class_name = class_map[class_num]

    try:
        character = character_manager.create_character(name, class_name)
    except InvalidCharacterClassError:
        print("ERROR: Invalid character class.")
        return new_game()

    character_manager.save_character(character)
    current_character = character
    print(f"\nCharacter '{name}' the {class_name} created successfully!")
    print("Starting your adventure...\n")
    game_loop() 

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    print("=== LOAD EXISTING CHARACTER ===")

    try:
        saved_names = character_manager.list_saved_characters()
    except Exception as no_save:
        print(f"Error retrieving saved characters: {no_save}")
        return

    if not saved_names:
        print("No saved characters found. Please start a new game first.")
        return

    print("Saved characters:")
    for idx, name in enumerate(saved_names, 1):
        print(f"{idx}. {name}")

    choice = input(f"Select a character to load (1-{len(saved_names)}): ")
    try:
        selected_index = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return load_game()

    if not (1 <= selected_index <= len(saved_names)):
        print(f"Please enter a number between 1 and {len(saved_names)}.")
        return load_game()

    selected_name = saved_names[selected_index - 1]

    try:
        character = character_manager.load_character(selected_name)
    except CharacterNotFoundError:
        print(f"ERROR: Character '{selected_name}' not found.")
        return load_game()
    except SaveFileCorruptedError:
        print(f"ERROR: Save file for '{selected_name}' is corrupted.")
        return load_game()

    current_character = character
    print(f"\nCharacter '{current_character['name']}' loaded successfully!")
    print("Resuming your adventure...\n")
    game_loop()

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False

        if game_running:
            save_game()

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    while True:
        print("\n=== GAME MENU ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        choice = input("Select an option (1-6): ")
        try:
            choice_num = int(choice)
        except ValueError:
            print("Please enter a valid number (1-6).")
            continue

        if 1 <= choice_num <= 6:
            return choice_num
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    stats = character_manager.get_character_stats(current_character)

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {stats['name']}")
    print(f"Class: {stats['class']}")
    print(f"Level: {stats['level']}")
    print(f"Max Health: {stats['max_health']}")
    print(f"Strength: {stats['strength']}")
    print(f"Magic: {stats['magic']}")
    print(f"Gold: {stats['gold']}")

    active_quests = quest_handler.get_active_quests(current_character)
    completed_quests = quest_handler.get_completed_quests(current_character)

    print("\nActive Quests:")
    if active_quests:
        for quest in active_quests:
            print(f"- {quest.name}: {quest.description}")
    else:
        print("None")

    print("\nCompleted Quests:")
    if completed_quests:
        for quest in completed_quests:
            print(f"- {quest.name}")
    else:
        print("None")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    inventory = current_character['inventory']

    print("\n=== INVENTORY ===")
    if not inventory:
        print("Your inventory is empty.")
        return

    for idx, item_name in enumerate(inventory, 1):
        print(f"{idx}. {item_name}")

    choice = input(f"Select an item (1-{len(inventory)}) or 0 to exit: ")
    try:
        choice_num = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return

    if choice_num == 0:
        return
    if not (1 <= choice_num <= len(inventory)):
        print("Invalid item selection.")
        return

    selected_item_name = inventory[choice_num - 1]
    print(f"Selected Item: {selected_item_name}")

    print("Item Options:")
    print("1. Use Item")
    print("2. Equip Item")
    print("3. Drop Item")
    print("4. Cancel")

    action = input("Choose an action (1-4): ")
    try:
        action_num = int(action)
    except ValueError:
        print("Please enter a valid action number.")
        return

    try:
        if action_num == 1:
            inventory_system.use_item(current_character, selected_item_name)
            print(f"You used {selected_item_name}.")
        elif action_num == 2:
            inventory_system.equip_item(current_character, selected_item_name)
            print(f"You equipped {selected_item_name}.")
        elif action_num == 3:
            inventory_system.remove_item(current_character, selected_item_name)
            print(f"You dropped {selected_item_name}.")
        elif action_num == 4:
            print("Canceled.")
        else:
            print("Invalid action.")
    except InventoryError as e:
        print(f"ERROR: {e}")


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

    while True:
        print("=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest")
        print("7. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            active = quest_handler.get_active_quests(current_character)
            print("--- Active Quests ---")
            if not active:
                print("No active quests.")
            else:
                for quest in active:
                    print(f"{quest.name} - {quest.description}")

        elif choice == "2":
            available = quest_handler.get_available_quests(current_character, all_quests)
            print("--- Available Quests ---")
            if not available:
                print("No available quests.")
            else:
                for quest in available:
                    print(f"{quest.quest_id}. {quest.name} - {quest.description}")

        elif choice == "3":
            completed = quest_handler.get_completed_quests(current_character)
            print("--- Completed Quests ---")
            if not completed:
                print("No completed quests.")
            else:
                for quest in completed:
                    print(f"{quest.name}")

        elif choice == "4":
            available = quest_handler.get_available_quests(current_character, all_quests)
            if not available:
                print("No quests available to accept.")
                continue

            print("--- Accept Quest ---")
            for quest in available:
                print(f"{quest.quest_id}. {quest.name}")

            quest_id = input("Enter quest ID to accept: ")

            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print("Quest accepted!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            active = quest_handler.get_active_quests(current_character)
            if not active:
                print("No active quests to abandon.")
                continue

            print("\n--- Abandon Quest ---")
            for quest in active:
                print(f"{quest.quest_id}. {quest.name}")

            quest_id = input("Enter quest ID to abandon: ")

            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print("Quest abandoned.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "6":
            active = quest_handler.get_active_quests(current_character)
            if not active:
                print("No quest to complete.")
                continue

            print("--- Complete Quest ---")
            for quest in active:
                print(f"{quest.quest_id}. {quest.name}")

            quest_id = input("Enter quest ID to complete: ")

            try:
                quest_handler.complete_quest(current_character, quest_id)
                print("Quest completed!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "7":
            break

        else:
            print("Invalid choice.")


def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    print("=== EXPLORING... ===")

    try:
        enemy = game_data.generate_enemy(current_character['level'])
    except Exception as e:
        print(f"Error generating enemy: {e}")
        return

    print(f"A wild {enemy['name']} appears!")

    try:
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start()
    except Exception as e:
        print(f"Combat error: {e}")
        return

    if result.get("dead"):
        handle_character_death()
        return

    xp = result.get("xp", 0)
    gold = result.get("gold", 0)
    current_character['xp'] += xp
    current_character['gold'] += gold

    print(f"Victory! You earned {xp} XP and {gold} gold.")

    try:
        character_manager.save_character(current_character)
    except Exception as e:
        print(f"Error saving after battle: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    while True:
        print("\n=== SHOP ===")
        print("1. Buy Items")
        print("2. Sell Items")
        print("3. Back")
        choice = input("Select an option (1-3): ")

        try:
            choice_num = int(choice)
        except ValueError:
            print("Please enter a valid number (1-3).")
            continue

        if choice_num == 1:
            print("\nAvailable items for purchase:")
            for idx, item_name in enumerate(all_items.keys(), 1):
                item = all_items[item_name]
                print(f"{idx}. {item_name} - Cost: {item['cost']} gold")
            buy_choice = input(f"Select an item to buy (1-{len(all_items)}): ")
            try:
                buy_index = int(buy_choice)
                if 1 <= buy_index <= len(all_items):
                    item_name = list(all_items.keys())[buy_index - 1]
                    item = all_items[item_name]
                    if current_character['gold'] >= item['cost']:
                        current_character['gold'] -= item['cost']
                        current_character['inventory'].append(item_name)
                        print(f"Bought {item_name}! Remaining gold: {current_character['gold']}")
                    else:
                        raise InsufficientResourcesError(f"Not enough gold to buy {item_name}.")
                else:
                    raise InvalidItemTypeError("Invalid item selection.")
            except ValueError:
                print("Please enter a valid number.")
            except (InsufficientResourcesError, InvalidItemTypeError) as e:
                print(f"ERROR: {e}")

        elif choice_num == 2:
            if not current_character['inventory']:
                print("You have no items to sell.")
                continue
            print("\nYour inventory:")
            for idx, item_name in enumerate(current_character['inventory'], 1):
                print(f"{idx}. {item_name}")
            sell_choice = input(f"Select an item to sell (1-{len(current_character['inventory'])}): ")
            try:
                sell_index = int(sell_choice)
                if 1 <= sell_index <= len(current_character['inventory']):
                    item_name = current_character['inventory'].pop(sell_index - 1)
                    if item_name not in all_items:
                        raise ItemNotFoundError(f"Item {item_name} not found in shop database.")
                    sell_value = all_items[item_name]['cost'] // 2
                    current_character['gold'] += sell_value
                    print(f"Sold {item_name} for {sell_value} gold. Total gold: {current_character['gold']}")
                else:
                    raise InvalidItemTypeError("Invalid item selection.")
            except ValueError:
                print("Please enter a valid number.")
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(f"ERROR: {e}")

        elif choice_num == 3:
            print("Leaving the shop.")
            break
        else:
            print("Please select a number between 1 and 3.")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)
        print(f"Game saved for {current_character['name']}.")
    except Exception as e:
        raise InvalidSaveDataError(f"Failed to save game for {current_character['name']}: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    try:
        all_quests = game_data.load_quests()
    except FileNotFoundError:
        try:
            game_data.create_default_data_files()
            all_quests = game_data.load_quests()
        except Exception:
            raise MissingDataFileError("Failed to create or load default quest data.")
    except ValueError:
        raise InvalidDataFormatError("Quest data file is corrupted or formatted incorrectly.")

    try:
        all_items = game_data.load_items()
    except FileNotFoundError:
        try:
            game_data.create_default_data_files()
            all_items = game_data.load_items()
        except Exception:
            raise MissingDataFileError("Failed to create or load default item data.")
    except ValueError:
        raise InvalidDataFormatError("Item data file is corrupted or formatted incorrectly.")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print(f"{current_character['name']} has fallen in battle!")
    choice = input("Do you want to revive (costs gold) or quit? [revive/quit]: ")

    if choice == "revive":
        try:
            character_manager.revive_character(current_character)
            print(f"{current_character['name']} has been revived!")
        except InsufficientResourcesError as e:
            print(f"Cannot revive: {e}")
            game_running = False
    elif choice == "quit":
        print("Game over. Returning to main menu.")
        game_running = False
    else:
        print("Invalid choice. Automatically quitting.")
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

