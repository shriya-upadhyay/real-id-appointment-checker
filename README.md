# NJ MVC Appointment Notifier

This script monitors the NJ MVC mobile unit appointment website and sends notifications via email when appointments become available.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your email credentials:
```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
```

3. Run the script:
```bash
python appointment_checker.py
```

## Features

- Monitors the NJ MVC mobile unit appointment website
- Sends email notifications when appointments become available
- Configurable check intervals

## Note

If you're using Gmail, you'll need to use an app-specific password instead of your regular password. You can generate this in your Google Account settings under Security > 2-Step Verification > App passwords. 