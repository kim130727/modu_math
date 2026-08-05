import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'app/app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (kIsWeb) {
    dotenv.loadFromString(envString: '', isOptional: true);
  } else {
    await dotenv.load(fileName: '.env', isOptional: true);
  }
  runApp(const ModuMathApp());
}
