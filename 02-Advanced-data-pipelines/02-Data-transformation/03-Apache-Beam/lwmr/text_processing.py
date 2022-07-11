from typing import List

import nltk

# Download the corpus the first time
nltk.download('punkt', quiet=True)


def get_words(txt: str) -> List[str]:
    """
    Extracts words from text
    """
    return nltk.word_tokenize(txt)
