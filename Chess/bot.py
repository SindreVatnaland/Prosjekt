import chess
import math
import numpy as np
import random


def MinMax(board, depth, color, alpha=-math.inf, beta=math.inf):
    if depth == 0 or abs(calculate_move(board)) >= abs(10000):
        return None, calculate_move(board)
    moves = chess.getMoves(board, color)
    best_move = None

    if color == chess.Color.black:
        best_score = -math.inf
        for from_move in moves:
            if moves[from_move]:
                for to_move in moves[from_move]:
                    if not chess.isCheck(chess.movePiece(from_move, to_move, board), color):
                        temp_board = chess.movePiece(from_move, to_move, board)
                        score = MinMax(temp_board, depth-1, change_color(color), alpha, beta)[1]
                        best_score = max(best_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
                        if best_score == score:
                            best_move = (from_move, to_move)
        return best_move, best_score
    else:
        lowest_score = math.inf
        for from_move in moves:
            if moves[from_move]:
                for to_move in moves[from_move]:
                    temp_board = chess.movePiece(from_move, to_move, board)
                    score = MinMax(temp_board, depth-1, change_color(color), alpha, beta)[1]
                    lowest_score = min(lowest_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
                    else:
                        best_move = (from_move, to_move)
        return best_move, lowest_score


def find_move(board, color):
    openings = np.load('openings.npy', allow_pickle='TRUE').item()
    try:
        moves = openings[board]
        move = random.choice(moves)
    except:
        depth = get_depth(board)
        move, score = MinMax(board, depth, color)
    return move


def calculate_move(board):
    score = 0
    pieces = get_pieces(board)
    for piece in pieces:
        if chess.isWhite(piece[0]):
            multiply = -1
            king = 1000
        else:
            multiply = 1
            king = 1200

        if chess.isPawn(piece[0]):
            score += multiply * 10
        elif chess.isKnight(piece[0]) or chess.isBishop(piece[0]):
            score += multiply * 30
        elif chess.isRook(piece[0]):
            score += multiply * 50
        elif chess.isQueen(piece[0]):
            score += multiply * 90
        elif chess.isKing(piece[0]):
            score += multiply * king

        if len(pieces) > 10:
            if (2 <= piece[1] % 8 <= 5) and chess.isWhite(piece[0]) and piece[1] >= 16 and not chess.isKing(piece[1]):
                if piece[1] % 8 == 2 or 5:
                    score += multiply * 1
                else:
                    score += multiply * 2
            elif (piece[1] % 8 == 2 or 3 or 4 or 5) and chess.isWhite(piece[0]) and piece[1] <= 48 and not chess.isKing(piece[0]):
                if piece[1] % 8 == 2 or 5:
                    score += multiply * 1
                else:
                    score += multiply * 2

        #Reward king on edge, needs fix
        elif chess.isKing(piece[0]) and len(pieces) < 10:
            weight = -5//(len(pieces)/10)
            if 24 <= piece[1] <= 40:
                score += multiply * 0 * weight
            elif (16 <= piece[1] <= 23) or (40 <= piece[1] <= 47):
                score += multiply * 1 * weight
            elif (8 <= piece[1] <= 15) or (48 <= piece[1] <= 55):
                score += multiply * 2 * weight
            elif (0 <= piece[1] <= 7) or (56 <= piece[1] <= 63):
                score += multiply * 3 * weight
            if 3 <= (piece[1] % 8) <= 4:
                score += multiply * 0 * weight
            elif piece[1] % 8 == 2 or 5:
                score += multiply * 1 * weight
            elif piece[1] % 8 == 1 or 6:
                score += multiply * 3 * weight
            elif piece[1] % 8 == 0 or 7:
                score += multiply * 5 * weight
    print(score)
    return score


def get_depth(board):
    len_pieces = len(get_pieces(board))
    if len_pieces > 10:
        depth = 3
    else:
        depth = 4

    return depth


def get_pieces(board):
    pieces = []
    for i in range(64):
        piece = chess.getPiece(i, board)
        if piece:
            pieces.append((piece, i))
    return pieces

def change_color(color):
    if color == chess.Color.white:
        color = chess.Color.black
    else:
        color = chess.Color.white
    return color
