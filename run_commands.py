#!/usr/bin/env python3
"""
ICGVWA Management Command Runner
Executes Django management commands based on YAML configuration
"""

import os
import sys
import yaml
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

class ManagementCommandRunner:
    def __init__(self, config_file='management_commands.yml'):
        self.config_file = config_file
        self.config = self.load_config()
        self.log_file = self.config.get('logging', {}).get('log_file', 'management_commands.log')
        
    def load_config(self):
        """Load YAML configuration file"""
        try:
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_file}' not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)
    
    def log_message(self, message, level='INFO'):
        """Log message to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {message}"
        
        # Print to console
        print(log_entry)
        
        # Write to log file if logging is enabled
        if self.config.get('logging', {}).get('enabled', True):
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry + '\n')
            except Exception as e:
                print(f"Warning: Could not write to log file: {e}")
    
    def execute_command(self, command, description=None):
        """Execute a single command"""
        if description:
            self.log_message(f"Executing: {description}")
        
        self.log_message(f"Command: {command}")
        
        try:
            # Execute command and capture output
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                self.log_message(f"SUCCESS: Command completed successfully")
                if result.stdout:
                    self.log_message(f"Output: {result.stdout.strip()}")
                return True
            else:
                self.log_message(f"ERROR: Command failed with return code {result.returncode}", 'ERROR')
                if result.stderr:
                    self.log_message(f"Error output: {result.stderr.strip()}", 'ERROR')
                return False
                
        except Exception as e:
            self.log_message(f"EXCEPTION: {str(e)}", 'ERROR')
            return False
    
    def confirm_dangerous_command(self, command_name):
        """Ask for confirmation before executing dangerous commands"""
        dangerous_commands = self.config.get('security', {}).get('dangerous_commands', [])
        
        if command_name in dangerous_commands:
            self.log_message(f"WARNING: '{command_name}' is marked as a dangerous command", 'WARNING')
            
            if self.config.get('security', {}).get('confirmation_required', True):
                response = input(f"Are you sure you want to execute '{command_name}'? (yes/no): ")
                if response.lower() not in ['yes', 'y']:
                    self.log_message("Command execution cancelled by user")
                    return False
                    
            # Suggest backup before dangerous operations
            if self.config.get('security', {}).get('backup_before_dangerous', True):
                backup_response = input("Do you want to create a backup first? (yes/no): ")
                if backup_response.lower() in ['yes', 'y']:
                    self.execute_backup()
        
        return True
    
    def execute_backup(self):
        """Execute database backup"""
        backup_commands = self.config.get('backup_commands', [])
        for cmd_config in backup_commands:
            if cmd_config.get('name') == 'backup_database':
                self.execute_command(cmd_config['command'], cmd_config['description'])
                break
    
    def run_single_command(self, command_name):
        """Run a single command by name"""
        # Search in all command categories
        all_commands = {}
        
        # Collect all commands from different categories
        for category in ['setup_commands', 'data_commands', 'user_commands', 'maintenance_commands', 'rbac_commands']:
            commands = self.config.get(category, [])
            for cmd in commands:
                all_commands[cmd['name']] = cmd
        
        # Check one-time commands
        one_time_commands = self.config.get('one_time_commands', [])
        for cmd in one_time_commands:
            all_commands[cmd['name']] = cmd
        
        if command_name not in all_commands:
            self.log_message(f"ERROR: Command '{command_name}' not found", 'ERROR')
            return False
        
        cmd_config = all_commands[command_name]
        
        # Check if it's a dangerous command
        if not self.confirm_dangerous_command(command_name):
            return False
        
        # Execute single command or sequence
        if 'command' in cmd_config:
            return self.execute_command(cmd_config['command'], cmd_config.get('description'))
        elif 'commands' in cmd_config:
            return self.run_command_sequence(cmd_config['commands'], cmd_config.get('description'))
        
        return False
    
    def run_command_sequence(self, commands, description=None):
        """Run a sequence of commands"""
        if description:
            self.log_message(f"Starting sequence: {description}")
        
        success_count = 0
        total_count = len(commands)
        
        for command in commands:
            if self.execute_command(command):
                success_count += 1
            else:
                self.log_message(f"Sequence failed at command: {command}", 'ERROR')
                break
        
        if success_count == total_count:
            self.log_message(f"Sequence completed successfully ({success_count}/{total_count})")
            return True
        else:
            self.log_message(f"Sequence failed ({success_count}/{total_count})", 'ERROR')
            return False
    
    def run_execution_order(self, order_name):
        """Run commands in a predefined execution order"""
        execution_orders = self.config.get('execution_order', {})
        
        if order_name not in execution_orders:
            self.log_message(f"ERROR: Execution order '{order_name}' not found", 'ERROR')
            return False
        
        commands = execution_orders[order_name]
        self.log_message(f"Starting execution order: {order_name}")
        
        success_count = 0
        for command_name in commands:
            if self.run_single_command(command_name):
                success_count += 1
            else:
                self.log_message(f"Execution order failed at: {command_name}", 'ERROR')
                break
        
        if success_count == len(commands):
            self.log_message(f"Execution order '{order_name}' completed successfully")
            return True
        else:
            self.log_message(f"Execution order '{order_name}' failed", 'ERROR')
            return False
    
    def list_commands(self):
        """List all available commands"""
        print("\n=== ICGVWA Management Commands ===")
        print(f"Project: {self.config.get('project', {}).get('name', 'Unknown')}")
        print(f"Version: {self.config.get('project', {}).get('version', 'Unknown')}")
        print()
        
        # List commands by category
        categories = {
            'setup_commands': 'Setup Commands',
            'data_commands': 'Data Management Commands',
            'user_commands': 'User Management Commands',
            'maintenance_commands': 'System Maintenance Commands',
            'rbac_commands': 'RBAC Commands'
        }
        
        for category_key, category_name in categories.items():
            commands = self.config.get(category_key, [])
            if commands:
                print(f"\n{category_name}:")
                for cmd in commands:
                    dangerous = " (DANGEROUS)" if cmd['name'] in self.config.get('security', {}).get('dangerous_commands', []) else ""
                    print(f"  {cmd['name']:<30} - {cmd['description']}{dangerous}")
        
        # List one-time commands
        one_time_commands = self.config.get('one_time_commands', [])
        if one_time_commands:
            print(f"\nOne-time Command Sequences:")
            for cmd in one_time_commands:
                print(f"  {cmd['name']:<30} - {cmd['description']}")
        
        # List execution orders
        execution_orders = self.config.get('execution_order', {})
        if execution_orders:
            print(f"\nExecution Orders:")
            for order_name in execution_orders.keys():
                print(f"  {order_name}")
        
        # List aliases
        aliases = self.config.get('aliases', {})
        if aliases:
            print(f"\nAliases:")
            for alias, target in aliases.items():
                print(f"  {alias:<30} -> {target}")
    
    def run_alias(self, alias_name):
        """Run command by alias"""
        aliases = self.config.get('aliases', {})
        if alias_name in aliases:
            target = aliases[alias_name]
            # Check if it's an execution order or single command
            if target in self.config.get('execution_order', {}):
                return self.run_execution_order(target)
            else:
                return self.run_single_command(target)
        else:
            self.log_message(f"ERROR: Alias '{alias_name}' not found", 'ERROR')
            return False

def main():
    parser = argparse.ArgumentParser(description='ICGVWA Management Command Runner')
    parser.add_argument('command', nargs='?', help='Command name, alias, or execution order to run')
    parser.add_argument('--list', '-l', action='store_true', help='List all available commands')
    parser.add_argument('--config', '-c', default='management_commands.yml', help='Path to YAML config file')
    parser.add_argument('--order', '-o', help='Run commands in execution order')
    
    args = parser.parse_args()
    
    runner = ManagementCommandRunner(args.config)
    
    if args.list:
        runner.list_commands()
        return
    
    if args.order:
        success = runner.run_execution_order(args.order)
        sys.exit(0 if success else 1)
    
    if args.command:
        # Try as single command first, then as alias
        success = runner.run_single_command(args.command)
        if not success:
            success = runner.run_alias(args.command)
        sys.exit(0 if success else 1)
    
    # No command specified, show help
    parser.print_help()

if __name__ == '__main__':
    main()