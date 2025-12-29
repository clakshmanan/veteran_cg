import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from veteran_app.models import VeteranMember, State, Rank, Group, BloodGroup
from datetime import datetime

class Command(BaseCommand):
    help = 'Import members from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        admin_user = User.objects.get(username='admin')
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            created_count = 0
            
            for row in reader:
                try:
                    state = State.objects.get(code=row['state_code'])
                    rank = Rank.objects.get(name=row['rank'])
                    group = Group.objects.get(name=row['group'])
                    blood_group = BloodGroup.objects.get(name=row['blood_group'])
                    
                    member, created = VeteranMember.objects.get_or_create(
                        p_number=row['p_number'],
                        defaults={
                            'association_id': row.get('association_id'),  # Add this line
                            'state': state,
                            'name': row['name'],
                            'rank': rank,
                            'group': group,
                            'date_of_birth': datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date(),
                            'blood_group': blood_group,
                            'contact': row['contact'],
                            'address': row['address'],
                            'date_of_joining': datetime.strptime(row['date_of_joining'], '%Y-%m-%d').date(),
                            'retired_on': datetime.strptime(row['retired_on'], '%Y-%m-%d').date(),
                            'association_date': datetime.strptime(row['association_date'], '%Y-%m-%d').date(),
                            'membership': row['membership'].lower() == 'true',
                            'created_by': admin_user,
                            'approved': True
                        }
                    )
                    
                    if created:
                        created_count += 1
                        
                except Exception as e:
                    self.stdout.write(f"Error importing {row.get('name', 'Unknown')}: {e}")
            
            self.stdout.write(f"Successfully imported {created_count} members")