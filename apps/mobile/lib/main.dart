import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/app_strings.dart';
import 'screens/student_assignments_screen.dart';
import 'screens/student_preview_screen.dart';
import 'package:flutter/foundation.dart';
import 'services/auth_service.dart';
import 'theme/app_theme.dart';
import 'widgets/language_toggle_button.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  WidgetsBinding.instance.ensureSemantics();
  runApp(const StudentApp());
}

/// One application for students and the editor's isolated solve preview.
class StudentApp extends StatefulWidget {
  const StudentApp({super.key});
  @override
  State<StudentApp> createState() => _StudentAppState();
}

class _StudentAppState extends State<StudentApp> {
  final auth = AuthService();
  Locale locale = const Locale('ko');
  @override
  Widget build(BuildContext context) => AppLocaleScope(
      locale: locale,
      onLocaleChanged: (value) => setState(() => locale = value),
      child: MaterialApp(
        title: 'Modu Math · Learning',
        debugShowCheckedModeBanner: false,
        theme: buildKidsTheme(),
        locale: locale,
        localizationsDelegates: const [
          AppStringsDelegate(),
          GlobalMaterialLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate
        ],
        supportedLocales: AppStrings.supportedLocales,
        home: kIsWeb && Uri.base.queryParameters['studentPreview'] == '1'
            ? const StudentPreviewScreen()
            : StudentAssignmentsScreen(authService: auth),
        builder: (context, child) => Stack(children: [
          if (child != null) child,
          const PositionedDirectional(
              top: 8, end: 8, child: SafeArea(child: LanguageToggleButton()))
        ]),
      ));
}
