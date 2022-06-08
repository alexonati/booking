import json
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Update fixture entry to current custom Auth Model.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Old structure backup file.')

    def handle(self, *args, **options):
        file = options.get('file')

        if not file:
            raise CommandError('File parameter not specified.')

        try:
            with open(file) as json_file:
                backup_data = json.load(json_file)

            # output = []
            for model_data in backup_data:
                if model_data.get('model') == 'auth.user':
                    model_data['model'] = 'users.authuser'
                    if 'fields' in model_data and 'username' in model_data['fields']:
                        del model_data['fields']['username']

                # output.append(model_data)

            with open(file, 'w') as json_file:
                json.dump(backup_data, json_file, indent=2)
        except Exception as e:
            raise CommandError('Something went wrong.', e)
