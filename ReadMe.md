# Vulnman

Vulnman is a vulnerability and pentesting management web application written in Python using the powerful django framework.

**This project is in an early stage! You may not want to use it at the moment!**

**There may be breaking changes in the database layout!**



## Features
Features are listed in the [documentation](https://vulnman.github.io/vulnman).

## Documentation

### Online
The documentation can be found under [https://vulnman.github.io/vulnman](https://vulnman.github.io/vulnman).

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
