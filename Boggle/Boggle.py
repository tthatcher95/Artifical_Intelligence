import itertools
import numpy as np
import copy
import time
import argparse

# parser = argparse.ArgumentParser(description='This is a demo script by nixCraft.')
# parser.add_argument('-d','--dict', help='Input file name',required=True)
# parser.add_argument('-b','--board',help='Output file name', required=True)
# args = parser.parse_args()

# Returns the text file as an array with each worth a single element
def get_set():
    return np.asarray(open("twl06.txt").read().splitlines())

# Makes the board into a tuple
def make_board(file):
    file = open(file)
    return tuple(line.split() for line in file)

board = make_board("4x4.txt")

# Returns the coordinates of each adjacent valid spot to move
def get_coordinates(board, x, y):

    # Height / Width of board
    row_length = len(board)
    col_length = len(board[0])

    def is_valid(y, x, col_length, row_length):

        if x >=0 and y >= 0 and x < col_length and y < row_length:
            return True
        else:
            return False

    adj_pos = []

    # Generates the possible moves through Cartesian Product
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            else:
                if is_valid(y + i, x + j, col_length, row_length):
                    adj_pos.append((y + i, x + j))
    return adj_pos

# Main Function
if __name__ == '__main__':

    # Calls the array of the text file and __init__ all other parts needed
    txt_file = get_set()
    words_found = set()
    path = set()
    board = make_board("4x4.txt")
    moves = 0
    word = []
    height = len(board)
    width = len(board[0])

    # The Search method that takes in:
    # word - The string that you are working on
    # row / col - The row and column you are accessing
    # path - Which is the locations you have been before
    # word_list - used to generate sub_lists to maximize efficiency

    def get_words(word, row, col, path, word_list):

        # Counts the amount of moves performed
        global moves
        moves += 1

        # Creates a copy of path every time get_words() is called
        # This serves so we do not modify the same path with each iteration
        path = copy.deepcopy(path)

        # Adds the part of the word that is being accessed
        word += board[row][col]
        path.add((row, col))

        # If word is in the text file adds to the array words_found
        if word.lower() in txt_file:
            words_found.add(word)

        # Takes in the board and loops through each valid move that can be executed
        current_coordinates = get_coordinates(board, col, row)
        current_coordinates = [coord for coord in current_coordinates if coord not in path]

        # Numpy function which takes all of the words that start with the string 'word'
        # And masks it to only reflect the words that start with my string 'word'
        prefix_mask = np.char.startswith(word_list, word.lower())

        # Generated the new sublist of words that contain the string 'word'
        word_list = word_list[prefix_mask]

        # If the string 'word' is not contained in the prefixes of any word in the
        # Text file it skips over it and moves on to next iteration
        if not np.any(prefix_mask):
            return

        for coord in current_coordinates:

            # Recursive call which passes the new_list to search through
            get_words(word, coord[0], coord[1], path, word_list)

    nodes = []

    # Find how many times the program has to run based on length and width of board
    for element in itertools.product(range(height), range(width)):
        nodes.append(element)

    # Starts the timer here
    time_0 = time.time()

    # Iterates through each starting point on the board
    for node in nodes:
        get_words('', node[0], node[1], path, txt_file)

    # End the timer and calculates the total time elapsed
    time_1 = time.time()
    total = time_1 - time_0

    # Formatting for the outputs
    (print('Searched total of', moves, 'moves in', "%.3f" % total, '\n'))
    for key, group in itertools.groupby(sorted(words_found, key = len), lambda x: len(x)):
        print('{} Letter Words Found: '.format(key), list(group))

    print('\nFound:', len(words_found), 'words total')
    print('Alpha-Sorted Words:', sorted(words_found))