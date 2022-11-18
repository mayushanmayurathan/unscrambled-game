"""CSC108: Fall 2021 -- Assignment 1: Unscramble

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Tom Fairgrieve, Sadia Sharmin, and 
Jacqueline Smith.
"""

# Move constants
SHIFT = 'S'
FLIP = 'F'
CHECK = 'C'

# Constant for hint functions
HINT_MODE_SECTION_LENGTH = 3


def get_section_start(section_num: int, section_len: int) -> int:
    """Return the starting index of the section corresponding to section_num
    if the length of a section is section_len.

    >>> get_section_start(1, 3)
    0
    >>> get_section_start(2, 3)
    3
    >>> get_section_start(3, 3)
    6
    >>> get_section_start(4, 3)
    9
    """
    # Write your code for get_section_start here
    
    return section_len * (section_num - 1)    

# Write the rest of your functions here

def is_valid_move(move: str) -> bool:
    """ Return True if and only if the inputted move represents a valid move, 
         i.e. it matches one of the three move constants.
         
    >>> is_valid_move(S)
    True
    >>> is_valid_move(F)
    True
    >>> is_valid_move(Z)
    False
    """
    return move == SHIFT or move == FLIP or move == CHECK

def get_num_sections(answer_string: str, section_length: int) -> int:
    """Return the number of sections in the answer_string based on
    section_length
    
    >>> get_num_sections(appleberry, 5)
    2
    >>> get_num_sections(carbarfar, 3)
    3
    """
    return int(len(answer_string) / section_length)

def is_valid_section(section_num: int, answer_string: str, section_length: 
                     int) -> bool:
    """ Return true if and only if section_num is valid for the given
    answer_string and section_length.
    
    >>> is_valid_section(4,'csiscool', 2)
    True
    >>> is_valid_section(5,'csiscool', 2)
    False
    """
    return len(answer_string) / section_length >= section_num > 0

def check_section(game_state: str, answer: str, section_num: int, section_length
                  : int) -> bool:
    """Return true if and only if game_state matches answer for the evaluated
    section_num of section_length letters.
    
    >>> check_section('banneh', 'banhen', 1, 3)
    True
    >>> check_section('nabneh', 'banhen', 1, 3)
    False
    """
    start = get_section_start(section_num, section_length)
    end = start + section_length
    
    return game_state[start:end] == answer[start:end]

def change_section(game_state: str, move: str, section_num: int, section_length: 
                   int) -> str:
    """Return an updated game_state that reflects the move done to the specific 
    section_num of section_length letters.
    
    >>> change_section('teerkocrlkae', 'F', 2, 4)
    'teerrocklkae'
    >>> change_section('teerkocrlkae', 'S', 2, 4)
    'teerocrklkae'
    """
    start = get_section_start(section_num, section_length)
    end = start + section_length
    word = ""
    
    for i in range(len(game_state)):
        if start <= i < end:
            if i % section_length == 0:
                if move == SHIFT:   
                    word += game_state[start+1:end] + game_state[start]
                if move == FLIP:
                    word += game_state[end-1] + game_state[start+1:end-1]\
                    + game_state[start]
        else: 
            word += game_state[i]     
    return word

    # The for loop cycles through for each letter in gamestate and runs 
    # it through the conditions for moves. If the letters include those from  
    # the section we chose to manipulate, then it proceeds to the flip/shift 
    # conditions, and if not, we return them in the state they were given. At 
    # the end, we return a modified version of gamestate called word.
    
def section_needs_flip(game_state: str, answer: str, section_num: int) -> bool:
    """Return true if the player cannot rearrange game_state of the specified
    section_num to answer without conducting a flip.
    
    >>> section_needs_flip('jararb','jarbar', 2)
    False
    >>> section_needs_flip('jarrab','jarbar', 2)
    True
    """
    start = get_section_start(section_num, HINT_MODE_SECTION_LENGTH)
    end = start + HINT_MODE_SECTION_LENGTH    
    
    if game_state[start] == answer[end - 1] and game_state[start + 1] == \
       answer[start + 1]:
        return True
    elif game_state[start] == answer[start] and game_state[start + 1] == \
       answer[end - 1]: 
        return True 
    elif game_state[end - 1] == answer[end - 1] and game_state[start] == \
       answer[start + 1]:
        return True
    else: 
        return False
    # For any 3 letter word, we are brute force testing all shift combinations
    # that cannot be rearranged into the answer.
   
def get_move_hint(game_state: str, answer: str, section_num: int) -> str:
    """Return a move that will help the player rearrange game_state of the
    specified section_num closer to answer. By repeatedly following the 
    hints, the game will be solved.
    
    >>> get_move_hint('jararb','jarbar', 2)
    'SHIFT'
    >>> get_move_hint('jarrab','jarbar', 2)
    'FLIP'
    """
    if section_needs_flip(game_state,answer,section_num):
        return "FLIP"
    return "SHIFT"