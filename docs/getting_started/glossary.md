# Glossary

This section will give a short overview about the terminology used within the vulnman applications.


## Components

**Vulnman Server:**
The [vulnman server](https://github.io/vulnman/vulnman) is the key part of the vulnman applications.
It is the part between you and the database which stores all results behind the scenes.

**Vulnman Cli:**
The [vulnman cli](https://github.io/vulnman/vulnman-cli) is a command line interface that you can use like a terminal to send results
of different command directly to your vulnman server.

**Vulnman Agent:**
TODO


## Classes

`Client`
:   A client is your customer who has hired you for a security analysis.

`Project`
:   A project can be seen as an engagement.

`Finding`
:   A finding is an object that is worth tracking but not a vulnerability (e.g. a Web Application).
Findings are not part of the report

`Vulnerability`
:   A vulnerability is a security issue that has an impact on your client.
Vulnerabilities can be excluded from the report, if needed.