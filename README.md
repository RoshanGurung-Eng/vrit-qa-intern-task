# QA Intern Task - Signup Automation

# What it does

This script automates the signup process on https://authorized-partner.vercel.app/
using Selenium with Python.

# How to run it

1. Clone this repo
2. Install dependencies: pip install -r requirements.txt
3. Run: python scripts/signup_automation.py

# My environment details

- Python: 3.14
- Selenium: 4.x
- Chrome browser
- Windows 11

# Test email/credentials I used

- Email: roshant99@yopmail.com
- Password: 98035bobU!
- Phone: 9800564571

# Important details to note

1. OTP is automatically scraped from the inbox in Yopmail.
2. Radix UI is used in dropdowns. I used JS to select options.
   - Note: In the demo video, some dropdown selections required manual
     interaction due to timing/rendering differences in the public environment.
   - Production fix: Configure test environment for direct value binding
     or add explicit waits for option visibility.
3. If in test env, OTP verification can be skipped for yopmail emails to ensure fully automated execution.

# Features that work

- Creates an account with all details.
- Scrape OTP from Yopmail.
- Completes all 4 steps in signup.
- All checkboxes.

# List of files in the codebase

- scripts/signup_automation.py - Python script.
- requirements.txt - Python packages.
- reports - screenshots of website output
- assets - contain demo video

- Roshan Gurung
