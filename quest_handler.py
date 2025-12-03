"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Abraheem ashe

AI Usage: Chat got was used periodically for logic errors and tips on how to write some lines of code simpiler

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest = quest_data_dict[quest_id]
    
    if character.get("level", 1) < quest.get("required_level", 1):
        raise InsufficientLevelError(f"Level too low to accept quest '{quest_id}'.")
    
    prerequisite = quest.get("prerequisite", "NONE")
    if prerequisite != "NONE" and prerequisite not in character.get("completed_quests", []):
        raise QuestRequirementsNotMetError(f"Prerequisite '{prerequisite}' not completed.")
    
    if quest_id in character.get("completed_quests", []):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed.")
    
    if quest_id in character.get("active_quests", []):
        return False  
    
    character.setdefault("active_quests", []).append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    quest = quest_data_dict[quest_id]
    
    # Remove from active quests
    character["active_quests"].remove(quest_id)
    # Add to completed quests
    character.setdefault("completed_quests", []).append(quest_id)
    
    # Grant rewards
    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)
    
    character["experience"] = character.get("experience", 0) + xp
    character["gold"] = character.get("gold", 0) + gold
    
    return {"xp_gained": xp, "gold_gained": gold}

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    character["active_quests"].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_list = []
    for quest_id in character.get("active_quests", []):
        if quest_id in quest_data_dict:
            active_list.append(quest_data_dict[quest_id])
    return active_list

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_list = []
    for quest_id in character.get("completed_quests", []):
        if quest_id in quest_data_dict:
            completed_list.append(quest_data_dict[quest_id])
    return completed_list

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available = []
    for quest_id, quest in quest_data_dict.items():
        # Skip if already completed or active
        if quest_id in character.get("completed_quests", []):
            continue
        if quest_id in character.get("active_quests", []):
            continue
        
        # Check level requirement
        if character.get("level", 1) < quest.get("required_level", 1):
            continue
        
        # Check prerequisite
        prereq = quest.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in character.get("completed_quests", []):
            continue
        
        # Quest is available
        available.append(quest)
    
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character.get("completed_quests", [])

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character.get("active_quests", [])

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    
    # Level requirement
    if character.get("level", 1) < quest.get("required_level", 1):
        return False
    
    # Already completed
    if quest_id in character.get("completed_quests", []):
        return False
    
    # Already active
    if quest_id in character.get("active_quests", []):
        return False
    
    # Prerequisite
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character.get("completed_quests", []):
        return False
    
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    chain = []
    current = quest_id
    
    while current != "NONE":
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current}' not found in prerequisite chain.")
        chain.append(current)  # append to the end
        prereq = quest_data_dict[current].get("prerequisite", "NONE")
        if prereq == current:
            break  
        current = prereq
    
    chain.reverse()  
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0  # avoid division by zero
    
    completed_quests = len(character.get("completed_quests", []))
    percentage = (completed_quests / total_quests) * 100
    return percentage

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0
    
    for quest_id in character.get("completed_quests", []):
        quest = quest_data_dict.get(quest_id)
        if quest:
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)
    
    return {"total_xp": total_xp, "total_gold": total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    result = []
    
    for quest_id, quest in quest_data_dict.items():
        level_req = quest.get("required_level", 1)
        if min_level <= level_req <= max_level:
            result.append(quest)
    
    return result

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}")
    
    prereq = quest_data.get("prerequisite", "NONE")
    if prereq == "NONE":
        print("Prerequisite: None")
    else:
        print(f"Prerequisite: {prereq}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("No quests to display.")
        return

    print("\n=== Quest List ===")
    for quest in quest_list:
        print(f"- {quest['title']} | Level: {quest['required_level']} | "
              f"XP: {quest['reward_xp']} | Gold: {quest['reward_gold']}")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    active_count = len(character.get("active_quests", []))
    completed_count = len(character.get("completed_quests", []))
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print("\n=== Quest Progress ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {completion_percentage:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite", "NONE")
        
        if prereq != "NONE":
            if prereq not in quest_data_dict:
                raise QuestNotFoundError(f"Quest '{quest_id}' has invalid prerequisite '{prereq}'.")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    #
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    #
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

