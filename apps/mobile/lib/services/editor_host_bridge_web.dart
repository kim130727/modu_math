// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use

import 'dart:async';
import 'dart:html' as html;

import '../widgets/renderer_json_canvas.dart';

class EditorHostBridge {
  EditorHostBridge({
    void Function(Map<String, dynamic> renderer)? onRenderer,
    void Function(String? elementId)? onSelection,
    void Function(RendererCanvasMode mode)? onMode,
  })  : _onRenderer = onRenderer,
        _onSelection = onSelection,
        _onMode = onMode {
    _subscription = html.window.onMessage.listen((event) {
      final raw = event.data;
      if (raw is! Map) return;
      final message = Map<String, dynamic>.from(raw);
      switch (message['type']) {
        case 'modu-math:host-renderer':
          final renderer = message['renderer'];
          if (renderer is Map) {
            _onRenderer?.call(Map<String, dynamic>.from(renderer));
          }
          break;
        case 'modu-math:host-selection':
          _onSelection?.call(message['elementId']?.toString());
          break;
        case 'modu-math:host-mode':
          _onMode?.call(
            message['mode'] == 'studentTest'
                ? RendererCanvasMode.studentTest
                : RendererCanvasMode.edit,
          );
          break;
      }
    });
  }

  final void Function(Map<String, dynamic> renderer)? _onRenderer;
  final void Function(String? elementId)? _onSelection;
  final void Function(RendererCanvasMode mode)? _onMode;
  late final StreamSubscription<html.MessageEvent> _subscription;

  void ready() => _post({'type': 'modu-math:flutter-editor-ready'});

  void selected(String? elementId, String? targetId) => _post({
        'type': 'modu-math:flutter-element-selected',
        'elementId': elementId,
        'targetId': targetId,
      });

  void patch(RendererElementPatch patch) => _post({
        'type': 'modu-math:flutter-layout-patch',
        'elementId': patch.elementId,
        'targetId': patch.targetId,
        'patch': patch.toLayoutPatch(),
      });

  void mode(RendererCanvasMode mode) => _post({
        'type': 'modu-math:flutter-mode-changed',
        'mode': mode.name,
      });

  void dispose() => _subscription.cancel();

  void _post(Map<String, dynamic> message) {
    final parent = html.window.parent;
    if (parent != null && parent != html.window) {
      parent.postMessage(message, '*');
    }
  }
}
