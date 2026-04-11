# SVG Diff Report

```diff
--- reference_semantic_final.svg
+++ generated_semantic.svg
@@ -1,7 +1,7 @@
 <?xml version="1.0" encoding="UTF-8"?>
-<svg xmlns="http://www.w3.org/2000/svg" width="1280.0" height="720.0" viewBox="0 0 1280.0 720.0">
-  <rect x="0" y="0" width="1280.0" height="720.0" fill="#F6F6F6" />
-  <text id="instruction" x="72" y="92" font-family="Malgun Gothic" font-size="42px" fill="#000000" font-weight="normal" text-anchor="start">□안에 알맞은 수를 구하시오.</text>
-  <rect id="question_box" x="280" y="240" width="720" height="180"  rx="24" stroke="#000000" stroke-width="3" fill="none" />
-  <text id="equation" x="640" y="345" font-family="Malgun Gothic" font-size="54px" fill="#000000" font-weight="normal" text-anchor="middle">410초=6분 □초</text>
+<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
+  <rect x="0" y="0" width="1280" height="720" fill="#F6F6F6" />
+  <text id="instruction" data-group="question" data-semantic-role="instruction" fill="#000000" font-family="Malgun Gothic" font-size="42px" font-weight="normal" x="72" y="92" text-anchor="start">□안에 알맞은 수를 구하시오.</text>
+  <rect id="question_box" data-group="question" data-semantic-role="question_container" stroke="#000000" stroke-width="3" fill="none" font-family="Malgun Gothic" font-weight="normal" x="280" y="240" width="720" height="180" rx="24" />
+  <text id="equation" data-group="question" data-semantic-role="equation" fill="#000000" font-family="Malgun Gothic" font-size="54px" font-weight="normal" x="640" y="345" text-anchor="middle">410초=6분 □초</text>
 </svg>
```
