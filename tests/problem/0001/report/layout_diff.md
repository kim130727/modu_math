# Layout JSON Diff Report

## Summary
- total_fields: 80
- same: 56
- different: 10
- missing_in_generated: 4
- missing_in_reference: 10

## Field Diff (non-same)
| path | status | reference | generated |
|---|---|---|---|
| `$.elements[1].attrs.font-size` | different | `"42px"` | `"42"` |
| `$.elements[1].attrs.text` | missing_in_reference | `null` | `"□안에 알맞은 수를 구하시오."` |
| `$.elements[1].attrs.text-anchor` | missing_in_generated | `"start"` | `null` |
| `$.elements[1].attrs.x` | different | `"72"` | `"72.0"` |
| `$.elements[1].attrs.y` | different | `"92"` | `"92.0"` |
| `$.elements[1].font_size` | missing_in_reference | `null` | `42` |
| `$.elements[2].attrs.font-family` | missing_in_reference | `null` | `"Malgun Gothic"` |
| `$.elements[2].attrs.font-weight` | missing_in_reference | `null` | `"normal"` |
| `$.elements[2].attrs.height` | different | `"180"` | `"180.0"` |
| `$.elements[2].attrs.width` | different | `"720"` | `"720.0"` |
| `$.elements[2].attrs.x` | different | `"280"` | `"280.0"` |
| `$.elements[2].attrs.y` | different | `"240"` | `"240.0"` |
| `$.elements[3].attrs.font-size` | different | `"54px"` | `"54"` |
| `$.elements[3].attrs.text` | missing_in_reference | `null` | `"410초=6분 □초"` |
| `$.elements[3].attrs.text-anchor` | missing_in_generated | `"middle"` | `null` |
| `$.elements[3].attrs.x` | different | `"640"` | `"640.0"` |
| `$.elements[3].attrs.y` | different | `"345"` | `"345.0"` |
| `$.elements[3].font_size` | missing_in_reference | `null` | `54` |
| `$.meta.generator` | missing_in_generated | `"problem.common.layout_tools.write_layout"` | `null` |
| `$.meta.source_svg` | missing_in_generated | `"C:/projects/modu_math/problem/0001/svg/final/semantic_final.svg"` | `null` |
| `$.metadata.generator` | missing_in_reference | `null` | `"modu_semantic.compiler_json.compile_layout_json"` |
| `$.metadata.source_svg` | missing_in_reference | `null` | `"generated://modu_semantic/semantic_final.svg"` |
| `$.problem_id` | missing_in_reference | `null` | `"0001"` |
| `$.schema_version` | missing_in_reference | `null` | `"modu_math.layout.v1"` |
