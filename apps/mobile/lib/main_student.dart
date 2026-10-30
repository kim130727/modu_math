import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/app_strings.dart';
import 'screens/student_assignments_screen.dart';
import 'services/auth_service.dart';
import 'theme/app_theme.dart';
import 'widgets/language_toggle_button.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  WidgetsBinding.instance.ensureSemantics();
  runApp(const StudentAssignmentApp());
}

/// The deployable student entry does not import offline repositories or editors.
class StudentAssignmentApp extends StatefulWidget {
  const StudentAssignmentApp({super.key});
  @override
  State<StudentAssignmentApp> createState() => _StudentAssignmentAppState();
}

class _StudentAssignmentAppState extends State<StudentAssignmentApp> {
  final auth = AuthService();
  Locale locale = const Locale('ko');
  @override
  Widget build(BuildContext context) => AppLocaleScope(
      locale: locale,
      onLocaleChanged: (value) => setState(() => locale = value),
      child: MaterialApp(
        title: 'Modu Math · Assignments',
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
        home: StudentAssignmentsScreen(authService: auth),
        builder: (context, child) => Stack(children: [
          if (child != null) child,
          const PositionedDirectional(
              top: 8, end: 8, child: SafeArea(child: LanguageToggleButton()))
        ]),
      ));
}
