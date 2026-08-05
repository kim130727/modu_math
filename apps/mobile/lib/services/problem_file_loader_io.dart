import 'dart:io';

Future<List<String>> loadLocalRendererPaths(String rootPath) async {
  final root = Directory(rootPath);
  if (!await root.exists()) {
    throw StateError('Local problem directory does not exist: $rootPath');
  }

  final paths = <String>[];
  await for (final entity in root.list(recursive: true, followLinks: false)) {
    if (entity is! File) {
      continue;
    }
    final path = _normalizePath(entity.path);
    if (path.endsWith('.renderer.json')) {
      paths.add(path);
    }
  }
  paths.sort();
  return paths;
}

Future<String> loadLocalText(String path) async {
  final file = File(path);
  if (!await file.exists()) {
    throw MissingLocalContent(path);
  }
  return file.readAsString();
}

String _normalizePath(String path) {
  return path.replaceAll(r'\', '/');
}

class MissingLocalContent implements Exception {
  const MissingLocalContent(this.path);

  final String path;

  @override
  String toString() => 'Missing local content: $path';
}
