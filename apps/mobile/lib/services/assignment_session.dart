import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';

import '../models/assignment.dart';
import 'student_assignment_service.dart';

/// Assignment-only state. Never invokes local grading or the practice queue.
class AssignmentSession extends ChangeNotifier {
  AssignmentSession({required this.service, required this.assignmentId})
      : _account = service.account;
  final StudentAssignmentService service;
  final int assignmentId;
  final String _account;
  StudentAssignment? assignment;
  int index = 0;
  bool loading = true;
  bool busy = false;
  Object? error;
  bool _disposed = false;
  final answers = <int, dynamic>{};
  final pending = <int>{};
  final retrying = <int>{};
  final _counts = <int, int>{};
  final feedback = <int, bool?>{};
  final hintLists = <int, List<Map<String, dynamic>>>{};
  final draftStatus = <int, String>{};
  final _dirty = <int>{};
  final _drafting = <int>{};
  final _elapsed = <int, int>{};
  final Stopwatch _watch = Stopwatch();
  Timer? _timer;
  Future<void> _localWrites = Future.value();
  Future<void> _remoteWrites = Future.value();
  bool get _active => !_disposed && service.account == _account;
  AssignmentItem? get item => assignment != null && assignment!.items.isNotEmpty
      ? assignment!.items[index]
      : null;
  int count(AssignmentItem item) => _counts[item.id] ?? item.attemptCount;
  int get completed =>
      assignment?.items.where((item) => count(item) > 0).length ?? 0;
  bool get canEdit =>
      !busy &&
      assignment?.canWork == true &&
      item != null &&
      !pending.contains(item!.id) &&
      (count(item!) == 0 || retrying.contains(item!.id)) &&
      count(item!) < assignment!.maxAttempts;
  bool get canSend =>
      !busy &&
      item != null &&
      (pending.contains(item!.id) || canEdit) &&
      complete(answers[item!.id], item!.fields.length);
  bool get canSubmit =>
      !busy &&
      assignment?.canWork == true &&
      completed == assignment!.total &&
      pending.isEmpty;
  static bool complete(dynamic answer, int fields) {
    if (fields == 1 && answer is List) {
      return answer.isNotEmpty && answer.every((v) => v != null);
    }
    final values = fields > 1 && answer is List ? answer : [answer];
    return values.length == fields &&
        values.every((v) => v != null && (v is! String || v.trim().isNotEmpty));
  }

  void _notify() {
    if (_active) notifyListeners();
  }

  int get elapsedMs => (_elapsed[item?.id] ?? 0) + _watch.elapsedMilliseconds;

  Future<void> load() async {
    loading = true;
    error = null;
    _watch.stop();
    _notify();
    try {
      final loaded = await service.detail(assignmentId);
      if (!_active) return;
      assignment = loaded;
      index =
          loaded.items.isEmpty ? 0 : index.clamp(0, loaded.items.length - 1);
      pending.clear();
      _counts.clear();
      feedback.clear();
      retrying.clear();
      _dirty.clear();
      _drafting.clear();
      for (final item in loaded.items) {
        var answer = item.draft ?? item.submittedAnswer;
        final local = await service.local(assignmentId, item.id, 'draft');
        final request = await service.pending(assignmentId, item.id);
        if (!_active) return;
        final localTime = DateTime.tryParse('${local?['updated_at'] ?? ''}');
        final remoteTimes = [item.draftUpdatedAt, item.lastSubmittedAt]
            .whereType<DateTime>()
            .toList()
          ..sort();
        if (loaded.canWork &&
            localTime != null &&
            (remoteTimes.isEmpty || localTime.isAfter(remoteTimes.last)) &&
            count(item) < loaded.maxAttempts) {
          answer = local!['answer'];
          draftStatus[item.id] = 'localSaved';
          _dirty.add(item.id);
          if (item.attemptCount > 0) retrying.add(item.id);
        }
        if (request != null) {
          answer = request['answer'];
          pending.add(item.id);
        }
        answers[item.id] = answer;
        if (loaded.canWork &&
            answer != null &&
            (item.attemptCount == 0 || retrying.contains(item.id))) {
          _drafting.add(item.id);
        }
        if (localTime != null &&
            (item.lastSubmittedAt == null ||
                localTime.isAfter(item.lastSubmittedAt!))) {
          _elapsed[item.id] = local?['elapsed_ms'] as int? ?? 0;
        }
        hintLists[item.id] = List.of(item.hints);
      }
    } catch (e) {
      if (_active) error = e;
    } finally {
      if (_active) {
        loading = false;
        _watch.reset();
        _watch.start();
        _notify();
      }
    }
  }

  void change(dynamic value) {
    if (!canEdit) return;
    final id = item!.id;
    answers[id] = value;
    _dirty.add(id);
    _drafting.add(id);
    draftStatus[id] = 'saving';
    error = null;
    final captured = jsonDecode(jsonEncode(value));
    final duration = elapsedMs;
    _localWrites = _localWrites.then((_) async {
      if (!_active) return;
      try {
        await service.persistDraft(assignmentId, id, captured,
            elapsedMs: duration);
      } catch (e) {
        error = e;
        _notify();
      }
    });
    _timer?.cancel();
    _timer = Timer(const Duration(milliseconds: 650), () {
      unawaited(_save(id, captured));
    });
    _notify();
  }

  Future<void> _save(int id, dynamic value) {
    _remoteWrites = _remoteWrites.then((_) async {
      await _localWrites;
      if (!_active) return;
      try {
        final synced = await service.saveDraft(assignmentId, id, value);
        if (_active && jsonEncode(answers[id]) == jsonEncode(value)) {
          draftStatus[id] = synced ? 'serverSaved' : 'localSaved';
          if (synced) _dirty.remove(id);
        }
      } catch (e) {
        if (_active) {
          error = e;
          draftStatus[id] = 'saveRejected';
        }
      }
      _notify();
    });
    return _remoteWrites;
  }

  Future<void> flush() async {
    _timer?.cancel();
    await _localWrites;
    final current = item;
    if (_active && current != null && _drafting.contains(current.id)) {
      try {
        await service.persistDraft(
            assignmentId, current.id, answers[current.id],
            elapsedMs: elapsedMs);
      } catch (e) {
        error = e;
        _notify();
      }
    }
    if (current != null && _dirty.contains(current.id)) {
      await _save(current.id, jsonDecode(jsonEncode(answers[current.id])));
    } else {
      await _remoteWrites;
    }
  }

  Future<void> move(int next) async {
    if (busy ||
        assignment == null ||
        next < 0 ||
        next >= assignment!.items.length) {
      return;
    }
    busy = true;
    _notify();
    await flush();
    if (!_active) return;
    if (item != null) _elapsed[item!.id] = elapsedMs;
    index = next;
    _watch.reset();
    _watch.start();
    busy = false;
    error = null;
    _notify();
  }

  void retry() {
    if (busy ||
        item == null ||
        assignment?.canWork != true ||
        count(item!) >= assignment!.maxAttempts) {
      return;
    }
    retrying.add(item!.id);
    _elapsed[item!.id] = 0;
    feedback.remove(item!.id);
    _watch.reset();
    _watch.start();
    _notify();
  }

  Future<void> send() async {
    if (!canSend) return;
    final current = item!;
    final value = jsonDecode(jsonEncode(answers[current.id]));
    final duration = elapsedMs;
    busy = true;
    error = null;
    _notify();
    await flush();
    try {
      if (!_active) return;
      final response =
          await service.submitAnswer(assignmentId, current.id, value, duration);
      if (!_active) return;
      pending.remove(current.id);
      error = null;
      retrying.remove(current.id);
      _dirty.remove(current.id);
      _drafting.remove(current.id);
      _counts[current.id] = response['attempt_number'] as int;
      feedback[current.id] = response['is_correct'] as bool?;
      _elapsed[current.id] = 0;
      _watch.reset();
      try {
        assignment = await service.detail(assignmentId);
      } catch (e) {
        error = e;
      }
    } catch (e) {
      if (!_active) return;
      error = e;
      if (await service.pending(assignmentId, current.id) != null) {
        pending.add(current.id);
      } else {
        pending.remove(current.id);
        try {
          assignment = await service.detail(assignmentId);
        } catch (_) {}
      }
    } finally {
      if (_active) {
        busy = false;
        _notify();
      }
    }
  }

  Future<void> nextHint() async {
    if (busy || item == null || assignment?.canWork != true) return;
    final current = item!;
    final hints = hintLists[current.id] ?? [];
    if (hints.length >= current.hintTotal) return;
    busy = true;
    error = null;
    _notify();
    try {
      final response =
          await service.hint(assignmentId, current.id, hints.length + 1);
      if (_active) {
        hintLists[current.id] = [...hints, assignmentMap(response['hint'])];
      }
    } catch (e) {
      if (_active) error = e;
    } finally {
      if (_active) {
        busy = false;
        _notify();
      }
    }
  }

  Future<void> finish() async {
    if (!canSubmit) return;
    busy = true;
    error = null;
    _notify();
    await flush();
    try {
      if (_active) assignment = await service.submit(assignmentId);
    } catch (e) {
      if (_active) error = e;
    } finally {
      if (_active) {
        busy = false;
        _watch.stop();
        _notify();
      }
    }
  }

  void pause() => _watch.stop();
  void resume() {
    if (_active && assignment?.canWork == true) _watch.start();
  }

  @override
  void dispose() {
    _timer?.cancel();
    _watch.stop();
    _disposed = true;
    super.dispose();
  }
}
