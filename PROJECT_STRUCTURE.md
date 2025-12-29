# Veteran Association Management System - Project Structure

## 📁 Root Directory Structure

```
veteran_cg/
├── 📁 .github/                          # GitHub configuration
│   └── copilot-instructions.md         # GitHub Copilot instructions
├── 📁 media/                           # User uploaded media files
│   ├── 📁 carousel/                    # Carousel images
│   ├── 📁 children/                    # Children photos (organized by year)
│   ├── 📁 documents/                   # Member documents
│   ├── 📁 events/                      # Event images
│   ├── 📁 gallery/                     # Gallery images
│   ├── 📁 matrimonial/                 # Matrimonial photos
│   ├── 📁 profiles/                    # Profile pictures
│   ├── 📁 resumes/                     # Resume documents
│   ├── 📁 state_heads/                 # State head photos
│   └── README.md                       # Media directory documentation
├── 📁 static/                          # Static assets (development)
│   ├── 📁 css/
│   │   └── style.css                   # Main stylesheet
│   ├── 📁 images/                      # Static images
│   │   ├── 📁 carousel/                # Static carousel images
│   │   ├── 📁 qrpayment/              # QR payment images
│   │   ├── 📁 state_admins/           # State admin photos
│   │   └── 📁 veterans/               # Veteran photos
│   └── 📁 js/
│       └── script.js                   # Main JavaScript file
├── 📁 staticfiles/                     # Collected static files (production)
│   ├── 📁 admin/                       # Django admin static files
│   ├── 📁 css/                         # Compressed CSS files
│   ├── 📁 django_extensions/           # Django extensions static files
│   ├── 📁 grappelli/                   # Grappelli admin theme
│   ├── 📁 images/                      # Static images (production)
│   ├── 📁 jazzmin/                     # Jazzmin admin theme
│   ├── 📁 js/                          # Compressed JavaScript files
│   ├── 📁 vendor/                      # Third-party libraries
│   └── staticfiles.json               # Static files manifest
├── 📁 veteran_app/                     # Main Django application
├── 📁 veteran_project/                 # Django project configuration
├── 📄 Configuration & Deployment Files
├── 📄 Database & Scripts
└── 📄 Documentation Files
```

## 📱 Django Application Structure (`veteran_app/`)

```
veteran_app/
├── 📁 management/                      # Custom Django management commands
│   ├── 📁 commands/
│   │   ├── __init__.py
│   │   ├── clear_data.py              # Clear database data
│   │   ├── create_accounts_user.py    # Create accounts user
│   │   ├── create_users.py            # Create system users
│   │   ├── data_manager.py            # Data management utilities
│   │   ├── fix_chat_portal.py         # Fix chat portal issues
│   │   ├── fix_state_permissions.py   # Fix state permissions
│   │   ├── generate_association_numbers.py # Generate association IDs
│   │   ├── import_members.py          # Import member data
│   │   ├── init_rbac.py              # Initialize RBAC system
│   │   ├── load_initial_data.py       # Load initial system data
│   │   ├── seed_data.py              # Seed master data
│   │   ├── seed_members.py           # Seed sample members
│   │   ├── seed_state_users.py       # Seed state users
│   │   └── setup_state_admin_permissions.py # Setup state permissions
│   └── __init__.py
├── 📁 migrations/                      # Database migrations
│   ├── __init__.py
│   ├── 0001_initial.py               # Initial database schema
│   ├── 0002_userstate.py             # User state mapping
│   ├── 0003_alter_veteranmember_document.py
│   ├── 0004_carouselslide_alter_veteranmember_document.py
│   ├── 0005_alter_userstate_options_userstate_approved_and_more.py
│   ├── 0006_notification_document.py
│   ├── 0007_veteranuser.py
│   ├── 0008_veteranmember_alternate_email_and_more.py
│   ├── 0009_veteranmember_nearest_dhq.py
│   ├── 0010_child_medicalcategory_and_more.py
│   ├── 0011_update_required_fields.py
│   ├── 0012_bankaccount_expensecategory_financialyear_and_more.py
│   ├── 0013_auto_20251105_0615.py
│   ├── 0014_veteranmember_medical_category_text_and_more.py
│   ├── 0015_matrimonial_child_name_alter_matrimonial_child.py
│   ├── 0016_event_eventcategory_eventregistration_paymentgateway_and_more.py
│   ├── 0017_rename_group_to_branch.py
│   ├── 0018_alter_branch_options_alter_veteranmember_branch_and_more.py
│   ├── 0019_reportconfiguration.py
│   ├── 0020_galleryimage.py
│   ├── 0021_veteranmember_zip_code.py
│   ├── 0022_userstate_bio_userstate_contact_number_and_more.py
│   ├── 0023_add_subscription_ref_no.py
│   ├── 0024_add_phone_validators.py
│   ├── 0025_alter_carouselslide_image_alter_child_child_photo_and_more.py
│   ├── 0026_add_association_id_card_fields.py
│   ├── 0027_update_association_number_format.py
│   ├── 0028_add_accounts_user.py
│   └── 0029_associationverification_permission_and_more.py
├── 📁 templates/                       # HTML templates
│   └── 📁 veteran_app/
│       ├── 📁 includes/               # Reusable template components
│       │   ├── messages.html          # Flash messages
│       │   ├── metric_cards.html      # Dashboard metrics
│       │   ├── navbar.html            # Navigation bar
│       │   ├── pagination.html        # Pagination component
│       │   └── veteran_member_form.html # Member form component
│       ├── 📁 rbac/                   # Role-Based Access Control templates
│       │   ├── audit_logs.html        # Audit logs view
│       │   ├── create_role.html       # Create role form
│       │   ├── dashboard.html         # RBAC dashboard
│       │   ├── delete_role.html       # Delete role confirmation
│       │   ├── edit_role.html         # Edit role form
│       │   ├── manage_permissions.html # Permission management
│       │   ├── manage_roles.html      # Role management
│       │   ├── permission_matrix.html # Permission matrix view
│       │   └── user_role_management.html # User role assignment
│       ├── about.html                 # About page
│       ├── admin_job_portal.html      # Admin job portal
│       ├── association_id_card.html   # Association ID card
│       ├── backup_codes.html          # 2FA backup codes
│       ├── base.html                  # Base template
│       ├── chat_portal.html           # Chat portal
│       ├── create_event.html          # Create event form
│       ├── create_veteran_user.html   # Create veteran user
│       ├── dashboard.html             # Main dashboard
│       ├── edit_event.html            # Edit event form
│       ├── event_detail.html          # Event details
│       ├── event_registration.html    # Event registration
│       ├── events_list.html           # Events listing
│       ├── gallery.html               # Photo gallery
│       ├── index.html                 # Home page
│       ├── job_portal_form.html       # Job portal form
│       ├── job_portal.html            # Job portal
│       ├── login.html                 # Login page
│       ├── manage_carousel.html       # Carousel management
│       ├── manage_children.html       # Children management
│       ├── manage_data.html           # Data management
│       ├── manage_events.html         # Event management
│       ├── manage_users.html          # User management
│       ├── manage_veteran_users.html  # Veteran user management
│       ├── matrimonial_form.html      # Matrimonial form
│       ├── matrimonial_portal.html    # Matrimonial portal
│       ├── media.html                 # Media management
│       ├── member_form.html           # Member form
│       ├── password_reset_admin.html  # Password reset (admin)
│       ├── payment_page.html          # Payment page
│       ├── payment_settings.html      # Payment settings
│       ├── reports_builder.html       # Reports builder
│       ├── send_chat_request.html     # Send chat request
│       ├── services.html              # Services page
│       ├── setup_2fa.html             # Setup 2FA
│       ├── state_dashboard.html       # State dashboard
│       ├── state_detail.html          # State details
│       ├── test_rbac.html             # RBAC testing
│       ├── transaction_list.html      # Transaction list
│       ├── treasurer_dashboard.html   # Treasurer dashboard
│       ├── user_profile.html          # User profile
│       ├── user_settings.html         # User settings
│       ├── verify_2fa.html            # Verify 2FA
│       ├── verify_association.html    # Association verification
│       ├── veteran_dashboard.html     # Veteran dashboard
│       ├── veteran_profile_detail.html # Veteran profile details
│       ├── veteran_profile_edit.html  # Edit veteran profile
│       ├── veteran_register.html      # Veteran registration
│       └── veteran_welcome.html       # Veteran welcome page
├── __init__.py                        # Python package marker
├── admin.py                           # Django admin configuration
├── apps.py                            # App configuration
├── context_processors.py             # Template context processors
├── decorators.py                      # Custom decorators
├── event_views.py                     # Event-related views
├── forms.py                           # Django forms
├── middleware.py                      # Custom middleware
├── models.py                          # Database models
├── rbac_models.py                     # RBAC models
├── rbac_urls.py                       # RBAC URL patterns
├── rbac_utils.py                      # RBAC utilities
├── rbac_views.py                      # RBAC views
├── security.py                        # Security utilities
├── services.py                        # Business logic services
├── signals.py                         # Django signals
├── tests.py                           # Unit tests
├── two_factor_utils.py                # Two-factor authentication utilities
├── urls.py                            # URL patterns
├── validators.py                      # Custom validators
├── verification_views.py              # Verification views
└── views.py                           # Main view functions
```

## ⚙️ Django Project Configuration (`veteran_project/`)

```
veteran_project/
├── __init__.py                        # Python package marker
├── asgi.py                           # ASGI configuration
├── production_settings.py            # Production settings
├── settings.py                       # Main Django settings
├── urls.py                           # Main URL configuration
└── wsgi.py                           # WSGI configuration
```

## 📄 Configuration & Deployment Files

```
├── .env                              # Environment variables (local)
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── build.sh                          # Build script (Linux/Mac)
├── deploy.bat                        # Deployment script (Windows)
├── deploy.sh                         # Deployment script (Linux/Mac)
├── Procfile                          # Heroku process file
├── render.yaml                       # Render deployment config
├── requirements.txt                  # Python dependencies
└── runtime.txt                       # Python runtime version
```

## 🗄️ Database & Scripts

```
├── db.sqlite3                        # SQLite database (development)
├── add_categories.py                 # Add categories script
├── add_medical_categories.py         # Add medical categories
├── apply_security_fixes.py           # Apply security fixes
├── create_accounts_postgresql.sql    # PostgreSQL accounts setup
├── create_accounts_table.sql         # Create accounts table
├── create_accounts_user_simple.py   # Simple accounts user creation
├── create_accounts_user.sql          # SQL for accounts user
├── create_placeholder_images.py     # Create placeholder images
├── django_shell_commands.py         # Django shell commands
├── insert_medical_categories_postgres.sql # PostgreSQL medical categories
├── insert_medical_categories.sql    # SQL medical categories
├── setup_accounts_user.bat          # Setup accounts user (Windows)
├── setup_accounts_user.py           # Setup accounts user script
├── shell_commands.txt               # Shell commands reference
├── test_rbac_view.py                # Test RBAC views
├── test_state_access.py             # Test state access
└── test_states.py                   # Test states functionality
```

## 📚 Documentation Files

```
├── ACCOUNTS_USER_SETUP.md            # Accounts user setup guide
├── ReadME.md                         # Main project documentation
├── PROJECT_STRUCTURE.md             # This file
└── security.log                     # Security audit log
```

## 🏗️ Key Architecture Components

### 1. **Models Layer** (`models.py`, `rbac_models.py`)
- **Core Models**: State, Rank, Branch, BloodGroup, VeteranMember
- **User Management**: UserState, VeteranUser
- **Content Management**: CarouselSlide, Notification, Document
- **Events**: Event, EventCategory, EventRegistration
- **Financial**: PaymentGateway, PaymentOrder, BankAccount
- **RBAC**: Role, Permission, UserRole, AuditLog

### 2. **Views Layer** (`views.py`, `event_views.py`, `rbac_views.py`, `verification_views.py`)
- **Authentication**: Login, logout, 2FA
- **Member Management**: CRUD operations for veterans
- **State Management**: State-specific dashboards
- **Event Management**: Event creation and registration
- **RBAC**: Role and permission management
- **Verification**: Association verification system

### 3. **Forms Layer** (`forms.py`)
- **Member Forms**: VeteranMemberForm, ChildForm
- **Authentication Forms**: LoginForm, 2FAForm
- **Event Forms**: EventForm, EventRegistrationForm
- **User Management Forms**: UserCreationForm, ProfileForm

### 4. **Security Layer** (`security.py`, `middleware.py`, `decorators.py`)
- **Authentication**: Multi-factor authentication
- **Authorization**: Role-based access control
- **Validation**: Input validation and sanitization
- **Audit**: Security logging and monitoring

### 5. **Services Layer** (`services.py`)
- **Business Logic**: Core application logic
- **Data Processing**: Member data management
- **Integration**: External service integration
- **Utilities**: Helper functions and utilities

## 🔧 Management Commands

The application includes comprehensive management commands for:

- **Data Management**: `seed_data.py`, `clear_data.py`, `import_members.py`
- **User Management**: `create_users.py`, `seed_state_users.py`
- **RBAC Setup**: `init_rbac.py`, `setup_state_admin_permissions.py`
- **System Maintenance**: `generate_association_numbers.py`, `fix_state_permissions.py`

## 📊 Database Schema Overview

### Core Entities
- **VeteranMember**: Central member entity with personal, military, and association details
- **State**: Indian states with administrative boundaries
- **UserState**: User-to-state mapping for access control
- **Event**: Event management system
- **Payment**: Financial transaction handling

### Relationships
- VeteranMember → State (Many-to-One)
- VeteranMember → Rank (Many-to-One)
- VeteranMember → Branch (Many-to-One)
- UserState → User (One-to-One)
- EventRegistration → Event (Many-to-One)

## 🚀 Deployment Structure

### Development
- SQLite database
- Local static files
- Debug mode enabled
- Development server

### Production
- PostgreSQL database
- Collected static files
- Production settings
- WSGI/ASGI server (Gunicorn/Uvicorn)

## 🔐 Security Features

- **Authentication**: Multi-factor authentication (2FA)
- **Authorization**: Role-based access control (RBAC)
- **Data Protection**: Input validation and sanitization
- **Audit Trail**: Comprehensive logging system
- **File Security**: Secure file upload handling
- **Session Management**: Secure session handling

---

**Project Status**: ✅ Production Ready
**Last Updated**: January 2025
**Django Version**: 5.2.6
**Python Version**: 3.8+