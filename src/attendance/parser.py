import camelot
import pandas as pd
import re
from typing import Dict, List, Any


def extract_all_numbers(text):
    if not text or pd.isna(text):
        return []
    text_str = str(text).replace(',', '').replace(' ', '')
    numbers = re.findall(r'\d+', text_str)
    return [int(n) for n in numbers]


def is_spaced_digit_garbage(text):
    """Check if text is a spaced-digit garbage pattern like '1 0 0', '1 8 0', '0 0 0'"""
    text = text.strip()
    if not text:
        return False
    # Pattern: single digits separated by spaces (e.g., "1 0 0", "1 8 0")
    parts = text.split()
    if len(parts) >= 2:
        return all(len(p) <= 2 and p.isdigit() for p in parts)
    return False


def extract_count_from_spaced_garbage(text):
    """
    Extract potential count from spaced-digit pattern.
    Pattern like '1 8 0' may have count=8 (middle digit).
    Pattern like '1 9 0' may have count=19 (first+second digits).
    """
    text = text.strip()
    parts = text.split()
    if len(parts) >= 2:
        # Check if it looks like "X count 0" pattern
        # The middle element(s) may be the count
        digits = [int(p) for p in parts if p.isdigit()]
        # Common pattern: X count 0 where X is 1 or 0 (formatting) and last is 0
        if len(digits) >= 3 and digits[-1] == 0:
            # Middle digit(s) may be count
            if digits[0] in [0, 1] and digits[1] > 0:
                return digits[1]
    return None


def extract_salary_field_from_rows(rows_data, field_label):
    """
    Extract count and amount for a salary field from a list of row data.
    Each row_data is the raw cell content from column 6.
    This preserves the cell structure to handle both formats:
    - Standard: 'label\\n...\\ncount\\namount' (label at start)
    - Reversed: '...\\ncount\\namount\\nlabel' (label at end)
    """
    for row_data in rows_data:
        if field_label in row_data:
            # Found the field in this cell
            parts = row_data.split('\n')
            
            # Special handling for fields that may have garbage data patterns
            if field_label in ['長距離手当', 'その他', '休日手当']:
                # Check for spaced-digit garbage and try to extract count from it
                garbage_count = None
                clean_parts = []
                for part in parts:
                    if is_spaced_digit_garbage(part):
                        # Try to extract count from this garbage
                        extracted = extract_count_from_spaced_garbage(part)
                        if extracted is not None:
                            garbage_count = extracted
                    else:
                        clean_parts.append(part)
                
                # Extract numbers from clean parts only
                clean_text = '\n'.join(clean_parts)
                all_nums = extract_all_numbers(clean_text)
                
                # For 長距離手当, special handling for "garbage + label + amount" format
                if field_label == '長距離手当':
                    # If after cleaning we only have the label and maybe some amounts
                    if len(all_nums) == 0 or (len(all_nums) <= 2 and all(n == 0 for n in all_nums)):
                        return {'count': 0, 'amount': 0}
                    if len(all_nums) >= 2:
                        # Standard format with count and amount at end
                        return {'count': all_nums[-2], 'amount': all_nums[-1]}
                    elif len(all_nums) == 1:
                        # Only amount found - use garbage_count if we extracted it
                        if garbage_count is not None:
                            return {'count': garbage_count, 'amount': all_nums[0]}
                        return {'count': 0, 'amount': all_nums[0]}
                
                # For その他
                if field_label == 'その他':
                    if len(all_nums) == 0 or (len(all_nums) <= 2 and all(n == 0 for n in all_nums)):
                        return {'count': 0, 'amount': 0}
                    if len(all_nums) >= 2:
                        return {'count': all_nums[-2], 'amount': all_nums[-1]}
                    elif len(all_nums) == 1:
                        return {'count': 0, 'amount': all_nums[0]}
                
                # Special handling for 休日手当: count = amount / 2600
                if field_label == '休日手当':
                    if len(all_nums) >= 1:
                        amount = all_nums[-1]
                        count = amount // 2600 if amount > 0 else 0
                        return {'count': count, 'amount': amount}
                    return {'count': 0, 'amount': 0}
            
            # Standard extraction for other fields
            all_nums = extract_all_numbers(row_data)
            
            if len(all_nums) >= 2:
                # Last two numbers are count and amount
                return {'count': all_nums[-2], 'amount': all_nums[-1]}
            elif len(all_nums) == 1:
                return {'count': 0, 'amount': all_nums[0]}
            else:
                return {'count': 0, 'amount': 0}
    
    return {'count': 0, 'amount': 0}


def extract_salary_field(col6_text, field_label):
    """
    Legacy function for compatibility - works on combined text.
    """
    lines = col6_text.split('\n')
    
    try:
        label_idx = None
        for idx, line in enumerate(lines):
            if field_label in line:
                label_idx = idx
                break
        
        if label_idx is None:
            return {'count': 0, 'amount': 0}
        
        label_line = lines[label_idx]
        
        # Get all numbers from the label line
        all_nums = extract_all_numbers(label_line)
        
        if len(all_nums) >= 2:
            return {'count': all_nums[-2], 'amount': all_nums[-1]}
        elif len(all_nums) == 1:
            return {'count': 0, 'amount': all_nums[0]}
        
        # No numbers on label line - check lines after 
        field_labels = ["基 本 給", "基本給", "保障残業", "乗車手当", "佐川割増手当",
                        "ダブル手当", "臨時手当", "夜勤手当", "休日手当", "長距離手当",
                        "その他", "計", "稼働時間"]
        
        numbers = []
        for idx in range(label_idx + 1, len(lines)):
            line = lines[idx].strip()
            
            is_field_label = False
            for label in field_labels:
                if label in line and label != field_label:
                    is_field_label = True
                    break
            if is_field_label:
                break
            
            line_numbers = extract_all_numbers(line)
            numbers.extend(line_numbers)
        
        if len(numbers) >= 2:
            return {'count': numbers[-2], 'amount': numbers[-1]}
        elif len(numbers) == 1:
            return {'count': 0, 'amount': numbers[0]}
        else:
            return {'count': 0, 'amount': 0}
    except Exception as e:
        print(f"  Error extracting {field_label}: {e}")
        return {'count': 0, 'amount': 0}


def parse_pdf(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
    
    if not tables or len(tables) == 0:
        raise ValueError("No tables found in PDF")
    
    employees = []
    
    for table_idx, table_obj in enumerate(tables):
        table = table_obj.df
        print(f"Processing table {table_idx + 1}/{len(tables)}, shape: {table.shape}")
        
        # Find ALL employee rows in this table
        employee_rows = []
        for row_idx in range(len(table)):
            for col_idx in range(min(3, len(table.columns))):
                cell = str(table.iloc[row_idx, col_idx])
                if re.search(r'\b(\d{6})\b', cell):
                    employee_rows.append(row_idx)
                    break
        
        print(f"  Found {len(employee_rows)} employees at rows: {employee_rows}")
        
        # Process each employee
        for emp_idx, employee_row in enumerate(employee_rows):
            employee_id = None
            name = None
            
            for col_idx in range(min(3, len(table.columns))):
                cell = str(table.iloc[employee_row, col_idx])
                
                employee_id_match = re.search(r'\b(\d{6})\b', cell)
                if employee_id_match:
                    employee_id = employee_id_match.group(1)
                    
                    lines = cell.split('\n')
                    skip = ['出勤', '公休', '有給', '欠勤', '遅刻', '早退', '運転手', '無欠']
                    for line in lines:
                        line = line.strip()
                        if line in skip or re.match(r'^[A-Z0-9ｱ-ﾝァ-ヶー]+$', line):
                            continue
                        name_match = re.search(r'([一-龯ぁ-んァ-ヶー]+\s+[一-龯ぁ-んァ-ヶー]+)', line)
                        if name_match:
                            name = name_match.group(1).strip()
                            break
                    break
            
            if not employee_id:
                continue
            
            print(f"    Employee: {employee_id} - {name}")
            
            if len(table.columns) <= 6:
                continue
            
            # Determine end row for this employee (next employee row or +14)
            start_row = employee_row
            if emp_idx + 1 < len(employee_rows):
                end_row = employee_rows[emp_idx + 1]
            else:
                end_row = min(employee_row + 14, len(table))
            
            kado_jikan = ""
            col6_rows = []  # Store raw row data (not combined)
            
            for row_idx in range(start_row, min(end_row, len(table))):
                col6_text = str(table.iloc[row_idx, 6])
                col6_rows.append(col6_text)
                
                if '稼働時間' in col6_text:
                    time_match = re.search(r'(\d+:\d+)', col6_text)
                    if time_match:
                        kado_jikan = time_match.group(1)
            
            col6_combined = '\n'.join(col6_rows)
            
            # Use row-based extraction for better format handling
            kihon_kyu = extract_salary_field_from_rows(col6_rows, '基 本 給')
            if kihon_kyu['count'] == 0 and kihon_kyu['amount'] == 0:
                kihon_kyu = extract_salary_field_from_rows(col6_rows, '基本給')
            
            hosho_zangyo = extract_salary_field_from_rows(col6_rows, '保障残業')
            josha_teate = extract_salary_field_from_rows(col6_rows, '乗車手当')
            sagawa_warimashi_teate = extract_salary_field_from_rows(col6_rows, '佐川割増手当')
            double_teate = extract_salary_field_from_rows(col6_rows, 'ダブル手当')
            rinji_teate = extract_salary_field_from_rows(col6_rows, '臨時手当')
            yakin_teate = extract_salary_field_from_rows(col6_rows, '夜勤手当')
            
            kyujitsu_teate = extract_salary_field_from_rows(col6_rows, '休日手当')
            
            chokyori_teate = extract_salary_field_from_rows(col6_rows, '長距離手当')
            sonota = extract_salary_field_from_rows(col6_rows, 'その他')
            
            kei_data = extract_salary_field_from_rows(col6_rows, '計')
            kei = kei_data['amount']
            
            lines = col6_combined.split('\n')
            shukkin_count = 0
            kokyu_count = 0
            
            # Parse the attendance line more carefully
            # Pattern: 出勤 出勤 ... N 公休 M ...
            # where N is shukkin count and M is kokyu count
            found_shukkin_num = False
            found_kokyu_keyword = False
            
            for line in lines[:25]:
                line = line.strip()
                if line == '出勤':
                    continue  # Skip individual attendance markers
                elif line == '公休':
                    found_kokyu_keyword = True
                    continue
                elif line and re.match(r'^\d+$', line):
                    num = int(line)
                    if not found_shukkin_num and 20 <= num <= 31:
                        shukkin_count = num
                        found_shukkin_num = True
                    elif found_kokyu_keyword and num <= 10:
                        # This is the kokyu count (right after 公休)
                        kokyu_count = num
                        break  # Done parsing attendance section
            
            employee_data = {
                'employee_id': employee_id,
                'name': name if name else "",
                'shukkin': {'count': shukkin_count if shukkin_count > 0 else 0, 'amount': 0},
                'kokyu': {'count': kokyu_count if kokyu_count > 0 else 0, 'amount': 0},
                'kado_jikan': kado_jikan,
                'kihon_kyu': kihon_kyu,
                'hosho_zangyo': hosho_zangyo,
                'josha_teate': josha_teate,
                'sagawa_warimashi_teate': sagawa_warimashi_teate,
                'double_teate': double_teate,
                'rinji_teate': rinji_teate,
                'yakin_teate': yakin_teate,
                'kyujitsu_teate': kyujitsu_teate,
                'chokyori_teate': chokyori_teate,
                'sonota': sonota,
                'kei': kei
            }
            
            employees.append(employee_data)
    
    return employees
