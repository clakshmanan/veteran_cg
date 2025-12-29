#!/usr/bin/env bash
# Render Build Script

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=veteran_project.render_settings

echo "Running database migrations..."
python manage.py migrate --settings=veteran_project.render_settings

echo "Loading initial data..."
python manage.py load_initial_data --settings=veteran_project.render_settings

echo "Seeding master data..."
python manage.py seed_data --settings=veteran_project.render_settings

echo "creating state_users data...."
python manage.py seed_state_users --settings=veteran_project.render_settings

echo "Creating accounts user..."
python manage.py create_accounts_user --settings=veteran_project.render_settings

echo "setting up the state_admin_permissions permissions ..."
python manage.py setup_state_admin_permissions --settings=veteran_project.render_settings

echo "fixing the state_permissions ..."
python manage.py fix_state_permissions --settings=veteran_project.render_settings

echo "Initializing RBAC..."
python manage.py init_rbac --settings=veteran_project.render_settings

echo "Setting up state admin permissions..."
python manage.py setup_state_admin_permissions --settings=veteran_project.render_settings

echo "Build completed successfully!"
