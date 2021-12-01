# Vulnman

Vulnman is a vulnerability management web application written in Python using the powerful django framework.

**This project is in an early stage! You may not want to use it at the moment!**

**There may be breaking changes in the database layout!**


## Features
- Multiple Projects
  - Manage found Hosts, Services, Webapps, ...
- Report generation (requires LaTeX environment on host)
    - PDF export
    - Multiple revisions with changelogs
    - Edit raw LaTeX source, if needed
- Vulnerability Management
  - Project Dashboard with charts
  - Vulnerability Templates
  - CVSS Calculator
  - Write vulnerability information Markdown
- Import vulnerability templates from CSV files


## Documentation

### Online
The documentation can be found under [https://blockomat2100.github.io/vulnman](https://blockomat2100.github.io/vulnman).

*Note: The documentation is in a really early state!*

### Build locally
You can build the documentation locally using sphinx.

```
cd docs/
pip install -r requirements.txt
export PATH=$PATH:/home/user/.local/bin
make html
```

The documentation files can be found under `_build/html`.



## Projects, Dependencies and Versions
- Bootstrap 5.0.1
- jquery 3.6.0
- jQuery Formset 1.5-pre
- Forkawesome 1.1.7
- Django latest
- chart.js 3.6.0
- Codemirror 5.64.0
