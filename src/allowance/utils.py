"""Text utilities for allowance parsing"""

import pandas as pd
import re


def clean_text(text):
    """Clean text by removing extra whitespace"""
    if pd.isna(text) or text == '':
        return ''
    return str(text).strip()


def clean_number(text):
    """Extract number from text"""
    if pd.isna(text) or text == '':
        return ''
    text = str(text).replace(',', '').replace(' ', '').strip()
    match = re.search(r'[\d\.]+', text)
    return match.group(0) if match else ''


def is_employee_id(text):
    """Check if text is a 6-digit employee ID"""
    text = clean_text(text)
    return bool(re.match(r'^\d{6}$', text))


def is_japanese_name(text):
    """Check if text contains Japanese characters"""
    text = clean_text(text)
    return bool(re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]{2,}', text))


def is_empty(value):
    """Check if value is empty or placeholder"""
    if not value:
        return True
    value = str(value).strip()
    return value in ['', '-', '―', '－']
