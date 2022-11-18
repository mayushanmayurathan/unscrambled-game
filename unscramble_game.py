"""CSC108: Fall 2021 -- Assignment 1: Unscramble

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Tom Fairgrieve, Sadia Sharmin, and 
Jacqueline Smith.

---

1. We do not expect you to understand the code in this file at this point in 
the course. You are welcome to read through it, but don't worry if you find it
confusing.

2. There are no docstring examples for some functions because they depend on 
randomness and/or user input.

3. You will not submit this file, so you should not make any changes to it. All 
of your code for the assignment should be in the unscramble_functions.py file.
"""

import random
from typing import Tuple
import unscramble_functions as uf

TEST = 'T'
NORMAL = 'N'
HINT = 'H'
SECTION_HINT = 1
MOVE_HINT = 2


def start_game() -> Tuple[str, str, str, str]:
    """Return the start state, answer, mode, and section length of a new game.
    """
    mode = get_mode()
    if in_test_mode(mode):
        answer, section_len = start_test_mode()
    elif in_hint_mode(mode):
        # Hint mode only works with a section length of 3
        games = ['CATDOGEMUFOX', 'WHOAREYOU', 'PIEEGGHAMOATBUNFIGJAM', 'ZIGZAG']
        answer = random.choice(games)
        section_len = uf.HINT_MODE_SECTION_LENGTH
    else:
        games = {'CATDOGEMUFOX': 3, 'ITISOK': 2, 'PYTHONORANGEWAFFLE': 6,
                 'CAKERICEKIWISOUPPIES': 4 , 'ROCKLAKE': 4}
        answer = random.choice(list(games.keys()))
        section_len = games[answer]
    state = generate_starting_point(answer, section_len)
    return state, answer, mode, section_len


def start_test_mode() -> Tuple[str, int]:
    """Return the answer and section_len that the user wants to test with.
    """
    answer = input('Enter the answer to use: ')
    prompt = 'Enter the section length to use: '
    section_len = input(prompt)
    while not (section_len.isdigit() and len(answer) % int(section_len) == 0):
        print('Invalid section length!')
        section_len = input(prompt)
    return answer, int(section_len)


def generate_starting_point(answer: str, section_len: int) -> str:
    """Return a scrambled version of answer with section length section_len.

    >>> random.seed(42)
    >>> generate_starting_point('CATDOGFOXEMU', 3)
    'ACTGODOXFMUE'
    """
    starter = ''
    for i in range(len(answer) // section_len):
        section = list(answer[section_len * i:section_len * (i + 1)])
        random.shuffle(section)
        starter = starter + ''.join(section)
    return starter


def get_section_hint(state: str, answer: str) -> int:
    """Return a random section number corresponding to a section of state that
    is not arranged the same as in answer.

    Precondition: Section length for state and answer is 3.

    >>> random.seed(42)
    >>> get_section_hint('CATDGOMUEXOF', 'CATDOGEMUFOX')
    3
    >>> get_section_hint('CTADGOMUEXOF', 'CATDOGEMUFOX')
    4
    """
    section_nums = [i + 1
                    for i in range(len(state) // uf.HINT_MODE_SECTION_LENGTH)]
    random.shuffle(section_nums)
    for section_num in section_nums:
        if not uf.check_section(state, answer, section_num,
                                uf.HINT_MODE_SECTION_LENGTH):
            return section_num
    return 0  # should never get here


def is_valid_mode(mode: str) -> bool:
    """Return True if and only if mode is a valid mode.

    >>> is_valid_mode('T')
    True
    >>> is_valid_mode('S')
    False
    """
    return mode == TEST or mode == NORMAL or mode == HINT


def in_test_mode(mode: str) -> bool:
    """Return True if and only if mode indicates the game is in test mode.

    >>> in_test_mode('T')
    True
    >>> in_test_mode('N')
    False
    """
    return mode == TEST


def in_hint_mode(mode: str) -> bool:
    """Return True if and only if mode indicates the game is in hint mode.

    >>> in_hint_mode('H')
    True
    >>> in_hint_mode('N')
    False
    """
    return mode == HINT


def make_move(state: str, answer: str, section_num: int, move: str,
              section_len: int) -> str:
    """Return the new game state after performing the game move specified by
    move on the section of state correspoding to section_num. If the move is
    checking, the specified section in the game state is compared to the 
    same section in answer.
    The section length is given by section_len


    >>> make_move('TCADOGEMUFOX', 'CATDOGEMUFOX', 1, 'S', 3)
    'CATDOGEMUFOX'
    >>> make_move('CATDOGUMEFOX', 'CATDOGEMUFOX', 3, 'C', 3)
    The section is incorrect
    'CATDOGUMEFOX'
    """
    if move == uf.CHECK:
        check_result = uf.check_section(state, answer, section_num, section_len)
        if check_result:
            print('The section is correct')
        else:
            print('The section is incorrect')
    else:
        state = uf.change_section(state, move, section_num, section_len)
    return state


def get_mode() -> str:
    """Return a valid game mode entered by the user.
    """
    prompt = 'Enter the mode to play [(T)est, (N)ormal, or (H)int]: '
    mode = input(prompt).upper()
    while not is_valid_mode(mode):
        print('Invalid mode!')
        mode = input(prompt).upper()
    return mode


def get_section_number(answer: str, section_len: int) -> int:
    """Return a valid section number for answer as entered by the user
    based on the section_len.
    """
    prompt = 'Enter a section number (1 - ' + \
        str(uf.get_num_sections(answer, section_len)) + '): '
    section_num = input(prompt)
    while not (section_num.isdigit() and
               uf.is_valid_section(int(section_num), answer, section_len)):
        print('Invalid section number!')
        section_num = input(prompt)
    return int(section_num)


def get_move() -> str:
    """Return a valid move entered by the user.
    """
    msg = 'Enter a move for that section (C to check, S to shift, F to flip): '
    move = input(msg).upper()
    while not uf.is_valid_move(move):
        print('Invalid move!')
        move = input(msg).upper()
    return move


def get_hints(state: str, answer: str, mode: str, hint_type: str,
              section_num: int) -> int:
    """Return 1 if a hint was given, and 0 if not. Prompt the user to answer
    whether they would like a hint of type hint_type if and only if mode
    indicates the game is in hint mode.

    If yes, generate the hint on how to rearrange state based on the current
    state and the asnwer (only using section_num if hint_type corresponds to 
    a move hint) and print the hint.

    Preconditon: section_num is a valid section and the section length of state
    and answer is 3 if hint_type is MOVE_HINT.
    """
    if in_hint_mode(mode):
        if hint_type == SECTION_HINT:
            hint = input('Enter Y if you want a section hint: ').upper()
            if hint == 'Y':
                print('Your section hint is: ' +
                      str(get_section_hint(state, answer)))
                return 1
        elif hint_type == MOVE_HINT:
            hint = input('Enter Y if you want a move hint: ').upper()
            if hint == 'Y':
                print('Your move hint is: ' +
                      uf.get_move_hint(state, answer, section_num))
                return 1
    return 0


def play_game(state: str, answer: str, mode: str, section_len: int) -> int:
    """Return the number of moves taken to move from state and arrive at 
    the correct answer given the mode and section_len.

    Run the main loop in game-mode mode, prompting the user for input and
    consequently updating state.
    """
    moves = 0
    if in_test_mode(mode):
        print('Answer: ' + answer)

    while state != answer:
        print('Current state: ' + state)
        moves += get_hints(state, answer, mode, SECTION_HINT, -1)
        section_num = get_section_number(answer, section_len)
        moves += get_hints(state, answer, mode, MOVE_HINT, section_num)
        move = get_move()
        state = make_move(state, answer, section_num, move, section_len)
        moves += 1
    return moves


if __name__ == '__main__':

    start_state, game_answer, game_mode, section_length = start_game()
    num_moves = play_game(start_state, game_answer, game_mode, section_length)
    print('You got the answer {0} in {1} moves!'.format(game_answer, num_moves))
