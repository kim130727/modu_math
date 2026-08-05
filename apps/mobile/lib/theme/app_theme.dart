import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class KidsPalette {
  static const cream = Color(0xFFFAFAF7);
  static const paper = Color(0xFFFFFFFF);
  static const sage = Color(0xFF5B67F1);
  static const olive = Color(0xFF8A8F98);
  static const ink = Color(0xFF111111);
  static const cocoa = Color(0xFF111111);
  static const cocoaSoft = Color(0xFF747982);
  static const butter = Color(0xFFF1F2EE);
  static const lemon = Color(0xFFFFB84D);
  static const coral = Color(0xFFD64550);
  static const mint = Color(0xFFE9F9EF);
  static const apricot = Color(0xFFFFF7E8);
  static const line = Color(0xFFE2E3DF);

  static const success = Color(0xFF27B58A);
  static const error = Color(0xFFD64550);
  static const errorSoft = Color(0xFFFFF0F1);
  static const warning = Color(0xFFFFB84D);
}

ThemeData buildKidsTheme() {
  final scheme = ColorScheme.fromSeed(
    seedColor: KidsPalette.sage,
    brightness: Brightness.light,
  ).copyWith(
    primary: KidsPalette.sage,
    onPrimary: Colors.white,
    primaryContainer: KidsPalette.butter,
    onPrimaryContainer: KidsPalette.ink,
    secondary: KidsPalette.success,
    onSecondary: Colors.white,
    secondaryContainer: KidsPalette.mint,
    onSecondaryContainer: KidsPalette.ink,
    tertiary: KidsPalette.warning,
    onTertiary: KidsPalette.ink,
    tertiaryContainer: KidsPalette.apricot,
    onTertiaryContainer: KidsPalette.ink,
    error: KidsPalette.error,
    onError: Colors.white,
    errorContainer: KidsPalette.errorSoft,
    onErrorContainer: KidsPalette.ink,
    surface: KidsPalette.paper,
    onSurface: KidsPalette.ink,
    surfaceContainerLowest: KidsPalette.cream,
    surfaceContainerLow: KidsPalette.paper,
    surfaceContainer: KidsPalette.butter,
    surfaceContainerHigh: const Color(0xFFE1E5F2),
    outline: KidsPalette.line,
    outlineVariant: KidsPalette.line,
  );

  final baseTextTheme = GoogleFonts.notoSansKrTextTheme();
  final textTheme = baseTextTheme.copyWith(
    displaySmall: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 44,
      fontWeight: FontWeight.w800,
      height: 1.12,
    ),
    headlineSmall: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 24,
      fontWeight: FontWeight.w800,
      height: 1.2,
    ),
    titleLarge: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 22,
      fontWeight: FontWeight.w800,
      height: 1.25,
    ),
    titleMedium: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 18,
      fontWeight: FontWeight.w700,
      height: 1.3,
    ),
    bodyLarge: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 17,
      fontWeight: FontWeight.w400,
      height: 1.45,
    ),
    bodyMedium: GoogleFonts.notoSansKr(
      color: KidsPalette.ink,
      fontSize: 15,
      fontWeight: FontWeight.w400,
      height: 1.45,
    ),
    bodySmall: GoogleFonts.notoSansKr(
      color: KidsPalette.cocoaSoft,
      fontSize: 13,
      fontWeight: FontWeight.w400,
      height: 1.4,
    ),
    labelLarge: GoogleFonts.notoSansKr(
      fontSize: 15,
      fontWeight: FontWeight.w800,
    ),
  );

  return ThemeData(
    colorScheme: scheme,
    scaffoldBackgroundColor: KidsPalette.cream,
    useMaterial3: true,
    textTheme: textTheme,
    fontFamily: GoogleFonts.notoSansKr().fontFamily,
    appBarTheme: AppBarTheme(
      backgroundColor: Colors.transparent,
      foregroundColor: KidsPalette.ink,
      centerTitle: false,
      elevation: 0,
      scrolledUnderElevation: 0,
      titleTextStyle: textTheme.titleLarge,
    ),
    tabBarTheme: TabBarThemeData(
      labelColor: KidsPalette.sage,
      unselectedLabelColor: KidsPalette.olive,
      indicatorColor: KidsPalette.sage,
      labelStyle: GoogleFonts.notoSansKr(fontWeight: FontWeight.w800),
      unselectedLabelStyle: GoogleFonts.notoSansKr(fontWeight: FontWeight.w600),
    ),
    cardTheme: CardThemeData(
      color: KidsPalette.paper,
      surfaceTintColor: Colors.transparent,
      elevation: 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: KidsPalette.line),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: KidsPalette.sage,
        foregroundColor: Colors.white,
        minimumSize: const Size(48, 48),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        textStyle: const TextStyle(fontWeight: FontWeight.w800),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: KidsPalette.sage,
        minimumSize: const Size(48, 48),
        side: const BorderSide(color: KidsPalette.line, width: 1.4),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        textStyle: const TextStyle(fontWeight: FontWeight.w800),
      ),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: KidsPalette.butter,
      selectedColor: KidsPalette.mint,
      side: const BorderSide(color: KidsPalette.line),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      labelStyle: const TextStyle(
        color: KidsPalette.ink,
        fontWeight: FontWeight.w700,
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: KidsPalette.paper,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: KidsPalette.line),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: KidsPalette.line),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: KidsPalette.sage, width: 1.6),
      ),
    ),
    dividerTheme: const DividerThemeData(color: KidsPalette.line, space: 32),
  );
}
