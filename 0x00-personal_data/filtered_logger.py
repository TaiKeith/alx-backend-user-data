#!/usr/bin/env python3
"""
Tasks module
"""
import re
from typing import List, Tuple
import logging
import os
import mysql.connector


# Define the PII_FIELDS constant with important PII fields from `user_data.csv`
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger with a RedactingFormatter to
    filter PII fields.

    Returns:
        logging.Logger: A configured logger object.
    """
    # Create a logger named "user_data"
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler with RedactingFormatter for logging output
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to a MySQL database using credentials from environment variables.

    Returns:
        MySQLConnection: A MySQL database connection object.
    """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=password,
        database=db_name
    )
    return connection
