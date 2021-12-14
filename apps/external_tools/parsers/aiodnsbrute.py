from vulnman.utils.tools import ToolResultParser


class Aiodnsbrute(ToolResultParser):
    """
    Example command:
    ``aiodnsbrute -w wordlist.txt example.com | tee aiodnsbrute.txt``
    """
    tool_name = "aiodnsbrute"

    def parse(self, result, project, creator, command=None):
        for line in result.split("\n"):
            if "[+]" in line:
                hostname = line.split(" ")[1].replace("\x1b[0m", "")
                ip = line.split(" ")[-1].replace("\t", "").replace("[", "").replace("]", "").replace("'", "")
                host, _created = self._get_or_create_host(ip, project, creator, command=command)
                self._get_or_create_hostname(hostname, host, project, creator, command=command)
