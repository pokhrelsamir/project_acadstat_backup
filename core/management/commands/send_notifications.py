from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send automated notifications to students needing attention (disabled)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--threshold',
            type=float,
            default=60,
            help='Percentage threshold (default: 60)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show who would be notified without sending',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Automated notification service is not available.'))
        self.stdout.write(self.style.NOTICE('  OpenRouter integration was removed from this project.'))
