import 'content_models.dart';

Map<String, dynamic> assignmentMap(dynamic value) =>
    value is Map ? Map<String, dynamic>.from(value) : {};

class AssignmentField {
  const AssignmentField(
      {required this.id, required this.type, this.choices = const []});
  final String id;
  final String type;
  final List<Map<String, dynamic>> choices;
  factory AssignmentField.fromJson(Map<String, dynamic> json) =>
      AssignmentField(
        id: '${json['id'] ?? 'answer'}',
        type: '${json['type'] ?? 'text'}',
        choices: (json['choices'] as List? ?? []).map(assignmentMap).toList(),
      );
}

class AssignmentItem {
  AssignmentItem.fromJson(Map<String, dynamic> json)
      : id = json['id'] as int,
        position = json['position'] as int? ?? 0,
        content = assignmentMap(json['content']),
        draft = json['draft_answer'],
        draftUpdatedAt = DateTime.tryParse('${json['draft_updated_at'] ?? ''}'),
        submittedAnswer = json['submitted_answer'],
        lastSubmittedAt =
            DateTime.tryParse('${json['last_submitted_at'] ?? ''}'),
        attemptCount = json['attempt_count'] as int? ?? 0,
        hintTotal = json['hint_total'] as int? ?? 0,
        hints =
            (json['revealed_hints'] as List? ?? []).map(assignmentMap).toList(),
        isCorrect = json['is_correct'] as bool?,
        answer = json['answer'],
        solution = assignmentMap(json['solution']);
  final int id;
  final int position;
  final Map<String, dynamic> content;
  final dynamic draft;
  final DateTime? draftUpdatedAt;
  final dynamic submittedAnswer;
  final DateTime? lastSubmittedAt;
  final int attemptCount;
  final int hintTotal;
  final List<Map<String, dynamic>> hints;
  final bool? isCorrect;
  final dynamic answer;
  final Map<String, dynamic> solution;
  String get prompt => '${content['prompt'] ?? ''}';
  String get unit => '${assignmentMap(content['input_schema'])['unit'] ?? ''}';
  List<AssignmentField> get fields {
    final values = assignmentMap(content['input_schema'])['fields'];
    if (values is List && values.isNotEmpty) {
      return values
          .map((v) => AssignmentField.fromJson(assignmentMap(v)))
          .toList();
    }
    return const [AssignmentField(id: 'answer', type: 'text')];
  }

  ProblemContent get problem => ProblemContent(
        summary: ProblemSummary.fromJson({
          'id': content['problem_id'] ?? '$id',
          'title': prompt,
          'language': content['language'] ?? 'ko',
          'type': content['problem_type'] ?? '',
        }),
        semantic: assignmentMap(content['semantic_data']),
        solvable: const {},
        renderer: assignmentMap(content['renderer_data']),
        layout: const {},
      );
}

class StudentAssignment {
  StudentAssignment.fromJson(Map<String, dynamic> json)
      : id = json['id'] as int,
        recipientId = json['recipient_id'] as int,
        title = '${json['title']}',
        status = '${json['status']}',
        startsAt = DateTime.tryParse('${json['starts_at'] ?? ''}'),
        dueAt = DateTime.tryParse('${json['due_at'] ?? ''}'),
        submittedAt = DateTime.tryParse('${json['submitted_at'] ?? ''}'),
        canWork = json['can_work'] == true,
        released = json['results_released'] == true,
        total = json['total'] as int? ?? 0,
        completed = json['completed'] as int? ?? 0,
        maxAttempts = json['max_attempts'] as int? ?? 1,
        correct = json['correct'] as int?,
        accuracy = (json['accuracy'] as num?)?.toDouble(),
        items = (json['items'] as List? ?? [])
            .map((v) => AssignmentItem.fromJson(assignmentMap(v)))
            .toList();
  final int id;
  final int recipientId;
  final String title;
  final String status;
  final DateTime? startsAt;
  final DateTime? dueAt;
  final DateTime? submittedAt;
  final bool canWork;
  final bool released;
  final int total;
  final int completed;
  final int maxAttempts;
  final int? correct;
  final double? accuracy;
  final List<AssignmentItem> items;
  double get progress => total == 0 ? 0 : completed / total;
}
