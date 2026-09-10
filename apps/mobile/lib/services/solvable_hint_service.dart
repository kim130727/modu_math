import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../utils/problem_text_sanitizer.dart';

class HintChoice {
  const HintChoice({
    required this.label,
    this.isCorrect = false,
  });

  final String label;
  final bool isCorrect;
}

class SolvableHint {
  const SolvableHint({
    required this.level,
    required this.title,
    required this.body,
    this.miniQuestion = '',
    this.acceptedAnswers = const [],
    this.choices = const [],
    this.groupKey,
    this.groupLabel,
    this.rendererFrames = const [],
    this.successMessage = '좋아요. 다음 단계로 가 볼게요.',
  });

  final int level;
  final String title;
  final String body;
  final String miniQuestion;
  final List<String> acceptedAnswers;
  final List<HintChoice> choices;
  final String? groupKey;
  final String? groupLabel;
  final List<Map<String, dynamic>> rendererFrames;
  final String successMessage;

  int get maxLevel => level;
}

List<SolvableHint> _withHintGroup(
  List<SolvableHint> hints, {
  String? groupKey,
  String? groupLabel,
}) {
  if (groupKey == null) {
    return hints;
  }
  return hints
      .map(
        (hint) => SolvableHint(
          level: hint.level,
          title: hint.title,
          body: hint.body,
          miniQuestion: hint.miniQuestion,
          acceptedAnswers: hint.acceptedAnswers,
          choices: hint.choices,
          groupKey: hint.groupKey ?? groupKey,
          groupLabel: hint.groupLabel ?? groupLabel,
          successMessage: hint.successMessage,
        ),
      )
      .toList();
}

class SolvableHintService {
  const SolvableHintService();

  List<SolvableHint> buildHints(
    ProblemContent content, {
    String locale = 'ko',
    AppStrings? strings,
  }) {
    final editorHints = _editorHints(content);
    if (editorHints.isNotEmpty) return editorHints;
    final hints = _buildRawHints(content);
    if (locale == 'ko') {
      return hints.map(_localizeSolvableHint).toList();
    }
    return hints
        .map((h) => _translateHintForLocale(h, locale, strings))
        .toList();
  }

  List<SolvableHint> _buildRawHints(ProblemContent content) {
    final multiplicationPlaceValueHints =
        _multiplicationPlaceValueHints(content);
    if (multiplicationPlaceValueHints.isNotEmpty) {
      return multiplicationPlaceValueHints;
    }

    final baseTenModelHints = _baseTenModelHints(content);
    if (baseTenModelHints.isNotEmpty) {
      return baseTenModelHints;
    }

    final expandedAdditionHints = _expandedAdditionHints(content);
    if (expandedAdditionHints.isNotEmpty) {
      return expandedAdditionHints;
    }

    final wordProblemHints = _wordProblemHints(content);
    if (wordProblemHints.isNotEmpty) {
      return wordProblemHints;
    }

    final comparisonHints = _comparisonHints(content);
    if (comparisonHints.isNotEmpty) {
      return comparisonHints;
    }

    final authoredHints = _authoredStudentHints(content);
    if (authoredHints.isNotEmpty) {
      return authoredHints;
    }

    if (!_isWordProblem(content) && !_isComparisonProblem(content)) {
      final columnHints = _columnAdditionHints(content);
      if (columnHints.isNotEmpty) {
        return columnHints;
      }
    }

    final diagnosticHints = _diagnosticQuestionHints(content);
    if (diagnosticHints.isNotEmpty) {
      return diagnosticHints;
    }

    final planHints = _planBasedHints(content);
    if (planHints.isNotEmpty) {
      return planHints;
    }

    if (_isAdditionProblem(content)) {
      return _additionFallbackHints;
    }

    return _generalFallbackHints(content);
  }
}

const List<SolvableHint> _additionFallbackHints = [
  SolvableHint(
    level: 1,
    title: '1단계: 묻는 것 찾기',
    body: '문제에서 무엇을 구해야 하는지 먼저 확인해요.',
    miniQuestion: '무엇을 구하는 문제인가요?',
    choices: [
      HintChoice(label: '전체 수', isCorrect: true),
      HintChoice(label: '처음 수'),
      HintChoice(label: '남은 수'),
    ],
    acceptedAnswers: ['전체 수', '전체'],
    successMessage: '맞아요. 구해야 하는 값을 먼저 확인하면 계산이 쉬워져요.',
  ),
  SolvableHint(
    level: 2,
    title: '2단계: 계산 방법 고르기',
    body: '전체나 합계를 구하는 문제라면 더하기를 쓰는지 확인해요.',
    miniQuestion: '전체를 구할 때 알맞은 계산은 무엇인가요?',
    choices: [
      HintChoice(label: '더하기', isCorrect: true),
      HintChoice(label: '빼기'),
      HintChoice(label: '비교하기'),
    ],
    acceptedAnswers: ['더하기', '+'],
    successMessage: '좋아요. 이제 주어진 값을 차근차근 계산해요.',
  ),
  SolvableHint(
    level: 3,
    title: '3단계: 자리 맞춰 계산',
    body: '오른쪽 자리부터 계산해요. 한 자리씩 보면 실수가 줄어요.',
    miniQuestion: '계산은 어느 자리부터 시작하나요?',
    choices: [
      HintChoice(label: '일의 자리', isCorrect: true),
      HintChoice(label: '십의 자리'),
      HintChoice(label: '백의 자리'),
    ],
    acceptedAnswers: ['일의 자리', '일'],
    successMessage: '맞아요. 일의 자리부터 시작해요.',
  ),
  SolvableHint(
    level: 4,
    title: '4단계: 다시 확인',
    body: '각 자리의 답과 올림한 1을 빠뜨리지 않았는지 확인해요.',
    miniQuestion: '마지막에 꼭 확인할 것은 무엇인가요?',
    choices: [
      HintChoice(label: '올림한 수를 더했는지', isCorrect: true),
      HintChoice(label: '글자가 크게 보이는지'),
      HintChoice(label: '문제를 한 번만 봤는지'),
    ],
    acceptedAnswers: ['올림', '받아올림'],
    successMessage: '좋아요. 올림까지 확인하면 더 정확해져요.',
  ),
];

List<SolvableHint> _generalFallbackHints(ProblemContent content) {
  return const [
    SolvableHint(
      level: 1,
      title: '1단계: 문제 파악하기',
      body: '문제에서 구하고자 하는 것이 무엇인지 꼼꼼히 읽어보세요.',
    ),
    SolvableHint(
      level: 2,
      title: '2단계: 핵심 조건 찾기',
      body: '주어진 그림이나 수식에서 필요한 단서를 찾아보세요.',
    ),
    SolvableHint(
      level: 3,
      title: '3단계: 차근차근 풀이하기',
      body: '단계를 나누어 계산하거나 규칙을 적용해 보세요.',
    ),
    SolvableHint(
      level: 4,
      title: '4단계: 정답 검토하기',
      body: '구한 답이 문제 조건과 맞는지 다시 한 번 확인해 보세요.',
    ),
  ];
}

SolvableHint _translateHintForLocale(
  SolvableHint hint,
  String locale,
  AppStrings? strings,
) {
  final stepStr = switch (locale) {
    'en' => 'Step ${hint.level}',
    'ja' => 'ステップ${hint.level}',
    'zh' => '第${hint.level}步',
    'km' => 'ជំហានទី ${hint.level}',
    'uk' => 'Крок ${hint.level}',
    _ => '${hint.level}단계',
  };

  return SolvableHint(
    level: hint.level,
    title: _translateHintTitle(hint.title, hint.level, locale, stepStr),
    body: _translateHintBody(hint.body, locale),
    miniQuestion: _translateHintQuestion(hint.miniQuestion, locale),
    choices: hint.choices
        .map((c) => HintChoice(
              label: _translateChoiceLabel(c.label, locale),
              isCorrect: c.isCorrect,
            ))
        .toList(),
    acceptedAnswers: hint.acceptedAnswers
        .map((a) => _translateChoiceLabel(a, locale))
        .toList(),
    successMessage: _translateHintSuccessMessage(hint.successMessage, locale),
    groupKey: hint.groupKey,
    groupLabel: hint.groupLabel != null
        ? _translateHintTitle(hint.groupLabel!, hint.level, locale, stepStr)
        : null,
  );
}

String _translateHintTitle(String title, int level, String locale, String stepStr) {
  final clean = title.replaceFirst(RegExp(r'^\s*\d+단계:\s*'), '').trim();

  final translations = <String, Map<String, String>>{
    '색칠된 자리의 실제 값 찾기': {
      'en': 'Find the actual value of the shaded digit',
      'ja': '色の付いた位の実際の値を求める',
      'zh': '找出涂色数位的实际数值',
      'km': 'រកតម្លៃពិតនៃខ្ទង់ដែលបានដាក់ពណ៌',
      'uk': 'Знайдіть фактичне значення виділеної цифри',
    },
    '곱하는 수 확인': {
      'en': 'Identify the multiplier',
      'ja': '掛ける数を確認する',
      'zh': '确认乘数',
      'km': 'ពិនិត្យមើលគុណនីយ',
      'uk': 'Визначте множник',
    },
    '알맞은 곱셈식 완성': {
      'en': 'Complete the multiplication expression',
      'ja': '正しい掛け算の式を完成させる',
      'zh': '完成正确的乘法算式',
      'km': 'បំពេញកន្សោមគុណដែលត្រឹមត្រូវ',
      'uk': 'Складіть правильний вираз множення',
    },
    '오른쪽 일의 자리 더하기': {
      'en': 'Add digits in the ones place',
      'ja': '一の位を足す',
      'zh': '计算个位相加',
      'km': 'បូកខ្ទង់រាយ',
      'uk': 'Додайте одиниці',
    },
    '일의 자리 더하기': {
      'en': 'Add digits in the ones place',
      'ja': '一の位を足す',
      'zh': '计算个位相加',
      'km': 'បូកខ្ទង់រាយ',
      'uk': 'Додайте одиниці',
    },
    '십의 자리 더하기': {
      'en': 'Add digits in the tens place',
      'ja': '十の位を足す',
      'zh': '计算十位相加',
      'km': 'បូកខ្ទង់ដប់',
      'uk': 'Додайте десятки',
    },
    '비교 기호 고르기': {
      'en': 'Choose comparison symbol',
      'ja': '比較記号を選ぶ',
      'zh': '选择比较符号',
      'km': 'ជ្រើសសញ្ញាប្រៀបធៀប',
      'uk': 'Виберіть знак порівняння',
    },
    '두 값 확인': {
      'en': 'Check both values',
      'ja': '2つの値を確認する',
      'zh': '确认两个数值',
      'km': 'ពិនិត្យតម្លៃទាំងពីរ',
      'uk': 'Перевірте обидва значення',
    },
    '수 모형 확인하기': {
      'en': 'Check base-ten model',
      'ja': '数の模型を確認する',
      'zh': '查看数位模型',
      'km': 'ពិនិត្យមើលគំរូចំនួន',
      'uk': 'Перевірте модель блоків',
    },
    '묻는 것 찾기': {
      'en': 'Understand what is asked',
      'ja': '問いを確認する',
      'zh': '找出问题所求',
      'km': 'ស្វែងយល់ពីបញ្ហា',
      'uk': 'Зрозумійте запитання',
    },
    '문제 파악하기': {
      'en': 'Understand the problem',
      'ja': '問題を把握する',
      'zh': '理解题意',
      'km': 'ស្វែងយល់ពីបញ្ហា',
      'uk': 'Зрозумійте задачу',
    },
    '계산 방법 고르기': {
      'en': 'Choose calculation method',
      'ja': '計算方法を選ぶ',
      'zh': '选择计算方法',
      'km': 'ជ្រើសវិធីគណនា',
      'uk': 'Виберіть метод обчислення',
    },
    '자리 맞춰 계산': {
      'en': 'Align and calculate',
      'ja': '位をそろえて計算する',
      'zh': '对齐数位计算',
      'km': 'គណនាតាមខ្ទង់',
      'uk': 'Обчисліть за розрядами',
    },
    '다시 확인': {
      'en': 'Review your answer',
      'ja': '答えを見直す',
      'zh': '核对答案',
      'km': 'ពិនិត្យមើលចម្លើយឡើងវិញ',
      'uk': 'Перевірте відповідь',
    },
    '정답 검토하기': {
      'en': 'Review your answer',
      'ja': '答えを見直す',
      'zh': '核对答案',
      'km': 'ពិនិត្យមើលចម្លើយឡើងវិញ',
      'uk': 'Перевірте відповідь',
    },
    '핵심 조건 찾기': {
      'en': 'Find key conditions',
      'ja': '重要な条件を見つける',
      'zh': '找出关键条件',
      'km': 'រកលក្ខខណ្ឌសំខាន់ៗ',
      'uk': 'Знайдіть ключові умови',
    },
    '차근차근 풀이하기': {
      'en': 'Solve step by step',
      'ja': '順番に解く',
      'zh': '循序渐进解题',
      'km': 'ដោះស្រាយមួយជំហានម្តងៗ',
      'uk': 'Розв’язуйте покроково',
    },
    '개념 확인': {
      'en': 'Concept check',
      'ja': '概念確認',
      'zh': '概念检查',
      'km': 'ពិនិត្យគោលគំនិត',
      'uk': 'Перевірка понять',
    },
    '중심을 지나는 가장 긴 선분 확인': {
      'en': 'Check longest segment through center',
      'ja': '中心を通る最も長い線分の確認',
      'zh': '确认经过中心的最长线段',
      'km': 'ពិនិត្យអង្កត់វែងបំផុតកាត់តាមផ្ចិត',
      'uk': 'Перевірте найдовший відрізок через центр',
    },
    '원의 중심에서 가장 멀리 있는 구멍 확인': {
      'en': 'Check hole furthest from center',
      'ja': '円の中心から最も遠い穴の確認',
      'zh': '确认离圆心最远的孔',
      'km': 'ពិនិត្យរន្ធដែលនៅឆ្ងាយបំផុតពីផ្ចិត',
      'uk': 'Перевірте отвір, найвіддаленіший від центра',
    },
    '컴퍼스를 벌려 원을 그리는 순서 확인': {
      'en': 'Check compass drawing order',
      'ja': 'コンパスを使って円を描く順序の確認',
      'zh': '确认圆规画圆顺序',
      'km': 'ពិនិត្យលំដាប់នៃការប្រើដែកឈានគូសរង្វង់',
      'uk': 'Перевірте порядок малювання кола циркулем',
    },
    '그림이 나타내는 분수 확인': {
      'en': 'Check fraction shown in diagram',
      'ja': '図が表す分数の確認',
      'zh': '确认图形表示的分数',
      'km': 'ពិនិត្យប្រភាគដែលបង្ហាញក្នុងរូបភាព',
      'uk': 'Перевірте дріб, показаний на малюнку',
    },
    '사다리를 따라가며 분수의 종류 판단': {
      'en': 'Follow ladder to classify fraction',
      'ja': 'あみだくじに沿って分数の種類を判定',
      'zh': '顺着梯子判断分数类型',
      'km': 'ដើរតាមជណ្ដើរដើម្បីកំណត់ប្រភេទប្រភាគ',
      'uk': 'Слідуйте за сходинками для класифікації дробу',
    },
    '그릇에 부었을 때 수면의 높이 비교': {
      'en': 'Compare water level when poured',
      'ja': '容器に注いだときの水面の高さを比較',
      'zh': '比较倒入容器后的水面高度',
      'km': 'ប្រៀបធៀបកម្ពស់ទឹកនៅពេលចាក់ចូលកែវ',
      'uk': 'Порівняйте рівень води при переливанні',
    },
    '들이를 직접 비교하는 올바른 방법 확인': {
      'en': 'Check correct way to compare capacity directly',
      'ja': 'かさを直接比べる正しい方法の確認',
      'zh': '确认直接比较容量的正确方法',
      'km': 'ពិនិត្យវិធីត្រឹមត្រូវដើម្បីប្រៀបធៀបចំណុះផ្ទាល់',
      'uk': 'Перевірте правильний спосіб прямого порівняння місткості',
    },
  };

  if (translations.containsKey(clean) && translations[clean]!.containsKey(locale)) {
    return '$stepStr: ${translations[clean]![locale]}';
  }

  final conceptCheckMatch = RegExp(r'^개념 확인\s*(\d+)?$').firstMatch(clean);
  if (conceptCheckMatch != null) {
    final num = conceptCheckMatch.group(1);
    final numSuffix = num != null ? ' $num' : '';
    return switch (locale) {
      'en' => '$stepStr: Concept check$numSuffix',
      'ja' => '$stepStr: 概念確認$numSuffix',
      'zh' => '$stepStr: 概念检查$numSuffix',
      'km' => '$stepStr: ពិនិត្យគោលគំនិត$numSuffix',
      'uk' => '$stepStr: Перевірка понять$numSuffix',
      _ => '$stepStr: $clean',
    };
  }

  final solutionGuideMatch = RegExp(r'^풀이 안내\s*(\d+)?$').firstMatch(clean);
  if (solutionGuideMatch != null) {
    final num = solutionGuideMatch.group(1);
    final numSuffix = num != null ? ' $num' : '';
    return switch (locale) {
      'en' => '$stepStr: Solution guide$numSuffix',
      'ja' => '$stepStr: 解法案内$numSuffix',
      'zh' => '$stepStr: 解题指引$numSuffix',
      'km' => '$stepStr: ការណែនាំដំណោះស្រាយ$numSuffix',
      'uk' => '$stepStr: Посібник із розв\'язання$numSuffix',
      _ => '$stepStr: $clean',
    };
  }

  final generalCalcMatch = RegExp(r'^(.+)\s*계산하기$').firstMatch(clean);
  if (generalCalcMatch != null) {
    final target = generalCalcMatch.group(1)!.trim();
    return switch (locale) {
      'en' => '$stepStr: Calculate $target',
      'ja' => '$stepStr: $targetを計算する',
      'zh' => '$stepStr: 计算 $target',
      'km' => '$stepStr: គណនា $target',
      'uk' => '$stepStr: Обчисліть $target',
      _ => '$stepStr: $clean',
    };
  }

  final calcMatch = RegExp(r'^식 계산하기\s*\((.+)\)$').firstMatch(clean);
  if (calcMatch != null) {
    final expr = calcMatch.group(1)!;
    return switch (locale) {
      'en' => '$stepStr: Calculate expression ($expr)',
      'ja' => '$stepStr: 式を計算する ($expr)',
      'zh' => '$stepStr: 计算算式 ($expr)',
      'km' => '$stepStr: គណនាកន្សោម ($expr)',
      'uk' => '$stepStr: Обчисліть вираз ($expr)',
      _ => '$stepStr: $clean',
    };
  }

  final ineqMatch = RegExp(r'^알맞은 부등호 기호 선택\s*\((.+)\)$').firstMatch(clean);
  if (ineqMatch != null) {
    final expr = ineqMatch.group(1)!;
    return switch (locale) {
      'en' => '$stepStr: Select inequality symbol ($expr)',
      'ja' => '$stepStr: 不等号を選ぶ ($expr)',
      'zh' => '$stepStr: 选择不等号 ($expr)',
      'km' => '$stepStr: ជ្រើសសញ្ញាវិសមភាព ($expr)',
      'uk' => '$stepStr: Виберіть знак нерівності ($expr)',
      _ => '$stepStr: $clean',
    };
  }

  return '$stepStr: $clean';
}

String _translateHintBody(String body, String locale) {
  final clean = body.trim();
  if (clean.isEmpty) return clean;

  final exactBodyTranslations = <String, Map<String, String>>{
    '69를 3으로 나눈 몫을 구한다.': {
      'en': 'Find the quotient of 69 divided by 3.',
      'ja': '69を3で割った商を求めます。',
      'zh': '求69除以3的商。',
      'km': 'ស្វែងរកផលចែកនៃ 69 ចែកនឹង 3។',
      'uk': 'Знайдіть частку від ділення 69 на 3.',
    },
    '보기 중 계산 결과와 같은 수를 찾는다.': {
      'en': 'Find the number matching the calculation result from options.',
      'ja': '選択肢から計算結果と同じ数を見つけます。',
      'zh': '在选项中找出与计算结果相同的数。',
      'km': 'ស្វែងរកចំនួនដែលត្រូវនឹងលទ្ធផលគណនាពីជម្រើស។',
      'uk': 'Знайдіть число, що відповідає результату обчислення, серед варіантів.',
    },
    '원 안의 네 선분을 비교한다.': {
      'en': 'Compare the four line segments in the circle.',
      'ja': '円の中の4つの線分を比較します。',
      'zh': '比较圆内的四条线段。',
      'km': 'ប្រៀបធៀបអង្កត់ទាំងបួននៅក្នុងរង្វង់។',
      'uk': 'Порівняйте чотири відрізки в колі.',
    },
    '중심을 지나는 선분을 찾는다.': {
      'en': 'Find the line segment passing through the center.',
      'ja': '中心を通る線分を見つけます。',
      'zh': '找出穿过圆心的线段。',
      'km': 'ស្វែងរកអង្កត់ដែលកាត់តាមផ្ចិត។',
      'uk': 'Знайдіть відрізок, що проходить через центр.',
    },
    '보기에서 그 선분에 해당하는 번호를 고른다.': {
      'en': 'Choose the number corresponding to that line segment from the options.',
      'ja': '選択肢からその線分に対応する番号を選びます。',
      'zh': '在选项中选择对应那条线段的编号。',
      'km': 'ជ្រើសរើសលេខដែលត្រូវនឹងអង្កត់នោះពីជម្រើស។',
      'uk': 'Виберіть номер, що відповідає цьому відрізку, із запропонованих варіантів.',
    },
    '구멍들의 위치를 비교한다.': {
      'en': 'Compare the positions of the holes.',
      'ja': '穴の位置を比較します。',
      'zh': '比较各个孔的位置。',
      'km': 'ប្រៀបធៀបទីតាំងនៃរន្ធនានា។',
      'uk': 'Порівняйте положення отворів.',
    },
    '누름 못과 연필심 사이가 가장 멀어지는 구멍을 찾는다.': {
      'en': 'Find the hole furthest between push pin and pencil lead.',
      'ja': '押しピンと鉛筆の芯の間が最も遠くなる穴を見つけます。',
      'zh': '找出图钉和铅笔芯距离最远的孔。',
      'km': 'ស្វែងរករន្ធដែលនៅឆ្ងាយបំផុតរវាងម្ជុលខ្ទាស់និងចុងខ្មៅដៃ។',
      'uk': 'Знайдіть отвір, найбільш віддалений між кнопкою та грифелем олівця.',
    },
    '그 구멍에 대응하는 기호를 답으로 둔다.': {
      'en': 'Use the letter corresponding to that hole as the answer.',
      'ja': 'その穴に対応する記号を答えとします。',
      'zh': '将对应那个孔的符号作为答案。',
      'km': 'កំណត់និមិត្តសញ្ញាដែលត្រូវនឹងរន្ធនោះជាចម្លើយ។',
      'uk': 'Запишіть букву, що відповідає цьому отвору, як відповідь.',
    },
    '해설의 순서를 따라 올바른 단계 배열을 확인한다.': {
      'en': 'Follow the explanation to check the correct order of steps.',
      'ja': '解説の手順に沿って、正しいステップの順序を確認します。',
      'zh': '根据解析顺序确认正确的步骤排列。',
      'km': 'ធ្វើតាមការពន្យល់ដើម្បីពិនិត្យលំដាប់លំដោយត្រឹមត្រូវនៃជំហាន។',
      'uk': 'Дотримуйтесь пояснення, щоб перевірити правильний порядок дій.',
    },
    '해당 순서와 같은 선택지를 찾는다.': {
      'en': 'Find the option that matches that order.',
      'ja': 'その順序と一致する選択肢を見つけます。',
      'zh': '找出与该顺序相同的选项。',
      'km': 'ស្វែងរកជម្រើសដែលត្រូវគ្នានឹងលំដាប់នោះ។',
      'uk': 'Знайдіть варіант, що відповідає цьому порядку.',
    },
    '그림의 색칠한 부분과 색칠하지 않은 부분을 분수 설명과 비교한다.': {
      'en': 'Compare the shaded and unshaded parts with the fraction explanation.',
      'ja': '図の色の付いた部分と付いていない部分を分数の説明と比較します。',
      'zh': '将图中涂色部分和未涂色部分与分数说明进行比较。',
      'km': 'ប្រៀបធៀបផ្នែកដាក់ពណ៌និងផ្នែកមិនដាក់ពណ៌ក្នុងរូបភាពជាមួយការពន្យល់ប្រភាគ។',
      'uk': 'Порівняйте зафарбовану та незафарбовану частини на малюнку з поясненням дробу.',
    },
    '말풍선의 설명이 그림과 맞는 사람을 찾는다.': {
      'en': 'Find the person whose speech bubble matches the diagram.',
      'ja': '吹き出しの説明が図と合っている人を見つけます。',
      'zh': '找出对话框说明与图形相符的人。',
      'km': 'ស្វែងរកបុគ្គលដែលការពន្យល់ក្នុងពពុះពាក្យត្រូវនឹងរូបភាព។',
      'uk': 'Знайдіть людину, чиє пояснення у виносці відповідає малюнку.',
    },
  };

  if (exactBodyTranslations.containsKey(clean) &&
      exactBodyTranslations[clean]!.containsKey(locale)) {
    return exactBodyTranslations[clean]![locale]!;
  }

  final shadedMatch = RegExp(
    r'^(?:(\d+)에서\s*)?색칠된 자리의 숫자 (\d+)은 실제 얼마를 나타내는지 확인해요\.?$',
  ).firstMatch(clean);
  if (shadedMatch != null) {
    final num = shadedMatch.group(1);
    final digit = shadedMatch.group(2)!;
    final prefix = num != null ? 'In $num, ' : '';
    final jaPrefix = num != null ? '$numで' : '';
    final zhPrefix = num != null ? '在$num中，' : '';
    final kmPrefix = num != null ? 'នៅក្នុង $num ' : '';
    final ukPrefix = num != null ? 'У $num ' : '';
    return switch (locale) {
      'en' => '${prefix}let\'s find the actual value represented by the shaded digit $digit.',
      'ja' => '$jaPrefix色の付いた位の数字$digitが実際に表す値を確認しましょう。',
      'zh' => '$zhPrefix确认涂色数位的数字$digit实际表示的数值。',
      'km' => '$kmPrefixសូមពិនិត្យមើលថាតើតួលេខ $digit ក្នុងខ្ទង់ដាក់ពណ៌ពិតជាតំណាងឱ្យប៉ុន្មាន។',
      'uk' => '$ukPrefixперевіримо, яке значення насправді представляє виділена цифра $digit.',
      _ => clean,
    };
  }

  if (clean.contains('색칠된 부분에 곱해지는 한 자리 수를 확인해요')) {
    return switch (locale) {
      'en' => 'Identify the single-digit multiplier for the shaded part.',
      'ja' => '色の付いた部分に掛けられている1桁の数を確認しましょう。',
      'zh' => '确认与涂色部分相乘的一位数。',
      'km' => 'ពិនិត្យមើលលេខមួយខ្ទង់ដែលគុណនឹងផ្នែកដាក់ពណ៌។',
      'uk' => 'Визначте одноцифровий множник для виділеної частини.',
      _ => clean,
    };
  }

  final prodMatch = RegExp(
    r'^색칠된 부분\((.+?)\)은 (.+?)과 (.+?)의 곱이에요\.?$',
  ).firstMatch(clean);
  if (prodMatch != null) {
    final prod = prodMatch.group(1)!;
    final a = prodMatch.group(2)!;
    final b = prodMatch.group(3)!;
    return switch (locale) {
      'en' => 'The shaded part ($prod) is the product of $a and $b.',
      'ja' => '色の付いた部分($prod)は、$aと$bの積です。',
      'zh' => '涂色部分（$prod）是$a与$b的乘积。',
      'km' => 'ផ្នែកដាក់ពណ៌ ($prod) គឺជាផលគុណនៃ $a និង $b។',
      'uk' => 'Зафарбована частина ($prod) є добутком $a та $b.',
      _ => clean,
    };
  }

  if (clean.contains('구한 답이 문제 조건과 맞는지')) {
    return switch (locale) {
      'en' => 'Check again if your answer matches the problem conditions.',
      'ja' => '求めた答えが問題の条件に合っているかもう一度確認してみましょう。',
      'zh' => '再次检查算出的答案是否符合题意。',
      'km' => 'សូមពិនិត្យមើលឡើងវិញថាតើចម្លើយដែលរកឃើញត្រូវនឹងលក្ខខណ្ឌបញ្ហាឬទេ។',
      'uk' => 'Перевірте ще раз, чи відповідає знайдена відповідь умовам задачі.',
      _ => clean,
    };
  }

  if (clean.contains('조건과 묻는 내용을 차례대로 정리')) {
    return switch (locale) {
      'en' => 'Organize the given conditions and what is being asked.',
      'ja' => '問題の条件と問われている内容を順に整理してみましょう。',
      'zh' => '把题目给出的条件和所求问题依次整理清楚。',
      'km' => 'រៀបចំលក្ខខណ្ឌដែលបានផ្ដល់ និងអ្វីដែលសួរតាមលំដាប់។',
      'uk' => 'Упорядкуйте дані умови та запитання задачі.',
      _ => clean,
    };
  }

  if (clean.contains('핵심 힌트나 식을 찾아보세요')) {
    return switch (locale) {
      'en' => 'Find the key hint or expression to solve the problem.',
      'ja' => '問題を解くための重要なヒントや式を見つけましょう。',
      'zh' => '找出解题的关键提示或算式。',
      'km' => 'ស្វែងរកជំនួយសំខាន់ ឬកន្សោមដើម្បីដោះស្រាយបញ្ហា។',
      'uk' => 'Знайдіть ключову підказку або вираз для розв’язання задачі.',
      _ => clean,
    };
  }

  if (clean.contains('계산 과정을 확인하며 단계별로')) {
    return switch (locale) {
      'en' => 'Follow the calculation step by step.',
      'ja' => '計算手順を確認しながら、順番に解いてみましょう。',
      'zh' => '跟着计算过程一步步进行求解。',
      'km' => 'ពិនិត្យដំណើរការគណនា ហើយដោះស្រាយមួយជំហានម្តងៗ។',
      'uk' => 'Виконуйте обчислення крок за кроком.',
      _ => clean,
    };
  }

  if (clean.contains('보이는 정답 표기를 그대로 기록')) {
    return switch (locale) {
      'en' => 'Record the displayed answer directly.',
      'ja' => '表示された答えをそのまま記録します。',
      'zh' => '直接记录显示的答案。',
      'km' => 'កត់ត្រាចម្លើយដែលបានបង្ហាញ។',
      'uk' => 'Запишіть відображену відповідь.',
      _ => clean,
    };
  }

  if (clean.contains('도착 라벨과 화면에 제시된 분류')) {
    return switch (locale) {
      'en' => 'Match each fraction\'s label with the classification on screen.',
      'ja' => '各分数の終点ラベルと画面に表示された分類を対応させます。',
      'zh' => '将每个分数的到达标签与屏幕上的分类相对应。',
      'km' => 'ផ្គូផ្គងស្លាកនៃប្រភាគនីមួយៗជាមួយចំណាត់ថ្នាក់នៅលើអេក្រង់។',
      'uk' => 'Зіставте мітку кожного дробу з класифікацією на екрані.',
      _ => clean,
    };
  }

  if (clean.contains('같은 모양과 크기의 그릇에 옮겨 담은 물의 높이')) {
    return switch (locale) {
      'en' => 'Compare the water level transferred into containers of the same shape and size.',
      'ja' => '同じ形と大きさの容器に移し替えた水の高さを比べます。',
      'zh' => '比较倒入同样形状和大小的容器中水的高度。',
      'km' => 'ប្រៀបធៀបកម្ពស់ទឹកដែលបានផ្ទេរទៅក្នុងធុងដែលមានរាង និងទំហំដូចគ្នា។',
      'uk' => 'Порівняйте рівень води, перелитої в посудини однакової форми та розміру.',
      _ => clean,
    };
  }

  if (clean.contains('물의 높이가 더 높은 쪽의 들이가 더 많다고')) {
    return switch (locale) {
      'en' => 'Determine that the higher water level indicates greater capacity.',
      'ja' => '水位が高い方の容器のかさがより多いと判断します。',
      'zh' => '判断水面较高的一侧容量更大。',
      'km' => 'កំណត់ថាកម្រិតទឹកកាន់តែខ្ពស់បង្ហាញពីចំណុះកាន់តែច្រើន។',
      'uk' => 'Визначте, що вищий рівень води вказує на більшу місткість.',
      _ => clean,
    };
  }

  if (clean.contains('제시된 설명이 높이 비교 방법인지')) {
    return switch (locale) {
      'en' => 'Check if the given explanation is a height comparison method.',
      'ja' => '提示された説明が高さの比較方法であるか確認します。',
      'zh' => '确认给出的说明是否为比较高度的方法。',
      'km' => 'ពិនិត្យមើលថាតើការពន្យល់ដែលបានផ្ដល់គឺជាវិធីប្រៀបធៀបកម្ពស់ឬទេ។',
      'uk' => 'Перевірте, чи є наведене пояснення методом порівняння висоти.',
      _ => clean,
    };
  }

  if (clean.contains('문장이 비교의 목적에 맞는지')) {
    return switch (locale) {
      'en' => 'Determine whether the statement matches the purpose of the comparison.',
      'ja' => '文が比較の目的に合っているかを判断します。',
      'zh' => '判断句子是否符合比较的目的。',
      'km' => 'កំណត់ថាតើប្រយោគនេះត្រូវនឹងគោលបំណងនៃការប្រៀបធៀបឬទេ។',
      'uk' => 'Визначте, чи відповідає твердження меті порівняння.',
      _ => clean,
    };
  }

  if (clean.contains('알맞은 순서나 식을 골라보세요')) {
    return switch (locale) {
      'en' => 'Select the correct order or expression.',
      'ja' => '正しい順序や式を選んでみましょう。',
      'zh' => '请选择正确的顺序或算式。',
      'km' => 'សូមជ្រើសរើសលំដាប់ ឬកន្សោមដែលត្រឹមត្រូវ។',
      'uk' => 'Виберіть правильний порядок або вираз.',
      _ => clean,
    };
  }

  if (clean.contains('계산 결과가 큰 것부터 차례대로 나열한 것은 무엇일까요')) {
    return switch (locale) {
      'en' => 'Which option lists the results from greatest to least?',
      'ja' => '計算結果が大きい順に並んでいるものはどれですか？',
      'zh' => '哪个选项是按计算结果从大到小排列的？',
      'km' => 'តើជម្រើសណារៀបចំលទ្ធផលពីធំទៅតូច?',
      'uk' => 'Який варіант розташовує результати від найбільшого до найменшого?',
      _ => clean,
    };
  }

  final calcStepMatch = RegExp(r'^(.+?)(?:을|를)\s*계산해요\.?$').firstMatch(clean);
  if (calcStepMatch != null) {
    final target = calcStepMatch.group(1)!.trim();
    return switch (locale) {
      'en' => 'Calculate $target.',
      'ja' => '$targetを計算しましょう。',
      'zh' => '计算 $target。',
      'km' => 'គណនា $target។',
      'uk' => 'Обчисліть $target.',
      _ => clean,
    };
  }

  final valBodyMatch = RegExp(r'^(.+?)(?:의 값은 얼마인가요|의 값은 얼마일까요|은 얼마인가요)\??$').firstMatch(clean);
  if (valBodyMatch != null) {
    final expr = valBodyMatch.group(1)!.trim();
    return switch (locale) {
      'en' => 'What is the value of $expr?',
      'ja' => '$exprの値はいくつですか？',
      'zh' => '$expr的值是多少？',
      'km' => 'តើតម្លៃនៃ $expr ស្មើនឹងប៉ុន្មាន?',
      'uk' => 'Яке значення виразу $expr?',
      _ => clean,
    };
  }

  return clean;
}

String _translateHintQuestion(String question, String locale) {
  final clean = question.trim();
  if (clean.isEmpty) return clean;

  if (clean.contains('순서대로 확인해 보세요')) {
    final base = clean
        .replaceFirst('순서대로 확인해 보세요.', '')
        .replaceFirst('순서대로 확인해 보세요', '')
        .trim();
    final translatedBase = _translateHintBody(base, locale);
    return switch (locale) {
      'en' => '$translatedBase Check in order.',
      'ja' => '$translatedBase 順番に確認してみましょう。',
      'zh' => '$translatedBase 请按顺序进行确认。',
      'km' => '$translatedBase សូមពិនិត្យមើលតាមលំដាប់។',
      'uk' => '$translatedBase Перевірте по черзі.',
      _ => clean,
    };
  }

  if (clean.contains('계산 결과가 큰 것부터 차례대로 나열한 것은 무엇일까요')) {
    return switch (locale) {
      'en' => 'Which option lists the results from greatest to least?',
      'ja' => '計算結果が大きい順に並んでいるものはどれですか？',
      'zh' => '哪个选项是按计算结果从大到小排列的？',
      'km' => 'តើជម្រើសណារៀបចំលទ្ធផលពីធំទៅតូច?',
      'uk' => 'Який варіант розташовує результати від найбільшого до найменшого?',
      _ => clean,
    };
  }

  if (clean.contains('알맞은 순서나 식을 골라보세요')) {
    return switch (locale) {
      'en' => 'Select the correct order or expression.',
      'ja' => '正しい順序や式を選んでみましょう。',
      'zh' => '请选择正确的顺序或算式。',
      'km' => 'សូមជ្រើសរើសលំដាប់ ឬកន្សោមដែលត្រឹមត្រូវ។',
      'uk' => 'Виберіть правильний порядок або вираз.',
      _ => clean,
    };
  }

  final digitMatch = RegExp(
    r'^(?:(\d+)에서\s*)?숫자 (\d+)은 실제 얼마를 나타내나요\??$',
  ).firstMatch(clean);
  if (digitMatch != null) {
    final num = digitMatch.group(1);
    final digit = digitMatch.group(2)!;
    final prefix = num != null ? 'In $num, ' : '';
    final jaPrefix = num != null ? '$numで' : '';
    final zhPrefix = num != null ? '在$num中，' : '';
    final kmPrefix = num != null ? 'នៅក្នុង $num ' : '';
    final ukPrefix = num != null ? 'У $num ' : '';
    return switch (locale) {
      'en' => '${prefix}what value does the digit $digit actually represent?',
      'ja' => '$jaPrefix数字$digitは実際にいくつを表していますか？',
      'zh' => '$zhPrefix数字$digit实际表示多少？',
      'km' => '$kmPrefixតើតួលេខ $digit ពិតជាតំណាងឱ្យប៉ុន្មាន?',
      'uk' => '$ukPrefixяке значення насправді представляє цифра $digit?',
      _ => clean,
    };
  }

  if (clean.contains('곱하는 수는 얼마인가요')) {
    return switch (locale) {
      'en' => 'What is the multiplier?',
      'ja' => '掛ける数はいくつですか？',
      'zh' => '乘数是多少？',
      'km' => 'តើគុណនីយជាអ្វី?',
      'uk' => 'Який множник?',
      _ => clean,
    };
  }

  if (clean.contains('색칠된 부분을 나타내는 알맞은 곱셈식은')) {
    return switch (locale) {
      'en' => 'Which multiplication expression represents the shaded part?',
      'ja' => '色の付いた部分を表す正しい掛け算の式はどれですか？',
      'zh' => '表示涂色部分的正确乘法算式是什么？',
      'km' => 'តើកន្សោមគុណណាដែលតំណាងឱ្យផ្នែកដាក់ពណ៌?',
      'uk' => 'Який вираз множення представляє зафарбовану частину?',
      _ => clean,
    };
  }

  if (clean.contains('빈칸에 들어갈 기호는')) {
    return switch (locale) {
      'en' => 'Which symbol goes in the blank?',
      'ja' => '空欄に入る記号は何ですか？',
      'zh' => '空格中应该填入什么符号？',
      'km' => 'តើសញ្ញាណាត្រូវដាក់ក្នុងចន្លោះទទេ?',
      'uk' => 'Який знак має бути у пропуску?',
      _ => clean,
    };
  }

  final valMatch = RegExp(r'^(.+?)(?:의 값은 얼마인가요|의 값은 얼마일까요|은 얼마인가요)\??$').firstMatch(clean);
  if (valMatch != null) {
    final expr = valMatch.group(1)!.trim();
    return switch (locale) {
      'en' => 'What is the value of $expr?',
      'ja' => '$exprの値はいくつですか？',
      'zh' => '$expr的值是多少？',
      'km' => 'តើតម្លៃនៃ $expr ស្មើនឹងប៉ុន្មាន?',
      'uk' => 'Яке значення виразу $expr?',
      _ => clean,
    };
  }

  if (clean.contains('이 문제에서 구해야 하는 것')) {
    return switch (locale) {
      'en' => 'What are we looking for in this problem?',
      'ja' => 'この問題で求めるものは何ですか？',
      'zh' => '这道题要求的是什么？',
      'km' => 'តើបញ្ហានេះសួររកអ្វី?',
      'uk' => 'Що потрібно знайти в цій задачі?',
      _ => clean,
    };
  }

  if (clean.contains('어떻게 계산해야 할까요')) {
    return switch (locale) {
      'en' => 'How should we calculate?',
      'ja' => 'どのように計算すればよいでしょうか？',
      'zh' => '应该如何计算？',
      'km' => 'តើយើងគួរគណនាយ៉ាងដូចម្តេច?',
      'uk' => 'Як нам слід обчислити?',
      _ => clean,
    };
  }

  if (clean.contains('먼저 해야 할 일')) {
    return switch (locale) {
      'en' => 'What should we do first?',
      'ja' => '最初に何をすべきでしょうか？',
      'zh' => '首先应该做什么？',
      'km' => 'តើយើងគួរធ្វើអ្វីមុនគេ?',
      'uk' => 'Що нам слід зробити спочатку?',
      _ => clean,
    };
  }

  return clean;
}

String _translateHintSuccessMessage(String msg, String locale) {
  final clean = msg.trim();
  if (clean.isEmpty) return clean;

  final shadedSuccess = RegExp(
    r'^맞아요\.\s*(\d+)은\s*.*?\s*숫자이므로 실제로는\s*(\d+)입니다\.?$',
  ).firstMatch(clean);
  if (shadedSuccess != null) {
    final digit = shadedSuccess.group(1)!;
    final val = shadedSuccess.group(2)!;
    return switch (locale) {
      'en' => 'Correct! The digit $digit represents $val.',
      'ja' => '正解です！数字$digitは実際には$valを表します。',
      'zh' => '正确！数字$digit实际表示$val。',
      'km' => 'ត្រឹមត្រូវ! តួលេខ $digit តំណាងឱ្យ $val។',
      'uk' => 'Правильно! Цифра $digit представляє $val.',
      _ => clean,
    };
  }

  final multSuccess = RegExp(
    r'^좋아요\.\s*곱하는 수는\s*(\d+)입니다\.?$',
  ).firstMatch(clean);
  if (multSuccess != null) {
    final val = multSuccess.group(1)!;
    return switch (locale) {
      'en' => 'Great! The multiplier is $val.',
      'ja' => 'よくできました！掛ける数は$valです。',
      'zh' => '很好！乘数是$val。',
      'km' => 'ល្អណាស់! គុណនីយគឺ $val។',
      'uk' => 'Чудово! Множник дорівнює $val.',
      _ => clean,
    };
  }

  final exprSuccess = RegExp(
    r'^정답이에요!\s*색칠된 부분은\s*(.+?)(?:를|을) 나타냅니다\.?$',
  ).firstMatch(clean);
  if (exprSuccess != null) {
    final expr = exprSuccess.group(1)!;
    return switch (locale) {
      'en' => 'Correct! The shaded part represents $expr.',
      'ja' => '正解です！色の付いた部分は$exprを表します。',
      'zh' => '回答正确！涂色部分表示$expr。',
      'km' => 'ត្រឹមត្រូវហើយ! ផ្នែកដាក់ពណ៌តំណាងឱ្យ $expr។',
      'uk' => 'Правильно! Зафарбована частина представляє $expr.',
      _ => clean,
    };
  }

  if (clean.contains('좋아요. 다음 단계로 가 볼게요')) {
    return switch (locale) {
      'en' => 'Great job! Let\'s move to the next step.',
      'ja' => 'よくできました！次のステップへ進みましょう。',
      'zh' => '很好！进入下一步。',
      'km' => 'ល្អណាស់! តោះទៅជំហានបន្ទាប់។',
      'uk' => 'Чудово! Перейдемо до наступного кроку.',
      _ => clean,
    };
  }

  final jsonChoiceSuccess = RegExp(
    r"^(?:맞아요|정답이에요|좋아요)[!.]?\s*\{.*?['\x22](?:label|text)['\x22]:\s*['\x22](.*?)['\x22].*?\}\s*(?:입니다|예요|이에요)\.?$",
  ).firstMatch(clean);
  if (jsonChoiceSuccess != null) {
    final val = jsonChoiceSuccess.group(1)!.trim();
    return switch (locale) {
      'en' => 'Correct! It is $val.',
      'ja' => '正解です！$valです。',
      'zh' => '正确！是$val。',
      'km' => 'ត្រឹមត្រូវ! គឺ $val។',
      'uk' => 'Правильно! Це $val.',
      _ => clean,
    };
  }

  final generalSuccessMatch = RegExp(
    r'^(?:맞아요|정답이에요|좋아요)[!.]?\s*(.+?)\s*(?:입니다|예요|이에요)\.?$',
  ).firstMatch(clean);
  if (generalSuccessMatch != null) {
    final val = generalSuccessMatch.group(1)!.trim();
    return switch (locale) {
      'en' => 'Correct! It is $val.',
      'ja' => '正解です！$valです。',
      'zh' => '正确！是$val。',
      'km' => 'ត្រឹមត្រូវ! គឺ $val។',
      'uk' => 'Правильно! Це $val.',
      _ => clean,
    };
  }

  return clean;
}

String _translateChoiceLabel(String label, String locale) {
  final clean = label.trim();
  final choiceTranslations = <String, Map<String, String>>{
    '가분수': {
      'en': 'Improper fraction',
      'ja': '仮分数',
      'zh': '假分数',
      'km': 'ប្រភាគមិនសុទ្ធ',
      'uk': 'Неправильний дріб',
    },
    '진분수': {
      'en': 'Proper fraction',
      'ja': '真分数',
      'zh': '真分数',
      'km': 'ប្រភាគសុទ្ធ',
      'uk': 'Правильний дріб',
    },
    '대분수': {
      'en': 'Mixed number',
      'ja': '帯分数',
      'zh': '带分数',
      'km': 'ចំនួនចម្រុះ',
      'uk': 'Мішане число',
    },
    '참': {
      'en': 'True',
      'ja': '正',
      'zh': '正确',
      'km': 'ពិត',
      'uk': 'Правда',
    },
    '거짓': {
      'en': 'False',
      'ja': '誤',
      'zh': '错误',
      'km': 'មិនពិត',
      'uk': 'Хибність',
    },
  };

  if (choiceTranslations.containsKey(clean) &&
      choiceTranslations[clean]!.containsKey(locale)) {
    return choiceTranslations[clean]![locale]!;
  }
  return clean;
}

SolvableHint _localizeSolvableHint(SolvableHint hint) {
  return SolvableHint(
    level: hint.level,
    title: _localizeText(hint.title),
    body: _localizeText(hint.body),
    miniQuestion: _localizeText(hint.miniQuestion),
    choices: hint.choices
        .map((c) => HintChoice(
              label: _localizeChoice(c.label),
              isCorrect: c.isCorrect,
            ))
        .toList(),
    acceptedAnswers: hint.acceptedAnswers.map(_localizeChoice).toList(),
    successMessage: _localizeText(hint.successMessage),
    groupKey: hint.groupKey,
    groupLabel: hint.groupLabel != null ? _localizeText(hint.groupLabel!) : null,
  );
}

String _localizeText(String input) {
  final text = input.trim();
  if (text.isEmpty) return text;
  final lower = text.toLowerCase();

  final findMatch = RegExp(
    r'^find\s+(.+?)\s+using the given information\.?$',
    caseSensitive: false,
  ).firstMatch(text);
  if (findMatch != null) {
    final target = findMatch.group(1)!.trim();
    return '$target을(를) 구해요.';
  }

  if (lower == 'what should we find?' ||
      lower == 'what does the problem ask for?' ||
      lower == 'what are we looking for?') {
    return '이 문제에서 구해야 하는 것은 무엇인가요?';
  }
  if (lower == 'how should we calculate?' ||
      lower == 'how do we solve this?' ||
      lower == 'what operation should we use?') {
    return '어떻게 계산해야 할까요?';
  }
  if (lower == 'what is the first step?' ||
      lower == 'what should we do first?') {
    return '먼저 해야 할 일은 무엇인가요?';
  }

  final isGreaterMatch = RegExp(
    r'^is\s+(.+?)\s+greater than\s+(.+?)\??$',
    caseSensitive: false,
  ).firstMatch(text);
  if (isGreaterMatch != null) {
    final expr = isGreaterMatch
        .group(1)!
        .trim()
        .replaceAll('x', '×')
        .replaceAll('*', '×');
    final threshold = isGreaterMatch.group(2)!.trim();
    return '$expr의 계산 결과는 $threshold보다 큰가요?';
  }

  final isLessMatch = RegExp(
    r'^is\s+(.+?)\s+less than\s+(.+?)\??$',
    caseSensitive: false,
  ).firstMatch(text);
  if (isLessMatch != null) {
    final expr = isLessMatch
        .group(1)!
        .trim()
        .replaceAll('x', '×')
        .replaceAll('*', '×');
    final threshold = isLessMatch.group(2)!.trim();
    return '$expr의 계산 결과는 $threshold보다 작은가요?';
  }

  final whichGreaterMatch = RegExp(
    r'^which\s+(?:products|expressions|values)\s+are\s+greater than\s+(.+?)\??$',
    caseSensitive: false,
  ).firstMatch(text);
  if (whichGreaterMatch != null) {
    final threshold = whichGreaterMatch.group(1)!.trim();
    return '계산 결과가 $threshold보다 큰 것은 무엇인가요?';
  }

  final whichLessMatch = RegExp(
    r'^which\s+(?:products|expressions|values)\s+are\s+less than\s+(.+?)\??$',
    caseSensitive: false,
  ).firstMatch(text);
  if (whichLessMatch != null) {
    final threshold = whichLessMatch.group(1)!.trim();
    return '계산 결과가 $threshold보다 작은 것은 무엇인가요?';
  }

  final mathMatch =
      RegExp(r'^what is\s*(.+)\?$', caseSensitive: false).firstMatch(text);
  if (mathMatch != null) {
    final expr = mathMatch
        .group(1)!
        .trim()
        .replaceAll('x', '×')
        .replaceAll('*', '×');
    return '$expr의 값은 얼마일까요?';
  }
  if (lower.contains('greatest to least')) {
    return '계산 결과가 큰 것부터 차례대로 나열한 것은 무엇일까요?';
  }
  if (lower.contains('least to greatest')) {
    return '계산 결과가 작은 것부터 차례대로 나열한 것은 무엇일까요?';
  }
  if (lower.contains('which order') || lower.contains('which expression')) {
    return '알맞은 순서나 식을 골라보세요.';
  }

  if (lower.contains('compute each') || lower.contains('calculate each')) {
    return '각 식을 차례대로 계산해요.';
  }
  if (lower.contains('compare each result') ||
      lower.contains('compare the results')) {
    return '계산 결과를 서로 비교해요.';
  }
  if (lower.contains('select the') || lower.contains('choose the')) {
    return '알맞은 식이나 보기를 골라요.';
  }
  if (lower.contains('find the total') ||
      lower.contains('calculate the total')) {
    return '전체 수를 계산해요.';
  }
  if (lower.contains('find the remaining') ||
      lower.contains('calculate the remaining')) {
    return '남은 수를 계산해요.';
  }

  return text;
}

String _localizeChoice(String choice) {
  final text = choice.trim();
  final lower = text.toLowerCase();

  final yesBecauseMatch = RegExp(
    r'^yes,?\s*because\s*(?:it\s+is\s*)?(.+)$',
    caseSensitive: false,
  ).firstMatch(text);
  if (yesBecauseMatch != null) {
    final reason = yesBecauseMatch.group(1)!.trim();
    final reasonNum = int.tryParse(reason);
    if (reasonNum != null) {
      return '네, 계산 결과가 $reasonNum이기 때문입니다.';
    }
    return '네, $reason이기 때문입니다.';
  }

  final noBecauseMatch = RegExp(
    r'^no,?\s*because\s*(?:it\s+is\s*)?(.+)$',
    caseSensitive: false,
  ).firstMatch(text);
  if (noBecauseMatch != null) {
    final reason = noBecauseMatch.group(1)!.trim();
    final reasonNum = int.tryParse(reason);
    if (reasonNum != null) {
      return '아니요, 계산 결과가 $reasonNum이기 때문입니다.';
    }
    return '아니요, $reason이기 때문입니다.';
  }

  if (lower == 'yes') return '네';
  if (lower == 'no') return '아니요';

  final andMatch =
      RegExp(r'^(\d+)\s+and\s+(\d+)$', caseSensitive: false).firstMatch(text);
  if (andMatch != null) {
    return '${andMatch.group(1)}과 ${andMatch.group(2)}';
  }

  final andExprMatch =
      RegExp(r'(.+?)\s+and\s+(.+)', caseSensitive: false).firstMatch(text);
  if (andExprMatch != null) {
    return '${andExprMatch.group(1)}와 ${andExprMatch.group(2)}';
  }

  if (RegExp(r'^[A-D](\s*,\s*[A-D])+$').hasMatch(text)) {
    return text
        .replaceAll('A', 'ㄱ')
        .replaceAll('B', 'ㄴ')
        .replaceAll('C', 'ㄷ')
        .replaceAll('D', 'ㄹ');
  }

  if (lower == 'total amount' || lower == 'total count' || lower == 'total') {
    return '전체 수';
  }
  if (lower == 'remaining amount' ||
      lower == 'remaining count' ||
      lower == 'remaining' ||
      lower == 'leftover') {
    return '남은 수';
  }
  if (lower == 'initial amount' ||
      lower == 'initial count' ||
      lower == 'initial') {
    return '처음 수';
  }
  if (lower == 'addition' || lower == 'add') return '더하기';
  if (lower == 'subtraction' || lower == 'subtract') return '빼기';
  if (lower == 'multiplication' || lower == 'multiply') return '곱하기';
  if (lower == 'division' || lower == 'divide') return '나누기';

  return text;
}

List<SolvableHint> _diagnosticQuestionHints(ProblemContent content) {
  final understanding = _mapAt(content.solvable, 'understanding');
  final rawList = understanding['diagnostic_questions'] ??
      content.solvable['diagnostic_questions'];
  if (rawList is! List || rawList.isEmpty) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (var i = 0; i < rawList.length; i++) {
    final item = rawList[i];
    if (item is! Map) {
      continue;
    }
    final prompt = _readText(item['prompt']);
    if (prompt.isEmpty) {
      continue;
    }
    final choicesList = item['choices'];
    final rawChoices = choicesList is List
        ? choicesList.map((c) => _extractChoiceLabel(c)).where((s) => s.isNotEmpty).toList()
        : <String>[];
    if (rawChoices.isEmpty) {
      continue;
    }

    final answerIndex =
        item['answer_index'] is int ? item['answer_index'] as int : 0;
    final rawAnswer = (answerIndex >= 0 && answerIndex < rawChoices.length)
        ? rawChoices[answerIndex]
        : _readText(item['answer'], fallback: rawChoices.first);

    final choices = rawChoices
        .map((choice) {
          final loc = _localizeChoice(choice);
          return HintChoice(
            label: loc,
            isCorrect: choice == rawAnswer,
          );
        })
        .toList();

    final level = i + 1;
    final localizedPrompt = _localizeText(prompt);
    final localizedAnswer = _localizeChoice(rawAnswer);

    hints.add(
      SolvableHint(
        level: level,
        title: '$level단계: 개념 확인 $level',
        body: localizedPrompt,
        miniQuestion: localizedPrompt,
        choices: choices,
        acceptedAnswers: [localizedAnswer, rawAnswer],
        successMessage: '맞아요! $localizedAnswer입니다.',
      ),
    );
  }
  return hints;
}

List<SolvableHint> _expandedAdditionHints(ProblemContent content) {
  final problemType =
      _readText(content.solvable['problem_type']).toLowerCase();
  final relation =
      _mapAt(_mapAt(content.solvable, 'understanding'), 'relation');
  final relationType = relation['type']?.toString().toLowerCase() ?? '';
  final isExpanded = (problemType.contains('expanded') ||
          problemType.contains('place_value') ||
          problemType.contains('decomposition') ||
          problemType.contains('부분합') ||
          problemType.contains('자리값') ||
          relationType.contains('expanded') ||
          relationType.contains('place_value') ||
          relationType.contains('decomposition')) &&
      !_isMultiplicationProblem(content);

  if (!isExpanded) {
    return const [];
  }

  final steps = content.solvable['steps'];
  if (steps is! List || steps.isEmpty) {
    return const [];
  }

  final hints = <SolvableHint>[];
  for (var i = 0; i < steps.length; i++) {
    final step = steps[i];
    if (step is! Map) {
      continue;
    }
    final stepId = step['id']?.toString() ?? '';
    if (stepId.contains('collect')) {
      continue;
    }

    final expr = _readText(step['expr']);
    final value = step['value'];
    final explanation = _readText(step['explanation']);
    final level = hints.length + 1;

    String title = '$level단계: 계산 ($expr)';
    String body = explanation.isNotEmpty ? explanation : '$expr을 계산해요.';
    String miniQ = '$expr의 값은 얼마인가요?';

    if (stepId.contains('first') || (stepId.contains('decompose') && i == 0)) {
      title = '$level단계: 첫 번째 수의 자리값 분해 ($expr)';
      body = explanation.isNotEmpty ? explanation : '$expr에서 알맞은 자리값을 찾아요.';
      miniQ = '첫 번째 수의 빈칸에 들어갈 자리값은 얼마인가요?';
    } else if (stepId.contains('second') || (stepId.contains('decompose') && i == 1)) {
      title = '$level단계: 두 번째 수의 자리값 분해 ($expr)';
      body = explanation.isNotEmpty ? explanation : '$expr에서 알맞은 자리값을 찾아요.';
      miniQ = '두 번째 수의 빈칸에 들어갈 자리값은 얼마인가요?';
    } else if (stepId.contains('ones') || expr.contains('일의 자리')) {
      title = '$level단계: 일의 자리 부분합 ($expr)';
      body = '일의 자리 숫자끼리 먼저 더해요. $explanation';
      miniQ = '첫 번째 칸에 들어갈 $expr의 값은 얼마인가요?';
    } else if (stepId.contains('tens') || expr.contains('십의 자리')) {
      title = '$level단계: 십의 자리 부분합 ($expr)';
      body = '십의 자리 숫자가 나타내는 실제 값을 더해요. $explanation';
      miniQ = '두 번째 칸에 들어갈 $expr의 값은 얼마인가요?';
    } else if (stepId.contains('hundreds') || expr.contains('백의 자리')) {
      title = '$level단계: 백의 자리 부분합 ($expr)';
      body = '백의 자리 숫자가 나타내는 실제 값을 더해요. $explanation';
      miniQ = '세 번째 칸에 들어갈 $expr의 값은 얼마인가요?';
    } else if (stepId.contains('total') || stepId.contains('partial_sums') || expr.contains('전체')) {
      title = '$level단계: 전체 합 완성하기 ($expr)';
      body = '구한 각 자리의 부분합을 모두 더해 전체 합을 완성해요. $explanation';
      miniQ = '마지막 칸에 들어갈 전체 합($expr)의 값은 얼마인가요?';
    }

    final int? numVal = _readInt(value);
    if (numVal == null) {
      continue;
    }

    final distractors = <int>[
      numVal >= 10 ? (numVal ~/ 10) : numVal + 1,
      numVal >= 10 ? numVal + 10 : (numVal > 1 ? numVal - 1 : numVal + 2),
      numVal >= 10 ? (numVal > 10 ? numVal - 10 : numVal * 10) : numVal * 10,
    ];

    hints.add(
      SolvableHint(
        level: level,
        title: title,
        body: body,
        miniQuestion: miniQ,
        choices: _numberChoices(numVal, distractors),
        acceptedAnswers: ['$numVal'],
        successMessage: '맞아요! $expr = $numVal입니다.',
      ),
    );
  }

  return hints;
}

List<SolvableHint> _baseTenModelHints(ProblemContent content) {
  final problemType =
      (content.semantic['problem_type'] ?? content.solvable['problem_type'] ?? '')
          .toString()
          .toLowerCase();
  final title = content.summary.title.toLowerCase();
  final prompt = content.prompt.toLowerCase();
  final isBaseTen = problemType.contains('base_ten_model') ||
      title.contains('수 모형') ||
      prompt.contains('수 모형');

  if (!isBaseTen) {
    return const [];
  }

  final hints = <SolvableHint>[];

  final diagnosticHints = _diagnosticQuestionHints(content);
  for (final hint in diagnosticHints) {
    hints.add(
      SolvableHint(
        level: hints.length + 1,
        title: '${hints.length + 1}단계: ${hint.title.replaceFirst(RegExp(r'^\d+단계:\s*'), '')}',
        body: hint.body,
        miniQuestion: hint.miniQuestion,
        choices: hint.choices,
        acceptedAnswers: hint.acceptedAnswers,
        successMessage: hint.successMessage,
      ),
    );
  }

  final steps = content.solvable['steps'];
  if (steps is List && steps.isNotEmpty) {
    for (final step in steps) {
      if (step is! Map) continue;
      final stepId = step['id']?.toString() ?? '';
      final expr = _readText(step['expr']);
      final explanation = _readText(step['explanation']);
      final val = step['value'];

      String stepTitle = '';
      String miniQ = '';
      List<String> accepted = [];
      List<HintChoice> choices = [];

      if (stepId.contains('add_ones') || stepId.contains('ones')) {
        stepTitle = '낱개 모형끼리 더하기 ($expr)';
        miniQ = '낱개 모형끼리 더한 개수($expr)는 몇 개인가요?';
      } else if (stepId.contains('regroup_tens') || stepId.contains('regroup')) {
        stepTitle = '십 모형 묶어 백 모형으로 바꾸기 ($expr)';
        miniQ = explanation.isNotEmpty ? explanation : '십 모형을 묶어 백 모형으로 바꾸어 보세요.';
      } else if (stepId.contains('add_direct_hundreds') || stepId.contains('direct_hundreds')) {
        stepTitle = '백 모형끼리 직접 더하기 ($expr)';
        miniQ = '원래 있던 백 모형끼리 더한 개수($expr)는 몇 개인가요?';
      } else if (stepId.contains('add_tens') || stepId.contains('tens')) {
        stepTitle = '십 모형끼리 더하기 ($expr)';
        miniQ = '십 모형끼리 더한 개수($expr)는 몇 개인가요?';
      } else if (stepId.contains('add_carried_hundred') || stepId.contains('carried')) {
        stepTitle = '받아올린 백 모형 합치기 ($expr)';
        miniQ = '받아올린 모형을 합친 백 모형의 개수($expr)는 몇 개인가요?';
      } else if (stepId.contains('compose_total') || stepId.contains('total')) {
        stepTitle = '전체 합 완성하기';
        miniQ = '수 모형으로 구한 최종 합($expr)은 얼마인가요?';
      } else {
        continue;
      }

      if (val is int || (val is String && int.tryParse(val) != null)) {
        final intNum = _readInt(val)!;
        accepted = ['$intNum', '$intNum개'];
        final distractors = <int>[
          intNum >= 10 ? intNum ~/ 10 : intNum + 1,
          intNum >= 10 ? intNum + 10 : (intNum > 1 ? intNum - 1 : intNum + 2),
          intNum >= 10 ? (intNum > 10 ? intNum - 10 : intNum * 10) : intNum * 10,
        ];
        choices = _numberChoices(intNum, distractors);
      } else if (val is List && val.length == 2) {
        accepted = ['${val[0]} / ${val[1]}', '백 모형 ${val[0]}개와 십 모형 ${val[1]}개', '${val[0]}', '${val[1]}'];
        choices = [
          HintChoice(label: '백 모형 ${val[0]}개와 십 모형 ${val[1]}개', isCorrect: true),
          HintChoice(label: '백 모형 ${val[1]}개와 십 모형 ${val[0]}개'),
          HintChoice(label: '백 모형 ${val[0]}개와 십 모형 ${val[0] + val[1]}개'),
        ];
      } else {
        continue;
      }

      if (hints.any((h) => h.body == explanation || h.title.contains(stepTitle))) {
        continue;
      }

      hints.add(
        SolvableHint(
          level: hints.length + 1,
          title: '${hints.length + 1}단계: $stepTitle',
          body: explanation.isNotEmpty ? explanation : '$expr을 계산해요.',
          miniQuestion: miniQ,
          choices: choices,
          acceptedAnswers: accepted,
          successMessage: '맞아요! $explanation',
        ),
      );
    }
  }

  if (hints.isEmpty) {
    final plan = content.solvable['plan'];
    if (plan is List) {
      for (var i = 0; i < plan.length; i++) {
        final planItem = _readText(plan[i]);
        if (planItem.isNotEmpty) {
          hints.add(
            SolvableHint(
              level: i + 1,
              title: '${i + 1}단계: 수 모형 확인하기',
              body: planItem,
              miniQuestion: '$planItem 순서대로 확인해 보세요.',
            ),
          );
        }
      }
    }
  }

  return hints;
}

List<SolvableHint> _wordProblemHints(ProblemContent content) {
  if (!_isWordProblem(content)) {
    return const [];
  }

  final hints = <SolvableHint>[];

  final diagnosticHints = _diagnosticQuestionHints(content);
  for (final hint in diagnosticHints) {
    hints.add(
      SolvableHint(
        level: hints.length + 1,
        title: '${hints.length + 1}단계: ${hint.title.replaceFirst(RegExp(r'^\d+단계:\s*'), '')}',
        body: hint.body,
        miniQuestion: hint.miniQuestion,
        choices: hint.choices,
        acceptedAnswers: hint.acceptedAnswers,
        successMessage: hint.successMessage,
      ),
    );
  }

  final steps = content.solvable['steps'];
  if (steps is List && steps.isNotEmpty) {
    for (final step in steps) {
      if (step is! Map) continue;
      final stepId = step['id']?.toString() ?? '';
      if (stepId.contains('collect')) continue;

      final expr = _readText(step['expr']);
      final goal = _readText(step['goal']);
      final explanation = _readText(step['explanation']);
      final int? numVal = _extractStepValue(step['value']);

      if (expr.isEmpty || numVal == null) continue;

      final level = hints.length + 1;
      final title = goal.isNotEmpty
          ? '$level단계: $goal ($expr)'
          : '$level단계: $expr 계산하기';
      final body = explanation.isNotEmpty ? explanation : '$expr을 계산해요.';
      final miniQ = '$expr의 값은 얼마인가요?';

      final distractors = <int>[
        numVal > 10 ? (numVal - 10) : numVal + 1,
        numVal >= 10 ? (numVal + 10) : (numVal > 1 ? numVal - 1 : numVal + 2),
      ];

      hints.add(
        SolvableHint(
          level: level,
          title: title,
          body: body,
          miniQuestion: miniQ,
          choices: _numberChoices(numVal, distractors),
          acceptedAnswers: ['$numVal', '$numVal${content.summary.unit}'],
          successMessage: '맞아요! $expr = $numVal입니다.',
        ),
      );
    }
  }

  return hints;
}

bool _isWordProblem(ProblemContent content) {
  final problemType =
      _readText(content.solvable['problem_type']).toLowerCase();
  final subUnit = content.summary.subUnit.toLowerCase();
  final title = content.summary.title.toLowerCase();
  final prompt = content.prompt;

  return problemType.contains('word_problem') ||
      problemType.contains('문장제') ||
      subUnit.contains('문장제') ||
      subUnit.contains('실생활') ||
      title.contains('구슬') ||
      title.contains('연필') ||
      title.contains('학생') ||
      prompt.length > 40;
}

int? _extractStepValue(Object? value) {
  if (value is num) return value.toInt();
  if (value is Map) {
    return _readInt(value['count']) ?? _readInt(value['value']);
  }
  return _readInt(value);
}

List<SolvableHint> _multiplicationPlaceValueHints(ProblemContent content) {
  if (!_isMultiplicationPlaceValueProblem(content)) {
    return const [];
  }

  final targetExpr = _findMultiplicationTargetExpression(content);
  if (targetExpr == null) {
    return const [];
  }

  final match = RegExp(r'(\d+)\s*[×x*]\s*(\d+)').firstMatch(targetExpr);
  if (match == null) {
    return const [];
  }

  final termA = int.parse(match.group(1)!);
  final termB = int.parse(match.group(2)!);

  final int placeValue;
  final int multiplier;
  if (termA >= 10 || termB < 10) {
    placeValue = termA;
    multiplier = termB;
  } else {
    placeValue = termB;
    multiplier = termA;
  }

  final firstDigit = int.parse(placeValue.toString()[0]);
  final String placeName;
  if (placeValue < 10) {
    placeName = '일의 자리';
  } else if (placeValue < 100) {
    placeName = '십의 자리';
  } else if (placeValue < 1000) {
    placeName = '백의 자리';
  } else {
    placeName = '천의 자리';
  }

  final multiplicand = _findMultiplicand(content);
  final product = placeValue * multiplier;
  final multiplicandPrefix =
      multiplicand != null ? '$multiplicand에서 ' : '';

  final step1Distractors = <int>[firstDigit];
  if (placeValue >= 100) {
    step1Distractors.add(placeValue ~/ 10);
  } else if (placeValue >= 10) {
    step1Distractors.add(placeValue * 10);
  } else {
    step1Distractors.add(firstDigit * 10);
  }

  final step2Distractors = <int>[
    multiplier == 4 ? 2 : (multiplier > 2 ? multiplier - 2 : multiplier + 2),
    multiplier == 4 ? 8 : (multiplier + 4) % 9 + 1,
  ];

  final step3DistractorList = <String>[
    '$firstDigit × $multiplier',
    placeValue >= 100
        ? '${placeValue ~/ 10} × $multiplier'
        : '${placeValue * 10} × $multiplier',
  ];

  return [
    SolvableHint(
      level: 1,
      title: '1단계: 색칠된 자리의 실제 값 찾기',
      body: '$multiplicandPrefix색칠된 자리의 숫자 $firstDigit은 실제 얼마를 나타내는지 확인해요.',
      miniQuestion: '$multiplicandPrefix숫자 $firstDigit은 실제 얼마를 나타내나요?',
      choices: _numberChoices(placeValue, step1Distractors),
      acceptedAnswers: ['$placeValue'],
      successMessage: '맞아요. $firstDigit은 $placeName 숫자이므로 실제로는 $placeValue입니다.',
    ),
    SolvableHint(
      level: 2,
      title: '2단계: 곱하는 수 확인',
      body: '색칠된 부분에 곱해지는 한 자리 수를 확인해요.',
      miniQuestion: '곱하는 수는 얼마인가요?',
      choices: _numberChoices(multiplier, step2Distractors),
      acceptedAnswers: ['$multiplier'],
      successMessage: '좋아요. 곱하는 수는 $multiplier입니다.',
    ),
    SolvableHint(
      level: 3,
      title: '3단계: 알맞은 곱셈식 완성',
      body: '색칠된 부분($product)은 $placeValue과 $multiplier의 곱이에요.',
      miniQuestion: '색칠된 부분을 나타내는 알맞은 곱셈식은 무엇인가요?',
      choices: _textChoices('$placeValue × $multiplier', step3DistractorList),
      acceptedAnswers: [
        '$placeValue × $multiplier',
        '$placeValue×$multiplier',
        '$placeValue * $multiplier',
      ],
      successMessage: '정답이에요! 색칠된 부분은 $placeValue × $multiplier를 나타냅니다.',
    ),
  ];
}

bool _isMultiplicationPlaceValueProblem(ProblemContent content) {
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    _readText(content.solvable['problem_type']),
    _readText(content.solvable['method']),
    content.prompt,
    _readText(content.solvable['target']),
    _readText(content.solvable['plan']),
  ].join(' ').toLowerCase();

  return (pieces.contains('multiplication') ||
          pieces.contains('곱셈') ||
          pieces.contains('세로셈')) &&
      (pieces.contains('place_value') ||
          pieces.contains('place value') ||
          pieces.contains('자리값') ||
          pieces.contains('부분곱') ||
          pieces.contains('shaded') ||
          pieces.contains('색칠') ||
          pieces.contains('어떤 수의 곱'));
}

String? _findMultiplicationTargetExpression(ProblemContent content) {
  final candidates = <String>[
    content.correctAnswer,
    _readText(content.solvable['target']),
    _readText(_mapAt(content.solvable, 'answer')['value']),
    _readText(content.solvable['given']),
    _readText(content.solvable['steps']),
  ];

  for (final item in candidates) {
    final match = RegExp(r'(\d+)\s*[×x*]\s*(\d+)').firstMatch(item);
    if (match != null) {
      return '${match.group(1)} × ${match.group(2)}';
    }
  }
  return null;
}

int? _findMultiplicand(ProblemContent content) {
  final pieces = <String>[
    _readText(content.solvable['given']),
    _readText(content.solvable['steps']),
    _readText(content.solvable['plan']),
    content.prompt,
  ].join(' ');

  final match = RegExp(r'(\d{2,4})\s*[×x*]').firstMatch(pieces);
  if (match != null) {
    return int.tryParse(match.group(1)!);
  }
  final digitMatch = RegExp(r'(\d{3,4})의\s*\d').firstMatch(pieces);
  if (digitMatch != null) {
    return int.tryParse(digitMatch.group(1)!);
  }
  return null;
}

List<SolvableHint> _planBasedHints(ProblemContent content) {
  final rawPlan = content.solvable['plan'];
  if (rawPlan is! List || rawPlan.isEmpty) {
    return const [];
  }
  final planItems = rawPlan
      .map((p) => _readText(p))
      .where((p) => p.isNotEmpty)
      .toList();
  if (planItems.isEmpty) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (var i = 0; i < planItems.length; i++) {
    final level = i + 1;
    final text = _localizeText(planItems[i]);
    hints.add(
      SolvableHint(
        level: level,
        title: '$level단계: 풀이 안내 $level',
        body: text,
      ),
    );
  }
  return hints;
}

List<SolvableHint> _comparisonHints(ProblemContent content) {
  if (!_isComparisonProblem(content)) {
    return const [];
  }

  final subproblemHints = _comparisonSubproblemHints(content);
  if (subproblemHints.isNotEmpty) {
    return subproblemHints;
  }

  final diagnosticHints = _diagnosticQuestionHints(content);
  if (diagnosticHints.isNotEmpty) {
    return diagnosticHints;
  }

  final steps = content.solvable['steps'];
  if (steps is List && steps.isNotEmpty) {
    final hints = <SolvableHint>[];
    for (final step in steps) {
      if (step is! Map) continue;
      final expr = _readText(step['expr']);
      final explanation = _readText(step['explanation']);
      final value = step['value'];
      final level = hints.length + 1;

      if (expr.isEmpty || value == null) continue;

      final valStr = value.toString().trim();
      final isOperator = valStr == '>' || valStr == '<' || valStr == '=';

      if (isOperator) {
        hints.add(
          SolvableHint(
            level: level,
            title: '$level단계: 알맞은 부등호 기호 선택 ($expr)',
            body: explanation.isNotEmpty
                ? explanation
                : '$expr에 알맞은 기호를 골라요.',
            miniQuestion: '○ 안에 들어갈 알맞은 기호는 무엇인가요?',
            choices: _textChoices(
              valStr,
              ['>', '=', '<'].where((s) => s != valStr).toList(),
            ),
            acceptedAnswers: [valStr],
            successMessage: '정답이에요! $valStr를 선택합니다.',
          ),
        );
      } else {
        final int? numVal = _readInt(value);
        if (numVal != null) {
          final distractors = <int>[numVal - 10, numVal + 10];
          hints.add(
            SolvableHint(
              level: level,
              title: '$level단계: 식 계산하기 ($expr)',
              body: explanation.isNotEmpty
                  ? explanation
                  : '$expr을 계산해요.',
              miniQuestion: '$expr의 값은 얼마인가요?',
              choices: _numberChoices(numVal, distractors),
              acceptedAnswers: ['$numVal'],
              successMessage: '맞아요! $expr = $numVal입니다.',
            ),
          );
        }
      }
    }
    if (hints.isNotEmpty) {
      return hints;
    }
  }

  return const [];
}

List<SolvableHint> _comparisonSubproblemHints(ProblemContent content) {
  if (!_isComparisonProblem(content)) {
    return const [];
  }
  final quantities = _mapAt(content.solvable['inputs'], 'quantities');
  final allEntries = quantities.entries
      .where((entry) => entry.value is Map)
      .map((entry) => MapEntry(entry.key.toString(), entry.value as Map))
      .where(
        (entry) =>
            entry.value.containsKey('left_expression') &&
            entry.value.containsKey('right_expression'),
      )
      .toList()
    ..sort((a, b) => a.key.compareTo(b.key));
  final entries = _selectComparisonEntriesForContent(content, allEntries);
  if (entries.isEmpty) {
    return const [];
  }

  final hints = <SolvableHint>[];
  for (final entry in entries.indexed) {
    final number = _comparisonEntryNumber(entry.$2.key) ?? entry.$1 + 1;
    final groupKey = entries.length > 1 ? '$number' : null;
    final groupLabel = entries.length > 1 ? '($number)' : null;
    final data = entry.$2.value;
    final leftExpression = data['left_expression']?.toString() ?? '';
    final rightExpression = data['right_expression']?.toString() ?? '';
    final leftValue = _readInt(data['left_value']);
    final rightValue = _readInt(data['right_value']);
    if (leftExpression.isEmpty ||
        rightExpression.isEmpty ||
        leftValue == null ||
        rightValue == null) {
      continue;
    }
    final operator = leftValue > rightValue
        ? '>'
        : leftValue < rightValue
            ? '<'
            : '=';
    hints.addAll(
      _comparisonHintsForSubproblem(
        number: number,
        leftExpression: leftExpression,
        leftValue: leftValue,
        rightExpression: rightExpression,
        rightValue: rightValue,
        operator: operator,
        groupKey: groupKey,
        groupLabel: groupLabel,
      ),
    );
  }
  return hints;
}

List<SolvableHint> _comparisonHintsForSubproblem({
  required int number,
  required String leftExpression,
  required int leftValue,
  required String rightExpression,
  required int rightValue,
  required String operator,
  String? groupKey,
  String? groupLabel,
}) {
  final hints = <SolvableHint>[];
  var level = 1;
  final leftNeedsCalculation = _additionExpressionTerms(leftExpression) != null;
  final rightNeedsCalculation =
      _additionExpressionTerms(rightExpression) != null;
  if (leftNeedsCalculation) {
    level = _appendExpressionPlaceValueHints(
      hints,
      problemNumber: number,
      sideLabel: '왼쪽',
      expression: leftExpression,
      expectedValue: leftValue,
      startLevel: level,
      groupKey: groupKey,
      groupLabel: groupLabel,
    );
  }
  if (rightNeedsCalculation) {
    level = _appendExpressionPlaceValueHints(
      hints,
      problemNumber: number,
      sideLabel: '오른쪽',
      expression: rightExpression,
      expectedValue: rightValue,
      startLevel: level,
      groupKey: groupKey,
      groupLabel: groupLabel,
    );
  }
  if (!leftNeedsCalculation && !rightNeedsCalculation) {
    level = _appendDirectComparisonValuesHint(
      hints,
      problemNumber: number,
      leftValue: leftValue,
      rightValue: rightValue,
      startLevel: level,
      groupKey: groupKey,
      groupLabel: groupLabel,
    );
  }
  final titleProblemLabel = groupLabel == null ? '' : ' $groupLabel';
  final questionProblemLabel = groupLabel == null ? '' : '$number번 ';
  hints.add(
    SolvableHint(
      level: level,
      title: '$level단계:$titleProblemLabel 비교 기호 고르기',
      body: '계산한 두 값을 비교해요. 왼쪽은 $leftValue, 오른쪽은 $rightValue입니다.',
      miniQuestion: '$questionProblemLabel빈칸에 들어갈 기호는 무엇인가요?',
      choices: _textChoices(operator, ['>', '=', '<']),
      acceptedAnswers: [operator],
      groupKey: groupKey,
      groupLabel: groupLabel,
      successMessage: '좋아요. $leftValue $operator $rightValue입니다.',
    ),
  );
  return _withHintGroup(hints, groupKey: groupKey, groupLabel: groupLabel);
}

List<MapEntry<String, Map<dynamic, dynamic>>>
    _selectComparisonEntriesForContent(
  ProblemContent content,
  List<MapEntry<String, Map<dynamic, dynamic>>> entries,
) {
  final suffixNumber = _subproblemNumberFromProblemId(content.summary.id);
  if (suffixNumber != null) {
    final suffixKey = 'problem_$suffixNumber';
    final selected = entries.where((entry) => entry.key == suffixKey).toList();
    if (selected.isNotEmpty) {
      return selected;
    }
  }
  final answerCount = _answerKeyCount(content);
  if (answerCount > 0 && answerCount < entries.length) {
    return entries.take(answerCount).toList();
  }
  return entries;
}

int? _subproblemNumberFromProblemId(String problemId) {
  final match = RegExp(r'_(\d+)$').firstMatch(problemId);
  if (match == null) {
    return null;
  }
  return int.tryParse(match.group(1)!);
}

int? _comparisonEntryNumber(String key) {
  final match = RegExp(r'^problem_(\d+)$').firstMatch(key);
  if (match == null) {
    return null;
  }
  return int.tryParse(match.group(1)!);
}

int _answerKeyCount(ProblemContent content) {
  final answer = _mapAt(content.solvable, 'answer').isNotEmpty
      ? _mapAt(content.solvable, 'answer')
      : _mapAt(content.semantic, 'answer');
  final key = answer['answer_key'];
  if (key is List && key.isNotEmpty) {
    return key.length;
  }
  final values = answer['values'];
  if (values is List && values.isNotEmpty) {
    return values.length;
  }
  final blanks = answer['blanks'];
  if (blanks is List && blanks.isNotEmpty) {
    return blanks.length;
  }
  return 0;
}

int _appendDirectComparisonValuesHint(
  List<SolvableHint> hints, {
  required int problemNumber,
  required int leftValue,
  required int rightValue,
  required int startLevel,
  String? groupKey,
  String? groupLabel,
}) {
  final titleProblemLabel = groupLabel == null ? '' : ' $groupLabel';
  final questionProblemLabel = groupLabel == null ? '' : '$problemNumber번 ';
  hints.add(
    SolvableHint(
      level: startLevel,
      title: '$startLevel단계:$titleProblemLabel 두 값 확인',
      body: '양쪽이 모두 수로 주어졌어요. 왼쪽 값과 오른쪽 값을 그대로 확인합니다.',
      miniQuestion: '$questionProblemLabel왼쪽 값은 무엇인가요?',
      choices: _numberChoices(leftValue, [leftValue - 10, leftValue + 10]),
      acceptedAnswers: ['$leftValue'],
      groupKey: groupKey,
      groupLabel: groupLabel,
      successMessage: '맞아요. 왼쪽 값은 $leftValue입니다.',
    ),
  );
  return startLevel + 1;
}

int _appendExpressionPlaceValueHints(
  List<SolvableHint> hints, {
  required int problemNumber,
  required String sideLabel,
  required String expression,
  required int expectedValue,
  required int startLevel,
  String? groupKey,
  String? groupLabel,
}) {
  final terms = _additionExpressionTerms(expression);
  if (terms == null) {
    return startLevel;
  }
  final titleProblemLabel = groupLabel == null ? '' : ' $groupLabel';
  final questionProblemLabel = groupLabel == null ? '' : '$problemNumber번 ';

  final left = terms[0];
  final right = terms[1];
  final onesLeft = left % 10;
  final onesRight = right % 10;
  final onesSum = onesLeft + onesRight;
  final onesDigit = onesSum % 10;
  final carryToTens = onesSum ~/ 10;
  final tensLeft = (left ~/ 10) % 10;
  final tensRight = (right ~/ 10) % 10;
  final tensSum = tensLeft + tensRight + carryToTens;
  final tensDigit = tensSum % 10;
  final carryToHundreds = tensSum ~/ 10;
  final hundredsLeft = (left ~/ 100) % 10;
  final hundredsRight = (right ~/ 100) % 10;

  hints.add(
    SolvableHint(
      level: startLevel,
      title: '$startLevel단계:$titleProblemLabel $sideLabel 일의 자리 더하기',
      body: '$sideLabel 식 $expression을 일의 자리부터 계산해요.',
      miniQuestion: '$onesLeft + $onesRight은 얼마인가요?',
      choices: _numberChoices(onesSum, [onesDigit, onesSum + 1]),
      acceptedAnswers: ['$onesSum'],
      successMessage: '맞아요. 일의 자리 합은 $onesSum입니다.',
    ),
  );
  hints.add(
    SolvableHint(
      level: startLevel + 1,
      title: '${startLevel + 1}단계:$titleProblemLabel $sideLabel 십의 자리 더하기',
      body: '일의 자리에서 올린 $carryToTens도 십의 자리 계산에 함께 넣어요.',
      miniQuestion: '십의 자리 계산으로 알맞은 것은 무엇인가요?',
      choices: _textChoices(
        '$tensLeft + $tensRight + $carryToTens',
        ['$tensLeft + $tensRight', '$onesLeft + $onesRight'],
      ),
      acceptedAnswers: [
        '$tensLeft+$tensRight+$carryToTens',
        '$tensLeft + $tensRight + $carryToTens',
      ],
      successMessage: '좋아요. 십의 자리에는 $tensDigit을 쓰고 $carryToHundreds을 올립니다.',
    ),
  );
  hints.add(
    SolvableHint(
      level: startLevel + 2,
      title: '${startLevel + 2}단계:$titleProblemLabel $sideLabel 값 완성',
      body: '마지막으로 백의 자리까지 계산해 $sideLabel 값을 완성해요.',
      miniQuestion: '$questionProblemLabel$sideLabel 식 $expression의 값은 무엇인가요?',
      choices: _numberChoices(
        expectedValue,
        [
          (hundredsLeft + hundredsRight) * 100 + tensDigit * 10 + onesDigit,
          expectedValue + 10,
        ],
      ),
      acceptedAnswers: ['$expectedValue'],
      successMessage: '맞아요. $sideLabel 값은 $expectedValue입니다.',
    ),
  );
  return startLevel + 3;
}

List<int>? _additionExpressionTerms(String expression) {
  final match = RegExp(r'^\s*(\d+)\s*\+\s*(\d+)\s*$').firstMatch(expression);
  if (match == null) {
    return null;
  }
  return [int.parse(match.group(1)!), int.parse(match.group(2)!)];
}

List<SolvableHint> _columnAdditionHints(ProblemContent content) {
  final termSets = _additionTermSets(content);
  if (termSets.isEmpty || !_isAdditionProblem(content)) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (final entry in termSets.indexed) {
    final titlePrefix = termSets.length > 1 ? '(${entry.$1 + 1}) ' : '';
    final groupKey = termSets.length > 1 ? '${entry.$1 + 1}' : null;
    final groupLabel = termSets.length > 1 ? '(${entry.$1 + 1})' : null;
    hints.addAll(
      _withHintGroup(
        _columnAdditionHintsForTerms(
          entry.$2[0].abs(),
          entry.$2[1].abs(),
          startLevel: 1,
          titlePrefix: titlePrefix,
        ),
        groupKey: groupKey,
        groupLabel: groupLabel,
      ),
    );
  }
  return hints;
}

List<SolvableHint> _columnAdditionHintsForTerms(
  int left,
  int right, {
  required int startLevel,
  String titlePrefix = '',
}) {
  final answer = left + right;
  final onesLeft = left % 10;
  final onesRight = right % 10;
  final onesSum = onesLeft + onesRight;
  final onesDigit = onesSum % 10;
  final carryToTens = onesSum ~/ 10;
  final tensLeft = (left ~/ 10) % 10;
  final tensRight = (right ~/ 10) % 10;
  final tensSum = tensLeft + tensRight + carryToTens;
  final tensDigit = tensSum % 10;
  final carryToHundreds = tensSum ~/ 10;
  final hundredsLeft = (left ~/ 100) % 10;
  final hundredsRight = (right ~/ 100) % 10;
  final hundredsSum = hundredsLeft + hundredsRight + carryToHundreds;

  return [
    SolvableHint(
      level: startLevel,
      title: '$startLevel단계: $titlePrefix일의 자리 더하기',
      body: '맨 오른쪽 일의 자리부터 더해요.',
      miniQuestion: '$onesLeft + $onesRight은 얼마인가요?',
      choices: _numberChoices(onesSum, [onesSum - 1, onesDigit, onesSum + 1]),
      acceptedAnswers: ['$onesSum'],
      successMessage: '맞아요. 일의 자리 합은 $onesSum이에요.',
    ),
    SolvableHint(
      level: startLevel + 1,
      title: '${startLevel + 1}단계: $titlePrefix일의 자리 쓰기',
      body: '$onesSum처럼 10을 넘으면 일의 자리 숫자만 아래에 쓰고, 1은 다음 자리로 올려요.',
      miniQuestion: '일의 자리에는 어떤 숫자를 쓰나요?',
      choices: _numberChoices(
        onesDigit,
        [onesSum, carryToTens, (onesDigit + 1) % 10],
      ),
      acceptedAnswers: ['$onesDigit'],
      successMessage: '좋아요. 일의 자리에는 $onesDigit을 쓰고, $carryToTens을 십의 자리로 올려요.',
    ),
    SolvableHint(
      level: startLevel + 2,
      title: '${startLevel + 2}단계: $titlePrefix십의 자리 더하기',
      body: '십의 자리 숫자들을 더할 때, 아까 올린 수도 함께 더해요.',
      miniQuestion: '십의 자리 계산으로 알맞은 것은 무엇인가요?',
      choices: _textChoices(
        '$tensLeft + $tensRight + $carryToTens',
        [
          '$tensLeft + $tensRight',
          '$onesLeft + $onesRight',
        ],
      ),
      acceptedAnswers: [
        '$tensLeft+$tensRight+$carryToTens',
        '$tensLeft + $tensRight + $carryToTens',
      ],
      successMessage:
          '맞아요. $tensLeft + $tensRight에 올린 $carryToTens을 더해서 $tensSum이 돼요.',
    ),
    SolvableHint(
      level: startLevel + 3,
      title: '${startLevel + 3}단계: $titlePrefix백의 자리와 답',
      body: '십의 자리에서 또 10을 넘으면 1을 백의 자리로 올려요. 마지막으로 각 자리 숫자를 이어 답을 만들어요.',
      miniQuestion: '백의 자리까지 계산하면 알맞은 답은 무엇인가요?',
      choices: _numberChoices(
        answer,
        [
          hundredsSum * 100 + tensDigit * 10 + onesSum,
          hundredsSum * 100 + (tensSum % 10) * 10 + carryToTens,
          answer + 10,
        ],
      ),
      acceptedAnswers: ['$answer'],
      successMessage: '좋아요. 일의 자리, 십의 자리, 백의 자리를 모두 확인했어요.',
    ),
  ];
}

List<HintChoice> _numberChoices(int correct, List<int> distractors) {
  final labels = <String>[];
  void add(int value) {
    if (value < 0) {
      return;
    }
    final label = value.toString();
    if (!labels.contains(label)) {
      labels.add(label);
    }
  }

  add(correct);
  for (final value in distractors) {
    add(value);
  }
  while (labels.length < 3) {
    add(correct + labels.length);
  }
  return labels
      .take(3)
      .map((label) => HintChoice(label: label, isCorrect: label == '$correct'))
      .toList();
}

List<HintChoice> _textChoices(String correct, List<String> distractors) {
  final labels = <String>[];
  void add(String value) {
    final label = value.trim();
    if (label.isNotEmpty && !labels.contains(label)) {
      labels.add(label);
    }
  }

  add(correct);
  for (final distractor in distractors) {
    add(distractor);
  }
  return labels
      .take(3)
      .map((label) => HintChoice(label: label, isCorrect: label == correct))
      .toList();
}

List<SolvableHint> _authoredStudentHints(ProblemContent content) {
  final rawHints = content.solvable['student_hints'];
  if (rawHints is! List) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (final item in rawHints) {
    if (item is! Map) {
      continue;
    }
    final level =
        item['level'] is int ? item['level'] as int : hints.length + 1;
    final body = _localizeText(_readText(item['text']));
    if (body.isEmpty) {
      continue;
    }
    final rawTitle = _readText(item['title'], fallback: '$level단계');
    hints.add(
      SolvableHint(
        level: level,
        title: _localizeText(rawTitle),
        body: _withoutAnswer(content, body),
        miniQuestion: _localizeText(_readText(item['mini_question'])),
      ),
    );
  }
  hints.sort((a, b) => a.level.compareTo(b.level));
  return hints;
}

List<SolvableHint> _editorHints(ProblemContent content) {
  final flow = content.renderer['tutor_flow'];
  if (flow is! List) return const [];
  final hints = <SolvableHint>[];
  for (final step in flow.whereType<Map>()) {
    if (step['phase'] != 'hint' || step['text'] is! String || (step['text'] as String).trim().isEmpty) continue;
    final frames = <Map<String, dynamic>>[];
    final rawFrames = step['frames'];
    if (rawFrames is List) {
      for (final frame in rawFrames.whereType<Map>()) {
        final overlays = frame['overlays'];
        if (overlays is! List || overlays.isEmpty) continue;
        final targets = overlays.whereType<Map>().where((o) => o['type'] == 'highlight').map((o) => o['target_ref']).toSet();
        dynamic highlight(dynamic element) {
          if (element is! Map) return element;
          final copy = Map<String, dynamic>.from(element);
          final refs = element['refs'];
          if (targets.contains(element['id']) || targets.contains(element['source_ref']) || (refs is Map && refs.values.any(targets.contains))) {
            copy['attributes'] = {...?element['attributes'] as Map?, 'stroke': '#0f766e', 'stroke-width': 4};
          }
          if (element['elements'] is List) copy['elements'] = (element['elements'] as List).map(highlight).toList();
          return copy;
        }
        final elements = ((content.renderer['elements'] as List?) ?? []).map(highlight).toList();
        for (final overlay in overlays.whereType<Map>()) {
          if (overlay['type'] != 'label') continue;
          final style = overlay['style'] is Map ? overlay['style'] as Map : {};
          elements.add({'id': 'hint.label.${elements.length}', 'type': 'text', 'text': overlay['text'] ?? '', 'attributes': {'x': overlay['x'] ?? 40, 'y': (overlay['y'] as num? ?? 40) + (style['font_size'] as num? ?? 24), 'font-size': style['font_size'] ?? 24, 'fill': style['fill'] ?? '#0f766e'}});
        }
        frames.add({...content.renderer, 'elements': elements});
      }
    }
    final title = step['title'] is String ? (step['title'] as String).trim() : '';
    hints.add(SolvableHint(level: hints.length + 1, title: title.isEmpty ? '힌트 ${hints.length + 1}' : title, body: step['text'] as String, rendererFrames: frames));
  }
  return hints;
}

bool _isAdditionProblem(ProblemContent content) {
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    _readText(content.solvable['method']),
    _readText(content.solvable['problem_type']),
    _readText(content.solvable['plan']),
    _readText(content.solvable['steps']),
  ].join(' ').toLowerCase();
  return pieces.contains('addition') ||
      pieces.contains('add_parts') ||
      pieces.contains('vertical_addition') ||
      pieces.contains('+') ||
      pieces.contains('더하기') ||
      pieces.contains('덧셈');
}

bool _isMultiplicationProblem(ProblemContent content) {
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    _readText(content.solvable['method']),
    _readText(content.solvable['problem_type']),
    _readText(content.solvable['plan']),
    _readText(content.solvable['steps']),
  ].join(' ').toLowerCase();
  return pieces.contains('multiplication') ||
      pieces.contains('multiply') ||
      pieces.contains('times') ||
      pieces.contains('×') ||
      pieces.contains('*') ||
      pieces.contains('곱하기') ||
      pieces.contains('곱셈');
}

bool _isComparisonProblem(ProblemContent content) {
  final inputs = _mapAt(content.solvable, 'inputs');
  final relation =
      _mapAt(_mapAt(content.solvable, 'understanding'), 'relation');
  final relationType = relation['type']?.toString().toLowerCase() ?? '';
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    content.summary.title,
    content.summary.subUnit,
    content.prompt,
    _readText(content.solvable['method']),
    _readText(content.solvable['problem_type']),
    _readText(inputs['answer_type']),
    relationType,
  ].join(' ').toLowerCase();

  final hasSymbols = inputs['allowed_symbols'] is List ||
      inputs.containsKey('left_expression') ||
      inputs.containsKey('right_value');

  return pieces.contains('comparison') ||
      pieces.contains('compare') ||
      pieces.contains('비교') ||
      pieces.contains('크기') ||
      pieces.contains('부등호') ||
      pieces.contains('comparison_operator') ||
      hasSymbols;
}

List<List<int>> _additionTermSets(ProblemContent content) {
  final fromQuantities = _additionTermSetsFromQuantities(content);
  if (fromQuantities.isNotEmpty) {
    return fromQuantities;
  }

  final fromSteps = _additionTermSetsFromSteps(content);
  if (fromSteps.isNotEmpty) {
    return fromSteps;
  }

  final terms = _additionTerms(content);
  return terms.length >= 2 ? [terms.take(2).toList()] : const [];
}

List<List<int>> _additionTermSetsFromQuantities(ProblemContent content) {
  final quantities =
      _mapAt(_mapAt(content.solvable['inputs'], 'quantities'), null);
  if (quantities.isEmpty) {
    return const [];
  }
  final firstAddend = _readInt(quantities['first_addend']);
  final secondAddend = _readInt(quantities['second_addend']);
  if (firstAddend != null && secondAddend != null) {
    return [
      [firstAddend, secondAddend],
    ];
  }

  final entries = quantities.entries
      .where((entry) => entry.value is Map)
      .map((entry) => MapEntry(entry.key.toString(), entry.value as Map))
      .toList()
    ..sort((a, b) => a.key.toString().compareTo(b.key.toString()));
  final selectedEntries = _selectAdditionEntriesForContent(content, entries);
  final sets = <List<int>>[];
  for (final entry in entries) {
    if (!selectedEntries.any((selected) => selected.key == entry.key)) {
      continue;
    }
    final value = entry.value;
    final first = _readInt(value['first_addend']);
    final second = _readInt(value['second_addend']);
    if (first != null && second != null) {
      sets.add([first, second]);
      continue;
    }
    final addends = value['addends'];
    if (addends is List) {
      final terms = addends
          .map((item) => _readInt(item))
          .whereType<int>()
          .take(2)
          .toList();
      if (terms.length >= 2) {
        sets.add(terms);
      }
    }
  }
  return sets;
}

List<List<int>> _additionTermSetsFromSteps(ProblemContent content) {
  final steps = content.solvable['steps'];
  if (steps is! List) {
    return const [];
  }
  final suffixNumber = _subproblemNumberFromProblemId(content.summary.id);
  final rawSteps = steps.whereType<Map>().where((step) {
    if (suffixNumber == null) {
      return true;
    }
    final id = step['id']?.toString() ?? '';
    return id.contains('problem_$suffixNumber');
  }).toList();
  final selectedSteps = suffixNumber == null && _answerKeyCount(content) > 0
      ? rawSteps.take(_answerKeyCount(content)).toList()
      : rawSteps;
  final sets = <List<int>>[];
  for (final step in selectedSteps) {
    final match = RegExp(r'(\d+)\s*\+\s*(\d+)')
        .firstMatch(step['expr']?.toString() ?? '');
    if (match == null) {
      continue;
    }
    sets.add([int.parse(match.group(1)!), int.parse(match.group(2)!)]);
  }
  return sets;
}

List<MapEntry<String, Map<dynamic, dynamic>>> _selectAdditionEntriesForContent(
  ProblemContent content,
  List<MapEntry<String, Map<dynamic, dynamic>>> entries,
) {
  final suffixNumber = _subproblemNumberFromProblemId(content.summary.id);
  if (suffixNumber != null) {
    final suffixKey = 'problem_$suffixNumber';
    final selected = entries.where((entry) => entry.key == suffixKey).toList();
    if (selected.isNotEmpty) {
      return selected;
    }
  }
  final answerCount = _answerKeyCount(content);
  if (answerCount > 0 && answerCount < entries.length) {
    return entries.take(answerCount).toList();
  }
  return entries;
}

List<int> _additionTerms(ProblemContent content) {
  final pieces = <String>[
    content.prompt,
    _readText(content.solvable['steps']),
    _readText(content.solvable['plan']),
    _readText(content.solvable['explanation']),
  ].join(' ');
  final match = RegExp(r'(\d+)\s*\+\s*(\d+)').firstMatch(pieces);
  if (match != null) {
    return [
      int.parse(match.group(1)!),
      int.parse(match.group(2)!),
    ];
  }

  final numbers = RegExp(r'\d+')
      .allMatches(pieces)
      .map((match) => int.tryParse(match.group(0) ?? ''))
      .whereType<int>()
      .where((number) => number >= 10)
      .toList();
  if (numbers.length >= 2) {
    return numbers.take(2).toList();
  }
  return const [];
}

String _withoutAnswer(ProblemContent content, String text) {
  final answer = content.correctAnswer.trim();
  if (answer.isEmpty) {
    return text;
  }
  return text.replaceAll(answer, '□');
}

String _extractChoiceLabel(Object? value) {
  if (value is String) {
    // Handle Python dict string format: "{'id': 'choice.1', 'label': 'VALUE', 'text': 'VALUE'}"
    final labelMatch = RegExp(
      r"""['"]?label['"]?\s*:\s*['"](.+?)['"]""",
    ).firstMatch(value);
    if (labelMatch != null) {
      final label = labelMatch.group(1)!.trim();
      // Skip generic placeholder values
      if (label.isNotEmpty && label != 'choices' && label != 'label' && label != 'choice') {
        return label;
      }
      // Try 'text' key as fallback
      final textMatch = RegExp(
        r"""['"]?text['"]?\s*:\s*['"](.+?)['"]""",
      ).firstMatch(value);
      if (textMatch != null) {
        final text = textMatch.group(1)!.trim();
        if (text.isNotEmpty && text != 'choices' && text != 'text' && text != 'choice') {
          return text;
        }
      }
      return '';
    }
  }
  return _readText(value);
}

String _readText(Object? value, {String fallback = ''}) {
  final text = _readTextParts(value).join(', ').trim();
  return text.isEmpty ? fallback : text;
}

List<String> _readTextParts(Object? value) {
  if (value == null) {
    return const [];
  }
  if (value is String || value is num || value is bool) {
    final text = sanitizeProblemText(value.toString()).trim();
    return text.isEmpty ? const [] : [text];
  }
  if (value is List) {
    return value.expand(_readTextParts).toList();
  }
  if (value is Map) {
    const preferredKeys = [
      'text',
      'description',
      'explanation',
      'expr',
      'label',
      'name',
      'value',
    ];
    final parts = <String>[];
    for (final key in preferredKeys) {
      if (value.containsKey(key)) {
        parts.addAll(_readTextParts(value[key]));
      }
    }
    if (parts.isNotEmpty) {
      return parts;
    }
    return value.values.expand(_readTextParts).toList();
  }
  return const [];
}

Map<String, dynamic> _mapAt(Object? value, Object? key) {
  final target = key == null
      ? value
      : value is Map
          ? value[key]
          : null;
  if (target is Map<String, dynamic>) {
    return target;
  }
  if (target is Map) {
    return target.map((key, value) => MapEntry(key.toString(), value));
  }
  return const {};
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  if (value is num) {
    return value.round();
  }
  return int.tryParse(value?.toString() ?? '');
}
