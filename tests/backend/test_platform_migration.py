import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


@pytest.mark.django_db(transaction=True)
def test_additive_migration_preserves_legacy_attempts_and_mastery():
    """Run on the isolated test DB, never on the user's development database."""
    before = [("learning", "0003_problem_catalog_data")]
    after = [("learning", "0004_learning_platform")]
    executor = MigrationExecutor(connection)
    latest = executor.loader.graph.leaf_nodes()
    executor.migrate(before)
    try:
        apps = executor.loader.project_state(before).apps
        user = apps.get_model("auth", "User").objects.create(username="legacy")
        problem = apps.get_model("learning", "Problem").objects.create(
            problem_id="legacy", answer={"value": 7}
        )
        attempt = apps.get_model("learning", "Attempt").objects.create(
            user_id=user.pk, problem_id=problem.pk, submitted_answer=7, is_correct=True
        )
        mastery = apps.get_model("learning", "Mastery").objects.create(
            user_id=user.pk, concept="legacy", attempt_count=1, correct_count=1, score=1
        )
        executor = MigrationExecutor(connection)
        executor.migrate(after)
        apps = executor.loader.project_state(after).apps
        migrated = apps.get_model("learning", "Attempt").objects.get(pk=attempt.pk)
        assert migrated.is_correct and migrated.submitted_answer == 7
        assert migrated.recipient_id is None and migrated.assignment_item_id is None
        stored = apps.get_model("learning", "Mastery").objects.get(pk=mastery.pk)
        assert (stored.attempt_count, stored.correct_count, stored.score) == (1, 1, 1)
    finally:
        MigrationExecutor(connection).migrate(latest)
