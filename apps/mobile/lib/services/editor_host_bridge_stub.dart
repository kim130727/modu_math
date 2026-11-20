import '../widgets/renderer_json_canvas.dart';

class EditorHostBridge {
  EditorHostBridge({
    void Function(Map<String, dynamic> renderer)? onRenderer,
    void Function(Map<String, dynamic> problem)? onProblem,
    void Function(String? elementId)? onSelection,
    void Function(RendererCanvasMode mode)? onMode,
  });

  void ready() {}
  void selected(String? elementId, String? targetId) {}
  void patch(RendererElementPatch patch) {}
  void mode(RendererCanvasMode mode) {}
  void dispose() {}
}
