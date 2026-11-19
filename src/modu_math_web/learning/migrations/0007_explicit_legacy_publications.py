from django.db import migrations


def preserve_legacy_publications(apps, schema_editor):
    """Record the legacy public catalog before removing implicit public access."""
    Problem = apps.get_model("learning", "Problem")
    Publication = apps.get_model("learning", "ProblemPublication")
    alias = schema_editor.connection.alias
    problem_ids = (
        Problem.objects.using(alias)
        .filter(publication__isnull=True)
        .values_list("pk", flat=True)
    )
    Publication.objects.using(alias).bulk_create(
        [
            Publication(
                problem_id=pk,
                status="published",
                visibility="public",
                allow_classroom_use=True,
            )
            for pk in problem_ids
        ],
        batch_size=1000,
    )


class Migration(migrations.Migration):
    dependencies = [("learning", "0006_problem_visibility")]
    operations = [
        migrations.RunPython(preserve_legacy_publications, migrations.RunPython.noop)
    ]
