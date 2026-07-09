# Example questions and answers about these topics

## Machine Learning (ML)

### Machine Learning Basics

#### Junior

**Q:** What is the difference between supervised, unsupervised, and reinforcement learning?

**A:** Supervised learning trains on examples with known labels, such as predicting churn from
historical customers. Unsupervised learning finds structure in unlabeled data, such as clusters
or latent topics. Reinforcement learning trains an agent to choose actions through rewards and
penalties from an environment.

**Q:** Can you explain the difference between classification and regression?

**A:** Classification predicts a discrete category, such as spam versus not spam or low, medium,
and high risk. Regression predicts a continuous numeric value, such as price, demand, or delivery
time.

#### Mid

**Q:** How would you handle an imbalanced classification dataset?

**A:** First, I would choose metrics that reflect the business goal, such as precision, recall,
F1-score, or PR-AUC instead of accuracy. Then I would consider stratified splitting, class weights,
over-sampling, under-sampling, synthetic examples, threshold tuning, and error analysis by segment.
I would also validate that any resampling only happens inside the training fold to avoid leakage.

**Q:** What is overfitting, and what techniques can reduce it?

**A:** Overfitting happens when a model learns noise or overly specific patterns from the training
data and performs poorly on unseen data. It can be reduced with more representative data, simpler
models, regularization, cross-validation, early stopping, dropout, pruning, data augmentation, and
careful feature selection.

#### Expert

**Q:** How would you design an ML solution when labels are noisy, incomplete, or expensive to obtain?

**A:** I would start by quantifying label quality, ambiguity, and coverage across key data segments.
Then I would combine approaches such as active learning, weak supervision, human-in-the-loop review,
semi-supervised learning, label consensus, robust loss functions, and confidence-based filtering.
The evaluation set should be curated carefully, because a noisy test set can hide real improvements
or reward the wrong behavior.

**Q:** How would you decide whether a traditional ML model is preferable to a deep learning model?

**A:** I would compare the data type, dataset size, latency needs, interpretability requirements,
maintenance cost, and expected performance. Traditional models are often better for tabular data,
small datasets, fast iteration, and explainability. Deep learning is usually preferable when the
input is high-dimensional or unstructured, such as images, audio, text, or multimodal data, and
there is enough data or transfer learning support.

### Deep Learning Basics

#### Junior

**Q:** What is a neural network, and what role do neurons and layers play?

**A:** A neural network is a model made of connected computational units that transform inputs into
predictions. Neurons compute weighted combinations of inputs and pass the result through activation
functions. Layers organize neurons so the model can learn progressively more complex representations.

**Q:** What is the purpose of an activation function?

**A:** An activation function introduces non-linearity into the network. Without it, stacked layers
would behave like a single linear model and could not learn complex patterns. Common examples are
ReLU, sigmoid, tanh, GELU, and softmax.

#### Mid

**Q:** How do backpropagation and gradient descent work together during training?

**A:** Backpropagation computes how much each parameter contributed to the prediction error by
applying the chain rule from the output layer back to earlier layers. Gradient descent then uses
those gradients to update parameters in the direction that reduces the loss. Repeating this process
lets the network gradually improve.

**Q:** What are common causes of vanishing or exploding gradients?

**A:** They often come from very deep networks, poor weight initialization, saturating activation
functions, high learning rates, unnormalized inputs, and recurrent connections over long sequences.
Vanishing gradients make early layers learn too slowly, while exploding gradients make training
unstable. Techniques such as ReLU variants, residual connections, normalization, gradient clipping,
and better initialization help reduce the problem.

#### Expert

**Q:** How would you debug a deep learning model that fails to converge?

**A:** I would verify the data pipeline first: labels, preprocessing, batching, class balance, and
train-validation splits. Then I would check whether the model can overfit a tiny dataset, inspect
loss curves and gradients, test simpler baselines, tune learning rate and optimizer settings, and
look for numerical instability. If needed, I would add instrumentation for activations, gradients,
and prediction distributions.

**Q:** How would you optimize a deep learning model for both accuracy and inference latency?

**A:** I would define target latency, throughput, hardware, and acceptable accuracy trade-offs before
optimizing. Then I would combine architecture selection, pruning, quantization, distillation,
operator fusion, batching, caching, compilation, and hardware-aware profiling. The final choice
should be validated with real production-like traffic, not only benchmark datasets.

### Model Evaluation

#### Junior

**Q:** What is the difference between accuracy, precision, recall, and F1-score?

**A:** Accuracy measures the overall fraction of correct predictions. Precision measures how many
positive predictions were actually positive. Recall measures how many real positives the model found.
F1-score is the harmonic mean of precision and recall, which is useful when both matter.

**Q:** Why do we split data into training, validation, and test sets?

**A:** The training set is used to fit the model, the validation set is used to tune choices such as
features and hyperparameters, and the test set is used for a final unbiased estimate. This split
helps detect overfitting and avoids judging a model on data it already influenced.

#### Mid

**Q:** When would ROC-AUC be misleading, and what metric would you use instead?

**A:** ROC-AUC can be misleading with highly imbalanced datasets because false positive rates may
look small even when the number of false positives is operationally large. In those cases, PR-AUC,
precision at K, recall at a fixed precision, cost-weighted metrics, or calibration metrics may be
more useful. The best metric depends on the decision threshold and business cost of each error type.

**Q:** How would you evaluate a model used in a business-critical decision process?

**A:** I would evaluate predictive quality, calibration, fairness across segments, robustness,
explainability, operational impact, and failure costs. I would also define approval criteria with
stakeholders, compare against the current process, review edge cases, and include human override
or audit mechanisms when decisions have high consequences.

#### Expert

**Q:** How would you design an offline and online evaluation strategy for a production ML model?

**A:** Offline evaluation should use representative holdout data, time-based splits when relevant,
segment metrics, calibration checks, stress tests, and comparisons with baselines. Online evaluation
should use shadow deployments, A/B tests, canaries, guardrail metrics, and monitoring for data,
model, system, and business outcomes. Both layers should connect model metrics to measurable product
or business impact.

**Q:** How would you detect whether a model's performance degradation is caused by data drift or
concept drift?

**A:** I would compare current input and feature distributions against training or recent stable
periods to detect data drift. To detect concept drift, I would analyze whether the relationship
between inputs and labels has changed, using delayed labels, proxy outcomes, segment-level errors,
and calibration changes. Data drift can exist without worse performance, so the diagnosis needs
both distribution monitoring and outcome-based evaluation.

---

## Software (SW)

### Software Engineering Basics

#### Junior

**Q:** What is the difference between a function, a class, and a module?

**A:** A function is a reusable block of logic that takes inputs and may return a result. A class is
a blueprint for objects that combine data and behavior. A module is a file or package that groups
related functions, classes, constants, and other code.

**Q:** Why is code readability important in software engineering?

**A:** Readable code is easier to understand, review, debug, test, and extend. Most software cost
comes after the first implementation, so clarity reduces defects and helps teams move faster over
time.

#### Mid

**Q:** How would you refactor duplicated logic in a codebase?

**A:** I would first confirm that the duplicated logic truly represents the same concept and is not
only accidentally similar. Then I would extract a shared function, class, module, or service at the
right abstraction level, add tests around the behavior, and migrate call sites incrementally. I would
avoid a shared abstraction if it makes independent use cases harder to evolve.

**Q:** What principles would you follow to design maintainable software?

**A:** I would aim for clear responsibilities, small cohesive modules, explicit interfaces, simple
data flow, meaningful names, automated tests, and observability. I would also keep dependencies
directional, isolate business rules from infrastructure details, and optimize for changes the
system is likely to need.

#### Expert

**Q:** How would you evaluate whether a codebase needs refactoring or a larger architectural change?

**A:** I would look at defect patterns, delivery bottlenecks, coupling, testability, scalability
limits, onboarding difficulty, and how often local changes require broad edits. Refactoring is
usually enough when the architecture still supports the product direction but implementation quality
is slowing the team. A larger architectural change is justified when core boundaries, data ownership,
runtime constraints, or scaling needs no longer match the business problem.

**Q:** How would you balance technical debt reduction with product delivery pressure?

**A:** I would make technical debt visible in terms of risk, cycle time, defect rate, and operational
cost. Then I would prioritize debt that blocks near-term product work, increases incident risk, or
compounds quickly. The practical approach is often to reserve capacity for targeted improvements,
include cleanup in feature work, and avoid large rewrites unless the return is clear.

### Software Development Cycle

#### Junior

**Q:** What are the main stages of the software development lifecycle?

**A:** Common stages are planning, requirements analysis, design, implementation, testing, deployment,
operation, and maintenance. Modern teams may repeat these stages iteratively rather than following
them once in a strict sequence.

**Q:** What is the purpose of code review?

**A:** Code review improves quality by finding defects, checking maintainability, sharing knowledge,
and aligning code with team standards. It also helps protect important system behaviors before code
reaches production.

#### Mid

**Q:** How would you manage requirements that change during development?

**A:** I would clarify the reason for the change, assess impact on scope, design, tests, delivery,
and users, then update priorities with stakeholders. I would keep the implementation modular so
changes are easier to absorb, and I would document decisions so the team understands the current
direction.

**Q:** What is the difference between agile, waterfall, and iterative development?

**A:** Waterfall follows a sequential process where each phase is largely completed before the next
starts. Agile emphasizes short feedback cycles, collaboration, and adapting priorities as new
information appears. Iterative development builds software through repeated increments and can exist
inside agile or non-agile processes.

#### Expert

**Q:** How would you improve a development process with frequent production defects?

**A:** I would classify defects by root cause, affected system area, detection point, and business
impact. Then I would improve the highest-leverage controls: clearer requirements, smaller changes,
better code review, automated tests, CI gates, staging parity, observability, feature flags, and
post-incident learning. The goal is to catch defects earlier and make production failures safer.

**Q:** How would you design a release strategy for a high-risk production feature?

**A:** I would use feature flags, progressive rollout, canary deployment, shadow traffic when useful,
strong monitoring, rollback plans, and clear ownership during launch. I would define success and
guardrail metrics in advance, validate migrations separately, and avoid coupling irreversible data
changes to the first user-facing release.

### Agents Knowledge

#### Junior

**Q:** What is an AI agent, and how is it different from a simple chatbot?

**A:** An AI agent can reason about a goal, choose actions, use tools, observe results, and continue
working across multiple steps. A simple chatbot usually responds only to the current message without
autonomously planning or acting in external systems.

**Q:** What are examples of tools an agent might use?

**A:** An agent might use search engines, databases, APIs, code interpreters, calendars, email
systems, file storage, ticketing tools, browsers, terminals, and internal business applications.
Tool access should be limited to what the task requires.

#### Mid

**Q:** How would you design an agent that can call external APIs safely?

**A:** I would define allowed APIs, strict schemas, authentication boundaries, rate limits, retries,
timeouts, and validation for inputs and outputs. Sensitive or destructive actions should require
confirmation, policy checks, audit logs, and idempotency. The agent should also handle API errors
without leaking secrets or taking unsafe fallback actions.

**Q:** What are common failure modes of autonomous agents?

**A:** Common failures include hallucinated plans, incorrect tool use, prompt injection, infinite
loops, poor state tracking, unsafe actions, brittle assumptions, weak error handling, and overuse of
tools. Agents can also optimize for the wrong objective if success criteria are vague.

#### Expert

**Q:** How would you design a multi-agent system with coordination, memory, and task delegation?

**A:** I would define agent roles, ownership boundaries, shared protocols, task routing, memory
scope, conflict resolution, and a supervisor or orchestrator for coordination. Memory should separate
short-term task context, long-term knowledge, and auditable decisions. Delegation should be observable,
bounded, and evaluated against clear completion criteria.

**Q:** How would you evaluate reliability and safety in an agent-based system?

**A:** I would create scenario-based evaluations that cover normal tasks, edge cases, adversarial
inputs, tool failures, permission boundaries, and long-running workflows. Metrics should include
task success, error recovery, unsafe action rate, policy violations, latency, cost, and human
intervention rate. Production monitoring and audit trails are essential because agents can fail in
unexpected ways.

### Software Architecture Patterns

#### Junior

**Q:** What is the MVC pattern, and why is it useful?

**A:** MVC separates an application into Model, View, and Controller responsibilities. The Model
handles data and business rules, the View handles presentation, and the Controller handles user
input and coordination. This separation improves maintainability and testability.

**Q:** What is the difference between monolithic and micro-services architecture?

**A:** A monolith packages most application functionality into one deployable unit. Micro-services
split functionality into independently deployable services with their own boundaries and often their
own data ownership. Micro-services can improve independent scaling and team autonomy, but they add
distributed system complexity.

#### Mid

**Q:** When would you use event-driven architecture?

**A:** I would use event-driven architecture when independent components need to react to state
changes asynchronously, such as order processing, notifications, analytics, or integrations. It is
useful for decoupling producers and consumers, smoothing traffic spikes, and enabling extensibility.
It requires careful handling of ordering, retries, idempotency, and observability.

**Q:** What are the trade-offs of using a layered architecture?

**A:** Layered architecture improves separation of concerns, testability, and consistency by placing
responsibilities into layers such as presentation, domain, application, and persistence. The trade-off
is that it can add boilerplate, indirection, and performance overhead if applied too rigidly. It works
best when boundaries are clear and dependencies flow in controlled directions.

#### Expert

**Q:** How would you choose between micro-services, modular monolith, and serverless architecture?

**A:** I would consider domain complexity, team structure, deployment independence, scaling patterns,
operational maturity, latency, cost, and compliance needs. A modular monolith is often a strong
default when boundaries are still evolving. Micro-services fit when domains and teams need independent
ownership, while serverless fits event-driven workloads, variable traffic, and low infrastructure
management needs.

**Q:** How would you evolve an architecture without disrupting existing users?

**A:** I would use incremental migration patterns such as strangler fig, feature flags, compatibility
layers, dual writes with reconciliation, shadow reads, and contract testing. Observability, rollback
paths, and clear migration checkpoints reduce risk. User-facing behavior should remain stable while
internal components are replaced behind controlled interfaces.

### System Design

#### Junior

**Q:** What is scalability, and why does it matter in system design?

**A:** Scalability is a system's ability to handle more users, data, traffic, or work without failing
or becoming too slow. It matters because systems often need to grow while preserving reliability,
performance, and cost efficiency.

**Q:** What is the difference between vertical and horizontal scaling?

**A:** Vertical scaling means adding more resources to one machine, such as more CPU, memory, or disk.
Horizontal scaling means adding more machines or instances and distributing the workload across them.
Horizontal scaling is usually more flexible but requires distributed system design.

#### Mid

**Q:** How would you design a URL shortener?

**A:** I would expose an API to create short links, generate or encode unique keys, store mappings in
a durable database, and redirect users from short URLs to long URLs with low latency. I would add
caching for popular links, rate limiting, abuse prevention, analytics, expiration rules, and collision
handling. The design should optimize reads because redirects usually dominate writes.

**Q:** How would you design a notification system that supports email, SMS, and push notifications?

**A:** I would separate notification creation from delivery using queues and channel-specific workers.
The system should manage templates, user preferences, provider integrations, retries, deduplication,
rate limits, and delivery status. It should also support observability and fallback behavior when one
channel or provider fails.

#### Expert

**Q:** How would you design a highly available real-time recommendation system?

**A:** I would combine offline model training, near-real-time feature pipelines, low-latency feature
serving, model serving, caching, and fallback recommenders. High availability would require
replication across zones, graceful degradation, circuit breakers, monitoring, and rollback for model
or feature issues. The serving path should be optimized separately from the training and analytics
paths.

**Q:** How would you design a distributed system that handles partial failures and eventual consistency?

**A:** I would assume network, node, dependency, and message failures are normal. The design should
use timeouts, retries with backoff, idempotency keys, durable queues, replication, quorum or consensus
where needed, and reconciliation jobs. For eventual consistency, I would make state transitions
explicit, expose clear user expectations, and monitor lag and conflict resolution.

---

## Infrastructure / DevOps / MLOps (Infra)

### Infrastructure Knowledge

#### Junior

**Q:** What is the difference between a server, a container, and a virtual machine?

**A:** A server is a physical or virtual machine that runs workloads. A virtual machine emulates a
complete machine with its own operating system on top of a hypervisor. A container packages an
application and its dependencies while sharing the host operating system kernel, making it lighter
than a virtual machine.

**Q:** What is the role of a load balancer?

**A:** A load balancer distributes incoming traffic across multiple backend instances. It improves
availability, scalability, and performance by avoiding overload on a single instance and routing
traffic away from unhealthy ones.

#### Mid

**Q:** How would you deploy an application using containers?

**A:** I would create a Docker image with the application and dependencies, scan and version it, push
it to a registry, and deploy it to a runtime such as Kubernetes, ECS, Cloud Run, or Docker Compose.
The deployment should include configuration management, secrets handling, health checks, resource
limits, logging, monitoring, and a rollback strategy.

**Q:** What are common reasons for infrastructure outages?

**A:** Common causes include bad deployments, capacity exhaustion, dependency failures, network
issues, expired certificates, misconfigured DNS, database overload, region or zone failures, security
incidents, and insufficient observability. Human error often contributes when changes are manual or
poorly reviewed.

#### Expert

**Q:** How would you design infrastructure for a system with unpredictable traffic spikes?

**A:** I would use autoscaling, load balancing, caching, queues, rate limiting, CDN support, and
graceful degradation. Capacity planning should include stress testing and clear saturation metrics.
For critical workloads, I would pre-warm infrastructure or keep baseline capacity when cold starts
or scaling delays would hurt users.

**Q:** How would you improve reliability across multiple regions or availability zones?

**A:** I would deploy redundant services across zones, replicate data according to recovery needs,
and use health-based traffic routing. For multi-region reliability, I would define active-active or
active-passive strategy, recovery time objectives, recovery point objectives, failover procedures,
and regular disaster recovery tests. Data consistency and operational complexity must be designed
explicitly.

### Model Deployment

#### Junior

**Q:** What does it mean to deploy a machine learning model?

**A:** Deploying a machine learning model means making it available for real use, such as through an
API, batch job, embedded application, or streaming service. Deployment also includes packaging the
model, dependencies, preprocessing, monitoring, and version control.

**Q:** What is the difference between batch inference and real-time inference?

**A:** Batch inference generates predictions for many records on a schedule or large job, such as
daily risk scores. Real-time inference returns predictions immediately for individual or small groups
of requests, such as fraud detection during checkout.

#### Mid

**Q:** How would you deploy a model behind an API endpoint?

**A:** I would package the model with the same preprocessing used in training, expose a prediction
endpoint, validate input schemas, and return structured outputs with confidence or metadata when
useful. The service should include authentication, rate limits, logging, monitoring, autoscaling,
health checks, and versioned artifacts. I would also test latency, throughput, and failure behavior.

**Q:** What are the risks of deploying a new model version to production?

**A:** Risks include worse accuracy on real traffic, data preprocessing mismatches, latency increases,
dependency issues, biased behavior, poor calibration, incompatible output schemas, and unexpected
business impact. A new model can also fail silently if monitoring only checks service health and not
prediction quality.

#### Expert

**Q:** How would you design a blue-green or canary deployment strategy for ML models?

**A:** For blue-green deployment, I would run the current and new model environments separately,
validate the new one, then switch traffic when it passes checks. For canary deployment, I would send
a small percentage of traffic to the new model and progressively increase it if quality, latency,
cost, and business guardrails stay healthy. Both strategies need rollback, version tracking, and
segment-level monitoring.

**Q:** How would you handle rollback, versioning, and reproducibility for deployed models?

**A:** I would version model artifacts, code, data snapshots, feature definitions, preprocessing,
dependencies, configuration, and evaluation results. Rollback should restore both the model and its
compatible serving pipeline. Reproducibility requires metadata lineage, immutable artifacts, and
documented training and deployment procedures.

### MLOps - Observability & Monitoring

#### Junior

**Q:** What metrics would you monitor for a deployed ML model?

**A:** I would monitor service metrics such as latency, throughput, error rate, and resource usage,
plus ML metrics such as prediction distribution, confidence, feature drift, missing values, and
eventual accuracy when labels arrive. Business metrics connected to model decisions are also
important.

**Q:** What is data drift?

**A:** Data drift is a change in the distribution of input data compared with the data used to train
or validate the model. It can happen because user behavior, seasonality, upstream systems, or the
environment changes.

#### Mid

**Q:** How would you detect that a model is degrading in production?

**A:** I would monitor delayed ground-truth metrics when labels are available and use proxy metrics
when they are not. I would also track prediction distributions, calibration, drift, segment-level
performance, business outcomes, and user feedback. Alerts should distinguish model-quality problems
from infrastructure or data pipeline failures.

**Q:** What logs and metrics would you collect for an ML inference service?

**A:** I would collect request IDs, model version, input schema validation results, selected features,
prediction output, confidence, latency, errors, resource usage, and downstream decision metadata.
Sensitive data should be minimized, masked, or stored under strict controls. Metrics should support
debugging, monitoring, auditing, and retraining decisions.

#### Expert

**Q:** How would you design an observability platform for multiple ML models in production?

**A:** I would create a common telemetry layer that captures service health, data quality, drift,
prediction behavior, model versions, feature lineage, labels, and business outcomes across models.
The platform should support dashboards, alerts, segment analysis, experiment tracking, audit logs,
and integration with incident management. It should also standardize schemas while allowing each
model to define domain-specific metrics.

**Q:** How would you connect business KPIs with technical ML monitoring metrics?

**A:** I would map each model decision to the business process it influences and define leading and
lagging indicators. Technical metrics such as drift, calibration, recall, latency, and coverage
should be connected to KPIs such as conversion, fraud loss, retention, cost, or customer satisfaction.
Dashboards and alerts should show both layers so teams can see whether technical changes affect
business outcomes.

### Architecture Design

#### Junior

**Q:** What is the difference between application architecture and infrastructure architecture?

**A:** Application architecture describes how software components, modules, services, and data flows
are organized. Infrastructure architecture describes the compute, network, storage, security, and
deployment environment that runs the application.

**Q:** Why is redundancy important in infrastructure design?

**A:** Redundancy provides backup capacity when a component fails. It improves availability by
removing single points of failure, such as one server, database instance, network path, or zone.

#### Mid

**Q:** How would you design infrastructure for a web application with a database and background workers?

**A:** I would use a load balancer in front of stateless web instances, a managed database with
backups and replicas as needed, a queue for background jobs, and separate worker instances to process
them. The design should include secrets management, networking, autoscaling, logging, monitoring,
CI/CD, migrations, and disaster recovery plans.

**Q:** How would you decide between managed cloud services and self-managed infrastructure?

**A:** I would compare operational burden, control, cost, compliance, scalability, reliability,
vendor lock-in, team expertise, and customization needs. Managed services are often better when the
team wants reliability and speed with less maintenance. Self-managed infrastructure can fit when
requirements demand deep control or specialized behavior.

#### Expert

**Q:** How would you design a secure, scalable, multi-environment cloud architecture?

**A:** I would separate environments such as development, staging, and production with clear network,
identity, data, and access boundaries. The architecture should use infrastructure as code, least
privilege IAM, private networking, encryption, secret management, centralized logging, automated
policy checks, autoscaling, and deployment pipelines. Shared components should be standardized but
production controls should be stricter.

**Q:** How would you design infrastructure that supports compliance, disaster recovery, and cost
optimization?

**A:** I would start with regulatory and business requirements for data classification, retention,
availability, and recovery. Then I would implement access controls, encryption, audit logging,
backups, replication, disaster recovery testing, cost allocation, budgets, autoscaling, and lifecycle
policies. The architecture should make compliance evidence and cost visibility available by default.

---

## Generative AI (GenAI)

### Transformer Architecture Fundamentals

#### Junior

**Q:** What is a transformer model?

**A:** A transformer is a neural network architecture designed to process sequences using attention
mechanisms instead of relying mainly on recurrence. It is widely used for language, vision, audio,
and multimodal tasks because it learns relationships between tokens efficiently.

**Q:** What is the purpose of attention in transformers?

**A:** Attention lets the model decide which parts of the input are most relevant for each token or
prediction. It helps capture dependencies between words or elements even when they are far apart in
the sequence.

#### Mid

**Q:** How does self-attention work?

**A:** Self-attention creates query, key, and value representations for each token. It compares
queries with keys to compute attention weights, then uses those weights to combine values into a new
context-aware representation. This allows every token to incorporate information from other tokens
in the same sequence.

**Q:** What are positional embeddings, and why are they needed?

**A:** Positional embeddings encode the order or position of tokens in a sequence. Transformers need
them because self-attention alone treats inputs as a set and does not inherently know token order.
They can be learned, fixed, relative, or rotary depending on the architecture.

#### Expert

**Q:** How would you explain the computational bottlenecks of transformer architectures?

**A:** The main bottleneck is self-attention, which scales quadratically with sequence length in time
and memory because each token attends to many other tokens. Training also requires large matrix
multiplications, activation memory, optimizer state, and high-bandwidth communication across
accelerators. During inference, long context windows and key-value cache memory can limit throughput
and latency.

**Q:** How would you compare transformers with RNNs and CNNs for sequence modeling?

**A:** RNNs process sequences step by step and naturally model order, but they are harder to
parallelize and struggle with long-range dependencies. CNNs are efficient and parallelizable but
capture context through fixed or stacked receptive fields. Transformers model global dependencies
more directly and parallelize well during training, but they can be more expensive for long sequences.

### LLM Knowledge

#### Junior

**Q:** What is a large language model?

**A:** A large language model is a neural network trained on large amounts of text to predict and
generate language. It can perform tasks such as answering questions, summarizing, translating,
writing code, and following instructions.

**Q:** What is the difference between prompting and fine-tuning?

**A:** Prompting guides a model's behavior by changing the input instructions or examples without
changing model weights. Fine-tuning updates the model weights using additional training data so the
model better fits a task, style, or domain.

#### Mid

**Q:** What are common causes of hallucinations in LLMs?

**A:** Hallucinations can come from missing context, ambiguous prompts, outdated or incorrect
training data, overconfident generation, weak retrieval, and pressure to answer when the model should
say it does not know. They also occur because language models optimize plausible next tokens rather
than direct truth verification.

**Q:** How would you choose between using an API-based LLM and hosting an open-source model?

**A:** I would compare quality, latency, cost, data privacy, customization, compliance, operational
complexity, reliability, and expected traffic. API-based models are usually faster to adopt and often
have strong quality. Hosted open-source models can provide more control, data isolation, and
customization, but require infrastructure and ML operations maturity.

#### Expert

**Q:** How would you design a secure enterprise chatbot using LLMs?

**A:** I would define access control, data boundaries, retrieval permissions, audit logging, prompt
injection defenses, output filtering, and human escalation paths. The chatbot should use secure RAG
over approved knowledge sources, avoid exposing secrets, cite sources, and respect user-level
permissions. I would also add evaluations, monitoring, red-team tests, and incident response
procedures.

**Q:** How would you evaluate and improve LLM responses for quality, safety, and usefulness?

**A:** I would build evaluation sets with realistic user tasks, expected criteria, adversarial cases,
and domain-specific rubrics. Metrics should cover correctness, groundedness, helpfulness, safety,
format adherence, latency, and cost. Improvements can come from better prompts, retrieval, tool use,
fine-tuning, guardrails, feedback loops, and model selection.

### RAG Knowledge

#### Junior

**Q:** What is Retrieval-Augmented Generation?

**A:** Retrieval-Augmented Generation is a pattern where a system retrieves relevant external
information and provides it to a generative model before it answers. This helps the model use
knowledge outside its training data.

**Q:** Why is RAG useful for question-answering systems?

**A:** RAG is useful because it can answer using current or private documents without retraining the
model. It can also improve factual grounding and provide citations or source references for answers.

#### Mid

**Q:** How would you chunk documents for a RAG system?

**A:** I would choose chunk boundaries that preserve semantic meaning, such as sections, paragraphs,
or code blocks, instead of splitting only by fixed length. Chunk size should balance context
completeness with retrieval precision and model context limits. I would test overlap, metadata,
hierarchical chunks, and domain-specific parsing.

**Q:** What is the role of embeddings and vector databases in RAG?

**A:** Embeddings convert text into numeric vectors that capture semantic meaning. A vector database
stores those vectors and supports similarity search, so the system can retrieve chunks related to a
user query. Metadata filters and hybrid search often improve retrieval quality.

#### Expert

**Q:** How would you improve retrieval quality in a large-scale RAG system?

**A:** I would improve document parsing, chunking, metadata, embedding model selection, hybrid
search, query rewriting, reranking, and permission-aware filtering. I would also evaluate retrieval
with labeled queries, recall at K, source coverage, latency, and failure analysis by document type.
Feedback from real user interactions can guide indexing and ranking improvements.

**Q:** How would you evaluate hallucination, citation quality, and answer correctness in RAG?

**A:** I would evaluate whether answers are supported by retrieved sources, whether citations point
to the exact relevant evidence, and whether unsupported claims are avoided. This can combine human
review, automated checks, LLM-as-judge with strict rubrics, answer-source entailment, and adversarial
queries. I would track hallucination rate, citation precision, citation recall, and task success.

---

## Others

### Data Engineering Basics (Data)

#### Junior

**Q:** What is the difference between structured, semi-structured, and unstructured data?

**A:** Structured data has a fixed schema, such as relational database tables. Semi-structured data
has flexible organization with tags or keys, such as JSON, XML, or logs. Unstructured data has no
strict schema, such as images, audio, PDFs, and free text.

**Q:** What is an ETL pipeline?

**A:** An ETL pipeline extracts data from sources, transforms it into a usable format, and loads it
into a target system such as a data warehouse. Some systems use ELT, where raw data is loaded first
and transformed later.

#### Mid

**Q:** How would you design a pipeline to process daily customer events?

**A:** I would ingest events from source systems, validate schemas, store raw data, transform it into
clean tables, and publish curated datasets for analytics or ML. The pipeline should include
scheduling, partitioning, deduplication, late-arriving event handling, data quality checks, lineage,
monitoring, and retry mechanisms.

**Q:** What are common causes of poor data quality?

**A:** Common causes include missing values, duplicates, inconsistent formats, schema changes,
incorrect joins, delayed events, manual entry errors, upstream bugs, unclear definitions, and lack of
ownership. Poor quality often appears when data producers and consumers do not share contracts.

#### Expert

**Q:** How would you design a reliable data platform for analytics and machine learning?

**A:** I would design layered storage for raw, cleaned, and curated data, with strong metadata,
lineage, governance, access control, orchestration, and quality checks. The platform should support
batch and streaming ingestion, reproducible transformations, feature generation, monitoring, and
self-service discovery. Reliability depends on clear data contracts, observability, and ownership.

**Q:** How would you handle schema evolution, late-arriving data, and pipeline failures?

**A:** I would use schema registries or contracts, backward-compatible changes, versioned datasets,
and validation at ingestion. Late-arriving data can be handled with watermarks, partition
reprocessing, merge logic, and clear freshness expectations. Pipeline failures need retries,
checkpointing, idempotent writes, alerts, and recovery playbooks.

### Data Analytics Engineering (Data)

#### Junior

**Q:** What is the difference between a data lake, a data warehouse, and a data lakehouse?

**A:** A data lake stores large amounts of raw or semi-processed data in flexible formats. A data
warehouse stores structured, curated data optimized for analytics and reporting. A lakehouse combines
lake flexibility with warehouse features such as transactions, schema management, and query
performance.

**Q:** What is a streaming data service, and when would you use it instead of batch processing?

**A:** A streaming data service processes events continuously as they arrive, using systems such as
Kafka, Kinesis, Pub/Sub, or Event Hubs. I would use it when low-latency insights or actions are
needed, such as fraud detection, monitoring, personalization, or operational dashboards.

#### Mid

**Q:** How would you design an analytics pipeline that ingests events from a streaming service into a
data warehouse?

**A:** I would collect events into a streaming platform, validate schemas, write raw events to durable
storage, process or aggregate them with a streaming job, and load curated tables into the warehouse.
The design should include deduplication, ordering strategy, dead-letter queues, partitioning,
monitoring, lineage, and data quality checks.

**Q:** How would you ensure data quality and consistency across a data lake and a warehouse?

**A:** I would define data contracts, validation rules, reconciliation checks, transformation tests,
and shared business definitions. Lineage and metadata should show how warehouse tables derive from
lake data. Consistency can be improved with transactional table formats, idempotent pipelines, and
regular source-to-target audits.

#### Expert

**Q:** How would you design a big data platform that supports both real-time analytics and historical
reporting?

**A:** I would use streaming ingestion for low-latency events, durable object storage for raw and
historical data, processing engines for batch and streaming transformations, and serving layers for
dashboards, ad hoc analysis, and APIs. The architecture should unify metadata, governance, quality
checks, lineage, and access control. Historical backfills and real-time views should use compatible
definitions.

**Q:** How would you optimize cost, performance, and governance across streaming services, data lakes,
and warehouses?

**A:** I would optimize storage formats, partitioning, clustering, retention policies, workload
isolation, autoscaling, caching, and query patterns. Governance should include access controls,
classification, lineage, masking, and audit logs. Cost controls need usage attribution, budgets,
right-sized compute, lifecycle policies, and regular review of unused datasets or jobs.

### Testing & QA (QA)

#### Junior

**Q:** What is the difference between unit, integration, and end-to-end tests?

**A:** Unit tests verify small pieces of logic in isolation. Integration tests verify that multiple
components work together, such as an API and database. End-to-end tests verify a complete user flow
through the system from the user's perspective.

**Q:** Why is automated testing important?

**A:** Automated testing gives fast feedback that code still works after changes. It reduces manual
effort, catches regressions earlier, and gives teams more confidence when refactoring or releasing.

#### Mid

**Q:** How would you decide what test cases to write for a new feature?

**A:** I would start from requirements, user flows, business rules, edge cases, failure modes, and
integration points. Then I would choose the right level of test for each risk, with more unit tests
for logic and fewer but meaningful integration or end-to-end tests for critical workflows. I would
include both expected behavior and important error paths.

**Q:** What is the difference between mocking and stubbing?

**A:** Stubbing provides predefined responses for a dependency so the test can control behavior.
Mocking also verifies interactions, such as whether a dependency was called with expected arguments.
Both can make tests faster and more focused, but overuse can make tests brittle.

#### Expert

**Q:** How would you design a testing strategy for a distributed system?

**A:** I would combine unit tests, contract tests, integration tests, end-to-end tests, load tests,
chaos testing, and observability-based validation. The strategy should cover network failures,
timeouts, retries, idempotency, eventual consistency, data corruption, and dependency degradation.
Contract testing and local simulation help catch issues before full environment tests.

**Q:** How would you improve quality in a team with frequent regressions and low test coverage?

**A:** I would identify the highest-risk areas, add characterization tests around current behavior,
and require tests for new or changed code. Then I would improve CI reliability, code review focus,
test data management, release safety, and post-incident learning. The goal is gradual coverage growth
around business-critical paths, not chasing a coverage number without risk reduction.
