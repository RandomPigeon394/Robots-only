import random

# --- Character Class ---
class Character:
    """
    This class represents the player character in the game. The character has attributes
    like health, strength, agility, and magic. The class also includes methods for combat 
    actions (attack, magic, heal) and checking the player's survival.
    """
    
    def __init__(self, name, char_class):
        """
        Initializes a new player character with the given name and class.

        Args:
            name (str): The name of the character.
            char_class (str): The character's chosen class (e.g., 'Warrior', 'Mage', 'Rogue').
        """
        self.name = name
        self.char_class = char_class
        self.health = 100  # Player starts with 100 health points
        self.strength = 0  # Placeholder strength, to be set by class
        self.agility = 0   # Placeholder agility, to be set by class
        self.magic = 0     # Placeholder magic, to be set by class
        self.inventory = []  # List of items the player carries

        # Call to set class-specific attributes (strength, agility, magic)
        self.set_class_attributes()

    def set_class_attributes(self):
        """
        Sets the player character's attributes based on their chosen class.
        Each class has different starting attributes that affect gameplay.

        Classes:
            Warrior: High strength, low magic.
            Mage: High magic, low strength.
            Rogue: Balanced with high agility.
        """
        if self.char_class == "Warrior":
            self.strength = 15
            self.agility = 5
            self.magic = 2
        elif self.char_class == "Mage":
            self.strength = 5
            self.agility = 10
            self.magic = 20
        elif self.char_class == "Rogue":
            self.strength = 10
            self.agility = 15
            self.magic = 5
        else:
            raise ValueError("Invalid character class.")  # If an invalid class is chosen, raise an error.

    def is_alive(self):
        """
        Checks whether the character is still alive based on their health.

        Returns:
            bool: True if health > 0, else False.
        """
        return self.health > 0

    def attack(self, enemy):
        """
        Performs a basic attack on an enemy. The attack's damage is calculated randomly 
        and is affected by the player's strength.

        Args:
            enemy (Enemy): The enemy object that the player is attacking.

        Returns:
            int: The amount of damage dealt to the enemy.
        """
        damage = random.randint(5, 10) + self.strength // 2
        enemy.health -= damage  # Decrease enemy health by damage dealt
        return damage

    def use_magic(self, enemy):
        """
        Uses a magical attack on the enemy. The damage is calculated based on the player's magic points.
        The player must have magic points available to use this action.

        Args:
            enemy (Enemy): The enemy object that the player is attacking with magic.

        Returns:
            int: The amount of damage dealt by the magic, or 0 if the player has no magic left.
        """
        if self.magic > 0:
            damage = random.randint(10, 20) + self.magic
            enemy.health -= damage
            self.magic -= 5  # Using magic consumes 5 magic points
            return damage
        else:
            return 0  # If no magic left, return 0 damage

    def heal(self):
        """
        Heals the player by a random amount. The healing value is between 10 and 20 HP.

        Returns:
            int: The amount of health restored.
        """
        healing = random.randint(10, 20)
        self.health += healing  # Increase health by the healing amount
        return healing

    def display_stats(self):
        """
        Displays the current stats of the player character, including health, strength, agility, and magic.

        Returns:
            str: A string containing the player's name, class, and stats.
        """
        return f"{self.name} ({self.char_class}) - Health: {self.health}, Strength: {self.strength}, Agility: {self.agility}, Magic: {self.magic}"


# --- Enemy Class ---
class Enemy:
    """
    Represents an enemy that the player may encounter during the game. The enemy has health,
    strength, and attack abilities, and will engage in combat with the player character.
    """
    
    def __init__(self, name, health, strength):
        """
        Initializes a new enemy with the given name, health, and strength.

        Args:
            name (str): The name of the enemy.
            health (int): The enemy's health points.
            strength (int): The enemy's strength, affecting its attack power.
        """
        self.name = name
        self.health = health
        self.strength = strength

    def attack(self, player):
        """
        The enemy attacks the player. The damage is calculated randomly and is influenced by the enemy's strength.

        Args:
            player (Character): The player character being attacked.

        Returns:
            int: The amount of damage dealt to the player.
        """
        damage = random.randint(5, 10) + self.strength // 2
        player.health -= damage  # Decrease player's health
        return damage

    def is_alive(self):
        """
        Checks whether the enemy is still alive based on their health.

        Returns:
            bool: True if health > 0, else False.
        """
        return self.health > 0


# --- Game Locations (World Expansion) ---
class Location:
    """
    Represents a location in the game world. Each location has its own story, encounters,
    and choices the player must make.
    """
    
    def __init__(self, name, description, enemies, story_choice, outcomes):
        """
        Initializes a location in the game with a name, description, potential enemies, 
        and the player's choices.

        Args:
            name (str): The name of the location (e.g., 'Haunted Forest').
            description (str): A brief description of the location.
            enemies (list): A list of enemies that might appear in this location.
            story_choice (str): A decision the player must make in this location.
            outcomes (dict): A dictionary of possible outcomes based on the player's decision.
        """
        self.name = name
        self.description = description
        self.enemies = enemies
        self.story_choice = story_choice
        self.outcomes = outcomes  # Map choices to outcomes (actions to perform)

    def enter(self, player):
        """
        The player enters this location and faces challenges, fights enemies, 
        and makes a decision that affects the story.

        Args:
            player (Character): The player character entering this location.
        """
        print(f"\nYou have entered {self.name}: {self.description}")
        
        # Randomly encounter enemies from the list
        if self.enemies:
            enemy = random.choice(self.enemies)
            print(f"\nA wild {enemy.name} appears!")
            while enemy.is_alive() and player.is_alive():
                action = input("Choose an action (Attack / Magic / Heal): ").lower()
                if action == "attack":
                    damage = player.attack(enemy)
                    print(f"You attacked the {enemy.name} for {damage} damage.")
                elif action == "magic":
                    damage = player.use_magic(enemy)
                    if damage > 0:
                        print(f"You cast a spell on the {enemy.name} for {damage} damage!")
                    else:
                        print("You have no magic left!")
                elif action == "heal":
                    healing = player.heal()
                    print(f"You healed yourself for {healing} HP.")
                else:
                    print("Invalid action. Try again.")
                
                if enemy.is_alive():
                    damage = enemy.attack(player)
                    print(f"The {enemy.name} attacked you for {damage} damage.")
                else:
                    print(f"You defeated the {enemy.name}!")
                    break
            
        # Make a decision based on story choice
        print(f"\n{self.story_choice}")
        choice = input("What will you do? ").lower()

        if choice in self.outcomes:
            self.outcomes[choice](player)
        else:
            print("Invalid choice. The story has taken an unexpected turn.")

# --- Game Functions ---
def start_game():
    """
    Starts the game by creating the player character. The player will choose their name
    and character class. The class will determine the character's starting attributes.

    Returns:
        Character: The player character object.
    """
    print("Welcome to the RPG Game!")
    name = input("Enter your character's name: ")  # Prompt for player name
    print("\nChoose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        char_class = "Warrior"
    elif choice == "2":
        char_class = "Mage"
    elif choice == "3":
        char_class = "Rogue"
    else:
        print("Invalid choice, defaulting to Warrior.")  # Fallback if an invalid class is chosen
        char_class = "Warrior"

    player = Character(name, char_class)  # Create the player character
    print(f"\nCharacter created: {player.display_stats()}")  # Show player stats
    return player


def bad_ending(player):
    """
    The bad ending of the game. The player is defeated or makes poor choices.
    """
    print("\nYou have failed the kingdom. The evil forces have won, and all hope is lost.")
    player.health = 0


def good_ending(player):
    """
    The good ending of the game. The player defeats the main antagonist and saves the kingdom.
    """
    print("\nCongratulations! You have defeated the dark forces and saved the kingdom!")
    player.health = 100


def main():
    """
    Main game loop. The game starts here and leads the player through the adventure.
    The player will create their character, face challenges, and decide their fate.

    """
    player = start_game()  # Start the game and create the player
    
    # Game world locations and branching paths
    haunted_forest = Location(
        "Haunted Forest", 
        "A dark and eerie forest filled with spirits and dangers.", 
        [Enemy("Ghost", 30, 5), Enemy("Zombie", 50, 8)], 
        "You encounter a spooky figure. Do you approach it or run?", 
        {
            "approach": lambda p: print("You approach and find a treasure chest!"),
            "run": lambda p: print("You run away, but an enemy attacks you.")
        }
    )
    
    enchanted_castle = Location(
        "Enchanted Castle",
        "A majestic castle, rumored to be filled with magical beings.",
        [Enemy("Sorcerer", 100, 20)],
        "The castle's doors are locked. Will you try to pick the lock or knock?",
        {
            "pick the lock": lambda p: print("You successfully pick the lock and enter."),
            "knock": lambda p: print("A guard opens the door and attacks!")
        }
    )
    
    # Simulate player progressing through the world
    haunted_forest.enter(player)
    enchanted_castle.enter(player)

    # Determine ending
    if player.is_alive():
        good_ending(player)  # Player succeeds
    else:
        bad_ending(player)  # Player fails


# Entry point of the program
if __name__ == "__main__":
    main()