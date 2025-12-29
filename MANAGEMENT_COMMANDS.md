# ICGVWA Management Commands

This directory contains tools to easily run Django management commands for the Indian Coast Guard Veteran Welfare Association (ICGVWA) system.

## 🚀 Quick Start

### Windows Users
```bash
# Run interactive menu
run_commands.bat

# Or run specific commands
run_commands.bat setup      # Fresh installation
run_commands.bat deploy     # Production deployment
run_commands.bat test       # Setup test environment
```

### Linux/Mac Users
```bash
# Install PyYAML if not already installed
pip install PyYAML

# Run interactive menu
python run_commands.py --list

# Run specific commands
python run_commands.py setup
python run_commands.py --order fresh_install
```

## 📋 Available Commands

### Setup Commands
- **setup/fresh_install** - Complete setup for new deployment
- **deploy/production_deployment** - Update existing deployment
- **test/setup_test_environment** - Development with sample data

### Data Management
- **migrate** - Run database migrations
- **collect** - Collect static files
- **seed** - Seed master data (states, ranks, branches)
- **users** - Create system users
- **accounts** - Create accounts/treasurer user

### Maintenance
- **clear** - Clear all data (DANGEROUS)
- **fix** - Fix state permissions
- **rbac** - Initialize Role-Based Access Control
- **backup** - Create database backup

## 🔧 Configuration Files

### management_commands.yml
Complete YAML configuration with all available commands, execution orders, and settings.

### run_commands.py
Python script that reads the YAML configuration and executes commands with proper logging and error handling.

### run_commands.bat
Windows batch script for easy command execution without needing to understand Python/YAML.

## 📖 Usage Examples

### Fresh Installation
```bash
# Windows
run_commands.bat setup

# Linux/Mac
python run_commands.py fresh_install
```

This will:
1. Run database migrations
2. Collect static files
3. Load initial data
4. Seed master data
5. Create accounts user
6. Initialize RBAC
7. Setup state admin permissions
8. Prompt to create superuser

### Production Deployment
```bash
# Windows
run_commands.bat deploy

# Linux/Mac
python run_commands.py production_deployment
```

This will:
1. Run database migrations
2. Collect static files (with --clear)
3. Load initial data
4. Generate association numbers

### Test Environment Setup
```bash
# Windows
run_commands.bat test

# Linux/Mac
python run_commands.py setup_test_environment
```

This will:
1. Run database migrations
2. Load initial data
3. Seed master data
4. Create state users
5. Create sample members
6. Create accounts user

## 🔐 Default Credentials

After running setup commands, these accounts will be available:

### State Admin Users
- **Username Pattern**: `state_{STATE_CODE}` (e.g., `state_AP`, `state_TN`)
- **Password**: `state123`
- **Access**: State-specific member management

### Accounts User
- **Username**: `accounts`
- **Password**: `accounts123`
- **Access**: Financial management and reports

### Superuser
- **Created manually** during setup process
- **Access**: Full system administration

## 🛡️ Security Features

### Dangerous Command Protection
Commands marked as dangerous (like `clear_data`) will:
- Show warning messages
- Require explicit confirmation
- Suggest creating backups first
- Log all actions

### Backup Recommendations
- Always backup before running dangerous commands
- Use `backup` command to create database snapshots
- Store backups in a secure location

## 📝 Logging

All command executions are logged to `management_commands.log` with:
- Timestamp
- Command executed
- Success/failure status
- Error messages (if any)

## 🔍 Troubleshooting

### Common Issues

1. **Python not found**
   - Install Python 3.8+
   - Add Python to system PATH

2. **manage.py not found**
   - Run commands from Django project root directory
   - Ensure you're in the correct folder

3. **Permission errors**
   - Run as administrator (Windows)
   - Use sudo if needed (Linux/Mac)

4. **Database errors**
   - Check database connection
   - Ensure database server is running
   - Verify database permissions

### Getting Help

```bash
# Windows
run_commands.bat help

# Linux/Mac
python run_commands.py --help
```

## 📁 File Structure

```
veteran_cg/
├── management_commands.yml     # YAML configuration
├── run_commands.py            # Python command runner
├── run_commands.bat           # Windows batch script
├── MANAGEMENT_COMMANDS.md     # This documentation
└── management_commands.log    # Execution log (created automatically)
```

## 🔄 Command Execution Order

Commands are executed in specific orders to ensure proper system setup:

### Fresh Install Order
1. migrate_database
2. collect_static
3. load_initial_data
4. create_superuser
5. seed_master_data
6. create_accounts_user
7. init_rbac
8. setup_state_admin_permissions

### Update Deployment Order
1. migrate_database
2. collect_static
3. generate_association_numbers
4. fix_state_permissions

## 💡 Tips

1. **Always test in development first** before running in production
2. **Create backups** before major operations
3. **Check logs** if commands fail
4. **Use aliases** for frequently used command sequences
5. **Run commands in order** for proper system setup

## 🆘 Support

If you encounter issues:
1. Check the log file for detailed error messages
2. Ensure all prerequisites are installed
3. Verify you're in the correct directory
4. Contact the system administrator for assistance

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Compatible with**: Django 5.2.6, Python 3.8+