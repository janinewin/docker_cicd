from typing import Union



def is_comment_line(line: str, comment_chars: str):
    """
    Returns true if the line starts with `comment_chars`.
    Strips first spaces from the left of the `line`
    """
    return line.lstrip().startswith(comment_chars)


def soft_equal_transform(txt: str, comment_chars: Union[str, None]) -> str:
    """
    Remove comments and transform newlines into spaces
    """
    txt_no_comment_no_newline = (
        txt.replace("\n", " ")
        if comment_chars is None
        else " ".join([line for line in txt.split("\n") if not is_comment_line(line, comment_chars)])
    )
    # Removes duplicate spaces and tabs
    return txt_no_comment_no_newline.replace("\t", "").replace(" ", "")


def soft_equal(a: str, b: str, comment_chars: Union[str, None] = None):
    """
    Two strings are soft-equal if
    - after removing all lines starting with the `comment_chars` (# in Python, -- in SQL)
    - transforming new lines in spaces
    - removing all spaces

    they're equal
    """
    tr_a = soft_equal_transform(a, comment_chars=comment_chars)
    tr_b = soft_equal_transform(b, comment_chars=comment_chars)
    return tr_a == tr_b
