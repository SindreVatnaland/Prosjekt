import chess
import math
from time import sleep


class Node:
    def __init__(self, depth, board, color, player=1):
        self.depth = depth
        self.board = board
        self.color = color
        self.player = player
        self.value = self.player * calculate_move(self.board)
        self.moves = {}
        self.children = []
        self.GetMoves()
        self.CreateChildren()

    def CreateChildren(self):
        if self.depth >= 0:
            for from_ in self.moves:
                if not self.moves[from_] is None:
                    for move in self.moves[from_]:
                        self.children.append(Node(self.depth-1, chess.movePiece(from_, move, self.board), change_color(self.color), -self.player))

    def GetMoves(self):
        for piece in range(64):
            if chess.getColor(chess.getPiece(piece, self.board)) == self.color:
                self.moves[piece] = chess.isValid(piece, self.board)


def MinMax(board, depth, color):
    if depth == 0 or abs(calculate_move(board)) >= abs(10000):
        return None, calculate_move(board)
    moves = get_moves(board, color)
    best_move = None

    if color == chess.Color.black:
        best_score = -math.inf
        for from_move in moves:
            for to_move in moves[from_move]:
                temp_board = chess.movePiece(from_move, to_move, board)
                score = MinMax(temp_board, depth-1, change_color(color))[1]
                best_score = max(best_score, score)
                if best_score == score:
                    best_score = score
                    best_move = (from_move, to_move)
        return best_move, best_score
    else:
        lowest_score = math.inf
        for from_move in moves:
            for to_move in moves[from_move]:
                temp_board = chess.movePiece(from_move, to_move, board)
                score = MinMax(temp_board, depth-1, change_color(color))[1]
                lowest_score = min(lowest_score, score)
                if lowest_score == score:
                    lowest_score = score
                    best_move = (from_move, to_move)
        return best_move, lowest_score


def find_move(board, color):
    # tree = Node(start_depth, board, color)
    move, score = MinMax(board, 3, color)

    # generation(board, start_depth, color)

    return move




def calculate_move(board):
    score = 0
    pieces = find_pieces(board)
    for piece in pieces:
        if chess.isWhite(chess.getColor(piece)):
            multiply = -1
        else:
            multiply = 1

        if chess.isPawn(piece):
            score += multiply * 10
        elif chess.isKnight(piece) or chess.isBishop(piece):
            score += multiply * 30
        elif chess.isRook(piece):
            score += multiply * 50
        elif chess.isQueen(piece):
            score += multiply * 90
        elif chess.isKing(piece):
            score += multiply * 1000
    return score


def calculate_move_last(board):
    #check if king is in check
    pass

def get_moves(board, color):
    moves = {}
    for piece in range(64):
        if chess.getColor(chess.getPiece(piece, board)) == color and chess.getPiece(piece, board):
            moves[piece] = chess.isValid(piece, board)
    return moves

def find_pieces(board):
    pieces = []
    for i in range(64):
        piece = chess.getPiece(i, board)
        if piece:
            pieces.append(piece)
    return pieces

def change_color(color):
    if color == chess.Color.white:
        color = chess.Color.black
    else:
        color = chess.Color.white
    return color
