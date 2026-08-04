Future<List<String>> loadLocalRendererPaths(String rootPath) {
  throw UnsupportedError(
      'Local problem files are not available on this platform.');
}

Future<String> loadLocalText(String path) {
  throw UnsupportedError(
      'Local problem files are not available on this platform.');
}

class MissingLocalContent implements Exception {
  const MissingLocalContent(this.path);

  final String path;

  @override
  String toString() => 'Missing local content: $path';
}
