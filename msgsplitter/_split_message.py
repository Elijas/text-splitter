from typing import List

from msgsplitter.exceptions import LengthLimitTooLowError
from msgsplitter.formatters.formatter_base import FormatterBase


def _get_this_message_length(i, j, chunk_lengths):
    text_character_count = sum(chunk_lengths[i:j + 1])
    space_character_count = j - i
    return text_character_count + space_character_count


def _get_groups(chunk_count, chunk_lengths, formatter):
    groups = []
    i = 0
    while i < chunk_count:
        last_j = None
        for j in range(i, chunk_count):
            message_length = _get_this_message_length(i, j, chunk_lengths)
            if formatter.is_message_too_long(message_length, len(groups) + 1):
                if last_j is None:
                    raise LengthLimitTooLowError
                groups.append((i, last_j))
                i = last_j + 1
                break
            if j == chunk_count - 1:
                groups.append((i, j))
                return groups
            last_j = j
    return groups


def split_message(message: str, formatter: FormatterBase) -> List[str]:
    """
    >>> split_message('', FormatterBase(length_limit=1))
    []
    >>> split_message('A', FormatterBase(length_limit=1))
    ['A']
    >>> split_message('A BC DEFG H I JK L', FormatterBase(length_limit=4))
    ['A BC', 'DEFG', 'H I', 'JK L']
    """
    chunks = message.split()
    chunk_lengths = list(map(len, chunks))
    chunk_count = len(chunk_lengths)

    return [' '.join(chunks[i:j + 1]) for i, j in _get_groups(chunk_count, chunk_lengths, formatter)]
