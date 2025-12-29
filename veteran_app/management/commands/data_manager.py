from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from veteran_app.models import *
from datetime import datetime, date
import csv

class Command(BaseCommand):
    help = 'Comprehensive data management operations'

    def add_arguments(self, parser):
        parser.add_argument('--action', type=str, required=True, 
                          choices=['create', 'update', 'delete', 'bulk_update', 'stats', 'export'],
                          help='Action to perform')
        parser.add_argument('--model', type=str, help='Model name (VeteranMember, User, State)')
        parser.add_argument('--id', type=int, help='Record ID')
        parser.add_argument('--field', type=str, help='Field to update')
        parser.add_argument('--value', type=str, help='New value')
        parser.add_argument('--filter', type=str, help='Filter criteria (e.g., state_code=AP)')
        parser.add_argument('--file', type=str, help='CSV file path for bulk operations')

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'create':
            self.create_record(options)
        elif action == 'update':
            self.update_record(options)
        elif action == 'delete':
            self.delete_record(options)
        elif action == 'bulk_update':
            self.bulk_update(options)
        elif action == 'stats':
            self.show_stats()
        elif action == 'export':
            self.export_data(options)

    def create_record(self, options):
        """Create new records"""
        if options['model'] == 'User':
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(f"Created user: {user.username}")
            
        elif options['model'] == 'VeteranMember':
            # Interactive veteran creation
            name = input("Name: ")
            state_code = input("State code: ")
            service_number = input("Service number: ")
            
            try:
                state = State.objects.get(code=state_code.upper())
                rank = Rank.objects.first()  # Default rank
                branch = Branch.objects.first()  # Default branch
                blood_group = BloodGroup.objects.first()  # Default blood group
                admin_user = User.objects.get(username='admin')
                
                veteran = VeteranMember.objects.create(
                    name=name,
                    state=state,
                    service_number=service_number,
                    rank=rank,
                    branch=branch,
                    blood_group=blood_group,
                    date_of_birth=date(1980, 1, 1),
                    contact='0000000000',
                    address='Address',
                    date_of_joining=date(2000, 1, 1),
                    retired_on=date(2020, 1, 1),
                    association_date=date.today(),
                    enrolled_date=date(2000, 1, 1),
                    spouse_name='Spouse Name',
                    created_by=admin_user
                )
                self.stdout.write(f"Created veteran: {veteran.name} (ID: {veteran.association_id})")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))

    def update_record(self, options):
        """Update existing records"""
        model_name = options['model']
        record_id = options['id']
        field = options['field']
        value = options['value']
        
        if model_name == 'VeteranMember':
            try:
                veteran = VeteranMember.objects.get(association_id=record_id)
                setattr(veteran, field, value)
                veteran.save()
                self.stdout.write(f"Updated {field} to {value} for veteran ID {record_id}")
            except VeteranMember.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Veteran with ID {record_id} not found"))
        
        elif model_name == 'User':
            try:
                user = User.objects.get(id=record_id)
                setattr(user, field, value)
                user.save()
                self.stdout.write(f"Updated {field} to {value} for user ID {record_id}")
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with ID {record_id} not found"))

    def delete_record(self, options):
        """Delete records"""
        model_name = options['model']
        record_id = options['id']
        
        if model_name == 'VeteranMember':
            try:
                veteran = VeteranMember.objects.get(association_id=record_id)
                name = veteran.name
                veteran.delete()
                self.stdout.write(f"Deleted veteran: {name} (ID: {record_id})")
            except VeteranMember.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Veteran with ID {record_id} not found"))

    def bulk_update(self, options):
        """Bulk update operations"""
        filter_criteria = options.get('filter', '')
        field = options['field']
        value = options['value']
        
        if filter_criteria:
            # Parse filter (e.g., "state_code=AP")
            key, val = filter_criteria.split('=')
            if key == 'state_code':
                queryset = VeteranMember.objects.filter(state__code=val)
            else:
                queryset = VeteranMember.objects.filter(**{key: val})
        else:
            queryset = VeteranMember.objects.all()
        
        count = queryset.update(**{field: value})
        self.stdout.write(f"Updated {count} records: {field} = {value}")

    def show_stats(self):
        """Show database statistics"""
        self.stdout.write("=== DATABASE STATISTICS ===")
        self.stdout.write(f"Total Veterans: {VeteranMember.objects.count()}")
        self.stdout.write(f"Total Users: {User.objects.count()}")
        self.stdout.write(f"Total States: {State.objects.count()}")
        self.stdout.write(f"Approved Veterans: {VeteranMember.objects.filter(approved=True).count()}")
        self.stdout.write(f"Active Members: {VeteranMember.objects.filter(membership=True).count()}")
        
        # State-wise breakdown
        self.stdout.write("\n=== STATE-WISE BREAKDOWN ===")
        for state in State.objects.all():
            count = VeteranMember.objects.filter(state=state).count()
            self.stdout.write(f"{state.name} ({state.code}): {count}")

    def export_data(self, options):
        """Export data to CSV"""
        filename = options.get('file', 'veterans_export.csv')
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow([
                'Association ID', 'Name', 'State', 'Service Number', 'Rank', 
                'Branch', 'Contact', 'Email', 'Approved', 'Membership'
            ])
            
            # Data
            for veteran in VeteranMember.objects.all():
                writer.writerow([
                    veteran.association_id,
                    veteran.name,
                    veteran.state.code,
                    veteran.service_number,
                    veteran.rank.name,
                    veteran.branch.name,
                    veteran.contact,
                    getattr(veteran, 'alternate_email', ''),
                    veteran.approved,
                    veteran.membership
                ])
        
        self.stdout.write(f"Exported data to {filename}")

# Usage Examples:
# python manage.py data_manager --action=stats
# python manage.py data_manager --action=create --model=User
# python manage.py data_manager --action=update --model=VeteranMember --id=1 --field=contact --value=9999999999
# python manage.py data_manager --action=bulk_update --filter=state_code=AP --field=approved --value=True
# python manage.py data_manager --action=export --file=veterans.csv