import re

import nltk

from nltk.corpus import stopwords
from nltk.tokenize import (
    sent_tokenize,
    word_tokenize
)


# =========================================================
# DOWNLOAD REQUIRED NLTK DATA
# =========================================================

nltk.download(
    "punkt",
    quiet=True
)

nltk.download(
    "punkt_tab",
    quiet=True
)

nltk.download(
    "stopwords",
    quiet=True
)


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):
    """Clean privacy policy text."""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# SPLIT SENTENCES
# =========================================================

def split_sentences(text):
    """Split text into individual sentences."""

    return sent_tokenize(text)


# =========================================================
# TOKENIZE TEXT
# =========================================================

def tokenize_text(sentence):
    """Convert a sentence into useful tokens."""

    words = word_tokenize(
        sentence
    )

    stop_words = set(
        stopwords.words("english")
    )

    tokens = [
        word
        for word in words
        if word.isalnum()
        and word not in stop_words
    ]

    return tokens
