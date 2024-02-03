from django.core.management.base import BaseCommand
from news.models import Category


class Command(BaseCommand):
    help = 'Delete all posts in current category'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        try:
            category = Category.objects.get(name=options['category'])
            self.stdout.write(f'Do you really want to delete all posts in {options["category"]}? yes/no')
            answer = input()
            if answer == 'yes':
                posts = category.post_set.all()
                posts.delete()
                self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))
