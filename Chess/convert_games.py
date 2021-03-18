import numpy as np
import chess
import bot

def add_pawn(board, possible_moves, letter_number, move, openings):
    for key in possible_moves:
        if possible_moves[key]:
            for mov in possible_moves[key]:
                if mov == (letter_number[move[-2]] + 8 * (int(move[-1])-1)) and chess.isPawn(chess.getPiece(key, board)):
                    try:
                        openings[board].append((key, mov))
                    except:
                        openings[board] = []
                        openings[board].append((key, mov))
                    return chess.movePiece(key, mov, board), openings

def add_knight(board, possible_moves, letter_number, move, openings):
    for key in possible_moves:
        if possible_moves[key]:
            for mov in possible_moves[key]:
                if mov == (letter_number[move[-2]] + 8 * (int(move[-1])-1)) and chess.isKnight(chess.getPiece(key, board)):
                    try:
                        openings[board].append((key, mov))
                    except:
                        openings[board] = []
                        openings[board].append((key, mov))
                    return chess.movePiece(key, mov, board), openings


def add_bishop(board, possible_moves, letter_number, move, openings):
    for key in possible_moves:
        if possible_moves[key]:
            for mov in possible_moves[key]:
                if mov == (letter_number[move[-2]] + 8 * (int(move[-1])-1)) and chess.isBishop(chess.getPiece(key, board)):
                    try:
                        openings[board].append((key, mov))
                    except:
                        openings[board] = []
                        openings[board].append((key, mov))
                    return chess.movePiece(key, mov, board), openings

def add_rook(board, possible_moves, letter_number, move, openings):
    for key in possible_moves:
        if possible_moves[key]:
            for mov in possible_moves[key]:
                if mov == (letter_number[move[-2]] + 8 * (int(move[-1])-1)) and chess.isRook(chess.getPiece(key, board)):
                    try:
                        openings[board].append((key, mov))
                    except:
                        openings[board] = []
                        openings[board].append((key, mov))
                    return chess.movePiece(key, mov, board), openings

def add_queen(board, possible_moves, letter_number, move, openings):
    for key in possible_moves:
        if possible_moves[key]:
            for mov in possible_moves[key]:
                if mov == (letter_number[move[-2]] + 8 * (int(move[-1])-1)) and chess.isQueen(chess.getPiece(key, board)):
                    try:
                        openings[board].append((key, mov))
                    except:
                        openings[board] = []
                        openings[board].append((key, mov))
                    return chess.movePiece(key, mov, board), openings

def add_king(board, possible_moves, letter_number, move, openings):
    for key in possible_moves:
        if possible_moves[key]:
            for mov in possible_moves[key]:
                if mov == (letter_number[move[-2]] + 8 * (int(move[-1])-1)) and chess.isKing(chess.getPiece(key, board)):
                    try:
                        openings[board].append((key, mov))
                    except:
                        openings[board] = []
                        openings[board].append((key, mov))
                    return chess.movePiece(key, mov, board), openings

def add_king_left(board, possible_moves, letter_number, move, openings, color):
    if color == chess.Color.white:
        from_ = 4
        to = 2
    else:
        from_ = 60
        to = 58
    return chess.movePiece(from_, to, board), openings

def add_king_right(board, possible_moves, letter_number, move, openings, color):
    if color == chess.Color.white:
        from_ = 4
        to = 6
    else:
        from_ = 60
        to = 62
    return chess.movePiece(from_, to, board), openings

starting_board = 822600792108962701109752665142821874674704896976585017661690405272942910148120593644329604648004

openings = {}
letter_number = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

with open('games.txt') as games:
    for j, game in enumerate(games):
        board = starting_board
        for i, move in enumerate(game.split(" ")):
            # move = move.strip("x")
            if i % 2 == 0:
                color = chess.Color.white
            else:
                color = chess.Color.black
            possible_moves = chess.getMoves(board, color)
            move = move.split("x")
            print(move)
            if len(move) > 1:
                move = move[0]+move[1]
            else:
                move = move[0]
            move = move.strip("+")
            if len(move) == 4:
                move = move[0]+move[2]+move[3]
            print(move)
            # print(possible_moves)
            try:
                if len(move) == 2: #pawn
                    board, openings = add_pawn(board, possible_moves, letter_number, move, openings)

                elif len(move) == 3 and move[0].islower():
                    board, openings = add_pawn(board, possible_moves, letter_number, move, openings)

                elif len(move) == 3 and move[0]=="N": #knight
                    board, openings = add_knight(board, possible_moves, letter_number, move, openings)

                elif len(move) == 3 and move[0]=="B": #bishop
                    board, openings = add_bishop(board, possible_moves, letter_number, move, openings)

                elif len(move) == 3 and move[0]=="R": #rook
                  board, openings = add_rook(board, possible_moves, letter_number, move, openings)

                elif len(move) == 3 and move[0]=="Q": #queen
                    board, openings = add_queen(board, possible_moves, letter_number, move, openings)

                elif len(move) == 3 and move[0]=="K": #king
                    board, openings = add_king(board, possible_moves, letter_number, move, openings)

                elif move == "O-O":
                    board, openings = add_king_right(board, possible_moves, letter_number, move, openings, color)

                elif move == "O-O-O":
                    board, openings = add_king_left(board, possible_moves, letter_number, move, openings, color)
            except:
                board = starting_board
                break
            if i > 8:
                print(j)
                board = starting_board
                print()
                break

# np.save('openings.npy', openings)

dictionary = np.load('openings.npy', allow_pickle='TRUE').item()