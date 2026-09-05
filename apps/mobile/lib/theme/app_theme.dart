import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Semantic colours shared by every screen.
/// Legacy names remain as aliases while feature widgets migrate gradually.
class KidsPalette {
  static const canvas = Color(0xFFF8FAFF);
  static const paper = Color(0xFFFFFFFF);
  static const primary = Color(0xFF4F46E5);
  static const primaryDark = Color(0xFF3730A3);
  static const primarySoft = Color(0xFFEEF2FF);
  static const ink = Color(0xFF1E1B4B);
  static const inkSoft = Color(0xFF5F6475);
  static const line = Color(0xFFE1E5F2);
  static const success = Color(0xFF10B981);
  static const successSoft = Color(0xFFECFDF5);
  static const warning = Color(0xFFF59E0B);
  static const warningSoft = Color(0xFFFFFBEB);
  static const error = Color(0xFFEF4444);
  static const errorSoft = Color(0xFFFEF2F2);

  static const cream = canvas;
  static const sage = primary;
  static const olive = inkSoft;
  static const cocoa = ink;
  static const cocoaSoft = inkSoft;
  static const butter = primarySoft;
  static const lemon = warning;
  static const coral = error;
  static const mint = successSoft;
  static const apricot = warningSoft;
}

class AppRadii {
  static const small = 12.0;
  static const medium = 18.0;
  static const large = 24.0;
  static const extraLarge = 32.0;
}

class AppLayout {
  static const maxContentWidth = 1200.0;

  static double horizontalPadding(double width) {
    if (width >= 1024) return 40;
    if (width >= 600) return 24;
    return 16;
  }
}

ThemeData buildKidsTheme() {
  const scheme = ColorScheme.light(
    primary: KidsPalette.primary,
    onPrimary: Colors.white,
    primaryContainer: KidsPalette.primarySoft,
    onPrimaryContainer: KidsPalette.ink,
    secondary: KidsPalette.warning,
    onSecondary: KidsPalette.ink,
    secondaryContainer: KidsPalette.warningSoft,
    onSecondaryContainer: KidsPalette.ink,
    tertiary: KidsPalette.success,
    onTertiary: Colors.white,
    tertiaryContainer: KidsPalette.successSoft,
    onTertiaryContainer: KidsPalette.ink,
    error: KidsPalette.error,
    onError: Colors.white,
    errorContainer: KidsPalette.errorSoft,
    onErrorContainer: KidsPalette.ink,
    surface: KidsPalette.paper,
    onSurface: KidsPalette.ink,
    onSurfaceVariant: KidsPalette.inkSoft,
    surfaceContainerLowest: KidsPalette.paper,
    surfaceContainerLow: KidsPalette.canvas,
    surfaceContainer: KidsPalette.primarySoft,
    surfaceContainerHigh: Color(0xFFE8EBF8),
    surfaceContainerHighest: Color(0xFFE1E5F2),
    outline: Color(0xFF7A8092),
    outlineVariant: KidsPalette.line,
  );

  final base = GoogleFonts.notoSansKrTextTheme();
  final textTheme = base.copyWith(
    displaySmall: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 40,
      fontWeight: FontWeight.w800,
      height: 1.18,
      letterSpacing: -1,
    ),
    headlineMedium: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 28,
      fontWeight: FontWeight.w800,
      height: 1.25,
    ),
    headlineSmall: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 24,
      fontWeight: FontWeight.w800,
      height: 1.3,
    ),
    titleLarge: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 21,
      fontWeight: FontWeight.w800,
      height: 1.3,
    ),
    titleMedium: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 17,
      fontWeight: FontWeight.w700,
      height: 1.4,
    ),
    bodyLarge: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 17,
      fontWeight: FontWeight.w500,
      height: 1.55,
    ),
    bodyMedium: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 15,
      fontWeight: FontWeight.w500,
      height: 1.5,
    ),
    bodySmall: GoogleFonts.notoSansKr(
      color: KidsPalette.inkSoft,
      fontSize: 13,
      fontWeight: FontWeight.w500,
      height: 1.45,
    ),
    labelLarge: GoogleFonts.notoSansKr(
      fontSize: 15,
      fontWeight: FontWeight.w800,
    ),
  );

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: KidsPalette.canvas,
    textTheme: textTheme,
    fontFamily: GoogleFonts.notoSansKr().fontFamily,
    visualDensity: VisualDensity.standard,
    materialTapTargetSize: MaterialTapTargetSize.padded,
    splashFactory: InkSparkle.splashFactory,
    appBarTheme: AppBarTheme(
      backgroundColor: KidsPalette.canvas.withValues(alpha: 0.96),
      foregroundColor: KidsPalette.ink,
      surfaceTintColor: Colors.transparent,
      centerTitle: false,
      elevation: 0,
      scrolledUnderElevation: 0,
      toolbarHeight: 72,
      titleTextStyle: textTheme.titleLarge,
    ),
    cardTheme: CardThemeData(
      color: KidsPalette.paper,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadii.large),
        side: const BorderSide(color: KidsPalette.line),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: KidsPalette.primary,
        foregroundColor: Colors.white,
        disabledBackgroundColor: KidsPalette.line,
        disabledForegroundColor: KidsPalette.inkSoft,
        minimumSize: const Size(52, 56),
        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 14),
        shape: const StadiumBorder(),
        textStyle: textTheme.labelLarge,
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: KidsPalette.primary,
        backgroundColor: KidsPalette.paper,
        minimumSize: const Size(52, 56),
        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 14),
        side: const BorderSide(color: KidsPalette.line, width: 1.5),
        shape: const StadiumBorder(),
        textStyle: textTheme.labelLarge,
      ),
    ),
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: KidsPalette.primary,
        minimumSize: const Size(48, 48),
        shape: const StadiumBorder(),
        textStyle: textTheme.labelLarge,
      ),
    ),
    iconButtonTheme: IconButtonThemeData(
      style: IconButton.styleFrom(
        foregroundColor: KidsPalette.ink,
        minimumSize: const Size.square(48),
      ),
    ),
    listTileTheme: const ListTileThemeData(
      iconColor: KidsPalette.primary,
      minTileHeight: 64,
      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 6),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: KidsPalette.primarySoft,
      selectedColor: KidsPalette.primary,
      disabledColor: KidsPalette.line,
      side: const BorderSide(color: KidsPalette.line),
      shape: const StadiumBorder(),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      labelStyle: textTheme.labelLarge?.copyWith(color: KidsPalette.ink),
      secondaryLabelStyle: textTheme.labelLarge?.copyWith(color: Colors.white),
      showCheckmark: false,
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: KidsPalette.paper,
      contentPadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadii.medium),
        borderSide: const BorderSide(color: KidsPalette.line),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadii.medium),
        borderSide: const BorderSide(color: KidsPalette.line, width: 1.5),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadii.medium),
        borderSide: const BorderSide(color: KidsPalette.primary, width: 2),
      ),
    ),
    progressIndicatorTheme: const ProgressIndicatorThemeData(
      color: KidsPalette.primary,
      linearTrackColor: KidsPalette.line,
    ),
    dialogTheme: DialogThemeData(
      backgroundColor: KidsPalette.paper,
      surfaceTintColor: Colors.transparent,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadii.large),
      ),
    ),
    bottomSheetTheme: const BottomSheetThemeData(
      backgroundColor: KidsPalette.paper,
      surfaceTintColor: Colors.transparent,
      showDragHandle: true,
    ),
    dividerTheme: const DividerThemeData(color: KidsPalette.line, space: 32),
    tabBarTheme: TabBarThemeData(
      labelColor: KidsPalette.primary,
      unselectedLabelColor: KidsPalette.inkSoft,
      indicatorColor: KidsPalette.primary,
      dividerColor: KidsPalette.line,
      labelStyle: textTheme.labelLarge,
      unselectedLabelStyle: textTheme.labelLarge,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: KidsPalette.primary,
      foregroundColor: Colors.white,
      shape: CircleBorder(),
    ),
  );
}
