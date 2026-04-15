from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProblemRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("problem_id", models.CharField(max_length=120, unique=True)),
                ("title", models.CharField(blank=True, default="", max_length=255)),
                ("semantic_path", models.CharField(blank=True, default="", max_length=500)),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("in_review", "In Review"), ("done", "Done")],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

