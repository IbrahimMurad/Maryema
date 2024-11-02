from django.contrib.auth.management.commands.createsuperuser import (
    Command as CreateSuperUserCommand,
)
from django.core.management import CommandError
from django.utils.translation import gettext as _


class Command(CreateSuperUserCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--email",
            dest="email",
            required=True,
            help=_("Specifies the email for the superuser."),
        )

    def handle(self, *args, **options):
        email = options.get("email")
        if not email:
            raise CommandError("You must provide an email address.")
        super().handle(*args, **options)
