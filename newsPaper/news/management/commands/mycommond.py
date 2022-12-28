from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'                          # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True                         # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)   # Positional arguments

    def handle(self, *args, **options):
        category = Category.objects.get(name=options['category'])
        
        answer = input(f'Вы правда хотите удалить все статьи в категории{options["category"]}?yes/no\n')
        if answer == 'yes':
            self.stdout.write(str(options['category'])) # здесь можете писать любой код, который выполняется при вызове вашей команды
            
            try:
                Post.objects.filter(postCategory=category).delete()
                self.stdout.write(self.style.SUCCES(f'Все новости в категории {category.name} успешно удалены')) # в случае неправильного подтверждения говорим, что в доступе отказано
                
            except category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {options["category"]}'))
        else:
            self.stdout.write(self.style.ERROR(f'Удаление отменено'))
            