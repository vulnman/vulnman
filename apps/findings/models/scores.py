import cvss
from django.db import models


class OWASPScore(models.Model):
    NOT_APPLICABLE = 0

    RISK_INFORMATIONAL = "Informational"
    RISK_LOW = "Low"
    RISK_MEDIUM = "Medium"
    RISK_HIGH = "High"
    RISK_CRITICAL = "Critical"

    # usually this is reversed in the OWASP documentation. However, it does not make
    # sense to me to give a *non technical* vulnerability lower risk.
    SKILLS_SECURITY = 1
    SKILLS_NETWORKING = 3
    SKILLS_ADVANCED_USER = 4
    SKILLS_SOME_TECHNICAL = 6
    SKILLS_NO_TECHNICAL = 9
    SKILLS_REQUIRED_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (SKILLS_SECURITY, "Security Penetration Skills (%s)" % SKILLS_SECURITY),
        (SKILLS_NETWORKING, "Networking And Programming Skills (%s)" % SKILLS_NETWORKING),
        (SKILLS_ADVANCED_USER, "Advanced Computer User (%s)" % SKILLS_ADVANCED_USER),
        (SKILLS_SOME_TECHNICAL, "Some Technical Skills (%s)" % SKILLS_SOME_TECHNICAL),
        (SKILLS_NO_TECHNICAL, "No Technical Skills (%s)" % SKILLS_NO_TECHNICAL)
    ]

    MOTIVE_LOW = 1
    MOTIVE_POSSIBLE = 4
    MOTIVE_HIGH = 9
    MOTIVE_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (MOTIVE_LOW, "Low Or No Reward (%s)" % MOTIVE_LOW),
        (MOTIVE_POSSIBLE, "Possible Reward (%s)" % MOTIVE_POSSIBLE),
        (MOTIVE_HIGH, "High Reward (%s)" % MOTIVE_HIGH)
    ]

    OPPORTUNITY_FULL_ACCESS = 0
    OPPORTUNITY_SPECIAL_ACCESS = 4
    OPPORTUNITY_SOME_ACCESS = 7
    OPPORTUNITY_NO_ACCESS = 9

    OPPORTUNITY_CHOICES = [
        (OPPORTUNITY_FULL_ACCESS, "Full access or expensive resources required (%s)" % OPPORTUNITY_FULL_ACCESS),
        (OPPORTUNITY_SPECIAL_ACCESS, "Special access or resources required (%s)" % OPPORTUNITY_SPECIAL_ACCESS),
        (OPPORTUNITY_SOME_ACCESS, "Some access or resources required (%s)" % OPPORTUNITY_SOME_ACCESS),
        (OPPORTUNITY_NO_ACCESS, "No access or resources required (%s)" % OPPORTUNITY_NO_ACCESS)
    ]

    POPULATION_SIZE_ADMINS = 2
    POPULATION_SIZE_INTRANET = 4
    POPULATION_SIZE_PARTNERS = 5
    POPULATION_SIZE_AUTHENTICATED = 6
    POPULATION_SIZE_ANONYMOUS = 9

    POPULATION_SIZE_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (POPULATION_SIZE_ADMINS, "System Administrators (%s)" % POPULATION_SIZE_ADMINS),
        (POPULATION_SIZE_INTRANET, "Intranet Users (%s)" % POPULATION_SIZE_INTRANET),
        (POPULATION_SIZE_PARTNERS, "Partners (%s)" % POPULATION_SIZE_PARTNERS),
        (POPULATION_SIZE_AUTHENTICATED, "Authenticated users (%s)" % POPULATION_SIZE_AUTHENTICATED),
        (POPULATION_SIZE_ANONYMOUS, "Anonymous users (%s)" % POPULATION_SIZE_ANONYMOUS)
    ]

    EASE_OF_DISCOVERY_IMPOSSIBLE = 1
    EASE_OF_DISCOVERY_DIFFICULT = 3
    EASE_OF_DISCOVERY_EASY = 7
    EASE_OF_DISCOVERY_AUTOMATED = 9

    EASE_OF_DISCOVERY_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (EASE_OF_DISCOVERY_IMPOSSIBLE, "Practically impossible (%s)" % EASE_OF_DISCOVERY_IMPOSSIBLE),
        (EASE_OF_DISCOVERY_DIFFICULT, "Difficult (%s)" % EASE_OF_DISCOVERY_DIFFICULT),
        (EASE_OF_DISCOVERY_EASY, "Easy (%s)" % EASE_OF_DISCOVERY_EASY),
        (EASE_OF_DISCOVERY_AUTOMATED, "Automated Tools Available (%s)" % EASE_OF_DISCOVERY_AUTOMATED)
    ]

    EASE_OF_EXPLOIT_THEORETICAL = 1
    EASE_OF_EXPLOIT_DIFFICULT = 3
    EASE_OF_EXPLOIT_EASY = 5
    EASE_OF_EXPLOIT_AUTOMATED = 9

    EASE_OF_EXPLOIT_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (EASE_OF_EXPLOIT_THEORETICAL, "Theoretical (%s)" % EASE_OF_EXPLOIT_THEORETICAL),
        (EASE_OF_EXPLOIT_DIFFICULT, "Difficult (%s)" % EASE_OF_EXPLOIT_DIFFICULT),
        (EASE_OF_EXPLOIT_EASY, "Easy (%s)" % EASE_OF_EXPLOIT_EASY),
        (EASE_OF_EXPLOIT_AUTOMATED, "Automated Tools Available (%s)" % EASE_OF_EXPLOIT_AUTOMATED)
    ]

    AWARENESS_UNKNOWN = 1
    AWARENESS_HIDDEN = 4
    AWARENESS_OBVIOUS = 6
    AWARENESS_PUBLIC_KNOWLEDGE = 9

    AWARENESS_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (AWARENESS_UNKNOWN, "Unknown (%s)" % AWARENESS_UNKNOWN),
        (AWARENESS_HIDDEN, "Hidden (%s)" % AWARENESS_HIDDEN),
        (AWARENESS_OBVIOUS, "Obvious (%s)" % AWARENESS_OBVIOUS),
        (AWARENESS_PUBLIC_KNOWLEDGE, "Public Knowledge (%s)" % AWARENESS_PUBLIC_KNOWLEDGE)
    ]

    INTRUSION_DETECTION_ACTIVE_DETECTION = 1
    INTRUSION_DETECTION_LOGGED_AND_REVIEWED = 3
    INTRUSION_DETECTION_LOGGED_WITHOUT_REVIEW = 8
    INTRUSION_DETECTION_NOT_LOGGED = 9

    INTRUSION_DETECTION_CHOICES = [
        (NOT_APPLICABLE, "Not Applicable (%s)" % NOT_APPLICABLE),
        (INTRUSION_DETECTION_ACTIVE_DETECTION, "Active detection in application (%s)" %
         INTRUSION_DETECTION_ACTIVE_DETECTION),
        (INTRUSION_DETECTION_LOGGED_AND_REVIEWED, "Logged and reviewed (%s)" % INTRUSION_DETECTION_LOGGED_AND_REVIEWED),
        (INTRUSION_DETECTION_LOGGED_WITHOUT_REVIEW, "Logged without review (%s)" %
         INTRUSION_DETECTION_LOGGED_WITHOUT_REVIEW),
        (INTRUSION_DETECTION_NOT_LOGGED, "Not logged (%s)" % INTRUSION_DETECTION_NOT_LOGGED)
    ]

    CONFIDENTIALITY_MINIMAL_NON_SENSITIVE = 2
    CONFIDENTIALITY_MINIMAL_CRITICAL = 6
    CONFIDENTIALITY_EXTENSIVE_NON_SENSITIVE = 6
    CONFIDENTIALITY_EXTENSIVE_CRITICAL = 7
    CONFIDENTIALITY_ALL_DATA = 9

    CONFIDENTIALITY_CHOICES = [
        (CONFIDENTIALITY_MINIMAL_NON_SENSITIVE, "Minimal non-sensitive data disclosed (%s)" %
         CONFIDENTIALITY_MINIMAL_NON_SENSITIVE),
        (CONFIDENTIALITY_MINIMAL_CRITICAL, "Minimal critical data disclosed (%s)" % CONFIDENTIALITY_MINIMAL_CRITICAL),
        (CONFIDENTIALITY_EXTENSIVE_NON_SENSITIVE, "Extensive non-sensitive data disclosed (%s)" %
         CONFIDENTIALITY_EXTENSIVE_NON_SENSITIVE),
        (CONFIDENTIALITY_EXTENSIVE_CRITICAL, "Extensive critical data disclosed (%s)" %
         CONFIDENTIALITY_EXTENSIVE_CRITICAL),
        (CONFIDENTIALITY_ALL_DATA, "All data disclosed (%s)" % CONFIDENTIALITY_ALL_DATA)
    ]

    INTEGRITY_MINIMAL_SLIGHTLY = 1
    INTEGRITY_MINIMAL_SERIOUSLY = 3
    INTEGRITY_EXTENSIVE_SLIGHTLY = 5
    INTEGRITY_EXTENSIVE_SERIOUSLY = 7
    INTEGRITY_ALL_DATA = 9

    INTEGRITY_CHOICES = [
        (INTEGRITY_MINIMAL_SLIGHTLY, "Minimal slightly corrupt data (%s)" % INTEGRITY_MINIMAL_SLIGHTLY),
        (INTEGRITY_MINIMAL_SERIOUSLY, "Minimal seriously corrupt data (%s)" % INTEGRITY_MINIMAL_SERIOUSLY),
        (INTEGRITY_EXTENSIVE_SLIGHTLY, "Extensive slightly corrupt data (%s)" % INTEGRITY_EXTENSIVE_SLIGHTLY),
        (INTEGRITY_EXTENSIVE_SERIOUSLY, "Extensive seriously corrupt data (%s)" % INTEGRITY_EXTENSIVE_SERIOUSLY),
        (INTEGRITY_ALL_DATA, "All data totally corrupt (%s)" % INTEGRITY_ALL_DATA)
    ]

    AVAILABILITY_MINIMAL_SECONDARY = 1
    AVAILABILITY_MINIMAL_PRIMARY = 5
    AVAILABILITY_EXTENSIVE_SECONDARY = 5
    AVAILABILITY_EXTENSIVE_PRIMARY = 7
    AVAILABILITY_ALL_SERVICES = 9

    AVAILABILITY_CHOICES = [
        (AVAILABILITY_MINIMAL_SECONDARY, "Minimal secondary services interrupted (%s)" %
         AVAILABILITY_MINIMAL_SECONDARY),
        (AVAILABILITY_MINIMAL_PRIMARY, "Minimal primary services interrupted (%s)" % AVAILABILITY_MINIMAL_PRIMARY),
        (AVAILABILITY_EXTENSIVE_SECONDARY, "Extensive secondary services interrupted (%s)" %
         AVAILABILITY_EXTENSIVE_SECONDARY),
        (AVAILABILITY_EXTENSIVE_PRIMARY, "Extensive primary services interrupted (%s)" %
         AVAILABILITY_EXTENSIVE_PRIMARY),
        (AVAILABILITY_ALL_SERVICES, "All services completely list (%s)" % AVAILABILITY_ALL_SERVICES)
    ]

    ACCOUNTABILITY_FULLY = 1
    ACCOUNTABILITY_POSSIBLY = 7
    ACCOUNTABILITY_ANONYMOUS = 9

    ACCOUNTABILITY_CHOICES = [
        (ACCOUNTABILITY_FULLY, "Fully traceable (%s)" % ACCOUNTABILITY_FULLY),
        (ACCOUNTABILITY_POSSIBLY, "Possibly traceable (%s)" % ACCOUNTABILITY_POSSIBLY),
        (ACCOUNTABILITY_ANONYMOUS, "Completely anonymous (%s)" % ACCOUNTABILITY_ANONYMOUS)
    ]

    FINANCIAL_LESS = 1
    FINANCIAL_MINOR = 3
    FINANCIAL_SIGNIFICANT = 7
    FINANCIAL_BANKRUPTCY = 9
    FINANCIAL_DAMAGE_CHOICES = [
        (FINANCIAL_LESS, "Less than the cost to fix the vulnerability (%s)" % FINANCIAL_LESS),
        (FINANCIAL_MINOR, "Minor effect on annual profit (%s)" % FINANCIAL_MINOR),
        (FINANCIAL_SIGNIFICANT, "Significant effect on annual profit (%s)" % FINANCIAL_SIGNIFICANT),
        (FINANCIAL_BANKRUPTCY, "Bankruptcy (%s)" % FINANCIAL_BANKRUPTCY)
    ]

    REPUTATION_MINIMAL = 1
    REPUTATION_MAJOR = 4
    REPUTATION_GOODWILL = 5
    REPUTATION_BRAND = 9
    REPUTATION_DAMAGE_CHOICES = [
        (REPUTATION_MINIMAL, "Minimal damage (%s)" % REPUTATION_MINIMAL),
        (REPUTATION_MAJOR, "Loss of major accounts (%s)" % REPUTATION_MAJOR),
        (REPUTATION_GOODWILL, "Loss of goodwill (%s)" % REPUTATION_GOODWILL),
        (REPUTATION_BRAND, "Brand damage (%s)" % REPUTATION_BRAND)
    ]

    COMPLIANCE_MINOR = 2
    COMPLIANCE_CLEAR = 5
    COMPLIANCE_HIGH = 7
    NON_COMPLIANCE_CHOICES = [
        (COMPLIANCE_MINOR, "Minor violation (%s)" % COMPLIANCE_MINOR),
        (COMPLIANCE_CLEAR, "Clear violation (%s)" % COMPLIANCE_CLEAR),
        (COMPLIANCE_HIGH, "High profile violation (%s)" % COMPLIANCE_HIGH)
    ]

    PRIVACY_ONE = 3
    PRIVACY_HUNDREDS = 5
    PRIVACY_THOUSANDS = 7
    PRIVACY_MILLIONS = 9
    PRIVACY_VIOLATION_CHOICES = [
        (PRIVACY_ONE, "One individual (%s)" % PRIVACY_ONE),
        (PRIVACY_HUNDREDS, "Hundreds of people (%s)" % PRIVACY_HUNDREDS),
        (PRIVACY_THOUSANDS, "Thousands of people (%s)" % PRIVACY_THOUSANDS),
        (PRIVACY_MILLIONS, "Millions of people (%s)" % PRIVACY_MILLIONS)
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    vulnerability = models.OneToOneField('findings.Vulnerability', on_delete=models.CASCADE)
    skills_required = models.PositiveIntegerField(choices=SKILLS_REQUIRED_CHOICES,
                                                  help_text="How technically skilled is this group of threat agents?")
    motive = models.PositiveIntegerField(choices=MOTIVE_CHOICES,
                                         help_text="How motivated is this group of threat agents to find and exploit"
                                                   " this vulnerability?")
    opportunity = models.PositiveIntegerField(choices=OPPORTUNITY_CHOICES,
                                              help_text="What resources and opportunities are required for this group "
                                                        "of threat agents to find and exploit this vulnerability?")
    population_size = models.PositiveIntegerField(choices=POPULATION_SIZE_CHOICES,
                                                  help_text="How large is this group of threat agents?")
    ease_of_discovery = models.PositiveIntegerField(choices=EASE_OF_DISCOVERY_CHOICES,
                                                    help_text="How easy is it for this group of threat agents to "
                                                              "discover this vulnerability? ")
    ease_of_exploit = models.PositiveIntegerField(choices=EASE_OF_EXPLOIT_CHOICES,
                                                  help_text="How easy is it for this group of threat agents to actually"
                                                            " exploit this vulnerability? ")
    awareness = models.PositiveIntegerField(choices=AWARENESS_CHOICES,
                                            help_text="How well known is this vulnerability to this group of threat "
                                                      "agents?")
    intrusion_detection = models.PositiveIntegerField(choices=INTRUSION_DETECTION_CHOICES,
                                                      help_text="How likely is an exploit to be detected?")
    loss_of_confidentiality = models.PositiveIntegerField(choices=CONFIDENTIALITY_CHOICES,
                                                          help_text="How much data could be disclosed and how "
                                                                    "sensitive is it?")
    loss_of_integrity = models.PositiveIntegerField(choices=INTEGRITY_CHOICES,
                                                    help_text="How much data could be corrupted and how damaged is it?")
    loss_of_availability = models.PositiveIntegerField(choices=AVAILABILITY_CHOICES,
                                                       help_text="How much service could be lost and how vital is it?")
    loss_of_accountability = models.PositiveIntegerField(choices=ACCOUNTABILITY_CHOICES,
                                                         help_text="Are the threat agents’ actions traceable to an "
                                                                   "individual?")
    financial_damage = models.PositiveIntegerField(choices=FINANCIAL_DAMAGE_CHOICES,
                                                   help_text="How much financial damage will result from an exploit?")
    reputation_damage = models.PositiveIntegerField(choices=REPUTATION_DAMAGE_CHOICES,
                                                    help_text="Would an exploit result in reputation damage that would "
                                                              "harm the business?")
    non_compliance = models.PositiveIntegerField(choices=NON_COMPLIANCE_CHOICES,
                                                 help_text="How much exposure does non-compliance introduce?")
    privacy_violation = models.PositiveIntegerField(choices=PRIVACY_VIOLATION_CHOICES,
                                                    help_text="How much personally identifiable information could be "
                                                              "disclosed?")

    @property
    def thread_agent_factor(self):
        factors = self.skills_required + self.motive + self.opportunity + self.population_size
        return factors / 4.0

    @property
    def vulnerability_factor(self):
        factors = self.ease_of_discovery + self.ease_of_exploit + self.awareness + self.intrusion_detection
        return factors / 4.0

    @property
    def technical_impact_factor(self):
        factors = self.loss_of_confidentiality + self.loss_of_integrity + self.loss_of_availability + \
                  self.loss_of_accountability
        return factors / 4.0

    @property
    def business_impact_factor(self):
        factors = self.financial_damage + self.reputation_damage + self.non_compliance + self.privacy_violation
        return factors / 4.0

    @property
    def likelihood_score(self):
        factors = (self.thread_agent_factor + self.vulnerability_factor) / 2.0
        if factors < 3:
            risk = self.RISK_LOW
        elif factors < 6:
            risk = self.RISK_MEDIUM
        elif factors < 9:
            risk = self.RISK_HIGH
        else:
            risk = None
        return factors, risk

    def is_configured(self):
        if self.impact_score is None:
            return False
        if self.likelihood_score[1] is None:
            return False
        return True

    @property
    def impact_score(self):
        factors = (self.technical_impact_factor + self.business_impact_factor) / 2.0
        if factors < 3:
            return factors, self.RISK_LOW
        elif factors < 6:
            return factors, self.RISK_MEDIUM
        elif factors < 9:
            return factors, self.RISK_HIGH
        return None

    @property
    def overall_risk_severity(self):
        # FIXME: ugly and needs improvement.
        impact = self.impact_score
        likelihood = self.likelihood_score
        if impact[0] < 3:
            if likelihood[1] == self.RISK_LOW:
                return self.RISK_INFORMATIONAL
            elif likelihood[1] == self.RISK_MEDIUM:
                return self.RISK_LOW
            elif likelihood[1] == self.RISK_HIGH:
                return self.RISK_MEDIUM
        elif impact[0] < 6:
            if likelihood[1] == self.RISK_LOW:
                return self.RISK_LOW
            elif likelihood[1] == self.RISK_MEDIUM:
                return self.RISK_MEDIUM
            elif likelihood[1] == self.RISK_HIGH:
                return self.RISK_HIGH
        elif impact[0] < 9:
            if likelihood[1] == self.RISK_LOW:
                return self.RISK_MEDIUM
            elif likelihood[1] == self.RISK_MEDIUM:
                return self.RISK_HIGH
            elif likelihood[1] == self.RISK_HIGH:
                return self.RISK_CRITICAL
        raise Exception("This should not happen!")

    @property
    def vector(self):
        likelihood = "SL:{sl}/M:{m}/O:{o}/S:{s}/ED:{ed}/EE:{ee}/A:{a}/ID:{id}".format(
            sl=self.skills_required, m=self.motive, o=self.opportunity, s=self.population_size,
            ed=self.ease_of_discovery, ee=self.ease_of_exploit, a=self.awareness, id=self.intrusion_detection)
        impact = "LC:{lc}/LI:{li}/LAV:{lav}/LAC:{lac}/FD:{fd}/RD:{rd}/NC:{nc}/PV:{pv}".format(
            lc=self.loss_of_confidentiality, li=self.loss_of_integrity, lav=self.loss_of_availability,
            lac=self.loss_of_accountability, fd=self.financial_damage, rd=self.reputation_damage,
            nc=self.non_compliance, pv=self.privacy_violation
        )
        return "(%s/%s)" % (likelihood, impact)


class CVSScore(models.Model):
    # Attack Vector
    CVSS_AV_NETWORK = "N"
    CVSS_AV_ADJACENT = "A"
    CVSS_AV_LOCAL = "L"
    CVSS_AV_PHYSICAL = "P"
    CVSS_AV_CHOICES = [
        (CVSS_AV_NETWORK, "Network (N)"), (CVSS_AV_PHYSICAL, "Physical (P)"),
        (CVSS_AV_ADJACENT, "Adjacent (A)", )
    ]

    # Attack Complexity
    CVSS_AC_LOW = "L"
    CVSS_AC_HIGH = "H"
    CVSS_AC_CHOICES = [
        (CVSS_AC_LOW, "Low (L)"), (CVSS_AC_HIGH, "High (H)")
    ]

    # Privileges Required
    CVSS_PR_NONE = "N"
    CVSS_PR_LOW = "L"
    CVSS_PR_HIGH = "H"
    CVSS_PR_CHOICES = [
        (CVSS_PR_NONE, "None (N)"), (CVSS_PR_LOW, "Low (L)"), (CVSS_PR_HIGH, "High (H)")
    ]

    # User Interaction
    CVSS_UI_NONE = "N"
    CVSS_UI_REQUIRED = "R"
    CVSS_UI_CHOICES = [
        (CVSS_UI_NONE, "None (N)"), (CVSS_UI_REQUIRED, "Required (R)")
    ]

    # Scope
    CVSS_S_UNCHANGED = "U"
    CVSS_S_CHANGED = "C"
    CVSS_S_CHOICES = [
        (CVSS_S_UNCHANGED, "Unchanged (U)"), (CVSS_S_CHANGED, "Changed (C)")
    ]
    # Confidentiality
    CVSS_C_NONE = "N"
    CVSS_C_LOW = "L"
    CVSS_C_HIGH = "H"
    CVSS_C_CHOICES = [
        (CVSS_C_NONE, "None (N)"), (CVSS_C_LOW, "Low (L)"), (CVSS_C_HIGH, "High (H)")
    ]

    # Integrity
    CVSS_I_NONE = "N"
    CVSS_I_LOW = "L"
    CVSS_I_HIGH = "H"
    CVSS_I_CHOICES = [
        (CVSS_I_NONE, "None (N)"), (CVSS_I_LOW, "Low (L)"), (CVSS_I_HIGH, "High (H)")
    ]

    # Availability
    CVSS_A_NONE = "N"
    CVSS_A_LOW = "L"
    CVSS_A_HIGH = "H"
    CVSS_A_CHOICES = [
        (CVSS_A_NONE, "None (N)"), (CVSS_A_LOW, "Low (L)"), (CVSS_A_HIGH, "High (H)")
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    vulnerability = models.OneToOneField('findings.Vulnerability', on_delete=models.CASCADE)
    attack_vector = models.CharField(max_length=3, choices=CVSS_AV_CHOICES, blank=True, null=True)
    attack_complexity = models.CharField(max_length=3, choices=CVSS_AC_CHOICES, blank=True, null=True)
    privilege_required = models.CharField(max_length=3, choices=CVSS_PR_CHOICES, blank=True, null=True)
    user_interaction = models.CharField(max_length=3, choices=CVSS_UI_CHOICES, blank=True, null=True)
    scope = models.CharField(max_length=3, choices=CVSS_S_CHOICES, blank=True, null=True)
    confidentiality = models.CharField(max_length=3, choices=CVSS_C_CHOICES, blank=True, null=True)
    integrity = models.CharField(max_length=3, choices=CVSS_I_CHOICES, blank=True, null=True)
    availability = models.CharField(max_length=3, choices=CVSS_A_CHOICES, blank=True, null=True)

    @property
    def vector(self):
        values = [
            "CVSS:3.1", "AV:%s" % self.attack_vector, "AC:%s" % self.attack_complexity,
            "PR:%s" % self.privilege_required, "UI:%s" % self.user_interaction, "S:%s" % self.scope,
            "C:%s" % self.confidentiality, "I:%s" % self.integrity, "A:%s" % self.availability
        ]
        return "/".join(values)

    def get_severity(self):
        # TODO: use vulnerability.SEVERITY_CHOICES instead
        return cvss.CVSS3(self.vector).severities()[0]

    def get_base_score(self):
        try:
            return cvss.CVSS3(self.vector).scores()[0]
        except:
            return None

    def is_configured(self):
        if not self.get_base_score():
            return False
        return True
