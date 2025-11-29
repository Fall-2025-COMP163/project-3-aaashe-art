"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Abraheem Ashe

AI Usage: [Document any AI assistance used]

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
    print("\n=== CREATE NEW CHARACTER ===")

    name = input("Enter character name: ")

    print("\nChoose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_choice = input("Select (1-4): ")

    try:
        class_num = int(class_choice)
    except ValueError:
        print("Please enter a valid number.")
        return new_game(character_manager)

    if class_num not in (1, 2, 3, 4):
        print("Please enter a number between 1 and 4.")
        return new_game(character_manager)

    if class_num == 1:
        class_name = "Warrior"
    elif class_num == 2:
        class_name = "Mage"
    elif class_num == 3:
        class_name = "Rogue"
    elif class_num == 4:
        class_name = "Cleric"

    try:
        character = character_manager.create_character(name, class_name)
    except InvalidCharacterClassError:
        print("ERROR: Invalid character class.")
        return new_game(character_manager)

    character_manager.save_character(character)

    print(f"\nCharacter '{name}' the {class_name} created successfully!")
    print("Starting your adventure...\n")
    game_loop(character)

    return character

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
    print("\n=== LOAD EXISTING CHARACTER ===")

    try:
        saved_names = character_manager.list_saved_characters()
    except Exception as no_save:
        print(f"Error retrieving saved characters: {no_save}")
        return

    if not saved_names:
        print("No saved characters found. Please start a new game first.")
        return

    print("\nSaved characters:")
    for save_chars, name in enumerate(saved_names, 1):
        print(f"{save_chars}. {name}")

    choice = input(f"Select a character to load (1-{len(saved_names)}): ")

    try:
        selected_index = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return load_game(character_manager)

    if not (1 <= selected_index <= len(saved_names)):
        print(f"Please enter a number between 1 and {len(saved_names)}.")
        return load_game(character_manager)

    selected_name = saved_names[selected_index - 1]

    try:
        character = character_manager.load_character(selected_name)
    except CharacterNotFoundError:
        print(f"ERROR: Character '{selected_name}' not found.")
        return load_game(character_manager)
    except SaveFileCorruptedError:
        print(f"ERROR: Save file for '{selected_name}' is corrupted.")
        return load_game(character_manager)

    current_character = character
    print(f"\nCharacter '{character.name}' loaded successfully!")
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

        if choice_num == 1:
            view_character_stats()
        elif choice_num == 2:
            view_inventory()
        elif choice_num == 3:
            quest_menu()
        elif choice_num == 4:
            explore()
        elif choice_num == 5:
            shop()
        elif choice_num == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False
        else:
            print("Invalid choice. Please select a number between 1 and 6.")
            continue

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
    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    pass

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

