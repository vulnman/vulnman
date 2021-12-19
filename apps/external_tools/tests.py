from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.external_tools.parsers.gobuster import GobusterDir
from apps.networking.models import Service
from apps.findings.models import Finding


class GobusterDirTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_parse(self):
        results = """
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://testphp.vulnweb.com
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /app/test.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Expanded:                true
[+] Timeout:                 10s
===============================================================
2021/12/08 12:50:54 Starting gobuster in directory enumeration mode
===============================================================
http://testphp.vulnweb.com/admin                (Status: 301) [Size: 169] [--> http://testphp.vulnweb.com/admin/]
http://testphp.vulnweb.com/cart.php             (Status: 200) [Size: 4903]
===============================================================
2021/12/08 12:50:55 Finished
===============================================================
"""
        project = self._create_project(creator=self.user1)
        gobuster = GobusterDir().parse(results, project, self.user1)
        self.assertEqual(project.host_set.count(), 1)
        self.assertEqual(Service.objects.filter(port=80).count(), 1)
        self.assertEqual(Finding.objects.count(), 2)
        self.assertEqual(Finding.objects.filter(data__contains="admin").count(), 1)
