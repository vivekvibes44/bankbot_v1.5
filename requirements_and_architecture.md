# BankBot v1.5 — Requirements and Architecture Document

**Project Name:** BankBot v1.5  
**Project Title:** Agentic AI Banking Assistant  
**Version:** 1.0  
**Status:** Proposed — Pre-development  
**Banking Identity:** Ready Bank (fictional)  
**Primary Objective:** Portfolio-oriented Agentic AI application

---

## 1. Project Overview

BankBot v1.5 is an Agentic AI-powered banking assistant designed to provide banking information, perform calculations, analyze simulated financial data, and execute multi-step customer-support workflows.

Unlike the original BankBot v1, which primarily focuses on document-based question answering through Retrieval-Augmented Generation (RAG), v1.5 introduces an intelligent agent capable of selecting and executing tools based on user requirements.

The application will feature an improved, interactive Streamlit interface designed to resemble a modern fintech banking application.

The project will use Ready Bank, a fictional banking institution, with synthetic banking policies and simulated customer data.

**Important:** Ready Bank is fictional. This application is an educational and portfolio project, not an operational banking system.

## 2. Project Objectives

1. Upgrade a conventional RAG chatbot into a tool-using Agentic AI assistant.
2. Introduce intelligent task routing and multi-step workflow execution.
3. Improve the user experience through a modern, interactive banking dashboard.
4. Integrate deterministic Python tools for banking calculations and operations.
5. Support conversational context across multiple interactions.
6. Implement validation, error handling, and human approval for consequential simulated actions.
7. Demonstrate practical applications of RAG, LLM tool calling, and agent orchestration.

## 3. Project Scope

### 3.1 In Scope

- Ready Bank banking knowledge assistant.
- RAG-based document retrieval.
- Single-agent orchestration.
- Tool calling and execution.
- Loan assistance and eligibility estimation.
- EMI and interest calculations.
- Banking product comparisons.
- Personalized document checklists.
- Simulated complaint registration and tracking.
- Simulated transaction analysis.
- Multi-step workflow execution.
- Conversation and workflow history.
- Modern Streamlit dashboard.
- Source citations and response grounding.
- Agent execution logging and evaluation.

### 3.2 Out of Scope

- Real banking integrations.
- Actual financial transactions.
- Real loan approval or credit decisions.
- Real customer authentication.
- Access to real customer account information.
- Autonomous submission of real banking applications.
- Direct modification of actual bank records.
- Multiple autonomous agents in the initial release.

## 4. Functional Requirements

### FR-01: Banking Knowledge Assistant

The system shall:

- Answer questions using the Ready Bank knowledge base.
- Retrieve relevant information from structured and unstructured documents.
- Support semantic retrieval and metadata filtering.
- Present supporting source information.
- Maintain conversational context.
- Handle unsupported questions using a defined fallback.
- Avoid generating unsupported banking policies or figures.

### FR-02: Agent Orchestration

The system shall:

- Understand natural-language requests.
- Identify the required task or capability.
- Select appropriate tools.
- Execute multiple tools when necessary.
- Handle missing information by asking follow-up questions.
- Validate tool outputs.
- Maintain task state.
- Return a consolidated response.

### FR-03: Loan Assistance

The system shall:

- Retrieve loan product information.
- Collect relevant applicant details.
- Perform preliminary eligibility checks.
- Calculate estimated EMIs.
- Compare available loan products.
- Generate document checklists.
- Explain results and their supporting policies.

All eligibility assessments shall be estimates, not official approvals.

### FR-04: Banking Calculation Tools

The system shall provide deterministic tools for:

- EMI calculation.
- Interest calculation.
- Loan eligibility assessment.
- Banking fee calculation.
- Loan product comparison.

The LLM shall select tools where appropriate, while Python performs the actual calculations.

### FR-05: Complaint Management

The system shall:

- Understand and categorize complaints.
- Request missing information.
- Retrieve relevant troubleshooting guidance.
- Create simulated complaint tickets.
- Generate ticket references.
- Retrieve ticket status.

### FR-06: Transaction Analysis

The system shall:

- Access synthetic transaction records.
- Categorize expenses.
- Calculate spending summaries.
- Compare spending across periods.
- Identify recurring transactions.
- Flag unusual transaction patterns.
- Generate visual summaries.

### FR-07: Multi-step Workflow Execution

The system shall:

- Convert user goals into executable steps.
- Execute tasks in a controlled sequence.
- Track workflow progress.
- Handle incomplete or failed steps.
- Request approval before consequential simulated actions.
- Save workflow results.

### FR-08: Conversation Management

The system shall:

- Maintain conversation history.
- Resolve follow-up questions using relevant context.
- Preserve important workflow information.
- Support multiple conversations.
- Avoid unnecessary repetition of previously collected information.

## 5. User Interface Requirements

The application shall use Streamlit with a modern fintech-inspired design.

### Main Navigation

1. Dashboard
2. AI Assistant
3. Loans
4. Accounts and Banking Information
5. Transactions
6. Customer Support
7. Conversation and Workflow History

### Dashboard

- Personalized welcome section.
- Quick-action cards.
- Available banking services.
- Recent workflow activity.
- Navigation to major features.

### AI Assistant

- Interactive chat interface.
- Conversation history.
- Quick prompts.
- Rich response cards.
- Expandable source citations.
- Agent activity panel.
- Workflow progress indicators.

### Loan Section

- Loan product comparison.
- Interactive EMI calculator.
- Preliminary eligibility assessment.
- Document checklist.

### Transaction Section

- Spending summaries.
- Category-wise charts.
- Transaction tables.
- Period comparisons.

### Customer Support Section

- Complaint creation.
- Ticket tracking.
- Troubleshooting guidance.

## 6. Non-functional Requirements

- Maintain modular and maintainable code.
- Keep frontend and backend responsibilities separate.
- Prefer free or low-cost hosted model services.
- Secure API keys using environment variables.
- Validate user inputs and tool arguments.
- Handle API failures and rate limits gracefully.
- Use synthetic customer and transaction data.
- Maintain logs for agent execution and tool calls.
- Support evaluation of retrieval and agent performance.
- Prevent unauthorized or unintended simulated actions.

## 7. Proposed Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Frontend | Streamlit |
| LLM | Groq-hosted model |
| Agent orchestration | LangGraph |
| LLM integration | LangChain |
| Embeddings | OpenRouter |
| Vector search | FAISS |
| Keyword search | Optional BM25 |
| Database | SQLite |
| Data validation | Pydantic |
| Data processing | Pandas |
| Visualization | Plotly |
| Web search | Tavily, optional fallback |

Technology choices may be revised after testing compatibility, performance, and API availability.

## 8. High-Level Architecture

The application will follow a modular architecture consisting of:

1. Presentation Layer — Streamlit interface.
2. Agent Layer — LangGraph orchestration and state management.
3. Tool Layer — Banking calculations, retrieval, database operations, and workflow actions.
4. Knowledge Layer — Document ingestion, embeddings, vector retrieval, and citations.
5. Data Layer — SQLite and synthetic banking datasets.
6. Validation Layer — Input validation, output verification, approval controls, and logging.

### Agent Execution Flow

User Request → Intent Understanding → Tool Selection → Tool Execution → Result Validation → Approval if Required → Response Generation → Workflow State Update.

The initial architecture will use one intelligent agent with multiple specialized tools, rather than multiple autonomous agents.

## 9. Proposed Project Structure

BankBot_v1_5/

- app.py
- config.py
- requirements.txt
- .env

agents/
- graph.py
- state.py
- nodes.py
- routing.py

tools/
- knowledge_tool.py
- loan_tools.py
- calculation_tools.py
- complaint_tools.py
- transaction_tools.py

rag/
- ingest.py
- loaders.py
- chunking.py
- embeddings.py
- retrieval.py
- citations.py

database/
- db.py
- models.py
- synthetic_data.py

ui/
- dashboard.py
- assistant.py
- loans.py
- transactions.py
- support.py

evaluation/
- retrieval_tests.py
- agent_tests.py
- workflow_tests.py

utils/
- validators.py
- logging_config.py

knowledge/
- accounts/
- loans/
- fees/
- digital_banking/
- eligibility/
- faq/

vector_store/
- faiss_index/

## 10. Development Roadmap

**Phase 1 — Requirements and Architecture**
- Finalize requirements.
- Finalize architecture.
- Define user workflows.
- Establish project structure.

**Phase 2 — Project Setup and UI Foundation**
- Create an independent project environment.
- Configure dependencies.
- Build the Streamlit dashboard.
- Implement navigation and page layouts.

**Phase 3 — Knowledge and RAG Layer**
- Prepare Ready Bank knowledge documents.
- Implement ingestion and metadata handling.
- Configure embeddings and FAISS.
- Implement retrieval and citations.

**Phase 4 — Agent Foundation**
- Introduce LangGraph.
- Define agent state.
- Integrate the RAG pipeline as a tool.
- Implement tool selection and execution.

**Phase 5 — Banking Tools**
- Implement EMI and interest calculations.
- Implement loan eligibility checks.
- Implement loan comparison.
- Generate document checklists.

**Phase 6 — Banking Workflows**
- Implement complaint management.
- Add simulated transaction analysis.
- Add multi-step task execution.
- Implement workflow history and approval controls.

**Phase 7 — Evaluation and Reliability**
- Evaluate retrieval quality.
- Test tool selection.
- Validate calculation accuracy.
- Test multi-step workflows.
- Test failure handling and grounding.

**Phase 8 — Portfolio Release**
- Refine the UI.
- Prepare demo scenarios.
- Document architecture and implementation.
- Prepare GitHub README and project presentation.

## 11. Evaluation Strategy

The project shall be evaluated across:

- Retrieval precision and recall.
- Answer faithfulness and relevance.
- Citation correctness.
- Tool-selection accuracy.
- Calculation correctness.
- Workflow completion rate.
- Error handling and reliability.
- Execution latency and API cost.

Performance targets shall be defined after baseline testing.

## 12. Safety and Data Boundaries

- All banking policies shall belong to the fictional Ready Bank.
- All customer and transaction data shall be synthetic.
- No real financial transactions shall be executed.
- No real loan applications shall be submitted.
- Consequential simulated actions shall require user confirmation.
- Sensitive information shall not be exposed in logs or responses.
- Banking recommendations shall clearly distinguish estimates from official decisions.

## 13. Definition of Project Success

BankBot v1.5 shall be considered successful when a user can:

1. Ask banking questions and receive source-grounded answers.
2. Request a loan assessment and receive calculated estimates.
3. Compare loan products and obtain document checklists.
4. Register and track simulated complaints.
5. Analyze synthetic transaction records.
6. Complete multi-step tasks through the agent.
7. Observe the agent's activity through the interface.
8. Review previous conversations and workflow results.

The final deliverable shall demonstrate a functional, visually polished Agentic AI banking application rather than a conventional document-question-answering chatbot.

---

**End of Document**