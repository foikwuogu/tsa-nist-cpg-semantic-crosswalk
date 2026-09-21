# Source: CISA Cross-Sector Cybersecurity Performance Goals (CPG)
Version: 1.0.1
URL: https://www.cisa.gov/sites/default/files/2023-03/CISA_CPG_REPORT_v1.0.1_FINAL.pdf
Accessed: 2026-09-20
License: U.S. Government work (public domain)
Extraction method: WebFetch text extraction (structured ID/title/description list)

ID | Title | Description
1.A | Organizational Cybersecurity Leadership | A single leader is responsible and accountable for cybersecurity within an organization.
1.B | Asset Inventory | Maintain regularly updated inventory of all organizational assets with IP addresses, including OT, updated monthly.
1.C | OT Cybersecurity Leadership | A single leader is responsible and accountable for OT-specific cybersecurity within an organization.
1.D | Improving IT and OT Cybersecurity Relationships | Organizations sponsor at least one social gathering annually focused on strengthening relationships between IT and OT security personnel.
1.E | Mitigating Known Vulnerabilities | All known exploited vulnerabilities in internet-facing systems are patched or mitigated within a risk-informed timeframe.
1.F | Third-Party Validation | Third parties regularly validate cybersecurity defenses through penetration tests, bug bounties, or incident simulations.
1.G | Supply Chain Incident Reporting | Contracts stipulate vendors notify organizations of security incidents within a risk-informed timeframe.
1.H | Supply Chain Vulnerability Disclosure | Contracts require vendors notify organizations of confirmed security vulnerabilities within a risk-informed timeframe.
1.I | Vendor/Supplier Cybersecurity Requirements | Procurement documents include cybersecurity requirements evaluated during vendor selection.
2.A | Changing Default Passwords | Enforce organization-wide policy requiring changing default manufacturer passwords before deployment.
2.B | Minimum Password Strength | Enforce system policy requiring minimum password length of 15+ characters for IT and OT assets.
2.C | Unique Credentials | Provision unique and separate credentials for similar services; users cannot reuse passwords across accounts.
2.D | Revoking Credentials for Departing Employees | Enforce administrative process by employee departure date revoking physical access and disabling user accounts.
2.E | Separating User and Privileged Accounts | No user accounts have administrator privileges; administrators maintain separate accounts for non-administrative tasks.
2.F | Network Segmentation | All OT network connections denied by default; necessary IT-OT communications pass through monitored intermediary.
2.G | Detection of Unsuccessful Login Attempts | Log all unsuccessful logins and alert security teams after specific consecutive failed attempts occur.
2.H | Basic Cybersecurity Training | Provide at least annual training covering phishing, email compromise, operational security, and password practices.
2.I | OT Cybersecurity Training | Personnel securing OT receive specialized OT-focused cybersecurity training at least annually.
2.J | Strong and Agile Encryption | Deploy properly configured SSL/TLS protecting data in transit when technically feasible.
2.K | Phishing-Resistant MFA | Implement MFA using strongest available method, prioritizing hardware-based phishing-resistant options.
2.L | Disable Macros by Default | System-enforced policy disabling Microsoft Office macros by default on all devices.
2.M | Document Device Configurations | Maintain accurate documentation of baseline and current configuration details of all critical IT and OT assets.
2.N | Secure Sensitive Data | Sensitive data and credentials not stored in plaintext; accessible only by authenticated, authorized users.
2.O | Email Security | Enable STARTTLS, SPF, DKIM, and DMARC set to "reject" on all corporate email infrastructure.
2.P | Document Network Topology | Maintain accurate documentation of network topology across all IT and OT networks with periodic reviews.
2.Q | Hardware and Software Approval Process | Require approval before new hardware, firmware, or software installation; maintain allowlist of approved items.
2.R | System Backups | Regularly backup all systems necessary for operations at least annually; store separately and test annually.
2.S | Incident Response Plans | Maintain, practice, and update IT and OT cybersecurity incident response plans for threat scenarios annually.
2.T | Log Collection | Collect access and security-focused logs for detection and incident response; notify when critical sources disable.
2.U | Secure Log Storage | Store logs in central system accessible only by authorized, authenticated users; retain per risk guidelines.
2.V | Prohibit Connection of Unauthorized Devices | Maintain policies preventing unauthorized media and hardware connection via USB disabling or port securing.
2.W | No Exploitable Services on Internet | Assets on public internet expose no exploitable services; unnecessary OS applications and protocols disabled.
2.X | Limit OT Connections to Public Internet | No OT assets on public internet unless explicitly required; exceptions documented with additional protections.
3.A | Detecting Relevant Threats and TTPs | Document list of relevant threats and maintain ability to detect instances via rules, alerting, or prevention systems.
4.A | Vulnerability Disclosure/Reporting | Maintain public, discoverable method for security researchers to notify organizations of vulnerabilities.
4.B | Deploy Security.txt Files | All public-facing web domains have security.txt file conforming to RFC 9116 recommendations.
4.C | Incident Reporting | Maintain codified policy on reporting confirmed cybersecurity incidents to external entities and CISA.
5.A | Incident Planning and Preparedness | Develop, maintain, and execute plans to recover and restore mission-critical assets impacted by incidents.
