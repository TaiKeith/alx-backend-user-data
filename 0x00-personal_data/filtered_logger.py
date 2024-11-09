#!/usr/bin/env python3
"""
Tasks module
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): A list of field names to be obfuscated.
        redaction (str): The string to replace field values with.
        message (str): The log message to be processed.
        separator (str): The character that separates fields in the log
                         message.

    Returns:
        str: The obfuscated log message with specified fields replaced by
             the redaction.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern,
                  lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)
