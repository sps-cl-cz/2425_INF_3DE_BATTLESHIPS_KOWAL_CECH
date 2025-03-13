import random

SHIP_LENGTHS = {
    1: [(0, 0), (1, 0)],
    2: [(0, 0), (1, 0), (2, 0)],
    3: [(0, 0), (1, 0), (2, 0), (3, 0)],
    4: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    5: [(0, 0), (1, 0), (2, 0), (2, 1)],
    6: [(0, 0), (0, 1), (0, 2)],
    7: [(0, 0), (0, 1)]
}

class BoardSetup:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.ship_positions = {}  # {ship_id: [(x1, y1), (x2, y2), ...]}

    def get_board(self) -> list[list[int]]:
        return self.board

    def get_tile(self, x: int, y: int) -> int:
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            raise IndexError("Coordinates out of bounds")
        return self.board[y][x]

    def place_ships(self) -> None:
        for ship_id, count in self.ships_dict.items():
            for _ in range(count):
                placed = False
                while not placed:
                    x = random.randint(0, self.cols - 1)
                    y = random.randint(0, self.rows - 1)
                    if self._can_place_ship(x, y, ship_id):
                        self._place_ship(x, y, ship_id)
                        placed = True

    def _can_place_ship(self, x, y, ship_id) -> bool:
        shape = SHIP_LENGTHS.get(ship_id)
        if not shape:
            return False
        try:
            # Check for ship overlap
            for dx, dy in shape:
                if self.board[y + dy][x + dx] != 0:
                    return False
            # Check for neighboring ships (excluding diagonal corners)
            for dx, dy in shape:
                for nx, ny in [(dx - 1, dy), (dx + 1, dy), (dx, dy - 1), (dx, dy + 1)]:
                    if 0 <= x + nx < self.cols and 0 <= y + ny < self.rows:
                        if self.board[y + ny][x + nx] != 0:
                            return False
            return True
        except IndexError:
            return False

    def _place_ship(self, x, y, ship_id) -> None:
        shape = SHIP_LENGTHS.get(ship_id)
        self.ship_positions.setdefault(ship_id, [])
        for dx, dy in shape:
            self.board[y + dy][x + dx] = ship_id
            self.ship_positions[ship_id].append((x + dx, y + dy))

    def reset_board(self) -> None:
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.ship_positions.clear()

    def board_stats(self) -> dict:
        empty = sum(cell == 0 for row in self.board for cell in row)
        occupied = self.rows * self.cols - empty
        return {"empty_spaces": empty, "occupied_spaces": occupied}

    def get_ship_positions(self, ship_id: int) -> list[tuple[int, int]]:
        """
        Returns a list of (x, y) positions for the given ship_id.
        """
        return self.ship_positions.get(ship_id, [])
