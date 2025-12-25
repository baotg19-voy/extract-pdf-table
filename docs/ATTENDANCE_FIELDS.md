# Attendance Fields (出勤簿)

## Field Reference

| Field | Japanese | Type | Description |
|-------|----------|------|-------------|
| employee_id | 社員ID | string | 6-digit employee ID |
| name | 氏名 | string | Employee name |
| shukkin | 出勤 | object | Working days `{count, amount: 0}` |
| kokyu | 公休 | object | Rest days `{count, amount: 0}` |
| kado_jikan | 稼働時間 | string | Working hours `HHH:MM` |
| kihon_kyu | 基本給 | object | Basic salary |
| hosho_zangyo | 保障残業 | object | Guaranteed overtime |
| josha_teate | 乗車手当 | object | Boarding allowance |
| sagawa_warimashi_teate | 佐川割増手当 | object | Sagawa markup |
| double_teate | ダブル手当 | object | Double shift allowance |
| rinji_teate | 臨時手当 | object | Temporary allowance |
| yakin_teate | 夜勤手当 | object | Night shift allowance |
| kyujitsu_teate | 休日手当 | object | Holiday allowance |
| chokyori_teate | 長距離手当 | object | Long distance allowance |
| sonota | その他 | object | Other |
| kei | 計 | integer | Total salary |

## Example Record

```json
{
  "employee_id": "160013",
  "name": "江頭 孝之",
  "shukkin": {"count": 28, "amount": 0},
  "kokyu": {"count": 3, "amount": 0},
  "kado_jikan": "396:59",
  "kihon_kyu": {"count": 28, "amount": 190400},
  "hosho_zangyo": {"count": 28, "amount": 70000},
  "josha_teate": {"count": 28, "amount": 28000},
  "sagawa_warimashi_teate": {"count": 17, "amount": 55500},
  "double_teate": {"count": 28, "amount": 435400},
  "rinji_teate": {"count": 1, "amount": 3000},
  "yakin_teate": {"count": 39, "amount": 39000},
  "kyujitsu_teate": {"count": 2, "amount": 5200},
  "chokyori_teate": {"count": 0, "amount": 0},
  "sonota": {"count": 0, "amount": 0},
  "kei": 884900
}
```

## Notes

- Allowance fields: `{count: occurrences, amount: yen}`
- `shukkin` and `kokyu`: amount is always 0
- `kyujitsu_teate`: count = amount ÷ 2600
