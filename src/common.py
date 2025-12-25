"""Common output functions"""

import json
import pandas as pd


def save_json(data, filepath):
    """Save to JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data, filepath):
    """Save to CSV"""
    pd.DataFrame(data).to_csv(filepath, index=False, encoding='utf-8-sig')


def save_markdown(data, filepath, title):
    """Save to Markdown"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\nTotal: {len(data)}\n\n")
        if data:
            keys = list(data[0].keys())
            f.write("| " + " | ".join(keys) + " |\n")
            f.write("|" + "|".join(["-"*(len(k)+2) for k in keys]) + "|\n")
            for item in data:
                f.write("| " + " | ".join([str(item.get(k, '')) for k in keys]) + " |\n")
