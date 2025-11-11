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




class StickmanDrawing:
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



class Hangman:
    """
    Controls the flow of the game:
    - Keeps track of correct and wrong guesses:
    - Knows remaning attempts
    - uses SecretWord to manage the hidden word
    """

     MAX_MISTAKES = 8

    def __init__(self, secret_word: str):
        self.secret = SecretWord(secret_word)
        self.wrong_letters = set()

    def remaining_attempts(self):
        return self.MAX_MISTAKES - len(self.wrong_letters)

    def is_lost(self):
        return len(self.wrong_letters) >= self.MAX_MISTAKES

    def is_won(self):
        return self.secret.is_fully_revealed()

    def guess(self, letter: str) -> bool:
        """Apply a guess. Returns True if correct."""
        if not letter or len(letter) != 1 or letter.lower() not in string.ascii_lowercase:
            print("⚠️  Please guess a single letter (A–Z).")
            return None
        letter = letter.lower()
        if letter in self.wrong_letters or letter in self.secret.revealed:
            print(f"⚠️  You already tried '{letter}'.")
            return None
        if self.secret.guess(letter):
            print(f"✅ Good guess: '{letter}' is in the word!")
            return True
        else:
            print(f"❌ Sorry: '{letter}' is not in the word.")
            self.wrong_letters.add(letter)
            return False

    def display_state(self):
        print(AsciiGallows.render(len(self.wrong_letters)))
        print(f"Word:    {self.secret.display()}")
        if self.wrong_letters:
            print(f"Wrong:   {' '.join(sorted(self.wrong_letters))}")
        print(f"Tries left: {self.remaining_attempts()}")
        print("-" * 32)

        
