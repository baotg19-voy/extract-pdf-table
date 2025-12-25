"""Number and text extraction utilities for attendance parsing"""

import re


def extract_all_numbers(text):
    """Extract ALL numbers from multi-line text"""
    if not text:
        return []
    numbers = re.findall(r'\d+', str(text))
    return [int(n) for n in numbers]


def clean_number(text):
    """Extract first number from text"""
    if not text:
        return None
    text = str(text).replace(',', '').replace(' ', '').strip()
    match = re.search(r'\d+', text)
    return int(match.group(0)) if match else None


def extract_time_format(text):
    """Extract HH:MM time format"""
    if not text:
        return None
    match = re.search(r'(\d{1,2}):(\d{2})', str(text))
    return match.group(0) if match else None


def filter_label_numbers(numbers, max_label=50):
    """Remove label row numbers (typically < 50)"""
    return [n for n in numbers if n > max_label]
