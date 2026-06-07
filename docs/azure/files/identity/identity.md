# Identity & Access

## Entra ID (Azure AD) Concepts

| Concept | Description |
| --- | --- |
| **Tenant** | Dedicated Entra ID instance for org |
| **User** | Human identity |
| **Service Principal** | App identity (manual credential management) |
| **Managed Identity** | Azure-managed service principal — no credentials |
| **System-Assigned MI** | Tied to resource lifecycle, auto-deleted |
| **User-Assigned MI** | Independent lifecycle, shared across resources |
| **Groups** | Security or M365, for role assignment |
| **App Registration** | Define an application in Entra ID |

### System Identity Type Decision Flow

```mermaid
--8<-- "azure/diagrams/identity/system-identity-type-decision-flow.mmd"
```

> **Exam tip:** Prefer Managed Identity over Service Principal whenever the
> workload runs in Azure and supports Entra-based managed identity auth.

## Entra Identity Scenarios

| Scenario | Solution | Tenant Type |
| --- | --- | --- |
| Employee / workforce identity | Entra ID (workforce tenant) | Workforce |
| Partner / vendor B2B access | Entra B2B (guest users) | Workforce |
| Customer-facing app identity | Entra External ID (external tenant) | External / CIAM |

> **Exam tip:** Entra External ID is the successor to Azure AD B2C for new customer identity
> (CIAM) projects. Existing B2C tenants continue to be supported, but new designs should target
> Entra External ID (external tenant). Do not confuse B2B guest users (workforce tenant) with
> External ID (separate external tenant).

### Entra Identity Scenario Decision Flow

```mermaid
--8<-- "azure/diagrams/identity/entra-identity-scenario-decision-flow.mmd"
```

## MSAL Authentication Flows (AZ-204)

| Service | Flow | Use Case | Key Feature |
| --- | --- | --- | --- |
| MSAL | Authorization Code + PKCE | Interactive sign-in from a browser SPA or native app | PKCE eliminates the need for a client secret in public clients; most secure interactive flow |
| MSAL | Client Credentials | Daemon or service-to-service call with no signed-in user | Uses app identity (client ID + secret or certificate); no user context |
| MSAL | On-Behalf-Of (OBO) | Middle-tier API calls a downstream API on behalf of the signed-in user | Middle tier exchanges its access token for a new token scoped to the downstream API |
| MSAL | Device Code | Input-constrained devices (CLI tools, smart TVs, IoT) | Device displays a code; user authenticates on a separate browser |

> **Exam tip:** On-behalf-of (OBO) is the correct flow when a middle-tier web API receives a token from a client and must call another downstream API using the signed-in user's identity — it propagates the user context through the call chain. Client credentials is for daemon apps or background services where no user is involved. Authorization code + PKCE is the secure flow for browser-based or native apps.

## DefaultAzureCredential Resolution Chain

`DefaultAzureCredential` (azure-identity) attempts credentials in the following order, stopping at the first that succeeds:

1. `EnvironmentCredential` — reads `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` / `AZURE_CLIENT_CERTIFICATE_PATH`, `AZURE_TENANT_ID`
2. `WorkloadIdentityCredential` — federated identity in Kubernetes (AKS workload identity)
3. `ManagedIdentityCredential` — Azure-hosted compute (App Service, Functions, VMs, ACI, AKS pod identity)
4. `VisualStudioCredential` — signed-in identity in Visual Studio (Windows)
5. `AzureCliCredential` — `az login` credential on the local machine
6. `AzurePowerShellCredential` — `Connect-AzAccount` credential
7. `InteractiveBrowserCredential` — browser-based interactive login (disabled by default in `DefaultAzureCredential`)

> **Exam tip:** `DefaultAzureCredential` lets the same application code run locally (resolves to Azure CLI credentials via `az login`) and in production on Azure (resolves to the managed identity assigned to the hosting resource) without any environment-specific branching or secret management. This is the recommended pattern for all Azure SDK clients.

## App Registration: Scopes vs Application Roles

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| Delegated Scopes (OAuth2 Permissions) | Permission Type | APIs called on behalf of a signed-in user | Require user consent or admin pre-consent; user identity is present in the token |
| Application Roles (App Permissions) | Permission Type | Daemon apps and service-to-service calls with no user context | Granted to the app's own identity; used with the client credentials flow; require admin consent |

> **Exam tip:** Delegated scopes (OAuth2 permissions) require a signed-in user — the token contains both the user and the app identity. Application roles (app permissions) are assigned to the application's own service principal and are used in the client credentials flow where no user is present. If the scenario describes a background job, scheduler, or daemon calling an API, the answer is application roles + client credentials.

## Hybrid Identity

| Service | Purpose | Protocol | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Entra Connect** | Sync on-prem AD identities to Entra ID | LDAP → OAuth/OIDC | Hybrid orgs needing SSO across on-prem and cloud | Password hash sync, pass-through auth, federation |
| **Entra Domain Services** | Managed domain services in Azure (no DCs to run) | LDAP / Kerberos / NTLM | Lift-and-shift apps requiring legacy auth in Azure | Fully managed, integrates with Entra ID tenant |
| **Entra ID-only** | Cloud-native identity with no on-prem dependency | OAuth 2.0 / OIDC / SAML | Greenfield cloud workloads | No infrastructure to manage |

> **Exam tip:** Choose Entra Domain Services when a lift-and-shift workload requires LDAP or
> Kerberos authentication in Azure and you do not want to deploy and manage domain controllers.
> Choose Entra Connect when the requirement is to sync existing on-premises Active Directory
> accounts to the cloud for SSO or hybrid authentication.

## RBAC

| Concept | Description |
| --- | --- |
| **Role Definition** | Set of allowed actions (e.g. Contributor) |
| **Role Assignment** | Assign role to principal at a scope |
| **Scope levels** | Management Group > Subscription > Resource Group > Resource |
| **Built-in roles** | Owner, Contributor, Reader, User Access Administrator |
| **Custom Roles** | Define your own action list |
| **Deny Assignments** | Block actions regardless of role (used by Blueprints) |

> **⚠️ Deprecation warning:** Vault Access Policies (Key Vault) and legacy Storage access
> policies are superseded by **Azure RBAC**. RBAC is Entra-native, auditable, and centrally
> managed. Migrate new and existing resources to RBAC.

## PIM Key Concepts

| Feature | Detail |
| --- | --- |
| **Eligible Assignment** | Role not active until user activates |
| **Active Assignment** | Role always active |
| **Activation** | User requests role, optionally requires MFA + justification |
| **Approval Workflow** | Require approver before activation |
| **Access Reviews** | Periodic certify that users still need roles |

> **Exam tip (AZ-500):** AZ-500 tests PIM activation depth — know the difference
> between eligible (requires activation) and active (always on) role assignments.
> Access Reviews are the recurring compliance mechanism; PIM is the just-in-time
> access mechanism. Conditional Access is the Zero Trust policy enforcement point
> — combine it with Identity Protection risk signals to auto-block risky sign-ins.

## Entra ID Join Types

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Entra ID Join (AAD Join)** | Cloud-only join | New cloud-only devices | No on-prem dependency; MDM enrolled |
| **Hybrid Entra ID Join** | Hybrid join | Existing domain-joined devices | Joined to both on-prem AD and Entra ID |
| **Entra ID Registered** | Personal device | BYOD | Minimal IT control; user account registered |

> **Exam tip:** Hybrid Entra ID Join requires line-of-sight to a domain controller or Azure AD Connect for initial join. It is used for existing corporate devices that need both on-prem GPO and cloud SSO.

### Entra ID Join Type Decision Flow

```mermaid
--8<-- "azure/diagrams/identity/entra-id-join-type-decision-flow.mmd"
```

## RBAC Built-in Roles

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Owner** | Full control | Any | Full resource management including access | Can assign roles; includes all Contributor perms |
| **Contributor** | Resource management | Any | Create and manage resources | Cannot assign roles or manage access |
| **Reader** | Read-only | Any | View resources, audit, monitoring | No create/update/delete; no role assignments |
| **User Access Administrator** | Access management | Any | Manage role assignments only | Cannot modify resources; only access control |

> **Exam tip:** User Access Administrator can grant Owner to others — this is a powerful role. Use it carefully and prefer just-in-time elevation via PIM over permanent assignment.

### RBAC Role Assignment Decision Flow

```mermaid
--8<-- "azure/diagrams/identity/rbac-role-assignment-decision-flow.mmd"
```
