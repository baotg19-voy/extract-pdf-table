"""Field extractors for attendance data"""

import re
from .utils import extract_all_numbers, clean_number, extract_time_format, filter_label_numbers


def _extract_from_cell(df, label_idx, col_idx=1):
    """Helper: Extract count/amount from cell near label"""
    # Try different row offsets from the label
    for row_offset in [-2, -1, -3, 0]:
        row_idx = label_idx + row_offset
        if 0 <= row_idx < len(df):
            numbers = extract_all_numbers(df.iloc[row_idx, col_idx])
            numbers = filter_label_numbers(numbers)
            if len(numbers) >= 2:
                return {'count': numbers[0], 'amount': numbers[1]}
    return {'count': 0, 'amount': 0}


def extract_kihon_kyu(df, start_idx, label_idx):
    """Extract basic salary (count, amount)"""
    return _extract_from_cell(df, label_idx)


def extract_hosho_zangyo(df, start_idx, label_idx):
    """Extract guaranteed overtime (count, amount)"""
    return _extract_from_cell(df, label_idx)


def extract_standard_allowance(df, start_idx, label_idx):
    """Extract standard allowance (count, amount)"""
    return _extract_from_cell(df, label_idx)


def extract_shukkin_kokyu(df, start_idx, label_idx):
    """Extract working days and rest days (backward search)"""
    for offset in range(15):
        idx = start_idx - offset
        if idx < 0:
            break
        text = str(df.iloc[idx, 1])
        numbers = extract_all_numbers(text)
        numbers = filter_label_numbers(numbers)
        if len(numbers) >= 2:
            return {'shukkin': numbers[0], 'kokyu': numbers[1]}
    return {'shukkin': 0, 'kokyu': 0}


def extract_kado_jikan(df, start_idx, label_idx):
    """Extract working hours in HH:MM format"""
    for offset in range(20):
        idx = start_idx - offset
        if idx < 0:
            break
        text = str(df.iloc[idx, 1])
        time = extract_time_format(text)
        if time:
            return time
    return None


def extract_kyujitsu_teate(df, start_idx, label_idx):
    """Extract holiday allowance (3 strategies)"""
    # Strategy 1: 2 rows before label
    numbers = extract_all_numbers(df.iloc[label_idx - 2, 1])
    numbers = filter_label_numbers(numbers)
    if len(numbers) >= 2:
        return {'count': numbers[0], 'amount': numbers[1]}
    
    # Strategy 2: 1 row before label
    numbers = extract_all_numbers(df.iloc[label_idx - 1, 1])
    numbers = filter_label_numbers(numbers)
    if len(numbers) >= 2:
        return {'count': numbers[0], 'amount': numbers[1]}
    
    # Strategy 3: 3 rows before label
    numbers = extract_all_numbers(df.iloc[label_idx - 3, 1])
    numbers = filter_label_numbers(numbers)
    if len(numbers) >= 2:
        return {'count': numbers[0], 'amount': numbers[1]}
    
    return {'count': 0, 'amount': 0}


def extract_chokyori_teate(df, start_idx, label_idx):
    """Extract long distance allowance (3 strategies + 0 0 pattern)"""
    # Check for "0 0" pattern
    text_before = str(df.iloc[label_idx - 1, 1])
    if re.search(r'\b0\s+0\s*$', text_before):
        return {'count': 0, 'amount': 0}
    
    # Strategy 1: 2 rows before label
    numbers = extract_all_numbers(df.iloc[label_idx - 2, 1])
    numbers = filter_label_numbers(numbers)
    if len(numbers) >= 2:
        return {'count': numbers[-2], 'amount': numbers[-1]}
    
    # Strategy 2: 1 row before label
    numbers = extract_all_numbers(df.iloc[label_idx - 1, 1])
    numbers = filter_label_numbers(numbers)
    if len(numbers) >= 2:
        return {'count': numbers[-2], 'amount': numbers[-1]}
    
    # Strategy 3: 3 rows before label
    numbers = extract_all_numbers(df.iloc[label_idx - 3, 1])
    numbers = filter_label_numbers(numbers)
    if len(numbers) >= 2:
        return {'count': numbers[-2], 'amount': numbers[-1]}
    
    return {'count': 0, 'amount': 0}


def extract_sonota(df, start_idx, label_idx):
    """Extract other allowance"""
    numbers = extract_all_numbers(df.iloc[label_idx - 2, 1])
    numbers = filter_label_numbers(numbers)
    return {
        'count': numbers[0] if len(numbers) > 0 else 0,
        'amount': numbers[1] if len(numbers) > 1 else 0
    }
