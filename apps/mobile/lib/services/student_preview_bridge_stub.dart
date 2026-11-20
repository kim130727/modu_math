class StudentPreviewBridge {
  StudentPreviewBridge(
      {required void Function(Map<String, dynamic>) onContent,
      required void Function(bool) onResult,
      required void Function(String) onError});
  void ready() {}
  void submit(dynamic answer, String revision) {}
  void dispose() {}
}
