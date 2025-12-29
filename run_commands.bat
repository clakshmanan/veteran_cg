@echo off
REM ICGVWA Management Command Runner for Windows
REM This batch file helps run Django management commands easily

setlocal enabledelayedexpansion

echo ========================================
echo ICGVWA Management Command Runner
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ERROR: manage.py not found in current directory
    echo Please run this script from the Django project root directory
    pause
    exit /b 1
)

REM Show menu if no arguments provided
if "%1"=="" goto :show_menu

REM Handle command line arguments
set COMMAND=%1
shift

if /i "%COMMAND%"=="setup" goto :fresh_install
if /i "%COMMAND%"=="deploy" goto :production_deployment
if /i "%COMMAND%"=="test" goto :setup_test_environment
if /i "%COMMAND%"=="reset" goto :reset_test_data
if /i "%COMMAND%"=="backup" goto :backup_database
if /i "%COMMAND%"=="migrate" goto :migrate_database
if /i "%COMMAND%"=="collect" goto :collect_static
if /i "%COMMAND%"=="seed" goto :seed_data
if /i "%COMMAND%"=="users" goto :create_users
if /i "%COMMAND%"=="accounts" goto :create_accounts_user
if /i "%COMMAND%"=="clear" goto :clear_data
if /i "%COMMAND%"=="fix" goto :fix_permissions
if /i "%COMMAND%"=="rbac" goto :init_rbac
if /i "%COMMAND%"=="help" goto :show_help

echo ERROR: Unknown command '%COMMAND%'
echo Use 'run_commands.bat help' to see available commands
pause
exit /b 1

:show_menu
echo Select an option:
echo.
echo === SETUP COMMANDS ===
echo 1. Fresh Install (Complete setup for new deployment)
echo 2. Production Deployment (Update existing deployment)
echo 3. Setup Test Environment (Development with sample data)
echo.
echo === DATA COMMANDS ===
echo 4. Migrate Database
echo 5. Collect Static Files
echo 6. Seed Master Data
echo 7. Create Users
echo 8. Create Accounts User
echo.
echo === MAINTENANCE COMMANDS ===
echo 9. Clear All Data (DANGEROUS)
echo 10. Fix State Permissions
echo 11. Initialize RBAC
echo 12. Generate Association Numbers
echo.
echo === BACKUP COMMANDS ===
echo 13. Backup Database
echo.
echo 0. Exit
echo.
set /p choice="Enter your choice (0-13): "

if "%choice%"=="0" exit /b 0
if "%choice%"=="1" goto :fresh_install
if "%choice%"=="2" goto :production_deployment
if "%choice%"=="3" goto :setup_test_environment
if "%choice%"=="4" goto :migrate_database
if "%choice%"=="5" goto :collect_static
if "%choice%"=="6" goto :seed_data
if "%choice%"=="7" goto :create_users
if "%choice%"=="8" goto :create_accounts_user
if "%choice%"=="9" goto :clear_data
if "%choice%"=="10" goto :fix_permissions
if "%choice%"=="11" goto :init_rbac
if "%choice%"=="12" goto :generate_association_numbers
if "%choice%"=="13" goto :backup_database

echo Invalid choice. Please try again.
pause
goto :show_menu

:fresh_install
echo.
echo === FRESH INSTALL SETUP ===
echo This will set up the system from scratch
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto :show_menu

echo [1/8] Running database migrations...
python manage.py migrate
if errorlevel 1 goto :error

echo [2/8] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 goto :error

echo [3/8] Loading initial data...
python manage.py load_initial_data
if errorlevel 1 goto :error

echo [4/8] Seeding master data...
python manage.py seed_data
if errorlevel 1 goto :error

echo [5/8] Creating accounts user...
python manage.py create_accounts_user
if errorlevel 1 goto :error

echo [6/8] Initializing RBAC...
python manage.py init_rbac
if errorlevel 1 goto :error

echo [7/8] Setting up state admin permissions...
python manage.py setup_state_admin_permissions
if errorlevel 1 goto :error

echo [8/8] Creating superuser...
echo Please create a superuser account:
python manage.py createsuperuser

echo.
echo === FRESH INSTALL COMPLETED SUCCESSFULLY ===
echo.
echo Next steps:
echo 1. Access the application at http://127.0.0.1:8000/
echo 2. Login with your superuser credentials
echo 3. Create state admin users if needed
echo.
pause
goto :show_menu

:production_deployment
echo.
echo === PRODUCTION DEPLOYMENT ===
echo This will update an existing deployment
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto :show_menu

echo [1/4] Running database migrations...
python manage.py migrate
if errorlevel 1 goto :error

echo [2/4] Collecting static files...
python manage.py collectstatic --noinput --clear
if errorlevel 1 goto :error

echo [3/4] Loading initial data...
python manage.py load_initial_data
if errorlevel 1 goto :error

echo [4/4] Generating association numbers...
python manage.py generate_association_numbers
if errorlevel 1 goto :error

echo.
echo === PRODUCTION DEPLOYMENT COMPLETED ===
pause
goto :show_menu

:setup_test_environment
echo.
echo === SETUP TEST ENVIRONMENT ===
echo This will create a complete test environment with sample data
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto :show_menu

echo [1/6] Running database migrations...
python manage.py migrate
if errorlevel 1 goto :error

echo [2/6] Loading initial data...
python manage.py load_initial_data
if errorlevel 1 goto :error

echo [3/6] Seeding master data...
python manage.py seed_data
if errorlevel 1 goto :error

echo [4/6] Creating state users...
python manage.py seed_state_users
if errorlevel 1 goto :error

echo [5/6] Creating sample members...
python manage.py seed_members
if errorlevel 1 goto :error

echo [6/6] Creating accounts user...
python manage.py create_accounts_user
if errorlevel 1 goto :error

echo.
echo === TEST ENVIRONMENT SETUP COMPLETED ===
echo.
echo Test credentials:
echo - Superuser: Create manually using 'python manage.py createsuperuser'
echo - State users: state_AP, state_TN, etc. (password: state123)
echo - Accounts user: accounts (password: accounts123)
echo.
pause
goto :show_menu

:reset_test_data
echo.
echo === RESET TEST DATA ===
echo WARNING: This will DELETE ALL DATA and reload test data
echo.
set /p confirm="Are you sure? This is DANGEROUS! (yes/no): "
if /i not "%confirm%"=="yes" goto :show_menu

echo [1/4] Clearing all data...
python manage.py clear_data
if errorlevel 1 goto :error

echo [2/4] Running migrations...
python manage.py migrate
if errorlevel 1 goto :error

echo [3/4] Seeding master data...
python manage.py seed_data
if errorlevel 1 goto :error

echo [4/4] Creating sample members...
python manage.py seed_members
if errorlevel 1 goto :error

echo.
echo === TEST DATA RESET COMPLETED ===
pause
goto :show_menu

:migrate_database
echo.
echo === MIGRATE DATABASE ===
python manage.py migrate
if errorlevel 1 goto :error
echo Database migration completed successfully.
pause
goto :show_menu

:collect_static
echo.
echo === COLLECT STATIC FILES ===
python manage.py collectstatic --noinput
if errorlevel 1 goto :error
echo Static files collected successfully.
pause
goto :show_menu

:seed_data
echo.
echo === SEED MASTER DATA ===
python manage.py seed_data
if errorlevel 1 goto :error
echo Master data seeded successfully.
pause
goto :show_menu

:create_users
echo.
echo === CREATE SYSTEM USERS ===
python manage.py create_users
if errorlevel 1 goto :error
echo System users created successfully.
pause
goto :show_menu

:create_accounts_user
echo.
echo === CREATE ACCOUNTS USER ===
python manage.py create_accounts_user
if errorlevel 1 goto :error
echo Accounts user created successfully.
echo Username: accounts
echo Password: accounts123
pause
goto :show_menu

:clear_data
echo.
echo === CLEAR ALL DATA ===
echo WARNING: This will DELETE ALL DATA from the database
echo.
set /p confirm="Are you absolutely sure? (yes/no): "
if /i not "%confirm%"=="yes" goto :show_menu

python manage.py clear_data
if errorlevel 1 goto :error
echo All data cleared successfully.
pause
goto :show_menu

:fix_permissions
echo.
echo === FIX STATE PERMISSIONS ===
python manage.py fix_state_permissions
if errorlevel 1 goto :error
echo State permissions fixed successfully.
pause
goto :show_menu

:init_rbac
echo.
echo === INITIALIZE RBAC ===
python manage.py init_rbac
if errorlevel 1 goto :error
echo RBAC system initialized successfully.
pause
goto :show_menu

:generate_association_numbers
echo.
echo === GENERATE ASSOCIATION NUMBERS ===
python manage.py generate_association_numbers
if errorlevel 1 goto :error
echo Association numbers generated successfully.
pause
goto :show_menu

:backup_database
echo.
echo === BACKUP DATABASE ===
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
set backup_file=backup_%timestamp%.json

echo Creating backup: %backup_file%
python manage.py dumpdata --natural-foreign --natural-primary > %backup_file%
if errorlevel 1 goto :error

echo Database backup created successfully: %backup_file%
pause
goto :show_menu

:show_help
echo.
echo === ICGVWA MANAGEMENT COMMANDS HELP ===
echo.
echo Usage: run_commands.bat [command]
echo.
echo Available commands:
echo   setup     - Fresh install (complete setup)
echo   deploy    - Production deployment
echo   test      - Setup test environment
echo   reset     - Reset test data (DANGEROUS)
echo   backup    - Backup database
echo   migrate   - Run database migrations
echo   collect   - Collect static files
echo   seed      - Seed master data
echo   users     - Create system users
echo   accounts  - Create accounts user
echo   clear     - Clear all data (DANGEROUS)
echo   fix       - Fix state permissions
echo   rbac      - Initialize RBAC
echo   help      - Show this help
echo.
echo Examples:
echo   run_commands.bat setup
echo   run_commands.bat deploy
echo   run_commands.bat backup
echo.
pause
goto :show_menu

:error
echo.
echo === ERROR ===
echo Command failed with error code %errorlevel%
echo Please check the error messages above and try again.
echo.
pause
goto :show_menu

:end
echo.
echo Goodbye!
pause