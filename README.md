# Frappe CI/CD Learning & Practice 🚀

Welcome to your Frappe CI/CD learning journey! This repository will help you understand and practice Continuous Integration with Frappe Framework and ERPNext development.

## What is CI for Frappe? 🤔

**Continuous Integration (CI)** for Frappe development means:
- Automatically testing your custom apps when you push code
- Running linting and code quality checks
- Testing database migrations
- Validating your Frappe apps across different Python/Node versions
- Ensuring your customizations don't break ERPNext

## Frappe Development Basics 📚

### Key Concepts
- **Frappe Framework**: Python web framework for building business applications
- **ERPNext**: Open-source ERP built on Frappe
- **Bench**: Command-line tool for managing Frappe/ERPNext installations
- **Apps**: Custom modules/applications built on Frappe framework

### Typical Frappe Development Workflow

```
1. Create Frappe App → 2. Develop Features → 3. Write Tests → 4. Push to Git → 5. CI Runs Tests → 6. Deploy
```

## Repository Structure 📁

```
CI_practice-/
├── frappe-app-example/          # Sample Frappe app with CI
├── .github/workflows/           # GitHub Actions for Frappe CI
├── bench-setup/                 # Bench installation scripts
├── exercises/                   # Hands-on CI exercises
└── docs/                       # Learning resources
```

## Quick Start with Frappe CI 🏃‍♂️

### Prerequisites
- Ubuntu/Debian Linux (WSL2 works on Windows)
- Python 3.8+
- Node.js 14+
- Git
- Basic knowledge of Python

### Getting Started
1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd CI_practice-
   ```

2. **Learn with the sample app**
   ```bash
   cd frappe-app-example
   ```

3. **Set up local development**
   ```bash
   ./bench-setup/install-bench.sh
   ```

## Learning Exercises 💪

### Exercise 1: Basic Frappe App CI
- Create a simple Frappe app
- Set up GitHub Actions to run tests
- Learn about Frappe's testing framework

### Exercise 2: Database Migrations CI
- Create DocTypes and database changes
- Test migrations in CI pipeline
- Handle migration rollbacks

### Exercise 3: Multi-version Testing
- Test your app across Python 3.8, 3.9, 3.10
- Test with different ERPNext versions
- Matrix builds for comprehensive testing

### Exercise 4: Code Quality CI
- ESLint for JavaScript
- Flake8/Black for Python
- Frappe-specific linting rules

## Frappe CI Best Practices ✅

- **Test database migrations** - Always test schema changes
- **Use fixture data** - Consistent test data across environments
- **Test API endpoints** - Validate your custom APIs
- **Check permissions** - Test role-based access
- **Performance testing** - Monitor query performance
- **Documentation** - Auto-generate API docs

## Common Frappe CI Pipeline 🔄

```yaml
Trigger (Push/PR) → 
Setup Frappe Environment → 
Install Dependencies → 
Create Test Site → 
Run Tests → 
Code Quality Checks → 
Generate Reports → 
Deploy (if main branch)
```

## Next Steps 🎯

1. Complete Exercise 1 to create your first Frappe app with CI
2. Set up a local Frappe development environment
3. Practice with the provided examples
4. Build your own custom app with comprehensive CI

---

**Let's start learning Frappe CI!** 🎉

```

Now let me create a GitHub Actions workflow for Frappe CI:

```yaml:.github/workflows/frappe-ci.yml
name: Frappe CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
        
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
        ports:
          - 3306:3306
          
      redis:
        image: redis:alpine
        options: --health-cmd="redis-cli ping" --health-interval=10s --health-timeout=5s --health-retries=3
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '16'
        
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
          
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          git build-essential python3-setuptools python3-dev \
          libffi-dev python3-pip libssl-dev libtiff5-dev \
          libmariadb-dev-compat libmariadb-dev \
          redis-tools libmysqlclient-dev
          
    - name: Install bench
      run: |
        pip install frappe-bench
        
    - name: Initialize bench
      run: |
        bench init --skip-redis-config-generation --frappe-branch version-14 frappe-bench
        cd frappe-bench
        
    - name: Create test site
      run: |
        cd frappe-bench
        bench new-site test_site --admin-password admin --db-root-password root
        bench --site test_site install-app frappe
        
    - name: Install custom app (if exists)
      run: |
        cd frappe-bench
        if [ -d "../frappe-app-example" ]; then
          bench get-app ../frappe-app-example
          bench --site test_site install-app frappe_app_example
        fi
        
    - name: Run tests
      run: |
        cd frappe-bench
        bench --site test_site run-tests --coverage
        
    - name: Code quality checks
      run: |
        cd frappe-bench
        # Run linting on custom apps
        if [ -d "apps/frappe_app_example" ]; then
          cd apps/frappe_app_example
          python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          python -m flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
        fi
```

Let me also create a sample Frappe app structure:

```python:frappe-app-example/setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="frappe_app_example",
    version="0.0.1",
    description="Example Frappe app for CI/CD learning",
    author="CI/CD Learner",
    author_email="learner@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
```

```python:frappe-app-example/frappe_app_example/__init__.py
__version__ = '0.0.1'
```

```json:frappe-app-example/frappe_app_example/hooks.py
app_name = "frappe_app_example"
app_title = "Frappe App Example"
app_publisher = "CI/CD Learner"
app_description = "Example Frappe app for learning CI/CD"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "learner@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_app_example/css/frappe_app_example.css"
# app_include_js = "/assets/frappe_app_example/js/frappe_app_example.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_app_example/css/frappe_app_example.css"
# web_include_js = "/assets/frappe_app_example/js/frappe_app_example.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_app_example/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#    "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_app_example.install.before_install"
# after_install = "frappe_app_example.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_app_example.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#    "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#    "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#    "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#    "*": {
#        "on_update": "method",
#        "on_cancel": "method",
#        "on_trash": "method"
#    }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#    "all": [
#        "frappe_app_example.tasks.all"
#    ],
#    "daily": [
#        "frappe_app_example.tasks.daily"
#    ],
#    "hourly": [
#        "frappe_app_example.tasks.hourly"
#    ],
#    "weekly": [
#        "frappe_app_example.tasks.weekly"
#    ]
#    "monthly": [
#        "frappe_app_example.tasks.monthly"
#    ]
# }

# Testing
# -------

# before_tests = "frappe_app_example.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#    "frappe.desk.doctype.event.event.get_events": "frappe_app_example.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#    "Task": "frappe_app_example.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
```

And let me create a requirements file:

```text:frappe-app-example/requirements.txt
frappe
```

Finally, let me create an exercise for
