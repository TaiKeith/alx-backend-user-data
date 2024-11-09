#!/usr/bin/env python3
"""
Tasks module
"""
import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize with fields to redact"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with redacted sensitive fields"""
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)
