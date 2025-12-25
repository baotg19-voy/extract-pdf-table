"""Allowance parser - working logic preserved, just refactored into src/allowance/"""

import camelot
import pandas as pd
import re


def clean_text(text):
    """Clean text"""
    if pd.isna(text) or text == '':
        return ''
    return str(text).strip()


def clean_number(text):
    """Extract number"""
    if pd.isna(text) or text == '':
        return ''
    text = str(text).replace(',', '').replace(' ', '').strip()
    match = re.search(r'[\d\.]+', text)
    return match.group(0) if match else ''


def parse_pdf(pdf_path):
    """Parse allowance PDF - WORKING LOGIC PRESERVED"""
    print(f"Extracting from: {pdf_path}")
    
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        print(f"✓ Used stream method - Found {len(tables)} table(s)")
    except:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        print(f"✓ Used lattice method - Found {len(tables)} table(s)")
    
    # Column mappings
    cols_37 = ['untenshu', 'sagawa_a', 'sagawa_b', 'sagawa_ba', 'sagawa_bb', 'sagawa_bba', 'sagawa_bbb', 'sagawa_bbba',
               'rinji_teate', 'chokyori_teate', 'joshu', 'ippan_a', 'ippan_b', 'ippan_ba', 'ippan_bb', 'ippan_bba',
               'ippan_bbb', 'yontonsha_a', 'yontonsha_b', 'yontonsha_ba', 'yontonsha_bb', 'yontonsha_bba',
               'yontonsha_bbb', 'yontonsha_bbba', 'sagawa_ippan_b', 'sagawa_ippan_ba', 'sagawa_ippan_bb',
               'sagawa_ippan_bba', 'juyon_yonhei_b', 'juyon_yonhei_ba', 'juyon_yonhei_bb', 'juronton_yontonhei_bba',
               'lorry_a', 'lorry_b', 'lorry_ba', 'lorry_bb', 'gokei']
    
    cols_44 = ['untenshu', 'sagawa_a', 'sagawa_b', 'sagawa_ba', 'sagawa_bb', 'sagawa_bba', 'sagawa_bbb', 'sagawa_bbba',
               'rinji_teate', 'chokyori_teate', 'joshu', 'ippan_a', 'ippan_b', 'ippan_b', 'ippan_ba', 'ippan_ba',
               'ippan_bb', 'ippan_bb', 'ippan_bba', 'ippan_bbb', 'yontonsha_a', 'yontonsha_b', 'yontonsha_b',
               'yontonsha_ba', 'yontonsha_ba', 'yontonsha_bb', 'yontonsha_bba', 'yontonsha_bbb', 'yontonsha_bbba',
               'sagawa_ippan_b', 'sagawa_ippan_ba', 'sagawa_ippan_bb', 'sagawa_ippan_bba', 'juyon_yonhei_b',
               'juyon_yonhei_ba', 'juyon_yonhei_bb', 'juronton_yontonhei_bba', 'lorry_a', 'lorry_b', 'lorry_b',
               'lorry_ba', 'lorry_ba', 'lorry_bb', 'gokei']
    
    all_employees = []
    
    for tidx, table in enumerate(tables):
        print(f"\nProcessing table {tidx + 1} from page {table.page}...")
        df = table.df
        print(f"Table shape: {df.shape}")
        
        # Get columns
        num_cols = len(df.columns)
        cols = cols_37 if num_cols == 37 else (cols_44 if num_cols == 44 else cols_37[:num_cols] if num_cols <= 37 else cols_44[:num_cols])
        print(f"Using {len(cols)}-column mapping")
        
        # Find header
        header_idx = None
        for idx, row in df.iterrows():
            row_text = ' '.join([clean_text(str(cell)) for cell in row if pd.notna(cell)])
            if 'A' in row_text and 'B' in row_text and ('BA' in row_text or '手当' in row_text):
                header_idx = idx
                print(f"Found header row at index {idx}")
                break
        
        if header_idx is None:
            print("Could not find header row, skipping table")
            continue
        
        # Parse rows
        current = None
        for idx in range(header_idx + 1, len(df)):
            row = df.iloc[idx]
            first_col = clean_text(str(row.iloc[0]))
            
            # Employee ID
            if re.match(r'^\d{6}$', first_col):
                if current and current.get('shimei'):
                    all_employees.append(current)
                    print(f"  Extracted: {current.get('shimei')} (ID: {current.get('shain_id')})")
                
                current = {'shain_id': first_col}
                for col_idx in range(1, min(len(row), len(cols))):
                    value = clean_text(str(row.iloc[col_idx]))
                    if value and value not in ['', '-', '―', '－']:
                        field = cols[col_idx]
                        if field not in current:
                            num = clean_number(value)
                            current[field] = num if num else value
            
            # Name
            elif re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]{2,}', first_col):
                if current:
                    current['shimei'] = first_col
                    for col_idx in range(1, min(len(row), len(cols))):
                        value = clean_text(str(row.iloc[col_idx]))
                        if value and value not in ['', '-', '―', '－']:
                            field = cols[col_idx]
                            if field not in current:
                                num = clean_number(value)
                                current[field] = num if num else value
            
            # More data
            elif current:
                for col_idx in range(1, min(len(row), len(cols))):
                    value = clean_text(str(row.iloc[col_idx]))
                    if value and value not in ['', '-', '―', '－']:
                        field = cols[col_idx]
                        if field not in current:
                            num = clean_number(value)
                            current[field] = num if num else value
        
        # Last employee
        if current and current.get('shimei'):
            all_employees.append(current)
            print(f"  Extracted: {current.get('shimei')} (ID: {current.get('shain_id')})")
    
    print(f"\n✓ Extracted {len(all_employees)} employee records")
    return all_employees


def main():
    """Main entry point"""
    from pathlib import Path
    from ..common import save_json, save_csv, save_markdown
    
    pdf_path = "materials/運転手手当一覧表 - Untenshu teate ichiran hyō - Driver Allowance List.pdf"
    output_folder = 'output/allowance'
    
    print("=" * 100)
    employees = parse_pdf(pdf_path)
    
    if employees:
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        save_json(employees, f'{output_folder}/driver_allowance.json')
        save_csv(employees, f'{output_folder}/driver_allowance.csv')
        save_markdown(employees, f'{output_folder}/driver_allowance.md', 'Driver Allowance List')
        print(f"\n✓ Complete! {len(employees)} records → {output_folder}/")
    else:
        print("\n✗ No data found")
