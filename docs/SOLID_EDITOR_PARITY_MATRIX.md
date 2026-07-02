# SolidJS Editor Parity Matrix

Date: 2026-07-02

Status meanings:

- `Baseline`: Existing editor behavior identified and covered by audit and/or existing tests.
- `Planned`: SolidJS work not implemented yet.
- `Blocked`: Needs implementation or further verification.
- `Pass`: Test/check passed.
- `Not run`: Not executed for SolidJS because Phase 1+ has not been implemented.

Existing test baseline:

```text
uv run pytest -> 110 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -> 46 passed, 1 warning

After Phase 1:
uv run pytest -> 111 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -> 47 passed, 1 warning
npm run typecheck -> passed
npm run build -> passed
```

| ID | Feature | Existing Editor | SolidJS | Auto Test | Manual Test | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| F001 | Editor page load at `/editor/`; separate `/editor-next/` page | Yes | Implemented Phase 1 | Existing and next route pass | Not run | Phase 1 implemented |
| F002 | Static CSS/JS asset loading | Yes | Implemented separate Solid assets | Existing and next static pass | Not run | Phase 1 implemented |
| F003 | Problem list loading | Yes | Implemented Phase 1 | Existing pass; Solid build pass | Not run | Phase 1 implemented |
| F004 | Problem tree filtering | Yes | Implemented simple filter | Solid build pass | Not run | Phase 1 implemented |
| F005 | Folder collapse/expand | Yes | Planned Phase 1+ | Not run | Not run | Planned |
| F006 | Problem selection/open | Yes | Implemented Phase 1 | Existing pass; Solid build pass | Not run | Phase 1 implemented |
| F007 | Path traversal rejection | Yes | Reuse server | Existing pass | Not run | Baseline |
| F008 | Artifact display | Yes | Implemented Phase 1 read-only | Existing partial pass; Solid build pass | Not run | Phase 1 implemented |
| F009 | SVG image asset rewrite | Yes | Reuse server | Existing pass | Not run | Baseline |
| F010 | DSL text editing/save | Yes | Planned Phase 5 | Existing pass | Not run | Planned |
| F011 | DSL format | Yes | Planned Phase 5 | Existing pass | Not run | Planned |
| F012 | Build | Yes | Planned Phase 6 | Existing pass | Not run | Planned |
| F013 | Build failure reporting | Yes | Planned Phase 6 | Existing partial pass | Not run | Planned |
| F014 | Manual layout patch | Yes | Planned Phase 5 | Existing pass | Not run | Planned |
| F015 | Patch + build | Yes | Planned Phase 5/6 | Existing pass | Not run | Planned |
| F016 | Single selection | Yes | Read-only slot list selection only | Solid build pass | Not run | Partial Phase 1 |
| F017 | Multi-selection | Yes | Planned Phase 2 | Not run | Not run | Planned |
| F018 | Marquee selection | Yes | Planned Phase 2 | Not run | Not run | Planned |
| F019 | Selection clear | Yes | Planned Phase 2 | Not run | Not run | Planned |
| F020 | Pick modes | Yes | Planned Phase 2/3 | Not run | Not run | Planned |
| F021 | SVG hit proxies | Yes | Planned Phase 2 | Existing static symbol check only | Not run | Planned |
| F022 | Drag move | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F023 | Drag throttling/local preview | Yes | Planned Phase 3 | Not run | Not run | Planned |
| F024 | Keyboard move | Yes | Planned Phase 3/4 | Not run | Not run | Planned |
| F025 | Snap toggle 5px | Yes | Planned Phase 2/3 | Not run | Not run | Planned |
| F026 | Resize handles | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F027 | Line endpoint edit | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F028 | Line/slot rotation | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F029 | Path point editing | Yes | Planned Phase 3 | Existing static symbol check | Not run | Planned |
| F030 | Polygon/path transforms | Yes | Planned Phase 3 | Existing static symbol check | Not run | Planned |
| F031 | Canvas selection/resize | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F032 | Property inspector coordinate edit | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F033 | Text inspector edit | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F034 | Inline text edit | Yes | Planned Phase 3 | Existing static asset check only | Not run | Planned |
| F035 | Font size controls | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F036 | Text alignment | Yes | Planned Phase 3 | Not run | Not run | Planned |
| F037 | Shape insertion gallery | Yes | Planned Phase 3 | Existing add patch pass | Not run | Planned |
| F038 | Text box insertion | Yes | Planned Phase 3 | Existing add patch pass | Not run | Planned |
| F039 | Image insertion | Yes | Planned Phase 3 | Existing add patch pass | Not run | Planned |
| F040 | Table insertion | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F041 | Graph paper insertion | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F042 | Bar model insertion | Yes | Planned Phase 3 | Existing server helpers pass | Not run | Planned |
| F043 | Tick bar insertion | Yes | Planned Phase 3 | Existing server helpers pass | Not run | Planned |
| F044 | Fraction/mixed fraction insertion | Yes | Planned Phase 3 | Existing fraction patch pass | Not run | Planned |
| F045 | Shape fill/stroke/dash formatting | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F046 | Delete selection | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F047 | Copy/paste selected slots | Yes | Planned Phase 3/4 | Existing add copied slot pass | Not run | Planned |
| F048 | Undo | Yes | Planned Phase 4 | Not run | Not run | Planned |
| F049 | Redo | Yes | Planned Phase 4 | Not run | Not run | Planned |
| F050 | History cap/reset | Yes | Planned Phase 4 | Not run | Not run | Planned |
| F051 | Alignment | Yes | Planned Phase 3/4 | Not run | Not run | Planned |
| F052 | Layer ordering | Yes | Planned Phase 3/4 | Existing override path partial | Not run | Planned |
| F053 | Table cell selection | Yes | Planned Phase 3 | Not run | Not run | Planned |
| F054 | Table divider adjustment | Yes | Planned Phase 3 | Existing server patch partial | Not run | Planned |
| F055 | Generated/helper group movement | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F056 | Generated slot override fallback | Yes | Reuse server | Existing pass | Not run | Baseline |
| F057 | Editor override delete/layer state | Yes | Reuse server | Existing pass | Not run | Baseline |
| F058 | Supported slot field validation | Yes | Reuse server | Existing pass | Not run | Baseline |
| F059 | Import insertion for added slots | Yes | Reuse server | Existing pass | Not run | Baseline |
| F060 | Semantic/solvable preservation on build | Yes | Reuse server | Existing pass | Not run | Baseline |
| F061 | Local image href inlining on build | Yes | Reuse server | Existing partial pass | Not run | Baseline |
| F062 | Error category/status messaging | Yes | Implemented Phase 1 loading/error status | Existing partial pass; Solid build pass | Not run | Phase 1 implemented |
| F063 | DSL/artifact slot ID caches | Yes | Planned typed equivalent | Not run | Not run | Planned |

## Phase 1 Minimum Matrix

These rows must move from `Planned` to implemented and verified before Phase 1 can be considered complete:

| ID | Feature | Existing Editor | SolidJS | Auto Test | Manual Test | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| F001 | Existing `/editor/` still loads and `/editor-next/` is separate | Yes | Implemented | Pass | Pending | Phase 1 implemented |
| F003 | Problem list loading | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F006 | Problem selection/open | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F008 | DSL/layout/renderer/SVG artifact read/display | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F016 | Read-only slot selection/list foundation | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F062 | Loading/error/status display | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
