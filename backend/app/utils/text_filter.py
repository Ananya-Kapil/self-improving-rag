from typing import Iterable
import re


MIN_CHUNK_LENGTH = 50


SKIP_KEYWORDS: Iterable[str] = (
    "table of contents",
    "contents",
    "acknowledgement",
    "acknowledgment",
    "certificate",
    "index",
    "candidate's declaration",
    "declaration",
)


def is_table_of_contents(chunk: str) -> bool:
    """
    Detect table of contents style chunks.
    Example:
    1. Introduction ........ 2
    2. Methodology ........ 5
    """

    lines = chunk.split("\n")

    toc_lines = 0

    for line in lines:
        line = line.strip()

        # Detect lines ending with page numbers
        if re.search(r"\d+\s*$", line):

            # Count numbered sections
            if re.search(r"^\d+[\.\)]", line):
                toc_lines += 1

    # If multiple lines look like TOC entries
    return toc_lines >= 3


def should_skip_chunk(chunk: str) -> bool:

    if not chunk:
        return True

    cleaned = chunk.strip()

    if len(cleaned) < MIN_CHUNK_LENGTH:
        return True

    normalized = cleaned.lower()


    # Keyword based filtering
    for keyword in SKIP_KEYWORDS:
        if keyword in normalized:
            return True


    # Pattern based filtering
    if is_table_of_contents(cleaned):
        return True


    return False