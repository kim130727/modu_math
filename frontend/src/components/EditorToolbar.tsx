import type { EditorStore, GalleryShapeDefinition } from "../stores/editorStore";
import { For, createSignal, onCleanup, onMount } from "solid-js";

interface EditorToolbarProps {
  store: EditorStore;
}

type InsertDialogKind = "table" | "graph" | "bar" | "tick" | "fraction" | "mixedFraction";

export function EditorToolbar(props: EditorToolbarProps) {
  const [problemPath, setProblemPath] = createSignal("");
  const [dialog, setDialog] = createSignal<InsertDialogKind | null>(null);
  const [shapeGalleryOpen, setShapeGalleryOpen] = createSignal(false);
  const [tableCols, setTableCols] = createSignal("5");
  const [tableRows, setTableRows] = createSignal("2");
  const [graphCols, setGraphCols] = createSignal("10");
  const [graphRows, setGraphRows] = createSignal("8");
  const [barBars, setBarBars] = createSignal("2");
  const [barCells, setBarCells] = createSignal("3");
  const [barShaded, setBarShaded] = createSignal("2,2");
  const [barFill, setBarFill] = createSignal("#f3d7ea");
  const [barStroke, setBarStroke] = createSignal("#666666");
  const [barDashed, setBarDashed] = createSignal(true);
  const [tickRows, setTickRows] = createSignal("2");
  const [tickTotal, setTickTotal] = createSignal("14");
  const [tickFilled, setTickFilled] = createSignal("9,10");
  const [tickMajor, setTickMajor] = createSignal("7");
  const [tickLabels, setTickLabels] = createSignal("");
  const [tickUnit, setTickUnit] = createSignal("m");
  const [tickScaleLabels, setTickScaleLabels] = createSignal(true);
  const [tickFractionLabel, setTickFractionLabel] = createSignal(true);
  const [tickAxisColor, setTickAxisColor] = createSignal("#111111");
  const [tickFillColor, setTickFillColor] = createSignal("#2563eb");
  const [mathWhole, setMathWhole] = createSignal("1");
  const [mathNumerator, setMathNumerator] = createSignal("1");
  const [mathDenominator, setMathDenominator] = createSignal("2");
  let imageInputRef!: HTMLInputElement;
  let shapeDropdownRef!: HTMLDivElement;
  const hasSelection = () => props.store.state.selectedIds.length > 0;
  const hasMultiSelection = () => props.store.state.selectedIds.length > 1;
  const isBusy = () => props.store.state.loading;
  const currentProblemPath = () => problemPath() || props.store.state.problemId || "";
  const canInsert = () => !!props.store.state.document && !props.store.state.loading;

  const openDialog = (kind: InsertDialogKind) => {
    if (!canInsert()) return;
    setShapeGalleryOpen(false);
    setDialog(kind);
  };

  const closeDialog = () => setDialog(null);

  onMount(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setShapeGalleryOpen(false);
        props.store.cancelDrawShape();
      }
    };
    const handlePointerDown = (event: PointerEvent) => {
      if (!shapeGalleryOpen()) return;
      const target = event.target;
      if (target instanceof Node && shapeDropdownRef?.contains(target)) return;
      setShapeGalleryOpen(false);
    };
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("pointerdown", handlePointerDown);
    onCleanup(() => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("pointerdown", handlePointerDown);
    });
  });

  const dialogTitle = () => {
    switch (dialog()) {
      case "table":
        return "표 삽입";
      case "graph":
        return "모눈종이 삽입";
      case "bar":
        return "막대 모델 삽입";
      case "tick":
        return "눈금 막대 삽입";
      case "mixedFraction":
        return "대분수 삽입";
      case "fraction":
        return "분수 삽입";
      default:
        return "";
    }
  };

  const submitDialog = async () => {
    const kind = dialog();
    if (!kind) return;
    if (kind === "table") await props.store.insertTable(toInt(tableRows(), 1, 20, 2), toInt(tableCols(), 1, 20, 5));
    if (kind === "graph") await props.store.insertGraphPaper(toInt(graphRows(), 1, 40, 8), toInt(graphCols(), 1, 40, 10));
    if (kind === "bar") {
      await props.store.insertBarModel({
        bars: toInt(barBars(), 1, 8, 2),
        cells: toInt(barCells(), 1, 20, 3),
        shadedCounts: barShaded(),
        fillColors: barFill(),
        stroke: barStroke(),
        dashed: barDashed(),
      });
    }
    if (kind === "tick") {
      const totalTicks = toInt(tickTotal(), 1, 40, 14);
      await props.store.insertTickBar({
        rows: toInt(tickRows(), 1, 8, 2),
        totalTicks,
        filledTicks: tickFilled(),
        majorEvery: toInt(tickMajor(), 0, totalTicks, 7),
        labels: tickLabels(),
        unit: tickUnit(),
        showScaleLabels: tickScaleLabels(),
        showFractionLabel: tickFractionLabel(),
        axisColor: tickAxisColor(),
        fillColor: tickFillColor(),
      });
    }
    if (kind === "fraction" || kind === "mixedFraction") {
      await props.store.insertFractionExpression({
        mixed: kind === "mixedFraction",
        whole: mathWhole(),
        numerator: mathNumerator(),
        denominator: mathDenominator(),
      });
    }
    closeDialog();
  };

  return (
    <>
      <header class="editor-next-toolbar ppt-titlebar ppt-ribbon">
        <div class="toolbar-title ribbon-group">
          <strong>ModuMath Editor Next</strong>
          <span>{props.store.state.problemId ?? "No problem selected"}</span>
          <input
            class="toolbar-problem-input"
            list="editorNextProblemOptions"
            value={currentProblemPath()}
            placeholder="Problem path"
            onInput={(event) => setProblemPath(event.currentTarget.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") void props.store.openProblem(currentProblemPath());
            }}
            disabled={props.store.state.loading}
          />
          <datalist id="editorNextProblemOptions">
            {props.store.state.problems.map((problem) => (
              <option value={problem.problem_id} />
            ))}
          </datalist>
        </div>
        <div class="toolbar-actions ribbon-group">
          <IconButton icon="pointer" label="Select" active={props.store.state.activeTool === "select"} onClick={() => props.store.setActiveTool("select")} disabled={props.store.state.loading} />
          <IconButton icon="hand" label="Pan" active={props.store.state.activeTool === "pan"} onClick={() => props.store.setActiveTool("pan")} disabled={props.store.state.loading} />
          <IconButton icon="magnet" label="Snap 5px" active={props.store.state.snapEnabled} onClick={() => props.store.setSnapEnabled(!props.store.state.snapEnabled)} disabled={props.store.state.loading} />
          <IconButton icon="undo" label="Undo" onClick={() => void props.store.undo()} disabled={props.store.state.loading || props.store.state.history.undoStack.length === 0} />
          <IconButton icon="redo" label="Redo" onClick={() => void props.store.redo()} disabled={props.store.state.loading || props.store.state.history.redoStack.length === 0} />
          <IconButton icon="copy" label="Copy" onClick={() => props.store.copySelectedSlots()} disabled={isBusy() || !hasSelection()} />
          <IconButton icon="paste" label="Paste" onClick={() => void props.store.pasteCopiedSlots()} disabled={isBusy() || !props.store.state.hasCopyBuffer} />
          <IconButton icon="refresh" label="Refresh problems" onClick={() => void props.store.refreshProblems()} disabled={props.store.state.loading} />
          <IconButton icon="folder" label="Open problem" onClick={() => void props.store.openProblem(currentProblemPath())} disabled={!currentProblemPath().trim() || props.store.state.loading} />
          <IconButton icon="reload" label="Reload problem" onClick={() => props.store.state.problemId && void props.store.openProblem(props.store.state.problemId)} disabled={!props.store.state.problemId || props.store.state.loading} />
          <IconButton icon="save" label="Save DSL" onClick={() => void props.store.saveDslDraft()} disabled={!props.store.state.problemId || props.store.state.saving || props.store.state.loading} />
          <IconButton icon="build" label="Build" onClick={() => void props.store.buildCurrentProblem()} disabled={!props.store.state.problemId || props.store.state.building || props.store.state.loading} />
          <IconButton icon="text" label="Text Box" onClick={() => void props.store.insertShape("text_box")} disabled={!canInsert()} />
          <IconButton icon="table" label="Table" onClick={() => openDialog("table")} disabled={!canInsert()} />
          <IconButton icon="bar" label="Bar Model" onClick={() => openDialog("bar")} disabled={!canInsert()} />
          <IconButton icon="tick" label="Tick Bar" onClick={() => openDialog("tick")} disabled={!canInsert()} />
          <IconButton icon="grid" label="Graph Paper" onClick={() => openDialog("graph")} disabled={!canInsert()} />
          <IconButton icon="fraction" label="Fraction" onClick={() => openDialog("fraction")} disabled={!canInsert()} />
          <IconButton icon="mixedFraction" label="Mixed Fraction" onClick={() => openDialog("mixedFraction")} disabled={!canInsert()} />
          <div class="ribbon-dropdown" ref={shapeDropdownRef}>
            <button
              type="button"
              class="icon-btn"
              title="Shapes"
              aria-label="Shapes"
              aria-haspopup="menu"
              aria-expanded={shapeGalleryOpen()}
              classList={{ active: shapeGalleryOpen() }}
              onClick={() => {
                if (!canInsert()) return;
                setShapeGalleryOpen((open) => !open);
              }}
              disabled={!canInsert()}
            >
              <Icon name="shapes" />
            </button>
            <div classList={{ "shape-gallery": true, open: shapeGalleryOpen() }} role="menu" aria-label="Shapes">
              <For each={SHAPE_CATEGORIES}>
                {(category) => (
                  <>
                    <div class="shape-category-title">{category.title}</div>
                    <div class="shape-grid">
                      <For each={category.shapes}>
                        {(shape) => (
                          <button
                            type="button"
                            class="shape-choice"
                            title={shape.label}
                            aria-label={shape.label}
                            onClick={async () => {
                              setShapeGalleryOpen(false);
                              if (shape.drawMode) {
                                props.store.beginDrawShape(shape);
                              } else {
                                await props.store.insertGalleryShape(shape);
                              }
                            }}
                          >
                            <ShapePreview shape={shape} />
                          </button>
                        )}
                      </For>
                    </div>
                  </>
                )}
              </For>
            </div>
          </div>
          <IconButton icon="rect" label="Rect" onClick={() => void props.store.insertShape("rect")} disabled={!canInsert()} />
          <IconButton icon="circle" label="Circle" onClick={() => void props.store.insertShape("circle")} disabled={!canInsert()} />
          <IconButton icon="line" label="Line" onClick={() => void props.store.insertShape("line")} disabled={!canInsert()} />
          <IconButton icon="triangle" label="Triangle" onClick={() => void props.store.insertShape("triangle")} disabled={!canInsert()} />
          <IconButton icon="curve" label="Curve" onClick={() => void props.store.insertShape("path")} disabled={!canInsert()} />
          <button
            type="button"
            class="icon-btn"
            title="Image"
            aria-label="Image"
            onClick={() => {
              if (!canInsert()) return;
              imageInputRef.click();
            }}
            disabled={!canInsert()}
          >
            <Icon name="image" />
          </button>
          <input
            ref={imageInputRef}
            type="file"
            accept="image/*"
            hidden
            onChange={(event) => {
              const file = event.currentTarget.files?.[0];
              event.currentTarget.value = "";
              if (file) void props.store.insertImageFile(file);
            }}
          />
          <IconButton icon="trash" label="Delete" onClick={() => void props.store.deleteSelectedSlots()} disabled={isBusy() || !hasSelection()} />
        </div>
        <div class="toolbar-actions toolbar-align ribbon-group" aria-label="Alignment and layer controls">
          <IconButton icon="alignLeft" label="Align left" onClick={() => void props.store.alignSelectedSlots("left")} disabled={isBusy() || !hasMultiSelection()} />
          <IconButton icon="alignCenter" label="Align center" onClick={() => void props.store.alignSelectedSlots("center")} disabled={isBusy() || !hasMultiSelection()} />
          <IconButton icon="alignRight" label="Align right" onClick={() => void props.store.alignSelectedSlots("right")} disabled={isBusy() || !hasMultiSelection()} />
          <IconButton icon="alignTop" label="Align top" onClick={() => void props.store.alignSelectedSlots("top")} disabled={isBusy() || !hasMultiSelection()} />
          <IconButton icon="alignMiddle" label="Align middle" onClick={() => void props.store.alignSelectedSlots("middle")} disabled={isBusy() || !hasMultiSelection()} />
          <IconButton icon="alignBottom" label="Align bottom" onClick={() => void props.store.alignSelectedSlots("bottom")} disabled={isBusy() || !hasMultiSelection()} />
          <IconButton icon="front" label="Bring to front" onClick={() => void props.store.layerSelectedSlots("front")} disabled={isBusy() || !hasSelection()} />
          <IconButton icon="back" label="Send to back" onClick={() => void props.store.layerSelectedSlots("back")} disabled={isBusy() || !hasSelection()} />
          <IconButton icon="forward" label="Bring forward" onClick={() => void props.store.layerSelectedSlots("forward")} disabled={isBusy() || !hasSelection()} />
          <IconButton icon="backward" label="Send backward" onClick={() => void props.store.layerSelectedSlots("backward")} disabled={isBusy() || !hasSelection()} />
        </div>
        <div class="toolbar-pickmodes ribbon-group" aria-label="Selection target filters">
          <button type="button" classList={{ active: props.store.state.pickMode === "all" }} onClick={() => props.store.setPickMode("all")} disabled={props.store.state.loading}>
            All
          </button>
          <button type="button" classList={{ active: props.store.state.pickMode === "text" }} onClick={() => props.store.setPickMode("text")} disabled={props.store.state.loading}>
            Text
          </button>
          <button type="button" classList={{ active: props.store.state.pickMode === "shape" }} onClick={() => props.store.setPickMode("shape")} disabled={props.store.state.loading}>
            Shape
          </button>
          <button type="button" classList={{ active: props.store.state.pickMode === "linepath" }} onClick={() => props.store.setPickMode("linepath")} disabled={props.store.state.loading}>
            Line/Path
          </button>
        </div>
      </header>
      {dialog() && (
        <div class="table-dialog" role="dialog" aria-modal="true" onClick={(event) => event.target === event.currentTarget && closeDialog()}>
          <div class="table-dialog-panel">
            <div class="table-dialog-title">
              <span>{dialogTitle()}</span>
              <button type="button" aria-label="닫기" onClick={closeDialog}>
                &times;
              </button>
            </div>
            <div class="table-dialog-fields" onKeyDown={(event) => {
              if (event.key === "Escape") closeDialog();
              if (event.key === "Enter") void submitDialog();
            }}>
              {dialog() === "table" && (
                <>
                  <label>열 개수(C):<input type="number" min="1" max="20" value={tableCols()} onInput={(event) => setTableCols(event.currentTarget.value)} /></label>
                  <label>행 개수(R):<input type="number" min="1" max="20" value={tableRows()} onInput={(event) => setTableRows(event.currentTarget.value)} /></label>
                </>
              )}
              {dialog() === "graph" && (
                <>
                  <label>좌우 칸:<input type="number" min="1" max="40" value={graphCols()} onInput={(event) => setGraphCols(event.currentTarget.value)} /></label>
                  <label>상하 칸:<input type="number" min="1" max="40" value={graphRows()} onInput={(event) => setGraphRows(event.currentTarget.value)} /></label>
                </>
              )}
              {dialog() === "bar" && (
                <>
                  <label>막대 수:<input type="number" min="1" max="8" value={barBars()} onInput={(event) => setBarBars(event.currentTarget.value)} /></label>
                  <label>칸 수:<input type="number" min="1" max="20" value={barCells()} onInput={(event) => setBarCells(event.currentTarget.value)} /></label>
                  <label>색칠 칸:<input value={barShaded()} onInput={(event) => setBarShaded(event.currentTarget.value)} /></label>
                  <label>색칠색:<input value={barFill()} onInput={(event) => setBarFill(event.currentTarget.value)} /></label>
                  <label>테두리색:<input value={barStroke()} onInput={(event) => setBarStroke(event.currentTarget.value)} /></label>
                  <label>칸 점선:<input type="checkbox" checked={barDashed()} onChange={(event) => setBarDashed(event.currentTarget.checked)} /></label>
                </>
              )}
              {dialog() === "tick" && (
                <>
                  <label>막대 수:<input type="number" min="1" max="8" value={tickRows()} onInput={(event) => setTickRows(event.currentTarget.value)} /></label>
                  <label>전체 눈금:<input type="number" min="1" max="40" value={tickTotal()} onInput={(event) => setTickTotal(event.currentTarget.value)} /></label>
                  <label>색칠 눈금:<input value={tickFilled()} onInput={(event) => setTickFilled(event.currentTarget.value)} /></label>
                  <label>큰 눈금:<input type="number" min="0" max="40" value={tickMajor()} onInput={(event) => setTickMajor(event.currentTarget.value)} /></label>
                  <label>라벨:<input value={tickLabels()} placeholder="예: 9/7 m,1 3/7 m" onInput={(event) => setTickLabels(event.currentTarget.value)} /></label>
                  <label>단위:<input value={tickUnit()} onInput={(event) => setTickUnit(event.currentTarget.value)} /></label>
                  <label>눈금 라벨:<input type="checkbox" checked={tickScaleLabels()} onChange={(event) => setTickScaleLabels(event.currentTarget.checked)} /></label>
                  <label>분할 라벨:<input type="checkbox" checked={tickFractionLabel()} onChange={(event) => setTickFractionLabel(event.currentTarget.checked)} /></label>
                  <label>눈금색:<input type="color" value={tickAxisColor()} onInput={(event) => setTickAxisColor(event.currentTarget.value)} /></label>
                  <label>색칠색:<input type="color" value={tickFillColor()} onInput={(event) => setTickFillColor(event.currentTarget.value)} /></label>
                </>
              )}
              {(dialog() === "fraction" || dialog() === "mixedFraction") && (
                <>
                  {dialog() === "mixedFraction" && <label>자연수:<input value={mathWhole()} onInput={(event) => setMathWhole(event.currentTarget.value)} /></label>}
                  <label>분자:<input value={mathNumerator()} onInput={(event) => setMathNumerator(event.currentTarget.value)} /></label>
                  <label>분모:<input value={mathDenominator()} onInput={(event) => setMathDenominator(event.currentTarget.value)} /></label>
                </>
              )}
            </div>
            <div class="table-dialog-actions">
              <button type="button" class="primary" onClick={() => void submitDialog()}>확인</button>
              <button type="button" onClick={closeDialog}>취소</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

interface ShapeCategory {
  title: string;
  shapes: GalleryShapeDefinition[];
}

const SHAPE_CATEGORIES: ShapeCategory[] = [
  {
    title: "Lines",
    shapes: [
      { id: "line", label: "Line", kind: "line" },
      { id: "hline", label: "Horizontal line", kind: "line", line: "horizontal" },
      { id: "vline", label: "Vertical line", kind: "line", line: "vertical" },
      { id: "drawLine", label: "Draw line", kind: "line", drawMode: true },
      { id: "elbow", label: "Elbow connector", kind: "path", d: "M 0 0 L 52 0 L 52 48", fill: "none", drawMode: true },
      { id: "curve", label: "Curve", kind: "path", d: "M 0 40 C 16 0, 34 80, 60 20", fill: "none", drawMode: true },
      { id: "freeform", label: "Freeform", kind: "path", d: "M 0 36 L 14 12 L 28 48 L 42 22 L 56 16 L 66 4", sourceWidth: 66, sourceHeight: 52, fill: "none", drawMode: true },
    ],
  },
  {
    title: "Rectangles",
    shapes: [
      { id: "rect", label: "Rectangle", kind: "rect" },
      { id: "roundRect", label: "Rounded rectangle", kind: "rect", rx: 6, ry: 6 },
      { id: "snip1", label: "Snipped rectangle", kind: "polygon", points: [[10, 0], [64, 0], [64, 46], [0, 46], [0, 10]] },
      { id: "snip2", label: "Diagonal snipped rectangle", kind: "polygon", points: [[10, 0], [64, 0], [64, 36], [54, 46], [0, 46], [0, 10]] },
      { id: "tab", label: "Tab rectangle", kind: "path", d: "M 0 12 Q 0 0 12 0 L 52 0 Q 64 0 64 12 L 64 46 L 0 46 Z" },
    ],
  },
  {
    title: "Basic Shapes",
    shapes: [
      { id: "circle", label: "Circle", kind: "circle", r: 43 },
      { id: "oval", label: "Oval", kind: "path", d: "M 32 0 C 49.7 0 64 10.3 64 23 C 64 35.7 49.7 46 32 46 C 14.3 46 0 35.7 0 23 C 0 10.3 14.3 0 32 0 Z" },
      { id: "triangle", label: "Triangle", kind: "polygon", points: [[32, 0], [64, 52], [0, 52]] },
      { id: "rightTriangle", label: "Right triangle", kind: "polygon", points: [[0, 0], [64, 52], [0, 52]] },
      { id: "parallelogram", label: "Parallelogram", kind: "polygon", points: [[16, 0], [64, 0], [48, 46], [0, 46]] },
      { id: "trapezoid", label: "Trapezoid", kind: "polygon", points: [[16, 0], [48, 0], [64, 46], [0, 46]] },
      { id: "diamond", label: "Diamond", kind: "polygon", points: [[32, 0], [64, 26], [32, 52], [0, 26]] },
      { id: "pentagon", label: "Pentagon", kind: "polygon", points: [[32, 0], [64, 20], [52, 52], [12, 52], [0, 20]] },
      { id: "hexagon", label: "Hexagon", kind: "polygon", points: [[18, 0], [46, 0], [64, 26], [46, 52], [18, 52], [0, 26]] },
      { id: "octagon", label: "Octagon", kind: "polygon", points: [[18, 0], [46, 0], [64, 18], [64, 34], [46, 52], [18, 52], [0, 34], [0, 18]] },
      { id: "cross", label: "Cross", kind: "polygon", points: [[24, 0], [40, 0], [40, 18], [64, 18], [64, 34], [40, 34], [40, 52], [24, 52], [24, 34], [0, 34], [0, 18], [24, 18]] },
      { id: "x", label: "X", kind: "polygon", points: [[8, 0], [32, 20], [56, 0], [64, 8], [40, 26], [64, 44], [56, 52], [32, 32], [8, 52], [0, 44], [24, 26], [0, 8]] },
      { id: "bracketPair", label: "Parentheses", kind: "path", d: "M 20 0 C 4 12, 4 40, 20 52 M 44 0 C 60 12, 60 40, 44 52", fill: "none" },
      { id: "arc", label: "Arc", kind: "path", d: "M 4 46 A 28 28 0 0 1 60 46", fill: "none" },
      { id: "quarterArc", label: "Quarter arc", kind: "path", d: "M 4 46 A 42 42 0 0 1 46 4", fill: "none" },
    ],
  },
  {
    title: "Teaching Aids",
    shapes: [
      { id: "pushPin", label: "Push pin", kind: "path", d: "M 32 4 C 44 4 54 11 54 20 C 54 29 44 36 32 36 C 20 36 10 29 10 20 C 10 11 20 4 32 4 Z M 25 34 L 39 34 L 39 44 L 25 44 Z M 32 44 L 38 58 L 26 58 Z", sourceWidth: 64, sourceHeight: 64, fill: "#A8B0B6", stroke: "#7E8790", stroke_width: 1.2 },
      {
        id: "boy",
        label: "Boy",
        kind: "composite",
        sourceWidth: 80,
        sourceHeight: 110,
        w: 80,
        h: 110,
        parts: [
          { id: "body", kind: "polygon", points: [[18, 104], [62, 104], [54, 67], [26, 67]], fill: "#60A5FA", stroke: "none" },
          { id: "head", kind: "circle", cx: 40, cy: 38, r: 24, fill: "#ffd9ad", stroke: "none" },
          { id: "hair.cap", kind: "path", d: "M 16 37 C 19 10 61 9 64 37 C 49 22 31 29 16 37 Z", fill: "#7C4A2D", stroke: "none" },
          { id: "eye.left", kind: "circle", cx: 31, cy: 42, r: 3.1, fill: "#2b2118", stroke: "none" },
          { id: "eye.right", kind: "circle", cx: 49, cy: 42, r: 3.1, fill: "#2b2118", stroke: "none" },
          { id: "eye.left.light", kind: "circle", cx: 30.1, cy: 40.9, r: 0.9, fill: "#ffffff", stroke: "none" },
          { id: "eye.right.light", kind: "circle", cx: 48.1, cy: 40.9, r: 0.9, fill: "#ffffff", stroke: "none" },
          { id: "smile", kind: "path", d: "M 33 52 Q 40 58 47 52", fill: "none", stroke: "#b86e39", stroke_width: 1.4 },
        ],
      },
      {
        id: "girl",
        label: "Girl",
        kind: "composite",
        sourceWidth: 90,
        sourceHeight: 112,
        w: 90,
        h: 112,
        parts: [
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
        ],
      },
      {
        id: "school",
        label: "School",
        kind: "composite",
        sourceWidth: 96,
        sourceHeight: 76,
        w: 96,
        h: 76,
        parts: [
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
        ],
      },
      {
        id: "house",
        label: "House",
        kind: "composite",
        sourceWidth: 84,
        sourceHeight: 62,
        w: 84,
        h: 62,
        parts: [
          { id: "yard", kind: "rect", x: 5, y: 53, width: 74, height: 8, rx: 4, ry: 4, stroke: "none", fill: "#b7e2b6" },
          { id: "body", kind: "rect", x: 16, y: 28, width: 52, height: 34, fill: "#ffe19a", stroke: "#8a6240", stroke_width: 1.4 },
          { id: "roof", kind: "polygon", points: [[9, 30], [42, 8], [75, 30]], fill: "#ef6b55", stroke: "#a64b43", stroke_width: 1.4 },
          { id: "chimney", kind: "rect", x: 58, y: 13, width: 8, height: 16, fill: "#ef6b55", stroke: "#a64b43", stroke_width: 1 },
          { id: "door", kind: "rect", x: 37, y: 40, width: 12, height: 22, fill: "#7cc3ff", stroke: "#795548", stroke_width: 1 },
          { id: "window.left", kind: "rect", x: 23, y: 36, width: 10, height: 10, fill: "#dff6ff", stroke: "#4f91b7", stroke_width: 1 },
          { id: "window.right", kind: "rect", x: 53, y: 36, width: 10, height: 10, fill: "#dff6ff", stroke: "#4f91b7", stroke_width: 1 },
        ],
      },
      {
        id: "playground",
        label: "Playground",
        kind: "composite",
        sourceWidth: 96,
        sourceHeight: 82,
        w: 96,
        h: 82,
        parts: [
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
        ],
      },
    ],
  },
  {
    title: "Block Arrows",
    shapes: [
      { id: "rightArrow", label: "Right arrow", kind: "polygon", points: [[0, 16], [42, 16], [42, 0], [64, 26], [42, 52], [42, 36], [0, 36]] },
      { id: "leftArrow", label: "Left arrow", kind: "polygon", points: [[64, 16], [22, 16], [22, 0], [0, 26], [22, 52], [22, 36], [64, 36]] },
      { id: "upArrow", label: "Up arrow", kind: "polygon", points: [[24, 52], [24, 18], [8, 18], [32, 0], [56, 18], [40, 18], [40, 52]] },
      { id: "downArrow", label: "Down arrow", kind: "polygon", points: [[24, 0], [40, 0], [40, 34], [56, 34], [32, 52], [8, 34], [24, 34]] },
      { id: "leftRightArrow", label: "Left right arrow", kind: "polygon", points: [[0, 26], [18, 6], [18, 18], [46, 18], [46, 6], [64, 26], [46, 46], [46, 34], [18, 34], [18, 46]] },
      { id: "quadArrow", label: "Four way arrow", kind: "polygon", points: [[32, 0], [46, 14], [38, 14], [38, 20], [50, 20], [50, 12], [64, 26], [50, 40], [50, 32], [38, 32], [38, 38], [46, 38], [32, 52], [18, 38], [26, 38], [26, 32], [14, 32], [14, 40], [0, 26], [14, 12], [14, 20], [26, 20], [26, 14], [18, 14]] },
      { id: "chevron", label: "Chevron", kind: "polygon", points: [[0, 0], [42, 0], [64, 26], [42, 52], [0, 52], [22, 26]] },
      { id: "notchedArrow", label: "Notched arrow", kind: "polygon", points: [[0, 8], [42, 8], [42, 0], [64, 26], [42, 52], [42, 44], [0, 44], [14, 26]] },
    ],
  },
  {
    title: "Math",
    shapes: [
      { id: "mathPlus", label: "Plus", kind: "polygon", points: [[27, 0], [37, 0], [37, 21], [64, 21], [64, 31], [37, 31], [37, 52], [27, 52], [27, 31], [0, 31], [0, 21], [27, 21]] },
      { id: "mathMinus", label: "Minus", kind: "rect", h: 12 },
      { id: "mathMultiply", label: "Multiply", kind: "path", d: "M 8 0 L 32 20 L 56 0 L 64 8 L 40 26 L 64 44 L 56 52 L 32 32 L 8 52 L 0 44 L 24 26 L 0 8 Z" },
      { id: "mathDivide", label: "Divide", kind: "path", d: "M 0 22 L 64 22 L 64 30 L 0 30 Z M 32 3 A 6 6 0 1 1 31.9 3 M 32 43 A 6 6 0 1 1 31.9 43" },
      { id: "mathEqual", label: "Equals", kind: "path", d: "M 0 14 L 64 14 L 64 22 L 0 22 Z M 0 30 L 64 30 L 64 38 L 0 38 Z" },
    ],
  },
  {
    title: "Flowchart",
    shapes: [
      { id: "flowProcess", label: "Process", kind: "rect" },
      { id: "flowTerminator", label: "Terminator", kind: "path", d: "M 14 0 L 50 0 C 68 0 68 46 50 46 L 14 46 C -4 46 -4 0 14 0 Z" },
      { id: "flowDecision", label: "Decision", kind: "polygon", points: [[32, 0], [64, 23], [32, 46], [0, 23]] },
      { id: "flowData", label: "Data", kind: "polygon", points: [[14, 0], [64, 0], [50, 46], [0, 46]] },
      { id: "flowDocument", label: "Document", kind: "path", d: "M 0 0 L 64 0 L 64 38 C 48 52 18 30 0 46 Z" },
      { id: "flowStoredData", label: "Stored data", kind: "path", d: "M 14 0 L 64 0 C 50 12 50 34 64 46 L 14 46 C -4 46 -4 0 14 0 Z" },
      { id: "flowDelay", label: "Delay", kind: "path", d: "M 0 0 L 40 0 C 72 0 72 46 40 46 L 0 46 Z" },
    ],
  },
  {
    title: "Stars And Banners",
    shapes: [
      { id: "star5", label: "5 point star", kind: "polygon", points: [[32, 0], [39, 19], [60, 19], [43, 31], [50, 52], [32, 39], [14, 52], [21, 31], [4, 19], [25, 19]] },
      { id: "star8", label: "8 point star", kind: "polygon", points: [[32, 0], [39, 17], [56, 8], [47, 25], [64, 32], [47, 39], [56, 56], [39, 47], [32, 64], [25, 47], [8, 56], [17, 39], [0, 32], [17, 25], [8, 8], [25, 17]], sourceHeight: 64 },
      { id: "burst", label: "Burst", kind: "polygon", points: [[32, 0], [39, 14], [54, 8], [50, 24], [64, 32], [50, 40], [54, 56], [39, 50], [32, 64], [25, 50], [10, 56], [14, 40], [0, 32], [14, 24], [10, 8], [25, 14]], sourceHeight: 64 },
      { id: "ribbon", label: "Ribbon", kind: "path", d: "M 0 8 L 20 8 L 20 0 L 44 0 L 44 8 L 64 8 L 52 26 L 64 44 L 44 44 L 44 52 L 20 52 L 20 44 L 0 44 L 12 26 Z" },
    ],
  },
  {
    title: "Callouts",
    shapes: [
      { id: "calloutRect", label: "Rectangular callout", kind: "path", d: "M 0 0 L 64 0 L 64 38 L 42 38 L 30 52 L 32 38 L 0 38 Z" },
      { id: "calloutRound", label: "Rounded callout", kind: "path", d: "M 8 0 L 56 0 Q 64 0 64 8 L 64 36 Q 64 44 56 44 L 42 44 L 30 52 L 32 44 L 8 44 Q 0 44 0 36 L 0 8 Q 0 0 8 0 Z" },
      { id: "calloutOval", label: "Oval callout", kind: "path", d: "M 32 0 C 50 0 64 10 64 24 C 64 38 50 48 32 48 C 27 48 22 47 18 46 L 4 54 L 10 42 C 4 38 0 32 0 24 C 0 10 14 0 32 0 Z", sourceHeight: 54 },
      { id: "calloutLine", label: "Line callout", kind: "path", d: "M 0 0 L 50 0 L 50 30 L 22 30 L 6 52", fill: "none" },
    ],
  },
];

function ShapePreview(props: { shape: GalleryShapeDefinition }) {
  const label = props.shape.label.split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase();
  if (props.shape.kind === "line") return <span class={`shape-preview shape-preview-${props.shape.line ?? "line"}`} />;
  if (props.shape.kind === "circle") return <span class="shape-preview shape-preview-circle" />;
  if (props.shape.kind === "rect") return <span class="shape-preview shape-preview-rect" />;
  if (props.shape.kind === "polygon") return <span class="shape-preview shape-preview-poly">{label}</span>;
  if (props.shape.kind === "composite") return <span class="shape-preview shape-preview-composite">{label}</span>;
  return <span class="shape-preview shape-preview-path">{label}</span>;
}

function IconButton(props: {
  icon: string;
  label: string;
  active?: boolean;
  disabled?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      class="icon-btn"
      classList={{ active: !!props.active }}
      title={props.label}
      aria-label={props.label}
      onClick={props.onClick}
      disabled={props.disabled}
    >
      <Icon name={props.icon} />
    </button>
  );
}

function Icon(props: { name: string }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      {iconContent(props.name)}
    </svg>
  );
}

function iconContent(name: string) {
  switch (name) {
    case "pointer":
      return <path d="M5 3 L18 14 L12 15 L9 21 L5 3 Z" />;
    case "hand":
      return <path d="M7 12 V7 M10 12 V4 M13 12 V6 M16 13 V9 M7 12 C5 12 4 13 5 15 L8 20 H15 C17 20 19 18 19 15 V11" />;
    case "magnet":
      return <path d="M6 4 V12 C6 16 9 19 12 19 C15 19 18 16 18 12 V4 M6 8 H10 M14 8 H18" />;
    case "undo":
      return <path d="M9 7 H5 V3 M5 7 C8 4 13 4 16 7 C19 10 19 15 16 18 C14 20 10 20 8 18" />;
    case "redo":
      return <path d="M15 7 H19 V3 M19 7 C16 4 11 4 8 7 C5 10 5 15 8 18 C10 20 14 20 16 18" />;
    case "copy":
      return <path d="M8 8 H18 V20 H8 Z M6 16 H4 V4 H14 V6" />;
    case "paste":
      return <path d="M8 5 H16 M9 3 H15 L16 5 H20 V21 H4 V5 H8 Z M8 10 H16 M8 14 H16 M8 18 H13" />;
    case "refresh":
    case "reload":
      return <path d="M20 7 V3 H16 M19 4 C16 2 11 2 8 5 C5 8 5 13 8 16 C11 19 16 19 19 16 M4 17 V21 H8" />;
    case "folder":
      return <path d="M3 6 H9 L11 8 H21 V18 H3 Z" />;
    case "save":
      return <path d="M5 4 H17 L20 7 V20 H4 V4 H5 Z M8 4 V10 H16 V4 M8 20 V14 H16 V20" />;
    case "build":
      return <path d="M7 4 H17 L20 8 L12 21 L4 8 Z M7 4 L12 21 M17 4 L12 21 M4 8 H20" />;
    case "text":
      return <path d="M5 6 H19 M12 6 V19 M9 19 H15" />;
    case "table":
      return <path d="M4 5 H20 V19 H4 Z M4 10 H20 M4 15 H20 M10 5 V19 M16 5 V19" />;
    case "bar":
      return <path d="M5 17 H19 M7 17 V10 H10 V17 M12 17 V6 H15 V17 M17 17 V12 H20" />;
    case "tick":
      return <path d="M4 12 H20 M6 8 V16 M10 9 V15 M14 8 V16 M18 9 V15" />;
    case "grid":
      return <path d="M4 4 H20 V20 H4 Z M4 9 H20 M4 14 H20 M9 4 V20 M14 4 V20" />;
    case "fraction":
      return <path d="M9 6 H15 M8 12 H16 M9 18 H15" />;
    case "mixedFraction":
      return <path d="M4 15 V9 M7 15 V9 M11 6 H17 M10 12 H18 M11 18 H17" />;
    case "shapes":
      return <path d="M5 15 L10 5 L15 15 Z M14 7 H20 V13 H14 Z M8 18 H18" />;
    case "rect":
      return <rect x="5" y="7" width="14" height="10" />;
    case "circle":
      return <circle cx="12" cy="12" r="7" />;
    case "line":
      return <path d="M5 18 L19 6" />;
    case "triangle":
      return <path d="M12 5 L20 18 H4 Z" />;
    case "curve":
      return <path d="M4 17 C8 4 14 20 20 7" />;
    case "image":
      return <path d="M4 5 H20 V19 H4 Z M7 15 L10 12 L13 15 L15 13 L19 17 M8 9 H8.5" />;
    case "trash":
      return <path d="M5 7 H19 M9 7 V5 H15 V7 M8 7 L9 20 H15 L16 7" />;
    case "alignLeft":
      return <path d="M5 5 V19 M8 7 H19 M8 12 H15 M8 17 H19" />;
    case "alignCenter":
      return <path d="M12 5 V19 M6 7 H18 M8 12 H16 M6 17 H18" />;
    case "alignRight":
      return <path d="M19 5 V19 M5 7 H16 M9 12 H16 M5 17 H16" />;
    case "alignTop":
      return <path d="M5 5 H19 M7 8 V19 M12 8 V15 M17 8 V19" />;
    case "alignMiddle":
      return <path d="M5 12 H19 M7 5 V19 M12 8 V16 M17 5 V19" />;
    case "alignBottom":
      return <path d="M5 19 H19 M7 5 V16 M12 9 V16 M17 5 V16" />;
    case "front":
      return <path d="M8 8 H18 V18 H8 Z M5 5 H15 V8 M5 5 V15 H8" />;
    case "back":
      return <path d="M6 6 H16 V16 H6 Z M9 9 H19 V19 H9" />;
    case "forward":
      return <path d="M7 9 H17 V19 H7 Z M10 5 H21 V16 M10 5 V9" />;
    case "backward":
      return <path d="M7 5 H17 V15 H7 Z M10 9 H21 V20 M10 15 V20" />;
    default:
      return <circle cx="12" cy="12" r="7" />;
  }
}

function toInt(value: string, min: number, max: number, fallback: number): number {
  const numeric = Number(value);
  const clean = Number.isFinite(numeric) ? Math.trunc(numeric) : fallback;
  return Math.max(min, Math.min(max, clean));
}
