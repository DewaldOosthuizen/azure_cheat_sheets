# Networking

## Load Balancers

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure Load Balancer** | L4 (TCP/UDP) | Regional | Internal or public VM load balancing | Low latency, non-HTTP |
| **Application Gateway** | L7 (HTTP/S) | Regional | Web apps, URL-based routing | WAF, SSL termination, cookie affinity |
| **Azure Front Door** | L7 (HTTP/S) | Global | Multi-region web apps, CDN+WAF | Anycast, global routing, WAF, CDN |
| **Traffic Manager** | DNS-based | Global | Non-HTTP global routing, failover | DNS TTL-based, not a proxy |
| **API Management** | L7 (HTTP/S) | Regional/Global | API gateway, rate limiting, auth | Policies, developer portal, caching |

> **Exam tip:** SLA-focused wording is a strong discriminator in load-balancing questions.
> Prefer options that are explicitly SLA-backed for production workloads and note that
> SLA terms generally depend on correct multi-instance or multi-region design.

### Decision Flow

```mermaid
--8<-- "azure/diagrams/networking/decision-flow.mmd"
```

## API Management (APIM)

### Tier Comparison

| Tier | VNet Injection | Scale Units | Availability Zones | Primary Use Case |
| --- | --- | --- | --- | --- |
| Consumption | None | Serverless (auto) | No | Lightweight, event-driven APIs; no portal; cold-start |
| Developer | External / Internal | 1 (no scale-out) | No | Non-production, dev/test, full feature exploration |
| Basic | None | Up to 2 | No | Entry-level production; no VNet, limited SLA |
| Standard | External / Internal | Up to 4 | No | Production; VNet injection without AZ or multi-region |
| Premium | External / Internal | Up to 31 per region | Yes (multi-region) | Enterprise; multi-region gateways, AZs, private APIs |

> **v2 note:** Basic v2 and Standard v2 are GA. They offer faster provisioning and VNet integration via injection (Standard v2) but do not yet support all Premium features (multi-region, self-hosted gateway at scale). Use Premium v1/v2 for full enterprise requirements.

### Policy Evaluation Order

| Layer | Trigger | Typical Use |
| --- | --- | --- |
| Inbound | Every request on arrival at gateway | JWT validation, rate limiting, IP filtering, rewriting |
| Backend | Just before forwarding to backend | Load-balance, set backend URL, retry policy |
| Outbound | After backend response, before reply | Response transformation, header stripping, caching |
| On-Error | Any unhandled exception in the chain | Uniform error responses, logging, alerting |

### Decision Flow — API Gateway Selection

```mermaid
--8<-- "azure/diagrams/networking/decision-flow-api-gateway-selection.mmd"
```

> **Exam Tips**
>
> - Consumption tier is serverless — there is no VNet injection and there is a cold-start on the first call after idle. Choose it only when portal and VNet are not required.
> - Premium is the only tier that supports multi-region gateway deployment and availability zones. Any exam scenario requiring geo-redundant API exposure points to Premium.
> - Policy evaluation order matters: Inbound is the correct layer to validate JWTs and enforce auth before the request reaches the backend. Placing auth in Outbound is a common distractor.

## Virtual Networks (VNet)

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **VNet Peering** | L3 | Regional / Global | Same or cross-region VNet connectivity without a gateway | Low latency; no gateway required; non-transitive by default |
| **VNet-to-VNet VPN** | L3 | Global | Cross-region or cross-subscription encrypted connectivity | IPSec/IKE tunnel; older pattern superseded by peering in most cases |
| **ExpressRoute** | L3 | Global | Private dedicated circuit for enterprise workloads | SLA-backed; avoids public internet; supports up to 100 Gbps |
| **VPN Gateway** | L3 | Regional | On-premises to Azure encrypted tunnel | Site-to-site, point-to-site, and VNet-to-VNet; cost-effective |
| **Azure Bastion** | L7 | Regional | Secure browser-based RDP/SSH without public VM IPs | Deployed per VNet; no jump-box VM required |
| **Private Endpoint** | L3 | Regional | Private IP access to PaaS services inside a VNet | NIC injected into VNet; DNS integration required |
| **Service Endpoint** | L3 | Regional | Route PaaS traffic over Azure backbone from a subnet | No private IP; PaaS firewall can restrict to specific subnets |

> **⚠️ Deprecation warning:** VNet-to-VNet VPN is superseded by VNet Peering for most
> cross-region and cross-subscription connectivity scenarios. Prefer peering (lower latency,
> no gateway required). Retain VNet-to-VNet VPN only when IPSec encryption across the Azure
> backbone is an explicit requirement.

> **Private Endpoint vs Service Endpoint:**
>
> - Private Endpoint = PaaS resource gets a NIC in your VNet (true private)
> - Service Endpoint = traffic stays on Azure backbone but PaaS still has public IP

```mermaid
--8<-- "azure/diagrams/networking/virtual-networks-vnet.mmd"
```

> **Exam tip (AZ-700):** Prefer ExpressRoute over VPN Gateway when the requirement
> mentions dedicated bandwidth, consistent latency SLAs, or compliance mandates that
> prohibit public-internet traversal. VPN Gateway (IPSec) is cost-effective for
> smaller branch offices or when ExpressRoute is unavailable in the region.

## DNS

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure DNS** | DNS | Global | Host public DNS zones in Azure | Authoritative DNS; delegates to Azure name servers |
| **Azure Private DNS Zones** | DNS | Regional (VNet-linked) | Name resolution within VNets | Auto-registration of VM records; linked to one or more VNets |
| **Private DNS Resolver** | DNS | Regional | Hybrid DNS — forward on-prem queries to Azure Private DNS | Inbound/outbound endpoints; replaces custom DNS VM |

## Network Security

### NSG and ASG

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **NSG** | L3/L4 | Subnet or NIC | Allow/deny inbound and outbound traffic by port, protocol, and IP range | Stateful; 5-tuple rules; default-deny inbound from Internet |
| **ASG** | L3/L4 | NIC (group tag) | Simplify NSG rules for multi-tier apps by grouping NICs logically | Referenced as source/destination in NSG rules; no IP management |

> **Exam tip:** Use ASGs when NSG rules would otherwise require explicit IP lists for
> multi-tier workloads. ASGs do not replace NSGs — they are used as dynamic address
> groups inside NSG rules.

> **Exam tip (AZ-700):** For AZ-700, know that NSGs operate at subnet or NIC level
> (L3/L4, 5-tuple), while Azure Firewall operates at the hub VNet level (L3–L7,
> FQDN-aware). Apply NSGs for micro-segmentation within a spoke; use Azure Firewall
> for centralised east-west and north-south inspection across the hub-spoke topology.

### DDoS Protection Tiers

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **DDoS Network Protection** | L3/L4 | VNet | Enterprise workloads requiring SLA guarantee and telemetry | Per-VNet billing; adaptive tuning; cost protection SLA |
| **DDoS IP Protection** | L3/L4 | Public IP | Single-resource protection without VNet-wide commitment | Pay-per-protected-IP; lighter entry point |
| **DDoS Infrastructure Protection** | L3/L4 | Platform (all Azure) | Baseline free protection for every Azure customer | Always-on; no configuration; limited telemetry |

> **Exam tip:** Choose DDoS Network Protection when the requirement mentions volumetric
> attack mitigation with SLA guarantees, custom thresholds, or attack analytics.
> Infrastructure Protection is free but provides no per-customer telemetry or SLA.

### Azure Firewall SKUs

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure Firewall Basic** | L3–L7 | Regional (hub VNet) | SMB workloads, dev/test, cost-sensitive scenarios | Fixed 250 Mbps throughput; no threat intel feed; no IDPS |
| **Azure Firewall Standard** | L3–L7 | Regional (hub VNet) | Production hub-and-spoke; FQDN filtering | Threat intelligence feed; application/network rules; SNAT |
| **Azure Firewall Premium** | L3–L7 | Regional (hub VNet) | Regulated or high-security environments | TLS inspection; IDPS; URL filtering; web categories |

> **Exam tip:** Choose Azure Firewall Premium when the requirement mentions TLS
> inspection, intrusion detection/prevention (IDPS), or URL-category filtering.
> Standard covers most production scenarios; Basic is not suitable for production
> workloads requiring threat intelligence.

### Decision Flow — Network Security Selection

```mermaid
--8<-- "azure/diagrams/networking/decision-flow-network-security-selection.mmd"
```

> **Exam tip (AZ-500):** For AZ-500, know the layered network security model:
> NSG = layer-4 allow/deny on subnet or NIC; Azure Firewall = stateful L3-L7
> with FQDN rules and threat intelligence; NVA = third-party deep inspection.
> DDoS Protection Standard (not Basic) is required when the question mentions
> SLA-backed mitigation, telemetry, or cost protection for volumetric attacks.

> **Exam tip (AZ-700):** For AZ-700, Private Endpoint requires DNS integration —
> the private DNS zone (e.g. privatelink.blob.core.windows.net) must be linked to
> every VNet that needs to resolve the private IP. Forgetting the DNS link is the
> most common misconfiguration; without it, the public FQDN resolves to the public
> IP even when the endpoint exists.

## Content Delivery (CDN)

| Service | Layer | Scope | Use Case | Key Feature |
|---|---|---|---|---|
| **Azure Front Door** | L7 (HTTP/S) | Global | CDN + WAF + global LB combined | Anycast PoP, WAF, SSL offload, caching rules |
| **Azure CDN (Microsoft)** | L7 (HTTP/S) | Global | Static asset delivery, simple CDN | Verizon/Akamai PoPs, rules engine, legacy option |

> **⚠️ Deprecation warning:** Azure CDN classic profiles (Verizon and Akamai) are retiring
> 30 September 2027. Migrate to **Azure Front Door** (CDN + WAF + global LB) or
> **Azure CDN Standard from Microsoft** for pure CDN workloads.
> See: [Microsoft retirement announcement](https://learn.microsoft.com/en-us/azure/cdn/classic-cdn-retirement-faq)

> **Exam tip:** Choose Azure Front Door when the requirement mentions global HTTP load balancing,
> WAF, or SSL offload at the edge.

## Connectivity Patterns

```mermaid
--8<-- "azure/diagrams/networking/connectivity-patterns.mmd"
```

| Pattern | Description |
| --- | --- |
| **Hub-Spoke** | Central hub VNet with shared services (firewall, bastion, DNS), spokes per workload |
| **Virtual WAN** | Microsoft-managed hub-spoke at scale, with SD-WAN integration |

## Load Balancer SKU Selection

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure Load Balancer Basic** | L4 | Regional | Dev/test, single availability set | Free; no SLA for multi-VM; no AZ support |
| **Azure Load Balancer Standard** | L4 | Regional/Zonal | Production VM load balancing | Zone-redundant; SLA 99.99%; HTTPS health probes |
| **Application Gateway** | L7 | Regional | HTTP/S web app routing | WAF, SSL offload, URL-based routing |

> **Exam tip:** Standard Load Balancer requires explicit NSG rules to allow traffic — Basic SKU allows traffic by default. Always use Standard for production workloads.

> **SLA note:** Basic Load Balancer is not designed for SLA-backed production.
> When a requirement explicitly calls for a formal load-balancing SLA, choose
> Standard Load Balancer and deploy with resilient backend instances.

### Load Balancer SKU Decision Flow

```mermaid
--8<-- "azure/diagrams/networking/load-balancer-sku-decision-flow.mmd"
```

## NSG vs ASG

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **NSG** | L4 (TCP/UDP) | Subnet or NIC | Allow/Deny inbound and outbound traffic | Priority-based rules; default deny |
| **ASG** | L4 (TCP/UDP) | NIC grouping | Group VMs logically for NSG rules | Simplifies rules for dynamic VM sets |

> **Exam tip:** ASGs do not replace NSGs — they are used inside NSG rules as source/destination to group NICs without managing individual IP addresses.

### NSG Rule Evaluation

```mermaid
--8<-- "azure/diagrams/networking/nsg-rule-evaluation.mmd"
```

## VNet Connectivity

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **VNet Peering** | L3 (IP) | Regional or Global | Low-latency VNet-to-VNet within or across regions | Non-transitive; no gateway required |
| **VPN Gateway** | L3 (IPsec/IKE) | Regional | Site-to-site, point-to-site, VNet-to-VNet over internet | Encrypted tunnel; supports BGP |
| **ExpressRoute** | L3 (private) | Global | Private on-premises to Azure; no public internet | Dedicated circuit; higher reliability |
| **Azure Bastion** | L7 (HTTPS/RDP) | Regional | Secure RDP/SSH to VMs without public IP | No public IP on VM needed |

> **Exam tip:** VNet Peering is non-transitive — if VNet A peers with VNet B and VNet B peers with VNet C, VNet A cannot reach VNet C without a direct peering or hub-spoke with gateway transit enabled.

### VNet Connectivity Decision Flow

```mermaid
--8<-- "azure/diagrams/networking/vnet-connectivity-decision-flow.mmd"
```

## IP Addressing and Subnet Ranges

### Common CIDR Reference

Azure reserves **5 IP addresses** in every subnet (not 2 as in standard TCP/IP):

| CIDR | Total IPs | Usable (Standard) | Usable (Azure) | Typical Use |
| --- | --- | --- | --- | --- |
| **/8** | 16,777,216 | 16,777,214 | 16,777,211 | Entire private Class A block — theoretical maximum |
| **/12** | 1,048,576 | 1,048,574 | 1,048,571 | Extremely large; rarely practical for a single subnet |
| **/16** | 65,536 | 65,534 | 65,531 | Large VNet address space; covers ≥12,000 host requirement |
| **/20** | 4,096 | 4,094 | 4,091 | Medium subnet; good for thousands of hosts |
| **/24** | 256 | 254 | 251 | Classic "Class C" size; common for small application subnets |
| **/27** | 32 | 30 | 27 | Small subnet; minimum recommended size for GatewaySubnet |
| **/28** | 16 | 14 | 11 | Very small; Azure Firewall, Bastion, or Application Gateway subnets |
| **/29** | 8 | 6 | 3 | Minimum usable Azure subnet; 3 hosts only |
| **/30** | 4 | 2 | n/a | Point-to-point links (on-prem only — not usable in Azure) |
| **/32** | 1 | 0 | 0 | Single host route; not a subnet |

### How CIDR Is Calculated

CIDR notation (e.g. `10.0.1.0/24`) encodes two things in one expression:
the network address and the prefix length. The prefix length (the number after the slash)
tells you how many bits identify the network. The remaining bits identify hosts.

**Formula:**

```text
Total IPs       = 2 ^ (32 - prefix)
Usable (std)    = Total - 2           (subtract network address + broadcast)
Usable (Azure)  = Total - 5           (subtract network + default gateway + 2 DNS + broadcast)
```

**Azure-reserved addresses in every subnet (example: 10.0.1.0/24):**

| Address | Reserved For |
| --- | --- |
| 10.0.1.0 | Network address |
| 10.0.1.1 | Default gateway (reserved by Azure) |
| 10.0.1.2 | DNS mapping (reserved by Azure) |
| 10.0.1.3 | DNS mapping (reserved by Azure) |
| 10.0.1.255 | Broadcast address |

**Worked example — sizing a subnet for 500 VMs in Azure:**

```text
Required hosts  = 500
Add Azure overhead → 500 + 5 = 505
Nearest power of 2 ≥ 505 → 2^10 = 1,024
Prefix length   = 32 - 10 = /22  (1,024 total; 1,019 usable in Azure)
```

**Quick power-of-2 lookup:**

| Prefix | 2^(32−n) |
| --- | --- |
| /20 | 4,096 |
| /21 | 2,048 |
| /22 | 1,024 |
| /23 | 512 |
| /24 | 256 |
| /25 | 128 |
| /26 | 64 |
| /27 | 32 |
| /28 | 16 |
| /29 | 8 |

> **Exam tip:** Azure always reserves 5 addresses per subnet. When a question gives a host
> count requirement, add 5 before selecting the prefix — a /24 supports 251 hosts, not 254.
> The minimum subnet size for most Azure services is /29 (3 usable hosts). Dedicated subnets
> such as GatewaySubnet, AzureFirewallSubnet, and AzureBastionSubnet each require their own
> dedicated subnet and have minimum size requirements (/27 for GatewaySubnet, /26 for Bastion).
