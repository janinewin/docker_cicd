class Game:
    def __init__(self) -> list:
        """Attribute a random grid to size 9"""
        self.grid = None # TODO
        pass

    def is_valid(self, word: str) -> bool:
        """Return True if and only if the word is valid, given the Game's grid"""
        pass # TODO


game = Game()
print(game.grid) # --> OQUWRBAZE
my_word = "BAROQUE"
game.is_valid(my_word) # --> True
