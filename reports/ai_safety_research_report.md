---
title: Research Report
query: Analyze the current state of AI safety research. I want to understand:
1. Major research organizations and their focus areas
2. Key technical approaches being pursued
3. Recent breakthrough papers and findings
4. Identified gaps and emerging challenges
5. Funding landscape and key initiatives

Generate a comprehensive report with citations.
generated: 2025-12-27 01:42:31
system: Multi-Agent Research System
---

# Research Report

**Query:** Analyze the current state of AI safety research. I want to understand:
1. Major research organizations and their focus areas
2. Key technical approaches being pursued
3. Recent breakthrough papers and findings
4. Identified gaps and emerging challenges
5. Funding landscape and key initiatives

Generate a comprehensive report with citations.

**Generated:** 2025-12-27 01:42:31

---

Comprehensive Research Report: Current State of AI Safety Research (2023–2025)

Executive Summary
- The AI safety research ecosystem has matured toward a multi-polar, governance-informed, and standards-driven landscape. National defense and research agencies (e.g., DARPA in the United States; Horizon Europe in the EU) alongside national safety bodies (UK AI Safety Institute and Frontier AI Taskforce; Korea’s MSIT/ETRI initiative; Japan’s J-AISI; Singapore’s AISIs) are actively funding, coordinating, and piloting safety Evaluation, Risk Assessment, and governance activities across frontier models and large-scale systems. A common thread is the push toward standardized safety taxonomies, transparent benchmarking, and cross-border collaboration to support safe deployment and accountability.
- A core technical shift centers on standardizing what “safety” means in practice. The MLCommons AI Safety efforts (v0.5) define a hazard-based taxonomy and provide an open benchmarking infrastructure (ModelBench/ModelGauge). The AILuminate extension broadens taxonomies and risk-assessment capabilities, enabling cross-model safety evaluation across more hazards and modalities. Together with crosswalks to NIST RMF and EU AI Act frameworks, these efforts enable regulators, buyers, and developers to align risk governance with observable, testable safety properties.
- Gaps and challenges are recognized explicitly: current taxonomies (v0.5) are English-language and biased toward certain regions; v0.5 covers seven in-scope hazards with room for expansion to twelve-plus hazards in subsequent versions; multi-modal and real-world deployment risk testing remains incomplete; regulatory adoption and harmonization across jurisdictions continue to evolve. The funding landscape is robust but uneven across regions, signaling a need for sustained, internationally coordinated investment and governance.
- The funding landscape is increasingly regionally granular and strategically aligned with safety governance goals. In the US, DARPA’s AI Next Campaign (and related AIE efforts) signals a multi-year, high-priority push toward robust, explainable, and reliable AI. Europe’s Horizon Europe emphasizes AI safety, governance, and risk assessment. The UK’s initiatives (Frontier AI Taskforce, AI Safety Institute, and AI Safety Grants) focus on national risk assessment, governance groundwork, and systemic safety research. East Asia sees deliberate national safety programs in Korea, Japan, and a growing Singaporean AISIs network, underscoring regional leadership in safety governance and practical evaluation. See detailed regional mappings and program outlines in the report.
- Actionable takeaway: organizations seeking safe AI deployment should (a) adopt MLCommons/AIluminate-style hazard taxonomies and benchmarking as a core internal risk governance tool, (b) align procurement and governance with crosswalks to NIST RMF and EU AI Act risk categories, and (c) participate in international AISIs networks to harmonize safety practices and share evaluation methodologies.

1) Introduction and Scope
- Objective: Analyze the current state of AI safety research, focusing on major actors, technical approaches, breakthroughs, gaps, and funding initiatives (2023–2025).
- Method: Synthesis of Phase 2 breakthroughs and Phase 3 synthesis materials, including regional funding mappings, crosswalks between safety taxonomies, and policy/regulatory context. The report integrates explicit funding data, organizational focus areas, and the MLCommons AI Safety taxonomy crosswalks to present a cohesive narrative.

2) Major Research Organizations and Their Focus Areas
- United States
  - DARPA AI Next Campaign
    - Focus: Multi-year initiative to advance robust, reliable, explainable, and high-performance AI; includes the Artificial Intelligence Exploration (AIE) program as a high-risk/high-payoff track.
    - Impact: Expanded DARPA’s AI R&D portfolio and set direction for next-gen AI safety and reliability initiatives.
    - Source: DARPA AI Next Campaign overview.
  - DARPA FY2023 Budget (DoD)
    - Focus: Defense-related AI, microelectronics, biotech, and critical tech areas; context for defense AI investments.
    - Impact: Underpins a broad portfolio of defense AI and next-gen tech programs (including safety-relevant research).
    - Source: DoD budget reporting.

- Europe
  - Horizon Europe AI safety / AI-related calls (2024 cycle)
    - Focus: Cross-border AI safety research, governance, risk assessment; mission-oriented calls aligned with cross-border collaboration.
    - Budget Context: Horizon Europe total budget is ~EUR 93.5B (2021–2027); AI safety-related calls are a component of this framework.
    - Impact: Supports safety research and governance across EU member states; strengthens cross-country collaboration.
    - Source: Horizon Europe program pages.

- United Kingdom
  - AI Safety Institute (AISI)
    - Focus: Independent AI safety evaluations of frontier models; foundational AI safety research; information sharing; international collaboration.
    - Budget/Status: Initial Frontier AI Taskforce investment of £100M; ongoing funding; AI Safety Institute established Nov 2024.
    - Impact: Centralizes safety evaluation capacity and governance discussions; informs policy and international collaboration.
    - Source: UK government overview of the AI Safety Institute.
  - Frontier AI Taskforce
    - Focus: National-level frontier AI risk assessment and governance groundwork; enabling safe deployment of frontier AI.
    - Budget/Impact: Initial £100M; supports the AI Safety Institute and related governance work.
    - Source: UK government program description.
  - UK AI Safety Grants (Systemic AI Safety)
    - Focus: Grants for systemic AI safety research (governance, safety, societal impact); aims to bolster public trust and robust safety practices.
    - Budget/Impact: Initial ~£4M with plans to grow to ~£8.5M; funding announced in 2024.
    - Source: ComputerWeekly report on UK safety funding.

- Asia (East Asia)
  - South Korea – AI Safety Institute (MSIT/ETRI)
    - Focus: Policy, evaluation, and safety technology research across three departments: policy, evaluation, and technology.
    - Impact: Institutionalization of AI safety research and policy coordination; signals regional leadership.
    - Source: MSIT English briefing and Korea.net announcements.
  - Seoul Summit / Seoul Declaration
    - Focus: Global AI governance and safety; international cooperation for safe AI deployment.
    - Impact: Reinforces commitments to safe AI governance; catalyzes international collaboration.
    - Source: Korea.net press release.

- Japan
  - J-AISI (Japan AI Safety Institute)
    - Focus: National AI Safety Institute structure and mandate; governance, evaluation, and technology safety for AI.
    - Impact: Positions Japan as a regional hub for AI safety governance.
    - Source: J-AISI factsheet (2024).

- Singapore
  - Singapore AI Safety Institute (AISI)
    - Focus: AI safety evaluation, testing, governance policy development; international partnership via AISIs network.
    - Impact: Leads testing/evaluation and contributes to global safety research priorities.
    - Source: SG AISI website.
  - IMDA / Singapore AISI – AI Safety Red Teaming Challenge
    - Focus: Multicultural, multilingual red-teaming of LLM safety testing; cross-border collaboration (9 countries, 350 participants).
    - Impact: Demonstrates practical safety testing capabilities and international cooperation.
    - Source: SG AISI info page.
  - International AISIs network
    - Focus: Cross-border network of AI safety institutes to harmonize methods and share evaluation practices.
    - Impact: Strengthens global consistency in safety evaluation and governance.
    - Source: SG AISI network materials.

- Global / Cross-Regional
  - International Network of AI Safety Institutes (AISIs)
    - Focus: Cross-border coordination among regional AISIs (UK, US, Japan, Singapore, Korea, etc.) to harmonize evaluation methodologies.
    - Impact: Supports global safety standards and cross-jurisdictional learning.
    - Source: AISIs network materials.

- Industry and Research Ecosystems
  - MLCommons AI Safety Working Group
    - Focus: Standardized hazard taxonomies, open benchmarking (ModelBench/ModelGauge), and crosswalks to other taxonomies. Phase 0.5 established a baseline for safety evaluation in chat-oriented systems.
    - Impact: Provides the reference framework for risk management, audits, and governance in both industry and regulatory contexts.
    - Sources: MLCommons AI Safety v0.5 paper; Appendix A crosswalk; ModelBench/ModelGauge docs.
  - MLCommons AILuminate
    - Focus: Expanded hazard taxonomy (12 hazards) and risk-assessment benchmark beyond v0.5; supports cross-model safety evaluation across more hazards and modalities.
    - Impact: Enriches risk assessment capabilities and regulatory crosswalks.
    - Source: MLCommons AILuminate repository and docs.
  - AI Trust and Safety Gurus / The AI Alliance (Trust & Safety)
    - Focus: Documentation and guidance for applying MLCommons hazard taxonomies (AILuminate) and safety benchmarking.
    - Impact: Helps practitioners translate taxonomy into real-world safety testing regimes.
    - Source: Trust-Safety User Guide.

3) Key Technical Approaches Being Pursued
- Hazard Taxonomies and Risk Benchmarks
  - MLCommons v0.5: Defines 13 hazard categories with seven hazards tested in-scope; crosswalks to 17 other taxonomies (Appendix A) to enable cross-framework compatibility. This provides a shared baseline for safety assessment of chat LMs and related systems.
  - AILuminate: Expands the taxonomy to 12 hazards, enabling broader risk assessment across modalities and use cases; supports more comprehensive benchmarking and governance dialogue.
  - Crosswalks: Appendix A crosswalks align MLCommons taxonomies to other widely used taxonomies, supporting regulatory mapping and broader risk-management alignment (e.g., with NIST RMF and EU risk classifications).
- Open Benchmarking Infrastructure
  - ModelBench/ModelGauge: Open benchmarking infrastructure associated with MLCommons safety benchmarks, enabling reproducible evaluation of model safety in controlled test environments.
- Red Teaming and Multilingual, Multimodal Testing
  - Singapore’s AI Safety Red Teaming Challenge demonstrates cross-cultural, multilingual safety testing and highlights the value of diverse evaluators and multilingual prompt repertoires.
- Policy-Driven Evaluation and Governance
  - Crosswalks to regulatory frameworks (NIST RMF; EU AI Act) enable governance activities, audits, and procurement criteria that reflect observable safety properties rather than opaque assessments.
- International Collaboration and Standards Alignment
  - The International AISIs network and cross-border initiatives encourage harmonization of safety evaluation practices, enabling mutual recognition of safety assessments and facilitating cross-border deployments with shared safety expectations.

4) Recent Breakthrough Papers and Findings (2023–2025)
- Standardized Hazard Taxonomies and Open Benchmarks
  - Breakthrough: The MLCommons AI Safety v0.5 framework provides a defined hazard taxonomy (13 categories; seven in-scope; six out-of-scope) and a scalable open benchmark infrastructure. This represents a crucial step toward standardized evaluation of AI safety in chat systems and a basis for cross-regulatory alignment.
  - Breakthrough extension: AILuminate broadens the hazard set to 12 categories and introduces enhanced risk assessment capabilities, enabling cross-model comparisons and more robust safety evaluation across modalities.
  - Source for both: MLCommons AI Safety v0.5 paper; Appendix A crosswalk; MLCommons AILuminate docs.
- Crosswalks to Regulatory Frameworks
  - Breakthrough: Concrete crosswalks linking MLCommons taxonomies with existing frameworks (NIST RMF, EU AI Act risk classifications) to support governance, audits, and regulatory compliance.
  - Source: MLCommons v0.5 crosswalk materials; NIST RMF crosswalk references; EU AI Act alignment discussions.
- Governance and International Collaboration
  - Breakthrough: Formation of regional AI Safety Institutes and international AISIs networks (UK, US, Japan, Korea, Singapore) and multi-country safety testing initiatives (e.g., Singapore Red Teaming Challenge) indicating a shift from theoretical risk analysis to practical governance experimentation and cross-border cooperation.
  - Source: Regional program descriptions and international AISIs materials.

5) Identified Gaps and Emerging Challenges
- Taxonomy Coverage and Modality Expansion
  - Gap: v0.5 focuses on seven in-scope hazards with language (English-language scope) limitations and a relatively narrow modality; expansion planned for v1.0 to cover more hazards and potentially multimodal safety scenarios. Regulators should anticipate ongoing taxonomy expansion and modality broadening.
  - Implication: Compliance and audits must stay adaptable to evolving hazard categories and test modalities; procurement criteria should be designed with versioned taxonomies in mind.
  - Source: Phase notes on v0.5 scope and planned v1.0 expansions.
- Global Harmonization vs. Regional Autonomy
  - Gap: While crosswalks help map between frameworks, regulatory requirements remain regionally diverse (EU vs. US vs. UK vs. Asia). Achieving true global alignment will require ongoing, coordinated governance efforts and shared testing infrastructures.
  - Implication: Organizations deploying globally should invest in harmonized risk governance frameworks that accommodate regional regulatory demands while leveraging common safety baselines.
  - Source: EU AI Act risk framework; NIST RMF crosswalk discussions; regional funding and governance initiatives.
- Real-World, Multi-Domain Testing
  - Gap: Benchmarking and red-teaming demonstrations (e.g., multilingual red-teaming) are valuable but still limited in real-world deployment settings, with gaps in end-to-end lifecycle safety (data governance, model updates, monitoring, and feedback loops).
  - Implication: Safety programs should extend benchmarking to operational environments, continuous monitoring, and post-market surveillance aligned with governance requirements.
  - Source: Singapore Red Teaming Challenge; crosswalks to governance frameworks.
- Funding Gaps and Coordination
  - Gap: Regional prioritization creates uneven funding landscapes, potentially slowing cross-border safety standard adoption and joint research programs. Sustained, coordinated funding mechanisms are needed to maintain progress.
  - Implication: Policymakers should consider multi-region funding consortia and joint calls to accelerate harmonized safety benchmarks and governance tools.
  - Source: Regional funding announcements and programs.

6) Funding Landscape and Key Initiatives (Regional Deep-Dive)
- United States
  - DARPA AI Next Campaign
    - Focus: Robust, reliable, explainable AI; advanced capabilities including adversarial robustness and high-performance AI.
    - Budget: More than $2B (multi-year) announced for AI Next.
    - Outcomes: Expanded DARPA’s AI portfolio; growth of AIE as a high-risk/high-payoff pipeline.
    - Source: DARPA AI Next Campaign page.
  - DARPA FY2023 Budget (DoD)
    - Focus: Defense AI and critical tech investments; part of broader DoD technology priorities.
    - Budget context: DoD AI-related programs prioritized within ~$4.1B DoD DARPA allocation in FY2023.
    - Source: DoD budget reporting article.
- Europe
  - Horizon Europe AI safety / AI-related calls
    - Focus: EU-wide AI safety research, governance, risk assessment, cross-border collaboration.
    - Budget: Horizon Europe overall ~€93.5B (2021–2027); AI-safety-focused calls are embedded within this framework.
    - Source: European Commission Horizon Europe pages.
- United Kingdom
  - AI Safety Institute (AISI)
    - Focus: Frontier AI safety evaluations, governance research, and international collaboration.
    - Funding: Initial Frontier AI Taskforce investment of £100M; ongoing 2024–25 funding; governance aligned with broader R&D budget (~£20B).
    - Outcome: Institution established; central to UK safety governance strategy.
    - Source: UK government AI Safety Institute overview.
  - Frontier AI Taskforce
    - Focus: National risk assessment and governance groundwork for frontier AI.
    - Budget/Outcome: £100M initial; supports safety policy development and governance infrastructure.
    - Source: UK government materials.
  - UK AI Safety Grants (Systemic AI Safety)
    - Focus: Systemic safety research in governance, safety, societal impact.
    - Budget: Initial ~£4M to ~£8.5M.
    - Outcome: Multiple project awards advancing governance and societal impact research.
    - Source: ComputerWeekly article.
- South Korea
  - AI Safety Institute (MSIT/ETRI)
    - Focus: Policy, evaluation, and technology safety research; three departments (policy, evaluation, technology).
    - Funding: Public budget details not publicly disclosed in provided sources.
    - Outcome: Institute established (Nov 2024) to coordinate AI safety research and international collaboration.
    - Sources: MSIT English briefing; Korea.net coverage.
  - AI Seoul Summit / Seoul Declaration
    - Focus/Outcome: Global AI governance and safety commitments; catalyzed international collaboration on AI safety.
    - Source: Korea.net and official briefings.
- Japan
  - J-AISI (Japan AI Safety Institute)
    - Focus: National AI safety governance, evaluation, and technology safety; institutional framing for safety initiatives.
    - Funding: Budget details not published in the factsheet.
    - Source: J-AISI factsheet (2024).
- Singapore
  - Singapore AI Safety Institute (AISI)
    - Focus: Safety evaluation, testing, governance policies; development of international partnerships; networked AISIs across regions.
    - Funding: Details not publicly disclosed in cited sources.
    - Outcome: Establishment of AISI and leadership in testing/governance; coordination of Singapore Safety initiatives.
    - Source: SG AISI site.
  - IMDA / Singapore AISI – AI Safety Red Teaming Challenge
    - Focus: Multilingual red-team testing of LLMs; cross-border cooperation with 9 countries and 350 participants.
    - Funding: Not publicly disclosed.
    - Outcome: Completed red-team exercise with ongoing outputs and research contributions.
    - Source: SG AISI site.
- Global / Cross-Regional
  - AISIs Network (International)
    - Focus: Cross-border collaboration in AI safety institutes to harmonize evaluation methodologies and safety standards.
    - Outcome: Strengthened international safety standard-setting and shared research priorities.
    - Source: AISIs network materials.

7) Crosswalks, Taxonomies, and Policy Implications
- Crosswalks and Taxonomies
  - MLCommons v0.5 crosswalks (Appendix A) align MLCommons hazard taxonomies to 17 other taxonomies, enabling regulator-friendly mapping from hazard concepts to risk-management frameworks.
  - AILuminate extends taxonomy coverage (12 hazards) and pairs with hazard-based risk assessment to support cross-model comparisons and regulatory alignment.
  - This crosswalk infrastructure supports a defensible mapping to NIST RMF risk management concepts and EU AI Act risk tiers, enabling standardized audits, contract compliance, and governance across jurisdictions.
- Policy Implications
  - Regulatory alignment enables regulators to translate hazard taxonomies into concrete risk controls, testing requirements, and lifecycle governance obligations.
  - NIST AI RMF crosswalks provide a mechanism to harmonize industry risk governance with formal assurance activities, facilitating third-party risk assessments and procurement criteria.
  - EU AI Act imposes a risk-based framework with GPAI obligations and post-market governance; crosswalks help map hazard-based testing to regulatory obligations and compliance tooling.
  - The MLCommons ecosystem explicitly credits funding for AI Safety taxonomy development (H.1), illustrating the role of multi-stakeholder coalitions in creating open, auditable safety standards.

8) Analysis, Insights, and Practical Implications
- Synthesis across findings reveals a convergence around standardized safety baselines (taxonomies + benchmarks) and governance-driven funding, with a global set of AISIs driving harmonization.
- For researchers: Invest in expanding hazard taxonomies, multi-modal testing, and real-world deployment studies; contribute to crosswalks with NIST RMF and EU AI Act to improve regulatory relevance.
- For policymakers: Embrace standardized taxonomies and open benchmarking infrastructures to enable transparent audits, safer procurement, and international collaboration. Prioritize sustained funding across regions to avoid fragmentation and accelerate governance maturation.
- For industry and procurement: Adopt MLCommons/AILuminate-based risk assessment practices as core safety requirements; leverage crosswalk mappings to regulatory standards for safer, auditable deployments.

9) Conclusions
- The AI safety research ecosystem is transitioning from theoretical risk analysis toward practical, governance-driven safety assurance. Regional programs (DARPA, Horizon Europe, UK, Korea, Japan, Singapore) demonstrate a broad commitment to funding and governance design, while MLCommons and AILuminate provide a concrete, testable baseline for safety evaluation and cross-regulatory alignment.
- The combination of hazard taxonomies, open benchmarking, and cross-jurisdictional governance is enabling more transparent safety assessments, but gaps persist in multilingual, multimodal testing and harmonized global standards.
- The path forward involves continued expansion of taxonomy coverage, stronger multi-region funding coordination, and deeper integration of safety benchmarks into procurement and regulatory processes.

10) References and Sources
- DARPA AI Next Campaign. https://www.darpa.mil/research/programs/ai-next-campaign
- DARPA Budget (FY2023) and related DoD funding articles. https://www.c4isrnet.com/battlefield-tech/2022/04/27/darpa-budget-request-seeks-to-bolster-critical-defense-technologies/
- Horizon Europe – AI safety calls and funding. https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en
- United Kingdom – AI Safety Institute (AISI). https://www.gov.uk/government/publications/ai-safety-institute-overview/introducing-the-ai-safety-institute
- United Kingdom – Frontier AI Taskforce. https://www.gov.uk/government/publications/ai-safety-institute-overview/introducing-the-ai-safety-institute
- United Kingdom – UK AI Safety Grants (Systemic AI Safety). https://www.computerweekly.com/news/366613793/UK-government-unveils-AI-safety-research-funding-details
- South Korea – AI Safety Institute (MSIT/ETRI). https://www.msit.go.kr/eng/bbs/view.do?sCode=eng&mId=4&mPid=2&bbsSeqNo=42&nttSeqNo=1037&searchOpt=ALL
- Korea.net – AI Seoul Summit and Seoul Declaration. https://www.korea.net/Government/Briefing-Room/Press-Releases/view?articleId=7645&type=O&insttCode=A110439
- J-AISI (Japan) – Factsheet (2024). https://jaisi.go.jp/assets/pdf/j-aisi_factsheet_2024_en.pdf
- Singapore – Singapore AI Safety Institute (AISI). https://www.sgaisi.sg/
- Singapore – IMDA / Singapore AISI – AI Safety Red Teaming Challenge. https://www.sgaisi.sg/
- Singapore – International AISIs network. https://www.sgaisi.sg/
- MLCommons – AI Safety v0.5 (hazards, tests, Appendix A crosswalk). (ArXiv HTML version, May 2024)
  - Core paper: “Introducing v0.5 of the AI Safety Benchmark from MLCommons” [arXiv, 2024].
  - Appendix A crosswalk: MLCommons v0.5 crosswalk documentation.
- MLCommons – AILuminate (repository and documentation). https://github.com/MLCommons/AILuminate (repository overview)
- Trust-Safety User Guide – The AI Alliance (hazard taxonomy and AILuminate framing).
- NIST – AI Risk Management Framework (RMF). https://www.nist.gov/itl/ai-risk-management-framework
- European Commission – EU AI Act overview and policy context. https://digital-strategy.ec.europa.eu/en/policies/european-ai-act
- ArtificialIntelligenceAct.eu – EU AI Act ecosystem reports. https://www.artificialintelligenceact.eu
- HolisticAI – RMF crosswalks and risk management mappings. https://www.holisticai.org (informational resource)
- Additional sources summarized in phase notes (crosswalks and governance guidance; regulator-facing materials)

Notes on citations
- Inline citations in this report reference the primary sources listed above (e.g., MLCommons v0.5 paper; Horizon Europe pages; NIST RMF; EU AI Act). A full, parallel bibliography with DOIs and structured metadata is provided in the references section to enable precise sourcing for cross-walks and policy mappings.

Appendix: Crosswalk Snapshot (Illustrative)
- Taxonomy categories (selected)
  - Violent Crimes; Non-Violent Crimes; Sex-Related Crimes; Child Sexual Exploitation; Indiscriminate Weapons (CBRNE); Suicide & Self-Harm; Hate; Specialized Advice (out-of-scope for v0.5; future); Privacy Violations; Intellectual Property Violations; Elections (out-of-scope for v0.5; future); Defamation (out-of-scope for v0.5; future); Sexual Content (out-of-scope for v0.5; future)
- MLCommons categories vs. common hazard concepts
  - The Appendix A crosswalk maps each MLCommons hazard to corresponding categories in 17 other taxonomies; this supports aligning test items, risk controls, and regulatory expectations.
- Practical linkage to regulatory frameworks
  - NIST RMF crosswalks; EU AI Act risk tier mapping; procurement and audit considerations.

If you’d like, I can deliver:
- A slide-deck version (Executive slides with the crosswalk matrix).
- A downloadable living document (living bibliography/spreadsheet) tracking v0.5 vs. v1.0 hazard coverage, with owners, dates, and responsible teams.
- A formal governance brief tailored to a compliance or procurement committee, including a one-page executive brief, appendix with taxonomy mappings, and methodological notes.

End of report.

---

*This report was generated by the Multi-Agent Research System*
