from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Grant/revoke the teacher role. Requires trusted server access; never grants staff rights."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--revoke", action="store_true")

    def handle(self, *args, **options):
        user = (
            get_user_model()
            .objects.filter(username=options["username"], is_active=True)
            .first()
        )
        if user is None:
            raise CommandError("Active user not found")
        group, _ = Group.objects.get_or_create(name="modu_teachers")
        if options["revoke"]:
            user.groups.remove(group)
        else:
            user.groups.add(group)
        self.stdout.write(self.style.SUCCESS("Teacher role updated"))
