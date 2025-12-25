# Allowance Field Mapping (運転手手当一覧表)

This document describes the mapping between Japanese field names in the driver allowance PDF and their Romaji equivalents in the output data.

## Field Mapping Table

| Japanese Field | Romaji Field | Type | Description |
|---|---|---|---|
| 社員ID | shain_id | string | Employee identification number (6 digits) |
| 氏名 | shimei | string | Employee full name in Japanese |
| 運転手 | untenshu | string | Driver designation |
| 佐川 A | sagawa_a | string | Sagawa A category count |
| 佐川 B | sagawa_b | string | Sagawa B category count |
| 佐川 BA | sagawa_ba | string | Sagawa BA category count |
| 佐川 BB | sagawa_bb | string | Sagawa BB category count |
| 佐川 BBA | sagawa_bba | string | Sagawa BBA category count |
| 佐川 BBB | sagawa_bbb | string | Sagawa BBB category count |
| 佐川 BBBA | sagawa_bbba | string | Sagawa BBBA category count |
| 臨時 手当 | rinji_teate | string | Temporary allowance amount |
| 長距離 手当 | chokyori_teate | string | Long distance allowance amount |
| 助手 | joshu | string | Assistant count |
| 一般 A | ippan_a | string | General A category count |
| 一般 B | ippan_b | string | General B category count |
| 一般 BA | ippan_ba | string | General BA category count |
| 一般 BB | ippan_bb | string | General BB category count |
| 一般 BBA | ippan_bba | string | General BBA category count |
| 一般 BBB | ippan_bbb | string | General BBB category count |
| 4ｔ A | yontonsha_a | string | 4-ton truck A category count |
| 4ｔ B | yontonsha_b | string | 4-ton truck B category count |
| 4ｔ BA | yontonsha_ba | string | 4-ton truck BA category count |
| 4ｔ BB | yontonsha_bb | string | 4-ton truck BB category count |
| 4ｔ BBA | yontonsha_bba | string | 4-ton truck BBA category count |
| 4t BBB | yontonsha_bbb | string | 4-ton truck BBB category count |
| 4t BBBA | yontonsha_bbba | string | 4-ton truck BBBA category count |
| 佐・一 B | sagawa_ippan_b | string | Sagawa-General B combined count |
| 佐・一 BA | sagawa_ippan_ba | string | Sagawa-General BA combined count |
| 佐・一 BB | sagawa_ippan_bb | string | Sagawa-General BB combined count |
| 佐・一 BBA | sagawa_ippan_bba | string | Sagawa-General BBA combined count |
| 10・4併 B | juyon_yonhei_b | string | 10t-4t combined B count |
| 10・4併 BA | juyon_yonhei_ba | string | 10t-4t combined BA count |
| 10・4併 BB | juyon_yonhei_bb | string | 10t-4t combined BB count |
| 10t4t併 BBA | juronton_yontonhei_bba | string | 10t-4t combined BBA count |
| ﾛｰﾘｰ A | lorry_a | string | Lorry A category count |
| ﾛｰﾘｰ B | lorry_b | string | Lorry B category count |
| ﾛｰﾘｰ BA | lorry_ba | string | Lorry BA category count |
| ﾛｰﾘｰ BB | lorry_bb | string | Lorry BB category count |
| 合計 | gokei | string | Total count/amount |

## Data Structure Example

```json
{
  "shain_id": "230618",
  "shimei": "相馬 秀政",
  "chokyori_teate": "114000",
  "ippan_b": "22",
  "ippan_ba": "5",
  "gokei": "27"
}
```

## Notes

- All field values are extracted as strings (even numeric values) to preserve original formatting
- Not all fields are present for every employee - only populated fields appear in output
- The PDF has two different column layouts:
  - **37 columns**: Compact structure (typically page 2)
  - **44 columns**: Expanded structure with spacing columns (typically page 1)
- Category codes (A, B, BA, BB, etc.) represent different tier levels of allowances
- `gokei` (total) represents the sum of all allowance categories for that employee
