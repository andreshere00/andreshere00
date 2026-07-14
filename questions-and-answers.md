# AI and Data interview evaluation questions

Each answer describes the evidence a strong candidate should provide. Questions are intentionally
open-ended so interviewers can probe for relevant examples, trade-offs, and decision making.

## Machine Learning (ML)

### Machine Learning Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **Describe a prediction problem you would frame as classification and one you would frame as regression. What would the model produce in each case?** | Correctly distinguishes discrete classes from continuous values and gives a practical example for each. |
| Low | **How would you turn a raw tabular dataset into a first model experiment?** | Identifies the target, inspects data quality, creates a leakage-safe split, preprocesses features, trains a simple baseline, and compares results. |
| Mid | **A model scores well on its training data but poorly on new records. What does that suggest, and what would you try first?** | Recognizes overfitting and suggests a proper validation split, simpler features or model, regularization, more representative data, or cross-validation. |
| Mid | **How would you explain the purpose of training, validation, and test data to a non-technical stakeholder?** | Explains fitting, model selection, and final unbiased evaluation without reusing the test set for decisions. |
| High | **How would you set and validate operating thresholds for a binary classifier when false-positive and false-negative costs differ by customer segment?** | Connects thresholds to business costs, calibration, segment metrics, uncertainty, monitoring, and an approval process for material trade-offs. |
| High | **Before approving a feature for a high-impact model, how would you evaluate its reliability, leakage risk, and potential harm?** | Covers data provenance, availability at prediction time, stability, causal or proxy risks, segment effects, governance, and post-launch monitoring. |

### Deep Learning Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What problem does an activation function solve in a neural network, and what can happen if all layers are linear?** | Explains that activation functions allow non-linear relationships and recognizes that stacked linear layers remain equivalent to one linear transformation. |
| Low | **A neural network's validation loss rises while training loss keeps falling. What does that indicate?** | Identifies overfitting and suggests checking the split, training duration, regularization, data augmentation, or model capacity. |
| Mid | **How would you choose activation functions, normalization, and initialization for a new deep learning model?** | Explains their effect on gradient flow and stability, uses sensible defaults such as ReLU-family activations and compatible initialization, and validates empirically. |
| Mid | **Training becomes unstable and the loss occasionally becomes NaN. What would you inspect in order?** | Checks inputs and labels, numerical operations, learning rate, gradients, mixed precision, initialization, normalization, and optimizer configuration. |
| High | **How would you make a deep learning model faster at inference while protecting an agreed quality target?** | Defines a baseline and budget, then evaluates batching, compilation, quantization, pruning, distillation, architecture changes, and production-like benchmarks. |
| High | **How would you tell whether a deep learning model has learned a useful pattern rather than exploiting an artifact?** | Uses held-out and segment tests, error analysis, augmentations or counterfactuals, data provenance review, and comparison against simple baselines. |

### Model Evaluation

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **How do accuracy, precision, recall, and F1-score differ, and when might accuracy be misleading?** | Correctly explains each metric and relates the choice to imbalance and the cost of different errors. |
| Low | **Why should a test dataset not be used repeatedly to tune a model?** | Explains that repeated tuning leaks test-set information and produces an optimistic estimate of future performance. |
| Mid | **How would you evaluate a model used in a business-critical decision process?** | Covers predictive quality, calibration, fairness across relevant segments, robustness, explainability, operational impact, and failure costs. |
| Mid | **A model's aggregate quality is stable, but complaints rise for one customer group. How would you investigate?** | Disaggregates metrics and data quality by relevant cohorts, validates sample size and labels, examines threshold and calibration differences, and considers fairness and remediation. |
| High | **How would you evaluate a model when ground-truth labels arrive weeks after each decision?** | Combines delayed-label evaluation with leading indicators, data-quality and prediction monitoring, controlled experiments, and explicit uncertainty about proxy metrics. |
| High | **What evidence would you require before replacing a human decision process with a model-assisted workflow?** | Includes representative evaluation, error and harm analysis, calibration, operational constraints, human override and audit design, rollout controls, and stakeholder approval. |

---

## Data (Data)

### Data Engineering Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **Walk through a simple daily pipeline that turns application events into a table analysts can use.** | Describes ingestion, raw retention, schema validation, transformation, loading, scheduling, monitoring, and rerun safety. |
| Low | **An input file contains duplicate and malformed records. What would you do before publishing the data?** | Defines validation rules, quarantine or dead-letter handling, deduplication keys, metrics, and a clear policy for failed records. |
| Mid | **How would you explain the value of partitioning a large dataset?** | Connects partitions to less data scanned, faster reads and writes, manageable processing, and an appropriate key such as event date. |
| Mid | **A daily job fails halfway through writing its output. How would you avoid leaving consumers with an inconsistent dataset?** | Uses staging or atomic publish patterns, idempotent writes, checkpoints, retry-safe logic, and alerting. |
| High | **How would you use PySpark to diagnose and correct a production pipeline whose output dropped unexpectedly at scale?** | Checks source and partition changes, row counts and joins, data skew, execution plans, resource pressure, data quality, and a reproducible safe fix. |
| High | **How would you design a data platform that supports reproducible backfills, schema evolution, and reliable recovery from failed jobs?** | Defines immutable raw data, contracts, versioned transformations, orchestration, idempotent writes, lineage, checkpoints, and controlled backfill procedures. |

### Analytics Engineering

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What is the difference between a data lake, a data warehouse, and a lakehouse?** | Distinguishes raw flexible storage, curated analytical storage, and a lakehouse's combination of flexible storage with warehouse-style reliability and performance. |
| Low | **When would you use batch processing rather than streaming, and vice versa?** | Relates the choice to freshness needs, complexity, cost, event volume, and the business decision being supported. |
| Mid | **How would you ingest Kinesis events into an analytics platform while handling retries and duplicate delivery?** | Defines event IDs, ordering assumptions, durable raw storage, schema validation, idempotent processing, watermarking, and monitoring. |
| Mid | **How would you make a business metric consistent across dashboards, notebooks, and ML features?** | Establishes a governed semantic definition, a canonical transformation, tests, ownership, lineage, and controlled version changes. |
| High | **A Snowflake dashboard query became slow and expensive. How would you diagnose and improve it without changing reported numbers?** | Uses query profiles and warehouse usage, then considers pruning, incremental models, clustering, materialization, caching, workload sizing, and reconciliation. |
| High | **How would you balance real-time reporting, historical correctness, governance, and cost across a streaming analytics platform?** | Clarifies service-level needs, designs retention and reconciliation, assigns ownership and access controls, compares architectures, and proposes measurable cost and quality guardrails. |

---

## Software (SW)

### Software Engineering Basics

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **How would you explain the difference between a function, a class, and a module in Python or TypeScript?** | Describes reusable behavior, encapsulated data and behavior, and a file or package boundary with an appropriate example. |
| Low | **What makes code easy for another engineer to read and change?** | Identifies meaningful names, small focused units, explicit interfaces, consistent style, tests, and concise documentation. |
| Mid | **How would you choose between synchronous and asynchronous code for an API that calls several remote services?** | Considers I/O versus CPU work, concurrency limits, timeouts, cancellation, error handling, complexity, and observability. |
| Mid | **What would you look for in a pull request that changes a data transformation used by several teams?** | Reviews correctness, schema and backward compatibility, tests, performance, ownership, rollout or migration, documentation, and observability. |
| High | **How would you make configuration and secrets safe across local development, CI, and production for several independently deployed services?** | Separates configuration from code, uses managed secret storage, workload identity and least privilege, avoids logging secrets, validates settings, rotates credentials, and audits access. |
| High | **How would you investigate an intermittent production error that cannot be reproduced locally across a distributed service?** | Uses correlation IDs, structured logs, metrics and traces, environment and dependency comparison, hypotheses, safe mitigation, and regression coverage. |

### Software Architecture

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What responsibilities would you expect a controller, service, and data-access layer to have in a typical application?** | Explains separation of input handling, business rules, and persistence, and connects it to maintainability and testing. |
| Low | **What is the practical difference between a monolith and microservices?** | Explains deployment and ownership boundaries, plus the added operational complexity of distributed communication. |
| Mid | **How would you introduce a new version of an API or data contract without breaking existing consumers?** | Uses compatibility rules, versioning or additive changes, contract tests, migration periods, consumer communication, and deprecation monitoring. |
| Mid | **When would you introduce an event-driven workflow instead of a synchronous API call?** | Identifies asynchronous or decoupled work, then addresses delivery guarantees, idempotency, schema versioning, retries, ordering, and observability. |
| High | **How would you design CI/CD for a service that includes application code, data migrations, and infrastructure changes?** | Includes isolated validation, security checks, reproducible artifacts, ordered migrations, environment promotion, progressive delivery, approval controls, and rollback plans. |
| High | **A modular monolith is becoming difficult to change. What evidence would make you split a component into a service, and how would you migrate it?** | Looks for stable domain boundaries, independent scaling or release needs, ownership, coupling costs, operational readiness, staged migration, and rollback. |

---

## Generative AI (GenAI)

### LLM Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What is a large language model, and what kinds of tasks is it suitable for?** | Describes next-token language modeling in practical terms and gives suitable examples without claiming guaranteed factual correctness. |
| Low | **What is the difference between prompting and fine-tuning an LLM?** | Explains that prompting changes the input while fine-tuning changes model weights, with an appropriate use case for each. |
| Mid | **How would you integrate an LLM API into an application while managing timeouts, errors, rate limits, and user feedback?** | Covers input and output validation, retries where safe, fallback behavior, logging, cost controls, and a user-facing error path. |
| Mid | **A chatbot gives fluent but unsupported answers. How would you diagnose and reduce the problem?** | Separates missing context, prompt, retrieval, and model failures; then adds abstention, citations, better context, and regression tests. |
| Mid | **How would you manage prompt and model changes so a production LLM behavior is reproducible?** | Versions prompts, models, configurations, and evaluation inputs, captures release evidence, and supports controlled rollback. |
| Mid | **What basic controls would you add before exposing an LLM application to external users?** | Covers authentication, input and output handling, data minimization, rate limits, safe logging, user feedback, and abuse monitoring. |
| High | **How do transformer architecture and context length affect the latency and cost of an LLM feature?** | Explains tokenization, attention and KV-cache costs, input and output token budgets, batching, model selection, and context-management trade-offs. |
| High | **A product team wants to use a larger model because demo quality is better. How would you make the production decision?** | Compares task-level quality and failure modes against latency, throughput, reliability, privacy, and total cost under production traffic. |
| High | **How would you determine whether fine-tuning is justified rather than using few-shot prompting or RAG?** | Identifies the failure type, data quantity and quality, maintenance burden, evaluation plan, safety implications, and the incremental value over simpler approaches. |
| High | **How would you design tool calling for an LLM that can create tickets or update business records?** | Uses strict schemas, least privilege, confirmation for impactful actions, server-side authorization, idempotency, audit logs, and recovery from partial failure. |
| High | **What would you monitor to detect that an LLM feature is becoming less useful or less safe after launch?** | Monitors task success, abstention and escalation, groundedness, policy violations, user feedback, latency, cost, model or prompt versions, and segment behavior. |
| High | **How would you explain an LLM limitation or uncertainty to a business stakeholder without overstating its capabilities?** | Gives a calibrated explanation with concrete examples, measurable evidence, known failure modes, guardrails, and a proposed validation path. |

### RAG Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What is Retrieval-Augmented Generation, and why can it improve an LLM answer?** | Explains retrieval of relevant external information before generation, plus the need to validate the retrieved source. |
| Low | **What role do embeddings and a vector database play in a RAG system?** | Explains semantic vector representations and similarity retrieval, and notes that metadata or keyword search can complement them. |
| Mid | **A RAG assistant retrieves relevant-looking documents but gives poor answers. How would you isolate the failure?** | Separately evaluates ingestion, chunking, retrieval recall, ranking, context assembly, generation, citations, and the answer rubric. |
| Mid | **How would you keep a RAG index current while preventing deleted or unauthorized content from being returned?** | Designs incremental updates and deletes, versioning, access-control filters at query time, reindexing, auditability, and freshness monitoring. |
| High | **How would you evaluate whether citations in a RAG response are useful and faithful across a regulated knowledge base?** | Checks that cited passages are retrieved, relevant, support each claim, use stable source locations, honor permissions, and avoid unsupported or misleading claims. |
| High | **How would you reduce retrieval latency for a large corpus without silently lowering answer quality?** | Establishes quality and latency baselines, then considers filtering, index tuning, caching, candidate limits, hybrid retrieval, reranking, and regression evaluation. |

### Agents Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What makes an AI agent different from a chatbot that only responds to a message?** | Identifies a goal, planning or state, tool use, observation of results, and bounded multi-step execution. |
| Low | **What kinds of tools might an agent use, and why should their permissions be limited?** | Gives practical examples and explains least privilege, validation, and the risk of external side effects. |
| Mid | **How would you decide whether a workflow needs one agent, multiple specialized agents, or deterministic orchestration?** | Favors the simplest reliable design, evaluates task decomposition and uncertainty, assigns ownership, constrains communication, and measures coordination overhead. |
| Mid | **An agent repeatedly retries a failing tool call and increases operational cost. How would you prevent and diagnose that behavior?** | Uses timeouts, retry budgets, idempotency, circuit breakers, state-aware stopping, traces, alerts, and explicit escalation paths. |
| High | **How would you evaluate an agent that executes multi-step workflows with external side effects?** | Builds scenario and adversarial suites, verifies tool-call correctness and final state, measures recovery and unsafe-action rates, and includes human review where needed. |
| High | **How would you use MCP or a similar protocol to expose internal tools safely to an agent with external side effects?** | Defines narrow typed tools, authenticates and authorizes at the server, scopes credentials, validates inputs and outputs, logs actions, and requires confirmation where needed. |

---

## Infrastructure (Infra)

### Infrastructure Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What is the difference between a virtual machine and a container?** | Explains operating-system isolation, resource sharing, packaging, and a practical use case without treating containers as a full security boundary. |
| Low | **What does a load balancer do for a web service?** | Explains traffic distribution, health checks, availability, and the need for multiple healthy backend instances. |
| Mid | **How would you choose between a virtual machine, a managed container platform, and serverless for a new workload?** | Weighs runtime needs, scaling, operations, latency, cost, networking, portability, and team expertise against requirements. |
| Mid | **How would you design secrets and service identities for a workload that accesses a database and a third-party API?** | Uses workload identity, least privilege, managed secret storage, rotation, network restrictions, auditing, and no embedded credentials. |
| High | **How would you prepare a stateful application for a regional outage?** | States recovery objectives, assesses dependency and data replication limits, chooses active-active or active-passive, defines failover, tests it, and documents operations. |
| High | **How would you reduce cloud spend across a multi-account platform without weakening reliability or security?** | Uses cost allocation and usage data, rightsizes resources, reviews storage and data transfer, schedules non-production workloads, protects critical capacity, and prevents unsafe savings. |

### Observability, Deployment & Monitoring

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What basic metrics would you monitor for a deployed API or model endpoint?** | Includes latency, error rate, throughput, availability, and resource usage; for models, also prediction or data-quality signals when available. |
| Low | **What is the difference between logs, metrics, and traces?** | Distinguishes event details, aggregated numerical time series, and request paths across components with a practical example for each. |
| Mid | **How would you roll out a risky release through CI/CD while preserving a fast rollback path?** | Uses automated checks, immutable artifacts, progressive delivery or flags, health and business guardrails, observability, ownership, and reversible migrations. |
| Mid | **What would you log for a model inference request, and what data should you avoid storing?** | Includes request correlation, model and feature versions, validation outcome, latency, errors, and safe output metadata while minimizing or protecting personal and sensitive data. |
| High | **An alert fires frequently but rarely indicates a user-impacting issue. How would you redesign the alerting strategy?** | Reviews alert history and impact, defines service-level objectives and error budgets, tunes thresholds or duration, uses symptom-based signals, adds routing and runbooks, and measures alert quality. |
| High | **How would you verify that a deployment improved reliability rather than merely changing the metrics?** | Compares a defined baseline and time window, checks user-facing service levels and error budgets, controls for traffic, and reviews regressions by segment. |

### Solutions Architecture & System Design

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What is scalability, and what is the difference between vertical and horizontal scaling?** | Explains handling increasing work by adding resources to one machine or adding instances, including the basic trade-offs. |
| Low | **What problem does caching solve, and what risk does it introduce?** | Explains lower latency and backend load alongside stale data, invalidation, and security considerations. |
| Mid | **A read-heavy service must respond quickly worldwide. How would you design caching without serving incorrect or sensitive data?** | Defines cache keys, TTL and invalidation, consistency needs, authorization boundaries, cache placement, fallback behavior, metrics, and capacity limits. |
| Mid | **How would you design for partial failures between a web service, queue, and database?** | Uses timeouts, bounded retries with backoff, idempotency, durable messages, dead-letter handling, reconciliation, and observable failure states. |
| High | **How would you make a trade-off between lower latency, higher availability, and lower cost for a customer-facing feature?** | Quantifies requirements and traffic, identifies the bottleneck and business impact, compares options, states assumptions, and proposes measurable guardrails. |
| High | **How would you migrate a critical service to a new architecture without disrupting users?** | Uses incremental compatibility patterns, contract tests, feature flags, shadow or dual-run validation, data reconciliation, monitoring, and rollback. |

---

## Others

### Communication Skills

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **How would you explain a simple model result to a non-technical stakeholder?** | Uses plain language, defines the decision and key limitation, avoids unsupported certainty, and checks the listener's understanding. |
| Low | **How would you report a data-quality issue to the person relying on the data?** | States the impact, known facts, uncertainty, immediate workaround if any, and when the next update will be provided. |
| Mid | **Tell us how you would handle conflicting feedback from engineering, product, and compliance on an AI feature.** | Clarifies goals and constraints, listens for underlying concerns, makes trade-offs explicit, records decisions, and escalates appropriately. |
| Mid | **How would you present an experiment result that is statistically uncertain but time-sensitive?** | Explains uncertainty and limitations plainly, gives risk-aware options, requests only necessary follow-up data, and avoids claiming certainty. |
| High | **How would you ensure a handoff of a production data or AI system is understandable to the team that will operate it?** | Provides concise documentation, ownership, runbooks, access and dependency details, known limitations, training, a verification path, and escalation routes. |
| High | **Describe how you would push back on a request for an unrealistic AI capability while keeping executives and delivery teams aligned.** | Clarifies the intended outcome, explains technical limits in plain language, presents evidence and safer alternatives, and proposes a testable next step. |

### Domain Knowledge

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **What would you ask to understand the business decision an AI or data product is meant to support?** | Identifies the user, decision, desired outcome, current process, constraints, and how success will be recognized. |
| Low | **How would you learn the meaning of an unfamiliar business metric before using it in analysis?** | Finds the owner and definition, checks the calculation and grain, reviews known caveats, and validates it against real workflow examples. |
| Mid | **How would you detect that a technically strong model optimizes the wrong business outcome?** | Connects labels and metrics to real decisions, checks incentives and proxies, examines segment effects, and uses stakeholder validation and experiments. |
| Mid | **What questions would you ask a domain expert before using their historical decisions as training labels?** | Asks about policy changes, bias, consistency, exceptions, timing, missing cases, incentives, and whether labels represent desired outcomes. |
| High | **How would you assess whether available data represents the population and workflow where a high-impact model will be used?** | Compares coverage, sampling, time periods, segments, collection processes, feedback loops, and harm risks; then documents gaps and mitigations. |
| High | **How would you decide when a rules-based workflow is more appropriate than an ML or LLM solution for a regulated decision?** | Compares ambiguity, data, explainability, change frequency, error cost, latency, maintenance, governance, and expected value against a simple baseline. |

### Problem Resolution Skills

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **A report suddenly has fewer rows than yesterday. What simple checks would you perform first?** | Checks source availability, dates, filters, row counts, schema changes, and recent pipeline or query changes before drawing conclusions. |
| Low | **A stakeholder reports an incorrect value in a dashboard. How would you begin investigating?** | Reproduces the issue, clarifies the expected result and scope, traces the metric definition and source data, and communicates findings. |
| Mid | **How would you resolve a disagreement between two valid technical approaches when both have incomplete evidence?** | Defines the decision and constraints, makes assumptions visible, runs the smallest discriminating experiment, considers reversibility, and records the decision. |
| Mid | **A data pipeline is correct most days but fails unpredictably at scale. How would you find the root cause?** | Narrows the failure with telemetry and reproducible slices, examines load, data skew, dependencies, timing, and resource limits, then validates a durable fix. |
| High | **How would you respond when an incident has multiple contributing causes across teams?** | Coordinates a blameless response, separates mitigation from root-cause analysis, maps contributing factors, assigns owned actions, and verifies their effectiveness. |
| High | **A high-value AI project is missing its quality target despite several iterations. How would you decide whether to continue, redesign, or stop it?** | Reassesses problem framing, data and label limits, baseline value, technical risks, alternatives, cost of delay, and explicit decision criteria. |

### Testing & QA

| Level | Question | What a strong answer should cover |
|---|---|---|
| Low | **How would you choose between a unit, integration, and end-to-end test for a new feature?** | Matches each test level to the behavior and risk, favoring fast unit coverage with focused integration and critical user-flow tests. |
| Low | **What test cases would you write for a function that cleans incoming customer records?** | Covers valid input, missing and malformed values, boundaries, duplicates, expected transformations, errors, and the documented contract. |
| Mid | **How would you test a bug fix so the same defect does not return?** | Creates a minimal regression test that fails before the fix, verifies the fix, and checks relevant neighboring behavior. |
| Mid | **How would you test code that calls an external API without making tests slow or unreliable?** | Uses stubs or fakes for deterministic unit tests, validates contracts separately, and reserves real integration calls for controlled environments. |
| High | **What test strategy would you use before approving a change to a data transformation consumed by critical reports and models?** | Verifies expected outputs, edge cases, schema compatibility, reconciliation, data quality, performance, downstream impact, release controls, and rollback. |
| High | **A test passes locally but fails intermittently in CI. How would you find and eliminate the underlying source of flakiness?** | Uses logs and reproduction, checks isolation, ordering, timing, dependencies, configuration, and resource contention, then validates a durable fix. |
