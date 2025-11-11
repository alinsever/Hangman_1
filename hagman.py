import pandas as pd
import string
import getpass



class SecretWord:
    """
    Represents the secret word that player 2 must guess.
    Responsible for storing the word, tracking revealed letters,
    and revealing them after correct guesses.
    """

    def __init__(self, word: str):
        # Normalize case (make comparisons case-insensitive)
        self.word = word.lower()

        # Create a list of underscores, one per character in the word
        self.revealed = ["_" if ch.isalpha() else ch for ch in self.word]

        # Track unique alphabetic letters that must still be guessed
        self.unique_letters = {ch for ch in self.word if ch.isalpha()}

        print(f"Secret word initialized with {len(self.word)} letters.")

    def guess(self, letter: str) -> bool:
        """Reveals the letter if present. Returns True if correct."""
        letter = letter.lower()
        if letter in self.unique_letters:
            self.unique_letters.remove(letter)
            # reveal all positions of this letter
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.revealed[i] = letter
            return True
        return False

    def display(self) -> str:
        """Returns the current masked word with spaces."""
        return " ".join(self.revealed)

    def is_fully_revealed(self) -> bool:
        """True if all letters have been guessed."""
        return not self.unique_letters




class AsciiGallows:
    """Renders the hangman based on number of wrong guesses (0-8)."""
    STAGES = [
        "",
        "+-----.\n|     \n|     \n|     \n'-----",
        "+-----.\n|     O\n|     \n|     \n'-----",
        "+-----.\n|     O\n|     |\n|     \n'-----",
        "+-----.\n|     O\n|    /|\n|     \n'-----",
        "+-----.\n|     O\n|    /|\\\n|     \n'-----",
        "+-----.\n|     O\n|    /|\\\n|    / \n'-----",
        "+-----.\n|     O\n|    /|\\\n|    / \\\n'-----",
        "+-----.\n|     O\n|    /|\\\n|    / \\\n'----- #"
    ]

    @classmethod
    def render(cls, mistakes: int) -> str:
        mistakes = max(0, min(8, mistakes))
        return cls.STAGES[mistakes]
