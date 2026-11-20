// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:async';
import 'dart:convert';
import 'dart:html' as html;

class StudentPreviewBridge {
  StudentPreviewBridge(
      {required void Function(Map<String, dynamic>) onContent,
      required void Function(bool) onResult,
      required void Function(String) onError}) {
    _subscription = html.window.onMessage.listen((event) {
      // dart:html hides another frame's Window in MessageEvent.source.
      if (event.origin != html.window.location.origin || event.data is! Map) {
        return;
      }
      final message =
          jsonDecode(jsonEncode(event.data)) as Map<String, dynamic>;
      switch (message['type']) {
        case 'modu-math:student-content':
          if (message['content'] is Map<String, dynamic>) {
            onContent(message['content']);
          }
          break;
        case 'modu-math:student-result':
          if (message['correct'] is bool) onResult(message['correct']);
          break;
        case 'modu-math:student-error':
          onError('${message['error']}');
          break;
      }
    });
  }
  late final StreamSubscription<html.MessageEvent> _subscription;
  void ready() => _post({'type': 'modu-math:student-ready'});
  void submit(dynamic answer, String revision) => _post({
        'type': 'modu-math:student-submit',
        'answer': answer,
        'revision': revision
      });
  void dispose() => _subscription.cancel();
  void _post(Map<String, dynamic> message) {
    html.window.parent?.postMessage(message, html.window.location.origin);
  }
}
