from abc import ABC, abstractmethod
 
class Color:
    WHITE = "white"
    BLACK = "black"
    
    @staticmethod
    def opposite(color):
        return Color.BLACK if color == Color.WHITE else Color.WHITE
 
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    @staticmethod
    def from_chess(coord):
        col = ord(coord[0]) - ord('a')
        row = 8 - int(coord[1])
        return Position(row, col)
    
    def to_chess(self):
        return f"{chr(self.col + ord('a'))}{8 - self.row}"
 
class Move:
    def __init__(self, from_pos, to_pos, piece, captured=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured = captured
    
    def __str__(self):
        return f"{self.piece.symbol} {self.from_pos.to_chess()} -> {self.to_pos.to_chess()}"
 
class Piece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
    
    @abstractmethod
    def get_possible_moves(self, board):
        pass
 
class Pawn(Piece):
    @property
    def symbol(self):
        return "♟" if self.color == "black" else "♙"
    
    def get_possible_moves(self, board):
        moves = []
        direction = -1 if self.color == "white" else 1
        start_row = 6 if self.color == "white" else 1
        
        forward = Position(self.position.row + direction, self.position.col)
        if board.is_valid(forward) and board.is_empty(forward):
            moves.append(forward)
            
            two_forward = Position(self.position.row + 2*direction, self.position.col)
            if self.position.row == start_row and board.is_valid(two_forward) and board.is_empty(two_forward):
                moves.append(two_forward)
        
        for dc in [-1, 1]:
            capture = Position(self.position.row + direction, self.position.col + dc)
            if board.is_valid(capture):
                target = board.get_piece(capture)
                if target and target.color != self.color:
                    moves.append(capture)
        
        return moves
 
class Rook(Piece):
    @property
    def symbol(self):
        return "♜" if self.color == "black" else "♖"
    
    def get_possible_moves(self, board):
        moves = []
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            for step in range(1, 8):
                pos = Position(self.position.row + dr*step, self.position.col + dc*step)
                if not board.is_valid(pos):
                    break
                if board.is_empty(pos):
                    moves.append(pos)
                else:
                    if board.get_piece(pos).color != self.color:
                        moves.append(pos)
                    break
        return moves
 
class Knight(Piece):
    @property
    def symbol(self):
        return "♞" if self.color == "black" else "♘"
    
    def get_possible_moves(self, board):
        moves = []
        offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, dc in offsets:
            pos = Position(self.position.row + dr, self.position.col + dc)
            if board.is_valid(pos) and (board.is_empty(pos) or board.get_piece(pos).color != self.color):
                moves.append(pos)
        return moves
 
class Bishop(Piece):
    @property
    def symbol(self):
        return "♝" if self.color == "black" else "♗"
    
    def get_possible_moves(self, board):
        moves = []
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            for step in range(1, 8):
                pos = Position(self.position.row + dr*step, self.position.col + dc*step)
                if not board.is_valid(pos):
                    break
                if board.is_empty(pos):
                    moves.append(pos)
                else:
                    if board.get_piece(pos).color != self.color:
                        moves.append(pos)
                    break
        return moves
 
class Queen(Piece):
    @property
    def symbol(self):
        return "♛" if self.color == "black" else "♕"
    
    def get_possible_moves(self, board):
        moves = []
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            for step in range(1, 8):
                pos = Position(self.position.row + dr*step, self.position.col + dc*step)
                if not board.is_valid(pos):
                    break
                if board.is_empty(pos):
                    moves.append(pos)
                else:
                    if board.get_piece(pos).color != self.color:
                        moves.append(pos)
                    break
        return moves
 
class King(Piece):
    @property
    def symbol(self):
        return "♚" if self.color == "black" else "♔"
    
    def get_possible_moves(self, board):
        moves = []
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                pos = Position(self.position.row + dr, self.position.col + dc)
                if board.is_valid(pos) and (board.is_empty(pos) or board.get_piece(pos).color != self.color):
                    moves.append(pos)
        return moves
 
class Wizard(Piece):
    @property
    def symbol(self):
        return "🧙"
    
    def get_possible_moves(self, board):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                pos = Position(self.position.row + dr, self.position.col + dc)
                if board.is_valid(pos) and (board.is_empty(pos) or board.get_piece(pos).color != self.color):
                    moves.append(pos)
        offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, dc in offsets:
            pos = Position(self.position.row + dr, self.position.col + dc)
            if board.is_valid(pos) and (board.is_empty(pos) or board.get_piece(pos).color != self.color):
                moves.append(pos)
        return moves
 
class Cavalier(Piece):
    @property
    def symbol(self):
        return "⚡"
    
    def get_possible_moves(self, board):
        moves = []
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            for step in range(1, 8):
                pos = Position(self.position.row + dr*step, self.position.col + dc*step)
                if not board.is_valid(pos):
                    break
                if board.is_empty(pos):
                    moves.append(pos)
                else:
                    if board.get_piece(pos).color != self.color:
                        moves.append(pos)
                    break
        offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, dc in offsets:
            pos = Position(self.position.row + dr, self.position.col + dc)
            if board.is_valid(pos) and (board.is_empty(pos) or board.get_piece(pos).color != self.color):
                moves.append(pos)
        return moves
 
class Guard(Piece):
    @property
    def symbol(self):
        return "🛡️"
    
    def get_possible_moves(self, board):
        moves = []
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            for step in range(1, 8):
                pos = Position(self.position.row + dr*step, self.position.col + dc*step)
                if not board.is_valid(pos):
                    break
                if board.is_empty(pos):
                    moves.append(pos)
                else:
                    if board.get_piece(pos).color != self.color:
                        moves.append(pos)
                    break
        direction = -1 if self.color == "white" else 1
        forward_left = Position(self.position.row + direction, self.position.col - 1)
        forward_right = Position(self.position.row + direction, self.position.col + 1)
        if board.is_valid(forward_left) and (board.is_empty(forward_left) or board.get_piece(forward_left).color != self.color):
            moves.append(forward_left)
        if board.is_valid(forward_right) and (board.is_empty(forward_right) or board.get_piece(forward_right).color != self.color):
            moves.append(forward_right)
        return moves
 
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.en_passant_target = None
        self.history = []
        self.setup()
    
    def setup(self):
        pieces_black = [
            (Rook, 0, 0), (Knight, 0, 1), (Wizard, 0, 2), (Queen, 0, 3),
            (King, 0, 4), (Cavalier, 0, 5), (Knight, 0, 6), (Guard, 0, 7)
        ]
        for piece_class, row, col in pieces_black:
            self.grid[row][col] = piece_class(Color.BLACK, Position(row, col))
        
        for col in range(8):
            self.grid[1][col] = Pawn(Color.BLACK, Position(1, col))
        
        pieces_white = [
            (Rook, 7, 0), (Knight, 7, 1), (Wizard, 7, 2), (Queen, 7, 3),
            (King, 7, 4), (Cavalier, 7, 5), (Knight, 7, 6), (Guard, 7, 7)
        ]
        for piece_class, row, col in pieces_white:
            self.grid[row][col] = piece_class(Color.WHITE, Position(row, col))
        
        for col in range(8):
            self.grid[6][col] = Pawn(Color.WHITE, Position(6, col))
    
    def is_valid(self, pos):
        return 0 <= pos.row < 8 and 0 <= pos.col < 8
    
    def is_empty(self, pos):
        return self.grid[pos.row][pos.col] is None
    
    def get_piece(self, pos):
        return self.grid[pos.row][pos.col]
    
    def is_square_attacked(self, pos, defending_color):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color != defending_color:
                    if pos in piece.get_possible_moves(self):
                        return True
        return False
    
    def get_valid_moves(self, piece):
        moves = []
        for target in piece.get_possible_moves(self):
            if self.is_valid_move(piece.position, target, piece):
                moves.append(target)
        return moves
    
    def is_valid_move(self, from_pos, to_pos, piece=None):
        if piece is None:
            piece = self.get_piece(from_pos)
            if not piece:
                return False
        
        if piece.color != self.current_turn:
            return False
        
        if to_pos not in piece.get_possible_moves(self):
            return False
        
        captured = self.get_piece(to_pos)
        if captured and captured.color == piece.color:
            return False
        
        original_piece = self.get_piece(to_pos)
        self.grid[to_pos.row][to_pos.col] = piece
        self.grid[from_pos.row][from_pos.col] = None
        old_pos = piece.position
        piece.position = to_pos
        
        king_pos = self.find_king(piece.color)
        in_check = self.is_square_attacked(king_pos, piece.color)
        
        self.grid[from_pos.row][from_pos.col] = piece
        self.grid[to_pos.row][to_pos.col] = original_piece
        piece.position = old_pos
        
        return not in_check
    
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return Position(row, col)
        return None
    
    def make_move(self, from_pos, to_pos):
        piece = self.get_piece(from_pos)
        if not piece:
            return False
        
        if not self.is_valid_move(from_pos, to_pos, piece):
            return False
        
        captured = self.get_piece(to_pos)
        move = Move(from_pos, to_pos, piece, captured)
        self.history.append(move)
        
        self.grid[to_pos.row][to_pos.col] = piece
        self.grid[from_pos.row][from_pos.col] = None
        piece.position = to_pos
        piece.has_moved = True
        
        if isinstance(piece, Pawn) and (to_pos.row == 0 or to_pos.row == 7):
            self.grid[to_pos.row][to_pos.col] = Queen(piece.color, to_pos)
        
        self.current_turn = Color.opposite(self.current_turn)
        return True
    
    def undo(self):
        if not self.history:
            return False
        
        move = self.history.pop()
        self.grid[move.from_pos.row][move.from_pos.col] = move.piece
        self.grid[move.to_pos.row][move.to_pos.col] = move.captured
        move.piece.position = move.from_pos
        move.piece.has_moved = False
        
        self.current_turn = move.piece.color
        return True
    
    def get_threatened_pieces(self, color):
        threatened = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    if self.is_square_attacked(piece.position, color):
                        threatened.append(piece)
        return threatened
    
    def is_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        return self.is_square_attacked(king_pos, color)
    
    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    for target in self.get_valid_moves(piece):
                        if self.is_valid_move(piece.position, target, piece):
                            return False
        return True
    
    def display(self, highlight_moves=None, highlight_threatened=None):
        print("\n  a   b   c   d   e   f   g   h")
        for row in range(8):
            print(f"{8-row} ", end="")
            for col in range(8):
                piece = self.grid[row][col]
                pos = Position(row, col)
                
                if highlight_moves and pos in highlight_moves:
                    print("\033[42m", end="")
                elif highlight_threatened:
                    is_threatened = False
                    for p in highlight_threatened:
                        if p.position == pos:
                            is_threatened = True
                            break
                    if is_threatened:
                        print("\033[41m", end="")
                elif (row + col) % 2 == 0:
                    print("\033[47m", end="")
                else:
                    print("\033[40m", end="")
                
                if piece:
                    symbol = piece.symbol
                    if len(symbol) > 1:
                        print(f" {symbol} ", end="")
                    else:
                        print(f" {symbol}  ", end="")
                else:
                    print("    ", end="")
                print("\033[0m", end="")
            print(f" {8-row}")
        print("  a   b   c   d   e   f   g   h")
 
class Game:
    def run(self):
        board = Board()
        
        while True:
            print("\n" + "="*50)
            
            if board.is_checkmate(board.current_turn):
                winner = Color.opposite(board.current_turn)
                print(f"Мат! Победили {winner}")
                break
            
            threatened = board.get_threatened_pieces(board.current_turn)
            
            if board.is_check(board.current_turn):
                print("ШАХ!")
            
            print(f"Ход: {board.current_turn}")
            board.display(highlight_threatened=threatened)
            
            print("\nКоманды: e2e4 - ход, moves - подсказка, undo - откат, exit - выход")
            cmd = input("> ").strip().lower()
            
            if cmd == "exit":
                break
            elif cmd == "undo":
                if board.undo():
                    print("Откат выполнен")
                else:
                    print("Нечего откатывать")
                continue
            elif cmd == "moves":
                print("Введи координаты фигуры (например: e2):")
                pos_input = input("> ").strip().lower()
                if len(pos_input) == 2:
                    try:
                        pos = Position.from_chess(pos_input)
                        piece = board.get_piece(pos)
                        if piece is None:
                            print("На этой клетке нет фигуры")
                        elif piece.color != board.current_turn:
                            print(f"Это фигура {piece.color}, а ход {board.current_turn}")
                        else:
                            moves = board.get_valid_moves(piece)
                            if moves:
                                print("Возможные ходы:", [p.to_chess() for p in moves])
                                board.display(highlight_moves=moves)
                            else:
                                print("Нет доступных ходов у этой фигуры")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                else:
                    print("Неверный формат. Введи 2 символа, например: e2")
                continue
            elif len(cmd) == 4:
                try:
                    from_pos = Position.from_chess(cmd[:2])
                    to_pos = Position.from_chess(cmd[2:])
                    if board.make_move(from_pos, to_pos):
                        print("Ход выполнен")
                    else:
                        print("Неверный ход")
                except:
                    print("Неверный формат")
            else:
                print("Неверная команда")
 
if __name__ == "__main__":
    Game().run()