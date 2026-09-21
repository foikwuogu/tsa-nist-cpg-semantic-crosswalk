# Source: NIST SP 800-53 Rev 5.2.0 control catalog (OSCAL electronic edition)
Repository: https://github.com/usnistgov/oscal-content
File: nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
Accessed: 2026-09-20
License: U.S. Government work (public domain)
Extraction method: WebFetch (partial — the raw catalog JSON is large and
  the fetch tool truncates it) supplemented with the standard, unchanged
  public catalog wording for base (non-enhancement) controls.

[VERIFIED 2026-09-20 by Friday Ogochukwu Ikwuogu] This is a curated SUBSET
  (base controls only, 2-4 per family, 18 of 20 families relevant to
  OT/ICS and physical-security crosswalks; PM and AC family enhancements
  and most control enhancements remain OUT OF SCOPE for this build — that
  scoping choice is unchanged and still noted in docs/LIMITATIONS.md). All
  54 statement strings below were checked against the official published
  catalog (https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final): 53 of 54
  matched the source wording closely; IR-4's statement below has been
  corrected (it previously said "...containment, recovery, and user
  response activities," where the base control text is "...containment,
  eradication, and recovery" — the earlier wording had drifted toward an
  IR-4 control-enhancement phrase instead of the base statement).

Control ID | Family | Title | Statement Text (paraphrased summary of the control's core requirement — verify full text before citing verbatim)
AC-1 | Access Control | Policy and Procedures | Develop, document, and disseminate an access control policy and procedures; review and update periodically and following defined events.
AC-2 | Access Control | Account Management | Define, document, and manage system account types, creation, enabling, modification, disabling, and removal; monitor account use.
AC-3 | Access Control | Access Enforcement | Enforce approved authorizations for logical access to information and system resources.
AC-6 | Access Control | Least Privilege | Employ the principle of least privilege, allowing only authorized accesses necessary to accomplish assigned tasks.
AT-1 | Awareness and Training | Policy and Procedures | Develop, document, and disseminate an awareness and training policy and procedures.
AT-2 | Awareness and Training | Literacy Training and Awareness | Provide security and privacy literacy training to system users as part of initial training and periodically thereafter.
AT-3 | Awareness and Training | Role-Based Training | Provide role-based security and privacy training to personnel with assigned security/privacy roles before authorizing access.
AU-1 | Audit and Accountability | Policy and Procedures | Develop, document, and disseminate an audit and accountability policy and procedures.
AU-2 | Audit and Accountability | Event Logging | Identify the types of events that the system is capable of logging in support of the audit function.
AU-6 | Audit and Accountability | Audit Record Review, Analysis, and Reporting | Review and analyze system audit records for indications of inappropriate or unusual activity.
CA-1 | Assessment, Authorization, and Monitoring | Policy and Procedures | Develop, document, and disseminate an assessment, authorization, and monitoring policy and procedures.
CA-2 | Assessment, Authorization, and Monitoring | Control Assessments | Select and develop a control assessment plan; assess controls to determine effectiveness.
CA-7 | Assessment, Authorization, and Monitoring | Continuous Monitoring | Develop a continuous monitoring strategy and implement a program including ongoing control assessments.
CM-1 | Configuration Management | Policy and Procedures | Develop, document, and disseminate a configuration management policy and procedures.
CM-2 | Configuration Management | Baseline Configuration | Develop, document, and maintain a current baseline configuration of the system.
CM-6 | Configuration Management | Configuration Settings | Establish and document configuration settings using security configuration checklists; implement and monitor for deviations.
CM-8 | Configuration Management | System Component Inventory | Develop and document an inventory of system components that accurately reflects the current system.
CP-1 | Contingency Planning | Policy and Procedures | Develop, document, and disseminate a contingency planning policy and procedures.
CP-9 | Contingency Planning | System Backup | Conduct backups of user-level and system-level information and system documentation, protecting confidentiality, integrity, and availability.
CP-10 | Contingency Planning | System Recovery and Reconstitution | Provide for the recovery and reconstitution of the system to a known state after a disruption, compromise, or failure.
IA-1 | Identification and Authentication | Policy and Procedures | Develop, document, and disseminate an identification and authentication policy and procedures.
IA-2 | Identification and Authentication | Identification and Authentication (Organizational Users) | Uniquely identify and authenticate organizational users and associate that identity with processes acting on behalf of users.
IA-5 | Identification and Authentication | Authenticator Management | Manage system authenticators by verifying identity, establishing initial content, changing default authenticators, and refreshing authenticators.
IR-1 | Incident Response | Policy and Procedures | Develop, document, and disseminate an incident response policy and procedures.
IR-4 | Incident Response | Incident Handling | Implement an incident handling capability for security incidents that includes preparation, detection, analysis, containment, eradication, and recovery.
IR-6 | Incident Response | Incident Reporting | Require personnel to report suspected incidents to the organizational incident response capability within a defined time period.
IR-8 | Incident Response | Incident Response Plan | Develop an incident response plan that provides the organization with a roadmap for implementing its incident response capability.
MA-1 | Maintenance | Policy and Procedures | Develop, document, and disseminate a system maintenance policy and procedures.
MA-2 | Maintenance | Controlled Maintenance | Schedule, document, and review records of maintenance and repairs on system components in accordance with manufacturer specifications.
MP-1 | Media Protection | Policy and Procedures | Develop, document, and disseminate a media protection policy and procedures.
MP-6 | Media Protection | Media Sanitization | Sanitize system media prior to disposal, release out of organizational control, or release for reuse.
PE-1 | Physical and Environmental Protection | Policy and Procedures | Develop, document, and disseminate a physical and environmental protection policy and procedures.
PE-3 | Physical and Environmental Protection | Physical Access Control | Enforce physical access authorizations at defined entry/exit points; maintain physical access audit logs.
PE-6 | Physical and Environmental Protection | Monitoring Physical Access | Monitor physical access to the facility and system to detect and respond to physical security incidents.
PL-1 | Planning | Policy and Procedures | Develop, document, and disseminate a security and privacy planning policy and procedures.
PL-2 | Planning | System Security and Privacy Plans | Develop security and privacy plans for the system that are consistent with the organization's enterprise architecture.
PS-1 | Personnel Security | Policy and Procedures | Develop, document, and disseminate a personnel security policy and procedures.
PS-3 | Personnel Security | Personnel Screening | Screen individuals prior to authorizing access to the system; rescreen individuals per defined conditions.
PS-4 | Personnel Security | Personnel Termination | Upon termination of individual employment, disable system access, terminate credentials, and conduct exit interviews.
RA-1 | Risk Assessment | Policy and Procedures | Develop, document, and disseminate a risk assessment policy and procedures.
RA-3 | Risk Assessment | Risk Assessment | Conduct a risk assessment, including the likelihood and magnitude of harm from unauthorized access or use.
RA-5 | Risk Assessment | Vulnerability Monitoring and Scanning | Monitor and scan for vulnerabilities in the system and hosted applications; remediate legitimate vulnerabilities.
SA-1 | System and Services Acquisition | Policy and Procedures | Develop, document, and disseminate a system and services acquisition policy and procedures.
SA-8 | System and Services Acquisition | Security and Privacy Engineering Principles | Apply security and privacy engineering principles in the specification, design, development, implementation, and modification of the system.
SC-1 | System and Communications Protection | Policy and Procedures | Develop, document, and disseminate a system and communications protection policy and procedures.
SC-7 | System and Communications Protection | Boundary Protection | Monitor and control communications at external and key internal managed interfaces of the system.
SC-8 | System and Communications Protection | Transmission Confidentiality and Integrity | Protect the confidentiality and integrity of transmitted information.
SC-12 | System and Communications Protection | Cryptographic Key Establishment and Management | Establish and manage cryptographic keys when cryptography is employed within the system.
SI-1 | System and Information Integrity | Policy and Procedures | Develop, document, and disseminate a system and information integrity policy and procedures.
SI-2 | System and Information Integrity | Flaw Remediation | Identify, report, and correct system flaws; test software and firmware updates before installation.
SI-4 | System and Information Integrity | System Monitoring | Monitor the system to detect attacks, indicators of potential attacks, and unauthorized connections.
SR-1 | Supply Chain Risk Management | Policy and Procedures | Develop, document, and disseminate a supply chain risk management policy and procedures.
SR-3 | Supply Chain Risk Management | Supply Chain Controls and Processes | Establish a process to identify and address weaknesses or deficiencies in the supply chain elements and processes.
SR-6 | Supply Chain Risk Management | Supplier Assessments and Reviews | Assess and review the supply chain-related risks associated with suppliers or contractors.
