from random import random
from time import sleep
from os import system, name as os_name


class Colors:
    CEND = "\33[0m"
    CBOLD = "\33[1m"
    CITALIC = "\33[3m"
    CURL = "\33[4m"
    CBLINK = "\33[5m"
    CBLINK2 = "\33[6m"
    CSELECTED = "\33[7m"

    CBLACK = "\33[30m"
    CRED = "\33[31m"
    CGREEN = "\33[32m"
    CYELLOW = "\33[33m"
    CBLUE = "\33[34m"
    CVIOLET = "\33[35m"
    CBEIGE = "\33[36m"
    CWHITE = "\33[37m"

    CBLACKBG = "\33[40m"
    CREDBG = "\33[41m"
    CGREENBG = "\33[42m"
    CYELLOWBG = "\33[43m"
    CBLUEBG = "\33[44m"
    CVIOLETBG = "\33[45m"
    CBEIGEBG = "\33[46m"
    CWHITEBG = "\33[47m"

    CGREY = "\33[90m"
    CRED2 = "\33[91m"
    CGREEN2 = "\33[92m"
    CYELLOW2 = "\33[93m"
    CBLUE2 = "\33[94m"
    CVIOLET2 = "\33[95m"
    CBEIGE2 = "\33[96m"
    CWHITE2 = "\33[97m"

    CGREYBG = "\33[100m"
    CREDBG2 = "\33[101m"
    CGREENBG2 = "\33[102m"
    CYELLOWBG2 = "\33[103m"
    CBLUEBG2 = "\33[104m"
    CVIOLETBG2 = "\33[105m"
    CBEIGEBG2 = "\33[106m"
    CWHITEBG2 = "\33[107m"


PieceUnicode: dict = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}


class Piece:
    name: str
    probability_tree: list[dict]

    def __init__(self, position: int = 0, name: str = " ") -> None:
        self.name = name

        self.probability_tree = [
            {"position": position, "probability": 1, "to_1": None, "to_2": None}
        ]

    def search_position_in_probability_tree(self, pos: int):
        for i, superposition in enumerate(self.probability_tree):
            if superposition["position"] == pos:
                return i

    def get_terminal_superpositions(self) -> list[int]:
        found: list[int] = []

        for i, superposition in enumerate(self.probability_tree):
            if (superposition["to_1"] is None) and (superposition["to_2"] is None):
                found.append(i)

        return found

    def move(
        self, from_1: int, to_1: int, to_2: int | None, k_1: float, k_2: float
    ) -> bool:
        from_i: int | None = self.search_position_in_probability_tree(from_1)
        to_1_searched: int | None = self.search_position_in_probability_tree(to_1)
        to_2_searched: int | None = None
        if to_2 is not None:
            to_2_searched = self.search_position_in_probability_tree(to_2)

        if to_1 == to_2:
            print(f"Err: {to_1} == {to_2}")
            input()
            return False

        if from_i is None:
            print(f"Err: {from_i} isn't a valid branch")
            input()
            return False

        from_branch: dict = self.probability_tree[from_i]

        if (from_branch["to_1"] is not None) or (from_branch["to_2"] is not None):
            print(f"Err: {from_i} isn't a terminal branch")
            input()
            return False

        if to_2 is None:
            if to_1_searched is None:
                self.probability_tree.append(
                    {
                        "position": to_1,
                        "probability": from_branch["probability"] * k_1,
                        "to_1": None,
                        "to_2": None,
                    }
                )
            else:
                self.probability_tree[to_1_searched]["probability"] += (
                    from_branch["probability"] * k_1
                )
                self.probability_tree[to_1_searched]["to_1"] = None
                self.probability_tree[to_1_searched]["to_2"] = None

            if k_1 == 1:
                self.probability_tree[from_i]["to_1"] = (
                    self.probability_tree.__len__() - 1
                )
            else:
                self.probability_tree[from_i]["probability"] *= 1 - k_1
            return True

        if to_1_searched is None:
            self.probability_tree.append(
                {
                    "position": to_1,
                    "probability": from_branch["probability"] / 2 * k_1,
                    "to_1": None,
                    "to_2": None,
                }
            )
        else:
            self.probability_tree[to_1_searched]["probability"] += (
                from_branch["probability"] / 2
            ) * k_1
            self.probability_tree[to_1_searched]["to_1"] = None
            self.probability_tree[to_1_searched]["to_2"] = None

        if to_2_searched is None:
            self.probability_tree.append(
                {
                    "position": to_2,
                    "probability": from_branch["probability"] / 2 * k_2,
                    "to_1": None,
                    "to_2": None,
                }
            )
        else:
            self.probability_tree[to_2_searched]["probability"] += (
                from_branch["probability"] / 2
            ) * k_2
            self.probability_tree[to_2_searched]["to_1"] = None
            self.probability_tree[to_2_searched]["to_2"] = None

        if k_1 == 1 and k_2 == 1:
            self.probability_tree[from_i]["to_1"] = self.probability_tree.__len__() - 2
            self.probability_tree[from_i]["to_2"] = self.probability_tree.__len__() - 1
        else:
            self.probability_tree[from_i]["probability"] = (
                1
                - self.probability_tree[from_i]["probability"] * k_2 / 2
                - self.probability_tree[from_i]["probability"] * k_1 / 2
            )

        return True

    def collapse(self) -> None:
        possible_locations: list[int] = self.get_terminal_superpositions()
        cumulative_probability: list[tuple[int, float, float]] = [(-1, 0, 0)]

        for i in possible_locations:
            branch: dict = self.probability_tree[i]
            cumulative_probability.append(
                (
                    i,
                    cumulative_probability[-1][2],
                    branch["probability"] + cumulative_probability[-1][2],
                )
            )

        collapsing_number: float = random()
        collapsed: int | None = None

        for j in cumulative_probability:
            if j[1] <= collapsing_number and collapsing_number < j[2]:
                collapsed = j[0]

        if collapsed is None:
            print("Err: collapsing algorithm not implemented properly")

            print(cumulative_probability)
            print(collapsing_number)
            print(collapsed)
            input()

            return

        self.probability_tree = [self.probability_tree[collapsed]]
        self.probability_tree[0]["probability"] = 1

    def __repr__(self) -> str:
        return PieceUnicode[self.name]


class Board:
    is_white_move: bool = True

    translations: dict = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }

    starting_board: str = (
        "rnbqkbnr"
        + "pppppppp"
        + "        "
        + "        "
        + "        "
        + "        "
        + "PPPPPPPP"
        + "RNBQKBNR"
    )

    def __init__(self) -> None:
        self.board: list[Piece | None] = []

        for i, piece in enumerate(self.starting_board):
            self.board.append(Piece(i, piece) if piece != " " else None)

    def calculate_line_of_sight_probability_BNQ(
        self, start_pos: int, end_pos: int, piece: str
    ) -> float:
        start_row: int = int(start_pos / 8)
        end_row: int = int(end_pos / 8)

        probability_scaling_factor: float = 1

        if piece.lower() == "b":
            is_top_left_bottom_right_diag: bool = False
            if start_pos % 9 == end_pos % 9:
                is_top_left_bottom_right_diag = True

            if start_row > end_row:
                for row in range(start_row - end_row - 1):
                    if is_top_left_bottom_right_diag:
                        cell = start_pos - 9 * (row + 1)
                    else:
                        cell = start_pos - 7 * (row + 1)

                    probability_scaling_factor *= 1 - self.get_piece_probability_at_pos(
                        cell
                    )

            else:
                for row in range(end_row - start_row - 1):
                    if is_top_left_bottom_right_diag:
                        cell = start_pos + 9 * (row + 1)
                    else:
                        cell = start_pos + 7 * (row + 1)

                    probability_scaling_factor *= 1 - self.get_piece_probability_at_pos(
                        cell
                    )

        if piece.lower() == "r":
            if start_row == end_row:
                if start_pos > end_pos:
                    for col in range(start_pos - end_pos - 1):
                        cell = start_pos - col + 1

                        probability_scaling_factor *= (
                            1 - self.get_piece_probability_at_pos(cell)
                        )

                if start_pos < end_pos:
                    for col in range(end_pos - start_pos - 1):
                        cell = start_pos - col - 1

                        probability_scaling_factor *= (
                            1 - self.get_piece_probability_at_pos(cell)
                        )

            if start_row > end_row:
                for row in range(start_row - end_row - 1):
                    cell = start_pos - 8 * (row + 1)

                    probability_scaling_factor *= 1 - self.get_piece_probability_at_pos(
                        cell
                    )

            else:
                for row in range(end_row - start_row - 1):
                    cell = start_row + 8 * (row + 1)

                    probability_scaling_factor *= 1 - self.get_piece_probability_at_pos(
                        cell
                    )

        if piece.lower() == "q":
            if start_pos % 9 == end_pos % 9 or start_pos % 7 == end_pos % 7:
                return self.calculate_line_of_sight_probability_BNQ(
                    start_pos, end_pos, "b"
                )
            else:
                return self.calculate_line_of_sight_probability_BNQ(
                    start_pos, end_pos, "r"
                )

        return probability_scaling_factor

    def get_piece_probability_at_pos(self, pos: int) -> float:
        for j, piece in enumerate(self.board):
            if piece is None:
                continue

            possible_locations: list[int] = piece.get_terminal_superpositions()

            for i in possible_locations:
                piece_location: int = piece.probability_tree[i]["position"]

                if piece_location == pos:
                    return piece.probability_tree[i]["probability"]

        return 0

    def cast_move_to_tuple(
        self, move: str
    ):  # move format = "e2e3e4" -> move piece at e2 to e3 and e4
        col_i: int = self.translations[move[0]]
        row_i: int = int(move[1]) - 1

        col_1: int = self.translations[move[2]]
        row_1: int = int(move[3]) - 1

        if move.__len__() == 6:
            col_2: int = self.translations[move[4]]
            row_2: int = int(move[5]) - 1
            return (row_i * 8 + col_i, row_1 * 8 + col_1, row_2 * 8 + col_2)

        return (row_i * 8 + col_i, row_1 * 8 + col_1, None)

    def move(self, move: str) -> bool:
        from_1: int
        to_1: int
        to_2: int | None

        from_1, to_1, to_2 = self.cast_move_to_tuple(move)

        piece_being_moved: Piece | None = None

        for piece in self.board:
            if piece is None:
                continue

            possible_locations: list[int] = piece.get_terminal_superpositions()

            for i in possible_locations:
                piece_location: int = piece.probability_tree[i]["position"]

                if piece_location == from_1:
                    piece_being_moved = piece

        if piece_being_moved is None:
            print("Err: Invalid move")
            input()
            return False

        scaling_factor_1: float = 1
        scaling_factor_2: float = 1

        if piece_being_moved.name in "bnqBNQ":
            scaling_factor_1 = self.calculate_line_of_sight_probability_BNQ(
                from_1, to_1, piece_being_moved.name
            )

            if to_2 is not None:
                scaling_factor_2 = self.calculate_line_of_sight_probability_BNQ(
                    from_1, to_2, piece_being_moved.name
                )

        if scaling_factor_1 == 0 or scaling_factor_2 == 0:
            print("Err: Line of sight blocked by a 100% piece")
            input()
            return False

        if to_2 is None and piece_being_moved.name.capitalize() == "K":
            print("Err: King can't be superposed")
            input()
            return False

        moved: bool = piece_being_moved.move(
            from_1, to_1, to_2, scaling_factor_1, scaling_factor_2
        )

        if not moved:
            return moved

        for j, piece in enumerate(self.board):
            if piece is None:
                continue

            possible_locations: list[int] = piece.get_terminal_superpositions()

            for i in possible_locations:
                piece_location: int = piece.probability_tree[i]["position"]

                if piece_location == to_1 or piece_location == to_2:
                    if piece_being_moved is not piece:
                        piece.collapse()
                        piece_being_moved.collapse()

                        if (
                            piece.probability_tree[0]["position"]
                            == piece_being_moved.probability_tree[0]["position"]
                        ):
                            self.board[j] = None

                    break

        return moved

    def draw(self):
        drawing_board: list[str] = ["\n\n\n" for _ in range(64)]

        for i, piece in enumerate(self.board):
            if piece is None:
                continue

            possible_locations: list[int] = piece.get_terminal_superpositions()

            for j in possible_locations:
                position: int = piece.probability_tree[j]["position"]
                probability: float = piece.probability_tree[j]["probability"]

                drawing_board[position] = f"""\

{piece}
{probability * 100:.3f}
"""

        print(
            f"{Colors.CYELLOW}"
            + "╭─────────"
            + "┬─────────" * 7
            + "╮"
            + f"{Colors.CEND}"
        )

        for row in range(8):
            lines: list[str] = [
                f"{Colors.CYELLOW}│{Colors.CEND}",
                f"{Colors.CYELLOW}│{Colors.CEND}",
                f"{Colors.CYELLOW}│{Colors.CEND}",
            ]

            for col in range(8):
                if (col + row) % 2 == 0:
                    lines[0] += (
                        f"{Colors.CBLACKBG}{drawing_board[row * 8 + col].split('\n')[0]:^9}{Colors.CEND}│"
                    )
                    lines[1] += (
                        f"{Colors.CBLACKBG}{drawing_board[row * 8 + col].split('\n')[1]:^9}{Colors.CEND}│"
                    )
                    lines[2] += (
                        f"{Colors.CBLACKBG}{drawing_board[row * 8 + col].split('\n')[2]:^9}{Colors.CEND}│"
                    )
                else:
                    lines[0] += f"{drawing_board[row * 8 + col].split('\n')[0]:^9}│"
                    lines[1] += f"{drawing_board[row * 8 + col].split('\n')[1]:^9}│"
                    lines[2] += f"{drawing_board[row * 8 + col].split('\n')[2]:^9}│"

            for line in lines:
                print(f"{line}  {row + 1}")

            if row != 7:
                print(
                    f"{Colors.CYELLOW}├{Colors.CEND}"
                    + "─────────"
                    + "┼─────────" * 7
                    + "┤"
                )
            else:
                print(
                    f"{Colors.CYELLOW}"
                    + "╰─────────"
                    + "┴─────────" * 7
                    + "╯"
                    + f"{Colors.CEND}"
                )

        print(
            f" {'a':^9} {'b':^9} {'c':^9} {'d':^9} {'e':^9} {'f':^9} {'g':^9} {'h':^9}"
        )

    def start(self):
        while True:
            self.clear()

            self.draw()
            print("\n")

            print(f"{Colors.CWHITEBG + Colors.CBLACK + ' White ' + Colors.CEND if self.is_white_move else Colors.CBLACKBG + Colors.CWHITE + ' Black ' + Colors.CEND }'s turn")

            move: str = input("Enter your move (eg. e2e3e4 or e2e4): ")

            try:
                moved: bool = self.move(move)
            except Exception:
                continue

            if moved:
                self.is_white_move = not self.is_white_move

    def clear(self) -> None:
        if os_name == "nt":
            system("cls")
        elif os_name == "posix":
            system("clear")


game: Board = Board()

game.start()
