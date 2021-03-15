import numpy as np

starting_board = 822600792108962701109752665142821874674704896976585017661690405272942910148120593644329604648004

BITS = 5

all_on = 2**(64*BITS)-1

class Piece:
    pawn = 1
    knight = 2
    bishop = 3
    rook = 4
    queen = 5
    king = 6

    specialPawn = 17
    specialRook = 20
    specialKing = 22


class Color:
    white = 0
    black = 1 << 3


def generateBoard(board):
    array = np.zeros((8, 8), dtype=int)
    i = 0
    for y in range(7, -1, -1):
        for x in range(8):
            array[y][x] = getPiece(i, board)
            i += 1
    # print(array)
    return array


def getRouteBit(field, piece):
    return piece << (5 * field)


def getPiece(field, cur_board):
    return ((0x1F << field * BITS) & cur_board) >> field * BITS


def getPieceName(piece):
    for name, i in Piece.__dict__.items():
        if i == piece:
            print(f"W-{name}")
        elif i == piece-8:
            print(f"B-{name}")


def changePiece(pos, cur_board, new_piece, color):
    new_piece = (new_piece | color)
    mask = mask_route(pos)
    cur_board = cur_board & mask
    new_board = cur_board | (getRouteBit(pos, new_piece))
    return new_board


def mask_route(route):
    mask_from_off = 2**((route+1)*BITS)-1
    piece_from_route = 2**(route*BITS)-1
    return(all_on ^ mask_from_off) ^ piece_from_route


def movePiece(from_, to, cur_board):
    from_piece = getPiece(from_, cur_board)
    if isValid(from_, cur_board):
        if isWhite(from_piece):
            piece_color = Color.white
        else:
            piece_color = Color.black
        if from_piece == Piece.pawn or Piece.king or Piece.rook:
            if isPawn(from_piece) and abs(from_ - to) == 16:
                cur_board = changePiece(from_, cur_board, Piece.specialPawn, piece_color)
                new_piece = getRouteBit(to, getPiece(from_, cur_board))
            elif isRook(from_piece):
                cur_board = changePiece(from_, cur_board, Piece.specialRook, piece_color)
                new_piece = getRouteBit(to, getPiece(from_, cur_board))
            elif isKing(from_piece):
                cur_board = changePiece(from_, cur_board, Piece.specialKing, piece_color)
                new_piece = getRouteBit(to, getPiece(from_, cur_board))
            else:
                new_piece = getRouteBit(to, from_piece)
        else:
            new_piece = getRouteBit(to, from_piece)

        if isKing(from_piece) and from_-to == 2:
            cur_board = changePiece(to+1, cur_board, Piece.specialRook, piece_color)
            cur_board = changePiece(to-2, cur_board, 0, piece_color)
        elif isKing(from_piece) and from_-to == -2:
            cur_board = changePiece(to+1, cur_board, 0, piece_color)
            cur_board = changePiece(to-1, cur_board, Piece.specialRook, piece_color)

        mask_from_bits = mask_route(from_)
        mask_to_bits = mask_route(to)
        mask = (mask_from_bits & mask_to_bits)

        cur_board = cur_board & mask
        cur_board = cur_board | new_piece

        if isWhite(from_piece):
            if isPawn(from_piece) and isPawn(getPiece(to-8, cur_board)) and isSpecial(getPiece(to-8, cur_board)):
                cur_board = changePiece(to-8, cur_board, 0, 0)
            if to >= 56:
                cur_board = changePiece(to, cur_board, Piece.queen, Color.white)
        else:
            if isPawn(from_piece) and (from_-to == 7 or 9) and isSpecial(getPiece(to+8, cur_board)):
                cur_board = changePiece(to+8, cur_board, 0, 0)
            if to <= 7:
                cur_board = changePiece(to, cur_board, Piece.queen, Color.black)

        if isWhite(from_piece):
            cur_board = undoSpecialPawns(Color.black, cur_board)
        elif not isWhite(from_piece):
            cur_board = undoSpecialPawns(Color.white, cur_board)

        # print(f"\nMoves piece from route {from_} to {to}")

    generateBoard(cur_board)

    return cur_board


def isValid(from_route, cur_board):
    from_piece = getPiece(from_route, cur_board)
    if isPawn(from_piece):
        # print("pawn")
        moves = findPawnMoves(from_route, cur_board)
        return moves


    elif isKnight(from_piece):
        # print("knight")
        moves = findKnightMoves(from_route, cur_board)
        return moves

    elif isBishop(from_piece):
        # print("bishop")
        moves = findStrifeMoves(from_route, cur_board)
        return moves

    elif isRook(from_piece):
        # print("rook")
        moves = findStraightMoves(from_route, cur_board)
        return moves


    elif isQueen(from_piece):
        # print("queen")
        strife = findStrifeMoves(from_route, cur_board)
        straight = findStraightMoves(from_route, cur_board)
        moves = strife + straight
        return moves


    elif isKing(from_piece):
        # print("king")
        moves = findKingMoves(from_route, cur_board)
        return moves

def findPawnMoves(from_route, cur_board):
    possible = []

    from_piece = getPiece(from_route, cur_board)

    if isWhite(from_piece):
        # print("white")
        if not getPiece(from_route+8, cur_board):
            possible.append(from_route+8)
        if from_route in range(8, 16) and not (getPiece(from_route+8, cur_board) or getPiece(from_route+16, cur_board)):
            possible.append(from_route+16)
        if getPiece(from_route+7, cur_board) != 0 and not isWhite(getPiece(from_route+7, cur_board)) and not from_route % 8 == 0:
            possible.append(from_route+7)
        if getPiece(from_route+9, cur_board) != 0 and not isWhite(getPiece(from_route+9, cur_board)) and not from_route % 8 == 7:
            possible.append(from_route+9)
        if getPiece(from_route-1, cur_board) == Piece.specialPawn | Color.black and not from_route % 8 == 0:
            possible.append(from_route+7)
        if getPiece(from_route+1, cur_board) == Piece.specialPawn | Color.black and not from_route % 8 == 7:
            possible.append(from_route+9)
    else:
        # print("black")
        if not getPiece(from_route-8, cur_board):
            possible.append(from_route-8)
        if from_route in range(48, 56) and not (getPiece(from_route-8, cur_board) or getPiece(from_route-16, cur_board)):
            possible.append(from_route-16)
        if getPiece(from_route-9, cur_board) != 0 and isWhite(getPiece(from_route-9, cur_board)) and not from_route % 8 == 0:
            possible.append(from_route-9)
        if getPiece(from_route-7, cur_board) != 0 and isWhite(getPiece(from_route-7, cur_board)) and not from_route % 8 == 7:
            possible.append(from_route-7)
        if getPiece(from_route+1, cur_board) == Piece.specialPawn | Color.white and not from_route % 8 == 7:
            possible.append(from_route-7)
        if getPiece(from_route-1, cur_board) == Piece.specialPawn | Color.white and not from_route % 8 == 0:
            possible.append(from_route-9)


    return possible


def findKnightMoves(from_route, cur_board):
    possible = []
    modulo = from_route % 8

    from_piece = getPiece(from_route, cur_board)
    color = getColor(from_piece)

    move1 = from_route+(2*8)+1
    move2 = from_route+(2*8)-1
    move3 = from_route-(2*8)+1
    move4 = from_route-(2*8)-1
    move5 = from_route+8+2
    move6 = from_route+8-2
    move7 = from_route-8+2
    move8 = from_route-8-2

    moves = [move1, move2, move3, move4, move5, move6, move7, move8]

    if modulo < 2:
        for move in moves:
            if 0 <= move <= 63:
                to_piece = getPiece(move, cur_board)
                if move % 8 <= 5 and (color != getColor(to_piece) or to_piece == 0):
                    possible.append(move)
    elif modulo > 5:
        for move in moves:
            if 0 <= move <= 63:
                to_piece = getPiece(move, cur_board)
                if move % 8 >= 2 and (color != getColor(to_piece) or to_piece == 0):
                    possible.append(move)
    elif 2 <= modulo <= 5:
        for move in moves:
            if 0 <= move <= 63:
                to_piece = getPiece(move, cur_board)
                if color != getColor(to_piece) or to_piece == 0:
                    possible.append(move)

    return possible


def findStrifeMoves(from_route, cur_board):
    possible = []
    diagonal_right_up = from_route
    diagonal_right_down = from_route
    diagonal_left_up = from_route
    diagonal_left_down = from_route

    if isWhite(getPiece(from_route, cur_board)):
        opponent_color = Color.black
        my_color = Color.white
    else:
        opponent_color = Color.white
        my_color = Color.black

    while diagonal_right_up < 56 and not diagonal_right_up % 8 == 7:
        diagonal_right_up += 9
        if getColor(getPiece(diagonal_right_up, cur_board)) == opponent_color and getPiece(diagonal_right_up, cur_board):
            possible.append(diagonal_right_up)
            break
        elif getColor(getPiece(diagonal_right_up, cur_board)) == my_color and getPiece(diagonal_right_up, cur_board):
            break
        possible.append(diagonal_right_up)

    while diagonal_right_down > 7 and not diagonal_right_down % 8 == 7:
        diagonal_right_down -= 7
        if getColor(getPiece(diagonal_right_down, cur_board)) == opponent_color and getPiece(diagonal_right_down, cur_board):
            possible.append(diagonal_right_down)
            break
        elif getColor(getPiece(diagonal_right_down, cur_board)) == my_color and getPiece(diagonal_right_down, cur_board):
            break
        possible.append(diagonal_right_down)

    while diagonal_left_up < 56 and not diagonal_left_up % 8 == 0:
        diagonal_left_up += 7
        if getColor(getPiece(diagonal_left_up, cur_board)) == opponent_color and getPiece(diagonal_left_up, cur_board):
            possible.append(diagonal_left_up)
            break
        elif getColor(getPiece(diagonal_left_up, cur_board)) == my_color and getPiece(diagonal_left_up, cur_board):
            break
        possible.append(diagonal_left_up)

    while diagonal_left_down > 7 and not diagonal_left_down % 8 == 0:
        diagonal_left_down -= 9
        if getColor(getPiece(diagonal_left_down, cur_board)) == opponent_color and getPiece(diagonal_left_down, cur_board):
            possible.append(diagonal_left_down)
            break
        elif getColor(getPiece(diagonal_left_down, cur_board)) == my_color and getPiece(diagonal_left_down, cur_board):
            break
        possible.append(diagonal_left_down)
    return possible


def findStraightMoves(from_route, cur_board):
    possible = []
    up = from_route
    down = from_route
    left = from_route
    right = from_route

    if isWhite(getPiece(from_route, cur_board)):
        opponent_color = Color.black
        my_color = Color.white
    else:
        opponent_color = Color.white
        my_color = Color.black

    while up < 56:
        up += 8
        if getColor(getPiece(up, cur_board)) == opponent_color and getPiece(up, cur_board):
            possible.append(up)
            break
        elif getColor(getPiece(up, cur_board)) == my_color and getPiece(up, cur_board):
            break
        possible.append(up)

    while down > 7:
        down -= 8
        if getColor(getPiece(down, cur_board)) == opponent_color and getPiece(down, cur_board):
            possible.append(down)
            break
        elif getColor(getPiece(down, cur_board)) == my_color and getPiece(down, cur_board):
            break
        possible.append(down)

    while not left % 8 == 0:
        left -= 1
        if getColor(getPiece(left, cur_board)) == opponent_color and getPiece(left, cur_board):
            possible.append(left)
            break
        elif getColor(getPiece(left, cur_board)) == my_color and getPiece(left, cur_board):
            break
        possible.append(left)

    while not right % 8 == 7:
        right += 1
        if getColor(getPiece(right, cur_board)) == opponent_color and getPiece(right, cur_board):
            possible.append(right)
            break
        elif getColor(getPiece(right, cur_board)) == my_color and getPiece(right, cur_board):
            break
        possible.append(right)
    return possible


def findKingMoves(from_route, cur_board):
    possible = []

    if isWhite(getPiece(from_route, cur_board)):
        opponent_color = Color.black
    else:
        opponent_color = Color.white

    move1 = from_route + 7
    move2 = from_route + 8
    move3 = from_route + 9
    move4 = from_route + 1
    move5 = from_route - 7
    move6 = from_route - 8
    move7 = from_route - 9
    move8 = from_route - 1

    moves = [move1, move2, move3, move4, move5, move6, move7, move8]

    for move in moves:
        if move < 0 or abs(move % 8 - from_route % 8) == 7 or move > 64:
            continue
        if (getColor(getPiece(move, cur_board)) == opponent_color and getPiece(move, cur_board)) or getPiece(move, cur_board) == 0:
            possible.append(move)
    king = getPiece(from_route, cur_board)

    if isKing(king) and not isSpecial(king):
        rook1 = getPiece(from_route+3, cur_board)
        rook2 = getPiece(from_route-4, cur_board)
        if getPiece(from_route+1, cur_board) == 0 and getPiece(from_route+2, cur_board) == 0 and not isSpecial(rook1):
            possible.append(from_route+2)
        if getPiece(from_route-1, cur_board) == 0 and getPiece(from_route-2, cur_board) == 0 and getPiece(from_route-3, cur_board) == 0 and not isSpecial(rook2):
            possible.append(from_route-2)
    return possible

def undoSpecialPawns(color, cur_board):
    for pos in range(64):
        piece = getPiece(pos, cur_board)
        if getColor(piece) == color and isPawn(piece):
            cur_board = changePiece(pos, cur_board, removeSpecial(piece), color)
    return cur_board

def isPawn(piece):
    return piece % 8 == 1


def isKnight(piece):
    return piece % 8 == 2


def isBishop(piece):
    return piece % 8 == 3


def isRook(piece):
    return piece % 8 == 4


def isQueen(piece):
    return piece % 8 == 5


def isKing(piece):
    return piece % 8 == 6


def getColor(piece):
    return piece & 8


def isWhite(piece):
    if piece & 8 == 0:
        return True
    else:
        return False


def isSpecial(piece):
    if piece & 16:
        return True
    else:
        return False


def makeSpecial(piece):
    return piece | 16


def removeSpecial(piece):
    return piece & 15


board = starting_board

print(board)
print("{0:b}".format(board))

