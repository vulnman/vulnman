# Plugin System
Vulnman has a plugin system that is used to process external tool reports.

The [vulnman-cli](https://github.com/vulnman/vulnman-cli) is rewriting the commands to match the required format for later processing in the background.

The [vulnman-server](https://github.com/vulnman/vulnman) finally processes all incoming tool results and maps the findings into its database models.


## Built-In Plugins
The "Example Commands" provided below are only required, if you upload the results directly without using the `vulnman-cli`.

| Tool | Example Command | Version Added |
| --- | ---| --- |
| nmap | `nmap -sV -sC -oX exmaple.xml example.com` | 0.2.2 |
| subfinder | `subfinder -d example.com | tee subfinder.txt` | 0.2.2 |
| Gobuster (DNS) | `gobuster dns -d example.com -w subdomains.txt | tee gobuster.dns.txt` | 0.2.2 |
| Gobuster (Dir) | `gobuster dir -u http://example.com -w common.txt | tee gobuster.dir.txt` | 0.2.2 |
| Gobuster (Vhost) | `gobuster vhost -u http://example.com -w subdomains.txt | tee gobuster.vhost.txt` | 0.2.2 |
| aiodnsbrute | `aiodnsbrute -w wordlist.txt example.com | tee aiodnsbrute.txt` | 0.2.2 |
| fierce | `fierce -domain example.com | tee fierce.txt` | 0.2.2 |
| infoga | `infoga --domain example.com -r infoga.txt` | 0.2.2 |
| BurpSuite Pro (XML) | - | 0.2.2 |
| nuclei | `nuclei -json -nc -o results.json -u http://localhost -t nuclei-templates` | 0.2.2 |
| testssl | `testssl -oj results.json https://example.com` | 0.2.2 |

## Writing your own Plugins
The plugin consists of two parts: 
The part that processes the (raw) output of the tool.
This is currently happening on the server (see [#60](https://github.com/vulnman/vulnman/issues/60)).
The second part is the plugin that handles the command rewrite and ensures all required arguments exist.
This part is currently really lightweight and easy to write.

This tutorial will create the gobuster dns plugin.

### Parser
First, you need to create a python package. This example uses the default location
of the built-in parsers (`tools/parsers/`).

Add your tool to your [settings file](../getting_started/configuration) file like shown below:

```python
CUSTOM_EXTERNAL_TOOLS = {
    "gobuster-dns": "tools.parsers.gobuster.GobusterDNS"
}
```

This is how the final plugin looks like:

```python
import re
from vulnman.utils.tools import ToolResultParser

class GobusterDNS(ToolResultParser):
    """
    Example Command:
    ``gobuster dns -w subdomains.txt -d example.com | tee gobuster-dns.txt``
    """
    tool_name = "gobuster dns"

    def parse(self, result, project, creator, command=None):
        for item in re.findall(r"(Found: )(.*)", result):
            ip = self._resolve(item[1])
            if ip:
                host, _created = self._get_or_create_host(ip, project, creator, command=command)
                _hostname, _created = self._get_or_create_hostname(item[1], host, project, creator, command=command)
```

### CLI
This is the most easy part in writing your own plugins.

If your plugin can be processed without writing the results to a temporary file and does not need any special flags to be set, this is how a plugin will look:

```python
from vulnman_plugins import plugin

class Subfinder(plugin.Plugin):
    _alias_ = 'subfinder'

    def setup(self):
        pass
```


The nuclei plugin for example, requires some special flags to be set, to write the results to a json file.
The following code shows how you can enforce such a command rewrite.

```python
from vulnman_plugins import plugin


class Nuclei(plugin.Plugin):
    _alias_ = 'nuclei'

    def setup(self):
        self.required_arguments = [
            plugin.Argument("-json", has_value=False), plugin.Argument("-o", is_filepath=True),
            plugin.Argument("-nc", has_value=False)
        ]
        self.use_temp_file = True
```

This part of the plugin needs to be added to the ``vulnman_plugins`` package.
