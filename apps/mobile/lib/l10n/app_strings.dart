import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app_strings_bundle.dart';

class AppStrings {
  const AppStrings(this._values);

  final Map<String, String> _values;

  static const supportedLocales = [
    Locale('ko'),
    Locale('uk'),
    Locale('en'),
    Locale('zh'),
    Locale('ja'),
    Locale('km'),
  ];

  static const fallback = AppStrings({
    'app.title': '모두수학',
    'language.tooltip': '언어 변경',
    'language.ko': '한국어',
    'language.en': 'English',
    'language.zh': '中文',
    'language.ja': '日本語',
    'language.km': 'ភាសាខ្មែរ',
    'language.uk': 'Українська',
    'common.grade': '레벨 {grade}',
    'common.problemCount': '{count}문제',
    'common.itemCount': '{count}개',
    'common.problemTitleForTopic': '{topic} 문제',
    'common.retry': '다시 시도',
    'common.reload': '다시 불러오기',
    'common.previousProblem': '이전 문제로',
    'common.nextProblem': '다음 문제로',
    'common.back': '이전 화면으로',
    'home.loadErrorTitle': '학습 정보를 불러오지 못했어요',
    'home.retry': '다시 시도',
    'home.reviewTooltip': '오답 노트',
    'home.reportTooltip': '학습 리포트',
    'home.heroTitle': '오늘은 한 문제씩\n생각해 볼까요?',
    'home.heroSubtitle': '맞춤 문제로 풀이 단계를 천천히 확인해요.',
    'home.startToday': '오늘 학습 시작',
    'home.chooseUnit': '단원에서 고르기',
    'home.today': '오늘',
    'home.accuracy': '정답률',
    'home.nextProblem': '다음 문제',
    'home.todayProblem': '오늘의 문제',
    'home.recommendationLoading': '추천 문제를 준비하고 있어요.',
    'home.unitLearning': '단원별 학습',
    'home.problemCount': '{count}문제',
    'home.prevUnit': '이전 단원',
    'home.nextUnit': '다음 단원',
    'home.loading': '오늘의 문제를 고르고 있어요',
    'answer.inputLabel': '답 입력',
    'answer.check': '정답 확인',
    'answer.showSolution': '힌트 보기',
    'answer.correct': '맞았어요!',
    'answer.incorrectWithAnswer': '다시 확인해 봐요. 힌트를 보고 한 번 더 생각해 봐요.',
    'answer.promptChoiceGroups': '각 항목에 알맞은 정답을 선택하세요',
    'answer.promptMultipleChoices': '알맞은 정답을 모두 선택하세요',
    'answer.promptSingleChoice': '알맞은 정답을 선택하세요',
    'answer.promptOx': '알맞은 답(○ 또는 ✕)을 선택하세요',
    'answer.oxTag': 'O / X',
    'answer.oxTrue': '참',
    'answer.oxFalse': '거짓',
    'answer.promptBlanks': '문제의 빈칸에 정답을 입력하세요',
    'answer.promptMultiAnswer': '각 물음에 알맞은 정답을 입력하세요',
    'answer.promptDefault': '정답을 입력하세요',
    'answer.checkAllBlanks': '왼쪽 문제의 빈칸을 순서대로 입력한 뒤 정답을 확인하세요.',
    'answer.keypadTooltip': '수학 키패드',
    'keypad.backspace': '지우기',
    'keypad.clearAll': '전체 지우기',
    'keypad.next': '다음',
    'keypad.nextBlank': '다음 빈칸',
    'keypad.reset': '초기화',
    'hint.title': '단계별 힌트',
    'hint.showHint': '힌트 보기',
    'hint.allRevealed': '모든 힌트를 봤어요',
    'hint.intro': '막히면 힌트를 한 단계씩 열어 보세요.',
    'hint.checkAnswer': '답 확인',
    'hint.confirm': '확인',
    'hint.tryAgain': '조금 달라요. 힌트를 다시 읽고 한 번 더 생각해 봐요.',
    'tutor.myAnswer': '내 답',
    'tutor.viewSolutionProcess': '풀이 과정 보기',
    'progress.title': '학습 결과',
    'progress.solved': '푼 문제',
    'progress.correct': '맞힌 문제',
    'progress.reviewAgain': '다시 볼 문제',
    'solution.title': '풀이 단계',
    'solution.empty': '등록된 풀이 단계가 없습니다.',
    'curriculum.title': '단원 학습',
    'curriculum.loadError': '단원 정보를 불러오지 못했어요.\n{error}',
    'curriculum.empty': '아직 학습할 문제가 없어요.',
    'curriculum.headerTitle': '오늘 배울 단원을 골라요',
    'curriculum.headerDescription': '단원을 고르면 문제 풀이와 온셈이가 바로 이어집니다.',
    'curriculum.groupTitle': '{domain}',
    'curriculum.domain.수와 연산': '수와 연산',
    'curriculum.domain.도형': '도형',
    'curriculum.domain.측정': '측정',
    'curriculum.domain.자료와 가능성': '자료와 가능성',
    'curriculum.domain.수학 개념': '수학 개념',
    'curriculum.unknownSemester': '단원 미정',
    'curriculum.semester.1학기': '1학기',
    'curriculum.semester.2학기': '2학기',
    'curriculum.semester.학기 미정': '단원 미정',
    'curriculum.topic.덧셈과 뺄셈': '덧셈과 뺄셈',
    'curriculum.topic.평면도형': '평면도형',
    'curriculum.topic.나눗셈': '나눗셈',
    'curriculum.topic.곱셈': '곱셈',
    'curriculum.topic.길이와 시간': '길이와 시간',
    'curriculum.topic.분수와 소수': '분수와 소수',
    'curriculum.topic.원': '원',
    'curriculum.topic.분수': '분수',
    'curriculum.topic.들이와 무게': '들이와 무게',
    'curriculum.topic.자료의 정리': '자료의 정리',
    'curriculum.viewAllUnits': '전체 단원 보기',
    'curriculum.unitDetailTitle': '{unit} 학습',
    'curriculum.startWholeUnit': '전체 단원 학습 시작 ({count}문제)',
    'curriculum.startWholeUnitShort': '전체 학습',
    'curriculum.subUnitSection': '소단원 선택 학습',
    'curriculum.subUnitSolve': '학습하기',
    'curriculum.defaultSubUnit': '기본 학습',
    'curriculum.exploreOtherUnits': '다른 단원 둘러보기',
    'curriculum.loading': '단원을 준비하고 있어요',
    'session.title': '학습 세션',
    'session.loading': '학습 세션을 준비하고 있어요',
    'problem.loading': '문제를 불러오고 있어요',
    'problemList.loading': '문제 목록을 모으고 있어요',
    'review.loading': '노트를 살펴보고 있어요',
    'report.loading': '학습 리포트를 정리하고 있어요',
    'studio.loading': '미리보기를 준비하고 있어요',
    'session.loadError': '학습 세션을 준비하지 못했어요.\n{error}',
    'session.empty': '이 단원에는 아직 문제가 없어요.',
    'session.resume': '이어 풀기',
    'session.retry': '다시 풀기',
    'session.completedCount': '{solved} / {total} 문제 완료',
    'session.allComplete': '모두 풀었어요. 다시 연습할 수 있어요.',
    'session.nextProblemLabel': '다음 문제',
    'session.nextProblemSubtitle': '다음에 풀 문제 · {title}',
    'problem.loadErrorTutor': '튜터 응답을 가져오지 못했어요. 잠시 뒤 다시 시도해 주세요.',
    'problem.noVisual': '이 문제는 아직 화면 자료가 없어요.',
    'problem.loadErrorTitle': '문제 자료를 불러오지 못했어요',
    'problem.loadErrorDescription': '다시 시도하거나 다음 문제로 넘어갈 수 있어요.',
    'problemList.loadError': '문제 목록을 불러오지 못했어요.\n{error}',
    'problemList.journeyDescription': '온셈이와 {count}개의 문제를 차례대로 풀어봅니다.',
    'problemList.solve': '풀기',
    'problemList.done': '완료',
    'problemList.startWithTutor': '온셈이로 시작',
    'tutor.title': '온셈이',
    'tutor.subtitle': '문제를 한 단계씩 같이 풀어요.',
    'tutor.voiceOffTooltip': '자동 읽기 끄기',
    'tutor.voiceOnTooltip': '자동 읽기 켜기',
    'tutor.replayTooltip': '마지막 튜터 말 다시 듣기',
    'tutor.restart': '다시 시작',
    'tutor.start': '시작',
    'tutor.nextStep': '다음 단계',
    'tutor.reset': '초기화',
    'tutor.nextProblem': '다음 문제로',
    'tutor.finishUnit': '단원 마치기',
    'tutor.emptyConversation': '시작하면 온셈이가 한 단계씩 도와줄게요.',
    'tutor.hint': '힌트',
    'tutor.chatInput': '궁금한 점을 직접 입력하거나 보기를 눌러 보세요.',
    'tutor.stopListeningTooltip': '듣는 중지',
    'tutor.speakTooltip': '음성으로 말하기',
    'tutor.sendTooltip': '보내기',
    'tutor.defaultLatest': '준비됐어요. 같이 풀어볼까요?',
    'tutor.noTextToRead': '아직 읽어 줄 튜터 말이 없어요.',
    'tutor.voiceUnavailable': '브라우저에서 음성 읽기를 사용할 수 없어요.',
    'tutor.thinking': '생각하고 있어요.',
    'tutor.firstQuestionPlaceholder': '시작하면 첫 번째 확인할 내용을 보여줄게요.',
    'tutor.correctReview': '맞아요! 다음 문제로 넘어가도 좋아요.',
    'tutor.incorrectReview': '조금만 다시 볼게요. 필요한 단계부터 같이 확인해요.',
    'tutor.student': '학생',
    'review.title': '오답노트 & 사고 단계 복습',
    'review.loadError': '오답노트를 불러올 수 없습니다: {error}',
    'review.filterTitle': '사고 원인별 필터',
    'review.all': '전체 보기',
    'review.empty': '오답 문제가 없습니다!\n꾸준한 학습으로 실력을 키워보세요.',
    'review.submittedAnswer': '제출한 답: {answer}',
    'review.headerTitle': '다시 볼 오답 {count}문제',
    'review.headerDescription': '틀린 원인을 짚어보며 다시 풀면 장기 기억으로 연결돼요.',
    'report.title': '학습 성장 리포트',
    'report.loadError': '리포트를 불러올 수 없습니다: {error}',
    'report.weaknessTitle': '사고 단계별 취약 분석',
    'report.noErrors': '아직 기록된 사고 단계 오류가 없습니다.\n문제 풀이 후 오답 원인을 기록해보세요!',
    'report.recordCount': '{count}회 기록',
    'report.masteryTitle': '단원별 개념 숙달도',
    'report.noMastery': '아직 풀어본 단원이 없습니다.',
    'report.masteryStats': '시도 문제: {count}개 | 정답률: {percent}%',
    'report.overviewTitle': '{name}의 성과 리포트',
    'report.streak': '{days}일 연속',
    'report.totalSolved': '누적 푼 문제',
    'report.overallAccuracy': '전체 정답률',
    'report.grade': '학습 학년',
    'mastery.notStarted': '시작 전',
    'mastery.good': '잘하고 있어요',
    'mastery.practicing': '연습 중',
    'mastery.needsReview': '복습 필요',
    'errorCategory.understanding_target': '문제 목표 이해 부족',
    'errorCategory.understanding_given': '주어진 조건 해석 오류',
    'errorCategory.planning_concept': '개념 연결 오류',
    'errorCategory.planning_operation': '연산/해결 계획 선택 오류',
    'errorCategory.execution_calculation': '계산 실수',
    'errorCategory.execution_representation': '표현 또는 식 작성 오류',
    'errorCategory.review_condition': '조건 확인 부족',
    'errorCategory.review_unit': '단위 또는 최종 검토 오류',
    'errorCategory.none': '오류 없음',
    'errorSheet.title': '어느 생각 단계에서 아쉬웠나요?',
    'errorSheet.description': '원인을 기록하면 다음 학습에서 온셈이가 더 알맞은 힌트를 준비할 수 있어요.',
    'errorSheet.understanding_target.title': '구하려는 것 놓침',
    'errorSheet.understanding_target.description': '문제에서 무엇을 구해야 하는지 잘 못 봤어요.',
    'errorSheet.understanding_given.title': '주어진 조건 해석 실수',
    'errorSheet.understanding_given.description': '주어진 숫자나 수식 조건을 다르게 읽었어요.',
    'errorSheet.planning_concept.title': '개념/공식 연결 오류',
    'errorSheet.planning_concept.description': '어떤 수학 개념이나 법칙을 써야 할지 생각 안 났어요.',
    'errorSheet.planning_operation.title': '연산 순서/식 세우기 오류',
    'errorSheet.planning_operation.description':
        '덧셈, 뺄셈, 곱셈, 나눗셈 등 해결 순서를 틀렸어요.',
    'errorSheet.execution_calculation.title': '아쉬운 계산 실수',
    'errorSheet.execution_calculation.description':
        '식은 맞았는데 사칙연산 계산에서 오차가 생겼어요.',
    'errorSheet.review_unit.title': '단위 또는 마지막 검산 부족',
    'errorSheet.review_unit.description': '단위(cm, 개 등)를 빠뜨렸거나 검산을 안 했어요.',
    'studio.noRenderableProblems': '렌더링 가능한 문제 자료가 없어요.',
    'studio.tutorLoadError': '튜터 응답을 받지 못했어요. 잠시 후 다시 시도해 주세요.',
    'studio.description': 'JSON 렌더링과 문제 구조를 한 화면에서 확인합니다.',
    'studio.problemListTooltip': '기존 문제 목록',
    'studio.defaultInstruction': '렌더링 데이터를 확인합니다.',
    'studio.loadError': 'JSON 문제를 불러오지 못했습니다.\n{error}',
    'loading.default': '온셈이가 문제를 준비하고 있어요',
    'common.close': '닫기',
    'auth.screenTitle': '학습 계정 로그인',
    'auth.loginTab': '로그인',
    'auth.registerTab': '회원가입',
    'auth.usernameLabel': '아이디 (사용자 이름)',
    'auth.usernameRequired': '아이디를 입력해 주세요.',
    'auth.passwordLabel': '비밀번호',
    'auth.passwordRequired': '비밀번호를 입력해 주세요.',
    'auth.loginButton': '로그인하기',
    'auth.emailOptionalLabel': '이메일 (선택)',
    'auth.registerPasswordLabel': '비밀번호 (8자 이상)',
    'auth.passwordMinLength': '8자 이상 입력해 주세요.',
    'auth.confirmPasswordLabel': '비밀번호 확인',
    'auth.confirmPasswordRequired': '비밀번호 확인을 입력해 주세요.',
    'auth.passwordsDoNotMatch': '비밀번호가 일치하지 않습니다.',
    'auth.registerButton': '회원가입 완료',
    'auth.accountTitle': '{username} 님의 계정',
    'auth.syncMessage': '현재 로그인되어 학습 기록이 백엔드 서버와 안전하게 동기화되고 있습니다.',
    'auth.logout': '로그아웃',
    'auth.learner': '학습자',
    'auth.manageAccount': '{username} (계정 관리)',
    'auth.login': '로그인',
    'auth.loginFailed': '로그인에 실패했습니다.',
    'auth.registerFailed': '회원가입에 실패했습니다.',
    'auth.networkError': '서버와 통신하는 중 오류가 발생했습니다.',
    'diagnostic.unauthenticatedTitle': '로그인하고 나만의 수학 진단을 받아보세요!',
    'diagnostic.unauthenticatedDescription': '문제를 풀 때마다 개념과 역량 숙련도가 자동으로 분석되고,\n취약점을 보완하는 맞춤 문제가 추천됩니다.',
    'diagnostic.loginOrRegister': '로그인 / 회원가입하기',
  });

  static AppStrings of(BuildContext context) {
    final activeLocale = AppLocaleScope.maybeOf(context)?.locale;
    if (activeLocale != null) {
      final code = activeLocale.languageCode;
      if (bundledTranslations.containsKey(code)) {
        return AppStrings(bundledTranslations[code]!);
      }
    }
    return Localizations.of<AppStrings>(context, AppStrings) ?? fallback;
  }

  static AppStrings forLocale(Locale locale, {BuildContext? context}) {
    final code = locale.languageCode;
    if (bundledTranslations.containsKey(code)) {
      return AppStrings(bundledTranslations[code]!);
    }
    if (context != null) {
      final loc = Localizations.of<AppStrings>(context, AppStrings);
      if (loc != null) return loc;
    }
    return fallback;
  }

  static Future<AppStrings> load(Locale locale) async {
    final languageCode = locale.languageCode;
    if (bundledTranslations.containsKey(languageCode)) {
      return SynchronousFuture<AppStrings>(
        AppStrings(bundledTranslations[languageCode]!),
      );
    }
    try {
      final raw = await rootBundle.loadString('assets/i18n/$languageCode.json');
      final decoded = jsonDecode(raw) as Map<String, dynamic>;
      return AppStrings({
        ...fallback._values,
        ...decoded.map((key, value) => MapEntry(key, value.toString())),
      });
    } on Object {
      return fallback;
    }
  }

  bool hasKey(String key) => _values.containsKey(key);

  String t(String key, [Map<String, Object?> args = const {}]) {
    var value = _values[key] ?? fallback._values[key] ?? key;
    for (final entry in args.entries) {
      value = value.replaceAll('{${entry.key}}', entry.value.toString());
    }
    return value;
  }

  String grade(int grade) => t('common.grade', {'grade': grade});

  String problemCount(int count) => t('common.problemCount', {'count': count});

  String itemCount(int count) => t('common.itemCount', {'count': count});

  String problemTitle(String value) {
    const suffix = ' 문제';
    if (!value.endsWith(suffix)) {
      return unitTitle(value);
    }
    final topic = value.substring(0, value.length - suffix.length).trim();
    return t('common.problemTitleForTopic', {
      'topic': unitTitle(topic),
    });
  }

  String domainTitle(String topicOrDomain) {
    final domain = switch (topicOrDomain) {
      '덧셈과 뺄셈' || '나눗셈' || '곱셈' || '분수와 소수' || '분수' || '수와 연산' => '수와 연산',
      '평면도형' || '원' || '도형' => '도형',
      '길이와 시간' || '들이와 무게' || '측정' => '측정',
      '자료의 정리' || '자료와 가능성' => '자료와 가능성',
      _ => '수학 개념',
    };
    return t('curriculum.domain.$domain');
  }

  String problemTitleById(String id, [String? fallback]) {
    final suffix = id.length >= 6 ? id.substring(id.length - 6) : id;
    final key = 'problem.title.$suffix';
    if (_values.containsKey(key)) {
      return _values[key]!;
    }
    return fallback ?? (id.isNotEmpty ? id : '');
  }

  String curriculumTerm(String value) {
    if (_values.containsKey('curriculum.topic.$value')) {
      return _values['curriculum.topic.$value']!;
    }
    if (_values.containsKey('curriculum.domain.$value')) {
      return _values['curriculum.domain.$value']!;
    }
    return t('curriculum.topic.$value') == 'curriculum.topic.$value'
        ? t('curriculum.semester.$value', const {})
        : t('curriculum.topic.$value');
  }

  String semester(String value) {
    if (value == '__unknown_semester__') {
      return t('curriculum.unknownSemester');
    }
    return t('curriculum.semester.$value') == 'curriculum.semester.$value'
        ? value
        : t('curriculum.semester.$value');
  }

  String subUnitName(String value) {
    final trimmed = value.trim();
    if (trimmed == '__basicLearning__' ||
        trimmed == '기본 학습' ||
        trimmed == 'Basic Learning' ||
        trimmed == '基本学習' ||
        trimmed == '基础学习' ||
        trimmed == 'ការសិក្សាមូលដ្ឋាន' ||
        trimmed == 'Базове навчання') {
      return t('curriculum.defaultSubUnit');
    }
    if (_values.containsKey('curriculum.topic.$trimmed')) {
      return _values['curriculum.topic.$trimmed']!;
    }
    if (_values.containsKey('curriculum.domain.$trimmed')) {
      return _values['curriculum.domain.$trimmed']!;
    }
    return unitTitle(value);
  }

  String unitTitle(String value) {
    var cleaned = value;
    // Content identifiers may carry a source curriculum grade. The product UI
    // is level-neutral, so expose only the useful unit/semester/topic label.
    cleaned = cleaned.replaceFirst(
      RegExp(r'^\s*(?:초등\s*)?\d+\s*학년\s*'),
      '',
    );
    cleaned = cleaned.replaceFirst(
      RegExp(r'^\s*grade\s*\d+\s*[,·\-]?\s*', caseSensitive: false),
      '',
    );
    cleaned = cleaned.replaceFirst(
      RegExp(r'^\s*小学\s*\d+\s*年生?\s*'),
      '',
    );
    cleaned = cleaned.replaceFirst(RegExp(r'^\s*\d+\s*年级\s*'), '');
    cleaned = cleaned.replaceFirst(
      RegExp(r'^\s*\d+\s*клас(?:у|і)?\s*', caseSensitive: false),
      '',
    );
    cleaned = cleaned.replaceAll(RegExp(r'^\s*\d+학년\s*'), '');
    cleaned = cleaned.replaceAll(RegExp(r'^\s*\d+학기\s*'), '');
    cleaned = cleaned.replaceAll(RegExp(r'^\s*\d+\.\s*'), '');
    cleaned = cleaned.trim();

    if (_values.containsKey('curriculum.topic.$cleaned')) {
      return _values['curriculum.topic.$cleaned']!;
    }
    if (_values.containsKey('curriculum.domain.$cleaned')) {
      return _values['curriculum.domain.$cleaned']!;
    }

    var translated = value;
    for (final entry in _values.entries) {
      const prefix = 'curriculum.topic.';
      if (entry.key.startsWith(prefix)) {
        translated = translated.replaceAll(
            entry.key.substring(prefix.length), entry.value);
      }
    }
    for (final entry in _values.entries) {
      const prefix = 'curriculum.domain.';
      if (entry.key.startsWith(prefix)) {
        translated = translated.replaceAll(
            entry.key.substring(prefix.length), entry.value);
      }
    }
    for (final entry in _values.entries) {
      const prefix = 'curriculum.semester.';
      if (entry.key.startsWith(prefix)) {
        translated = translated.replaceAll(
            entry.key.substring(prefix.length), entry.value);
      }
    }
    return translated;
  }

  String errorCategory(String code) => t('errorCategory.$code');

  String masteryLevel(String value) {
    return switch (value) {
      '시작 전' => t('mastery.notStarted'),
      '잘하고 있어요' => t('mastery.good'),
      '연습 중' => t('mastery.practicing'),
      '복습 필요' => t('mastery.needsReview'),
      _ => value,
    };
  }
}

class AppLocaleScope extends InheritedWidget {
  const AppLocaleScope({
    super.key,
    required this.locale,
    required this.onLocaleChanged,
    required super.child,
  });

  final Locale locale;
  final ValueChanged<Locale> onLocaleChanged;

  static AppLocaleScope? maybeOf(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<AppLocaleScope>();
  }

  @override
  bool updateShouldNotify(AppLocaleScope oldWidget) {
    return locale != oldWidget.locale;
  }
}

class AppStringsDelegate extends LocalizationsDelegate<AppStrings> {
  const AppStringsDelegate();

  @override
  bool isSupported(Locale locale) {
    return AppStrings.supportedLocales
        .any((supported) => supported.languageCode == locale.languageCode);
  }

  @override
  Future<AppStrings> load(Locale locale) => AppStrings.load(locale);

  @override
  bool shouldReload(AppStringsDelegate old) => false;
}
