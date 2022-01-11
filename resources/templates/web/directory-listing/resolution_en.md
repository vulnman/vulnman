There is not usually any good reason to provide directory listings, and disabling them may place additional hurdles in the path of an attacker. This can normally be achieved in two ways:

- Configure your web server to prevent directory listings for all paths beneath the web root;
- Place into each directory a default file (such as index.html) that the web server will display instead of returning a directory listing.