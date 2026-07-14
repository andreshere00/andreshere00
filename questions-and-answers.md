# AI and Data interview evaluation questions

Each answer describes the evidence a strong candidate should provide. Questions are intentionally
open-ended so interviewers can probe for relevant examples, trade-offs, and decision making.

## Machine Learning (ML)

### Machine Learning Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **Describe a prediction problem you would frame as classification and one you would frame as regression. What would the model produce in each case?** | Correctly distinguishes discrete classes from continuous values and gives a practical example for each. |
| Low | **How would you turn a raw tabular dataset into a first model experiment?** | Identifies the target, inspects data quality, creates a leakage-safe split, preprocesses features, trains a simple baseline, and compares results. |
| Low | **A model scores well on its training data but poorly on new records. What does that suggest, and what would you try first?** | Recognizes overfitting and suggests a proper validation split, simpler features or model, regularization, more representative data, or cross-validation. |
| Low | **How would you explain the purpose of training, validation, and test data to a non-technical stakeholder?** | Explains fitting, model selection, and final unbiased evaluation without reusing the test set for decisions. |
| Low | **How would you decide whether accuracy is enough to evaluate a binary classifier?** | Connects metric choice to class balance and error costs, and mentions precision, recall, F1, PR-AUC, or a decision threshold when appropriate. |
| Low | **Before trusting a model feature, what checks would you perform?** | Covers completeness, type and range checks, leakage, stability, business meaning, and whether the feature is available at prediction time. |

### Deep Learning Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **You need to build an image classifier with limited labeled data. How would you choose a starting architecture and training approach?** | Proposes transfer learning, an appropriate pretrained model, augmentation, a validation strategy, and a simple baseline before a custom network. |
| Mid | **A neural network's validation loss rises while training loss keeps falling. How would you investigate and respond?** | Diagnoses overfitting and discusses data quality, split integrity, augmentation, regularization, early stopping, model capacity, and learning curves. |
| Mid | **How would you choose activation functions, normalization, and initialization for a new deep learning model?** | Explains their effect on gradient flow and stability, uses sensible defaults such as ReLU-family activations and compatible initialization, and validates empirically. |
| Mid | **Training becomes unstable and the loss occasionally becomes NaN. What would you inspect in order?** | Checks inputs and labels, numerical operations, learning rate, gradients, mixed precision, initialization, normalization, and optimizer configuration. |
| Mid | **How would you make a deep learning model faster at inference while protecting an agreed quality target?** | Defines a baseline and budget, then evaluates batching, compilation, quantization, pruning, distillation, architecture changes, and production-like benchmarks. |
| Mid | **How would you tell whether a deep learning model has learned a useful pattern rather than exploiting an artifact?** | Uses held-out and segment tests, error analysis, augmentations or counterfactuals, data provenance review, and comparison against simple baselines. |

### Model Evaluation

| Level | Question | What a strong answer should cover |
|---|---|---|
| High | **Design an evaluation plan for a fraud model where false approvals and false declines have different financial costs.** | Translates costs into operating thresholds and metrics, uses time-aware and segment evaluation, calibration, business baselines, and post-launch guardrails. |
| High | **How would you prove that an apparent offline improvement is genuine and likely to transfer to production?** | Checks leakage and split design, confidence intervals, repeated or temporal validation, segment performance, data parity, and online experimentation or shadowing. |
| High | **A model's aggregate quality is stable, but complaints rise for one customer group. How would you investigate?** | Disaggregates metrics and data quality by relevant cohorts, validates sample size and labels, examines threshold and calibration differences, and considers fairness and remediation. |
| High | **How would you distinguish data drift, concept drift, and a serving defect after a quality alert?** | Compares input distributions, feature transformations, predictions, delayed labels, model versions, and serving logs against a known-good baseline. |
| High | **How would you evaluate a model when ground-truth labels arrive weeks after each decision?** | Combines delayed-label evaluation with leading indicators, data-quality and prediction monitoring, controlled experiments, and explicit uncertainty about proxy metrics. |
| High | **What evidence would you require before replacing a human decision process with a model-assisted workflow?** | Includes representative evaluation, error and harm analysis, calibration, operational constraints, human override and audit design, rollout controls, and stakeholder approval. |

---

## Data (Data)

### Data Engineering Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **Walk through a simple daily pipeline that turns application events into a table analysts can use.** | Describes ingestion, raw retention, schema validation, transformation, loading, scheduling, monitoring, and rerun safety. |
| Low | **An input file contains duplicate and malformed records. What would you do before publishing the data?** | Defines validation rules, quarantine or dead-letter handling, deduplication keys, metrics, and a clear policy for failed records. |
| Low | **How would you explain the value of partitioning a large dataset?** | Connects partitions to less data scanned, faster reads and writes, manageable processing, and an appropriate key such as event date. |
| Low | **A daily job fails halfway through writing its output. How would you avoid leaving consumers with an inconsistent dataset?** | Uses staging or atomic publish patterns, idempotent writes, checkpoints, retry-safe logic, and alerting. |
| Low | **How would you use PySpark to investigate why a dataset became unexpectedly small?** | Checks input partitions and dates, row counts at each transformation, filters and joins, nulls, duplicates, and execution or source errors. |
| Low | **What information would you record so another engineer can understand and rerun a data pipeline?** | Includes source, owner, schedule, schema, transformation logic, dependencies, output location, quality checks, and recovery steps. |

### Analytics Engineering

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **How would you model raw product events into trusted metrics for active users and conversion?** | Defines grain, event identity, deduplication, session or user logic, late data behavior, documented metric definitions, and tested curated models. |
| Mid | **A Snowflake dashboard query became slow and expensive. How would you diagnose and improve it?** | Uses query profiles and warehouse usage, then considers pruning, incremental models, clustering, materialization, caching, and workload sizing. |
| Mid | **How would you ingest Kinesis events into an analytics platform while handling retries and duplicate delivery?** | Defines event IDs, ordering assumptions, durable raw storage, schema validation, idempotent processing, watermarking, and monitoring. |
| Mid | **How would you make a business metric consistent across dashboards, notebooks, and ML features?** | Establishes a governed semantic definition, a canonical transformation, tests, ownership, lineage, and controlled version changes. |
| Mid | **How would you detect and handle late-arriving events in a revenue report?** | Defines event time versus processing time, a freshness window, incremental backfills or merges, reconciliation, and communication of revisions. |
| Mid | **How would you balance a request for real-time reporting against cost and data-quality requirements?** | Clarifies latency needs and decisions enabled, compares streaming and micro-batch options, and proposes service-level, freshness, and cost controls. |

---

## Software (SW)

### Software Engineering Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **How would you structure a Python service that validates a request, applies business rules, and calls external dependencies?** | Separates responsibilities, uses typed interfaces and clear error handling, isolates side effects, and makes core logic testable. |
| Mid | **You inherit a TypeScript or Python module with repeated logic and weak tests. How would you improve it safely?** | First adds characterization tests, identifies genuine common behavior, makes small refactors, preserves contracts, and validates each step. |
| Mid | **How would you choose between synchronous and asynchronous code for an API that calls several remote services?** | Considers I/O versus CPU work, concurrency limits, timeouts, cancellation, error handling, complexity, and observability. |
| Mid | **What would you look for in a pull request that changes a data transformation used by several teams?** | Reviews correctness, schema and backward compatibility, tests, performance, ownership, rollout or migration, documentation, and observability. |
| Mid | **How would you make configuration and secrets safe across local development, CI, and production?** | Separates configuration from code, uses secret management and least privilege, avoids logging secrets, validates settings, and documents rotation. |
| Mid | **How would you investigate an intermittent production error that cannot be reproduced locally?** | Uses correlation IDs, structured logs, metrics and traces, environment and dependency comparison, hypotheses, and a safe fix with regression coverage. |

### Software Architecture

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **How would you choose boundaries for a service that manages data ingestion, transformation, and serving?** | Bases boundaries on domain ownership, cohesion, data contracts, deployment needs, failure isolation, and team responsibility rather than technology alone. |
| Mid | **When would you introduce an event-driven workflow instead of a synchronous API call?** | Identifies asynchronous or decoupled work, then addresses delivery guarantees, idempotency, schema versioning, retries, ordering, and observability. |
| Mid | **How would you introduce a new version of an API or data contract without breaking existing consumers?** | Uses compatibility rules, versioning or additive changes, contract tests, migration periods, consumer communication, and deprecation monitoring. |
| Mid | **How would you design CI/CD for a service that includes application code, data migrations, and infrastructure changes?** | Includes isolated validation, security checks, reproducible artifacts, ordered migrations, environment promotion, progressive delivery, approval controls, and rollback plans. |
| Mid | **A modular monolith is becoming difficult to change. What evidence would make you split a component into a service?** | Looks for stable domain boundaries, independent scaling or release needs, ownership, coupling costs, operational readiness, and a staged migration plan. |
| Mid | **How would you document an architectural decision that has meaningful trade-offs?** | Records context, options, decision, consequences, assumptions, owners, and conditions that would trigger review or reversal. |

---

## Generative AI (GenAI)

### LLM Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| High | **How would you decide whether an LLM API, a self-hosted model, fine-tuning, or prompt and retrieval improvements best solve a product need?** | Starts with measurable requirements, compares quality, privacy, latency, cost, control, operational burden, and validates the choice with representative evaluation. |
| High | **Design an enterprise LLM assistant that can access internal knowledge with different user permissions.** | Covers identity propagation, permission-aware retrieval, data isolation, source citations, audit logs, secret protection, and denial-safe behavior. |
| High | **How would you build an evaluation suite for an LLM feature before and after changes?** | Defines realistic tasks, expected behavior and rubrics, groundedness and safety cases, adversarial inputs, regression sets, human review, latency, and cost. |
| High | **A chatbot gives fluent but unsupported answers. How would you diagnose and reduce the problem?** | Separates retrieval, prompt, model, tool, and evaluation failures; adds abstention, citations, better context, verification, and measured regression tests. |
| High | **How would you manage prompt, model, tool, and policy changes so a production LLM behavior is reproducible?** | Versions all inputs and configurations, captures evaluation evidence, uses controlled rollout and rollback, and traces requests to exact artifacts. |
| High | **How would you protect an LLM application from prompt injection and unintended data disclosure?** | Treats retrieved and user text as untrusted, enforces authorization outside the model, constrains tools, minimizes data, validates outputs, logs safely, and red-teams attacks. |
| High | **How do transformer architecture and context length affect the latency and cost of an LLM feature?** | Explains tokenization, attention and KV-cache costs, input and output token budgets, batching, model selection, and context-management trade-offs. |
| High | **A product team wants to use a larger model because demo quality is better. How would you make the production decision?** | Compares task-level quality and failure modes against latency, throughput, reliability, privacy, and total cost under production traffic. |
| High | **How would you determine whether fine-tuning is justified rather than using few-shot prompting or RAG?** | Identifies the failure type, data quantity and quality, maintenance burden, evaluation plan, safety implications, and the incremental value over simpler approaches. |
| High | **How would you design tool calling for an LLM that can create tickets or update business records?** | Uses strict schemas, least privilege, confirmation for impactful actions, server-side authorization, idempotency, audit logs, and recovery from partial failure. |
| High | **What would you monitor to detect that an LLM feature is becoming less useful or less safe after launch?** | Monitors task success, abstention and escalation, groundedness, policy violations, user feedback, latency, cost, model or prompt versions, and segment behavior. |
| High | **How would you explain an LLM limitation or uncertainty to a business stakeholder without overstating its capabilities?** | Gives a calibrated explanation with concrete examples, measurable evidence, known failure modes, guardrails, and a proposed validation path. |

### RAG Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **How would you design document ingestion and chunking for a knowledge base containing policies, PDFs, and technical guides?** | Preserves document structure and metadata, handles parsing quality and updates, selects chunk boundaries and overlap empirically, and retains source references. |
| Mid | **How would you choose and evaluate embeddings, lexical search, vector search, and reranking for a RAG system?** | Uses labeled queries and retrieval metrics, compares semantic and keyword failure modes, applies metadata filters, and measures latency and cost. |
| Mid | **A RAG assistant retrieves relevant-looking documents but gives poor answers. How would you isolate the failure?** | Separately evaluates ingestion, chunking, retrieval recall, ranking, context assembly, generation, citations, and the answer rubric. |
| Mid | **How would you keep a RAG index current while preventing deleted or unauthorized content from being returned?** | Designs incremental updates and deletes, versioning, access-control filters at query time, reindexing, auditability, and freshness monitoring. |
| Mid | **How would you evaluate whether citations in a RAG response are useful and faithful?** | Checks that cited passages are retrieved, relevant, support each claim, use stable source locations, and avoid unsupported claims or misleading citations. |
| Mid | **How would you reduce retrieval latency for a large corpus without silently lowering answer quality?** | Establishes quality and latency baselines, then considers filtering, index tuning, caching, candidate limits, hybrid retrieval, reranking, and regression evaluation. |

### Agents Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| High | **Design an agent that investigates a data-quality incident using warehouse queries, documentation, and ticketing tools.** | Defines a bounded goal, tool contracts, permissions, planning and state, evidence collection, approval boundaries, audit logs, and a clear completion condition. |
| High | **How would you use MCP or a similar protocol to expose internal tools safely to an agent?** | Defines narrow, typed tools; authenticates and authorizes at the server; validates inputs and outputs; scopes credentials; and logs actions. |
| High | **How would you decide whether a workflow needs one agent, multiple specialized agents, or deterministic orchestration?** | Favors the simplest reliable design, evaluates task decomposition and uncertainty, assigns ownership, constrains communication, and measures coordination overhead. |
| High | **An agent repeatedly retries a failing tool call and increases operational cost. How would you prevent and diagnose that behavior?** | Uses timeouts, retry budgets, idempotency, circuit breakers, state-aware stopping, traces, alerts, and explicit escalation paths. |
| High | **How would you evaluate an agent that executes multi-step workflows with external side effects?** | Builds scenario and adversarial suites, verifies tool-call correctness and final state, measures recovery and unsafe-action rates, and includes human review where needed. |
| High | **How would you design memory for an agent while avoiding stale, sensitive, or untraceable decisions?** | Separates session state from curated knowledge, defines retention and ownership, records provenance, supports expiry and correction, and enforces access controls. |

---

## Infrastructure (Infra)

### Infrastructure Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **How would you deploy a containerized API on AWS, Azure, or GCP with secure configuration and safe scaling?** | Selects appropriate managed services, configures identity and secrets, health checks, resource limits, autoscaling, networking, logging, and rollback. |
| Mid | **A service occasionally fails during traffic peaks. How would you determine whether the bottleneck is compute, database, network, or a dependency?** | Uses saturation, latency, error, and dependency metrics plus traces, then validates a hypothesis before scaling or changing architecture. |
| Mid | **How would you choose between a virtual machine, a managed container platform, and serverless for a new workload?** | Weighs runtime needs, scaling, operations, latency, cost, networking, portability, and team expertise against requirements. |
| Mid | **How would you design secrets and service identities for a workload that accesses a database and a third-party API?** | Uses workload identity, least privilege, managed secret storage, rotation, network restrictions, auditing, and no embedded credentials. |
| Mid | **How would you prepare an application for a regional outage?** | States recovery objectives, assesses dependencies and data replication, chooses active-active or active-passive, defines failover, tests it, and documents operations. |
| Mid | **How would you find and reduce avoidable cloud spend without weakening reliability?** | Uses cost allocation and usage data, rightsizes resources, reviews storage and data transfer, schedules non-production workloads, and protects critical capacity. |

### Observability, Deployment & Monitoring

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **What dashboards and alerts would you create for a newly deployed API or ML inference service?** | Covers golden signals, dependency health, resource saturation, deployment and version context, model or data signals when relevant, and actionable alert thresholds. |
| Mid | **How would you use logs, metrics, and traces together to investigate a rise in request latency?** | Correlates requests with structured logs and traces, identifies the slow span or dependency, compares baselines, and validates the suspected cause. |
| Mid | **How would you roll out a risky release through CI/CD while preserving a fast rollback path?** | Uses automated checks, immutable artifacts, progressive delivery or flags, health and business guardrails, observability, ownership, and reversible migrations. |
| Mid | **What would you log for a model inference request, and what data should you avoid storing?** | Includes request correlation, model and feature versions, validation outcome, latency, errors, and safe output metadata while minimizing or protecting personal and sensitive data. |
| Mid | **An alert fires frequently but rarely indicates a user-impacting issue. How would you improve it?** | Reviews alert history and impact, tunes thresholds or duration, uses symptom-based signals, adds routing and runbooks, and measures alert quality. |
| Mid | **How would you verify that a deployment improved reliability rather than merely changing the metrics?** | Compares a defined baseline and time window, checks user-facing service levels and error budgets, controls for traffic, and reviews regressions by segment. |

### Solutions Architecture & System Design

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **Design a system that accepts user uploads, processes them asynchronously, and makes results available through an API.** | Clarifies requirements, uses durable storage and queues, idempotent workers, status tracking, security, retries, observability, scaling, and cost-aware retention. |
| Mid | **How would you choose between a modular monolith, microservices, and serverless components for a new product?** | Starts with domain and delivery needs, evaluates boundaries, scaling, team ownership, latency, operational complexity, and migration options. |
| Mid | **A read-heavy service must respond quickly worldwide. How would you design caching without serving incorrect or sensitive data?** | Defines cache keys, TTL and invalidation, consistency needs, authorization boundaries, cache placement, fallback behavior, metrics, and capacity limits. |
| Mid | **How would you design for partial failures between a web service, queue, and database?** | Uses timeouts, bounded retries with backoff, idempotency, durable messages, dead-letter handling, reconciliation, and observable failure states. |
| Mid | **How would you make a trade-off between lower latency, higher availability, and lower cost for a customer-facing feature?** | Quantifies requirements and traffic, identifies the bottleneck and business impact, compares options, states assumptions, and proposes measurable guardrails. |
| Mid | **How would you migrate a critical service to a new architecture without disrupting users?** | Uses incremental compatibility patterns, contract tests, feature flags, shadow or dual-run validation, data reconciliation, monitoring, and rollback. |

---

## Others

### Communication Skills

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **Describe how you would explain a model quality trade-off to a product manager deciding whether to launch.** | Translates metrics and uncertainty into user and business impact, states options and recommendation, and invites an informed decision. |
| Mid | **How would you communicate a data-quality issue that may invalidate a stakeholder's report?** | States impact and confidence clearly, avoids blame, explains evidence and next steps, provides an update cadence, and documents the resolution. |
| Mid | **Tell us how you would handle conflicting feedback from engineering, product, and compliance on an AI feature.** | Clarifies goals and constraints, listens for underlying concerns, makes trade-offs explicit, records decisions, and escalates appropriately. |
| Mid | **How would you present an experiment result that is statistically uncertain but time-sensitive?** | Explains uncertainty and limitations plainly, gives risk-aware options, requests only necessary follow-up data, and avoids claiming certainty. |
| Mid | **How would you ensure a handoff of a data or AI system is understandable to the team that will operate it?** | Provides concise documentation, ownership, runbooks, access and dependency details, known limitations, training, and a verification path. |
| Mid | **Describe how you would push back on a request for an unrealistic AI capability while keeping the discussion productive.** | Clarifies the intended outcome, explains technical limits in plain language, presents evidence and safer alternatives, and proposes a testable next step. |

### Domain Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Mid | **You join a team building models for a new business domain. How would you learn enough domain context before proposing a solution?** | Identifies users and decision makers, maps workflows and incentives, studies historical outcomes and definitions, shadows experts, and validates assumptions. |
| Mid | **How would you turn a vague request to “use AI to improve retention” into a well-defined problem?** | Defines the decision, user, outcome, baseline, constraints, success metric, data availability, and whether AI is justified. |
| Mid | **How would you detect that a technically strong model optimizes the wrong business outcome?** | Connects labels and metrics to real decisions, checks incentives and proxies, examines segment effects, and uses stakeholder validation and experiments. |
| Mid | **What questions would you ask a domain expert before using their historical decisions as training labels?** | Asks about policy changes, bias, consistency, exceptions, timing, missing cases, incentives, and whether labels represent desired outcomes. |
| Mid | **How would you assess whether available data represents the population and workflow where a model will be used?** | Compares coverage, sampling, time periods, segments, collection processes, and feedback loops, then documents gaps and mitigations. |
| Mid | **How would you decide when a rules-based workflow is more appropriate than an ML or LLM solution?** | Compares ambiguity, data, explainability, change frequency, error cost, latency, maintenance, and expected value against a simple baseline. |

### Problem Resolution Skills

| Level | Question | What a strong answer should cover |
|---|---|---|
| High | **A production model suddenly changes its predictions after an upstream release. How would you lead the investigation?** | Establishes impact and containment, forms evidence-driven hypotheses, compares versions and data, coordinates owners, communicates status, and prevents recurrence. |
| High | **A high-value AI project is missing its quality target despite several iterations. How would you decide whether to continue, redesign, or stop it?** | Reassesses problem framing, data and label limits, baseline value, technical risks, alternatives, cost of delay, and explicit decision criteria. |
| High | **How would you resolve a disagreement between two valid technical approaches when both have incomplete evidence?** | Defines the decision and constraints, makes assumptions visible, runs the smallest discriminating experiment, considers reversibility, and records the decision. |
| High | **A data pipeline is correct most days but fails unpredictably at scale. How would you find the root cause?** | Narrows the failure with telemetry and reproducible slices, examines load, data skew, dependencies, timing, and resource limits, then validates a durable fix. |
| High | **How would you respond when an incident has multiple contributing causes across teams?** | Coordinates a blameless response, separates mitigation from root-cause analysis, maps contributing factors, assigns owned actions, and verifies their effectiveness. |
| High | **How would you approach a problem where the requested outcome cannot be measured directly?** | Defines a decision-oriented proxy, validates its relationship to the outcome, quantifies uncertainty and Goodhart risk, and revisits it with real feedback. |

### Testing & QA

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **How would you choose between a unit, integration, and end-to-end test for a new feature?** | Matches each test level to the behavior and risk, favoring fast unit coverage with focused integration and critical user-flow tests. |
| Low | **What test cases would you write for a function that cleans incoming customer records?** | Covers valid input, missing and malformed values, boundaries, duplicates, expected transformations, errors, and the documented contract. |
| Low | **How would you test a bug fix so the same defect does not return?** | Creates a minimal regression test that fails before the fix, verifies the fix, and checks relevant neighboring behavior. |
| Low | **How would you test code that calls an external API without making tests slow or unreliable?** | Uses stubs or fakes for deterministic unit tests, validates contracts separately, and reserves real integration calls for controlled environments. |
| Low | **What would you check before approving a change to a data transformation?** | Verifies expected outputs, edge cases, schema compatibility, data quality checks, test coverage, and the impact on downstream consumers. |
| Low | **A test passes locally but fails in CI. What would you inspect first?** | Checks logs, environment differences, test isolation, ordering, timing, dependencies, configuration, and reproducibility before changing the test. |
