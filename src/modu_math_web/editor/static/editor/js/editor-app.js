import {
  applyLayoutPatches,
  applyLayoutPatchesAndBuild,
  buildProblem as requestBuildProblem,
  classifyApiError,
  formatDsl as requestFormatDsl,
  listProblems as requestProblemList,
  loadProblem as requestProblemDetail,
  saveDsl as requestSaveDsl,
} from "./editor-api.js";
import { createLayoutPatchCommand, clearHistory as clearCommandHistory, executeCommand as executeEditorCommand } from "./editor-commands.js";
import { getState, resetState, setState, subscribe } from "./editor-state.js";
import {
  adjustedBBox as canvasAdjustedBBox,
  adjustedCanvasBox as canvasAdjustedCanvasBox,
  appendStrokeHitProxy as canvasAppendStrokeHitProxy,
  appendTextHitProxy as canvasAppendTextHitProxy,
  bindCanvasSlotInteractionEvents as canvasBindCanvasSlotInteractionEvents,
  beginMarqueeBox as canvasBeginMarqueeBox,
  capturePointer as canvasCapturePointer,
  clientRectToSvgBox as canvasClientRectToSvgBox,
  cloneBBox as canvasCloneBBox,
  clamp as canvasClamp,
  createSlotDragSnapshot as canvasCreateSlotDragSnapshot,
  createDrawState as canvasCreateDrawState,
  curvePathFromPoints as canvasCurvePathFromPoints,
  clearPathPointHandles as canvasClearPathPointHandles,
  drawPathFromState as canvasDrawPathFromState,
  editablePathFromD as canvasEditablePathFromD,
  ensureDrawPreview as canvasEnsureDrawPreview,
  ensureSelectionOverlay as canvasEnsureSelectionOverlay,
  formatPolygonPoints as canvasFormatPolygonPoints,
  formatPathPoint as canvasFormatPathPoint,
  freeformPathFromPoints as canvasFreeformPathFromPoints,
  finishMarqueeBox as canvasFinishMarqueeBox,
  hideSelectionOverlay as canvasHideSelectionOverlay,
  inflateHitBox as canvasInflateHitBox,
  initCanvas,
  linePatchFromEndpoint as canvasLinePatchFromEndpoint,
  linePatchFromRotation as canvasLinePatchFromRotation,
  pathPointPatchFromHandle as canvasPathPointPatchFromHandle,
  parsePolygonPoints as canvasParsePolygonPoints,
  pointToBoxDistance as canvasPointToBoxDistance,
  pointToSegmentDistance as canvasPointToSegmentDistance,
  pointInRotatedFrame as canvasPointInRotatedFrame,
  renderPathPointHandles as canvasRenderPathPointHandles,
  renderSvgContainer,
  renderTableAdjustmentHandles as canvasRenderTableAdjustmentHandles,
  removeDrawPreview as canvasRemoveDrawPreview,
  releasePointerCapture as canvasReleasePointerCapture,
  rotatePointAround as canvasRotatePointAround,
  scheduleDragFrame as canvasScheduleDragFrame,
  scalePathD as canvasScalePathD,
  shiftPathD as canvasShiftPathD,
  syncSlotHitProxies as canvasSyncSlotHitProxies,
  svgPoint as canvasSvgPoint,
  transformPathD as canvasTransformPathD,
  translateSelectionOverlay as canvasTranslateSelectionOverlay,
  updateMarqueeBox as canvasUpdateMarqueeBox,
  updateDrawStatePoint as canvasUpdateDrawStatePoint,
  updateSelectionOverlay as canvasUpdateSelectionOverlay,
} from "./editor-canvas.js";
import { bindCommitInputs, initProperties } from "./editor-properties.js";
    let currentProblemId = null;
    let knownProblems = [];
    let dragState = null;
    let resizeState = null;
    let selectedSlots = new Map();
    let selectedSlotId = null;
    let selectedElement = null;
    let keyboardCommitTimer = null;
    let undoStack = [];
    let redoStack = [];
    let historyBusy = false;
    let dragFrameRequested = false;
    let resizeFrameRequested = false;
    let pendingResizePoint = null;
    let lastDragStatusAt = 0;
    let dragCommitTimer = null;
    let dragCommitTask = null;
    let pendingPatchSaves = [];
    let copyBuffer = null;
    let pasteSequence = 0;
    let pickMode = "all";
    let marqueeState = null;
    let pendingDrawShape = null;
    let drawState = null;
    let inlineTextEditState = null;
    let dslSlotIdCache = { layoutText: null, dsl: null, ids: null };
    let sourceDslSlotIdCache = { dsl: null, ids: null };
    let rendererSlotRefCache = { rendererText: null, byElementId: null };
    let layoutGroupCache = { layoutText: null, groups: null, byMember: null };
    let selectedTableCells = [];
    let snapEnabled = true;
    let collapsedProblemFolders = new Set();
    const SNAP_STEP = 5;
    const DEFAULT_SHAPE_STYLE = { fill: "#ffffff", stroke: "#111827", stroke_width: 1.5 };
    const SHAPE_FILL_SWATCHES = ["#ffffff", "#f8fafc", "#fef3c7", "#fed7aa", "#fecaca", "#bfdbfe", "#bbf7d0", "#ddd6fe", "#111827", "#6b7280", "#dc2626", "#2563eb", "#16a34a", "#7c3aed", "#f59e0b", "none"];
    const SHAPE_CATEGORIES = [
      {
        title: "선",
        shapes: [
          { id: "line", label: "선", kind: "line", icon: '<line x1="3" y1="16" x2="19" y2="4"/>' },
          { id: "hline", label: "가로선", kind: "line", line: "horizontal", icon: '<line x1="3" y1="10" x2="19" y2="10"/>' },
          { id: "vline", label: "세로선", kind: "line", line: "vertical", icon: '<line x1="11" y1="3" x2="11" y2="17"/>' },
          { id: "elbow", label: "꺾은 선", kind: "path", d: "M 0 0 L 52 0 L 52 48", fill: "none", icon: '<path d="M5 4H15V15"/>' },
          { id: "curve", label: "곡선", kind: "path", d: "M 0 40 C 16 0, 34 80, 60 20", fill: "none", icon: '<path d="M3 15 C7 2,13 19,20 6"/>' },
          { id: "freeform", label: "자유형", kind: "path", d: "M 0 36 L 14 12 L 28 48 L 42 22 L 56 16 L 66 4", sourceWidth: 66, sourceHeight: 52, fill: "none", icon: '<path d="M3 15 L8 4 L11 17 L15 8 L19 5 L21 3"/>' },
        ],
      },
      {
        title: "사각형",
        shapes: [
          { id: "rect", label: "사각형", kind: "rect", icon: '<rect class="shape-fill" x="4" y="5" width="15" height="11"/>' },
          { id: "roundRect", label: "모서리가 둥근 사각형", kind: "rect", rx: 6, ry: 6, icon: '<rect class="shape-fill" x="4" y="5" width="15" height="11" rx="3"/>' },
          { id: "snip1", label: "한쪽 모서리 잘린 사각형", kind: "polygon", points: [[10, 0], [64, 0], [64, 46], [0, 46], [0, 10]], icon: '<polygon class="shape-fill" points="7,4 19,4 19,16 4,16 4,7"/>' },
          { id: "snip2", label: "대각 모서리 잘린 사각형", kind: "polygon", points: [[10, 0], [64, 0], [64, 36], [54, 46], [0, 46], [0, 10]], icon: '<polygon class="shape-fill" points="7,4 19,4 19,13 16,16 4,16 4,7"/>' },
          { id: "tab", label: "탭 사각형", kind: "path", d: "M 0 12 Q 0 0 12 0 L 52 0 Q 64 0 64 12 L 64 46 L 0 46 Z", icon: '<path class="shape-fill" d="M4 8 Q4 4 8 4 H16 Q20 4 20 8 V16 H4 Z"/>' },
        ],
      },
      {
        title: "기본 도형",
        shapes: [
          { id: "circle", label: "원", kind: "circle", r: 43, icon: '<circle class="shape-fill" cx="11" cy="10" r="7"/>' },
          { id: "oval", label: "타원", kind: "path", d: "M 32 0 C 49.7 0 64 10.3 64 23 C 64 35.7 49.7 46 32 46 C 14.3 46 0 35.7 0 23 C 0 10.3 14.3 0 32 0 Z", icon: '<ellipse class="shape-fill" cx="11" cy="10" rx="8" ry="6"/>' },
          { id: "triangle", label: "삼각형", kind: "polygon", points: [[32, 0], [64, 52], [0, 52]], icon: '<polygon class="shape-fill" points="11,4 19,16 3,16"/>' },
          { id: "rightTriangle", label: "직각 삼각형", kind: "polygon", points: [[0, 0], [64, 52], [0, 52]], icon: '<polygon class="shape-fill" points="5,4 19,16 5,16"/>' },
          { id: "parallelogram", label: "평행사변형", kind: "polygon", points: [[16, 0], [64, 0], [48, 46], [0, 46]], icon: '<polygon class="shape-fill" points="8,5 20,5 16,16 4,16"/>' },
          { id: "trapezoid", label: "사다리꼴", kind: "polygon", points: [[16, 0], [48, 0], [64, 46], [0, 46]], icon: '<polygon class="shape-fill" points="8,5 16,5 20,16 4,16"/>' },
          { id: "diamond", label: "마름모", kind: "polygon", points: [[32, 0], [64, 26], [32, 52], [0, 26]], icon: '<polygon class="shape-fill" points="11,3 20,10 11,17 2,10"/>' },
          { id: "pentagon", label: "오각형", kind: "polygon", points: [[32, 0], [64, 20], [52, 52], [12, 52], [0, 20]], icon: '<polygon class="shape-fill" points="11,3 19,8 16,17 6,17 3,8"/>' },
          { id: "hexagon", label: "육각형", kind: "polygon", points: [[18, 0], [46, 0], [64, 26], [46, 52], [18, 52], [0, 26]], icon: '<polygon class="shape-fill" points="7,4 15,4 20,10 15,16 7,16 2,10"/>' },
          { id: "octagon", label: "팔각형", kind: "polygon", points: [[18, 0], [46, 0], [64, 18], [64, 34], [46, 52], [18, 52], [0, 34], [0, 18]], icon: '<polygon class="shape-fill" points="7,4 15,4 19,8 19,12 15,16 7,16 3,12 3,8"/>' },
          { id: "cross", label: "십자", kind: "polygon", points: [[24, 0], [40, 0], [40, 18], [64, 18], [64, 34], [40, 34], [40, 52], [24, 52], [24, 34], [0, 34], [0, 18], [24, 18]], icon: '<polygon class="shape-fill" points="9,3 13,3 13,8 19,8 19,12 13,12 13,17 9,17 9,12 3,12 3,8 9,8"/>' },
          { id: "plus", label: "더하기", kind: "polygon", points: [[27, 0], [37, 0], [37, 21], [64, 21], [64, 31], [37, 31], [37, 52], [27, 52], [27, 31], [0, 31], [0, 21], [27, 21]], icon: '<polygon class="shape-fill" points="9,3 13,3 13,8 19,8 19,12 13,12 13,17 9,17 9,12 3,12 3,8 9,8"/>' },
          { id: "x", label: "곱하기", kind: "polygon", points: [[8, 0], [32, 20], [56, 0], [64, 8], [40, 26], [64, 44], [56, 52], [32, 32], [8, 52], [0, 44], [24, 26], [0, 8]], icon: '<path d="M5 4 L18 16 M18 4 L5 16"/>' },
          { id: "bracketPair", label: "괄호", kind: "path", d: "M 20 0 C 4 12, 4 40, 20 52 M 44 0 C 60 12, 60 40, 44 52", fill: "none", icon: '<path d="M8 4 C4 7,4 13,8 16 M14 4 C18 7,18 13,14 16"/>' },
          { id: "arc", label: "호", kind: "path", d: "M 4 46 A 28 28 0 0 1 60 46", fill: "none", icon: '<path d="M4 16 A7 7 0 0 1 18 16"/>' },
          { id: "quarterArc", label: "1/4호", kind: "path", d: "M 4 46 A 42 42 0 0 1 46 4", fill: "none", icon: '<path d="M5 16 A11 11 0 0 1 16 5"/>' },
        ],
      },
      {
        title: "교구",
        shapes: [
          { id: "pushPin", label: "누름 못", kind: "path", d: "M 32 4 C 44 4 54 11 54 20 C 54 29 44 36 32 36 C 20 36 10 29 10 20 C 10 11 20 4 32 4 Z M 25 34 L 39 34 L 39 44 L 25 44 Z M 32 44 L 38 58 L 26 58 Z", sourceWidth: 64, sourceHeight: 64, fill: "#A8B0B6", stroke: "#7E8790", stroke_width: 1.2, icon: '<path class="shape-fill" d="M11 4C15 4 19 6.5 19 10S15 16 11 16S3 13.5 3 10S7 4 11 4Z M8.5 15H13.5V18H8.5Z M11 18L14 22H8Z"/>' },
          { id: "boy", label: "남자", kind: "composite", sourceWidth: 80, sourceHeight: 110, w: 80, h: 110, icon: '<circle class="shape-fill" cx="12" cy="7" r="5" fill="#ffd9ad"/><path class="shape-fill" d="M7 7C8 1 17 1 17 7C14 4 10 5 7 7Z" fill="#8a4b2a"/><circle cx="10" cy="8" r="0.75" fill="#2b2118"/><circle cx="14" cy="8" r="0.75" fill="#2b2118"/><path d="M10.5 11 Q12 12 13.5 11" fill="none" stroke="#b86e39" stroke-width="0.8"/><polygon class="shape-fill" points="7,20 17,20 15,12 9,12" fill="#60a5fa"/>', parts: [
            { id: "body", kind: "polygon", points: [[18, 104], [62, 104], [54, 67], [26, 67]], fill: "#60A5FA", stroke: "none" },
            { id: "head", kind: "circle", cx: 40, cy: 38, r: 24, fill: "#ffd9ad", stroke: "none" },
            { id: "hair.cap", kind: "path", d: "M 16 37 C 19 10 61 9 64 37 C 49 22 31 29 16 37 Z", fill: "#7C4A2D", stroke: "none" },
            { id: "eye.left", kind: "circle", cx: 31, cy: 42, r: 3.1, fill: "#2b2118", stroke: "none" },
            { id: "eye.right", kind: "circle", cx: 49, cy: 42, r: 3.1, fill: "#2b2118", stroke: "none" },
            { id: "eye.left.light", kind: "circle", cx: 30.1, cy: 40.9, r: 0.9, fill: "#ffffff", stroke: "none" },
            { id: "eye.right.light", kind: "circle", cx: 48.1, cy: 40.9, r: 0.9, fill: "#ffffff", stroke: "none" },
            { id: "smile", kind: "path", d: "M 33 52 Q 40 58 47 52", fill: "none", stroke: "#b86e39", stroke_width: 1.4 },
          ] },
          { id: "girl", label: "여자", kind: "composite", sourceWidth: 90, sourceHeight: 112, w: 90, h: 112, icon: '<circle class="shape-fill" cx="12" cy="7" r="5" fill="#ffd9ad"/><path class="shape-fill" d="M7 7C8 1 17 1 17 7C13 5 10 5 7 7Z" fill="#8a3f32"/><circle cx="10" cy="8" r="0.75" fill="#2b2118"/><circle cx="14" cy="8" r="0.75" fill="#2b2118"/><path d="M10.5 11 Q12 12 13.5 11" fill="none" stroke="#b86e39" stroke-width="0.8"/><polygon class="shape-fill" points="7,20 17,20 15,12 9,12" fill="#f06aa0"/>', parts: [
            { id: "tail.left", kind: "path", d: "M 20 37 C 4 40 11 72 4 78", fill: "none", stroke: "#8A3F32", stroke_width: 5 },
            { id: "tail.right", kind: "path", d: "M 70 37 C 86 40 79 72 86 78", fill: "none", stroke: "#8A3F32", stroke_width: 5 },
            { id: "body", kind: "polygon", points: [[22, 106], [68, 106], [58, 68], [32, 68]], fill: "#F06AA0", stroke: "none" },
            { id: "head", kind: "circle", cx: 45, cy: 38, r: 24, fill: "#ffd9ad", stroke: "none" },
            { id: "hair.cap", kind: "path", d: "M 21 37 C 24 10 66 9 69 37 C 53 24 37 28 21 37 Z", fill: "#8A3F32", stroke: "none" },
            { id: "eye.left", kind: "circle", cx: 36, cy: 42, r: 3.1, fill: "#2b2118", stroke: "none" },
            { id: "eye.right", kind: "circle", cx: 54, cy: 42, r: 3.1, fill: "#2b2118", stroke: "none" },
            { id: "eye.left.light", kind: "circle", cx: 35.1, cy: 40.9, r: 0.9, fill: "#ffffff", stroke: "none" },
            { id: "eye.right.light", kind: "circle", cx: 53.1, cy: 40.9, r: 0.9, fill: "#ffffff", stroke: "none" },
            { id: "smile", kind: "path", d: "M 38 52 Q 45 58 52 52", fill: "none", stroke: "#b86e39", stroke_width: 1.4 },
            { id: "bow.left", kind: "polygon", points: [[38, 76], [24, 69], [32, 87]], fill: "#D487D8", stroke: "none" },
            { id: "bow.right", kind: "polygon", points: [[52, 76], [66, 69], [58, 87]], fill: "#D487D8", stroke: "none" },
          ] },
          { id: "school", label: "학교", kind: "composite", sourceWidth: 96, sourceHeight: 76, w: 96, h: 76, icon: '<rect class="shape-fill" x="5" y="9" width="14" height="10" fill="#ffd98a"/><polygon class="shape-fill" points="3,9 12,4 21,9" fill="#e96f4a"/><path d="M12 4V1L17 3"/><circle cx="12" cy="12" r="2" fill="#f8fbff"/>', parts: [
            { id: "yard", kind: "rect", x: 4, y: 64, width: 86, height: 8, rx: 4, ry: 4, stroke: "none", fill: "#b7e2b6" },
            { id: "body", kind: "rect", x: 18, y: 34, width: 60, height: 40, fill: "#ffd98a", stroke: "#7f6b4d", stroke_width: 1.4 },
            { id: "roof", kind: "polygon", points: [[12, 36], [48, 18], [84, 36]], fill: "#e96f4a", stroke: "#9b5738", stroke_width: 1.4 },
            { id: "tower", kind: "rect", x: 39, y: 24, width: 18, height: 50, fill: "#f3c35b", stroke: "#7f6b4d", stroke_width: 1.3 },
            { id: "tower.roof", kind: "polygon", points: [[35, 24], [48, 14], [61, 24]], fill: "#e96f4a", stroke: "#9b5738", stroke_width: 1.2 },
            { id: "flag.pole", kind: "line", x1: 48, y1: 14, x2: 48, y2: 0, stroke: "#4b5563", stroke_width: 1.2 },
            { id: "flag", kind: "polygon", points: [[48, 0], [64, 5], [48, 10]], fill: "#ff8a8a", stroke: "#d14343", stroke_width: 1 },
            { id: "clock", kind: "circle", cx: 48, cy: 39, r: 7, fill: "#f8fbff", stroke: "#5b7187", stroke_width: 1.2 },
            { id: "door", kind: "rect", x: 42, y: 55, width: 12, height: 19, fill: "#8fd3ff", stroke: "#795548", stroke_width: 1.1 },
            { id: "window.left.top", kind: "rect", x: 25, y: 42, width: 9, height: 8, fill: "#dff6ff", stroke: "#5082a9", stroke_width: 1 },
            { id: "window.left.bottom", kind: "rect", x: 25, y: 56, width: 9, height: 8, fill: "#dff6ff", stroke: "#5082a9", stroke_width: 1 },
            { id: "window.right.top", kind: "rect", x: 62, y: 42, width: 9, height: 8, fill: "#dff6ff", stroke: "#5082a9", stroke_width: 1 },
            { id: "window.right.bottom", kind: "rect", x: 62, y: 56, width: 9, height: 8, fill: "#dff6ff", stroke: "#5082a9", stroke_width: 1 },
          ] },
          { id: "house", label: "집", kind: "composite", sourceWidth: 84, sourceHeight: 62, w: 84, h: 62, icon: '<rect class="shape-fill" x="6" y="10" width="13" height="9" fill="#ffe19a"/><polygon class="shape-fill" points="4,10 12,4 20,10" fill="#ef6b55"/><rect x="10" y="13" width="4" height="6" fill="#7cc3ff"/>', parts: [
            { id: "yard", kind: "rect", x: 5, y: 53, width: 74, height: 8, rx: 4, ry: 4, stroke: "none", fill: "#b7e2b6" },
            { id: "body", kind: "rect", x: 16, y: 28, width: 52, height: 34, fill: "#ffe19a", stroke: "#8a6240", stroke_width: 1.4 },
            { id: "roof", kind: "polygon", points: [[9, 30], [42, 8], [75, 30]], fill: "#ef6b55", stroke: "#a64b43", stroke_width: 1.4 },
            { id: "chimney", kind: "rect", x: 58, y: 13, width: 8, height: 16, fill: "#ef6b55", stroke: "#a64b43", stroke_width: 1 },
            { id: "door", kind: "rect", x: 37, y: 40, width: 12, height: 22, fill: "#7cc3ff", stroke: "#795548", stroke_width: 1 },
            { id: "window.left", kind: "rect", x: 23, y: 36, width: 10, height: 10, fill: "#dff6ff", stroke: "#4f91b7", stroke_width: 1 },
            { id: "window.right", kind: "rect", x: 53, y: 36, width: 10, height: 10, fill: "#dff6ff", stroke: "#4f91b7", stroke_width: 1 },
          ] },
          { id: "playground", label: "놀이터", kind: "composite", sourceWidth: 96, sourceHeight: 82, w: 96, h: 82, icon: '<circle class="shape-fill" cx="13" cy="12" r="8" fill="#c9eeb6"/><path d="M9 18 C13 14 15 12 19 10" stroke="#f08bb4" stroke-width="2"/><path d="M8 15 L12 5 L18 15"/><line x1="10" y1="5" x2="16" y2="5"/>', parts: [
            { id: "ground", kind: "circle", cx: 52, cy: 50, r: 35, fill: "#c9eeb6", stroke: "none" },
            { id: "trunk", kind: "rect", x: 13, y: 29, width: 6, height: 28, fill: "#a96a3d", stroke: "none" },
            { id: "tree.top", kind: "circle", cx: 16, cy: 22, r: 13, fill: "#7bcf6b", stroke: "none" },
            { id: "swing.top", kind: "line", x1: 42, y1: 18, x2: 76, y2: 18, stroke: "#61a66d", stroke_width: 2 },
            { id: "swing.left", kind: "line", x1: 42, y1: 18, x2: 33, y2: 60, stroke: "#61a66d", stroke_width: 2 },
            { id: "swing.right", kind: "line", x1: 76, y1: 18, x2: 85, y2: 60, stroke: "#61a66d", stroke_width: 2 },
            { id: "rope.left", kind: "line", x1: 54, y1: 18, x2: 54, y2: 42, stroke: "#9ca3af", stroke_width: 1.2 },
            { id: "rope.right", kind: "line", x1: 64, y1: 18, x2: 64, y2: 42, stroke: "#9ca3af", stroke_width: 1.2 },
            { id: "seat", kind: "rect", x: 50, y: 42, width: 18, height: 4, rx: 2, ry: 2, fill: "#f59e0b", stroke: "none" },
            { id: "slide", kind: "path", d: "M 30 58 C 49 46, 61 38, 76 32", fill: "none", stroke: "#f08bb4", stroke_width: 4 },
            { id: "ladder", kind: "line", x1: 28, y1: 58, x2: 38, y2: 30, stroke: "#60a5fa", stroke_width: 2 },
          ] },
        ],
      },
      {
        title: "블록 화살표",
        shapes: [
          { id: "rightArrow", label: "오른쪽 화살표", kind: "polygon", points: [[0, 16], [42, 16], [42, 0], [64, 26], [42, 52], [42, 36], [0, 36]], icon: '<polygon class="shape-fill" points="3,8 14,8 14,4 21,10 14,16 14,12 3,12"/>' },
          { id: "leftArrow", label: "왼쪽 화살표", kind: "polygon", points: [[64, 16], [22, 16], [22, 0], [0, 26], [22, 52], [22, 36], [64, 36]], icon: '<polygon class="shape-fill" points="21,8 10,8 10,4 3,10 10,16 10,12 21,12"/>' },
          { id: "upArrow", label: "위쪽 화살표", kind: "polygon", points: [[24, 52], [24, 18], [8, 18], [32, 0], [56, 18], [40, 18], [40, 52]], icon: '<polygon class="shape-fill" points="9,17 9,8 5,8 12,3 19,8 15,8 15,17"/>' },
          { id: "downArrow", label: "아래쪽 화살표", kind: "polygon", points: [[24, 0], [40, 0], [40, 34], [56, 34], [32, 52], [8, 34], [24, 34]], icon: '<polygon class="shape-fill" points="9,3 15,3 15,12 19,12 12,17 5,12 9,12"/>' },
          { id: "leftRightArrow", label: "좌우 화살표", kind: "polygon", points: [[0, 26], [18, 6], [18, 18], [46, 18], [46, 6], [64, 26], [46, 46], [46, 34], [18, 34], [18, 46]], icon: '<polygon class="shape-fill" points="3,10 8,5 8,8 16,8 16,5 21,10 16,15 16,12 8,12 8,15"/>' },
          { id: "quadArrow", label: "상하좌우 화살표", kind: "polygon", points: [[32, 0], [46, 14], [38, 14], [38, 20], [50, 20], [50, 12], [64, 26], [50, 40], [50, 32], [38, 32], [38, 38], [46, 38], [32, 52], [18, 38], [26, 38], [26, 32], [14, 32], [14, 40], [0, 26], [14, 12], [14, 20], [26, 20], [26, 14], [18, 14]], icon: '<polygon class="shape-fill" points="12,3 16,7 14,7 14,9 17,9 17,7 21,11 17,15 17,13 14,13 14,15 16,15 12,19 8,15 10,15 10,13 7,13 7,15 3,11 7,7 7,9 10,9 10,7 8,7"/>' },
          { id: "chevron", label: "갈매기형 수장", kind: "polygon", points: [[0, 0], [42, 0], [64, 26], [42, 52], [0, 52], [22, 26]], icon: '<polygon class="shape-fill" points="3,5 15,5 21,10 15,16 3,16 9,10"/>' },
          { id: "notchedArrow", label: "오목 오른쪽 화살표", kind: "polygon", points: [[0, 8], [42, 8], [42, 0], [64, 26], [42, 52], [42, 44], [0, 44], [14, 26]], icon: '<polygon class="shape-fill" points="3,6 14,6 14,4 21,10 14,16 14,14 3,14 7,10"/>' },
        ],
      },
      {
        title: "수식 도형",
        shapes: [
          { id: "mathPlus", label: "더하기", kind: "polygon", points: [[27, 0], [37, 0], [37, 21], [64, 21], [64, 31], [37, 31], [37, 52], [27, 52], [27, 31], [0, 31], [0, 21], [27, 21]], icon: '<path d="M11 4V16 M5 10H17"/>' },
          { id: "mathMinus", label: "빼기", kind: "rect", h: 12, icon: '<path d="M5 10H17"/>' },
          { id: "mathMultiply", label: "곱하기", kind: "path", d: "M 8 0 L 32 20 L 56 0 L 64 8 L 40 26 L 64 44 L 56 52 L 32 32 L 8 52 L 0 44 L 24 26 L 0 8 Z", icon: '<path d="M6 5 L17 16 M17 5 L6 16"/>' },
          { id: "mathDivide", label: "나누기", kind: "path", d: "M 0 22 L 64 22 L 64 30 L 0 30 Z M 32 3 A 6 6 0 1 1 31.9 3 M 32 43 A 6 6 0 1 1 31.9 43", icon: '<path d="M5 10H17"/><circle cx="11" cy="5" r="1.5"/><circle cx="11" cy="15" r="1.5"/>' },
          { id: "mathEqual", label: "같음", kind: "path", d: "M 0 14 L 64 14 L 64 22 L 0 22 Z M 0 30 L 64 30 L 64 38 L 0 38 Z", icon: '<path d="M5 8H17 M5 13H17"/>' },
        ],
      },
      {
        title: "순서도",
        shapes: [
          { id: "flowProcess", label: "프로세스", kind: "rect", icon: '<rect class="shape-fill" x="4" y="5" width="15" height="11"/>' },
          { id: "flowTerminator", label: "터미네이터", kind: "path", d: "M 14 0 L 50 0 C 68 0 68 46 50 46 L 14 46 C -4 46 -4 0 14 0 Z", icon: '<path class="shape-fill" d="M8 5H16 C21 5 21 16 16 16H8 C3 16 3 5 8 5Z"/>' },
          { id: "flowDecision", label: "판단", kind: "polygon", points: [[32, 0], [64, 23], [32, 46], [0, 23]], icon: '<polygon class="shape-fill" points="11,4 20,10 11,16 2,10"/>' },
          { id: "flowData", label: "데이터", kind: "polygon", points: [[14, 0], [64, 0], [50, 46], [0, 46]], icon: '<polygon class="shape-fill" points="7,5 20,5 16,16 3,16"/>' },
          { id: "flowDocument", label: "문서", kind: "path", d: "M 0 0 L 64 0 L 64 38 C 48 52 18 30 0 46 Z", icon: '<path class="shape-fill" d="M4 5H20V14 C15 18 9 12 4 16Z"/>' },
          { id: "flowStoredData", label: "저장 데이터", kind: "path", d: "M 14 0 L 64 0 C 50 12 50 34 64 46 L 14 46 C -4 46 -4 0 14 0 Z", icon: '<path class="shape-fill" d="M8 5H20 C16 8 16 13 20 16H8 C3 16 3 5 8 5Z"/>' },
          { id: "flowDelay", label: "지연", kind: "path", d: "M 0 0 L 40 0 C 72 0 72 46 40 46 L 0 46 Z", icon: '<path class="shape-fill" d="M4 5H14 C22 5 22 16 14 16H4Z"/>' },
        ],
      },
      {
        title: "별 및 현수막",
        shapes: [
          { id: "star5", label: "별 5개", kind: "polygon", points: [[32, 0], [39, 19], [60, 19], [43, 31], [50, 52], [32, 39], [14, 52], [21, 31], [4, 19], [25, 19]], icon: '<polygon class="shape-fill" points="11,3 13,8 19,8 14,11 16,17 11,13 6,17 8,11 3,8 9,8"/>' },
          { id: "star8", label: "별 8개", kind: "polygon", points: [[32, 0], [39, 17], [56, 8], [47, 25], [64, 32], [47, 39], [56, 56], [39, 47], [32, 64], [25, 47], [8, 56], [17, 39], [0, 32], [17, 25], [8, 8], [25, 17]], icon: '<polygon class="shape-fill" points="11,2 13,7 18,4 15,9 20,11 15,13 18,18 13,15 11,20 9,15 4,18 7,13 2,11 7,9 4,4 9,7"/>' },
          { id: "burst", label: "폭발형", kind: "polygon", points: [[32, 0], [39, 14], [54, 8], [50, 24], [64, 32], [50, 40], [54, 56], [39, 50], [32, 64], [25, 50], [10, 56], [14, 40], [0, 32], [14, 24], [10, 8], [25, 14]], icon: '<polygon class="shape-fill" points="11,2 13,7 18,4 16,9 21,11 16,13 18,18 13,15 11,20 9,15 4,18 6,13 1,11 6,9 4,4 9,7"/>' },
          { id: "ribbon", label: "리본", kind: "path", d: "M 0 8 L 20 8 L 20 0 L 44 0 L 44 8 L 64 8 L 52 26 L 64 44 L 44 44 L 44 52 L 20 52 L 20 44 L 0 44 L 12 26 Z", icon: '<path class="shape-fill" d="M3 6H8V4H16V6H21L18 10L21 14H16V16H8V14H3L6 10Z"/>' },
        ],
      },
      {
        title: "설명선",
        shapes: [
          { id: "calloutRect", label: "사각 설명선", kind: "path", d: "M 0 0 L 64 0 L 64 38 L 42 38 L 30 52 L 32 38 L 0 38 Z", icon: '<path class="shape-fill" d="M4 5H20V14H14L10 18L11 14H4Z"/>' },
          { id: "calloutRound", label: "둥근 설명선", kind: "path", d: "M 8 0 L 56 0 Q 64 0 64 8 L 64 36 Q 64 44 56 44 L 42 44 L 30 52 L 32 44 L 8 44 Q 0 44 0 36 L 0 8 Q 0 0 8 0 Z", icon: '<path class="shape-fill" d="M7 5H17Q20 5 20 8V13Q20 16 17 16H14L10 19L11 16H7Q4 16 4 13V8Q4 5 7 5Z"/>' },
          { id: "calloutOval", label: "타원 설명선", kind: "path", d: "M 32 0 C 50 0 64 10 64 24 C 64 38 50 48 32 48 C 27 48 22 47 18 46 L 4 54 L 10 42 C 4 38 0 32 0 24 C 0 10 14 0 32 0 Z", icon: '<path class="shape-fill" d="M12 4C18 4 21 7 21 11C21 15 17 18 11 18C9 18 8 17 7 17L3 20L5 16C3 15 2 13 2 11C2 7 6 4 12 4Z"/>' },
          { id: "calloutLine", label: "선 설명선", kind: "path", d: "M 0 0 L 50 0 L 50 30 L 22 30 L 6 52", fill: "none", icon: '<path d="M4 5H18V13H10L5 18"/>' },
        ],
      },
    ];

    function setStatus(text, ok = true) {
      const el = document.getElementById("status");
      el.className = ok ? "ok" : "err";
      el.textContent = text;
    }

    function snapValue(v) {
      if (!snapEnabled) return v;
      return Math.round(v / SNAP_STEP) * SNAP_STEP;
    }

    function updateSnapButton() {
      const btn = document.getElementById("snapToggleBtn");
      if (!btn) return;
      const label = snapEnabled ? "Snap: ON (5px)" : "Snap: OFF";
      btn.classList.toggle("active", snapEnabled);
      btn.title = label;
      btn.setAttribute("aria-label", label);
    }

    async function withApiErrors(operation) {
      try {
        return await operation();
      } catch (error) {
        const category = error.category || classifyApiError(error.message, error.status, error.payload);
        error.rawMessage = error.message;
        error.message = userMessageForError(category);
        throw error;
      }
    }

    function userMessageForError(category) {
      const messages = {
        DSL_PARSE_ERROR: "DSL 문서를 해석하지 못했습니다.",
        DSL_PATCH_ERROR: "선택한 도형의 변경 사항을 저장하지 못했습니다.",
        BUILD_ERROR: "문제 빌드에 실패했습니다.",
        SCHEMA_ERROR: "생성된 문서 구조가 올바르지 않습니다.",
        NETWORK_ERROR: "서버와 통신하지 못했습니다.",
        UNKNOWN_ERROR: "요청을 처리하지 못했습니다.",
      };
      return messages[category] || messages.UNKNOWN_ERROR;
    }

    function renderSvg(svgText) {
      const preview = document.getElementById("svgPreview");
      inlineTextEditState = null;
      renderSvgContainer(preview, svgText);
      selectedSlots = new Map();
      selectedTableCells = [];
      selectedSlotId = null;
      selectedElement = null;
      setState({ selectedIds: [], hoveredId: null });
      resizeState = null;
      bindSlotInteractions();
      updateCanvasGuide();
      updateCanvasControls();
      applyPickMode();
      updateSelectionHandles();
      updateTextEditControls();
    }

    function renderJsonView(id, value) {
      const el = document.getElementById(id);
      if (!el) return;
      if (value === null || value === undefined) {
        el.value = "";
        return;
      }
      el.value = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    }

    function renderArtifacts(artifacts) {
      renderSvg(artifacts?.svg || null);
      renderJsonView("semanticView", artifacts?.semantic || null);
      renderJsonView("solvableView", artifacts?.solvable || null);
      renderJsonView("layoutView", artifacts?.layout || null);
      renderJsonView("rendererView", artifacts?.renderer || null);
    }

    function getSvgPoint(svg, clientX, clientY) {
      return canvasSvgPoint(svg, clientX, clientY);
    }

    function svgBBoxClientRect(el) {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg || !el || !el.getBBox) return null;
      let box = null;
      try {
        box = el.getBBox();
      } catch (_) {
        box = null;
      }
      if (!box || (box.width <= 0 && box.height <= 0)) {
        box = elementHitBox(el, svg);
      }
      if (!box) return null;
      const ctm = svg.getScreenCTM();
      if (!ctm) return null;
      const point = svg.createSVGPoint();
      const corners = [
        [box.x, box.y],
        [box.x + box.width, box.y],
        [box.x, box.y + box.height],
        [box.x + box.width, box.y + box.height],
      ].map(([x, y]) => {
        point.x = x;
        point.y = y;
        return point.matrixTransform(ctm);
      });
      const xs = corners.map((p) => p.x);
      const ys = corners.map((p) => p.y);
      const left = Math.min(...xs);
      const right = Math.max(...xs);
      const top = Math.min(...ys);
      const bottom = Math.max(...ys);
      return { left, top, right, bottom, width: right - left, height: bottom - top };
    }

    function clientRectToSvgBox(svg, rect) {
      if (!svg || !rect || rect.width < 0 || rect.height < 0) return null;
      return canvasClientRectToSvgBox(svg, rect);
    }

    function inflatedBoxForStroke(el, box) {
      if (!el || !box) return box;
      const raw = el.getAttribute("stroke-width") || el.style?.getPropertyValue("stroke-width") || "0";
      const strokeWidth = Number.parseFloat(raw);
      const pad = Number.isFinite(strokeWidth) ? strokeWidth / 2 : 0;
      if (pad <= 0) return box;
      return {
        x: box.x - pad,
        y: box.y - pad,
        width: box.width + pad * 2,
        height: box.height + pad * 2,
      };
    }

    function visualSvgBox(el, svg) {
      if (!el || !svg) return null;
      const wasSelected = el.classList.contains("slot-selected");
      if (wasSelected) el.classList.remove("slot-selected");
      try {
        const rect = el.getBoundingClientRect && el.getBoundingClientRect();
        if (rect && (rect.width > 0 || rect.height > 0)) {
          return inflatedBoxForStroke(el, clientRectToSvgBox(svg, rect));
        }
      } catch (_) {
        // Fall through to geometry bbox.
      } finally {
        if (wasSelected) el.classList.add("slot-selected");
      }
      try {
        const raw = el.getBBox();
        const ctm = el.getCTM && el.getCTM();
        if (!ctm) return inflatedBoxForStroke(el, raw);
        const point = svg.createSVGPoint();
        const corners = [
          [raw.x, raw.y],
          [raw.x + raw.width, raw.y],
          [raw.x + raw.width, raw.y + raw.height],
          [raw.x, raw.y + raw.height],
        ].map(([x, y]) => {
          point.x = x;
          point.y = y;
          return point.matrixTransform(ctm);
        });
        const xs = corners.map((p) => p.x);
        const ys = corners.map((p) => p.y);
        const minX = Math.min(...xs);
        const minY = Math.min(...ys);
        const maxX = Math.max(...xs);
        const maxY = Math.max(...ys);
        return inflatedBoxForStroke(el, { x: minX, y: minY, width: maxX - minX, height: maxY - minY });
      } catch (_) {
        return null;
      }
    }

    function geometrySvgBox(el) {
      if (!el || !el.getBBox) return null;
      try {
        return inflatedBoxForStroke(el, el.getBBox());
      } catch (_) {
        return null;
      }
    }

    function pointsBox(points) {
      if (!points || !points.length) return null;
      const xs = points.map((p) => p.x);
      const ys = points.map((p) => p.y);
      const minX = Math.min(...xs);
      const minY = Math.min(...ys);
      const maxX = Math.max(...xs);
      const maxY = Math.max(...ys);
      return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
    }

    function sampleCubic(p0, p1, p2, p3, steps = 18) {
      const out = [];
      for (let i = 0; i <= steps; i += 1) {
        const t = i / steps;
        const mt = 1 - t;
        out.push({
          x: mt * mt * mt * p0.x + 3 * mt * mt * t * p1.x + 3 * mt * t * t * p2.x + t * t * t * p3.x,
          y: mt * mt * mt * p0.y + 3 * mt * mt * t * p1.y + 3 * mt * t * t * p2.y + t * t * t * p3.y,
        });
      }
      return out;
    }

    function sampleQuadratic(p0, p1, p2, steps = 18) {
      const out = [];
      for (let i = 0; i <= steps; i += 1) {
        const t = i / steps;
        const mt = 1 - t;
        out.push({
          x: mt * mt * p0.x + 2 * mt * t * p1.x + t * t * p2.x,
          y: mt * mt * p0.y + 2 * mt * t * p1.y + t * t * p2.y,
        });
      }
      return out;
    }

    function pathSampledBox(d) {
      const tokens = pathTokens(d);
      const points = [];
      let i = 0;
      let cmd = null;
      let current = { x: 0, y: 0 };
      let subpathStart = { x: 0, y: 0 };
      const isCommand = (token) => /^[a-zA-Z]$/.test(token);
      const num = (token) => Number(token);
      const addPoint = (x, y) => {
        current = { x, y };
        points.push(current);
      };
      while (i < tokens.length) {
        if (isCommand(tokens[i])) {
          cmd = tokens[i].toUpperCase();
          i += 1;
          if (cmd === "Z") {
            addPoint(subpathStart.x, subpathStart.y);
            continue;
          }
        }
        if (!cmd) break;
        const count = PATH_PARAM_COUNTS[cmd];
        if (!count || i + count > tokens.length) break;
        const vals = tokens.slice(i, i + count).map(num);
        if (vals.some((v) => !Number.isFinite(v))) break;
        if (cmd === "M") {
          addPoint(vals[0], vals[1]);
          subpathStart = { ...current };
        } else if (cmd === "L" || cmd === "T") {
          addPoint(vals[0], vals[1]);
        } else if (cmd === "H") {
          addPoint(vals[0], current.y);
        } else if (cmd === "V") {
          addPoint(current.x, vals[0]);
        } else if (cmd === "C") {
          const p0 = current;
          const p1 = { x: vals[0], y: vals[1] };
          const p2 = { x: vals[2], y: vals[3] };
          const p3 = { x: vals[4], y: vals[5] };
          points.push(...sampleCubic(p0, p1, p2, p3));
          current = p3;
        } else if (cmd === "S" || cmd === "Q") {
          const p0 = current;
          const p1 = { x: vals[0], y: vals[1] };
          const p2 = { x: vals[vals.length - 2], y: vals[vals.length - 1] };
          points.push(...sampleQuadratic(p0, p1, p2));
          current = p2;
        } else if (cmd === "A") {
          addPoint(vals[5], vals[6]);
        }
        i += count;
      }
      return pointsBox(points);
    }

    function slotValueBox(el) {
      if (!el) return null;
      const value = readSlotPatchValue(el);
      if (!value) return null;
      const tag = el.tagName.toLowerCase();
      let box = null;
      if ((tag === "rect" || tag === "image" || tag === "text") && value.x !== undefined && value.y !== undefined) {
        const width = value.width !== undefined ? Number(value.width) : 0;
        const height = value.height !== undefined ? Number(value.height) : 0;
        box = { x: Number(value.x), y: Number(value.y), width, height };
      } else if (tag === "circle" && value.cx !== undefined && value.cy !== undefined && value.r !== undefined) {
        const r = Number(value.r);
        box = { x: Number(value.cx) - r, y: Number(value.cy) - r, width: r * 2, height: r * 2 };
      } else if (tag === "line" && value.x1 !== undefined) {
        const x1 = Number(value.x1);
        const y1 = Number(value.y1);
        const x2 = Number(value.x2);
        const y2 = Number(value.y2);
        box = { x: Math.min(x1, x2), y: Math.min(y1, y2), width: Math.abs(x2 - x1), height: Math.abs(y2 - y1) };
      } else if (tag === "polygon" && Array.isArray(value.points)) {
        box = pointsBox(value.points.map(([x, y]) => ({ x: Number(x), y: Number(y) })));
      } else if (tag === "path" && typeof value.d === "string") {
        box = pathSampledBox(value.d);
      }
      return inflatedBoxForStroke(el, box);
    }

    function hideInlineTextEditor() {
      const editor = document.getElementById("inlineTextEditor");
      if (editor) editor.style.display = "none";
      inlineTextEditState = null;
    }

    async function finishInlineTextEdit(commit = true) {
      const state = inlineTextEditState;
      const editor = document.getElementById("inlineTextEditor");
      if (!state || !editor) return;
      inlineTextEditState = null;
      editor.style.display = "none";
      if (!commit) {
        state.el.textContent = state.originalText;
        updateTextEditControls();
        return;
      }
      const text = editor.value;
      if (text === state.originalText) {
        updateTextEditControls();
        return;
      }
      applyPatchValueToElement(state.el, { text });
      updateSelectionHandles();
      updateTextEditControls();
      try {
        let patches = [{ target: state.slotId, op: "update", value: { text } }];
        const tableBase = tableBaseFromSlotId(state.slotId);
        const tableItem = tableBase ? selectedSlots.get(tableBase) : null;
        if (tableItem && tableItem.isTableGroup) {
          const layoutValues = tableRelayoutValues(tableItem);
          patches = layoutValues.map((entry) => ({
            target: entry.slotId,
            op: "update",
            value: entry.slotId === state.slotId ? { ...entry.value, text } : entry.value,
          }));
          if (!patches.some((patch) => patch.target === state.slotId)) {
            patches.push({ target: state.slotId, op: "update", value: { text } });
          }
        }
        await commitPatches(patches, `텍스트 수정 완료: ${state.slotId}`);
      } catch (e) {
        setStatus(String(e), false);
      }
    }

    function beginInlineTextEdit(el, slotId, ev) {
      const editor = document.getElementById("inlineTextEditor");
      const container = document.getElementById("svgPreview");
      const rect = svgBBoxClientRect(el);
      if (!editor || !container || !rect) return false;
      setSelectedElement(el, slotId, false);
      const containerRect = container.getBoundingClientRect();
      const scale = (() => {
        const svg = container.querySelector("svg");
        const ctm = svg ? svg.getScreenCTM() : null;
        return ctm ? Math.sqrt(ctm.a * ctm.a + ctm.b * ctm.b) : 1;
      })();
      const fontSize = Number(el.getAttribute("font-size") || 28) * scale;
      editor.value = el.textContent || "";
      editor.style.left = `${rect.left - containerRect.left - 2}px`;
      editor.style.top = `${rect.top - containerRect.top - 2}px`;
      editor.style.width = `${Math.max(48, rect.width + 12)}px`;
      editor.style.height = `${Math.max(24, rect.height + 8)}px`;
      editor.style.fontSize = `${Math.max(12, fontSize)}px`;
      editor.style.fontFamily = el.getAttribute("font-family") || '"Segoe UI", "Pretendard", sans-serif';
      editor.style.display = "block";
      inlineTextEditState = { el, slotId, originalText: el.textContent || "" };
      editor.onkeydown = (keyEv) => {
        if (keyEv.key === "Enter") {
          keyEv.preventDefault();
          finishInlineTextEdit(true);
        } else if (keyEv.key === "Escape") {
          keyEv.preventDefault();
          finishInlineTextEdit(false);
        }
      };
      editor.onblur = () => finishInlineTextEdit(true);
      requestAnimationFrame(() => {
        editor.focus();
        editor.select();
      });
      setStatus(`텍스트 편집: ${slotId}`, true);
      ev.preventDefault();
      ev.stopPropagation();
      return true;
    }

    async function commitPatches(patches, reason = "저장 완료", withBuild = false, problemId = currentProblemId, formatSource = false) {
      if (!problemId) return;
      if (!patches || !patches.length) return;
      if (!(document.getElementById("dslEditor").value || "").trim()) {
        throw new Error("DSL 파일이 비어 있어 편집할 수 없습니다. 유효한 DSL을 먼저 복구하거나 저장하세요.");
      }
      const preserveSelection = Array.from(selectedSlots.keys());
      setState({
        pendingPatches: [...getState().pendingPatches, ...patches],
        dirty: true,
        saving: true,
        saveStatus: "saving",
        error: null,
      });
      const savePromise = withApiErrors(() => (
        withBuild
          ? applyLayoutPatchesAndBuild(problemId, patches, { format: formatSource })
          : applyLayoutPatches(problemId, patches, { format: formatSource })
      ));
      pendingPatchSaves.push(savePromise);
      let data;
      try {
        data = await savePromise;
      } finally {
        pendingPatchSaves = pendingPatchSaves.filter((item) => item !== savePromise);
      }
      if (problemId === currentProblemId) {
        document.getElementById("dslEditor").value = data.dsl || "";
        setState({
          dsl: data.dsl || "",
          pendingPatches: [],
          dirty: false,
          saving: false,
          saveStatus: "saved",
        });
      }
      if (withBuild) {
        if (problemId === currentProblemId) {
          const nextArtifacts = data.artifacts || getState().artifacts || null;
          if (nextArtifacts && nextArtifacts.svg) {
            renderArtifacts(nextArtifacts);
          }
          setState({ artifacts: nextArtifacts, building: false, buildStatus: "built" });
          renderLog(data.build?.stdout || "", data.build?.stderr || "");
          restoreSelection(preserveSelection);
        }
      }
      const last = patches[patches.length - 1];
      const slotId = last.target;
      const value = last.value;
      if (problemId === currentProblemId) {
        document.getElementById("slotId").value = slotId;
        document.getElementById("patchJson").value = value === undefined ? "" : JSON.stringify(value, null, 2);
        updateInspectorControls();
        setStatus(reason, true);
      }
    }

    function restoreSelection(slotIds) {
      if (!slotIds || !slotIds.length) return;
      clearSelection();
      for (const slotId of slotIds) {
        const el = findElementBySlotId(slotId);
        if (el) setSelectedElement(el, slotId, true);
      }
      updateSelectionHandles();
      updateTextEditControls();
    }

    async function commitSlotPatch(slotId, value, reason = "저장 완료", withBuild = false) {
      await commitPatches([{ target: slotId, op: "update", value }], reason, withBuild);
    }

    function queueDragCommit(task) {
      if (dragCommitTimer) clearTimeout(dragCommitTimer);
      dragCommitTask = task;
      dragCommitTimer = setTimeout(async () => {
        dragCommitTimer = null;
        const queuedTask = dragCommitTask;
        dragCommitTask = null;
        if (queuedTask) await queuedTask();
      }, 120);
    }

    async function flushPendingPatchSaves() {
      if (dragCommitTimer) {
        clearTimeout(dragCommitTimer);
        dragCommitTimer = null;
        const queuedTask = dragCommitTask;
        dragCommitTask = null;
        if (queuedTask) await queuedTask();
      }
      while (pendingPatchSaves.length) {
        await Promise.allSettled([...pendingPatchSaves]);
      }
    }

    function extractDslSlotIds() {
      const layoutText = document.getElementById("layoutView")?.value || "";
      const dsl = document.getElementById("dslEditor").value || "";
      if (dslSlotIdCache.ids && dslSlotIdCache.layoutText === layoutText && dslSlotIdCache.dsl === dsl) {
        return dslSlotIdCache.ids;
      }
      const ids = new Set();
      if (layoutText.trim()) {
        try {
          const layout = JSON.parse(layoutText);
          const slots = Array.isArray(layout.slots) ? layout.slots : [];
          for (const slot of slots) {
            if (slot && typeof slot.id === "string" && slot.id) ids.add(slot.id);
          }
        } catch (_) {
          // Fall back to source scanning below while the layout pane is stale or invalid.
        }
      }

      const re = /\bid\s*=\s*["']([^"']+)["']/g;
      let m = null;
      while ((m = re.exec(dsl)) !== null) {
        ids.add(m[1]);
      }
      dslSlotIdCache = { layoutText, dsl, ids };
      return ids;
    }

    function extractSourceDslSlotIds() {
      const dsl = document.getElementById("dslEditor").value || "";
      if (sourceDslSlotIdCache.ids && sourceDslSlotIdCache.dsl === dsl) {
        return sourceDslSlotIdCache.ids;
      }
      const ids = new Set();
      const re = /\bid\s*=\s*["']([^"']+)["']/g;
      let m = null;
      while ((m = re.exec(dsl)) !== null) {
        ids.add(m[1]);
      }
      sourceDslSlotIdCache = { dsl, ids };
      return ids;
    }

    function extractRendererSlotRefs() {
      const rendererText = document.getElementById("rendererView")?.value || "";
      if (rendererSlotRefCache.byElementId && rendererSlotRefCache.rendererText === rendererText) {
        return rendererSlotRefCache.byElementId;
      }
      const byElementId = new Map();
      if (rendererText.trim()) {
        try {
          const renderer = JSON.parse(rendererText);
          const visit = (elements) => {
            for (const element of Array.isArray(elements) ? elements : []) {
              const id = typeof element?.id === "string" ? element.id : "";
              if (id) {
                const refs = element.refs && typeof element.refs === "object" ? element.refs : {};
                const candidates = [
                  typeof refs.layout_slot_id === "string" ? refs.layout_slot_id : "",
                  typeof element.source_ref === "string" ? element.source_ref : "",
                ].filter(Boolean);
                if (candidates.length) byElementId.set(id, candidates);
              }
              if (Array.isArray(element?.elements)) visit(element.elements);
            }
          };
          visit(renderer.elements);
        } catch (_) {
          // Renderer pane can be stale while a problem is loading.
        }
      }
      rendererSlotRefCache = { rendererText, byElementId };
      return byElementId;
    }

    function isDirectDslSlotId(slotId) {
      return extractDslSlotIds().has(slotId);
    }

    function currentCanvasBox() {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return { x: 0, y: 0, width: 960, height: 640 };
      const vb = svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal : null;
      const x = vb ? Number(vb.x || 0) : 0;
      const y = vb ? Number(vb.y || 0) : 0;
      const width = vb && vb.width ? vb.width : Number(svg.getAttribute("width") || 960);
      const height = vb && vb.height ? vb.height : Number(svg.getAttribute("height") || 640);
      return { x, y, width, height };
    }

    function defaultInsertOrigin(width, height) {
      const canvas = currentCanvasBox();
      return {
        x: snapValue(Math.max(10, (canvas.width - width) / 2)),
        y: snapValue(Math.max(10, (canvas.height - height) / 2)),
      };
    }

    function selectedInsertOrigin(width, height) {
      if (selectedSlots.size !== 1) return null;
      const item = Array.from(selectedSlots.values())[0];
      if (!item || item.isCanvas || item.isFraction) return null;
      const box = itemBBox(item);
      if (!box || !Number.isFinite(box.x) || !Number.isFinite(box.y) || !Number.isFinite(box.width) || !Number.isFinite(box.height)) return null;
      return {
        x: snapValue(box.x + box.width / 2 - width / 2),
        y: snapValue(box.y + box.height / 2 - height / 2),
      };
    }

    function selectedInsertRegionId() {
      if (selectedSlots.size !== 1) return null;
      const item = Array.from(selectedSlots.values())[0];
      if (!item || item.isCanvas) return null;
      const ids = Array.isArray(item.slotIds) && item.slotIds.length ? item.slotIds : [item.slotId];
      for (const slotId of ids) {
        const regionId = layoutRegionBySlotId(slotId);
        if (regionId) return regionId;
      }
      return null;
    }

    function firstUsableRegionId() {
      const layoutText = document.getElementById("layoutView")?.value || "";
      if (!layoutText.trim()) return null;
      try {
        const layout = JSON.parse(layoutText);
        const regions = Array.isArray(layout.regions) ? layout.regions : [];
        const diagram = regions.find((region) => region && (region.role === "diagram" || region.flow === "absolute"));
        const first = diagram || regions[0];
        return first && typeof first.id === "string" ? first.id : null;
      } catch (_) {
        return null;
      }
    }

    function uniqueInsertedSlotId(base) {
      const ids = extractDslSlotIds();
      const clean = String(base || "shape").replace(/[^a-zA-Z0-9_]+/g, "_").replace(/^_+|_+$/g, "") || "shape";
      for (let i = 1; i < 10000; i += 1) {
        const candidate = `slot.inserted.${clean}.${i}`;
        if (!ids.has(candidate)) return candidate;
      }
      return `slot.inserted.${clean}.${Date.now()}`;
    }

    function uniqueFigureBase(base) {
      const ids = extractDslSlotIds();
      const clean = String(base || "figure").replace(/[^a-zA-Z0-9_]+/g, "_").replace(/^_+|_+$/g, "") || "figure";
      for (let i = 1; i < 10000; i += 1) {
        const candidate = `slot.figure.${clean}_${i}`;
        let exists = false;
        for (const id of ids) {
          if (id === candidate || id.startsWith(`${candidate}.`)) {
            exists = true;
            break;
          }
        }
        if (!exists) return candidate;
      }
      return `slot.figure.${clean}_${Date.now()}`;
    }

    function tableSlotBase(slotId) {
      const m = String(slotId || "").match(/^(slot\.table(?:_\d+)?)(?:\.|$)/);
      return m ? m[1] : null;
    }

    function graphPaperSlotBase(slotId) {
      const m = String(slotId || "").match(/^(slot\.graphpaper(?:_\d+)?)(?:\.|$)/);
      return m ? m[1] : null;
    }

    function mathSlotBase(slotId) {
      const m = String(slotId || "").match(/^(slot\.math\.[a-zA-Z0-9_]+)(?:\.(?:whole|num|bar|den))?$/);
      return m ? m[1] : null;
    }

    function uniqueTableBase() {
      const ids = extractDslSlotIds();
      const used = new Set();
      for (const id of ids) {
        const base = tableSlotBase(id);
        if (base) used.add(base);
      }
      if (!used.has("slot.table")) return "slot.table";
      for (let i = 1; i < 10000; i += 1) {
        const candidate = `slot.table_${i}`;
        if (!used.has(candidate)) return candidate;
      }
      return `slot.table_${Date.now()}`;
    }

    function uniqueGraphPaperBase() {
      const ids = extractDslSlotIds();
      const used = new Set();
      for (const id of ids) {
        const base = graphPaperSlotBase(id);
        if (base) used.add(base);
      }
      if (!used.has("slot.graphpaper")) return "slot.graphpaper";
      for (let i = 1; i < 10000; i += 1) {
        const candidate = `slot.graphpaper_${i}`;
        if (!used.has(candidate)) return candidate;
      }
      return `slot.graphpaper_${Date.now()}`;
    }

    function uniqueMathBase(kind = "frac") {
      const ids = extractDslSlotIds();
      const used = new Set();
      for (const id of ids) {
        const base = mathSlotBase(id);
        if (base) used.add(base);
      }
      const clean = String(kind || "expr").replace(/[^a-zA-Z0-9_]+/g, "_").replace(/^_+|_+$/g, "") || "expr";
      const first = `slot.math.${clean}`;
      if (!used.has(first)) return first;
      for (let i = 1; i < 10000; i += 1) {
        const candidate = `slot.math.${clean}_${i}`;
        if (!used.has(candidate)) return candidate;
      }
      return `slot.math.${clean}_${Date.now()}`;
    }

    function scalePoints(points, x, y, width, height, sourceWidth = 64, sourceHeight = 52) {
      return points.map(([px, py]) => [
        snapValue(x + (px / sourceWidth) * width),
        snapValue(y + (py / sourceHeight) * height),
      ]);
    }

    function scaleShapePath(d, x, y, width, height, sourceWidth = 64, sourceHeight = 52) {
      return canvasTransformPathD(
        d,
        (px, py) => [
          snapValue(x + (px / sourceWidth) * width),
          snapValue(y + (py / sourceHeight) * height),
        ],
        (rx, ry) => [snapValue((rx / sourceWidth) * width), snapValue((ry / sourceHeight) * height)]
      );
    }

    function scaledCompositePart(part, x, y, width, height, sourceWidth = 64, sourceHeight = 52) {
      const sx = width / sourceWidth;
      const sy = height / sourceHeight;
      const content = {};
      for (const [key, value] of Object.entries(part || {})) {
        if (["id", "kind"].includes(key)) continue;
        content[key] = value;
      }
      if (part.kind === "rect") {
        content.x = snapValue(x + Number(part.x || 0) * sx);
        content.y = snapValue(y + Number(part.y || 0) * sy);
        content.width = snapValue(Number(part.width || 0) * sx);
        content.height = snapValue(Number(part.height || 0) * sy);
        if (part.rx !== undefined) content.rx = snapValue(Number(part.rx || 0) * sx);
        if (part.ry !== undefined) content.ry = snapValue(Number(part.ry || 0) * sy);
      } else if (part.kind === "circle") {
        content.cx = snapValue(x + Number(part.cx || 0) * sx);
        content.cy = snapValue(y + Number(part.cy || 0) * sy);
        content.r = snapValue(Number(part.r || 0) * Math.min(sx, sy));
      } else if (part.kind === "line") {
        content.x1 = snapValue(x + Number(part.x1 || 0) * sx);
        content.y1 = snapValue(y + Number(part.y1 || 0) * sy);
        content.x2 = snapValue(x + Number(part.x2 || 0) * sx);
        content.y2 = snapValue(y + Number(part.y2 || 0) * sy);
      } else if (part.kind === "polygon") {
        content.points = scalePoints(part.points || [], x, y, width, height, sourceWidth, sourceHeight);
      } else if (part.kind === "path") {
        content.d = scaleShapePath(part.d || "", x, y, width, height, sourceWidth, sourceHeight);
      }
      return { kind: part.kind, content };
    }

    function addRegionToPatch(value) {
      const regionId = firstUsableRegionId();
      return regionId ? { ...value, region_id: regionId } : value;
    }

    function compositeShapePatches(def) {
      const fallbackWidth = Number(def.w || def.sourceWidth || 80);
      const fallbackHeight = Number(def.h || def.sourceHeight || fallbackWidth);
      const { x, y } = defaultInsertOrigin(fallbackWidth, fallbackHeight);
      const base = uniqueFigureBase(def.id);
      const regionId = firstUsableRegionId();
      const patches = [];
      for (const part of def.parts || []) {
        if (!part || !part.id || !part.kind) continue;
        const value = scaledCompositePart(part, x, y, fallbackWidth, fallbackHeight, def.sourceWidth || fallbackWidth, def.sourceHeight || fallbackHeight);
        patches.push({
          target: `${base}.${part.id}`,
          op: "add",
          value: regionId ? { ...value, region_id: regionId } : value,
        });
      }
      return { base, patches };
    }

    function tablePatches(rows, cols) {
      const cleanRows = Math.max(1, Math.min(20, Number(rows) || 1));
      const cleanCols = Math.max(1, Math.min(20, Number(cols) || 1));
      const cellWidth = 105;
      const cellHeight = 58;
      const width = cleanCols * cellWidth;
      const height = cleanRows * cellHeight;
      const { x, y } = defaultInsertOrigin(width, height);
      const base = uniqueTableBase();
      const regionId = firstUsableRegionId();
      const withRegion = (value) => regionId ? { ...value, region_id: regionId } : value;
      const patches = [];
      patches.push({
        target: `${base}.outer`,
        op: "add",
        value: withRegion({
          kind: "rect",
          content: { x, y, width, height, fill: "#ffffff", stroke: "#111827", stroke_width: 1 },
        }),
      });
      for (let r = 1; r <= cleanRows; r += 1) {
        for (let c = 1; c <= cleanCols; c += 1) {
          patches.push({
            target: `${base}.r${r}c${c}.fill`,
            op: "add",
            value: withRegion({
              kind: "rect",
              content: {
                x: snapValue(x + (c - 1) * cellWidth),
                y: snapValue(y + (r - 1) * cellHeight),
                width: cellWidth,
                height: cellHeight,
                fill: "none",
                stroke: "none",
                stroke_width: 0,
              },
            }),
          });
        }
      }
      for (let c = 1; c < cleanCols; c += 1) {
        const px = snapValue(x + c * cellWidth);
        patches.push({
          target: `${base}.v${c}`,
          op: "add",
          value: withRegion({
            kind: "line",
            content: { x1: px, y1: y, x2: px, y2: y + height, stroke: "#111827", stroke_width: 1 },
          }),
        });
      }
      for (let r = 1; r < cleanRows; r += 1) {
        const py = snapValue(y + r * cellHeight);
        patches.push({
          target: `${base}.h${r}`,
          op: "add",
          value: withRegion({
            kind: "line",
            content: { x1: x, y1: py, x2: x + width, y2: py, stroke: "#111827", stroke_width: 1 },
          }),
        });
      }
      for (let r = 1; r <= cleanRows; r += 1) {
        for (let c = 1; c <= cleanCols; c += 1) {
          const fontSize = 22;
          const baselineOffset = cellHeight / 2 + fontSize * 0.35;
          patches.push({
            target: `${base}.r${r}c${c}`,
            op: "add",
            value: withRegion({
              kind: "text",
              content: {
                text: "",
                x: snapValue(x + (c - 0.5) * cellWidth),
                y: snapValue(y + (r - 1) * cellHeight + baselineOffset),
                font_size: fontSize,
                max_width: Math.max(8, cellWidth - 20),
                anchor: "middle",
                style_role: "table",
                fill: "#111827",
              },
            }),
          });
        }
      }
      return { base, patches };
    }

    function graphPaperPatches(rows, cols) {
      const cleanRows = Math.max(1, Math.min(40, Number(rows) || 1));
      const cleanCols = Math.max(1, Math.min(40, Number(cols) || 1));
      const cellSize = 25;
      const width = cleanCols * cellSize;
      const height = cleanRows * cellSize;
      const { x, y } = defaultInsertOrigin(width, height);
      const originX = snapValue(x);
      const originY = snapValue(y);
      const base = uniqueGraphPaperBase();
      const regionId = firstUsableRegionId();
      const withRegion = (value) => regionId ? { ...value, region_id: regionId } : value;
      const patches = [];
      const stroke = "#2563eb";
      const stroke_width = 1;
      for (let c = 0; c <= cleanCols; c += 1) {
        const px = originX + c * cellSize;
        patches.push({
          target: `${base}.v${c}`,
          op: "add",
          value: withRegion({
            kind: "line",
            content: { x1: px, y1: originY, x2: px, y2: originY + height, stroke, stroke_width },
          }),
        });
      }
      for (let r = 0; r <= cleanRows; r += 1) {
        const py = originY + r * cellSize;
        patches.push({
          target: `${base}.h${r}`,
          op: "add",
          value: withRegion({
            kind: "line",
            content: { x1: originX, y1: py, x2: originX + width, y2: py, stroke, stroke_width },
          }),
        });
      }
      return { base, patches };
    }

    function configList(value) {
      return String(value ?? "").split(",").map((item) => item.trim()).filter(Boolean);
    }

    function configListValue(items, index, fallback) {
      if (!Array.isArray(items) || !items.length) return fallback;
      return items[Math.min(index, items.length - 1)] || fallback;
    }

    function clampInt(value, min, max, fallback) {
      const num = Number(value);
      const clean = Number.isFinite(num) ? Math.trunc(num) : fallback;
      return Math.max(min, Math.min(max, clean));
    }

    function barModelPatches({
      bars = 2,
      cells = 3,
      shadedCounts = "2,2",
      fillColors = "#f3d7ea",
      stroke = "#666666",
      dashed = true,
    } = {}) {
      const cleanBars = clampInt(bars, 1, 8, 2);
      const cleanCells = clampInt(cells, 1, 20, 3);
      const shadedList = configList(shadedCounts);
      const colorList = configList(fillColors);
      const cellWidth = 58;
      const barHeight = 40;
      const barGap = 54;
      const width = cleanCells * cellWidth;
      const height = cleanBars * barHeight + (cleanBars - 1) * barGap;
      const { x, y } = defaultInsertOrigin(width, height);
      const base = uniqueFigureBase("bar_model");
      const regionId = firstUsableRegionId();
      const withRegion = (value) => regionId ? { ...value, region_id: regionId } : value;
      const strokeColor = String(stroke || "#666666").trim() || "#666666";
      const patches = [];

      for (let barIndex = 0; barIndex < cleanBars; barIndex += 1) {
        const barY = snapValue(y + barIndex * (barHeight + barGap));
        const shaded = clampInt(configListValue(shadedList, barIndex, "0"), 0, cleanCells, 0);
        const fill = String(configListValue(colorList, barIndex, "#f3d7ea") || "#f3d7ea").trim() || "#f3d7ea";
        for (let cellIndex = 0; cellIndex < shaded; cellIndex += 1) {
          patches.push({
            target: `${base}.bar${barIndex + 1}.shade${cellIndex + 1}`,
            op: "add",
            value: withRegion({
              kind: "rect",
              content: {
                x: snapValue(x + cellIndex * cellWidth),
                y: barY,
                width: cellWidth,
                height: barHeight,
                fill,
                stroke: "none",
                stroke_width: 0,
              },
            }),
          });
        }
        patches.push({
          target: `${base}.bar${barIndex + 1}.outline`,
          op: "add",
          value: withRegion({
            kind: "rect",
            content: {
              x,
              y: barY,
              width,
              height: barHeight,
              fill: "none",
              stroke: strokeColor,
              stroke_width: 1.5,
            },
          }),
        });
        for (let cellIndex = 1; cellIndex < cleanCells; cellIndex += 1) {
          const px = snapValue(x + cellIndex * cellWidth);
          const content = {
            x1: px,
            y1: barY,
            x2: px,
            y2: snapValue(barY + barHeight),
            stroke: strokeColor,
            stroke_width: 1,
          };
          if (dashed) content.stroke_dasharray = "5 3";
          patches.push({
            target: `${base}.bar${barIndex + 1}.div${cellIndex}`,
            op: "add",
            value: withRegion({ kind: "line", content }),
          });
        }
      }

      return { base, patches };
    }

    function tickBarPatches({
      rows = 2,
      totalTicks = 14,
      filledTicks = "9,10",
      majorEvery = 7,
      labels = "",
      unit = "m",
      showScaleLabels = true,
      showFractionLabel = true,
      axisColor = "#111111",
      fillColor = "#2563eb",
    } = {}) {
      const cleanRows = clampInt(rows, 1, 8, 2);
      const cleanTotal = clampInt(totalTicks, 1, 40, 14);
      const cleanMajor = clampInt(majorEvery, 0, cleanTotal, 7);
      const filledList = configList(filledTicks);
      const labelList = configList(labels);
      const width = 464;
      const rowGap = 96;
      const labelWidth = 118;
      const height = Math.max(70, (cleanRows - 1) * rowGap + 82);
      const { x, y } = defaultInsertOrigin(labelWidth + width, height);
      const axisX = snapValue(x + labelWidth);
      const base = uniqueFigureBase("tick_bar");
      const regionId = firstUsableRegionId();
      const withRegion = (value) => regionId ? { ...value, region_id: regionId } : value;
      const patches = [];
      const stroke = String(axisColor || "#111111").trim() || "#111111";
      const fill = String(fillColor || "#2563eb").trim() || "#2563eb";
      const step = width / cleanTotal;
      const unitText = String(unit || "").trim();

      for (let rowIndex = 0; rowIndex < cleanRows; rowIndex += 1) {
        const rowBase = `${base}.row${rowIndex + 1}`;
        const axisY = snapValue(y + 30 + rowIndex * rowGap);
        const filled = clampInt(configListValue(filledList, rowIndex, "0"), 0, cleanTotal, 0);
        const rowLabel = String(configListValue(labelList, rowIndex, "") || "").trim();
        if (rowLabel) {
          patches.push({
            target: `${rowBase}.label`,
            op: "add",
            value: withRegion({
              kind: "text",
              content: {
                text: rowLabel,
                x: snapValue(x),
                y: snapValue(axisY + 9),
                font_size: 28,
                style_role: "label",
                fill: stroke,
              },
            }),
          });
        }
        if (filled > 0) {
          patches.push({
            target: `${rowBase}.fill`,
            op: "add",
            value: withRegion({
              kind: "line",
              content: {
                x1: axisX,
                y1: axisY,
                x2: snapValue(axisX + filled * step),
                y2: axisY,
                stroke: fill,
                stroke_width: 8,
              },
            }),
          });
        }
        patches.push({
          target: `${rowBase}.axis`,
          op: "add",
          value: withRegion({
            kind: "line",
            content: {
              x1: axisX,
              y1: axisY,
              x2: snapValue(axisX + width),
              y2: axisY,
              stroke,
              stroke_width: 2,
            },
          }),
        });
        for (let tick = 0; tick <= cleanTotal; tick += 1) {
          const isMajor = cleanMajor > 0 && tick % cleanMajor === 0;
          const tickHeight = isMajor ? 18 : 14;
          const px = snapValue(axisX + tick * step);
          patches.push({
            target: `${rowBase}.tick${tick}`,
            op: "add",
            value: withRegion({
              kind: "line",
              content: {
                x1: px,
                y1: snapValue(axisY - tickHeight / 2),
                x2: px,
                y2: snapValue(axisY + tickHeight / 2),
                stroke,
                stroke_width: 2,
              },
            }),
          });
          if (isMajor && showScaleLabels) {
            const value = cleanMajor > 0 ? tick / cleanMajor : tick;
            const label = tick === cleanTotal && unitText ? `${value}(${unitText})` : String(value);
            patches.push({
              target: `${rowBase}.label${tick}`,
              op: "add",
              value: withRegion({
                kind: "text",
                content: {
                  text: label,
                  x: snapValue(px - (tick === 0 ? 6 : tick === cleanTotal ? 14 : 8)),
                  y: snapValue(axisY + 34),
                  font_size: 26,
                  style_role: "label",
                  fill: stroke,
                },
              }),
            });
          }
        }
        if (showFractionLabel && cleanMajor > 0 && cleanMajor < cleanTotal) {
          patches.push({
            target: `${rowBase}.major_fraction`,
            op: "add",
            value: withRegion({
              kind: "text",
              content: {
                text: `${cleanMajor}/${cleanMajor}`,
                x: snapValue(axisX + cleanMajor * step - 18),
                y: snapValue(axisY - 22),
                font_size: 24,
                style_role: "label",
                fill: stroke,
              },
            }),
          });
        }
      }

      return { base, patches };
    }

    function cleanMathText(value, fallback) {
      const text = String(value ?? "").trim();
      return text || fallback;
    }

    function fractionPatches({ mixed = false, whole = "1", numerator = "1", denominator = "2" } = {}) {
      const wholeText = cleanMathText(whole, "1");
      const numeratorText = cleanMathText(numerator, "1");
      const denominatorText = cleanMathText(denominator, "2");
      const base = uniqueMathBase(mixed ? "mixed_fraction" : "fraction");
      const fontSize = 30;
      const barWidth = 42;
      const width = mixed ? 88 : 54;
      const height = 72;
      const { x, y } = selectedInsertOrigin(width, height) || defaultInsertOrigin(width, height);
      const fractionX = mixed ? snapValue(x + 58) : snapValue(x + width / 2);
      const numeratorY = snapValue(y + 22);
      const barY = snapValue(y + 36);
      const denominatorY = snapValue(y + 58);
      const patches = [];
      const regionId = selectedInsertRegionId() || firstUsableRegionId();
      const withRegion = (value) => regionId ? { ...value, region_id: regionId } : value;

      if (mixed) {
        patches.push({
          target: `${base}.whole`,
          op: "add",
          value: withRegion({
            kind: "text",
            content: {
              text: wholeText,
              x: snapValue(x + 18),
              y: snapValue(y + 44),
              font_size: fontSize,
              anchor: "middle",
              style_role: "body",
              fill: "#222222",
            },
          }),
        });
      }

      patches.push({
        target: `${base}.num`,
        op: "add",
        value: withRegion({
          kind: "text",
          content: {
            text: numeratorText,
            x: fractionX,
            y: numeratorY,
            font_size: fontSize,
            anchor: "middle",
            style_role: "body",
            fill: "#222222",
          },
        }),
      });
      patches.push({
        target: `${base}.bar`,
        op: "add",
        value: withRegion({
          kind: "line",
          content: {
            x1: snapValue(fractionX - barWidth / 2),
            y1: barY,
            x2: snapValue(fractionX + barWidth / 2),
            y2: barY,
            stroke: "#222222",
            stroke_width: 2.2,
          },
        }),
      });
      patches.push({
        target: `${base}.den`,
        op: "add",
        value: withRegion({
          kind: "text",
          content: {
            text: denominatorText,
            x: fractionX,
            y: denominatorY,
            font_size: fontSize,
            anchor: "middle",
            style_role: "body",
            fill: "#222222",
          },
        }),
      });
      return { base, patches };
    }

    async function insertTable(rows, cols) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      const { base, patches } = tablePatches(rows, cols);
      await commitPatches(patches, `표 삽입 완료: ${cols}열 x ${rows}행`);
      restoreSelection([`${base}.outer`]);
    }

    async function insertGraphPaper(rows, cols) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      const { base, patches } = graphPaperPatches(rows, cols);
      await commitPatches(patches, `모눈종이 삽입 완료: ${cols}칸 x ${rows}칸`);
      restoreSelection([`${base}.v0`]);
    }

    async function insertBarModel(options) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      const { base, patches } = barModelPatches(options);
      await commitPatches(patches, `막대 모델 삽입 완료: ${patches.length}개`);
      restoreSelection([`${base}.bar1.outline`]);
    }

    async function insertTickBar(options) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      const { base, patches } = tickBarPatches(options);
      await commitPatches(patches, `눈금 막대 삽입 완료: ${patches.length}개`);
      restoreSelection([`${base}.row1.axis`]);
    }

    async function insertFractionExpression(options) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      const { base, patches } = fractionPatches(options);
      await commitPatches(patches, `${options?.mixed ? "대분수" : "분수"} 삽입 완료`);
      restoreSelection([`${base}.num`]);
    }


    function shapePayload(def) {
      const width = Number(def.w || 120);
      const height = Number(def.h || (def.kind === "line" ? 70 : 86));
      const { x, y } = defaultInsertOrigin(width, height);
      const stroke = def.stroke || DEFAULT_SHAPE_STYLE.stroke;
      const fill = def.fill !== undefined ? def.fill : DEFAULT_SHAPE_STYLE.fill;
      const stroke_width = def.stroke_width || DEFAULT_SHAPE_STYLE.stroke_width;

      if (def.kind === "line") {
        const horizontal = def.line === "horizontal";
        const vertical = def.line === "vertical";
        const content = horizontal
          ? { x1: x, y1: y + height / 2, x2: x + width, y2: y + height / 2, stroke, stroke_width }
          : vertical
            ? { x1: x + width / 2, y1: y, x2: x + width / 2, y2: y + height, stroke, stroke_width }
            : { x1: x, y1: y + height, x2: x + width, y2: y, stroke, stroke_width };
        return addRegionToPatch({ kind: "line", content });
      }
      if (def.kind === "rect") {
        return addRegionToPatch({
          kind: "rect",
          content: {
            x,
            y,
            width,
            height,
            rx: def.rx,
            ry: def.ry,
            fill,
            stroke,
            stroke_width,
          },
        });
      }
      if (def.kind === "circle") {
        const r = Number(def.r || Math.min(width, height) / 2);
        return addRegionToPatch({
          kind: "circle",
          content: {
            cx: x + r,
            cy: y + r,
            r,
            fill,
            stroke,
            stroke_width,
          },
        });
      }
      if (def.kind === "polygon") {
        return addRegionToPatch({
          kind: "polygon",
          content: {
            points: scalePoints(def.points, x, y, width, height, def.sourceWidth || 64, def.sourceHeight || 52),
            fill,
            stroke,
            stroke_width,
          },
        });
      }
      return addRegionToPatch({
        kind: "path",
        content: {
          d: scaleShapePath(def.d, x, y, width, height, def.sourceWidth || 64, def.sourceHeight || 52),
          fill,
          stroke,
          stroke_width,
        },
      });
    }

    function textPayload() {
      const fontSize = 24;
      const { x, y } = defaultInsertOrigin(120, fontSize * 1.2);
      return addRegionToPatch({
        kind: "text",
        content: {
          text: "텍스트",
          x,
          y: y + fontSize,
          font_size: fontSize,
          fill: "#111827",
        },
      });
    }

    function textBoxPayload() {
      const width = 360;
      const height = 70;
      const { x, y } = defaultInsertOrigin(width, height);
      return addRegionToPatch({
        kind: "text_box",
        content: {
          text: "텍스트",
          x,
          y,
          width,
          height,
          font_size: 24,
          fill: "#111827",
        },
      });
    }

    function readFileAsDataUrl(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ""));
        reader.onerror = () => reject(reader.error || new Error("그림 파일을 읽을 수 없습니다."));
        reader.readAsDataURL(file);
      });
    }

    function imageSizeFromDataUrl(href) {
      return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve({ width: img.naturalWidth || 240, height: img.naturalHeight || 160 });
        img.onerror = () => resolve({ width: 240, height: 160 });
        img.src = href;
      });
    }

    async function imagePayloadFromFile(file) {
      if (!file || !file.type || !file.type.startsWith("image/")) throw new Error("이미지 파일을 선택하세요.");
      const href = await readFileAsDataUrl(file);
      const intrinsic = await imageSizeFromDataUrl(href);
      const maxWidth = 320;
      const maxHeight = 240;
      const scale = Math.min(1, maxWidth / Math.max(intrinsic.width, 1), maxHeight / Math.max(intrinsic.height, 1));
      const width = Math.max(24, Math.round(intrinsic.width * scale));
      const height = Math.max(24, Math.round(intrinsic.height * scale));
      const { x, y } = defaultInsertOrigin(width, height);
      return addRegionToPatch({
        kind: "image",
        content: {
          href,
          x,
          y,
          width,
          height,
          preserve_aspect_ratio: "xMidYMid meet",
        },
      });
    }

    async function insertSlot(slotId, value, label) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      await commitPatches([{ target: slotId, op: "add", value }], `${label} 삽입 완료`);
      restoreSelection([slotId]);
    }

    async function insertTextBox() {
      await insertSlot(uniqueInsertedSlotId("text"), textPayload(), "텍스트");
    }

    async function insertShape(def) {
      if (def.kind === "composite") {
        if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
        const { base, patches } = compositeShapePatches(def);
        await commitPatches(patches, `${def.label || "교구"} 삽입 완료`);
        restoreSelection(patches.length ? [patches[0].target] : []);
        return;
      }
      await insertSlot(uniqueInsertedSlotId(def.id), shapePayload(def), def.label || "도형");
    }

    function beginDrawShape(def) {
      if (!currentProblemId) throw new Error("문제를 먼저 여세요.");
      pendingDrawShape = def;
      clearSelection();
      hideShapeFormatMenu();
      document.getElementById("shapeGallery")?.classList.remove("open");
      setStatus(`${def.label || "도형"}: 캔버스에서 드래그하여 그리세요.`, true);
    }

    function formatPathPoint(point) {
      return canvasFormatPathPoint(point);
    }

    function curvePathFromPoints(start, end) {
      return canvasCurvePathFromPoints(start, end);
    }

    function freeformPathFromPoints(points) {
      return canvasFreeformPathFromPoints(points);
    }

    function drawPathFromState(state) {
      return canvasDrawPathFromState(state);
    }

    function createDrawState(svg, def, start, pointerId) {
      return canvasCreateDrawState(svg, def, start, pointerId);
    }

    function updateDrawStatePoint(state, point) {
      canvasUpdateDrawStatePoint(state, point);
    }

    function ensureDrawPreview(svg) {
      return canvasEnsureDrawPreview(svg);
    }

    function removeDrawPreview() {
      canvasRemoveDrawPreview();
    }

    function beginShapeDrawOnCanvas(svg, ev) {
      if (!pendingDrawShape || ev.button !== 0) return false;
      const start = getSvgPoint(svg, ev.clientX, ev.clientY);
      drawState = createDrawState(svg, pendingDrawShape, start, ev.pointerId);
      const preview = ensureDrawPreview(svg);
      preview.setAttribute("d", drawPathFromState(drawState));
      canvasCapturePointer(svg, ev.pointerId);
      ev.preventDefault();
      ev.stopPropagation();
      return true;
    }

    function updateShapeDraw(ev) {
      if (!drawState) return;
      const point = getSvgPoint(drawState.svg, ev.clientX, ev.clientY);
      updateDrawStatePoint(drawState, point);
      ensureDrawPreview(drawState.svg).setAttribute("d", drawPathFromState(drawState));
      ev.preventDefault();
    }

    async function endShapeDraw(ev) {
      if (!drawState) return;
      const local = drawState;
      drawState = null;
      pendingDrawShape = null;
      canvasReleasePointerCapture(local.svg, local.pointerId);
      removeDrawPreview();
      const end = local.current || local.start;
      if (Math.hypot(end.x - local.start.x, end.y - local.start.y) < 4 && (local.points || []).length < 2) {
        setStatus("그리기가 취소되었습니다.", false);
        return;
      }
      const d = drawPathFromState(local);
      const slotId = uniqueInsertedSlotId(local.def.id);
      const value = addRegionToPatch({
        kind: "path",
        content: {
          d,
          fill: "none",
          stroke: local.def.stroke || DEFAULT_SHAPE_STYLE.stroke,
          stroke_width: local.def.stroke_width || DEFAULT_SHAPE_STYLE.stroke_width,
        },
      });
      try {
        await insertSlot(slotId, value, local.def.label || "도형");
      } catch (e) {
        setStatus(String(e), false);
      }
    }

    async function insertImageFromFile(file) {
      await insertSlot(uniqueInsertedSlotId("image"), await imagePayloadFromFile(file), "그림");
    }

    function renderShapeGallery() {
      const gallery = document.getElementById("shapeGallery");
      if (!gallery) return;
      gallery.innerHTML = "";
      for (const category of SHAPE_CATEGORIES) {
        const title = document.createElement("div");
        title.className = "shape-category-title";
        title.textContent = category.title;
        gallery.appendChild(title);
        const grid = document.createElement("div");
        grid.className = "shape-grid";
        for (const shape of category.shapes) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "shape-choice";
          btn.title = shape.label;
          btn.setAttribute("aria-label", shape.label);
          btn.innerHTML = `<svg viewBox="0 0 22 20" aria-hidden="true" focusable="false">${shape.icon}</svg>`;
          btn.addEventListener("click", async () => {
            gallery.classList.remove("open");
            try {
              if (shape.draw_mode) beginDrawShape(shape);
              else await insertShape(shape);
            }
            catch (e) { setStatus(String(e), false); }
          });
          grid.appendChild(btn);
        }
        gallery.appendChild(grid);
      }
    }

    function toggleShapeGallery() {
      const gallery = document.getElementById("shapeGallery");
      if (!gallery) return;
      gallery.classList.toggle("open");
    }

    function toDslSlotId(svgElementId) {
      const ids = toDslSlotIds(svgElementId);
      return ids.length ? ids[0] : svgElementId;
    }

    function rendererSlotIds(svgElementId) {
      if (!svgElementId) return [];
      const refs = extractRendererSlotRefs().get(svgElementId) || [];
      const allIds = extractDslSlotIds();
      const seen = new Set();
      const out = [];
      for (const ref of refs) {
        if (!ref || seen.has(ref)) continue;
        if (allIds.has(ref) || ref.startsWith("slot.")) {
          seen.add(ref);
          out.push(ref);
        }
      }
      return out;
    }

    function toDslSlotIds(svgElementId) {
      if (!svgElementId) return [];
      const rendererIds = rendererSlotIds(svgElementId);
      if (rendererIds.length) return rendererIds;
      const allIds = extractDslSlotIds();
      const sourceIds = extractSourceDslSlotIds();
      if (sourceIds.has(svgElementId)) return [svgElementId];
      const parts = svgElementId.split(".");
      const sourceMatches = [];
      while (parts.length > 1) {
        parts.pop();
        const candidate = parts.join(".");
        if (sourceIds.has(candidate)) sourceMatches.push(candidate);
        const splitCandidates = Array.from(sourceIds)
          .filter((id) => id.startsWith(`${candidate}_`))
          .sort((a, b) => a.localeCompare(b, "ko"));
        if (splitCandidates.length > 0) return splitCandidates;
      }
      if (sourceMatches.length) return [sourceMatches[0]];

      if (allIds.has(svgElementId)) return [svgElementId];
      const layoutParts = svgElementId.split(".");
      while (layoutParts.length > 1) {
        layoutParts.pop();
        const candidate = layoutParts.join(".");
        if (allIds.has(candidate)) return [candidate];
        const splitCandidates = Array.from(allIds)
          .filter((id) => id.startsWith(`${candidate}_`))
          .sort((a, b) => a.localeCompare(b, "ko"));
        if (splitCandidates.length > 0) return splitCandidates;
      }
      return [];
    }

    function fallbackSlotIdFromSvgId(svgElementId) {
      if (!svgElementId) return "";
      const base = String(svgElementId)
        .replace(/\.(text|line|rect|path|polygon|circle)$/i, "")
        .replace(/\.(image)$/i, "")
        .replace(/__(hit|proxy)$/i, "");
      if (!base || base === "selectionOverlay") return "";
      if (!base.startsWith("slot.")) return "";
      return base;
    }

    function parseFractionPartId(svgElementId) {
      if (!svgElementId) return null;
      const base = svgElementId.replace(/\.(text|line|rect|path|polygon|circle|image)$/i, "");
      const m = base.match(/^(slot\..+)\.(whole|num|bar|den)$/);
      if (!m) return null;
      const dslIds = extractDslSlotIds();
      if (!dslIds.has(`${m[1]}.num`) || !dslIds.has(`${m[1]}.bar`) || !dslIds.has(`${m[1]}.den`)) return null;
      return { prefix: m[1], part: m[2] };
    }

    function isDraggableSlotElement(el) {
      if (!el) return false;
      if (el.classList && (el.classList.contains("selection-handle") || el.classList.contains("selection-bounds") || el.classList.contains("selection-line") || el.classList.contains("slot-hit-proxy"))) return false;
      const tag = el.tagName.toLowerCase();
      return tag === "text" || tag === "rect" || tag === "image" || tag === "circle" || tag === "line" || tag === "path" || tag === "polygon";
    }

    function draggableSlotElements(svg, prefix = null) {
      if (!svg) return [];
      const out = [];
      const nodes = svg.__draggableSlotElements || Array.from(svg.querySelectorAll("[id]")).filter((node) => isDraggableSlotElement(node) && slotIdFromElement(node));
      svg.__draggableSlotElements = nodes;
      for (const node of nodes) {
        const sid = slotIdFromElement(node);
        if (prefix && !sid.startsWith(prefix)) continue;
        out.push(node);
      }
      return out;
    }

    function matchesPickMode(el) {
      if (!el) return false;
      const tag = el.tagName.toLowerCase();
      if (pickMode === "all") return true;
      if (pickMode === "linepath") {
        if (!(tag === "line" || tag === "path")) return false;
        const id = el.getAttribute("id") || "";
        // Exclude fraction bars in line/path pick mode.
        if (/^slot\..+\.bar\.line$/i.test(id)) return false;
        return true;
      }
      if (pickMode === "text") return tag === "text";
      if (pickMode === "shape") return tag === "rect" || tag === "image" || tag === "circle" || tag === "polygon";
      return true;
    }

    function slotIdFromElement(el) {
      const rawId = el ? el.getAttribute("id") : "";
      const fracInfo = parseFractionPartId(rawId);
      if (fracInfo) return fracInfo.prefix;
      const ids = toDslSlotIds(rawId);
      return ids.length ? ids[0] : fallbackSlotIdFromSvgId(rawId);
    }

    function slotIdsFromElement(el) {
      const rawId = el ? el.getAttribute("id") : "";
      const fracInfo = parseFractionPartId(rawId);
      if (fracInfo) return [fracInfo.prefix];
      const ids = toDslSlotIds(rawId);
      return ids.length ? ids : (fallbackSlotIdFromSvgId(rawId) ? [fallbackSlotIdFromSvgId(rawId)] : []);
    }

    function arrowBaseFromSlotId(slotId) {
      if (!slotId || !slotId.includes("arrow")) return null;
      // e.g. slot.arrow_head, slot.arrow_body, slot.arrow.head -> slot.arrow
      const base = slotId
        .replace(/(?:_head\d*|_body\d*)$/i, "")
        .replace(/(?:\.head\d*|\.body\d*)$/i, "");
      if (base !== slotId) return base;
      // body id can be already base-shaped: slot.label.arrow
      if (/(?:^|[._])arrow$/i.test(slotId)) return slotId;
      return null;
    }

    function collectArrowGroupSlotIds(slotId) {
      const base = arrowBaseFromSlotId(slotId);
      if (!base) return [slotId];
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return [slotId];
      const out = new Set([slotId]);
      const nodes = draggableSlotElements(svg);
      for (const node of nodes) {
        const sid = slotIdFromElement(node);
        if (!sid) continue;
        if (sid === base || sid.startsWith(`${base}_head`) || sid.startsWith(`${base}_body`) || sid.startsWith(`${base}.head`) || sid.startsWith(`${base}.body`)) {
          out.add(sid);
        }
      }
      return Array.from(out);
    }

    function figureBaseFromSlotId(slotId) {
      if (!slotId) return null;
      const barModel = slotId.match(/^(slot\.figure\.bar_model_\d+\.bar\d+)\./);
      if (barModel) return barModel[1];
      const tickBar = slotId.match(/^(slot\.figure\.tick_bar_\d+\.row\d+)\./);
      if (tickBar) return tickBar[1];
      const m = slotId.match(/^(slot\.figure\.[^.]+)\./);
      return m ? m[1] : null;
    }

    function characterGroupInfoFromSlotId(slotId) {
      if (!slotId) return null;
      let m = slotId.match(/^slot\.([^.]+)\.person(?:\.|$)/);
      if (m) return { kind: "speaker", key: m[1], base: `slot.character.${m[1]}` };
      m = slotId.match(/^slot\.person_(left|mid|right)(?:\.|$)/);
      if (m) return { kind: "cardPerson", key: m[1], base: `slot.character.${m[1]}` };
      m = slotId.match(/^slot\.(?:name|card)_(left|mid|right)(?:$|_)/);
      if (m) return { kind: "cardPerson", key: m[1], base: `slot.character.${m[1]}` };
      return null;
    }

    function characterGroupBaseFromSlotId(slotId) {
      const info = characterGroupInfoFromSlotId(slotId);
      if (!info) return null;
      const group = collectCharacterGroupSlotIds(slotId);
      return group ? group.base : null;
    }

    function tableLayoutSlotIds() {
      const ids = new Set();
      const layoutText = document.getElementById("layoutView")?.value || "";
      if (!layoutText.trim()) return ids;
      try {
        const layout = JSON.parse(layoutText);
        for (const slot of Array.isArray(layout.slots) ? layout.slots : []) {
          const id = typeof slot?.id === "string" ? slot.id : "";
          const role = slot?.content?.style_role;
          if (tableSlotBase(id) || role === "table") ids.add(id);
        }
      } catch (_) {
        // Layout pane can be stale while a problem is loading.
      }
      return ids;
    }

    function layoutGroups() {
      const layoutText = document.getElementById("layoutView")?.value || "";
      if (layoutGroupCache.layoutText === layoutText && layoutGroupCache.groups && layoutGroupCache.byMember) return layoutGroupCache;
      const groups = [];
      const byMember = new Map();
      if (layoutText.trim()) {
        try {
          const layout = JSON.parse(layoutText);
          for (const group of Array.isArray(layout.groups) ? layout.groups : []) {
            const id = typeof group?.id === "string" ? group.id : "";
            const memberIds = Array.isArray(group?.member_ids) ? group.member_ids.filter((sid) => typeof sid === "string" && sid) : [];
            if (!id || memberIds.length < 2) continue;
            const entry = { id, memberIds };
            groups.push(entry);
            for (const sid of memberIds) {
              if (!byMember.has(sid)) byMember.set(sid, []);
              byMember.get(sid).push(entry);
            }
          }
        } catch (_) {
          // Layout pane can be stale while a problem is loading.
        }
      }
      layoutGroupCache = { layoutText, groups, byMember };
      return layoutGroupCache;
    }

    function layoutGroupBaseFromSlotId(slotId) {
      if (!slotId) return null;
      const matches = layoutGroups().byMember.get(slotId) || [];
      return matches.length ? matches[0].id : null;
    }

    function tableBaseFromSlotId(slotId) {
      if (!slotId) return null;
      const ids = tableLayoutSlotIds();
      const directBase = tableSlotBase(slotId);
      if (directBase) return directBase;
      if (ids.has(slotId)) return tableSlotBase(slotId);
      return null;
    }

    function graphPaperBaseFromSlotId(slotId) {
      return graphPaperSlotBase(slotId);
    }

    function paperFoldBaseFromSlotId(slotId) {
      if (!slotId) return null;
      const m = slotId.match(/^(slot\.[^.]+)\.(?:stage\d+|arrow\d+)(?:\.|$)/);
      return m ? m[1] : null;
    }

    function generatedHelperBaseFromSlotId(slotId) {
      if (!slotId) return null;
      if (slotId.startsWith("slot.grid.")) return "slot.grid";
      const point = slotId.match(/^(slot\.pt\.[^.]+)\./);
      if (point) return point[1];
      return null;
    }

    function measurementToolBaseFromSlotId(slotId) {
      if (!slotId) return null;
      const m = slotId.match(/^(slot\..+)\.(?:ruler|compass)(?:\.|$)/);
      return m ? m[1] : null;
    }

    function collectTableGroupSlotIds(slotId) {
      const base = tableBaseFromSlotId(slotId);
      if (!base) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const layoutIds = tableLayoutSlotIds();
      const out = [];
      for (const node of draggableSlotElements(svg)) {
        const sid = slotIdFromElement(node);
        if (!sid) continue;
        if ((sid.startsWith(`${base}.`) || (layoutIds.has(sid) && tableSlotBase(sid) === base)) && !out.includes(sid)) out.push(sid);
      }
      return out.length ? { base, slotIds: out, groupKind: "table" } : null;
    }

    function collectGraphPaperGroupSlotIds(slotId) {
      const base = graphPaperBaseFromSlotId(slotId);
      if (!base) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const out = [];
      for (const node of draggableSlotElements(svg, `${base}.`)) {
        const sid = slotIdFromElement(node);
        if (sid && sid.startsWith(`${base}.`) && !out.includes(sid)) out.push(sid);
      }
      return out.length > 1 ? { base, slotIds: out, groupKind: "graphPaper" } : null;
    }

    function selectableGroupBaseFromSlotId(slotId) {
      return layoutGroupBaseFromSlotId(slotId) || figureBaseFromSlotId(slotId) || characterGroupBaseFromSlotId(slotId) || tableBaseFromSlotId(slotId) || graphPaperBaseFromSlotId(slotId) || paperFoldBaseFromSlotId(slotId) || measurementToolBaseFromSlotId(slotId) || generatedHelperBaseFromSlotId(slotId);
    }

    function collectLayoutGroupSlotIds(slotId) {
      const matches = layoutGroups().byMember.get(slotId) || [];
      if (!matches.length) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const visibleIds = new Set();
      for (const node of draggableSlotElements(svg)) {
        const sid = slotIdFromElement(node);
        if (sid) visibleIds.add(sid);
      }
      for (const group of matches) {
        const slotIds = group.memberIds.filter((sid) => visibleIds.has(sid));
        if (slotIds.length > 1) return { base: group.id, slotIds, groupKind: "layout" };
      }
      return null;
    }

    function collectFigureGroupSlotIds(slotId) {
      const base = figureBaseFromSlotId(slotId);
      if (!base) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const out = [];
      for (const node of draggableSlotElements(svg, "slot.figure.")) {
        const sid = slotIdFromElement(node);
        if (sid && sid.startsWith(`${base}.`) && !out.includes(sid)) out.push(sid);
      }
      return out.length ? { base, slotIds: out, groupKind: "figure" } : null;
    }

    function collectCharacterGroupSlotIds(slotId) {
      const info = characterGroupInfoFromSlotId(slotId);
      if (!info) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const out = [];
      let hasPerson = false;
      for (const node of draggableSlotElements(svg)) {
        const sid = slotIdFromElement(node);
        if (!sid) continue;
        let include = false;
        if (info.kind === "speaker") {
          include = sid.startsWith(`slot.${info.key}.person.`);
          if (sid.startsWith(`slot.${info.key}.person.`)) hasPerson = true;
        } else if (info.kind === "cardPerson") {
          include = sid.startsWith(`slot.person_${info.key}.`) || sid === `slot.name_${info.key}` || sid.startsWith(`slot.name_${info.key}_`) || sid === `slot.card_${info.key}` || sid.startsWith(`slot.card_${info.key}_`);
          if (sid.startsWith(`slot.person_${info.key}.`)) hasPerson = true;
        }
        if (include && !out.includes(sid)) out.push(sid);
      }
      return hasPerson && out.length > 1 ? { base: info.base, slotIds: out, groupKind: "character" } : null;
    }

    function collectPaperFoldGroupSlotIds(slotId) {
      const base = paperFoldBaseFromSlotId(slotId);
      if (!base) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const out = [];
      for (const node of draggableSlotElements(svg, `${base}.`)) {
        const sid = slotIdFromElement(node);
        if (sid && sid.startsWith(`${base}.`) && !out.includes(sid)) out.push(sid);
      }
      return out.length > 1 ? { base, slotIds: out, groupKind: "paperFold" } : null;
    }

    function collectGeneratedHelperGroupSlotIds(slotId) {
      const base = generatedHelperBaseFromSlotId(slotId);
      if (!base) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const out = [];
      for (const node of draggableSlotElements(svg, `${base}.`)) {
        const sid = slotIdFromElement(node);
        if (sid && sid.startsWith(`${base}.`) && !out.includes(sid)) out.push(sid);
      }
      return out.length > 1 ? { base, slotIds: out, groupKind: "generated" } : null;
    }

    function collectMeasurementToolGroupSlotIds(slotId) {
      const base = measurementToolBaseFromSlotId(slotId);
      if (!base) return null;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const out = [];
      for (const node of draggableSlotElements(svg, `${base}.`)) {
        const sid = slotIdFromElement(node);
        if (!sid) continue;
        if ((sid.startsWith(`${base}.ruler.`) || sid.startsWith(`${base}.compass.`)) && !out.includes(sid)) out.push(sid);
      }
      return out.length > 1 ? { base, slotIds: out, groupKind: "measurement" } : null;
    }

    function collectSelectableGroupSlotIds(slotId) {
      return collectLayoutGroupSlotIds(slotId) || collectFigureGroupSlotIds(slotId) || collectCharacterGroupSlotIds(slotId) || collectTableGroupSlotIds(slotId) || collectGraphPaperGroupSlotIds(slotId) || collectPaperFoldGroupSlotIds(slotId) || collectMeasurementToolGroupSlotIds(slotId) || collectGeneratedHelperGroupSlotIds(slotId);
    }

    function elementsForSlotIds(slotIds) {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return [];
      const out = [];
      for (const node of draggableSlotElements(svg)) {
        const sid = slotIdFromElement(node);
        if (slotIds.includes(sid)) out.push(node);
      }
      return out;
    }

    function applyPickMode() {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return;
      const nodes = draggableSlotElements(svg);
      for (const node of nodes) {
        if (matchesPickMode(node)) node.classList.remove("pick-disabled");
        else node.classList.add("pick-disabled");
      }
      document.getElementById("pickAllBtn").classList.toggle("active", pickMode === "all");
      document.getElementById("pickLinePathBtn").classList.toggle("active", pickMode === "linepath");
      document.getElementById("pickTextBtn").classList.toggle("active", pickMode === "text");
      document.getElementById("pickShapeBtn").classList.toggle("active", pickMode === "shape");
    }

    function intersects(a, b) {
      return a.x <= b.x + b.width && a.x + a.width >= b.x && a.y <= b.y + b.height && a.y + a.height >= b.y;
    }

    function beginMarquee(svg, ev) {
      const container = document.getElementById("svgPreview");
      const box = document.getElementById("marqueeBox");
      marqueeState = canvasBeginMarqueeBox(svg, container, box, ev);
    }

    function updateMarquee(ev) {
      if (!marqueeState) return;
      const container = document.getElementById("svgPreview");
      const box = document.getElementById("marqueeBox");
      canvasUpdateMarqueeBox(container, box, marqueeState, ev);
    }

    function endMarquee(ev) {
      if (!marqueeState) return;
      const local = marqueeState;
      marqueeState = null;
      const box = document.getElementById("marqueeBox");
      const pickRect = canvasFinishMarqueeBox(box, local, ev);
      if (!pickRect) return;
      if (pickRect.width < 2 && pickRect.height < 2) {
        clearSelection();
        return;
      }

      clearSelection();
      const nodes = draggableSlotElements(local.svg);
      for (const node of nodes) {
        if (!matchesPickMode(node)) continue;
        let bb = null;
        try {
          bb = node.getBBox();
        } catch (_) {
          bb = null;
        }
        if (!bb || !intersects(pickRect, bb)) continue;
        const slotId = slotIdFromElement(node);
        if (!slotId) continue;
        setSelectedElement(node, slotId, true);
      }
      setStatus(`영역 선택: ${selectedSlots.size}개`, true);
    }

    function findDraggableSlotAncestor(node) {
      let cur = node;
      while (cur && cur.tagName && cur.tagName.toLowerCase() !== "svg") {
        if (cur.id && isDraggableSlotElement(cur) && slotIdsFromElement(cur).length) return cur;
        cur = cur.parentNode;
      }
      return null;
    }

    function isEmptySvgClickTarget(svg, target) {
      if (!(target instanceof SVGElement)) return false;
      if (target === svg) return true;
      if (target.classList.contains("canvas-guide")) return true;
      if (target.classList.contains("selection-bounds")) return true;
      if (target.classList.contains("selection-line")) return true;
      const id = target.getAttribute("id") || "";
      return id === "canvasGuide" || id === "selectionOverlay";
    }

    function inflateHitBox(box, pad) {
      return canvasInflateHitBox(box, pad);
    }

    function clamp(value, min, max) {
      return canvasClamp(value, min, max);
    }

    function pointToSegmentDistance(point, a, b) {
      return canvasPointToSegmentDistance(point, a, b);
    }

    function pointToBoxDistance(point, box) {
      return canvasPointToBoxDistance(point, box);
    }

    function pathAnchorPoints(d) {
      const tokens = pathTokens(d);
      const points = [];
      let i = 0;
      let cmd = null;
      const isCommand = (token) => /^[a-zA-Z]$/.test(token);
      const num = (token) => Number(token);
      while (i < tokens.length) {
        if (isCommand(tokens[i])) {
          cmd = tokens[i].toUpperCase();
          i += 1;
          if (cmd === "Z") continue;
        }
        if (!cmd) break;
        const count = PATH_PARAM_COUNTS[cmd];
        if (!count || i + count > tokens.length) break;
        const vals = tokens.slice(i, i + count).map(num);
        if (vals.some((v) => !Number.isFinite(v))) break;
        if (cmd === "M" || cmd === "L" || cmd === "T") points.push({ x: vals[0], y: vals[1] });
        else if (cmd === "H" && points.length) points.push({ x: vals[0], y: points[points.length - 1].y });
        else if (cmd === "V" && points.length) points.push({ x: points[points.length - 1].x, y: vals[0] });
        else if (cmd === "C") points.push({ x: vals[4], y: vals[5] });
        else if (cmd === "S" || cmd === "Q") points.push({ x: vals[vals.length - 2], y: vals[vals.length - 1] });
        else if (cmd === "A") points.push({ x: vals[5], y: vals[6] });
        i += count;
      }
      return points;
    }

    function pointToElementDistance(node, point, box) {
      const tag = node.tagName.toLowerCase();
      if (node.getAttribute("transform")) return pointToBoxDistance(point, box);
      if (tag === "text") {
        return pointToBoxDistance(point, box);
      }
      if (tag === "line") {
        return pointToSegmentDistance(
          point,
          { x: Number(node.getAttribute("x1") || 0), y: Number(node.getAttribute("y1") || 0) },
          { x: Number(node.getAttribute("x2") || 0), y: Number(node.getAttribute("y2") || 0) }
        );
      }
      if (tag === "circle") {
        const cx = Number(node.getAttribute("cx") || 0);
        const cy = Number(node.getAttribute("cy") || 0);
        const r = Math.max(0, Number(node.getAttribute("r") || 0));
        const fill = String(node.getAttribute("fill") || "").toLowerCase();
        const centerDistance = Math.hypot(point.x - cx, point.y - cy);
        return fill && fill !== "none" ? Math.max(0, centerDistance - r) : Math.abs(centerDistance - r);
      }
      if (tag === "path" || tag === "polygon") {
        const points = tag === "polygon"
          ? parsePolygonPoints(node.getAttribute("points") || "").map(([x, y]) => ({ x, y }))
          : pathAnchorPoints(node.getAttribute("d") || "");
        if (points.length >= 2) {
          let best = Infinity;
          for (let i = 1; i < points.length; i += 1) best = Math.min(best, pointToSegmentDistance(point, points[i - 1], points[i]));
          return best;
        }
      }
      return pointToBoxDistance(point, box);
    }

    function tableCellPositionFromSlotId(slotId) {
      const m = String(slotId || "").match(/^(slot\.table(?:_\d+)?)\.r(\d+)c(\d+)$/);
      if (!m) return null;
      return { base: m[1], row: Number(m[2]), col: Number(m[3]) };
    }

    function uniqueSortedNumbers(values) {
      const sorted = values
        .filter((value) => Number.isFinite(value))
        .sort((a, b) => a - b);
      const out = [];
      for (const value of sorted) {
        if (!out.length || Math.abs(out[out.length - 1] - value) > 0.01) out.push(value);
      }
      return out;
    }

    function escapedRegExp(value) {
      return String(value || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }

    function tableCellHitBox(node, svg) {
      const cell = tableCellPositionFromSlotId(slotIdFromElement(node));
      if (!cell || !svg) return null;
      const nodes = draggableSlotElements(svg, `${cell.base}.`);
      const outer = nodes.find((el) => slotIdFromElement(el) === `${cell.base}.outer` && el.tagName.toLowerCase() === "rect");
      if (!outer) return null;
      const outerValue = readSlotPatchValue(outer);
      if (!outerValue) return null;
      const left = Number(outerValue.x);
      const top = Number(outerValue.y);
      const right = left + Number(outerValue.width);
      const bottom = top + Number(outerValue.height);
      if (![left, top, right, bottom].every(Number.isFinite)) return null;

      const xs = [left, right];
      const ys = [top, bottom];
      const vPattern = new RegExp(`^${escapedRegExp(cell.base)}\\.v\\d+$`);
      const hPattern = new RegExp(`^${escapedRegExp(cell.base)}\\.h\\d+$`);
      for (const el of nodes) {
        const sid = slotIdFromElement(el);
        if (!sid || el.tagName.toLowerCase() !== "line") continue;
        const value = readSlotPatchValue(el);
        if (!value) continue;
        if (vPattern.test(sid)) {
          xs.push(Number(value.x1));
        } else if (hPattern.test(sid)) {
          ys.push(Number(value.y1));
        }
      }

      const colBounds = uniqueSortedNumbers(xs);
      const rowBounds = uniqueSortedNumbers(ys);
      if (cell.col < 1 || cell.col >= colBounds.length || cell.row < 1 || cell.row >= rowBounds.length) return null;
      const x = colBounds[cell.col - 1];
      const y = rowBounds[cell.row - 1];
      return {
        x,
        y,
        width: Math.max(1, colBounds[cell.col] - x),
        height: Math.max(1, rowBounds[cell.row] - y),
      };
    }

    function textHitBox(node, svg = null) {
      if (node.getAttribute("data-slot-kind") === "text_box") {
        const x = Number(node.getAttribute("data-box-x") || node.getAttribute("x") || 0);
        const y = Number(node.getAttribute("data-box-y") || node.getAttribute("y") || 0);
        const width = Number(node.getAttribute("data-box-width") || 0);
        const height = Number(node.getAttribute("data-box-height") || 0);
        return width > 0 && height > 0 ? { x, y, width, height } : null;
      }

      const text = node.textContent || "";
      const fontSize = Number(node.getAttribute("font-size") || node.getAttribute("font_size") || 28);
      const x = Number(node.getAttribute("x") || 0);
      const y = Number(node.getAttribute("y") || 0);
      const lineCount = Math.max(1, text.split(/\n/).length);
      const maxLineLength = Math.max(1, ...text.split(/\n/).map((line) => line.length));
      const estimated = {
        x: x - 6,
        y: y - fontSize,
        width: Math.max(fontSize * 0.8, maxLineLength * fontSize * 0.62) + 12,
        height: lineCount * fontSize * 1.25 + 8,
      };

      let box = null;
      try {
        box = svg ? visualSvgBox(node, svg) : node.getBBox();
      } catch (_) {
        box = null;
      }
      if (!box || box.width <= 0 || box.height <= 0) return estimated;

      const padded = inflateHitBox(box, Math.max(6, fontSize * 0.25));
      const minWidth = Math.max(fontSize * 1.35, estimated.width);
      const minHeight = Math.max(fontSize * 1.35, estimated.height);
      const width = Math.max(padded.width, minWidth);
      const height = Math.max(padded.height, minHeight);
      const centerX = padded.x + padded.width / 2;
      const centerY = padded.y + padded.height / 2;
      return {
        x: centerX - width / 2,
        y: centerY - height / 2,
        width,
        height,
      };
    }

    function elementHitBox(node, svg = null) {
      const tag = node.tagName.toLowerCase();
      if (tag === "rect" || tag === "image") {
        const x = Number(node.getAttribute("x") || 0);
        const y = Number(node.getAttribute("y") || 0);
        const width = Number(node.getAttribute("width") || 0);
        const height = Number(node.getAttribute("height") || 0);
        return width > 0 && height > 0 ? { x, y, width, height } : null;
      }
      if (tag === "text") {
        const cellBox = tableCellHitBox(node, svg);
        return cellBox || textHitBox(node, svg);
      }
      if (tag === "line") {
        if (svg && node.getAttribute("transform")) {
          return inflateHitBox(visualSvgBox(node, svg), 8);
        }
        const x1 = Number(node.getAttribute("x1") || 0);
        const y1 = Number(node.getAttribute("y1") || 0);
        const x2 = Number(node.getAttribute("x2") || 0);
        const y2 = Number(node.getAttribute("y2") || 0);
        const pad = Math.max(8, Number(node.getAttribute("stroke-width") || 1) * 3);
        return {
          x: Math.min(x1, x2) - pad,
          y: Math.min(y1, y2) - pad,
          width: Math.abs(x2 - x1) + pad * 2,
          height: Math.abs(y2 - y1) + pad * 2,
        };
      }
      if (tag === "circle") {
        if (svg && node.getAttribute("transform")) {
          return inflateHitBox(visualSvgBox(node, svg), 8);
        }
        const cx = Number(node.getAttribute("cx") || 0);
        const cy = Number(node.getAttribute("cy") || 0);
        const r = Number(node.getAttribute("r") || 0);
        if (!Number.isFinite(cx) || !Number.isFinite(cy) || !Number.isFinite(r)) return null;
        const pad = Math.max(8, Number(node.getAttribute("stroke-width") || 1) * 3);
        const rr = Math.max(0, r) + pad;
        return { x: cx - rr, y: cy - rr, width: rr * 2, height: rr * 2 };
      }
      try {
        const bb = node.getBBox();
        if (!bb) return null;
        if (tag === "path" || tag === "polygon") {
          if (svg && node.getAttribute("transform")) {
            return inflateHitBox(visualSvgBox(node, svg), 8);
          }
          const pad = Math.max(8, Number(node.getAttribute("stroke-width") || 1) * 3);
          return { x: bb.x - pad, y: bb.y - pad, width: bb.width + pad * 2, height: bb.height + pad * 2 };
        }
        return bb;
      } catch (_) {
        return null;
      }
    }

    function pickPriority(node) {
      const tag = node.tagName.toLowerCase();
      if (tag === "text") return 0;
      if (tag === "line" || tag === "path") return 0;
      if (tag === "circle") return 1;
      if (tag === "polygon") return 1;
      if (tag === "image") return 2;
      if (tag === "rect") return 3;
      return 4;
    }

    function matchingSlotElementAtPoint(svg, clientX, clientY) {
      const seen = new Set();
      for (const node of document.elementsFromPoint(clientX, clientY)) {
        if (!(node instanceof SVGElement) || !svg.contains(node)) continue;
        const slotTarget = node.__slotProxyTarget || findDraggableSlotAncestor(node);
        if (!slotTarget || seen.has(slotTarget)) continue;
        seen.add(slotTarget);
        if (matchesPickMode(slotTarget)) return slotTarget;
      }
      const point = getSvgPoint(svg, clientX, clientY);
      const nodes = draggableSlotElements(svg);
      const candidates = [];
      for (let i = nodes.length - 1; i >= 0; i -= 1) {
        const node = nodes[i];
        if (!matchesPickMode(node)) continue;
        const bb = elementHitBox(node, svg);
        if (!bb) continue;
        if (point.x >= bb.x && point.x <= bb.x + bb.width && point.y >= bb.y && point.y <= bb.y + bb.height) {
          const area = Math.max(0, bb.width) * Math.max(0, bb.height);
          const distance = pointToElementDistance(node, point, bb);
          candidates.push({ node, priority: pickPriority(node), distance, area, z: i });
        }
      }
      if (candidates.length) {
        candidates.sort((a, b) => a.distance - b.distance || a.priority - b.priority || a.area - b.area || b.z - a.z);
        return candidates[0].node;
      }
      return null;
    }

    function matchingTextSlotElementAtPoint(svg, clientX, clientY) {
      const point = getSvgPoint(svg, clientX, clientY);
      const nodes = draggableSlotElements(svg);
      const candidates = [];
      for (let i = nodes.length - 1; i >= 0; i -= 1) {
        const node = nodes[i];
        if (node.tagName.toLowerCase() !== "text") continue;
        if (!matchesPickMode(node)) continue;
        const bb = elementHitBox(node, svg);
        if (!bb) continue;
        if (point.x >= bb.x && point.x <= bb.x + bb.width && point.y >= bb.y && point.y <= bb.y + bb.height) {
          const area = Math.max(0, bb.width) * Math.max(0, bb.height);
          const distance = pointToElementDistance(node, point, bb);
          candidates.push({ node, distance, area, z: i });
        }
      }
      if (candidates.length) {
        candidates.sort((a, b) => a.distance - b.distance || a.area - b.area || b.z - a.z);
        return candidates[0].node;
      }
      return null;
    }

    function readSlotPatchValue(el) {
      const tag = el.tagName.toLowerCase();
      const transform = el.getAttribute("transform") || "";
      const withTransform = (value) => {
        if (transform) value.transform = transform;
        return value;
      };
      const styleAttrs = (names) => {
        const out = {};
        for (const name of names) {
          const attrName = name.replace(/_/g, "-");
          const raw = el.getAttribute(attrName) || el.style?.getPropertyValue(attrName) || "";
          if (raw && raw !== "none") out[name] = name === "stroke_width" ? Number(raw) : raw;
        }
        return out;
      };
      const readText = () => {
        const rawText = el.getAttribute("data-raw-text");
        if (rawText !== null) return rawText;
        const tspans = Array.from(el.querySelectorAll("tspan"));
        if (tspans.length) return tspans.map((node) => node.textContent || "").join("\n");
        return el.textContent || "";
      };
      if (tag === "text") {
        if (el.getAttribute("data-slot-kind") === "text_box") {
          return withTransform({
            text: readText(),
            x: Number(el.getAttribute("data-box-x") || 0),
            y: Number(el.getAttribute("data-box-y") || 0),
            width: Number(el.getAttribute("data-box-width") || 0),
            height: Number(el.getAttribute("data-box-height") || 0),
            font_size: Number(el.getAttribute("font-size") || el.getAttribute("font_size") || 0) || undefined,
            fill: el.getAttribute("fill") || undefined,
          });
        }
        return withTransform({
          text: readText(),
          x: Number(el.getAttribute("x") || 0),
          y: Number(el.getAttribute("y") || 0),
          font_size: Number(el.getAttribute("font-size") || el.getAttribute("font_size") || 0) || undefined,
          max_width: Number(el.getAttribute("max_width") || el.getAttribute("max-width") || 0) || undefined,
          anchor: el.getAttribute("text-anchor") || el.getAttribute("anchor") || undefined,
          ...styleAttrs(["fill"]),
        });
      }
      if (tag === "rect") {
        return withTransform({
          x: Number(el.getAttribute("x") || 0),
          y: Number(el.getAttribute("y") || 0),
          width: Number(el.getAttribute("width") || 0),
          height: Number(el.getAttribute("height") || 0),
          rx: Number(el.getAttribute("rx") || 0) || undefined,
          ry: Number(el.getAttribute("ry") || 0) || undefined,
          ...styleAttrs(["fill", "stroke", "stroke_width", "stroke_dasharray"]),
        });
      }
      if (tag === "image") {
        return withTransform({
          href: el.getAttribute("href") || el.getAttribute("xlink:href") || "",
          x: Number(el.getAttribute("x") || 0),
          y: Number(el.getAttribute("y") || 0),
          width: Number(el.getAttribute("width") || 0),
          height: Number(el.getAttribute("height") || 0),
          preserve_aspect_ratio: el.getAttribute("preserveAspectRatio") || undefined,
        });
      }
      if (tag === "circle") {
        return withTransform({
          cx: Number(el.getAttribute("cx") || 0),
          cy: Number(el.getAttribute("cy") || 0),
          r: Number(el.getAttribute("r") || 0),
          ...styleAttrs(["fill", "stroke", "stroke_width", "stroke_dasharray"]),
        });
      }
      if (tag === "line") {
        return withTransform({
          x1: Number(el.getAttribute("x1") || 0),
          y1: Number(el.getAttribute("y1") || 0),
          x2: Number(el.getAttribute("x2") || 0),
          y2: Number(el.getAttribute("y2") || 0),
          ...styleAttrs(["stroke", "stroke_width", "stroke_dasharray"]),
        });
      }
      if (tag === "path") {
        return withTransform({ d: el.getAttribute("d") || "", ...styleAttrs(["fill", "stroke", "stroke_width", "stroke_dasharray"]) });
      }
      if (tag === "polygon") {
        const pts = parsePolygonPoints(el.getAttribute("points") || "");
        return withTransform({ points: pts, ...styleAttrs(["fill", "stroke", "stroke_width", "stroke_dasharray"]) });
      }
      return null;
    }

    function hideShapeFormatMenu() {
      document.getElementById("shapeFormatMenu")?.classList.remove("open");
    }

    function positionShapeFormatMenu(ev) {
      const menu = document.getElementById("shapeFormatMenu");
      if (!menu) return false;
      menu.classList.add("open");
      const margin = 8;
      const width = menu.offsetWidth || 226;
      const height = menu.offsetHeight || 150;
      const left = Math.min(Math.max(margin, ev.clientX), window.innerWidth - width - margin);
      const top = Math.min(Math.max(margin, ev.clientY), window.innerHeight - height - margin);
      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
      ev.preventDefault();
      ev.stopPropagation();
      return true;
    }

    function selectedShapeFormatItem() {
      if (selectedSlots.size !== 1) return null;
      const item = Array.from(selectedSlots.values())[0];
      if (!item || item.isCanvas || item.isFraction || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup || item.isCharacterGroup || item.isLayoutGroup) return null;
      if (!item.el) return null;
      const tag = item.el.tagName.toLowerCase();
      if (!["rect", "circle", "line", "path", "polygon"].includes(tag)) return null;
      return item;
    }

    function validHexColor(value) {
      return /^#[0-9a-fA-F]{6}$/.test(String(value || ""));
    }

    function openShapeFormatMenu(ev, el) {
      const rawId = el.getAttribute("id");
      const slotIds = slotIdsFromElement(el);
      const slotId = slotIds[0] || fallbackSlotIdFromSvgId(rawId);
      if (!slotId) return false;
      setSelectedElement(el, slotId, false);
      const tableItem = selectedSlots.size === 1 ? Array.from(selectedSlots.values())[0] : null;
      if (tableItem && tableItem.isTableGroup) {
        const svg = document.getElementById("svgPreview").querySelector("svg");
        const cell = tableCellAtPoint(svg, tableItem, ev.clientX, ev.clientY);
        if (cell) {
          if (!selectedTableCells.some((selected) => sameTableCell(selected, cell))) {
            setSelectedTableCell(tableItem, cell, false);
          }
          updateSelectionHandles();
          const fillEntry = tableCellFillForCell(tableItem, cell);
          const value = fillEntry ? readSlotPatchValue(fillEntry.el) || {} : {};
          const fillInput = document.getElementById("shapeFillColorInput");
          if (fillInput && validHexColor(value.fill)) fillInput.value = value.fill;
          return positionShapeFormatMenu(ev);
        }
      }
      selectedTableCells = [];
      const item = selectedShapeFormatItem();
      if (!item) return false;
      item.slotIds = slotIds.length ? slotIds : [slotId];
      updateSelectionHandles();
      updateTextEditControls();

      const value = readSlotPatchValue(item.el) || {};
      const fillInput = document.getElementById("shapeFillColorInput");
      if (fillInput && validHexColor(value.fill)) fillInput.value = value.fill;
      const strokeInput = document.getElementById("shapeStrokeColorInput");
      if (strokeInput && validHexColor(value.stroke)) strokeInput.value = value.stroke;

      return positionShapeFormatMenu(ev);
    }

    async function applyShapeFormatPatch(stylePatch, label) {
      const item = selectedShapeFormatItem();
      if (!item) throw new Error("도형을 먼저 선택하세요.");
      const value = { ...(readSlotPatchValue(item.el) || {}), ...stylePatch };
      const before = [{ slotId: item.slotId, value: readSlotPatchValue(item.el) || {} }];
      applyPatchValueToElement(item.el, value);
      updateSelectionHandles();
      const targets = item.slotIds || [item.slotId];
      await commitPatches(targets.map((target) => ({ target, op: "update", value })), `${label} 적용 완료`);
      const after = [{ slotId: item.slotId, value: JSON.parse(JSON.stringify(value)) }];
      if (!historyBusy) pushHistory(before, after, label);
    }

    async function applyShapeFill(fill) {
      if (selectedTableFillContextItem()) {
        await applyTableCellFill(fill);
        return;
      }
      const item = selectedShapeFormatItem();
      if (!item) throw new Error("도형을 먼저 선택하세요.");
      if (item.el.tagName.toLowerCase() === "line") throw new Error("선에는 채우기를 적용할 수 없습니다.");
      await applyShapeFormatPatch({ fill }, "채우기");
    }

    async function applyShapeStroke(stroke) {
      const item = selectedShapeFormatItem();
      if (!item) throw new Error("도형 또는 선을 먼저 선택하세요.");
      const current = readSlotPatchValue(item.el) || {};
      const strokeWidth = Number(current.stroke_width);
      await applyShapeFormatPatch({
        stroke,
        stroke_width: Number.isFinite(strokeWidth) && strokeWidth > 0 ? strokeWidth : DEFAULT_SHAPE_STYLE.stroke_width,
      }, "선 색");
    }

    function selectedStrokeOrDefault() {
      const item = selectedShapeFormatItem();
      const current = item ? (readSlotPatchValue(item.el) || {}) : {};
      return validHexColor(current.stroke) ? current.stroke : DEFAULT_SHAPE_STYLE.stroke;
    }

    function renderShapeFormatSwatches() {
      const fillWrap = document.getElementById("shapeFillSwatches");
      if (!fillWrap) return;
      fillWrap.innerHTML = "";
      for (const color of SHAPE_FILL_SWATCHES) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "shape-swatch";
        if (color === "none") {
          btn.classList.add("transparent");
          btn.title = "채우기 없음";
        } else {
          btn.style.background = color;
          btn.title = color;
        }
        btn.addEventListener("click", async () => {
          try { await applyShapeFill(color); hideShapeFormatMenu(); }
          catch (e) { setStatus(String(e), false); }
        });
        fillWrap.appendChild(btn);
      }

      const strokeWrap = document.getElementById("shapeStrokeSwatches");
      if (!strokeWrap) return;
      strokeWrap.innerHTML = "";
      for (const color of SHAPE_FILL_SWATCHES) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "shape-swatch";
        if (color === "none") {
          btn.classList.add("transparent");
          btn.title = "선 없음";
        } else {
          btn.style.background = color;
          btn.title = color;
        }
        btn.addEventListener("click", async () => {
          try {
            if (color === "none") await applyShapeFormatPatch({ stroke: "none", stroke_width: 0, stroke_dasharray: "" }, "선 없음");
            else await applyShapeStroke(color);
            hideShapeFormatMenu();
          } catch (e) { setStatus(String(e), false); }
        });
        strokeWrap.appendChild(btn);
      }
    }

    function parseRotateTransform(transform) {
      const m = String(transform || "").match(/rotate\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)/);
      if (!m) return { angle: 0, cx: null, cy: null };
      return { angle: Number(m[1]) || 0, cx: Number(m[2]), cy: Number(m[3]) };
    }

    function pointInRotatedFrame(point, rotation) {
      return canvasPointInRotatedFrame(point, rotation);
    }

    function rotateTransform(angle, cx, cy) {
      const roundedAngle = Math.abs(angle) < 0.0001 ? 0 : Number(angle.toFixed(2));
      const rx = Number(cx.toFixed(2));
      const ry = Number(cy.toFixed(2));
      return `rotate(${roundedAngle} ${rx} ${ry})`;
    }

    function shiftRotateTransform(transform, dx, dy, useSnap = true) {
      if (!transform) return transform;
      const snap = (v) => (useSnap ? snapValue(v) : v);
      return String(transform).replace(
        /rotate\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)/g,
        (_, angle, cx, cy) => rotateTransform(Number(angle) || 0, snap(Number(cx) + dx), snap(Number(cy) + dy))
      );
    }

    function shiftElementRotateCenter(el, dx, dy, useSnap = true) {
      const transform = el.getAttribute("transform") || "";
      if (!transform || !/rotate\(/.test(transform)) return null;
      const shifted = shiftRotateTransform(transform, dx, dy, useSnap);
      el.setAttribute("transform", shifted);
      return shifted;
    }

    function shiftedStartRotateTransform(startValue, dx, dy, useSnap = true) {
      const transform = startValue && startValue.transform;
      if (!transform || !/rotate\(/.test(transform)) return null;
      return shiftRotateTransform(transform, dx, dy, useSnap);
    }

    function rotationValueFromPointer(startValue, startBox, startPoint, pointerPoint) {
      const cx = startBox.x + startBox.width / 2;
      const cy = startBox.y + startBox.height / 2;
      const a0 = Math.atan2(startPoint.y - cy, startPoint.x - cx);
      const a1 = Math.atan2(pointerPoint.y - cy, pointerPoint.x - cx);
      const prior = parseRotateTransform(startValue && startValue.transform);
      let angle = prior.angle + ((a1 - a0) * 180) / Math.PI;
      if (snapEnabled) angle = Math.round(angle / 5) * 5;
      return { ...startValue, transform: rotateTransform(angle, cx, cy) };
    }

    function rotationValuesForGroup(startEntries, startBox, startPoint, pointerPoint) {
      return (startEntries || []).map((entry) => ({
        ...entry,
        value: rotationValueFromPointer(entry.value, startBox, startPoint, pointerPoint),
      }));
    }

    function pathTokens(d) {
      return (d || "").match(/[a-zA-Z]|-?\d*\.?\d+(?:e[-+]?\d+)?/g) || [];
    }

    const PATH_PARAM_COUNTS = { M: 2, L: 2, T: 2, H: 1, V: 1, C: 6, S: 4, Q: 4, A: 7 };

    function shiftPathD(d, dx, dy, useSnap = true) {
      const snap = (v) => (useSnap ? snapValue(v) : v);
      return canvasShiftPathD(d, dx, dy, snap);
    }

    function scalePathD(d, startBox, nextBox, useSnap = true) {
      const snap = (v) => (useSnap ? snapValue(v) : v);
      return canvasScalePathD(d, startBox, nextBox, snap);
    }

    function parsePolygonPoints(raw) {
      return canvasParsePolygonPoints(raw);
    }

    function formatPolygonPoints(points) {
      return canvasFormatPolygonPoints(points);
    }

    function editablePathFromD(d) {
      return canvasEditablePathFromD(d);
    }

    function clearPathPointHandles(layer) {
      canvasClearPathPointHandles(layer);
    }

    function pathPointPatchFromHandle(startValue, handle, point) {
      const snap = (v) => snapEnabled ? snapValue(v) : v;
      return canvasPathPointPatchFromHandle(startValue, handle, point, snap);
    }

    function textBoxTextX(el, x, width) {
      const anchor = el.getAttribute("text-anchor") || "";
      if (anchor === "middle") return x + width / 2;
      if (anchor === "end") return x + width;
      return x;
    }

    function moveTextBoxTspans(el, textX, dy = 0, snap = (v) => v) {
      for (const tspan of el.querySelectorAll("tspan")) {
        tspan.setAttribute("x", String(textX));
        tspan.setAttribute("y", String(snap(Number(tspan.getAttribute("y") || 0) + dy)));
      }
    }

    function syncSlotHitProxies(el) {
      canvasSyncSlotHitProxies(el);
    }

    function applyElementDelta(el, dx, dy, useSnap = true) {
      const snap = (v) => (useSnap ? snapValue(v) : v);
      const tag = el.tagName.toLowerCase();
      if (tag === "text" && el.getAttribute("data-slot-kind") === "text_box") {
        const nx = snap(Number(el.getAttribute("data-box-x") || 0) + dx);
        const ny = snap(Number(el.getAttribute("data-box-y") || 0) + dy);
        const textX = snap(Number(el.getAttribute("x") || 0) + dx);
        const textY = snap(Number(el.getAttribute("y") || 0) + dy);
        el.setAttribute("data-box-x", String(nx));
        el.setAttribute("data-box-y", String(ny));
        el.setAttribute("x", String(textX));
        el.setAttribute("y", String(textY));
        const transform = shiftElementRotateCenter(el, dx, dy, useSnap);
        moveTextBoxTspans(el, textX, dy, snap);
        syncSlotHitProxies(el);
        const out = { x: nx, y: ny };
        if (transform) out.transform = transform;
        return out;
      }
      if (tag === "text" || tag === "rect" || tag === "image") {
        const nx = snap(Number(el.getAttribute("x") || 0) + dx);
        const ny = snap(Number(el.getAttribute("y") || 0) + dy);
        el.setAttribute("x", String(nx));
        el.setAttribute("y", String(ny));
        const transform = shiftElementRotateCenter(el, dx, dy, useSnap);
        syncSlotHitProxies(el);
        const out = { x: nx, y: ny };
        if (transform) out.transform = transform;
        return out;
      }
      if (tag === "circle") {
        const ncx = snap(Number(el.getAttribute("cx") || 0) + dx);
        const ncy = snap(Number(el.getAttribute("cy") || 0) + dy);
        el.setAttribute("cx", String(ncx));
        el.setAttribute("cy", String(ncy));
        const transform = shiftElementRotateCenter(el, dx, dy, useSnap);
        syncSlotHitProxies(el);
        const out = { cx: ncx, cy: ncy };
        if (transform) out.transform = transform;
        return out;
      }
      if (tag === "line") {
        const nx1 = snap(Number(el.getAttribute("x1") || 0) + dx);
        const ny1 = snap(Number(el.getAttribute("y1") || 0) + dy);
        const nx2 = snap(Number(el.getAttribute("x2") || 0) + dx);
        const ny2 = snap(Number(el.getAttribute("y2") || 0) + dy);
        el.setAttribute("x1", String(nx1));
        el.setAttribute("y1", String(ny1));
        el.setAttribute("x2", String(nx2));
        el.setAttribute("y2", String(ny2));
        const transform = shiftElementRotateCenter(el, dx, dy, useSnap);
        syncSlotHitProxies(el);
        const out = { x1: nx1, y1: ny1, x2: nx2, y2: ny2 };
        if (transform) out.transform = transform;
        return out;
      }
      if (tag === "path") {
        const nd = shiftPathD(el.getAttribute("d") || "", dx, dy, useSnap);
        el.setAttribute("d", nd);
        const transform = shiftElementRotateCenter(el, dx, dy, useSnap);
        syncSlotHitProxies(el);
        const out = { d: nd };
        if (transform) out.transform = transform;
        return out;
      }
      if (tag === "polygon") {
        const pts = parsePolygonPoints(el.getAttribute("points") || "");
        const moved = pts.map(([x, y]) => {
          const nx = useSnap ? snapValue(x + dx) : x + dx;
          const ny = useSnap ? snapValue(y + dy) : y + dy;
          return [nx, ny];
        });
        el.setAttribute("points", formatPolygonPoints(moved));
        const transform = shiftElementRotateCenter(el, dx, dy, useSnap);
        syncSlotHitProxies(el);
        const out = { points: moved };
        if (transform) out.transform = transform;
        return out;
      }
      return null;
    }

    function applyDragDeltaToSelection(dx, dy) {
      let lastValue = null;
      for (const item of selectedSlots.values()) {
        if (item.isFraction || item.isCharacterGroup || item.isLayoutGroup || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup) {
          for (const node of item.elements || []) lastValue = applyElementDelta(node, dx, dy, false);
        } else {
          lastValue = applyElementDelta(item.el, dx, dy, false);
        }
      }
      return lastValue;
    }

    function markDragMoveApplied(dx, dy) {
      if (!dragState) return false;
      dragState.moved = true;
      if (!translateSelectionOverlay(dx, dy)) updateSelectionHandles();
      const now = Date.now();
      if (now - lastDragStatusAt > 90) {
        lastDragStatusAt = now;
        setStatus(`드래그 중: ${selectedSlots.size}개 선택${snapEnabled ? " (snap 5px)" : ""}`, true);
      }
      return true;
    }

    function snapAndApplyMoveFix(elements, dx, dy) {
      const snappedMove = snapPatchValue({ move_dx: dx, move_dy: dy });
      const fixDx = snappedMove.move_dx - dx;
      const fixDy = snappedMove.move_dy - dy;
      if (fixDx !== 0 || fixDy !== 0) {
        for (const node of elements || []) applyElementDelta(node, fixDx, fixDy, false);
      }
      return snappedMove;
    }

    function appendMovedElementPatch(node, local, patches, after) {
      const slotId = slotIdFromElement(node);
      const current = readSlotPatchValue(node);
      const beforeValue = local.beforeMap.get(slotId);
      const value = movedPatchValueFromBefore(beforeValue, current);
      if (!slotId || !value) return false;
      applyPatchValueToElement(node, value);
      patches.push({ target: slotId, op: "update", value });
      after.push({ slotId, value: JSON.parse(JSON.stringify(value)) });
      return true;
    }

    function appendMovePatch(slotId, value, patches, after) {
      patches.push({ target: slotId, op: "update", value });
      after.push({ slotId, value });
    }

    function appendMultiTargetPatch(slotIds, value, patches, after) {
      for (const id of slotIds) {
        after.push({ slotId: id, value: JSON.parse(JSON.stringify(value)) });
        patches.push({ target: id, op: "update", value });
      }
    }

    function buildDragEndPatchSet(local) {
      const after = [];
      const patches = [];
      for (const item of selectedSlots.values()) {
        if (item.isFraction) {
          const startAnchor = local.fractionStartAnchors ? local.fractionStartAnchors.get(item.slotId) : null;
          const moved = fractionVisualDelta(item.slotId, startAnchor);
          const snappedMove = snapAndApplyMoveFix(item.elements, moved.dx, moved.dy);
          appendMovePatch(item.slotId, snappedMove, patches, after);
          continue;
        }
        if (item.isCharacterGroup || item.isLayoutGroup || item.isGeneratedGroup) {
          snapAndApplyMoveFix(item.elements, local.totalDx, local.totalDy);
          for (const node of item.elements || []) {
            appendMovedElementPatch(node, local, patches, after);
          }
          continue;
        }
        if (item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup) {
          const snappedMove = snapAndApplyMoveFix(item.elements, local.totalDx, local.totalDy);
          appendMovePatch(item.slotId, snappedMove, patches, after);
          continue;
        }
        if (item.isTableGroup) {
          const snappedMove = snapAndApplyMoveFix(item.elements, local.totalDx, local.totalDy);
          appendMovePatch(item.slotId, snappedMove, patches, after);
          continue;
        }
        if (item.isGraphPaperGroup) {
          for (const node of item.elements || []) {
            appendMovedElementPatch(node, local, patches, after);
          }
          continue;
        }
        const current = readSlotPatchValue(item.el);
        const beforeValue = local.beforeMap.get(item.slotId);
        const value = movedPatchValueFromBefore(beforeValue, current);
        if (!value) continue;
        applyPatchValueToElement(item.el, value);
        appendMultiTargetPatch(item.slotIds || [item.slotId], value, patches, after);
      }
      return { patches, after };
    }

    function ensureSelectionOverlay(svg) {
      return canvasEnsureSelectionOverlay(svg, beginResizeFromHandle);
    }

    function updateCanvasGuide() {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return;
      let guide = svg.querySelector("#canvasGuide");
      if (!guide) {
        guide = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        guide.setAttribute("id", "canvasGuide");
        guide.setAttribute("class", "canvas-guide");
        svg.insertBefore(guide, svg.firstChild);
      }
      const box = getSvgCanvasBounds() || currentCanvasBox();
      const inset = 0.75;
      guide.setAttribute("x", String((box.x || 0) + inset));
      guide.setAttribute("y", String((box.y || 0) + inset));
      guide.setAttribute("width", String(Math.max(0, (box.width || 0) - inset * 2)));
      guide.setAttribute("height", String(Math.max(0, (box.height || 0) - inset * 2)));
    }

    function selectedResizableItem() {
      if (selectedSlots.size !== 1) return null;
      const item = Array.from(selectedSlots.values())[0];
      if (!item || item.isFraction || !item.el) return null;
      if (item.isCanvas) return item;
      if (item.isPaperFoldGroup || item.isMeasurementGroup || item.isGeneratedGroup) return null;
      if (item.isCharacterGroup) return item;
      if (item.isFigureGroup || item.isTableGroup || item.isGraphPaperGroup || item.isLayoutGroup) return item;
      const tag = item.el.tagName.toLowerCase();
      if (!["text", "rect", "image", "circle", "line", "path", "polygon"].includes(tag)) return null;
      return item;
    }

    function tableOuterBox(item, svg) {
      if (!item || !item.isTableGroup) return null;
      const base = item.slotId || "slot.table";
      const elements = item.elements || [];
      const outer = elements.find((el) => slotIdFromElement(el) === `${base}.outer` && el.tagName.toLowerCase() === "rect");
      if (outer) {
        const value = readSlotPatchValue(outer);
        if (value && value.x !== undefined && value.y !== undefined && value.width !== undefined && value.height !== undefined) {
          return { x: Number(value.x), y: Number(value.y), width: Number(value.width), height: Number(value.height) };
        }
      }
      const boxes = [];
      for (const el of elements) {
        const tag = el.tagName.toLowerCase();
        if (!(tag === "rect" || tag === "line" || tag === "path" || tag === "polygon")) continue;
        const box = visualSvgBox(el, svg);
        if (box) boxes.push(box);
      }
      if (!boxes.length) return null;
      const minX = Math.min(...boxes.map((b) => b.x));
      const minY = Math.min(...boxes.map((b) => b.y));
      const maxX = Math.max(...boxes.map((b) => b.x + b.width));
      const maxY = Math.max(...boxes.map((b) => b.y + b.height));
      return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
    }

    function itemBBox(item) {
      if (item && item.isCanvas) {
        return getSvgCanvasBounds();
      }
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (item && item.isTableGroup) {
        const tableBox = tableOuterBox(item, svg);
        if (tableBox) return tableBox;
      }
      if (item && !item.isFigureGroup && !item.isPaperFoldGroup && !item.isMeasurementGroup && !item.isTableGroup && !item.isGraphPaperGroup && !item.isLayoutGroup && !item.isFraction && item.el) {
        const rotation = parseRotateTransform(item.el.getAttribute("transform") || "");
        const rawBox = geometrySvgBox(item.el);
        if (rawBox && rotation.angle && rotation.cx !== null && rotation.cy !== null) return rawBox;
      }
      const elements = item && (item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isLayoutGroup || item.isFraction || item.isGeneratedGroup || item.isCharacterGroup) ? (item.elements || []) : [item.el];
      const boxes = [];
      for (const el of elements) {
        const box = item?.isFigureGroup ? (slotValueBox(el) || visualSvgBox(el, svg)) : visualSvgBox(el, svg);
        if (box) boxes.push(box);
      }
      if (!boxes.length) return null;
      const minX = Math.min(...boxes.map((b) => b.x));
      const minY = Math.min(...boxes.map((b) => b.y));
      const maxX = Math.max(...boxes.map((b) => b.x + b.width));
      const maxY = Math.max(...boxes.map((b) => b.y + b.height));
      return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
    }

    function selectionTransformForItem(item) {
      if (!item || item.isCanvas || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isLayoutGroup || item.isGeneratedGroup || item.isFraction || !item.el) return { transform: "", rotation: null };
      const rotation = parseRotateTransform(item.el.getAttribute("transform") || "");
      if (!rotation.angle || rotation.cx === null || rotation.cy === null) return { transform: "", rotation: null };
      return { transform: rotateTransform(rotation.angle, rotation.cx, rotation.cy), rotation };
    }

    function tableDividerInfo(el) {
      const slotId = slotIdFromElement(el);
      const m = slotId && slotId.match(/^(slot\.table(?:_\d+)?)\.([vh])\d+$/);
      if (!m) return null;
      const value = readSlotPatchValue(el);
      if (!value) return null;
      const axis = m[2];
      const tag = el.tagName.toLowerCase();
      if (tag === "line" && value.x1 !== undefined) {
        return { slotId, axis, x1: value.x1, y1: value.y1, x2: value.x2, y2: value.y2 };
      }
      if (tag === "rect" && value.x !== undefined) {
        if (axis === "v") return { slotId, axis, x1: value.x, y1: value.y, x2: value.x, y2: value.y + (value.height || 0) };
        return { slotId, axis, x1: value.x, y1: value.y, x2: value.x + (value.width || 0), y2: value.y };
      }
      return null;
    }

    function updateTableAdjustmentHandles(svg, layer, item) {
      for (const old of layer.querySelectorAll(".table-cell-selected")) old.remove();
      const infos = item && item.isTableGroup
        ? (item.elements || []).map((el) => tableDividerInfo(el)).filter(Boolean)
        : [];
      canvasRenderTableAdjustmentHandles(layer, infos, beginResizeFromHandle);
      if (!item || !item.isTableGroup || !selectedTableCells.length) return;
      for (const cell of selectedTableCells.filter((entry) => entry.base === item.slotId)) {
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", "table-cell-selected");
        rect.setAttribute("x", String(cell.left));
        rect.setAttribute("y", String(cell.top));
        rect.setAttribute("width", String(cell.right - cell.left));
        rect.setAttribute("height", String(cell.bottom - cell.top));
        layer.appendChild(rect);
      }
    }

    function updatePathPointHandles(svg, layer, item) {
      if (!item || !item.el || item.el.tagName.toLowerCase() !== "path" || item.el.getAttribute("transform")) {
        canvasRenderPathPointHandles(layer, null, beginResizeFromHandle);
        return;
      }
      canvasRenderPathPointHandles(layer, editablePathFromD(item.el.getAttribute("d") || ""), beginResizeFromHandle);
    }

    function updateSelectionHandles() {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return;
      const layer = ensureSelectionOverlay(svg);
      clearPathPointHandles(layer);
      const item = selectedResizableItem();
      if (!item) {
        updateTableAdjustmentHandles(svg, layer, null);
        canvasHideSelectionOverlay(layer);
        return;
      }
      const box = itemBBox(item);
      if (!box || box.width < 0 || box.height < 0) {
        updateTableAdjustmentHandles(svg, layer, null);
        canvasHideSelectionOverlay(layer);
        return;
      }
      const selectionTransform = selectionTransformForItem(item);
      const isLine = !item.isCanvas && !item.isFigureGroup && !item.isPaperFoldGroup && !item.isGraphPaperGroup && !item.isLayoutGroup && item.el && item.el.tagName.toLowerCase() === "line";
      const line = isLine ? {
        x1: Number(item.el.getAttribute("x1") || 0),
        y1: Number(item.el.getAttribute("y1") || 0),
        x2: Number(item.el.getAttribute("x2") || 0),
        y2: Number(item.el.getAttribute("y2") || 0),
      } : null;
      canvasUpdateSelectionOverlay(layer, {
        box,
        isCanvas: !!item.isCanvas,
        isLine,
        line,
        transform: selectionTransform.transform,
      });
      updatePathPointHandles(svg, layer, item);
      updateTableAdjustmentHandles(svg, layer, item);
      svg.appendChild(layer);
    }

    function translateSelectionOverlay(dx, dy) {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return false;
      const layer = svg.querySelector("#selectionOverlay");
      return canvasTranslateSelectionOverlay(layer, dx, dy);
    }

    function cloneBBox(box) {
      return canvasCloneBBox(box);
    }

    function adjustedBBox(startBox, handle, dx, dy) {
      return canvasAdjustedBBox(startBox, handle, dx, dy);
    }

    function adjustedCanvasBox(startBox, handle, dx, dy) {
      return canvasAdjustedCanvasBox(startBox, handle, dx, dy);
    }

    function linePatchFromEndpoint(el, handle, startValue, point) {
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      return canvasLinePatchFromEndpoint(el, handle, startValue, point, snap);
    }

    function rotatePointAround(point, center, angleRadians) {
      return canvasRotatePointAround(point, center, angleRadians);
    }

    function linePatchFromRotation(el, startValue, startPoint, pointerPoint) {
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      return canvasLinePatchFromRotation(el, startValue, startPoint, pointerPoint, { snap, snapAngle: snapEnabled });
    }

    function resizePatchForElement(el, handle, startValue, startBox, nextBox) {
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      const tag = el.tagName.toLowerCase();
      if (handle === "c") {
        const dx = nextBox.x - startBox.x;
        const dy = nextBox.y - startBox.y;
        if (tag === "text" && el.getAttribute("data-slot-kind") === "text_box") {
          const x = snap(startValue.x + dx);
          const y = snap(startValue.y + dy);
          const textX = snap(Number(el.getAttribute("x") || 0) + dx);
          const textY = snap(Number(el.getAttribute("y") || 0) + dy);
          el.setAttribute("data-box-x", String(x));
          el.setAttribute("data-box-y", String(y));
          el.setAttribute("x", String(textX));
          el.setAttribute("y", String(textY));
          const transform = shiftedStartRotateTransform(startValue, dx, dy, snapEnabled);
          if (transform) el.setAttribute("transform", transform);
          moveTextBoxTspans(el, textX, dy, snap);
          const out = { x, y, width: startValue.width, height: startValue.height };
          if (transform) out.transform = transform;
          return out;
        }
        if (tag === "text" || tag === "rect" || tag === "image") {
          const x = snap(startValue.x + dx);
          const y = snap(startValue.y + dy);
          el.setAttribute("x", String(x));
          el.setAttribute("y", String(y));
          const out = { x, y };
          const transform = shiftedStartRotateTransform(startValue, dx, dy, snapEnabled);
          if (transform) el.setAttribute("transform", transform);
          if (transform) out.transform = transform;
          if (tag === "rect" || tag === "image") {
            out.width = startValue.width;
            out.height = startValue.height;
          }
          if (tag === "text" && startValue.font_size !== undefined) out.font_size = startValue.font_size;
          return out;
        }
        if (tag === "circle") {
          const cx = snap(startValue.cx + dx);
          const cy = snap(startValue.cy + dy);
          el.setAttribute("cx", String(cx));
          el.setAttribute("cy", String(cy));
          const out = { cx, cy, r: startValue.r };
          const transform = shiftedStartRotateTransform(startValue, dx, dy, snapEnabled);
          if (transform) el.setAttribute("transform", transform);
          if (transform) out.transform = transform;
          return out;
        }
        if (tag === "line") {
          const x1 = snap(startValue.x1 + dx);
          const y1 = snap(startValue.y1 + dy);
          const x2 = snap(startValue.x2 + dx);
          const y2 = snap(startValue.y2 + dy);
          el.setAttribute("x1", String(x1));
          el.setAttribute("y1", String(y1));
          el.setAttribute("x2", String(x2));
          el.setAttribute("y2", String(y2));
          const out = { x1, y1, x2, y2 };
          const transform = shiftedStartRotateTransform(startValue, dx, dy, snapEnabled);
          if (transform) el.setAttribute("transform", transform);
          if (transform) out.transform = transform;
          return out;
        }
        if (tag === "path") {
          const d = shiftPathD(startValue.d || "", dx, dy);
          el.setAttribute("d", d);
          const out = { d };
          const transform = shiftedStartRotateTransform(startValue, dx, dy, snapEnabled);
          if (transform) el.setAttribute("transform", transform);
          if (transform) out.transform = transform;
          return out;
        }
        if (tag === "polygon") {
          const points = (startValue.points || []).map(([x, y]) => [snap(x + dx), snap(y + dy)]);
          el.setAttribute("points", formatPolygonPoints(points));
          const out = { points };
          const transform = shiftedStartRotateTransform(startValue, dx, dy, snapEnabled);
          if (transform) el.setAttribute("transform", transform);
          if (transform) out.transform = transform;
          return out;
        }
        return null;
      }
      if (tag === "rect" || tag === "image") {
        const x = snap(nextBox.x);
        const y = snap(nextBox.y);
        const width = Math.max(4, snap(nextBox.width));
        const height = Math.max(4, snap(nextBox.height));
        el.setAttribute("x", String(x));
        el.setAttribute("y", String(y));
        el.setAttribute("width", String(width));
        el.setAttribute("height", String(height));
        return { x, y, width, height };
      }
      if (tag === "circle") {
        const cx = snap(nextBox.x + nextBox.width / 2);
        const cy = snap(nextBox.y + nextBox.height / 2);
        const r = Math.max(2, snap(Math.max(nextBox.width, nextBox.height) / 2));
        el.setAttribute("cx", String(cx));
        el.setAttribute("cy", String(cy));
        el.setAttribute("r", String(r));
        return { cx, cy, r };
      }
      if (tag === "line") {
        let x1 = startValue.x1;
        let y1 = startValue.y1;
        let x2 = startValue.x2;
        let y2 = startValue.y2;
        if (handle.includes("w")) x1 += nextBox.x - startBox.x;
        if (handle.includes("e")) x2 += (nextBox.x + nextBox.width) - (startBox.x + startBox.width);
        if (handle.includes("n")) y1 += nextBox.y - startBox.y;
        if (handle.includes("s")) y2 += (nextBox.y + nextBox.height) - (startBox.y + startBox.height);
        x1 = snap(x1);
        y1 = snap(y1);
        x2 = snap(x2);
        y2 = snap(y2);
        el.setAttribute("x1", String(x1));
        el.setAttribute("y1", String(y1));
        el.setAttribute("x2", String(x2));
        el.setAttribute("y2", String(y2));
        return { x1, y1, x2, y2 };
      }
      if (tag === "text") {
        if (el.getAttribute("data-slot-kind") === "text_box") {
          const x = snap(nextBox.x);
          const y = snap(nextBox.y);
          const width = Math.max(8, snap(nextBox.width));
          const height = Math.max(8, snap(nextBox.height));
          const dx = x - startValue.x;
          const dy = y - startValue.y;
          const textX = snap(textBoxTextX(el, x, width));
          el.setAttribute("data-box-x", String(x));
          el.setAttribute("data-box-y", String(y));
          el.setAttribute("data-box-width", String(width));
          el.setAttribute("data-box-height", String(height));
          el.setAttribute("x", String(textX));
          el.setAttribute("y", String(snap(Number(el.getAttribute("y") || 0) + dy)));
          moveTextBoxTspans(el, textX, dy, snap);
          return { x, y, width, height, font_size: startValue.font_size };
        }
        const width = Math.max(8, snap(nextBox.width));
        const x = snap(nextBox.x);
        const y = snap(startValue.y);
        const fontSize = startValue.font_size || Number(el.getAttribute("font-size") || 28);
        el.setAttribute("x", String(x));
        el.setAttribute("y", String(y));
        el.setAttribute("font-size", String(fontSize));
        el.setAttribute("max_width", String(width));
        return { x, y, font_size: fontSize, max_width: width };
      }
      if (tag === "path") {
        const d = scalePathD(startValue.d || "", startBox, nextBox);
        el.setAttribute("d", d);
        return { d };
      }
      if (tag === "polygon") {
        const points = (startValue.points || []).map(([x, y]) => {
          const p = mapPointBetweenBoxes(x, y, startBox, nextBox);
          return [snap(p.x), snap(p.y)];
        });
        el.setAttribute("points", formatPolygonPoints(points));
        return { points };
      }
      return null;
    }

    function mapPointBetweenBoxes(x, y, startBox, nextBox) {
      const sx = nextBox.width / Math.max(startBox.width, 1);
      const sy = nextBox.height / Math.max(startBox.height, 1);
      return {
        x: nextBox.x + (x - startBox.x) * sx,
        y: nextBox.y + (y - startBox.y) * sy,
      };
    }

    function resizePatchForGroupElement(el, startValue, startBox, nextBox) {
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      const tag = el.tagName.toLowerCase();
      const sx = nextBox.width / Math.max(startBox.width, 1);
      const sy = nextBox.height / Math.max(startBox.height, 1);
      const scale = Math.max(sx, sy);
      if (tag === "text" || tag === "rect" || tag === "image") {
        const p = mapPointBetweenBoxes(startValue.x, startValue.y, startBox, nextBox);
        const out = { x: snap(p.x), y: snap(p.y) };
        if (tag === "rect" || tag === "image") {
          out.width = Math.max(4, snap((startValue.width || 0) * sx));
          out.height = Math.max(4, snap((startValue.height || 0) * sy));
        }
        if (tag === "text" && startValue.font_size !== undefined) {
          out.font_size = Math.max(6, snap(startValue.font_size * scale));
        }
        if (tag === "text" && startValue.max_width !== undefined) {
          out.max_width = Math.max(8, snap(startValue.max_width * sx));
        }
        applyPatchValueToElement(el, out);
        return out;
      }
      if (tag === "circle") {
        const p = mapPointBetweenBoxes(startValue.cx, startValue.cy, startBox, nextBox);
        const out = {
          cx: snap(p.x),
          cy: snap(p.y),
          r: Math.max(2, snap((startValue.r || 0) * scale)),
        };
        applyPatchValueToElement(el, out);
        return out;
      }
      if (tag === "line") {
        const p1 = mapPointBetweenBoxes(startValue.x1, startValue.y1, startBox, nextBox);
        const p2 = mapPointBetweenBoxes(startValue.x2, startValue.y2, startBox, nextBox);
        const out = { x1: snap(p1.x), y1: snap(p1.y), x2: snap(p2.x), y2: snap(p2.y) };
        applyPatchValueToElement(el, out);
        return out;
      }
      if (tag === "path") {
        const out = { d: scalePathD(startValue.d || "", startBox, nextBox) };
        applyPatchValueToElement(el, out);
        return out;
      }
      if (tag === "polygon") {
        const out = {
          points: (startValue.points || []).map(([x, y]) => {
            const p = mapPointBetweenBoxes(x, y, startBox, nextBox);
            return [snap(p.x), snap(p.y)];
          }),
        };
        applyPatchValueToElement(el, out);
        return out;
      }
      return null;
    }

    function resizeFigureGroup(state, nextBox) {
      const values = [];
      for (const entry of state.startValue || []) {
        const value = resizePatchForGroupElement(entry.el, entry.value, state.startBox, nextBox);
        if (value) values.push({ slotId: entry.slotId, el: entry.el, value });
      }
      return values;
    }

    function resizeGraphPaperGroup(state, nextBox) {
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      const verticals = [];
      const horizontals = [];
      for (const entry of state.startValue || []) {
        const slotId = String(entry.slotId || "");
        const vMatch = slotId.match(/\.v(\d+)$/);
        const hMatch = slotId.match(/\.h(\d+)$/);
        if (vMatch) verticals.push({ ...entry, index: Number(vMatch[1]) });
        if (hMatch) horizontals.push({ ...entry, index: Number(hMatch[1]) });
      }
      verticals.sort((a, b) => a.index - b.index);
      horizontals.sort((a, b) => a.index - b.index);
      if (verticals.length < 2 || horizontals.length < 2) return resizeFigureGroup(state, nextBox);

      const colCount = Math.max(1, verticals.length - 1);
      const rowCount = Math.max(1, horizontals.length - 1);
      const left = snap(nextBox.x);
      const top = snap(nextBox.y);
      const cellWidth = Math.max(snapEnabled ? SNAP_STEP : 1, snap(nextBox.width / colCount));
      const cellHeight = Math.max(snapEnabled ? SNAP_STEP : 1, snap(nextBox.height / rowCount));
      const right = left + cellWidth * colCount;
      const bottom = top + cellHeight * rowCount;
      const values = [];

      for (const entry of verticals) {
        const x = left + cellWidth * entry.index;
        const value = {
          ...entry.value,
          x1: x,
          y1: top,
          x2: x,
          y2: bottom,
        };
        applyPatchValueToElement(entry.el, value);
        values.push({ slotId: entry.slotId, el: entry.el, value });
      }
      for (const entry of horizontals) {
        const y = top + cellHeight * entry.index;
        const value = {
          ...entry.value,
          x1: left,
          y1: y,
          x2: right,
          y2: y,
        };
        applyPatchValueToElement(entry.el, value);
        values.push({ slotId: entry.slotId, el: entry.el, value });
      }
      return values;
    }

    function tableDividerValuesFromDrag(state, dx, dy) {
      const m = String(state.handle || "").match(/^table-([vh]):(.+)$/);
      if (!m) return null;
      const axis = m[1];
      const slotId = m[2];
      const target = (state.startValue || []).find((entry) => entry.slotId === slotId);
      if (!target || !target.value) return null;
      const value = { ...target.value };
      const delta = axis === "v" ? dx : dy;
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      const tag = target.el.tagName.toLowerCase();
      if (tag === "line") {
        if (axis === "v") {
          value.x1 = snap(target.value.x1 + delta);
          value.x2 = snap(target.value.x2 + delta);
          value.y1 = target.value.y1;
          value.y2 = target.value.y2;
        } else {
          value.y1 = snap(target.value.y1 + delta);
          value.y2 = snap(target.value.y2 + delta);
          value.x1 = target.value.x1;
          value.x2 = target.value.x2;
        }
      } else if (tag === "rect") {
        if (axis === "v") value.x = snap(target.value.x + delta);
        else value.y = snap(target.value.y + delta);
      } else {
        return null;
      }
      applyPatchValueToElement(target.el, value);
      const out = [{ slotId: target.slotId, el: target.el, value }];
      out.push(...tableRelayoutValues(state.item));
      return mergePatchEntries(out);
    }

    function approximateTextWidth(text, fontSize) {
      let width = 0;
      for (const ch of String(text || "")) {
        if (/\s/.test(ch)) width += fontSize * 0.35;
        else width += ch.charCodeAt(0) < 128 ? fontSize * 0.58 : fontSize * 0.92;
      }
      return width;
    }

    function approximateWrappedLineCount(text, maxWidth, fontSize) {
      const cleanMax = Number(maxWidth || 0);
      if (!cleanMax || cleanMax <= 0) return Math.max(1, String(text || "").split(/\n/).length);
      let count = 0;
      for (const paragraph of String(text || "").split(/\n/)) {
        if (!paragraph) {
          count += 1;
          continue;
        }
        let current = "";
        const words = paragraph.split(" ");
        for (const word of words) {
          const pieces = [];
          let piece = "";
          for (const ch of word) {
            const trialPiece = piece + ch;
            if (piece && approximateTextWidth(trialPiece, fontSize) > cleanMax) {
              pieces.push(piece);
              piece = ch;
            } else {
              piece = trialPiece;
            }
          }
          pieces.push(piece || word);
          for (const nextPiece of pieces) {
            const trial = current ? `${current} ${nextPiece}` : nextPiece;
            if (current && approximateTextWidth(trial, fontSize) > cleanMax) {
              count += 1;
              current = nextPiece;
            } else {
              current = trial;
            }
          }
        }
        if (current) count += 1;
      }
      return Math.max(1, count);
    }

    function tableGridEdges(item) {
      if (!item || !item.isTableGroup) return null;
      const base = item.slotId || "slot.table";
      const outer = (item.elements || []).find((el) => slotIdFromElement(el) === `${base}.outer`);
      if (!outer) return null;
      const outerValue = readSlotPatchValue(outer);
      if (!outerValue || outerValue.x === undefined || outerValue.y === undefined || outerValue.width === undefined || outerValue.height === undefined) return null;
      const left = Number(outerValue.x);
      const right = left + Number(outerValue.width);
      const top = Number(outerValue.y);
      const bottom = top + Number(outerValue.height);
      const verticals = [];
      const horizontals = [];
      for (const el of item.elements || []) {
        const info = tableDividerInfo(el);
        if (info && info.axis === "v") verticals.push(Number(info.x1));
        if (info && info.axis === "h") horizontals.push(Number(info.y1));
      }
      return {
        cols: uniqueSortedNumbers([left, ...verticals, right]),
        rows: uniqueSortedNumbers([top, ...horizontals, bottom]),
      };
    }

    function tableTextCells(item) {
      if (!item || !item.isTableGroup) return [];
      const base = item.slotId || "slot.table";
      const cells = [];
      for (const el of item.elements || []) {
        const slotId = slotIdFromElement(el);
        const m = slotId && slotId.match(/^(slot\.table(?:_\d+)?)\.r(\d+)c(\d+)$/);
        if (!m || m[1] !== base || el.tagName.toLowerCase() !== "text") continue;
        cells.push({ el, slotId, row: Number(m[2]) - 1, col: Number(m[3]) - 1 });
      }
      return cells;
    }

    function tableCellFillSlotId(base, row, col) {
      return `${base}.r${row + 1}c${col + 1}.fill`;
    }

    function tableCellKey(cell) {
      return cell ? `${cell.base}:r${cell.row + 1}c${cell.col + 1}` : "";
    }

    function sameTableCell(a, b) {
      return !!a && !!b && a.base === b.base && a.row === b.row && a.col === b.col;
    }

    function tableCellAtPoint(svg, item, clientX, clientY) {
      const grid = tableGridEdges(item);
      if (!svg || !grid) return null;
      const point = getSvgPoint(svg, clientX, clientY);
      const col = grid.cols.findIndex((left, index) => index < grid.cols.length - 1 && point.x >= left && point.x <= grid.cols[index + 1]);
      const row = grid.rows.findIndex((top, index) => index < grid.rows.length - 1 && point.y >= top && point.y <= grid.rows[index + 1]);
      if (row < 0 || col < 0) return null;
      return {
        base: item.slotId || "slot.table",
        row,
        col,
        left: grid.cols[col],
        right: grid.cols[col + 1],
        top: grid.rows[row],
        bottom: grid.rows[row + 1],
      };
    }

    function tableCellByIndex(item, row, col) {
      const grid = tableGridEdges(item);
      if (!grid || row < 0 || col < 0 || row + 1 >= grid.rows.length || col + 1 >= grid.cols.length) return null;
      return {
        base: item.slotId || "slot.table",
        row,
        col,
        left: grid.cols[col],
        right: grid.cols[col + 1],
        top: grid.rows[row],
        bottom: grid.rows[row + 1],
      };
    }

    function tableCellFillElements(item) {
      if (!item || !item.isTableGroup) return [];
      const base = item.slotId || "slot.table";
      const fills = [];
      for (const el of item.elements || []) {
        const slotId = slotIdFromElement(el);
        const m = slotId && slotId.match(/^(slot\.table(?:_\d+)?)\.r(\d+)c(\d+)\.fill$/);
        if (!m || m[1] !== base || el.tagName.toLowerCase() !== "rect") continue;
        fills.push({ el, slotId, row: Number(m[2]) - 1, col: Number(m[3]) - 1 });
      }
      return fills;
    }

    function tableCellFillForCell(item, cell) {
      return tableCellFillElements(item).find((entry) => entry.row === cell.row && entry.col === cell.col) || null;
    }

    function setSelectedTableCell(item, cell, append = false) {
      if (!item || !cell) {
        selectedTableCells = [];
        return;
      }
      if (!append) {
        selectedTableCells = [cell];
        return;
      }
      const exists = selectedTableCells.some((selected) => sameTableCell(selected, cell));
      selectedTableCells = exists
        ? selectedTableCells.filter((selected) => !sameTableCell(selected, cell))
        : [...selectedTableCells.filter((selected) => selected.base === cell.base), cell];
      if (!selectedTableCells.length) selectedTableCells = [cell];
    }

    function selectedTableFillContextItem() {
      if (!selectedTableCells.length || selectedSlots.size !== 1) return null;
      const item = Array.from(selectedSlots.values())[0];
      return item && item.isTableGroup ? item : null;
    }

    function tableStructuralElements(item) {
      const base = item?.slotId || "slot.table";
      const outer = (item?.elements || []).find((el) => slotIdFromElement(el) === `${base}.outer`) || null;
      const verticals = [];
      const horizontals = [];
      for (const el of item?.elements || []) {
        const info = tableDividerInfo(el);
        if (info && info.axis === "v") verticals.push({ el, slotId: info.slotId, value: readSlotPatchValue(el) });
        if (info && info.axis === "h") horizontals.push({ el, slotId: info.slotId, value: readSlotPatchValue(el) });
      }
      verticals.sort((a, b) => Number(a.value?.x1 ?? 0) - Number(b.value?.x1 ?? 0));
      horizontals.sort((a, b) => Number(a.value?.y1 ?? 0) - Number(b.value?.y1 ?? 0));
      return { outer, verticals, horizontals };
    }

    function applyTableAutoFitRows(item, options = {}) {
      const grid = tableGridEdges(item);
      if (!grid || grid.rows.length < 2 || grid.cols.length < 2) return [];
      const paddingY = Number(options.paddingY ?? 10);
      const minRowHeight = Number(options.minRowHeight ?? 34);
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      const rowHeights = [];
      for (let row = 0; row < grid.rows.length - 1; row += 1) {
        rowHeights[row] = Math.max(minRowHeight, grid.rows[row + 1] - grid.rows[row]);
      }

      for (const cell of tableTextCells(item)) {
        if (cell.row < 0 || cell.row >= rowHeights.length || cell.col < 0 || cell.col + 1 >= grid.cols.length) continue;
        const current = readSlotPatchValue(cell.el);
        if (!current) continue;
        const fontSize = Number(current.font_size || cell.el.getAttribute("font-size") || 18);
        const maxWidth = Math.max(8, grid.cols[cell.col + 1] - grid.cols[cell.col] - 20);
        const lineCount = approximateWrappedLineCount(current.text ?? cell.el.getAttribute("data-raw-text") ?? cell.el.textContent ?? "", maxWidth, fontSize);
        const required = Math.max(minRowHeight, fontSize + (lineCount - 1) * fontSize * 1.2 + paddingY * 2);
        rowHeights[cell.row] = Math.max(rowHeights[cell.row], snap(required));
      }

      const nextRows = [grid.rows[0]];
      for (const height of rowHeights) {
        nextRows.push(snap(nextRows[nextRows.length - 1] + height));
      }
      const oldBottom = grid.rows[grid.rows.length - 1];
      const nextBottom = nextRows[nextRows.length - 1];
      const changed = nextRows.some((value, index) => Math.abs(value - grid.rows[index]) > 0.01);
      if (!changed) return [];

      const { outer, verticals, horizontals } = tableStructuralElements(item);
      const values = [];
      if (outer) {
        const current = readSlotPatchValue(outer);
        if (current) {
          const value = { ...current, height: snap(Number(current.height || 0) + (nextBottom - oldBottom)) };
          applyPatchValueToElement(outer, value);
          values.push({ slotId: slotIdFromElement(outer), el: outer, value });
        }
      }
      for (const entry of verticals) {
        if (!entry.value) continue;
        const value = { ...entry.value, y1: nextRows[0], y2: nextBottom };
        applyPatchValueToElement(entry.el, value);
        values.push({ slotId: entry.slotId, el: entry.el, value });
      }
      for (let i = 0; i < horizontals.length; i += 1) {
        const entry = horizontals[i];
        if (!entry.value || i + 1 >= nextRows.length - 1) continue;
        const y = nextRows[i + 1];
        const value = { ...entry.value, y1: y, y2: y };
        applyPatchValueToElement(entry.el, value);
        values.push({ slotId: entry.slotId, el: entry.el, value });
      }
      return values;
    }

    function tableTextCellLayoutValues(item) {
      const grid = tableGridEdges(item);
      if (!grid) return [];
      const base = item.slotId || "slot.table";
      const padding = 10;
      const values = [];
      for (const el of item.elements || []) {
        const slotId = slotIdFromElement(el);
        const m = slotId && slotId.match(/^(slot\.table(?:_\d+)?)\.r(\d+)c(\d+)$/);
        if (!m || el.tagName.toLowerCase() !== "text") continue;
        if (m[1] !== base) continue;
        const row = Number(m[2]) - 1;
        const col = Number(m[3]) - 1;
        if (col < 0 || col + 1 >= grid.cols.length || row < 0 || row + 1 >= grid.rows.length) continue;
        const current = readSlotPatchValue(el);
        if (!current) continue;
        const left = grid.cols[col];
        const right = grid.cols[col + 1];
        const top = grid.rows[row];
        const bottom = grid.rows[row + 1];
        const maxWidth = Math.max(8, right - left - padding * 2);
        const fontSize = Number(current.font_size || el.getAttribute("font-size") || 18);
        const lineCount = approximateWrappedLineCount(current.text ?? el.getAttribute("data-raw-text") ?? el.textContent ?? "", maxWidth, fontSize);
        const lineStep = fontSize * 1.2;
        const totalTextHeight = Math.max(fontSize, fontSize + (lineCount - 1) * lineStep);
        const y = Math.max(top + fontSize, top + (bottom - top - totalTextHeight) / 2 + fontSize);
        const value = {
          ...current,
          x: snapEnabled ? snapValue((left + right) / 2) : (left + right) / 2,
          y: snapEnabled ? snapValue(y) : y,
          max_width: snapEnabled ? snapValue(maxWidth) : maxWidth,
          anchor: current.anchor || el.getAttribute("text-anchor") || "middle",
        };
        applyPatchValueToElement(el, value);
        values.push({ slotId, el, value });
      }
      return values;
    }

    function tableCellFillLayoutValues(item) {
      const grid = tableGridEdges(item);
      if (!grid) return [];
      const values = [];
      for (const fill of tableCellFillElements(item)) {
        if (fill.col < 0 || fill.col + 1 >= grid.cols.length || fill.row < 0 || fill.row + 1 >= grid.rows.length) continue;
        const current = readSlotPatchValue(fill.el);
        if (!current) continue;
        const value = {
          ...current,
          x: grid.cols[fill.col],
          y: grid.rows[fill.row],
          width: grid.cols[fill.col + 1] - grid.cols[fill.col],
          height: grid.rows[fill.row + 1] - grid.rows[fill.row],
        };
        applyPatchValueToElement(fill.el, value);
        values.push({ slotId: fill.slotId, el: fill.el, value });
      }
      return values;
    }

    function mergePatchEntries(entries) {
      const bySlot = new Map();
      for (const entry of entries || []) {
        if (!entry || !entry.slotId || !entry.value) continue;
        bySlot.set(entry.slotId, entry);
      }
      return Array.from(bySlot.values());
    }

    function tableRelayoutValues(item, options = {}) {
      return mergePatchEntries([
        ...(options.autoFit === false ? [] : applyTableAutoFitRows(item, options)),
        ...tableCellFillLayoutValues(item),
        ...tableTextCellLayoutValues(item),
      ]);
    }

    function tableFontSizeValues(item, fontSize) {
      const cleanFontSize = Number(fontSize);
      if (!item || !item.isTableGroup || !Number.isFinite(cleanFontSize) || cleanFontSize <= 0) return [];
      const values = [];
      for (const cell of tableTextCells(item)) {
        const current = readSlotPatchValue(cell.el);
        if (!current) continue;
        const value = { ...current, font_size: cleanFontSize };
        applyPatchValueToElement(cell.el, value);
        values.push({ slotId: cell.slotId, el: cell.el, value });
      }
      return mergePatchEntries([...values, ...tableRelayoutValues(item)]);
    }

    function tableCellFillContent(cell, fill) {
      return {
        x: cell.left,
        y: cell.top,
        width: cell.right - cell.left,
        height: cell.bottom - cell.top,
        fill,
        stroke: "none",
        stroke_width: 0,
      };
    }

    function tableLayerOrderPatch(item, ensureSlotIds = []) {
      const base = item?.slotId || "slot.table";
      const layoutText = document.getElementById("layoutView")?.value || "";
      if (!layoutText.trim()) return null;
      let layout = null;
      try {
        layout = JSON.parse(layoutText);
      } catch (_) {
        return null;
      }
      const allTableIds = new Set([...(item.slotIds || []), ...ensureSlotIds]);
      for (const fill of tableCellFillElements(item)) allTableIds.add(fill.slotId);
      const outerId = `${base}.outer`;
      const fillIds = Array.from(allTableIds).filter((id) => /^slot\.table(?:_\d+)?\.r\d+c\d+\.fill$/.test(id)).sort();
      const textIds = Array.from(allTableIds).filter((id) => /^slot\.table(?:_\d+)?\.r\d+c\d+$/.test(id)).sort();
      const dividerIds = Array.from(allTableIds).filter((id) => /^slot\.table(?:_\d+)?\.[vh]\d+$/.test(id)).sort((a, b) => {
        const ma = a.match(/\.([vh])(\d+)$/);
        const mb = b.match(/\.([vh])(\d+)$/);
        if (!ma || !mb) return a.localeCompare(b);
        if (ma[1] !== mb[1]) return ma[1].localeCompare(mb[1]);
        return Number(ma[2]) - Number(mb[2]);
      });

      for (const region of layout.regions || []) {
        if (!region || !Array.isArray(region.slot_ids)) continue;
        if (!region.slot_ids.includes(outerId) && !ensureSlotIds.some((id) => region.slot_ids.includes(id))) continue;
        const regionIds = new Set([...region.slot_ids, ...ensureSlotIds]);
        const tableOrdered = [
          ...(regionIds.has(outerId) ? [outerId] : []),
          ...fillIds.filter((id) => regionIds.has(id) || ensureSlotIds.includes(id)),
          ...dividerIds.filter((id) => regionIds.has(id)),
          ...textIds.filter((id) => regionIds.has(id)),
        ];
        const tableSet = new Set(tableOrdered);
        const rest = region.slot_ids.filter((id) => !id.startsWith(`${base}.`) || !tableSet.has(id));
        const insertAt = Math.max(0, region.slot_ids.indexOf(outerId));
        const nextOrder = [...rest.slice(0, insertAt), ...tableOrdered, ...rest.slice(insertAt)];
        return {
          target: "__layer__",
          op: "layer",
          value: { region_id: region.id || firstUsableRegionId() || "region.diagram", slot_ids: nextOrder },
        };
      }
      return null;
    }

    async function applyTableCellFill(fill) {
      const item = selectedTableFillContextItem();
      if (!item || !selectedTableCells.length) throw new Error("채울 표 셀을 먼저 선택하세요.");
      const cells = selectedTableCells
        .filter((cell) => cell.base === item.slotId)
        .map((cell) => tableCellByIndex(item, cell.row, cell.col))
        .filter(Boolean);
      if (!cells.length) throw new Error("채울 표 셀을 먼저 선택하세요.");
      const patches = [];
      const addIds = [];
      const regionId = layoutRegionBySlotId(`${item.slotId}.outer`) || firstUsableRegionId();
      for (const cell of cells) {
        const slotId = tableCellFillSlotId(cell.base, cell.row, cell.col);
        const existing = tableCellFillForCell(item, cell);
        const content = tableCellFillContent(cell, fill);
        if (existing) {
          const value = { ...(readSlotPatchValue(existing.el) || {}), ...content };
          applyPatchValueToElement(existing.el, value);
          patches.push({ target: existing.slotId, op: "update", value });
        } else {
          addIds.push(slotId);
          patches.push({
            target: slotId,
            op: "add",
            value: {
              kind: "rect",
              ...(regionId ? { region_id: regionId } : {}),
              content,
            },
          });
        }
      }
      const layerPatch = tableLayerOrderPatch(item, addIds);
      if (layerPatch) patches.push(layerPatch);
      await commitPatches(patches, `셀 채우기 적용 완료: ${cells.length}개`);
      selectedTableCells = cells;
    }

    function tableColumnEdges(item) {
      const base = item?.slotId || "slot.table";
      const outer = (item.elements || []).find((el) => slotIdFromElement(el) === `${base}.outer`);
      if (!outer) return null;
      const outerValue = readSlotPatchValue(outer);
      if (!outerValue || outerValue.x === undefined || outerValue.width === undefined) return null;
      const left = Number(outerValue.x);
      const right = left + Number(outerValue.width);
      const dividers = [];
      for (const el of item.elements || []) {
        const info = tableDividerInfo(el);
        if (info && info.axis === "v") dividers.push(Number(info.x1));
      }
      return [left, ...dividers.sort((a, b) => a - b), right];
    }

    function tableTextAlignmentValues(item, align) {
      const edges = tableColumnEdges(item);
      if (!edges) return [];
      const anchor = align === "center" ? "middle" : align === "right" ? "end" : "start";
      const padding = 10;
      const values = [];
      for (const el of item.elements || []) {
        const slotId = slotIdFromElement(el);
        const m = slotId && slotId.match(/^(slot\.table(?:_\d+)?)\.r\d+c(\d+)$/);
        if (!m || el.tagName.toLowerCase() !== "text") continue;
        if (m[1] !== item.slotId) continue;
        const col = Number(m[2]) - 1;
        if (col < 0 || col + 1 >= edges.length) continue;
        const left = edges[col];
        const right = edges[col + 1];
        const current = readSlotPatchValue(el);
        if (!current) continue;
        const x = align === "center" ? (left + right) / 2 : align === "right" ? right - padding : left + padding;
        const value = {
          ...current,
          x: snapEnabled ? snapValue(x) : x,
          anchor,
          max_width: Math.max(8, snapEnabled ? snapValue(right - left - padding * 2) : right - left - padding * 2),
        };
        applyPatchValueToElement(el, value);
        values.push({ slotId, el, value });
      }
      return values;
    }

    function clearSelection() {
      for (const item of selectedSlots.values()) {
        if (item.isCanvas) continue;
        const nodes = item.elements || [item.el];
        for (const node of nodes) node.classList.remove("slot-selected");
      }
      selectedSlots = new Map();
      selectedElement = null;
      selectedSlotId = null;
      updateSelectionHandles();
      updateTextEditControls();
    }

    function selectCanvas() {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return;
      clearSelection();
      selectedSlots.set("__canvas__", { el: svg, slotId: "__canvas__", elements: [], isCanvas: true });
      selectedElement = svg;
      selectedSlotId = "__canvas__";
      updateSelectionHandles();
      updateTextEditControls();
      setStatus("캔버스 선택: 핸들을 드래그해 크기 조절", true);
    }

    function setSelectedElement(el, slotId, append = false) {
      if (!append) clearSelection();
      if (!el || !slotId) return;
      const selectableGroup = collectSelectableGroupSlotIds(slotId);
      if (selectableGroup) {
        const elements = elementsForSlotIds(selectableGroup.slotIds);
        if (!elements.length) return;
        if (append && selectedSlots.has(selectableGroup.base)) {
          const existing = selectedSlots.get(selectableGroup.base);
          for (const node of (existing.elements || [])) node.classList.remove("slot-selected");
          selectedSlots.delete(selectableGroup.base);
        } else {
          selectedSlots.set(selectableGroup.base, {
            el: elements[0],
            slotId: selectableGroup.base,
            slotIds: selectableGroup.slotIds,
            elements,
            isFigureGroup: selectableGroup.groupKind === "figure",
            isPaperFoldGroup: selectableGroup.groupKind === "paperFold",
            isMeasurementGroup: selectableGroup.groupKind === "measurement",
            isTableGroup: selectableGroup.groupKind === "table",
            isGraphPaperGroup: selectableGroup.groupKind === "graphPaper",
            isCharacterGroup: selectableGroup.groupKind === "character",
            isGeneratedGroup: selectableGroup.groupKind === "generated",
            isLayoutGroup: selectableGroup.groupKind === "layout",
          });
          for (const node of elements) node.classList.add("slot-selected");
        }
        const last = Array.from(selectedSlots.values()).at(-1) || null;
        selectedElement = last ? last.el : null;
        selectedSlotId = last ? last.slotId : null;
        updateSelectionHandles();
        updateTextEditControls();
        return;
      }
      const fracInfo = parseFractionPartId(el.getAttribute("id"));
      const elements = (fracInfo && fracInfo.prefix === slotId) ? fractionPartElements(slotId) : [el];
      const isFraction = elements.length > 1;
      const resolvedSlotIds = isFraction ? [slotId] : (slotIdsFromElement(el).length ? slotIdsFromElement(el) : [slotId]);
      const arrowGroupIds = collectArrowGroupSlotIds(slotId);
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return;
      const allNodes = draggableSlotElements(svg);

      const toggleOff = append && arrowGroupIds.every((id) => selectedSlots.has(id));
      if (toggleOff) {
        for (const gid of arrowGroupIds) {
          const existing = selectedSlots.get(gid);
          if (!existing) continue;
          for (const node of (existing.elements || [existing.el])) node.classList.remove("slot-selected");
          selectedSlots.delete(gid);
        }
      } else {
        for (const gid of arrowGroupIds) {
          let nodeForId = null;
          if (gid === slotId && slotIdFromElement(el) === gid) {
            nodeForId = el;
          }
          for (const n of allNodes) {
            if (nodeForId) break;
            if (slotIdFromElement(n) === gid) {
              nodeForId = n;
              break;
            }
          }
          if (!nodeForId) continue;
          const fi = parseFractionPartId(nodeForId.getAttribute("id"));
          const els = (fi && fi.prefix === gid) ? fractionPartElements(gid) : [nodeForId];
          const frac = els.length > 1;
          selectedSlots.set(gid, { el: nodeForId, slotId: gid, slotIds: gid === slotId ? resolvedSlotIds : [gid], elements: els, isFraction: frac });
          for (const node of els) node.classList.add("slot-selected");
        }
      }
      const last = Array.from(selectedSlots.values()).at(-1) || null;
      selectedElement = last ? last.el : null;
      selectedSlotId = last ? last.slotId : null;
      updateSelectionHandles();
      updateTextEditControls();
    }

    function selectedTextItem() {
      if (selectedSlots.size !== 1) return null;
      const item = Array.from(selectedSlots.values())[0];
      if (!item || !item.el || item.el.tagName.toLowerCase() !== "text") return null;
      return item;
    }

    function setInspectorField(id, value) {
      const el = document.getElementById(id);
      if (!el) return;
      el.value = value === undefined || value === null ? "" : String(value);
    }

    function updateCanvasControls() {
      const canvas = currentCanvasBox();
      setInspectorField("canvasX", canvas.x ?? 0);
      setInspectorField("canvasY", canvas.y ?? 0);
      setInspectorField("canvasW", canvas.width ?? "");
      setInspectorField("canvasH", canvas.height ?? "");
    }

    function updateInspectorControls() {
      const selected = selectedSlots.size === 1 ? Array.from(selectedSlots.values())[0] : null;
      const canInspect = selected && !selected.isCanvas && !selected.isFigureGroup && !selected.isPaperFoldGroup && !selected.isMeasurementGroup && !selected.isTableGroup && !selected.isGraphPaperGroup && !selected.isGeneratedGroup && !selected.isCharacterGroup && !selected.isLayoutGroup && !selected.isFraction && selected.el;
      const value = canInspect ? readSlotPatchValue(selected.el) : null;
      const tableCells = selected && selected.isTableGroup ? tableTextCells(selected) : [];
      const tableFontSize = tableCells.length
        ? readSlotPatchValue(tableCells[0].el)?.font_size
        : "";
      updateCanvasControls();
      setInspectorField("slotId", selected ? selected.slotId : "");
      setInspectorField("propX", value?.x ?? value?.cx ?? value?.x1 ?? "");
      setInspectorField("propY", value?.y ?? value?.cy ?? value?.y1 ?? "");
      setInspectorField("propW", value?.width ?? "");
      setInspectorField("propH", value?.height ?? "");
      setInspectorField("propFontSize", selected?.isTableGroup ? tableFontSize : value?.font_size ?? "");
      setInspectorField("propRotate", value?.transform ?? "");
      const patch = document.getElementById("patchJson");
      if (patch && value) patch.value = JSON.stringify(value, null, 2);
    }

    async function commitCanvasFields() {
      if (!currentProblemId) throw new Error("먼저 문제를 선택하세요.");
      const readCanvasNumber = (id) => {
        const raw = document.getElementById(id)?.value;
        if (raw === undefined || raw === null || raw === "") return undefined;
        const n = Number(raw);
        return Number.isFinite(n) ? n : undefined;
      };
      const width = readCanvasNumber("canvasW");
      const height = readCanvasNumber("canvasH");
      if (width === undefined || height === undefined || width <= 0 || height <= 0) {
        throw new Error("캔버스 W/H는 1 이상이어야 합니다.");
      }
      const value = {
        width: snapEnabled ? snapValue(width) : width,
        height: snapEnabled ? snapValue(height) : height,
      };
      const before = [{ slotId: "__canvas__", value: currentCanvasBox() }];
      applyCanvasPatchValue(value);
      updateCanvasGuide();
      updateCanvasControls();
      updateSelectionHandles();
      await commitPatches([{ target: "__canvas__", op: "update", value }], "캔버스 크기 저장 완료");
      const after = [{ slotId: "__canvas__", value: JSON.parse(JSON.stringify(value)) }];
      if (!historyBusy) pushHistory(before, after, "캔버스 크기");
    }

    function updateTextEditControls() {
      const input = document.getElementById("textEditInput");
      const button = document.getElementById("textEditBtn");
      updateInspectorControls();
      if (!input || !button) return;
      const item = selectedTextItem();
      if (!item) {
        input.value = "";
        input.disabled = true;
        button.disabled = true;
        return;
      }
      input.disabled = false;
      button.disabled = false;
      input.value = item.el.textContent || "";
    }

    async function commitInspectorFields() {
      if (selectedSlots.size !== 1) throw new Error("요소 하나를 선택하세요.");
      const item = Array.from(selectedSlots.values())[0];
      const readNumber = (id) => {
        const raw = document.getElementById(id)?.value;
        if (raw === undefined || raw === null || raw === "") return undefined;
        const n = Number(raw);
        return Number.isFinite(n) ? n : undefined;
      };
      if (item && item.isTableGroup) {
        const font = readNumber("propFontSize");
        if (font === undefined || font <= 0) throw new Error("표 텍스트 Font 값을 입력하세요.");
        const before = readSelectedStates();
        const values = tableFontSizeValues(item, font);
        const patches = values.map((entry) => ({ target: entry.slotId, op: "update", value: entry.value }));
        if (!patches.length) throw new Error("표 텍스트를 찾지 못했습니다.");
        updateSelectionHandles();
        await commitPatches(patches, `표 글꼴 크기 저장 완료: ${font}`);
        const after = readSelectedStates();
        if (!historyBusy && before.length === after.length) pushHistory(before, after, "표 글꼴 크기");
        return;
      }
      if (!item || item.isCanvas || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup || item.isCharacterGroup || item.isLayoutGroup || item.isFraction || !item.el) {
        throw new Error("선택한 요소를 속성 패널에서 수정할 수 없습니다.");
      }
      const current = readSlotPatchValue(item.el) || {};
      const value = { ...current };
      const x = readNumber("propX");
      const y = readNumber("propY");
      const w = readNumber("propW");
      const h = readNumber("propH");
      const font = readNumber("propFontSize");
      const transform = document.getElementById("propRotate")?.value || "";
      const tag = item.el.tagName.toLowerCase();
      if (tag === "circle") {
        if (x !== undefined) value.cx = x;
        if (y !== undefined) value.cy = y;
      } else if (tag === "line") {
        const dx = x !== undefined && current.x1 !== undefined ? x - current.x1 : 0;
        const dy = y !== undefined && current.y1 !== undefined ? y - current.y1 : 0;
        if (dx || dy) Object.assign(value, applyElementDelta(item.el, dx, dy, false));
      } else {
        if (x !== undefined) value.x = x;
        if (y !== undefined) value.y = y;
      }
      if (w !== undefined) value.width = w;
      if (h !== undefined) value.height = h;
      if (font !== undefined) value.font_size = font;
      if (transform) value.transform = transform;
      else if (current.transform !== undefined) value.transform = "";
      applyPatchValueToElement(item.el, value);
      updateSelectionHandles();
      await commitPatches([{ target: item.slotId, op: "update", value }], `속성 저장 완료: ${item.slotId}`);
    }

    async function updateSelectedText() {
      const item = selectedTextItem();
      if (!item) throw new Error("텍스트 요소를 먼저 선택하세요.");
      const text = document.getElementById("textEditInput").value;
      applyPatchValueToElement(item.el, { text });
      updateSelectionHandles();
      await commitPatches([{ target: item.slotId, op: "update", value: { text } }], `텍스트 수정 완료: ${item.slotId}`);
    }

    async function alignSelectedTextInCell(align) {
      if (selectedSlots.size !== 1) throw new Error("표 또는 텍스트 하나를 선택하세요.");
      const item = Array.from(selectedSlots.values())[0];
      const anchor = align === "center" ? "middle" : align === "right" ? "end" : "start";
      let patches = [];
      if (item.isTableGroup) {
        const values = tableTextAlignmentValues(item, align);
        patches = values.map((entry) => ({ target: entry.slotId, op: "update", value: entry.value }));
      } else if (item.el && item.el.tagName.toLowerCase() === "text") {
        const value = { ...(readSlotPatchValue(item.el) || {}), anchor };
        applyPatchValueToElement(item.el, value);
        patches = [{ target: item.slotId, op: "update", value }];
      }
      if (!patches.length) throw new Error("정렬할 텍스트를 찾지 못했습니다.");
      updateSelectionHandles();
      await commitPatches(patches, `텍스트 ${align} 정렬 완료`);
    }

    async function nudgeSelectedFontSize(delta) {
      if (selectedSlots.size !== 1) throw new Error("텍스트 또는 표 하나를 선택하세요.");
      const item = Array.from(selectedSlots.values())[0];
      let currentFont = null;
      if (item.isTableGroup) {
        const cells = tableTextCells(item);
        currentFont = cells.length ? readSlotPatchValue(cells[0].el)?.font_size : null;
      } else if (item.el && item.el.tagName.toLowerCase() === "text") {
        currentFont = readSlotPatchValue(item.el)?.font_size;
      }
      const next = Math.max(6, Math.min(96, Math.round(Number(currentFont || 18) + delta)));
      setInspectorField("propFontSize", next);
      await commitInspectorFields();
    }

    function readSelectedStates() {
      const states = [];
      for (const item of selectedSlots.values()) {
        if (item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup || item.isCharacterGroup || item.isLayoutGroup) {
          for (const node of item.elements || []) {
            const slotId = slotIdFromElement(node);
            const value = readSlotPatchValue(node);
            if (slotId && value) states.push({ slotId, value: JSON.parse(JSON.stringify(value)) });
          }
          continue;
        }
        const value = readSlotPatchValue(item.el);
        if (value) states.push({ slotId: item.slotId, value: JSON.parse(JSON.stringify(value)) });
      }
      return states;
    }

    function applyPatchValueToElement(el, value) {
      const tag = el.tagName.toLowerCase();
      if (value.transform !== undefined) {
        if (value.transform) el.setAttribute("transform", String(value.transform));
        else el.removeAttribute("transform");
      }
      const applyStyleAttrs = () => {
        for (const [field, attr] of [["fill", "fill"], ["stroke", "stroke"], ["stroke_width", "stroke-width"], ["stroke_dasharray", "stroke-dasharray"]]) {
          if (value[field] === undefined) continue;
          const next = value[field];
          if (next === null || next === "") el.removeAttribute(attr);
          else el.setAttribute(attr, String(next));
        }
      };
      applyStyleAttrs();
      if (tag === "text") {
        if (value.text !== undefined) {
          el.textContent = String(value.text);
          el.removeAttribute("data-raw-text");
        }
        if (el.getAttribute("data-slot-kind") === "text_box") {
          const boxX = value.x !== undefined ? Number(value.x) : Number(el.getAttribute("data-box-x") || 0);
          const boxY = value.y !== undefined ? Number(value.y) : Number(el.getAttribute("data-box-y") || 0);
          const boxWidth = value.width !== undefined ? Number(value.width) : Number(el.getAttribute("data-box-width") || 0);
          const boxHeight = value.height !== undefined ? Number(value.height) : Number(el.getAttribute("data-box-height") || 0);
          el.setAttribute("data-box-x", String(boxX));
          el.setAttribute("data-box-y", String(boxY));
          el.setAttribute("data-box-width", String(boxWidth));
          el.setAttribute("data-box-height", String(boxHeight));
          el.setAttribute("x", String(textBoxTextX(el, boxX, boxWidth)));
          if (value.y !== undefined) el.setAttribute("y", String(boxY + Number(el.getAttribute("font-size") || 28)));
        } else {
          if (value.x !== undefined) el.setAttribute("x", String(value.x));
          if (value.y !== undefined) el.setAttribute("y", String(value.y));
        }
        if (value.font_size !== undefined) el.setAttribute("font-size", String(value.font_size));
        if (value.max_width !== undefined) el.setAttribute("max_width", String(value.max_width));
        if (value.anchor !== undefined) {
          if (value.anchor) el.setAttribute("text-anchor", String(value.anchor));
          else el.removeAttribute("text-anchor");
        }
      } else if ((tag === "rect" || tag === "image") && value.x !== undefined && value.y !== undefined) {
        el.setAttribute("x", String(value.x));
        el.setAttribute("y", String(value.y));
        if (value.width !== undefined && value.height !== undefined) {
          el.setAttribute("width", String(value.width));
          el.setAttribute("height", String(value.height));
        }
        if (tag === "image") {
          if (value.href !== undefined) el.setAttribute("href", String(value.href));
          if (value.preserve_aspect_ratio !== undefined) {
            if (value.preserve_aspect_ratio) el.setAttribute("preserveAspectRatio", String(value.preserve_aspect_ratio));
            else el.removeAttribute("preserveAspectRatio");
          }
        }
      } else if (tag === "circle" && value.cx !== undefined && value.cy !== undefined) {
        el.setAttribute("cx", String(value.cx));
        el.setAttribute("cy", String(value.cy));
        if (value.r !== undefined) el.setAttribute("r", String(value.r));
      } else if (tag === "line" && value.x1 !== undefined) {
        el.setAttribute("x1", String(value.x1));
        el.setAttribute("y1", String(value.y1));
        el.setAttribute("x2", String(value.x2));
        el.setAttribute("y2", String(value.y2));
      } else if (tag === "path" && value.d !== undefined) {
        el.setAttribute("d", String(value.d));
      } else if (tag === "polygon" && value.points !== undefined) {
        const pts = (value.points || []).map((p) => `${p[0]},${p[1]}`).join(" ");
        el.setAttribute("points", pts);
      }
    }

    function applyCanvasPatchValue(value) {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg || !value) return;
      const width = Number(value.width || 0);
      const height = Number(value.height || 0);
      if (width <= 0 || height <= 0) return;
      svg.setAttribute("width", String(width));
      svg.setAttribute("height", String(height));
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      updateCanvasGuide();
      updateCanvasControls();
    }

    function snapPatchValue(value) {
      if (!snapEnabled || !value) return value;
      const keepTransform = (out) => {
        if (value.transform !== undefined) out.transform = value.transform;
        return out;
      };
      if (value.x !== undefined && value.y !== undefined) {
        const out = { x: snapValue(value.x), y: snapValue(value.y) };
        if (value.text !== undefined) out.text = value.text;
        if (value.width !== undefined) out.width = snapValue(value.width);
        if (value.height !== undefined) out.height = snapValue(value.height);
        if (value.font_size !== undefined) out.font_size = snapValue(value.font_size);
        if (value.max_width !== undefined) out.max_width = snapValue(value.max_width);
        if (value.anchor !== undefined) out.anchor = value.anchor;
        if (value.href !== undefined) out.href = value.href;
        if (value.preserve_aspect_ratio !== undefined) out.preserve_aspect_ratio = value.preserve_aspect_ratio;
        return keepTransform(out);
      }
      if (value.text !== undefined) return keepTransform({ text: value.text });
      if (value.cx !== undefined && value.cy !== undefined) {
        const out = { cx: snapValue(value.cx), cy: snapValue(value.cy) };
        if (value.r !== undefined) out.r = snapValue(value.r);
        return keepTransform(out);
      }
      if (value.x1 !== undefined && value.y1 !== undefined) {
        return keepTransform({
          x1: snapValue(value.x1),
          y1: snapValue(value.y1),
          x2: snapValue(value.x2),
          y2: snapValue(value.y2),
        });
      }
      if (value.move_dx !== undefined && value.move_dy !== undefined) {
        return { move_dx: snapValue(value.move_dx), move_dy: snapValue(value.move_dy) };
      }
      return value;
    }

    function patchAnchor(value) {
      if (!value) return null;
      if (value.x !== undefined && value.y !== undefined) return { x: Number(value.x), y: Number(value.y) };
      if (value.cx !== undefined && value.cy !== undefined) return { x: Number(value.cx), y: Number(value.cy) };
      if (value.x1 !== undefined && value.y1 !== undefined) return { x: Number(value.x1), y: Number(value.y1) };
      if (Array.isArray(value.points) && value.points.length) return { x: Number(value.points[0][0]), y: Number(value.points[0][1]) };
      if (value.d !== undefined) {
        const nums = String(value.d).match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi);
        if (nums && nums.length >= 2) return { x: Number(nums[0]), y: Number(nums[1]) };
      }
      return null;
    }

    function movedPatchValueFromBefore(beforeValue, currentValue) {
      if (!beforeValue || !currentValue) return currentValue;
      if (!snapEnabled) return currentValue;
      const beforeAnchor = patchAnchor(beforeValue);
      const currentAnchor = patchAnchor(currentValue);
      if (!beforeAnchor || !currentAnchor) return currentValue;
      const dx = snapValue(currentAnchor.x - beforeAnchor.x);
      const dy = snapValue(currentAnchor.y - beforeAnchor.y);
      const out = JSON.parse(JSON.stringify(beforeValue));
      if (out.x !== undefined) out.x = beforeValue.x + dx;
      if (out.y !== undefined) out.y = beforeValue.y + dy;
      if (out.cx !== undefined) out.cx = beforeValue.cx + dx;
      if (out.cy !== undefined) out.cy = beforeValue.cy + dy;
      if (out.x1 !== undefined) out.x1 = beforeValue.x1 + dx;
      if (out.y1 !== undefined) out.y1 = beforeValue.y1 + dy;
      if (out.x2 !== undefined) out.x2 = beforeValue.x2 + dx;
      if (out.y2 !== undefined) out.y2 = beforeValue.y2 + dy;
      if (Array.isArray(out.points)) out.points = beforeValue.points.map(([x, y]) => [x + dx, y + dy]);
      if (out.d !== undefined) out.d = shiftPathD(beforeValue.d, dx, dy, false);
      if (beforeValue.transform) out.transform = shiftRotateTransform(beforeValue.transform, dx, dy, false);
      return out;
    }

    function fractionPartElements(prefix) {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return [];
      const parts = [];
      const whole = svg.querySelector(`[id^="${prefix}.whole."]`);
      const num = svg.querySelector(`[id^="${prefix}.num."]`);
      const den = svg.querySelector(`[id^="${prefix}.den."]`);
      const bar = svg.querySelector(`[id^="${prefix}.bar."]`);
      if (whole instanceof SVGElement) parts.push(whole);
      if (num instanceof SVGElement) parts.push(num);
      if (den instanceof SVGElement) parts.push(den);
      if (bar instanceof SVGElement) parts.push(bar);
      return parts;
    }

    function elementAnchor(el) {
      if (!el) return null;
      const tag = el.tagName.toLowerCase();
      if (tag === "text") return { x: Number(el.getAttribute("x") || 0), y: Number(el.getAttribute("y") || 0) };
      if (tag === "line") return { x: Number(el.getAttribute("x1") || 0), y: Number(el.getAttribute("y1") || 0) };
      if (tag === "rect") return { x: Number(el.getAttribute("x") || 0), y: Number(el.getAttribute("y") || 0) };
      if (tag === "image") return { x: Number(el.getAttribute("x") || 0), y: Number(el.getAttribute("y") || 0) };
      if (tag === "circle") return { x: Number(el.getAttribute("cx") || 0), y: Number(el.getAttribute("cy") || 0) };
      return null;
    }

    function fractionVisualDelta(prefix, startAnchor) {
      const elems = fractionPartElements(prefix);
      if (!elems.length || !startAnchor) return { dx: 0, dy: 0 };
      const now = elementAnchor(elems[0]);
      if (!now) return { dx: 0, dy: 0 };
      return { dx: now.x - startAnchor.x, dy: now.y - startAnchor.y };
    }

    function findElementBySlotId(slotId) {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const nodes = draggableSlotElements(svg);
      for (const node of nodes) {
        const grouped = slotIdFromElement(node);
        if (grouped === slotId) return node;
        const mapped = toDslSlotId(node.getAttribute("id"));
        if (mapped === slotId) return node;
      }
      return null;
    }

    function resizePatchForCanvas(svg, handle, startValue, startBox, nextBox) {
      const snap = (v) => (snapEnabled ? snapValue(v) : v);
      const changesWidth = handle.includes("e") || handle.includes("w");
      const changesHeight = handle.includes("n") || handle.includes("s");
      const width = Math.max(20, snap(changesWidth ? nextBox.width : startValue.width));
      const height = Math.max(20, snap(changesHeight ? nextBox.height : startValue.height));
      if (width === startValue.width && height === startValue.height) return null;
      svg.setAttribute("width", String(width));
      svg.setAttribute("height", String(height));
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      return { width, height };
    }

    function layoutRegionBySlotId(slotId) {
      const layoutText = document.getElementById("layoutView")?.value || "";
      if (!layoutText.trim()) return null;
      try {
        const layout = JSON.parse(layoutText);
        for (const region of layout.regions || []) {
          if (Array.isArray(region.slot_ids) && region.slot_ids.includes(slotId)) return region.id || null;
        }
      } catch (_) {
        return null;
      }
      return null;
    }

    function selectedLayerSlotIds() {
      const out = [];
      for (const item of selectedSlots.values()) {
        if (item.isCanvas) continue;
        if (Array.isArray(item.slotIds) && item.slotIds.length) {
          out.push(...item.slotIds);
        } else if (item.elements && item.elements.length) {
          for (const node of item.elements) {
            const slotId = slotIdFromElement(node);
            if (slotId) out.push(slotId);
          }
        } else if (item.slotId) {
          out.push(item.slotId);
        }
      }
      return Array.from(new Set(out));
    }

    function reorderLayerIds(order, selectedIds, mode) {
      const selected = selectedIds.filter((id) => order.includes(id));
      if (!selected.length) return order;
      const selectedSet = new Set(selected);
      const rest = order.filter((id) => !selectedSet.has(id));
      if (mode === "front") return [...rest, ...selected];
      if (mode === "back") return [...selected, ...rest];

      let next = [...order];
      if (mode === "forward") {
        for (let i = next.length - 2; i >= 0; i -= 1) {
          if (!selectedSet.has(next[i]) || selectedSet.has(next[i + 1])) continue;
          [next[i], next[i + 1]] = [next[i + 1], next[i]];
        }
      } else if (mode === "backward") {
        for (let i = 1; i < next.length; i += 1) {
          if (!selectedSet.has(next[i]) || selectedSet.has(next[i - 1])) continue;
          [next[i - 1], next[i]] = [next[i], next[i - 1]];
        }
      }
      return next;
    }

    async function layerSelected(mode) {
      const selectedIds = selectedLayerSlotIds();
      if (!selectedIds.length) throw new Error("레이어를 조정할 요소를 선택하세요.");
      const layoutText = document.getElementById("layoutView")?.value || "";
      if (!layoutText.trim()) throw new Error("layout 정보를 찾지 못했습니다. 먼저 build 하세요.");
      const layout = JSON.parse(layoutText);
      const patches = [];
      for (const region of layout.regions || []) {
        if (!region || !Array.isArray(region.slot_ids)) continue;
        const regionSelected = selectedIds.filter((id) => region.slot_ids.includes(id));
        if (!regionSelected.length) continue;
        const nextOrder = reorderLayerIds(region.slot_ids, regionSelected, mode);
        if (nextOrder.join("\u0001") === region.slot_ids.join("\u0001")) continue;
        region.slot_ids = nextOrder;
        patches.push({
          target: "__layer__",
          op: "layer",
          value: { region_id: region.id || "region.stem", slot_ids: nextOrder },
        });
      }
      if (!patches.length) {
        setStatus("레이어 순서를 바꿀 수 있는 선택이 없습니다.", false);
        return;
      }
      document.getElementById("layoutView").value = JSON.stringify(layout, null, 2);
      await commitPatches(patches, `레이어 조정 완료: ${mode}`, true);
    }

    function selectedCopyItems() {
      const seen = new Set();
      const out = [];
      for (const item of selectedSlots.values()) {
        const nodes = item.elements || [item.el];
        for (const node of nodes) {
          const slotId = slotIdFromElement(node);
          if (!slotId || seen.has(slotId)) continue;
          const value = readSlotPatchValue(node);
          if (!value) continue;
          const tag = node.tagName.toLowerCase();
          const kind = tag === "text" && node.getAttribute("data-slot-kind") === "text_box" ? "text_box" : tag;
          let bbox = null;
          try {
            bbox = visualSvgBox(node, node.ownerSVGElement);
          } catch (_) {
            bbox = null;
          }
          seen.add(slotId);
          out.push({
            sourceId: slotId,
            kind,
            regionId: layoutRegionBySlotId(slotId),
            content: JSON.parse(JSON.stringify(value)),
            bbox: bbox ? { x: bbox.x, y: bbox.y, width: bbox.width, height: bbox.height } : null,
          });
        }
      }
      return out;
    }

    function cloneSlotId(sourceId, suffix) {
      const fig = sourceId.match(/^slot\.figure\.([^.]+)\.(.+)$/);
      if (fig) return `slot.figure.${fig[1]}_${suffix}.${fig[2]}`;
      return `${sourceId}.${suffix}`;
    }

    function shiftedCopyContent(content, dx, dy) {
      const out = JSON.parse(JSON.stringify(content || {}));
      if (out.x !== undefined) out.x += dx;
      if (out.y !== undefined) out.y += dy;
      if (out.cx !== undefined) out.cx += dx;
      if (out.cy !== undefined) out.cy += dy;
      if (out.x1 !== undefined) out.x1 += dx;
      if (out.y1 !== undefined) out.y1 += dy;
      if (out.x2 !== undefined) out.x2 += dx;
      if (out.y2 !== undefined) out.y2 += dy;
      if (Array.isArray(out.points)) out.points = out.points.map(([x, y]) => [x + dx, y + dy]);
      if (out.d !== undefined) out.d = shiftPathD(out.d, dx, dy, false);
      return out;
    }

    function copyItemsBBox(items) {
      const boxes = (items || []).map((item) => item.bbox).filter(Boolean);
      if (!boxes.length) return null;
      const minX = Math.min(...boxes.map((box) => box.x));
      const minY = Math.min(...boxes.map((box) => box.y));
      const maxX = Math.max(...boxes.map((box) => box.x + box.width));
      const maxY = Math.max(...boxes.map((box) => box.y + box.height));
      return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
    }

    function fitPasteOffsetToCanvas(items, dx, dy) {
      const box = copyItemsBBox(items);
      const bounds = getSvgCanvasBounds();
      if (!box || !bounds) return { dx, dy };
      const minX = bounds.x;
      const minY = bounds.y;
      const maxX = bounds.x + bounds.width;
      const maxY = bounds.y + bounds.height;
      let nextDx = dx;
      let nextDy = dy;
      if (box.x + nextDx < minX) nextDx = minX - box.x;
      if (box.y + nextDy < minY) nextDy = minY - box.y;
      if (box.width <= bounds.width && box.x + box.width + nextDx > maxX) nextDx = maxX - (box.x + box.width);
      if (box.height <= bounds.height && box.y + box.height + nextDy > maxY) nextDy = maxY - (box.y + box.height);
      if (box.x + nextDx < minX) nextDx = minX - box.x;
      if (box.y + nextDy < minY) nextDy = minY - box.y;
      return { dx: nextDx, dy: nextDy };
    }

    function copySelectedSlots() {
      const items = selectedCopyItems();
      if (!items.length) throw new Error("복사할 요소를 먼저 선택하세요.");
      copyBuffer = { items };
      setStatus(`복사 완료: ${items.length}개`, true);
    }

    async function pasteCopiedSlots() {
      if (!copyBuffer || !copyBuffer.items || !copyBuffer.items.length) throw new Error("붙여넣을 복사본이 없습니다.");
      const existingIds = extractDslSlotIds();
      let suffix = "";
      let offset = 0;
      do {
        pasteSequence += 1;
        suffix = `copy${pasteSequence}`;
        offset = 15 * pasteSequence;
      } while (copyBuffer.items.some((item) => existingIds.has(cloneSlotId(item.sourceId, suffix))));
      const pasteOffset = fitPasteOffsetToCanvas(copyBuffer.items, offset, offset);
      const patches = copyBuffer.items.map((item) => ({
        target: cloneSlotId(item.sourceId, suffix),
        op: "add",
        value: {
          kind: item.kind,
          region_id: item.regionId,
          content: shiftedCopyContent(item.content, pasteOffset.dx, pasteOffset.dy),
        },
      }));
      await commitPatches(patches, `붙여넣기 완료: ${patches.length}개`);
      restoreSelection(patches.map((p) => p.target));
    }

    function pushHistory(before, after, label) {
      const patches = (after || []).map((s) => ({ target: s.slotId, op: "update", value: s.value }));
      executeEditorCommand(createLayoutPatchCommand({ description: label, patches }), getState());
      undoStack.push({ before, after, label });
      if (undoStack.length > 100) undoStack.shift();
      redoStack = [];
    }

    async function applyHistoryEntry(entry, useBefore) {
      const states = useBefore ? entry.before : entry.after;
      const patches = states.map((s) => ({ target: s.slotId, op: "update", value: s.value }));
      for (const s of states) {
        if (s.slotId === "__canvas__") {
          applyCanvasPatchValue(s.value);
          continue;
        }
        const el = findElementBySlotId(s.slotId);
        if (el) applyPatchValueToElement(el, s.value);
      }
      updateSelectionHandles();
      historyBusy = true;
      try {
        await commitPatches(patches, useBefore ? `Undo: ${entry.label}` : `Redo: ${entry.label}`);
      } finally {
        historyBusy = false;
      }
    }

    function queueKeyboardCommit(patches, label, beforeStates = null) {
      if (keyboardCommitTimer) clearTimeout(keyboardCommitTimer);
      keyboardCommitTimer = setTimeout(async () => {
        keyboardCommitTimer = null;
        try {
          const before = beforeStates || readSelectedStates();
          await commitPatches(patches, label, false);
          if (!historyBusy) {
            const after = readSelectedStates();
            if (before.length === after.length && after.length > 0) pushHistory(before, after, "키보드 이동");
          }
        } catch (e) {
          setStatus(String(e), false);
        }
      }, 220);
    }

    function beginResizeFromHandle(ev) {
      if (ev.button !== 0) return;
      const item = selectedResizableItem();
      if (!item) return;
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return;
      const box = itemBBox(item);
      if (!box) return;
      const svgClientRect = svg.getBoundingClientRect();
      const canvasScaleX = item.isCanvas && svgClientRect.width > 0 ? box.width / svgClientRect.width : 1;
      const canvasScaleY = item.isCanvas && svgClientRect.height > 0 ? box.height / svgClientRect.height : 1;
      const startValue = (item.isCharacterGroup || item.isLayoutGroup || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup)
        ? (item.elements || [])
            .map((el) => ({ el, slotId: slotIdFromElement(el), value: readSlotPatchValue(el) }))
            .filter((entry) => entry.slotId && entry.value)
        : item.isCanvas
          ? { width: box.width, height: box.height }
        : readSlotPatchValue(item.el);
      if (!startValue || (Array.isArray(startValue) && !startValue.length)) return;
      const handle = ev.currentTarget.getAttribute("data-handle") || "c";
      const startGlobalPoint = getSvgPoint(svg, ev.clientX, ev.clientY);
      const selectionRotation = selectionTransformForItem(item).rotation;
      resizeFrameRequested = false;
      pendingResizePoint = null;
      resizeState = {
        svg,
        item,
        handle,
        startPoint: pointInRotatedFrame(startGlobalPoint, selectionRotation),
        startGlobalPoint,
        selectionRotation,
        startClientX: ev.clientX,
        startClientY: ev.clientY,
        canvasScaleX,
        canvasScaleY,
        startBox: cloneBBox(box),
        startValue: (item.isCharacterGroup || item.isLayoutGroup || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup)
          ? startValue.map((entry) => ({ ...entry, value: JSON.parse(JSON.stringify(entry.value)) }))
          : JSON.parse(JSON.stringify(startValue)),
        lastValue: null,
        moved: false,
        pointerId: ev.pointerId,
        handleEl: ev.currentTarget,
      };
      canvasCapturePointer(ev.currentTarget, ev.pointerId);
      ev.preventDefault();
      ev.stopPropagation();
    }

    function updateResize(ev) {
      if (!resizeState) return;
      const rawPoint = resizeState.item.isCanvas ? null : getSvgPoint(resizeState.svg, ev.clientX, ev.clientY);
      const p = rawPoint ? pointInRotatedFrame(rawPoint, resizeState.selectionRotation) : null;
      const singleTag = resizeState.item.el ? resizeState.item.el.tagName.toLowerCase() : "";
      if (singleTag === "path" && String(resizeState.handle || "").startsWith("path:") && p) {
        const value = pathPointPatchFromHandle(resizeState.startValue, resizeState.handle, p);
        if (value) {
          applyPatchValueToElement(resizeState.item.el, value);
          resizeState.lastValue = value;
          resizeState.moved = true;
          updateSelectionHandles();
          setStatus(`곡선 점 조절 중: ${resizeState.item.slotId}${snapEnabled ? " (snap 5px)" : ""}`, true);
          return;
        }
      }
      if (singleTag === "line" && !resizeState.item.isCanvas && !resizeState.item.isFigureGroup && !resizeState.item.isPaperFoldGroup && !resizeState.item.isMeasurementGroup && !resizeState.item.isGraphPaperGroup && !resizeState.item.isLayoutGroup) {
        let value = null;
        if (resizeState.handle === "p1" || resizeState.handle === "p2") {
          value = linePatchFromEndpoint(resizeState.item.el, resizeState.handle, resizeState.startValue, p);
        } else if (resizeState.handle === "r") {
          value = linePatchFromRotation(resizeState.item.el, resizeState.startValue, resizeState.startPoint, p);
        }
        if (value) {
          resizeState.lastValue = value;
          resizeState.moved = true;
          updateSelectionHandles();
          setStatus(`선 조절 중: ${resizeState.item.slotId}${snapEnabled ? " (snap 5px)" : ""}`, true);
          return;
        }
      }
      if (resizeState.handle === "r" && !resizeState.item.isCanvas) {
        const value = (resizeState.item.isCharacterGroup || resizeState.item.isLayoutGroup || resizeState.item.isFigureGroup || resizeState.item.isPaperFoldGroup || resizeState.item.isMeasurementGroup || resizeState.item.isTableGroup || resizeState.item.isGraphPaperGroup)
          ? rotationValuesForGroup(resizeState.startValue, resizeState.startBox, resizeState.startGlobalPoint, rawPoint)
          : rotationValueFromPointer(resizeState.startValue, resizeState.startBox, resizeState.startGlobalPoint, rawPoint);
        if (Array.isArray(value)) {
          for (const entry of value) applyPatchValueToElement(entry.el, entry.value);
        } else {
          applyPatchValueToElement(resizeState.item.el, value);
        }
        resizeState.lastValue = value;
        resizeState.moved = true;
        updateSelectionHandles();
        setStatus(`회전 중: ${resizeState.item.slotId}`, true);
        return;
      }
      const dx = resizeState.item.isCanvas
        ? (ev.clientX - resizeState.startClientX) * resizeState.canvasScaleX
        : p.x - resizeState.startPoint.x;
      const dy = resizeState.item.isCanvas
        ? (ev.clientY - resizeState.startClientY) * resizeState.canvasScaleY
        : p.y - resizeState.startPoint.y;
      if (resizeState.item.isTableGroup && String(resizeState.handle || "").startsWith("table-")) {
        const value = tableDividerValuesFromDrag(resizeState, dx, dy);
        if (!value) return;
        resizeState.lastValue = value;
        resizeState.moved = true;
        updateSelectionHandles();
        setStatus(`표 ${resizeState.handle.includes("table-v:") ? "열" : "행"} 조절 중: ${resizeState.item.slotId}${snapEnabled ? " (snap 5px)" : ""}`, true);
        return;
      }
      const nextBox = resizeState.item.isCanvas
        ? adjustedCanvasBox(resizeState.startBox, resizeState.handle, dx, dy)
        : adjustedBBox(resizeState.startBox, resizeState.handle, dx, dy);
      const value = resizeState.item.isGraphPaperGroup
        ? resizeGraphPaperGroup(resizeState, nextBox)
        : (resizeState.item.isCharacterGroup || resizeState.item.isLayoutGroup || resizeState.item.isFigureGroup || resizeState.item.isPaperFoldGroup || resizeState.item.isMeasurementGroup || resizeState.item.isTableGroup)
          ? resizeFigureGroup(resizeState, nextBox)
        : resizeState.item.isCanvas
          ? resizePatchForCanvas(resizeState.svg, resizeState.handle, resizeState.startValue, resizeState.startBox, nextBox)
        : resizePatchForElement(
            resizeState.item.el,
            resizeState.handle,
            resizeState.startValue,
            resizeState.startBox,
            nextBox
          );
      if (!value) return;
      if (!Array.isArray(value) && resizeState.startValue && resizeState.startValue.transform && value.transform === undefined) {
        value.transform = resizeState.startValue.transform;
      }
      if (Array.isArray(value)) {
        for (const entry of value) {
          const startEntry = (resizeState.startValue || []).find((s) => s.slotId === entry.slotId);
          if (startEntry && startEntry.value && startEntry.value.transform && entry.value.transform === undefined) {
            entry.value.transform = startEntry.value.transform;
          }
        }
      }
      resizeState.lastValue = value;
      resizeState.moved = true;
      updateSelectionHandles();
      setStatus(`크기 조절 중: ${resizeState.item.slotId}${snapEnabled ? " (snap 5px)" : ""}`, true);
    }

    function scheduleResizeUpdate(ev) {
      pendingResizePoint = { clientX: ev.clientX, clientY: ev.clientY };
      if (resizeFrameRequested) return;
      resizeFrameRequested = true;
      requestAnimationFrame(() => {
        resizeFrameRequested = false;
        if (!resizeState || !pendingResizePoint) return;
        const point = pendingResizePoint;
        pendingResizePoint = null;
        updateResize(point);
      });
    }

    function flushResizeUpdate() {
      if (!resizeState || !pendingResizePoint) return;
      const point = pendingResizePoint;
      pendingResizePoint = null;
      resizeFrameRequested = false;
      updateResize(point);
    }

    async function endResize(ev) {
      if (!resizeState) return;
      flushResizeUpdate();
      const local = resizeState;
      resizeState = null;
      pendingResizePoint = null;
      resizeFrameRequested = false;
      canvasReleasePointerCapture(local.handleEl, local.pointerId);
      if (!local.moved || !local.lastValue) {
        updateSelectionHandles();
        return;
      }
      if (local.item.isCharacterGroup || local.item.isLayoutGroup || local.item.isFigureGroup || local.item.isPaperFoldGroup || local.item.isMeasurementGroup || local.item.isTableGroup || local.item.isGraphPaperGroup) {
        const before = [];
        const after = [];
        const patches = [];
        for (const entry of local.startValue || []) {
          before.push({ slotId: entry.slotId, value: JSON.parse(JSON.stringify(entry.value)) });
        }
        for (const entry of local.lastValue || []) {
          const value = snapPatchValue(entry.value);
          if (!entry.slotId || !value) continue;
          applyPatchValueToElement(entry.el, value);
          after.push({ slotId: entry.slotId, value: JSON.parse(JSON.stringify(value)) });
          patches.push({ target: entry.slotId, op: "update", value });
        }
        updateSelectionHandles();
        try {
          await commitPatches(patches, `크기 조절 저장 완료: ${local.item.slotId}`);
          if (!historyBusy && before.length === after.length && before.length > 0) pushHistory(before, after, "크기 조절");
        } catch (e) {
          setStatus(String(e), false);
        }
        return;
      }
      if (local.item.isCanvas) {
        const value = local.lastValue;
        updateSelectionHandles();
        const before = [{ slotId: "__canvas__", value: local.startValue }];
        const after = [{ slotId: "__canvas__", value: JSON.parse(JSON.stringify(value)) }];
        try {
          await commitPatches([{ target: "__canvas__", op: "update", value }], "캔버스 크기 저장 완료");
          selectCanvas();
          if (!historyBusy) pushHistory(before, after, "캔버스 크기");
        } catch (e) {
          setStatus(String(e), false);
        }
        return;
      }
      const value = snapPatchValue(local.lastValue);
      applyPatchValueToElement(local.item.el, value);
      updateSelectionHandles();
      const before = [{ slotId: local.item.slotId, value: local.startValue }];
      const after = [{ slotId: local.item.slotId, value: JSON.parse(JSON.stringify(value)) }];
      try {
        const targets = local.item.slotIds || [local.item.slotId];
        await commitPatches(targets.map((target) => ({ target, op: "update", value })), `크기 조절 저장 완료: ${local.item.slotId}`);
        if (!historyBusy) pushHistory(before, after, "크기 조절");
      } catch (e) {
        setStatus(String(e), false);
      }
    }

    function bindSlotInteractions() {
      const container = document.getElementById("svgPreview");
      const svg = container.querySelector("svg");
      if (!svg) return;
      if (svg.dataset.dragBound === "1") return;
      svg.dataset.dragBound = "1";

      const slotElements = draggableSlotElements(svg);
      function beginSlotPointerDown(el, ev) {
        if (ev.button !== 0) return false;
        if (!matchesPickMode(el)) return false;
        const rawId = el.getAttribute("id");
        const fracInfo = parseFractionPartId(rawId);
        const resolvedSlotIds = fracInfo ? [fracInfo.prefix] : slotIdsFromElement(el);
        const slotId = resolvedSlotIds[0] || rawId;
        if (!slotId) {
          setStatus(`드래그 불가 요소: ${el.getAttribute("id") || "(unknown id)"}`, false);
          return false;
        }
        const appendSelection = ev.shiftKey || ev.ctrlKey || ev.metaKey;
        const selectionKey = selectableGroupBaseFromSlotId(slotId) || slotId;
        const existingSelection = selectedSlots.get(selectionKey);
        const keepGroupSelection = !appendSelection && existingSelection && existingSelection.el === el;
        if (!keepGroupSelection) setSelectedElement(el, slotId, appendSelection);
        const selected = selectedSlots.get(selectionKey);
        if (selected && selected.isTableGroup) {
          const cell = tableCellAtPoint(svg, selected, ev.clientX, ev.clientY);
          if (cell) {
            setSelectedTableCell(selected, cell, appendSelection);
            updateSelectionHandles();
            setStatus(`표 셀 선택: ${cell.row + 1}행 ${cell.col + 1}열`, true);
          }
        } else {
          selectedTableCells = [];
        }
        if (selected && !selected.isCharacterGroup && !selected.isLayoutGroup && !selected.isFigureGroup && !selected.isPaperFoldGroup && !selected.isMeasurementGroup && !selected.isTableGroup && !selected.isGraphPaperGroup) selected.slotIds = resolvedSlotIds;
        const start = getSvgPoint(svg, ev.clientX, ev.clientY);
        const dragSnapshot = canvasCreateSlotDragSnapshot(selectedSlots, { slotIdFromElement, readSlotPatchValue, elementAnchor });
        dragState = {
          problemId: currentProblemId,
          svg,
          slotId: selectionKey,
          start,
          moved: false,
          beforeMap: dragSnapshot.beforeMap,
          captureEl: el,
          pointerId: ev.pointerId,
          totalDx: 0,
          totalDy: 0,
          fractionStartAnchors: dragSnapshot.fractionStartAnchors,
        };
        canvasCapturePointer(el, ev.pointerId);
        ev.preventDefault();
        return true;
      }

      const hitProxyHandlers = {
        onPointerDown(el, ev) {
          const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY);
          if (beginSlotPointerDown(matched || el, ev)) ev.stopPropagation();
        },
        onDoubleClick(el, ev) {
          const editTarget = matchingTextSlotElementAtPoint(svg, ev.clientX, ev.clientY) || el;
          if (editTarget.tagName.toLowerCase() !== "text") return;
          if (!matchesPickMode(editTarget)) return;
          const resolvedSlotIds = toDslSlotIds(editTarget.getAttribute("id"));
          if (resolvedSlotIds.length !== 1) return;
          beginInlineTextEdit(editTarget, resolvedSlotIds[0], ev);
        },
      };

      function addStrokeHitProxy(el) {
        return canvasAppendStrokeHitProxy(svg, el, hitProxyHandlers);
      }

      function addHitProxies() {
        // Delegated pointer handling plus bbox fallback below covers thin lines
        // and text boxes without doubling the SVG DOM with per-slot proxies.
        return;
        for (const el of slotElements) {
          if (addStrokeHitProxy(el)) continue;
          if (el.tagName.toLowerCase() !== "text") continue;
          if (el.getAttribute("data-slot-kind") !== "text_box") continue;
          const bb = elementHitBox(el);
          if (!bb) continue;
          canvasAppendTextHitProxy(svg, el, bb, hitProxyHandlers);
        }
      }

      addHitProxies();

      canvasBindCanvasSlotInteractionEvents(svg, container, {
        onPointerDownCapture(ev) {
        if (pendingDrawShape && beginShapeDrawOnCanvas(svg, ev)) return;
        const target = ev.target;
        if (target instanceof SVGElement && target.classList.contains("selection-handle")) return;
        if (isEmptySvgClickTarget(svg, target)) {
          const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY);
          if (matched && beginSlotPointerDown(matched, ev)) ev.stopPropagation();
          return;
        }
        if (target instanceof SVGElement && target.__slotProxyTarget) {
          const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY);
          if (beginSlotPointerDown(matched || target.__slotProxyTarget, ev)) ev.stopPropagation();
          return;
        }
        const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY);
        if (matched && beginSlotPointerDown(matched, ev)) ev.stopPropagation();
      },

        onContextMenu(ev) {
        const target = ev.target;
        const proxyTarget = target instanceof SVGElement ? target.__slotProxyTarget : null;
        const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY) || proxyTarget;
        if (matched && openShapeFormatMenu(ev, matched)) return;
        hideShapeFormatMenu();
      },

        onDoubleClick(ev) {
        const target = ev.target;
        if (!(target instanceof SVGElement)) return;
        const el = matchingTextSlotElementAtPoint(svg, ev.clientX, ev.clientY) || findDraggableSlotAncestor(target);
        if (!el || el.tagName.toLowerCase() !== "text") return;
        if (!matchesPickMode(el)) return;
        const rawId = el.getAttribute("id");
        const resolvedSlotIds = toDslSlotIds(rawId);
        if (resolvedSlotIds.length !== 1) return;
        beginInlineTextEdit(el, resolvedSlotIds[0], ev);
      },

        onPointerDown(ev) {
        if (pendingDrawShape) return;
        const target = ev.target;
        if (!(target instanceof SVGElement)) return;
        const slotTarget = findDraggableSlotAncestor(target);
        if (slotTarget && !matchesPickMode(slotTarget)) {
          const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY);
          if (matched && beginSlotPointerDown(matched, ev)) return;
        }
        if (!slotTarget) {
          const matched = matchingSlotElementAtPoint(svg, ev.clientX, ev.clientY);
          if (matched && beginSlotPointerDown(matched, ev)) return;
          clearSelection();
          if (ev.button === 0) beginMarquee(svg, ev);
        }
      },

        onContainerPointerDown(ev) {
          if (ev.button !== 0) return;
          if (ev.target === container) clearSelection();
        },

        onPointerMove(ev) {
        if (drawState) {
          updateShapeDraw(ev);
          return;
        }
        if (resizeState) {
          scheduleResizeUpdate(ev);
          return;
        }
        if (marqueeState) {
          updateMarquee(ev);
          return;
        }
        if (!dragState) return;
        const p = getSvgPoint(svg, ev.clientX, ev.clientY);
        dragFrameRequested = canvasScheduleDragFrame(dragState, p, dragFrameRequested, ({ dx: pdx, dy: pdy }) => {
          dragFrameRequested = false;
          if (!dragState) return;
          if (pdx === 0 && pdy === 0) return;
          const lastValue = applyDragDeltaToSelection(pdx, pdy);
          if (!lastValue) return;
          markDragMoveApplied(pdx, pdy);
        });
      },

        async onPointerUp(ev) {
        if (drawState) {
          await endShapeDraw(ev);
          return;
        }
        if (resizeState) {
          await endResize(ev);
          return;
        }
        if (marqueeState) {
          endMarquee(ev);
          return;
        }
        if (!dragState) return;
        const local = dragState;
        dragState = null;
        canvasReleasePointerCapture(local.captureEl, local.pointerId);
        if (!local.moved) return;
        updateSelectionHandles();
        const before = [];
        const { patches, after } = buildDragEndPatchSet(local);
        if (!patches.length) return;
        setStatus(`드래그 저장 중: ${patches.length}개`, true);
        queueDragCommit(async () => {
          try {
            await commitPatches(patches, `드래그 저장 완료: ${patches.length}개`, false, local.problemId, false);
            if (!historyBusy) {
              for (const pch of patches) {
                const found = local.beforeMap.get(pch.target);
                if (found) before.push({ slotId: pch.target, value: found });
              }
              if (before.length === after.length && before.length > 0) {
                pushHistory(before, after, "드래그 이동");
              }
            }
          } catch (e) {
            setStatus(String(e), false);
          }
        });
      },
      });
    }

    function selectedItemsWithValues() {
      const items = [];
      for (const item of selectedSlots.values()) {
        if (item.isCanvas) continue;
        const value = (item.isFraction || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup || item.isCharacterGroup || item.isLayoutGroup) ? { move_dx: 0, move_dy: 0 } : readSlotPatchValue(item.el);
        if (!value) continue;
        let bbox = null;
        try {
          if (item.isFraction || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup || item.isGeneratedGroup || item.isCharacterGroup || item.isLayoutGroup) {
            bbox = itemBBox(item);
          } else {
            bbox = item.el.getBBox();
          }
        } catch (_) {
          bbox = null;
        }
        items.push({
          slotId: item.slotId,
          slotIds: item.slotIds || [item.slotId],
          el: item.el,
          value,
          bbox,
          isFraction: !!item.isFraction,
          isFigureGroup: !!item.isFigureGroup,
          isPaperFoldGroup: !!item.isPaperFoldGroup,
          isMeasurementGroup: !!item.isMeasurementGroup,
          isTableGroup: !!item.isTableGroup,
          isGraphPaperGroup: !!item.isGraphPaperGroup,
          isGeneratedGroup: !!item.isGeneratedGroup,
          isCharacterGroup: !!item.isCharacterGroup,
          isLayoutGroup: !!item.isLayoutGroup,
          elements: item.elements || [item.el],
        });
      }
      return items;
    }

    function getSvgCanvasBounds() {
      const svg = document.getElementById("svgPreview").querySelector("svg");
      if (!svg) return null;
      const vb = svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal : null;
      if (vb && vb.width > 0 && vb.height > 0) {
        return { x: vb.x, y: vb.y, width: vb.width, height: vb.height };
      }
      const w = Number(svg.getAttribute("width") || 0);
      const h = Number(svg.getAttribute("height") || 0);
      if (w > 0 && h > 0) return { x: 0, y: 0, width: w, height: h };
      return null;
    }

    async function alignSelected(mode) {
      const items = selectedItemsWithValues();
      if (items.length < 2) {
        setStatus("정렬은 2개 이상 선택 시 사용하세요.", false);
        return;
      }
      const itemsWithBox = items.filter((i) => i.bbox);
      if (itemsWithBox.length < 2) {
        setStatus("정렬용 bbox 정보를 가져오지 못했습니다.", false);
        return;
      }
      const before = readSelectedStates();
      const bounds = getSvgCanvasBounds();
      const lefts = itemsWithBox.map((i) => i.bbox.x);
      const rights = itemsWithBox.map((i) => i.bbox.x + i.bbox.width);
      const tops = itemsWithBox.map((i) => i.bbox.y);
      const bottoms = itemsWithBox.map((i) => i.bbox.y + i.bbox.height);
      const centersX = itemsWithBox.map((i) => i.bbox.x + i.bbox.width / 2);
      const centersY = itemsWithBox.map((i) => i.bbox.y + i.bbox.height / 2);

      let targetMetric = 0;
      if (mode === "left") targetMetric = Math.min(...lefts);
      if (mode === "center") targetMetric = centersX.reduce((s, v) => s + v, 0) / centersX.length;
      if (mode === "right") targetMetric = Math.max(...rights);
      if (mode === "top") targetMetric = Math.min(...tops);
      if (mode === "middle") targetMetric = centersY.reduce((s, v) => s + v, 0) / centersY.length;
      if (mode === "bottom") targetMetric = Math.max(...bottoms);

      const patches = [];
      for (const item of itemsWithBox) {
        const b = item.bbox;
        let dx = 0;
        let dy = 0;
        if (mode === "left") dx = targetMetric - b.x;
        if (mode === "center") dx = targetMetric - (b.x + b.width / 2);
        if (mode === "right") dx = targetMetric - (b.x + b.width);
        if (mode === "top") dy = targetMetric - b.y;
        if (mode === "middle") dy = targetMetric - (b.y + b.height / 2);
        if (mode === "bottom") dy = targetMetric - (b.y + b.height);

        if (bounds) {
          const minDx = bounds.x - b.x;
          const maxDx = bounds.x + bounds.width - (b.x + b.width);
          const minDy = bounds.y - b.y;
          const maxDy = bounds.y + bounds.height - (b.y + b.height);
          dx = Math.max(minDx, Math.min(maxDx, dx));
          dy = Math.max(minDy, Math.min(maxDy, dy));
        }

        if (item.isFraction) {
          for (const node of item.elements) applyElementDelta(node, dx, dy, false);
          const snappedMove = snapPatchValue({ move_dx: dx, move_dy: dy });
          const fixDx = snappedMove.move_dx - dx;
          const fixDy = snappedMove.move_dy - dy;
          if (fixDx !== 0 || fixDy !== 0) {
            for (const node of item.elements) applyElementDelta(node, fixDx, fixDy, false);
          }
          patches.push({ target: item.slotId, op: "update", value: snappedMove });
        } else if (item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isGeneratedGroup) {
          for (const node of item.elements) applyElementDelta(node, dx, dy, false);
          const snappedMove = snapPatchValue({ move_dx: dx, move_dy: dy });
          const fixDx = snappedMove.move_dx - dx;
          const fixDy = snappedMove.move_dy - dy;
          if (fixDx !== 0 || fixDy !== 0) {
            for (const node of item.elements) applyElementDelta(node, fixDx, fixDy, false);
          }
          patches.push({ target: item.slotId, op: "update", value: snappedMove });
        } else if (item.isTableGroup || item.isGraphPaperGroup || item.isLayoutGroup || item.isCharacterGroup) {
          for (const node of item.elements) applyElementDelta(node, dx, dy, true);
          for (const node of item.elements) {
            const slotId = slotIdFromElement(node);
            const value = readSlotPatchValue(node);
            if (slotId && value) patches.push({ target: slotId, op: "update", value });
          }
        } else {
          const patchValue = applyElementDelta(item.el, dx, dy, true);
          if (!patchValue) continue;
          for (const target of item.slotIds || [item.slotId]) {
            patches.push({ target, op: "update", value: patchValue });
          }
        }
      }
      if (!patches.length) return;
      await commitPatches(patches, `정렬 저장 완료: ${mode}`);
      updateSelectionHandles();
      const after = readSelectedStates();
      if (!historyBusy && before.length === after.length) pushHistory(before, after, `정렬(${mode})`);
    }

    async function undoAction() {
      if (!undoStack.length) return setStatus("Undo 이력이 없습니다.", false);
      const entry = undoStack.pop();
      await applyHistoryEntry(entry, true);
      redoStack.push(entry);
    }

    async function redoAction() {
      if (!redoStack.length) return setStatus("Redo 이력이 없습니다.", false);
      const entry = redoStack.pop();
      await applyHistoryEntry(entry, false);
      undoStack.push(entry);
    }

    function renderLog(stdout, stderr) {
      document.getElementById("buildLog").textContent = [stdout || "", stderr || ""].join("\n").trim();
    }

    async function loadProblems() {
      const tree = document.getElementById("problemTree");
      const count = document.getElementById("problemTreeCount");
      if (tree) tree.innerHTML = "<em>문제 목록을 불러오는 중입니다.</em>";
      if (count) count.textContent = "";
      const data = await withApiErrors(() => requestProblemList());
      knownProblems = data.problems || [];
      const options = document.getElementById("problemOptions");
      options.innerHTML = "";
      for (const p of knownProblems) {
        const option = document.createElement("option");
        option.value = p.problem_id;
        options.appendChild(option);
      }
      renderProblemTree();
      if (!currentProblemId && knownProblems.length > 0) {
        document.getElementById("problemInput").value = knownProblems[0].problem_id;
      }
      setStatus(`문제 목록 로드 완료: ${knownProblems.length}개`, true);
    }

    function filteredProblemIds() {
      const filter = (document.getElementById("problemFilterInput")?.value || "").trim().toLocaleLowerCase("ko");
      const ids = knownProblems.map((p) => p.problem_id);
      if (!filter) return ids;
      return ids.filter((id) => id.toLocaleLowerCase("ko").includes(filter));
    }

    function buildTree(problemIds) {
      const root = {};
      for (const id of problemIds) {
        const parts = id.split("/");
        let node = root;
        for (let i = 0; i < parts.length; i += 1) {
          const part = parts[i];
          if (!node[part]) node[part] = { __children: {}, __leaf: false, __id: null };
          if (i === parts.length - 1) {
            node[part].__leaf = true;
            node[part].__id = id;
          }
          node = node[part].__children;
        }
      }
      return root;
    }

    function renderTreeNode(container, nodeObj, parentPath = "", forceOpen = false) {
      const ul = document.createElement("ul");
      const keys = Object.keys(nodeObj).sort((a, b) => a.localeCompare(b, "ko"));
      for (const key of keys) {
        const meta = nodeObj[key];
        const li = document.createElement("li");
        const childKeys = Object.keys(meta.__children);
        if (childKeys.length > 0) {
          const folderPath = parentPath ? `${parentPath}/${key}` : key;
          const isOpen = forceOpen || !collapsedProblemFolders.has(folderPath);
          const folder = document.createElement("button");
          folder.className = "folder";
          folder.classList.toggle("open", isOpen);
          folder.textContent = key;
          folder.onclick = () => {
            if (collapsedProblemFolders.has(folderPath)) collapsedProblemFolders.delete(folderPath);
            else collapsedProblemFolders.add(folderPath);
            renderProblemTree();
          };
          li.appendChild(folder);
          const childContainer = document.createElement("div");
          childContainer.className = "children";
          childContainer.classList.toggle("collapsed", !isOpen);
          renderTreeNode(childContainer, meta.__children, folderPath, forceOpen);
          li.appendChild(childContainer);
        } else if (meta.__leaf) {
          const btn = document.createElement("button");
          btn.className = "file-btn";
          btn.classList.toggle("active", meta.__id === currentProblemId);
          btn.textContent = key;
          btn.onclick = async () => {
            document.getElementById("problemInput").value = meta.__id;
            try { await selectProblem(meta.__id); } catch (e) { setStatus(String(e), false); }
          };
          li.appendChild(btn);
        }
        ul.appendChild(li);
      }
      container.appendChild(ul);
    }

    function renderProblemTree() {
      const tree = document.getElementById("problemTree");
      const count = document.getElementById("problemTreeCount");
      const problemIds = filteredProblemIds();
      const filterActive = (document.getElementById("problemFilterInput")?.value || "").trim().length > 0;
      tree.innerHTML = "";
      if (count) count.textContent = `${problemIds.length} / ${knownProblems.length}개`;
      if (!problemIds.length) {
        tree.innerHTML = "<em>문제가 없습니다.</em>";
        return;
      }
      const root = buildTree(problemIds);
      renderTreeNode(tree, root, "", filterActive);
    }

    async function selectProblem(problemId) {
      const trimmed = (problemId || "").trim();
      if (!trimmed) throw new Error("problem_id를 입력하세요.");
      await flushPendingPatchSaves();
      currentProblemId = trimmed;
      resetState();
      clearCommandHistory();
      setState({ problemId: trimmed, loading: true, error: null });
      document.getElementById("selectedProblem").textContent = trimmed;
      const detail = await withApiErrors(() => requestProblemDetail(trimmed));
      document.getElementById("dslEditor").value = detail.dsl || "";
      setState({ dsl: detail.dsl || "", artifacts: detail, loading: false, dirty: false });
      renderArtifacts(detail);
      renderLog("", "");
      renderProblemTree();
      setStatus(`불러오기 완료: ${trimmed}`, true);
    }

    async function saveDsl() {
      if (!currentProblemId) throw new Error("먼저 문제를 선택하세요.");
      const dsl = document.getElementById("dslEditor").value;
      setState({ saving: true, saveStatus: "saving", error: null });
      await withApiErrors(() => requestSaveDsl(currentProblemId, dsl)).then((data) => {
        if (typeof data.dsl === "string") document.getElementById("dslEditor").value = data.dsl;
      });
      setState({ dsl: document.getElementById("dslEditor").value, saving: false, saveStatus: "saved", dirty: false });
      setStatus("DSL 저장 완료", true);
    }

    async function formatDsl() {
      if (!currentProblemId) throw new Error("먼저 문제를 선택하세요.");
      await saveDsl();
      const data = await withApiErrors(() => requestFormatDsl(currentProblemId));
      document.getElementById("dslEditor").value = data.dsl || "";
      setStatus("DSL 정리 완료", true);
    }

    async function buildProblem() {
      if (!currentProblemId) throw new Error("먼저 문제를 선택하세요.");
      await flushPendingPatchSaves();
      setState({ building: true, buildStatus: "building", error: null });
      const data = await withApiErrors(() => requestBuildProblem(currentProblemId));
      renderArtifacts(data.artifacts || null);
      setState({ artifacts: data.artifacts || null, building: false, buildStatus: "built" });
      renderLog(data.stdout, data.stderr);
      setStatus("빌드 완료", true);
    }

    function readPatchPayload() {
      const target = document.getElementById("slotId").value.trim();
      if (!target) throw new Error("slot id를 입력하세요.");
      const value = JSON.parse(document.getElementById("patchJson").value);
      return { patches: [{ target, op: "update", value }] };
    }

    async function patchOnly() {
      if (!currentProblemId) throw new Error("먼저 문제를 선택하세요.");
      const payload = readPatchPayload();
      const data = await withApiErrors(() => applyLayoutPatches(currentProblemId, payload.patches));
      document.getElementById("dslEditor").value = data.dsl || "";
      setStatus("레이아웃 패치 완료", true);
    }

    async function patchAndBuild() {
      if (!currentProblemId) throw new Error("먼저 문제를 선택하세요.");
      const payload = readPatchPayload();
      const data = await withApiErrors(() => applyLayoutPatchesAndBuild(currentProblemId, payload.patches));
      document.getElementById("dslEditor").value = data.dsl || "";
      renderArtifacts(data.artifacts || null);
      renderLog(data.build?.stdout || "", data.build?.stderr || "");
      setStatus("패치 + 빌드 완료", true);
    }

    async function deleteSelectedSlots() {
      if (!selectedSlots.size) throw new Error("삭제할 요소를 먼저 선택하세요.");
      const ids = [];
      const nodesToRemove = [];
      for (const item of selectedSlots.values()) {
        if (item.isCanvas) continue;
        if (item.elements && item.elements.length) {
          for (const node of item.elements) {
            const slotId = slotIdFromElement(node);
            if (slotId) ids.push(slotId);
            nodesToRemove.push(node);
          }
          continue;
        }
        for (const slotId of item.slotIds || [item.slotId]) {
          if (slotId) ids.push(slotId);
        }
        if (item.el) nodesToRemove.push(item.el);
      }
      const uniqueSlotIds = Array.from(new Set(ids));
      if (!uniqueSlotIds.length) throw new Error("캔버스는 삭제할 수 없습니다.");
      const patches = uniqueSlotIds.map((slotId) => ({ target: slotId, op: "delete" }));
      for (const node of Array.from(new Set(nodesToRemove))) {
        if (node && node.parentNode) node.parentNode.removeChild(node);
      }
      clearSelection();
      await commitPatches(patches, `요소 삭제 완료: ${patches.length}개`, false, currentProblemId, false);
    }

    document.getElementById("openBtn").onclick = async () => {
      try { await selectProblem(document.getElementById("problemInput").value); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("refreshListBtn").onclick = async () => {
      try { await loadProblems(); setStatus("문제 목록 갱신 완료", true); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("problemFilterInput").addEventListener("input", () => renderProblemTree());
    document.getElementById("reloadBtn").onclick = async () => {
      try { await selectProblem(currentProblemId); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("saveBtn").onclick = async () => {
      try { await saveDsl(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("formatDslBtn").onclick = async () => {
      try { await formatDsl(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("buildBtn").onclick = async () => {
      try { await buildProblem(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("insertTextBoxBtn").onclick = async () => {
      try { await insertTextBox(); }
      catch (e) { setStatus(String(e), false); }
    };
    function openTableDialog() {
      const dialog = document.getElementById("tableInsertDialog");
      if (!dialog) return;
      document.getElementById("tableColsInput").value = "5";
      document.getElementById("tableRowsInput").value = "2";
      dialog.hidden = false;
      setTimeout(() => document.getElementById("tableColsInput")?.focus(), 0);
    }
    function closeTableDialog() {
      const dialog = document.getElementById("tableInsertDialog");
      if (dialog) dialog.hidden = true;
    }
    async function confirmTableDialog() {
      const cols = Math.max(1, Math.min(20, Number(document.getElementById("tableColsInput")?.value || 5)));
      const rows = Math.max(1, Math.min(20, Number(document.getElementById("tableRowsInput")?.value || 2)));
      document.getElementById("tableColsInput").value = String(cols);
      document.getElementById("tableRowsInput").value = String(rows);
      await insertTable(rows, cols);
      closeTableDialog();
    }
    function openGraphPaperDialog() {
      const dialog = document.getElementById("graphPaperInsertDialog");
      if (!dialog) return;
      document.getElementById("graphPaperColsInput").value = "10";
      document.getElementById("graphPaperRowsInput").value = "8";
      dialog.hidden = false;
      setTimeout(() => document.getElementById("graphPaperColsInput")?.focus(), 0);
    }
    function closeGraphPaperDialog() {
      const dialog = document.getElementById("graphPaperInsertDialog");
      if (dialog) dialog.hidden = true;
    }
    async function confirmGraphPaperDialog() {
      const cols = Math.max(1, Math.min(40, Number(document.getElementById("graphPaperColsInput")?.value || 10)));
      const rows = Math.max(1, Math.min(40, Number(document.getElementById("graphPaperRowsInput")?.value || 8)));
      document.getElementById("graphPaperColsInput").value = String(cols);
      document.getElementById("graphPaperRowsInput").value = String(rows);
      await insertGraphPaper(rows, cols);
      closeGraphPaperDialog();
    }
    function openBarModelDialog() {
      const dialog = document.getElementById("barModelInsertDialog");
      if (!dialog) return;
      document.getElementById("barModelBarsInput").value = "2";
      document.getElementById("barModelCellsInput").value = "3";
      document.getElementById("barModelShadedInput").value = "2,2";
      document.getElementById("barModelFillInput").value = "#f3d7ea";
      document.getElementById("barModelStrokeInput").value = "#666666";
      document.getElementById("barModelDashedInput").checked = true;
      dialog.hidden = false;
      setTimeout(() => document.getElementById("barModelBarsInput")?.focus(), 0);
    }
    function closeBarModelDialog() {
      const dialog = document.getElementById("barModelInsertDialog");
      if (dialog) dialog.hidden = true;
    }
    async function confirmBarModelDialog() {
      const bars = clampInt(document.getElementById("barModelBarsInput")?.value || 2, 1, 8, 2);
      const cells = clampInt(document.getElementById("barModelCellsInput")?.value || 3, 1, 20, 3);
      document.getElementById("barModelBarsInput").value = String(bars);
      document.getElementById("barModelCellsInput").value = String(cells);
      await insertBarModel({
        bars,
        cells,
        shadedCounts: document.getElementById("barModelShadedInput")?.value,
        fillColors: document.getElementById("barModelFillInput")?.value,
        stroke: document.getElementById("barModelStrokeInput")?.value,
        dashed: Boolean(document.getElementById("barModelDashedInput")?.checked),
      });
      closeBarModelDialog();
    }
    function openTickBarDialog() {
      const dialog = document.getElementById("tickBarInsertDialog");
      if (!dialog) return;
      document.getElementById("tickBarRowsInput").value = "2";
      document.getElementById("tickBarTotalInput").value = "14";
      document.getElementById("tickBarFilledInput").value = "9,10";
      document.getElementById("tickBarMajorInput").value = "7";
      document.getElementById("tickBarLabelsInput").value = "";
      document.getElementById("tickBarUnitInput").value = "m";
      document.getElementById("tickBarScaleLabelsInput").checked = true;
      document.getElementById("tickBarFractionLabelInput").checked = true;
      document.getElementById("tickBarAxisColorInput").value = "#111111";
      document.getElementById("tickBarFillColorInput").value = "#2563eb";
      dialog.hidden = false;
      setTimeout(() => document.getElementById("tickBarRowsInput")?.focus(), 0);
    }
    function closeTickBarDialog() {
      const dialog = document.getElementById("tickBarInsertDialog");
      if (dialog) dialog.hidden = true;
    }
    async function confirmTickBarDialog() {
      const rows = clampInt(document.getElementById("tickBarRowsInput")?.value || 2, 1, 8, 2);
      const totalTicks = clampInt(document.getElementById("tickBarTotalInput")?.value || 14, 1, 40, 14);
      const majorEvery = clampInt(document.getElementById("tickBarMajorInput")?.value || 7, 0, totalTicks, 7);
      document.getElementById("tickBarRowsInput").value = String(rows);
      document.getElementById("tickBarTotalInput").value = String(totalTicks);
      document.getElementById("tickBarMajorInput").value = String(majorEvery);
      await insertTickBar({
        rows,
        totalTicks,
        majorEvery,
        filledTicks: document.getElementById("tickBarFilledInput")?.value,
        labels: document.getElementById("tickBarLabelsInput")?.value,
        unit: document.getElementById("tickBarUnitInput")?.value,
        showScaleLabels: Boolean(document.getElementById("tickBarScaleLabelsInput")?.checked),
        showFractionLabel: Boolean(document.getElementById("tickBarFractionLabelInput")?.checked),
        axisColor: document.getElementById("tickBarAxisColorInput")?.value,
        fillColor: document.getElementById("tickBarFillColorInput")?.value,
      });
      closeTickBarDialog();
    }
    let pendingMathMixed = false;
    function openMathDialog(mixed = false) {
      const dialog = document.getElementById("mathInsertDialog");
      if (!dialog) return;
      pendingMathMixed = mixed;
      document.getElementById("mathInsertTitle").textContent = mixed ? "대분수 삽입" : "분수 삽입";
      document.getElementById("mathWholeLabel").hidden = !mixed;
      document.getElementById("mathWholeInput").value = "1";
      document.getElementById("mathNumeratorInput").value = "1";
      document.getElementById("mathDenominatorInput").value = "2";
      dialog.hidden = false;
      setTimeout(() => (mixed ? document.getElementById("mathWholeInput") : document.getElementById("mathNumeratorInput"))?.focus(), 0);
    }
    function closeMathDialog() {
      const dialog = document.getElementById("mathInsertDialog");
      if (dialog) dialog.hidden = true;
    }
    async function confirmMathDialog() {
      await insertFractionExpression({
        mixed: pendingMathMixed,
        whole: document.getElementById("mathWholeInput")?.value,
        numerator: document.getElementById("mathNumeratorInput")?.value,
        denominator: document.getElementById("mathDenominatorInput")?.value,
      });
      closeMathDialog();
    }
    document.getElementById("insertTableBtn").onclick = openTableDialog;
    document.getElementById("insertGraphPaperBtn").onclick = openGraphPaperDialog;
    document.getElementById("insertBarModelBtn").onclick = openBarModelDialog;
    document.getElementById("insertTickBarBtn").onclick = openTickBarDialog;
    document.getElementById("insertFractionBtn").onclick = () => openMathDialog(false);
    document.getElementById("insertMixedFractionBtn").onclick = () => openMathDialog(true);
    let imageInsertInFlight = false;

    document.getElementById("insertImageBtn").onclick = () => {
      if (imageInsertInFlight) return;
      const input = document.getElementById("insertImageInput");
      if (!input) return;
      input.value = "";
      input.click();
    };
    document.getElementById("insertImageInput").addEventListener("change", async (ev) => {
      const input = ev.currentTarget;
      const file = input.files && input.files[0];
      input.value = "";
      if (!file || imageInsertInFlight) return;
      imageInsertInFlight = true;
      const button = document.getElementById("insertImageBtn");
      if (button) button.disabled = true;
      try {
        await insertImageFromFile(file);
      } catch (e) {
        setStatus(String(e), false);
      } finally {
        imageInsertInFlight = false;
        if (button) button.disabled = false;
      }
    });
    document.getElementById("shapeGalleryBtn").onclick = (ev) => {
      ev.stopPropagation();
      toggleShapeGallery();
    };
    document.getElementById("tableConfirmBtn").onclick = async () => {
      try { await confirmTableDialog(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("tableCancelBtn").onclick = closeTableDialog;
    document.getElementById("tableCancelXBtn").onclick = closeTableDialog;
    document.getElementById("tableInsertDialog").addEventListener("click", (ev) => {
      if (ev.target === ev.currentTarget) closeTableDialog();
    });
    document.getElementById("graphPaperConfirmBtn").onclick = async () => {
      try { await confirmGraphPaperDialog(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("graphPaperCancelBtn").onclick = closeGraphPaperDialog;
    document.getElementById("graphPaperCancelXBtn").onclick = closeGraphPaperDialog;
    document.getElementById("graphPaperInsertDialog").addEventListener("click", (ev) => {
      if (ev.target === ev.currentTarget) closeGraphPaperDialog();
    });
    document.getElementById("barModelConfirmBtn").onclick = async () => {
      try { await confirmBarModelDialog(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("barModelCancelBtn").onclick = closeBarModelDialog;
    document.getElementById("barModelCancelXBtn").onclick = closeBarModelDialog;
    document.getElementById("barModelInsertDialog").addEventListener("click", (ev) => {
      if (ev.target === ev.currentTarget) closeBarModelDialog();
    });
    document.getElementById("tickBarConfirmBtn").onclick = async () => {
      try { await confirmTickBarDialog(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("tickBarCancelBtn").onclick = closeTickBarDialog;
    document.getElementById("tickBarCancelXBtn").onclick = closeTickBarDialog;
    document.getElementById("tickBarInsertDialog").addEventListener("click", (ev) => {
      if (ev.target === ev.currentTarget) closeTickBarDialog();
    });
    document.getElementById("mathConfirmBtn").onclick = async () => {
      try { await confirmMathDialog(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("mathCancelBtn").onclick = closeMathDialog;
    document.getElementById("mathCancelXBtn").onclick = closeMathDialog;
    document.getElementById("mathInsertDialog").addEventListener("click", (ev) => {
      if (ev.target === ev.currentTarget) closeMathDialog();
    });
    for (const id of ["tableColsInput", "tableRowsInput"]) {
      document.getElementById(id).addEventListener("keydown", async (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          try { await confirmTableDialog(); }
          catch (e) { setStatus(String(e), false); }
        }
        if (ev.key === "Escape") closeTableDialog();
      });
    }
    for (const id of ["graphPaperColsInput", "graphPaperRowsInput"]) {
      document.getElementById(id).addEventListener("keydown", async (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          try { await confirmGraphPaperDialog(); }
          catch (e) { setStatus(String(e), false); }
        }
        if (ev.key === "Escape") closeGraphPaperDialog();
      });
    }
    for (const id of ["barModelBarsInput", "barModelCellsInput", "barModelShadedInput", "barModelFillInput", "barModelStrokeInput", "barModelDashedInput"]) {
      document.getElementById(id).addEventListener("keydown", async (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          try { await confirmBarModelDialog(); }
          catch (e) { setStatus(String(e), false); }
        }
        if (ev.key === "Escape") closeBarModelDialog();
      });
    }
    for (const id of ["tickBarRowsInput", "tickBarTotalInput", "tickBarFilledInput", "tickBarMajorInput", "tickBarLabelsInput", "tickBarUnitInput", "tickBarScaleLabelsInput", "tickBarFractionLabelInput", "tickBarAxisColorInput", "tickBarFillColorInput"]) {
      document.getElementById(id).addEventListener("keydown", async (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          try { await confirmTickBarDialog(); }
          catch (e) { setStatus(String(e), false); }
        }
        if (ev.key === "Escape") closeTickBarDialog();
      });
    }
    for (const id of ["mathWholeInput", "mathNumeratorInput", "mathDenominatorInput"]) {
      document.getElementById(id).addEventListener("keydown", async (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          try { await confirmMathDialog(); }
          catch (e) { setStatus(String(e), false); }
        }
        if (ev.key === "Escape") closeMathDialog();
      });
    }
    document.getElementById("shapeGallery").addEventListener("click", (ev) => ev.stopPropagation());
    document.getElementById("shapeFormatMenu").addEventListener("click", (ev) => ev.stopPropagation());
    document.addEventListener("click", () => {
      document.getElementById("shapeGallery")?.classList.remove("open");
      hideShapeFormatMenu();
    });
    document.getElementById("shapeApplyFillBtn").onclick = async () => {
      try {
        await applyShapeFill(document.getElementById("shapeFillColorInput").value || "#ffffff");
        hideShapeFormatMenu();
      } catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("shapeApplyStrokeBtn").onclick = async () => {
      try {
        await applyShapeStroke(document.getElementById("shapeStrokeColorInput").value || DEFAULT_SHAPE_STYLE.stroke);
        hideShapeFormatMenu();
      } catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("shapeNoBorderBtn").onclick = async () => {
      try {
        await applyShapeFormatPatch({ stroke: "none", stroke_width: 0, stroke_dasharray: "" }, "테두리 제거");
        hideShapeFormatMenu();
      } catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("shapeSolidBtn").onclick = async () => {
      try {
        await applyShapeFormatPatch({ stroke: selectedStrokeOrDefault(), stroke_width: DEFAULT_SHAPE_STYLE.stroke_width, stroke_dasharray: "" }, "실선");
        hideShapeFormatMenu();
      } catch (e) { setStatus(String(e), false); }
    };
    function bindStrokeDashButton(id, label, dasharray) {
      document.getElementById(id).onclick = async () => {
        try {
          await applyShapeFormatPatch({
            stroke: selectedStrokeOrDefault(),
            stroke_width: DEFAULT_SHAPE_STYLE.stroke_width,
            stroke_dasharray: dasharray,
          }, label);
          hideShapeFormatMenu();
        } catch (e) { setStatus(String(e), false); }
      };
    }
    bindStrokeDashButton("shapeShortDashBtn", "짧은 점선", "4 3");
    bindStrokeDashButton("shapeDashedBtn", "긴 점선", "10 6");
    bindStrokeDashButton("shapeDotDashBtn", "점-대시", "10 4 2 4");
    bindStrokeDashButton("shapeDottedBtn", "촘촘 점선", "2 5");
    document.getElementById("patchBtn").onclick = async () => {
      try { await patchOnly(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("patchBuildBtn").onclick = async () => {
      try { await patchAndBuild(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("textEditBtn").onclick = async () => {
      try { await updateSelectedText(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("textEditInput").addEventListener("keydown", async (ev) => {
      if (ev.key !== "Enter") return;
      ev.preventDefault();
      try { await updateSelectedText(); }
      catch (e) { setStatus(String(e), false); }
    });
    document.getElementById("fontDecreaseBtn").onclick = async () => {
      try { await nudgeSelectedFontSize(-2); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("fontIncreaseBtn").onclick = async () => {
      try { await nudgeSelectedFontSize(2); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("textAlignLeftBtn").onclick = async () => {
      try { await alignSelectedTextInCell("left"); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("textAlignCenterBtn").onclick = async () => {
      try { await alignSelectedTextInCell("center"); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("textAlignRightBtn").onclick = async () => {
      try { await alignSelectedTextInCell("right"); }
      catch (e) { setStatus(String(e), false); }
    };
    for (const tab of document.querySelectorAll(".ppt-tab")) {
      tab.addEventListener("click", () => {
        const target = tab.dataset.tab;
        for (const item of document.querySelectorAll(".ppt-tab")) {
          item.classList.toggle("active", item === tab);
        }
        for (const panel of document.querySelectorAll(".ppt-tab-panel")) {
          panel.classList.toggle("active", panel.id === target);
        }
      });
    }
    bindCommitInputs(
      ["propX", "propY", "propW", "propH", "propFontSize", "propRotate"],
      () => commitInspectorFields().catch((e) => setStatus(String(e), false)),
    );
    bindCommitInputs(
      ["canvasW", "canvasH"],
      () => commitCanvasFields().catch((e) => setStatus(String(e), false)),
    );
    document.getElementById("selectCanvasBtn").onclick = () => {
      try { selectCanvas(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("snapToggleBtn").onclick = () => {
      snapEnabled = !snapEnabled;
      updateSnapButton();
      setStatus(snapEnabled ? "5px 스냅 활성화" : "5px 스냅 비활성화", true);
    };
    document.getElementById("alignLeftBtn").onclick = async () => { try { await alignSelected("left"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("alignCenterBtn").onclick = async () => { try { await alignSelected("center"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("alignRightBtn").onclick = async () => { try { await alignSelected("right"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("alignTopBtn").onclick = async () => { try { await alignSelected("top"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("alignMiddleBtn").onclick = async () => { try { await alignSelected("middle"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("alignBottomBtn").onclick = async () => { try { await alignSelected("bottom"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("bringFrontBtn").onclick = async () => { try { await layerSelected("front"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("sendBackBtn").onclick = async () => { try { await layerSelected("back"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("bringForwardBtn").onclick = async () => { try { await layerSelected("forward"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("sendBackwardBtn").onclick = async () => { try { await layerSelected("backward"); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("undoBtn").onclick = async () => { try { await undoAction(); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("redoBtn").onclick = async () => { try { await redoAction(); } catch (e) { setStatus(String(e), false); } };
    document.getElementById("deleteBtn").onclick = async () => {
      try { await deleteSelectedSlots(); }
      catch (e) { setStatus(String(e), false); }
    };
    document.getElementById("pickAllBtn").onclick = () => {
      pickMode = "all";
      applyPickMode();
      setStatus("선택 모드: All", true);
    };
    document.getElementById("pickLinePathBtn").onclick = () => {
      pickMode = "linepath";
      applyPickMode();
      setStatus("선택 모드: Line/Path", true);
    };
    document.getElementById("pickTextBtn").onclick = () => {
      pickMode = "text";
      applyPickMode();
      setStatus("선택 모드: Text", true);
    };
    document.getElementById("pickShapeBtn").onclick = () => {
      pickMode = "shape";
      applyPickMode();
      setStatus("선택 모드: Shape", true);
    };
    document.addEventListener("keydown", (ev) => {
      const active = document.activeElement;
      if (active && (active.tagName === "INPUT" || active.tagName === "TEXTAREA")) return;

      if ((ev.ctrlKey || ev.metaKey) && !ev.shiftKey && ev.key.toLowerCase() === "z") {
        ev.preventDefault();
        undoAction().catch((e) => setStatus(String(e), false));
        return;
      }
      if ((ev.ctrlKey || ev.metaKey) && (ev.key.toLowerCase() === "y" || (ev.shiftKey && ev.key.toLowerCase() === "z"))) {
        ev.preventDefault();
        redoAction().catch((e) => setStatus(String(e), false));
        return;
      }
      if ((ev.ctrlKey || ev.metaKey) && !ev.shiftKey && ev.key.toLowerCase() === "c") {
        ev.preventDefault();
        try { copySelectedSlots(); }
        catch (e) { setStatus(String(e), false); }
        return;
      }
      if ((ev.ctrlKey || ev.metaKey) && !ev.shiftKey && ev.key.toLowerCase() === "v") {
        ev.preventDefault();
        pasteCopiedSlots().catch((e) => setStatus(String(e), false));
        return;
      }
      if (ev.key === "Escape") {
        if (drawState || pendingDrawShape) {
          drawState = null;
          pendingDrawShape = null;
          removeDrawPreview();
          setStatus("그리기가 취소되었습니다.", false);
          return;
        }
        hideShapeFormatMenu();
        document.getElementById("shapeGallery")?.classList.remove("open");
        return;
      }
      if (!selectedSlots.size) return;

      if (ev.key === "Delete" || ev.key === "Backspace") {
        ev.preventDefault();
        deleteSelectedSlots().catch((e) => setStatus(String(e), false));
        return;
      }

      let dx = 0;
      let dy = 0;
      const step = ev.shiftKey ? 10 : 1;
      if (ev.key === "ArrowLeft") dx = -step;
      if (ev.key === "ArrowRight") dx = step;
      if (ev.key === "ArrowUp") dy = -step;
      if (ev.key === "ArrowDown") dy = step;
      if (dx === 0 && dy === 0) return;
      ev.preventDefault();

      const beforeStates = readSelectedStates();
      const patches = [];
      const handledFractionPrefixes = new Set();
      for (const item of selectedSlots.values()) {
        if (item.isCharacterGroup || item.isLayoutGroup) {
          for (const node of item.elements || []) applyElementDelta(node, dx, dy, false);
          for (const node of item.elements || []) {
            const slotId = slotIdFromElement(node);
            const value = readSlotPatchValue(node);
            if (slotId && value) patches.push({ target: slotId, op: "update", value });
          }
          continue;
        }
        if (item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup) {
          for (const node of item.elements || []) applyElementDelta(node, dx, dy, false);
          patches.push({ target: item.slotId, op: "update", value: { move_dx: dx, move_dy: dy } });
          continue;
        }
        if (item.isGeneratedGroup || item.isGraphPaperGroup) {
          for (const node of item.elements || []) applyElementDelta(node, dx, dy, false);
          for (const node of item.elements || []) {
            const slotId = slotIdFromElement(node);
            const value = readSlotPatchValue(node);
            if (slotId && value) patches.push({ target: slotId, op: "update", value });
          }
          continue;
        }
        const fracInfo = parseFractionPartId(item.el.getAttribute("id"));
        if (fracInfo && fracInfo.prefix === item.slotId) {
          if (handledFractionPrefixes.has(fracInfo.prefix)) continue;
          const elems = fractionPartElements(fracInfo.prefix);
          for (const el of elems) applyElementDelta(el, dx, dy, false);
          patches.push({ target: fracInfo.prefix, op: "update", value: { move_dx: dx, move_dy: dy } });
          handledFractionPrefixes.add(fracInfo.prefix);
          continue;
        }
        const value = applyElementDelta(item.el, dx, dy, false);
        if (!value) continue;
        for (const target of item.slotIds || [item.slotId]) {
          patches.push({ target, op: "update", value });
        }
      }
      if (!patches.length) return;
      updateSelectionHandles();
      setStatus(`키보드 이동 중 ${patches.length}개 선택${snapEnabled ? " (snap 5px)" : ""}`, true);
      queueKeyboardCommit(patches, `키보드 이동 저장 완료: ${patches.length}개`, beforeStates);
    });

    initCanvas({
      container: document.getElementById("svgPreview"),
      onSelectionChange: (selectedIds) => setState({ selectedIds }),
      onCommand: (command) => executeEditorCommand(command, getState()),
      getState,
    });
    initProperties({
      root: document.querySelector(".ppt-inspector"),
      onCommand: (command) => executeEditorCommand(command, getState()),
      getState,
    });
    subscribe((next) => {
      document.body.dataset.dirty = next.dirty ? "true" : "false";
    });

    renderShapeGallery();
    renderShapeFormatSwatches();
    loadProblems().catch((e) => {
      const tree = document.getElementById("problemTree");
      if (tree) tree.innerHTML = `<em>${String(e)}</em>`;
      setStatus(String(e), false);
    });





