# Semantic JSON Diff Report

## Summary
- total_fields: 81
- same: 46
- different: 2
- missing_in_generated: 22
- missing_in_reference: 11

## Field Diff (non-same)
| path | status | reference | generated |
|---|---|---|---|
| `$.answer.choices` | missing_in_reference | `null` | `[]` |
| `$.answer.choices[0].is_correct` | missing_in_generated | `false` | `null` |
| `$.answer.choices[0].value` | missing_in_generated | `"40"` | `null` |
| `$.answer.choices[1].is_correct` | missing_in_generated | `true` | `null` |
| `$.answer.choices[1].value` | missing_in_generated | `"50"` | `null` |
| `$.answer.choices[2].is_correct` | missing_in_generated | `false` | `null` |
| `$.answer.choices[2].value` | missing_in_generated | `"60"` | `null` |
| `$.domain` | missing_in_reference | `null` | `{}` |
| `$.domain.blank_symbol` | missing_in_generated | `"□"` | `null` |
| `$.domain.computed_answer` | missing_in_generated | `50` | `null` |
| `$.domain.left_seconds` | missing_in_generated | `410` | `null` |
| `$.domain.minutes` | missing_in_generated | `6` | `null` |
| `$.domain.unit_from` | missing_in_generated | `"초"` | `null` |
| `$.domain.unit_mid` | missing_in_generated | `"분"` | `null` |
| `$.domain.unit_to` | missing_in_generated | `"초"` | `null` |
| `$.meta.derived_from` | missing_in_generated | `"C:/projects/modu_math/problem/0001/json/semantic/semantic.json"` | `null` |
| `$.meta.removed_element_ids[0]` | missing_in_generated | `"answer_blank"` | `null` |
| `$.meta.source_svg` | missing_in_generated | `"C:/projects/modu_math/problem/0001/svg/edit/semantic_edit.svg"` | `null` |
| `$.meta.stage` | missing_in_generated | `"edit"` | `null` |
| `$.metadata.source.confidence` | missing_in_generated | `0.6` | `null` |
| `$.metadata.source.created_at` | missing_in_generated | `"2026-04-07T01:05:45.296672+00:00"` | `null` |
| `$.metadata.source.generator` | different | `"rule_parser"` | `"modu_semantic"` |
| `$.metadata.source.input_path` | missing_in_generated | `"C:/projects/modu_math/problem/0001/input/0001.png"` | `null` |
| `$.metadata.source.input_type` | different | `"png"` | `"python_dsl"` |
| `$.metadata.source.parser_name` | missing_in_generated | `"PngToSemanticDraftParser"` | `null` |
| `$.render.elements[0].alignment` | missing_in_reference | `null` | `"left"` |
| `$.render.elements[0].z_index` | missing_in_reference | `null` | `0` |
| `$.render.elements[1].alignment` | missing_in_reference | `null` | `"left"` |
| `$.render.elements[1].anchor` | missing_in_reference | `null` | `"start"` |
| `$.render.elements[1].figure_type` | missing_in_generated | `"rounded_box"` | `null` |
| `$.render.elements[1].font_family` | missing_in_reference | `null` | `"Malgun Gothic"` |
| `$.render.elements[1].font_weight` | missing_in_reference | `null` | `"normal"` |
| `$.render.elements[1].z_index` | missing_in_reference | `null` | `0` |
| `$.render.elements[2].alignment` | missing_in_reference | `null` | `"left"` |
| `$.render.elements[2].z_index` | missing_in_reference | `null` | `0` |
