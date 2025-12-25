"""
Test allowance parser output against correct.json
Usage: python -m src.allowance.test
"""

import json
from pathlib import Path


def compare_records(actual, expected):
    """Compare two JSON records and return differences"""
    issues = []
    
    if len(actual) != len(expected):
        issues.append(f"Record count mismatch: got {len(actual)}, expected {len(expected)}")
        return issues
    
    for i, (act_rec, exp_rec) in enumerate(zip(actual, expected)):
        emp_id = act_rec.get('employee_id', 'unknown')
        
        exp_keys = set(exp_rec.keys())
        act_keys = set(act_rec.keys())
        
        missing_keys = exp_keys - act_keys
        extra_keys = act_keys - exp_keys
        
        if missing_keys:
            issues.append(f"Employee {emp_id}: Missing keys {missing_keys}")
        if extra_keys:
            issues.append(f"Employee {emp_id}: Extra keys {extra_keys}")
        
        for key in exp_keys & act_keys:
            exp_val = exp_rec[key]
            act_val = act_rec[key]
            
            if exp_val != act_val:
                issues.append(f"Employee {emp_id}, field '{key}': got {act_val}, expected {exp_val}")
    
    return issues


def test():
    """Test allowance parser output against correct.json"""
    print("\n" + "=" * 70)
    print("TESTING ALLOWANCE PARSER")
    print("=" * 70 + "\n")
    
    actual_path = 'output/allowance/driver_allowance.json'
    expected_path = 'output/allowance/correct.json'
    
    if not Path(actual_path).exists():
        print(f"❌ Error: {actual_path} not found. Run extraction first.")
        return False
    
    if not Path(expected_path).exists():
        print(f"❌ Error: {expected_path} not found.")
        return False
    
    with open(actual_path, 'r', encoding='utf-8') as f:
        actual = json.load(f)
    
    with open(expected_path, 'r', encoding='utf-8') as f:
        expected = json.load(f)
    
    print(f"Loaded {len(actual)} actual records")
    print(f"Loaded {len(expected)} expected records\n")
    
    issues = compare_records(actual, expected)
    
    if not issues:
        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("Structure and data match perfectly with correct.json")
        return True
    else:
        print("=" * 70)
        print(f"❌ FOUND {len(issues)} ISSUES:")
        print("=" * 70)
        for issue in issues[:20]:
            print(f"  • {issue}")
        if len(issues) > 20:
            print(f"\n  ... and {len(issues) - 20} more issues")
        return False


if __name__ == "__main__":
    import sys
    success = test()
    sys.exit(0 if success else 1)
