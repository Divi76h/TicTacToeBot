import numpy as np
import random


class TicTacToe:
    def __init__(self):
        self.boardStatus = np.full(shape=(3, 3), fill_value="-")
        self.asciiStart = 65

        while True:
            try:
                option = int(input("1) X: plays first\n"
                                   "2) O: plays second\n"
                                   "3) Random\n"
                                   "What do you want to play as: "))
                if 0 < option < 4:
                    break
                else:
                    print("option can only be 1, 2 or 3")
            except:
                print("invalid option")
        if option == 1:
            self.player = "X"
            self.computer = "O"
        elif option == 2:
            self.player = "O"
            self.computer = "X"
        elif option == 3:
            self.player = "X" if random.randrange(2) == 0 else "O"
            self.computer = "X" if self.player == "O" else "O"

        self.playersLastMove = None
        self.computersLastMove = None

        self.computerFirstCorner = None
        self.badCorner = None

        self.turn = 0

        self.tie = False
        self.Xwins = False
        self.Owins = False

        self.playerPlayAdjToComputer = False
        self.isPlayerFirstMoveCorner = False

        self.corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
        self.edges = [[0, 1], [1, 0], [1, 2], [2, 1]]

        self.oppCornerDict = {(0, 0): (2, 2), (0, 2): (2, 0)}
        self.computerCornerAdj = {(0, 0): ([0, 1], [1, 0]), (0, 2): ([0, 1], [1, 2]),
                                  (2, 0): ([1, 0], [2, 1]), (2, 2): ([2, 1], [1, 2])}
        self.ansIfPlayerPlaysComputerCornerAdj = {((0, 0), (0, 1)): (2, 0), ((0, 0), (1, 0)): (0, 2),
                                                  ((0, 2), (0, 1)): (2, 2), ((0, 2), (1, 2)): (0, 0),
                                                  ((2, 0), (1, 0)): (2, 2), ((2, 0), (2, 1)): (0, 0),
                                                  ((2, 2), (2, 1)): (0, 2), ((2, 2), (1, 2)): (2, 0)}

    def Display(self):
        # First row
        print()
        print("  ", end='')
        for j in range(len(self.boardStatus)):
            print(f"| {j + 1} ", end='')
        print("| ")
        print(f'{(4 * 4) * "-"}')

        # Other rows
        for i in range(len(self.boardStatus)):
            print(f"{chr(self.asciiStart + i)} ", end='')
            for j in range(3):
                print(f"| {self.boardStatus[i][j]} ", end='')
            print("| ")
            print(f'{(4 * 4) * "-"}')

    def IsWinner(self, player):
        for i in range(len(self.boardStatus)):
            if self.boardStatus[i][0] == self.boardStatus[i][1] == self.boardStatus[i][2] == player:
                return True
            if self.boardStatus[0][i] == self.boardStatus[1][i] == self.boardStatus[2][i] == player:
                return True

        if self.boardStatus[0][0] == self.boardStatus[1][1] == self.boardStatus[2][2] == player:
            return True

        if self.boardStatus[0][2] == self.boardStatus[1][1] == self.boardStatus[2][0] == player:
            return True

        return False

    def IsBoardFilled(self):
        for row in self.boardStatus:
            for item in row:
                if item == '-':
                    return False
        return True

    def IsPositionOccupied(self, position):
        return False if self.boardStatus[position[0]][position[1]] == "-" else True

    def IsGameover(self):
        self.Xwins = self.IsWinner('X')
        if not self.Xwins:
            self.Owins = self.IsWinner('O')

        self.tie = self.IsBoardFilled()

        gameover = self.Xwins or self.Owins or self.tie

        if self.computer == 'X':
            if self.Xwins:
                print("Computer wins as 'X'")
            elif self.Owins:
                print("Player wins as 'O'")
        elif self.computer == 'O':
            if self.Owins:
                print("Computer wins as 'O'")
            elif self.Xwins:
                print("Player wins as 'X'")
        elif self.tie:
            print('Its a tie')

        return gameover

    def Move(self, position, player):
        self.boardStatus[position[0], position[1]] = player

    def RawPositionToLogical(self, rawPosition):
        return [ord(rawPosition[0].upper()) - self.asciiStart, int(rawPosition[1]) - 1]

    def InputCheck(self, position):
        if position[0].isalpha() and position[1].isnumeric():
            return self.RawPositionToLogical(position)
        elif position[0].isnumeric() and position[1].isalpha():
            return self.RawPositionToLogical([position[1], position[0]])
        else:
            raise ValueError

    def Input(self):
        while True:
            position = input("enter position where you want to play: ")
            try:
                if len(position) == 3:
                    position = self.InputCheck(position.split(" "))
                    if not self.IsPositionOccupied(position):
                        self.playersLastMove = position
                        self.Move(position, self.player)
                        break
                    else:
                        print("position occupied")
                elif len(position) == 2:
                    position = self.InputCheck(list(position))
                    if not self.IsPositionOccupied(position):
                        self.playersLastMove = position
                        self.Move(position, self.player)
                        break
                    else:
                        print("position occupied")
                else:
                    print("invalid position")
            except:
                print("invalid position")

    def CanWin_PositionToWin(self, player):
        for i in range(len(self.boardStatus)):
            for j in range(len(self.boardStatus)):
                if self.boardStatus[i][j] == self.boardStatus[i][0 if j == 2 else j + 1] == player:
                    winPosition = [i, 2 if j == 0 else j - 1]
                    if not self.IsPositionOccupied(winPosition):
                        return True, winPosition
                if self.boardStatus[j][i] == self.boardStatus[0 if j == 2 else j + 1][i] == player:
                    winPosition = [2 if j == 0 else j - 1, i]
                    if not self.IsPositionOccupied(winPosition):
                        return True, winPosition

        for i in range(len(self.boardStatus)):
            if self.boardStatus[i][i] == self.boardStatus[0 if i == 2 else 1 + i][0 if i == 2 else i + 1] == player:
                winPosition = [2 if i == 0 else i - 1, 2 if i == 0 else i - 1]
                if not self.IsPositionOccupied(winPosition):
                    return True, winPosition
            if self.boardStatus[0 if i == 2 else i][2 if i == 0 else i] == self.boardStatus[2 if i == 2 else i + 1][
                1 if i == 0 else 0] == player:
                winPosition = [2 if i == 0 else i - 1, 1 if i == 2 else i + i]
                if not self.IsPositionOccupied(winPosition):
                    return True, winPosition

        return False, [None]

    def EmptyCorners(self, removeOppositeCorner=False):
        corners = []
        for corner in self.corners:
            if not self.IsPositionOccupied(corner):
                corners.append(corner)

        if removeOppositeCorner:
            try:
                corners.remove(self.OppositeToComputerFirstCorner())
            except:
                pass
        return corners

    def EmptyEdges(self):
        edges = []
        for edge in self.edges:
            if not self.IsPositionOccupied(edge):
                edges.append(edge)
        return edges

    def OppositeToComputerFirstCorner(self):
        if tuple(self.computerFirstCorner) in list(self.oppCornerDict.keys()):
            return list(self.oppCornerDict.get(tuple(self.computerFirstCorner)))
        elif tuple(self.computerFirstCorner) in list(self.oppCornerDict.values()):
            return list(list(self.oppCornerDict.keys())[
                            list(self.oppCornerDict.values()).index(tuple(self.computerFirstCorner))])

    def DidPlayerPlayClosestCornerToComputerFirstCorner(self):
        if (self.computerFirstCorner == [0, 0] or self.computerFirstCorner == [2, 2]) and self.playersLastMove in [
            [0, 2], [2, 0]]:
            return True
        elif (self.computerFirstCorner == [0, 2] or self.computerFirstCorner == [2, 0]) and self.playersLastMove in [
            [0, 0], [2, 2]]:
            return True

    def DidPlayerPlayAdjToComputerFirstCorner(self):
        if self.playersLastMove in self.computerCornerAdj.get(tuple(self.computerFirstCorner)):
            self.playerPlayAdjToComputer = True
            return True

    def RandomPlay(self):
        empty = []
        for i in range(len(self.boardStatus)):
            for j in range(len(self.boardStatus)):
                if not self.IsPositionOccupied([i, j]):
                    empty.append([i, j])
        return random.choice(empty)

    def BestPlay(self):
        if self.computer == 'X':
            if (self.boardStatus == np.full(shape=(3, 3), fill_value="-")).all():
                self.computerFirstCorner = random.choice(self.EmptyCorners())
                return self.computerFirstCorner
            elif self.turn == 1 and (
                    self.playersLastMove == [1, 1] or self.DidPlayerPlayClosestCornerToComputerFirstCorner()):
                return self.OppositeToComputerFirstCorner()
            elif self.turn == 1 and self.DidPlayerPlayAdjToComputerFirstCorner():
                return list(self.ansIfPlayerPlaysComputerCornerAdj.get(
                    (tuple(self.computerFirstCorner), tuple(self.playersLastMove))))
            elif self.turn == 2 and self.playerPlayAdjToComputer:
                return [1, 1]
            else:
                return random.choice(self.EmptyCorners(removeOppositeCorner=True))
        elif self.computer == "O":
            if self.turn == 1 and self.playersLastMove in self.corners:
                self.isPlayerFirstMoveCorner = True
                return [1, 1]
            elif self.isPlayerFirstMoveCorner and self.turn == 2 and self.playersLastMove in self.corners:
                return random.choice(self.EmptyEdges())
            elif self.turn == 1 and self.playersLastMove == [1, 1]:
                return random.choice(self.EmptyCorners())
            else:
                return self.RandomPlay()

    def Computer(self):
        canComputerWin_PositionToWin = self.CanWin_PositionToWin(self.computer)
        # print("Can Computer Win:", canComputerWin_PositionToWin)
        canPlayerWin_PositionToWin = self.CanWin_PositionToWin(self.player)

        if canComputerWin_PositionToWin[0]:
            self.Move(canComputerWin_PositionToWin[1], self.computer)
        elif canPlayerWin_PositionToWin[0]:
            self.Move(canPlayerWin_PositionToWin[1], self.computer)
        else:
            # print("\trying")
            position = self.BestPlay()
            # print("No error")
            # print("best calculated move:", position)
            self.computersLastMove = position
            self.Move(position, self.computer)

    def Start(self):
        print("\ncomputer starts" if self.player == "O" else "\nplayer starts")
        if self.computer == "X":
            pass
        else:
            self.Display()
        while True:
            if self.player == "X":
                self.Input()
                self.Display()
                if self.IsGameover():
                    break
            else:
                self.Computer()
                self.Display()
                if self.IsGameover():
                    break

            if self.player == "O":
                self.Input()
                self.Display()
                self.turn += 1
                if self.IsGameover():
                    break
            else:
                self.turn += 1
                self.Computer()
                self.Display()
                if self.IsGameover():
                    break
        self.WantToPlayAgain()

    def WantToPlayAgain(self):
        option = input("\nWant to play again? (y/n): ")
        if option.lower() in ["y", "yes"]:
            self.ResetAndStart()
        else:
            pass

    def ResetAndStart(self):
        self.__init__()
        self.Start()


if __name__ == "__main__":
    game = TicTacToe()
    game.Start()
