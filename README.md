# URL Filter Application

A web-based URL filtering application built with Flask that allows administrators and teachers to manage and monitor URL access. The application provides role-based access control with separate interfaces for administrators and teachers.

## Features

- Role-based authentication system (Admin and Teacher)
- URL filtering and management
- Access history tracking
- Dashboard for both administrators and teachers
- Real-time URL monitoring
- Customizable filtering rules

## Project Structure
url_filter_app/
│
├── app/                    # Application package
│   ├── config.py          # Configuration settings
│   ├── models.py          # Database models
│   ├── utils.py           # Utility functions
│   │
│   ├── routes/            # Route handlers
│   │   ├── admin.py       # Admin routes
│   │   ├── auth.py        # Authentication routes
│   │   └── teacher.py     # Teacher routes
│   │
│   ├── static/            # Static files
│   │   ├── css/
│   │   └── img/
│   │
│   └── templates/         # HTML templates
│       ├── admin/         # Admin interface templates
│       ├── teacher/       # Teacher interface templates
│       ├── base.html      # Base template
│       ├── index.html     # Landing page
│       └── login.html     # Login page
│
├── requirements.txt        # Python dependencies
└── run.py                 # Application entry point
Copy
## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url_filter_app.git
cd url_filter_app

Create and activate a virtual environment:

bashCopypython -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

Install dependencies:

bashCopypip install -r requirements.txt

Configure the application:

Copy config.py.example to config.py (if applicable)
Update configuration settings as needed


Initialize the database:

bashCopyflask db init
flask db migrate
flask db upgrade
Running the Application

Start the development server:

bashCopypython run.py

Access the application at http://localhost:5000

Usage
Administrator Features

Add/remove teachers
Manage URL filtering rules
View access history
Monitor active URLs
Configure system settings

Teacher Features

View allowed/blocked URLs
Request URL access changes
View personal access history

Contributing

Fork the repository
Create a new branch for your feature
Commit your changes
Push to your branch
Create a Pull Request

Security Considerations

All passwords are hashed before storage
Session management implemented
CSRF protection enabled
Input validation on all forms
Regular security updates recommended

License
This project is licensed under the MIT License - see the LICENSE file for details.
Support
For support, please open an issue in the GitHub repository or contact the development team.
Acknowledgments

Flask framework and its contributors
All open-source libraries used in this project
