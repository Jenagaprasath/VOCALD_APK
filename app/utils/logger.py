"""Vocald - App-Wide Logger Setup"""
import logging
from kivy.logger import Logger


def setup_logger():
    """Initialize Vocald logger."""
    Logger.setLevel(logging.DEBUG)
    Logger.info("Vocald: Logger initialized")