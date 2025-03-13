import random

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]

    def get_next_attack(self) -> tuple[int, int]:
        # Calculate probability map
        prob_map = self._calculate_probability_map()

        # Find the highest probability cell
        best_x, best_y = max(
            ((x, y) for y in range(self.rows) for x in range(self.cols) if self.enemy_board[y][x] == '?'),
            key=lambda pos: prob_map[pos[1]][pos[0]],
        )

        return best_x, best_y

    def _calculate_probability_map(self) -> list[list[int]]:
        prob_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for ship_length in self.ships_dict.values():
            if ship_length > 0:
                # Horizontal placement
                for y in range(self.rows):
                    for x in range(self.cols - ship_length + 1):
                        if all(self.enemy_board[y][x + i] == '?' for i in range(ship_length)):
                            for i in range(ship_length):
                                prob_map[y][x + i] += 1

                # Vertical placement
                for x in range(self.cols):
                    for y in range(self.rows - ship_length + 1):
                        if all(self.enemy_board[y + i][x] == '?' for i in range(ship_length)):
                            for i in range(ship_length):
                                prob_map[y + i][x] += 1

        return prob_map

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        if is_hit:
            self.enemy_board[y][x] = 'H'
            if is_sunk:
                self._mark_sunk(x, y)
        else:
            self.enemy_board[y][x] = 'M'

    def _mark_sunk(self, x, y):
        self.enemy_board[y][x] = 'S'
        for ship_id in self.ships_dict:
            if self.ships_dict[ship_id] > 0:
                self.ships_dict[ship_id] -= 1
                break

        # Mark surrounding cells as 'X' to avoid future shots
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.enemy_board[ny][nx] == '?':
                self.enemy_board[ny][nx] = 'X'

    def get_enemy_board(self) -> list[list[str]]:
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        return self.ships_dict

    def all_ships_sunk(self) -> bool:
        return all(count == 0 for count in self.ships_dict.values())
