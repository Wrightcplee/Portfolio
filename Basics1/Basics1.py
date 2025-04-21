"""
Group name: Hello World
Authors: Lee Cheng Peng, John Elisa, Jakob Binder, Lachlan Wilmot
"""

###################################     TEMPLATE    ##########################################
import time
import random


def display_rules():  
    print("""
    _____________________________________________________________________________
    Twenty One is a game of chance where players take turns rolling two dice every 
    round until they decide to stop rolling and lock in their score or end up 
    going bust with a total over 21. The objective is to be the closest to 21 
    when everyone is done rolling.

    Rules are as per follows:
        - Players begin with a score of 0.
        - Each player has one turn to either roll or stop rolling each round.
        - Players can only do a regular roll of two dice until they 
          reach a score of at least 14.
        - Players with a score >= 14 have the option to only roll one dice.
        - If a player scores more than 21 they go bust and are out of the game.
        - The winning player is the one with the score closest to 21 when everyone 
          has finished rolling.
        - If all players go bust, no one wins.
        - If more than one player has the winning score, no one wins.
    _____________________________________________________________________________
    """)
    input("Press enter to go back")
    return


def display_main_menu():                       
    print("------------Main Menu------------")
    print("Welcome to Twenty One!")
    print("1. Solo")
    print("2. Local Multiplayer")
    print("3. Rules")
    print("4. Exit")
    print("---------------------------------")


def int_input(prompt="", restricted_to=None):
    """
    Helper function that modifies the regular input method,
    and keeps asking for input until a valid one is entered. Input 
    can also be restricted to a set of integers.

    Arguments:
        - prompt: String representing the message to display for input
        - restricted: List of integers for when the input must be restricted
                    to a certain set of numbers

    Returns the input in integer type.
    """
    while True:
        player_input = input(prompt)
        try:                           
            int_player_input = int(player_input)
        except ValueError:
            continue
        if restricted_to is None:
            break
        elif int_player_input in restricted_to:
            break

    return int_player_input


def cpu_player_choice(score):
    """
    This function simply returns a choice for the CPU player based
    on their score.

    Arguments:
        - score: Int

    Returns an int representing a choice from 1, 2 or 3.
    """
    time.sleep(2)  
    if score < 14: 
        return 1
    elif score < 17: 
        return 3
    else:
        return 2
###################################     TEMPLATE    ##########################################

###################################   DISPLAY FEATURES  #####################################
def display_game_options(player):
    """
    Prints the game options depending on if a player's score is
    >= 14.
    
    Arguments:
      - player: A player dictionary object
    """
    if player['score'] >= 14:     #Players with a score >= 14 have the option to only roll one dice
        print (f"------------{player['name']}'s turn------------\n{player['name']}'s score: {player['score']}\n1. Roll\n2. Stay\n3. Roll One")
    else:                 #Players can only do a regular roll of two dice until they reach a score of at least 14
        print (f"------------{player['name']}'s turn------------\n{player['name']}'s score: {player['score']}\n1. Roll\n2. Stay")

def display_round_stats(round, players):
    """
    Print the round statistics provided a list of players.

    Arguments:
      - round: Integer for round number
      - players: A list of player-dictionary objects
    """
    print (f"-----------Round {round}-----------")     #displays the current round of the game
    for player in players:      #for loop prints the current score of every player in players
        print (f"{player['name']} is at {player['score']}")

###################################   DISPLAY FEATURES    ##########################################

###################################   DICE ROLL   ############################################
import random           # allows a way to generate random numbers with random.randint(x,y)
def roll_dice(num_of_dice=1):
    """
    Rolls dice based on num_of_dice passed as an argument.

    Arguments:
        - num_of_dice: Integer for amount of dice to roll

    Returns the following tuple: (rolls, display_string)
        - rolls: A list of each roll result as an int
        - display_string: A string combining the dice art for all rolls into one string
    """
    die_art = {
        1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
        2: ["┌─────────┐", "│  ●      │", "│         │", "│      ●  │", "└─────────┘"],
        3: ["┌─────────┐", "│  ●      │", "│    ●    │", "│      ●  │", "└─────────┘"],
        4: ["┌─────────┐", "│  ●   ●  │", "│         │", "│  ●   ●  │", "└─────────┘"],
        5: ["┌─────────┐", "│  ●   ●  │", "│    ●    │", "│  ●   ●  │", "└─────────┘"],
        6: ["┌─────────┐", "│  ●   ●  │", "│  ●   ●  │", "│  ●   ●  │", "└─────────┘"]
    }
    roll = []
    for i in range(num_of_dice):    # appends the random value of the roll into the list  
        roll.append(random.randint(1,6))
    row1 = ""                       # empty string for each row
    row2 = ""
    row3 = ""
    row4 = ""
    row5 = ""
    for i in roll:               # for the value in the list [roll], takes the value(i) and the index and adds it to corresponding rows 
        row1 += die_art.get(i)[0]
        row2 += die_art.get(i)[1]
        row3 += die_art.get(i)[2]
        row4 += die_art.get(i)[3]
        row5 += die_art.get(i)[4]
    display_string = f"{row1}\n{row2}\n{row3}\n{row4}\n{row5}\n"   #Variable that holds the art of the dice.
    return (roll,display_string)


###################################   DICE ROLL   ############################################

###################################   EXECUTE TURN    ##########################################
def execute_turn(player, player_input):
    """
    Executes one turn of the round for a given player.

    Arguments:
      - player: A player dictionary object

    Returns an updated player dictionary object.
    """
    if player_input == 2:           #if a player chooses option 2, his score stays
        print (f"{player['name']} has stayed with a score of {player['score']}")
        player['stayed'] = True
    elif player_input == 1:         #if a player chooses option 1, he rolls the dice twice
        result = roll_dice(2)
        player['score'] += sum(result[0])
        print (f"Rolling both...\n{result[1]}\n{player['name']} is now on {player['score']}")
    elif player_input == 3:         #if a player chooses option 3, he rolls the dice once 
        result = roll_dice(1)
        player['score'] += sum(result[0])
        print (f"Rolling one...\n{result[1]}\n{player['name']} is now on {player['score']}")
    if player['score'] > 21:        #if a player scores more than 21, he goes bust
        player['at_14'] = True
        player['bust'] = True
        print(f"{player['name']} goes bust!")
    elif player['score'] >= 14:     #if a player scores more than 14, he is eligible to roll the dice once in the next round
        player['at_14'] = True
    return player

###################################  EXECUTE TURN END   ########################################

###################################   END GAME CHECK  ##########################################
def end_of_game(players):  # this is the function that is to be called when all players are either bust or stayed
    """
    Takes the list of all players and determines if the game has finished,
    returning false if not else printing the result before returning true.

    Arguments:
      - players: A list of player-dictionary objects

    Returns True if round has ended or False if not. If true results are
    printed before return.
    """
    for player in players:  
        if player['bust'] == False and player['stayed'] == False:  # this signify's the game is not finished by returning false given these conditions 
            return False
    score = []            
    for player in players:  # for every player's score that is not bust, appends to score
        if player['bust'] == False:        
            score.append(player['score'])
    if len(score) == 0:         #if every player goes bust and no score gets added, it prints the sentence below
        print("Everyone's gone bust! No one wins :(")
    else:
        highest_score = max(score)  # this statement returns the highest score and stores them to this variable
        if score.count(highest_score) >= 2:  # if there are more than two numbers in the variable score than it is deemed that there has been a draw
            print ("The game is a draw! No one wins :(") 
        else:  # this is if there is only one number in the highest score variable
            for player in players:
                if player['score'] == highest_score:  # this is to select the winning players score, ensuring the correct name is matched to the score
                    print (f"{player['name']} is the winner!")
    return True        # this return true is as instructed to say that the game is finished 

#################################  END GAME CHECK  ############################################

################################  SOLO GAME   ###################################################

def solo_game():
    """
    This function defines a game loop for a solo game of Twenty One against 
    AI.
    """
    player1 = {'name': 'Player 1', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}      #sets everything on default for the player1
    bot = {'name': 'CPU Player', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}        #sets everything on default for the bot 
    players = [player1, bot]
    round = 0
    player1['name'] = input("Please enter Player name: ")
    while end_of_game(players) == False:                              #while loop iterates as long as the game has not ended                     
        display_round_stats(round,players)
        if player1['stayed'] == False and player1['bust'] == False:   #if condition checks whether the player is still eligible to roll the dice
            display_game_options(player1)
            player_input = 0
            if player1['at_14'] == False:                             #if condition checks whether the player's score is more than 14
                while player_input not in (1,2):
                    player_input = int_input("")
            else:                                                     #iterates if player's score is more than 14
                while player_input not in (1,2,3):
                    player_input = int_input("")
            execute_turn(player1,player_input)
        if bot['stayed'] == False and bot['bust'] == False:           #if condition checks whether the bot is still playing
            display_game_options(bot)
            execute_turn(bot,cpu_player_choice(bot['score']))          #cpu function that is provided
        round += 1


################################  SOLO GAME   ###################################################

############################### MULTIPLAYER GAME  ###########################################

def multiplayer_game(num_of_players):
    """
    This function defines a game loop for a local multiplayer game of Twenty One, 
    where each iteration of the while loop is a round within the game. 
    """
    players = []
    for i in range(num_of_players):                                   #for loop takes the player's default dictionary at the start of the game and adds it to the list
        i = {'name': 'Player', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}
        players.append(i)
    for player in players:                                            #for loop asks for the players names and adds them to the dictionary value
        player['name'] = input(f"Please enter Player {players.index(player)+1}'s name: ")
    round = 0
    while end_of_game(players) == False:                              #while loop iterates as long as the game has not ended 
        display_round_stats(round,players)
        for player in players:                                        #one round of game
            if player['stayed'] == False and player['bust'] == False: #if condition checks whether the player is still eligible to roll the dice
                display_game_options(player)
                player_input = 0
                if player['at_14'] == False:                          #if condition checks whether the player's score is more than 14
                    while player_input not in (1,2):
                        player_input = int_input("")
                else:                                                 #iterates if player's score is more than 14
                    while player_input not in (1,2,3):
                        player_input = int_input("")
                execute_turn(player,player_input)
        round += 1

############################### MULTIPLAYER GAME  ###########################################

###################################    MAIN MENU DONE    #######################################
def main():
    """
    Defines the main loop that allows the player to start a game, view rules or quit.
    """
    while True:                                                       #the while loop is continually met as the condition is set to true
        display_main_menu() 
        print("Please make a choice: 1 / 2 / 3 / 4")
        ans = input('> ')
        if ans == "1":                                                #if statement iterates when player chooses to play the Solo Game
            while True:
                print("Start Solo Game? Y / N")    
                ans_1 = input('> ')
                if ans_1 == "Y" or ans_1 == "y":                      #if a player confirms with an input of Y or y, it starts the Solo Game
                    print("Solo Game starts, have fun!")              #it leaves the while loop and starts the Solo Game
                    solo_game()                                             
                    break                                               
                if ans_1 == "N" or ans_1 == "n":                      #if a player rejects to start the Solo Game, it return back to the main menu 
                    break                      
        if ans == "2":                                                #if statement iterates when player chooses to play the Multiplayer Game
            while True:
                print("Start Mulitplayer Game? Y / N")
                ans_2 = input('> ')
                if ans_2 == "Y" or ans_2 == "y":                      #if a player confirms with an input of Y or y, it starts the Multiplayer Game
                    print("Local Multiplayer Game starts")
                    num_of_players = int_input("Please enter the number of players: ")
                    while num_of_players <= 0:
                        num_of_players = int_input("Please key in a number more than 0\nPlease enter the number of players: ")
                    print("Multiplayer Game with", num_of_players, "players starts!")
                    multiplayer_game(num_of_players)
                    break
                if ans_2 == "N" or ans_2 == "n":
                    break
        if ans == "3":                                                #if statement iterates when player chooses to display the rules
            display_rules()
        if ans == "4":                                                #if statement iterates when player chooses to leave the game
            print("We hope you enjoyed playing Twenty One!")
            return
###################################   MAIN MENU DONE    #######################################

main()  # to call the main function and have the program run
