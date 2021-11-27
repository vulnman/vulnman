# Vulnman

Vulnman is a vulnerability management web application written in Python using the powerful django framework.

**This project is in an early stage! You may not want to use it at the moment!**

**There may be breaking changes in the database layout!**


## Features
- Multiple Projects
- Report generation (requires LaTeX environment on host)
    - PDF export
    - Multiple revisions with changelogs
    - Edit raw LaTeX source, if needed
- Vulnerability Management
- Populate vulnerability values using searchable vulnerability templates
- Import vulnerability templates from CSV files


## Documentation
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

