# Change these three lines (plus DOMAINS and GROUPS) to build a practice exam for another certification.
EXAM = "SC-500"
EXAM_TITLE = "Implementing End-to-End Security Controls for Cloud and AI Workloads"
STUDY_GUIDE = "https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-500"

# Source: STUDY_GUIDE (fetched 2026-11-10)
# Allocation: D1 123 (25%), D2 139 (28%), D3 116 (23%), D4 122 (24%) = 500,
# midpoints of the official weight ranges (22.5 / 27.5 / 22.5 / 22.5), rounded per group.
DOMAINS = {
    "1": ("Manage identity, access, and governance", "20-25%"),
    "2": ("Secure storage, databases, and networking", "25-30%"),
    "3": ("Secure compute", "20-25%"),
    "4": ("Manage and monitor security posture", "20-25%"),
}
# group id: (title, questions per objective, objectives)
GROUPS = {
    "1.1": ("Secure access to resources by using Microsoft Entra ID", 6, [
        "Implement and configure Privileged Identity Management (PIM)",
        "Implement conditional access policies",
        "Implement and configure authentication methods, including multifactor authentication (MFA) and passwordless",
        "Implement and configure identity for applications, including enterprise applications and app registrations",
        "Manage OAuth permission grants and consent settings",
        "Implement and configure managed identities for Azure resources"]),
    "1.2": ("Secure secrets and keys by using Azure Key Vault", 6, [
        "Deploy Key Vault",
        "Configure Key Vault settings",
        "Configure access to Key Vault",
        "Configure firewall settings on Key Vault",
        "Manage keys, secrets, and certificates",
        "Scan for secrets by using Defender Cloud Security Posture Management (Defender CSPM)",
        "Implement Defender for Key Vault"]),
    "1.3": ("Implement governance to enforce security and regulatory compliance", 5, [
        "Implement and configure security controls by using Azure Policy, including built-in and custom policy definitions",
        "Evaluate regulatory compliance by using Microsoft Defender for Cloud",
        "Implement and configure security controls in Defender for Cloud, including security standards and recommendations",
        "Implement resource locks",
        "Manage Azure built-in role assignments",
        "Manage custom roles, including Azure roles and Microsoft Entra roles",
        "Evaluate and remediate overprivileged access assignments by using Azure role-based access control (RBAC)",
        "Configure security controls for backup protection by using Azure Backup security features",
        "Implement and configure security controls by using infrastructure as code"]),
    "2.1": ("Implement security for storage accounts", 10, [
        "Implement and configure security for storage accounts",
        "Configure Azure Storage firewall rules",
        "Implement Defender for Storage threat protection configurations",
        "Manage access to storage, including access policies"]),
    "2.2": ("Implement security for databases", 9, [
        "Implement platform-level security configurations in Azure SQL",
        "Configure database auditing for Azure SQL Database and Azure SQL Managed Instance",
        "Configure Defender for Databases protection across Azure database services"]),
    "2.3": ("Implement security for Azure network services", 8, [
        "Implement and manage network security groups (NSGs) and application security groups (ASGs)",
        "Implement and configure network access policies by using Azure Virtual Network Manager",
        "Configure security for an Azure Virtual WAN",
        "Implement and configure security for virtual private network (VPN) connections",
        "Implement and configure Microsoft Entra Private Access",
        "Configure Azure private endpoints to secure access to Azure platform as a service (PaaS) resources",
        "Configure Azure Private Link services to secure access to network resources",
        "Implement and configure Azure Firewall",
        "Evaluate effective security rules by using Azure Network Watcher diagnostics"]),
    "3.1": ("Implement security for AI", 4, [
        "Identify overexposure of data in SharePoint",
        "Identify risks related to Microsoft Copilot and AI apps by using Microsoft Purview Data Security Posture Management (DSPM)",
        "Enable and configure real-time protection for Microsoft Copilot Studio agents",
        "Implement conditional access for Microsoft Entra Agent ID",
        "Analyze blast radius for security risks related to Entra Agent ID by using Defender XDR",
        "Manage Entra Agent ID access",
        "Configure and deploy AI Gateway in Azure API Management for Microsoft Foundry",
        "Enable Defender for AI Service in Cloud Workload Protection in Defender for Cloud",
        "Configure guardrails for agent security in Foundry",
        "Monitor AI security by using the Data and AI security dashboard in Defender for Cloud",
        "Manage agents in Microsoft 365 admin center"]),
    "3.2": ("Implement security for servers and virtual machines (VMs)", 4, [
        "Implement and configure disk encryption",
        "Plan and implement Azure Bastion",
        "Enable and enforce use of just-in-time (JIT) VM access",
        "Extend security controls to hybrid and multicloud servers by using Azure Arc",
        "Onboard servers to Defender for Servers in Defender for Cloud, including hybrid and multicloud scenarios",
        "Configure Defender for Servers settings, including vulnerability scanning, and endpoint detection and response (EDR)",
        "Implement and manage agentless scanning for VMs in Defender for Servers",
        "Configure security features on a VM, including secure boot, virtual Trusted Platform Module (vTPM), integrity monitoring, and security type",
        "Enforce security configuration of Azure-managed servers by using Azure Machine Configuration"]),
    "3.3": ("Implement security for application platform services", 4, [
        "Detect misconfigurations and runtime risks in container workloads by using Defender for Containers",
        "Implement and configure security controls for Azure Kubernetes Service (AKS)",
        "Implement and configure security controls for Azure Container Registry",
        "Implement and configure security controls for Azure Container Instances and Azure Container Apps",
        "Implement and configure security controls for Azure Functions, including authentication and network access",
        "Implement and configure security controls for Azure Logic Apps",
        "Implement and configure security controls for Azure App Service",
        "Implement and configure Azure Web Application Firewall",
        "Implement security policies for back-end API protection by using API Management"]),
    "4.1": ("Manage security posture by using Defender for Cloud", 6, [
        "Identify security risks by using Defender CSPM",
        "Evaluate compliance against security frameworks by using Defender for Cloud",
        "Enable and configure Defender for Cloud workload protection plans",
        "Connect hybrid cloud and multicloud environments to Defender for Cloud, including Amazon Web Services (AWS) and Google Cloud Platform (GCP)",
        "Configure Microsoft Defender Vulnerability Management settings for Azure VMs",
        "Discover unprotected assets and vulnerabilities by using Microsoft Defender External Attack Surface Management (EASM)"]),
    "4.2": ("Implement activity and event collection in Microsoft Sentinel", 6, [
        "Create and connect workspaces in Microsoft Sentinel",
        "Assign roles in Microsoft Sentinel",
        "Implement and use content hub solutions",
        "Configure and use Microsoft data connectors for Azure resources",
        "Implement and configure syslog and Common Event Format (CEF) event collections",
        "Implement and configure collection of Windows Security events by using data collection rules, including Windows Event Forwarding (WEF)",
        "Create custom log tables in the workspace to store ingested data",
        "Implement automation rules and playbooks in Microsoft Sentinel",
        "Implement data retention in Microsoft Sentinel data stores",
        "Query Microsoft Purview Audit in Defender XDR"]),
    "4.3": ("Implement Microsoft Security Copilot", 5, [
        "Configure workspaces for Security Copilot",
        "Manage permissions and roles in Security Copilot",
        "Enable and configure plugins",
        "Enable and configure Microsoft agents and Security Store agents"]),
}
TOTAL = 500  # question bank size; validate.py and build.py check against it
# Exceptions to the per-group count so the total is exactly TOTAL.
OVERRIDE = {
    "2.2.1": 9, "2.2.2": 9, "2.2.3": 9,
    "4.3.1": 7, "4.3.2": 7, "4.3.3": 6, "4.3.4": 6,
}


def objectives():
    """{objective id: (text, target count)}"""
    out = {}
    for g, (_, n, objs) in GROUPS.items():
        for i, text in enumerate(objs, 1):
            oid = f"{g}.{i}"
            out[oid] = (text, OVERRIDE.get(oid, n))
    return out


if __name__ == "__main__":
    o = objectives()
    by_dom = {d: sum(n for k, (_, n) in o.items() if k[0] == d) for d in DOMAINS}
    print(len(o), "objectives,", sum(n for _, n in o.values()), "questions", by_dom)
    assert sum(n for _, n in o.values()) == TOTAL
    for g, (title, n, objs) in GROUPS.items():
        print(g, title, [o[f"{g}.{i}"][1] for i in range(1, len(objs) + 1)])
