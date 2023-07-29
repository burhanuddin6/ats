# Applicant tracking system

> An applicant tracking system (ATS) helps companies organize candidates for hiring and recruitment purposes.

[![code analysis welcome](https://img.shields.io/badge/code&nbsp;analysis-pylint-blue.svg?style=flat)](https://github.com/dwyl/esta/issues)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

## Requirements (Prerequisites)
Tools and packages required to successfully install this project.

- [[Python 3.10](https://realpython.com/installing-python/)] and up 

## Installation

Once you downloaded project, Run this following command
```
pip install -r requirements.txt
```

## Starting django server
```
python manage.py runserver
```
Then, Go to: https://localhost:8000 or http://127.0.0.1:8000

## Code Quality

Use pylint suggestions from workflow and improve the coding style in the following order:

  - imports style issues
  - module naming
  - function/class docstring
  - function naming (ignore method names inside applicants/models.py beause these are django specific)
  - ignore other (class, methods, variable, constants) naming for now. The current variable naming is consistent therefore, change the test to support that naming convention.

## TODO Testing

- Add testcase to check models
- Add testcase to check pages
- Add testcase to check js using selenium

## How to Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate. If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

Steps to contribute:
1. Fork this repository ([ats-public](https://github.com/burhanuddin6/ats_public))
2. Create your feature branch (git checkout -b feature/enhancement)
3. Commit your changes (git commit -am 'Add some enhancement')
4. Push to the branch (git push origin feature/enhancement)
5. Create a new Pull Request
