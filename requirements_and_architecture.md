# BankBot v1.5 — Requirements and Architecture Document

**Project Name:** BankBot v1.5  
**Project Title:** Agentic AI Banking Assistant  
**Version:** 1.0  
**Status:** Implemented — Final Integration and Documentation  
**Banking Identity:** Ready Bank (Fictional)  
**Primary Objective:** Portfolio-oriented Agentic AI application

---

## 1. Project Overview

BankBot v1.5 is an Agentic AI-powered banking assistant developed to provide banking information, perform financial calculations, analyze simulated transaction data, and support customer-service workflows.

Unlike the original BankBot v1, which primarily focused on document-based question answering through Retrieval-Augmented Generation (RAG), v1.5 introduces a tool-using AI agent capable of interpreting user requests, selecting appropriate tools, and executing tasks through LangGraph.

The application combines a modular Streamlit interface, a Groq-hosted language model, OpenRouter embeddings, FAISS-based document retrieval, and an SQLite database.

The system supports banking knowledge retrieval, loan assistance, EMI calculations, eligibility estimation, simulated complaint management, and transaction analysis.

The application uses Ready Bank, a fictional banking institution, with synthetic banking policies and simulated customer data.

**Important:** Ready Bank is fictional. BankBot v1.5 is an educational and portfolio project, not an operational banking system.

## 2. Project Objectives

1. Upgrade a conventional RAG chatbot into a tool-using Agentic AI assistant.
2. Implement intelligent task routing and tool execution using LangGraph.
3. Provide a modern, interactive banking interface using Streamlit.
4. Integrate deterministic Python tools for banking calculations and simulated banking operations.
5. Support conversational context through LangGraph thread-based state management.
6. Implement validation, error handling, and human approval for consequential simulated actions.
7. Integrate document retrieval into the agent as a banking knowledge tool.
8. Demonstrate practical applications of RAG, LLM tool calling, agent orchestration, and human-in-the-loop workflows.

## 3. Project Scope

### 3.1 Implemented Scope

- Ready Bank banking knowledge assistant.
- RAG-based document retrieval.
- Single-agent orchestration using LangGraph.
- LLM-based tool selection and execution.
- Loan EMI and interest calculations.
- Preliminary loan eligibility assessment.
- Loan product comparison.
- Simulated complaint registration and tracking.
- Human approval and rejection of complaint registration requests.
- Synthetic customer and account records.
- Simulated transaction history.
- Spending summaries and category-wise analysis.
- Monthly spending analysis.
- Conversation state management.
- Agent activity and tool execution history.
- Structured result presentation.
- RAG source information in assistant responses.
- Modular Streamlit dashboard with seven navigation pages.
- SQLite-based data persistence.

### 3.2 Out of Scope

- Real banking integrations.
- Actual financial transactions.
- Official loan approval or credit decisions.
- Real customer authentication.
- Access to real customer account information.
- Submission of real banking applications.
- Modification of actual bank records.
- Multiple autonomous agents.
- Live banking web search.
- Advanced hybrid retrieval using BM25.
- Automated anomaly or fraud detection.

## 4. Functional Requirements

### FR-01: Banking Knowledge Assistant

The system shall:

- Answer banking questions using the Ready Bank knowledge base.
- Retrieve relevant information from supported knowledge documents.
- Use semantic similarity search through FAISS.
- Generate embeddings using an OpenRouter-hosted embedding model.
- Present relevant source information in the assistant interface.
- Maintain conversational context through the agent's thread state.
- Route calculation and operational questions to appropriate tools when required.
- Provide fallback responses when the knowledge base cannot support an answer.

### FR-02: Agent Orchestration

The system shall:

- Interpret natural-language user requests.
- Identify the required banking capability.
- Select appropriate tools through LLM tool calling.
- Execute selected tools through LangGraph.
- Support requests requiring multiple tool interactions.
- Ask follow-up questions when required information is missing.
- Process tool outputs and generate consolidated responses.
- Maintain conversation state using thread identifiers.
- Pause workflows when human approval is required.

The initial implementation uses a single intelligent agent with multiple specialized tools rather than multiple autonomous agents.

### FR-03: Loan Assistance

The system shall:

- Provide information about available loan products.
- Perform preliminary loan eligibility assessments.
- Calculate estimated EMIs.
- Calculate total interest and repayment amounts.
- Compare available loan products based on their interest rates.
- Explain calculation results.

Eligibility assessments are estimates based on configured criteria and do not represent official loan approvals.

### FR-04: Banking Calculation Tools

The system shall provide deterministic Python tools for:

- EMI calculation.
- Total interest calculation.
- Total repayment calculation.
- Preliminary loan eligibility assessment.
- Loan product comparison.

The LLM selects the appropriate tool, while Python performs the actual calculations.

### FR-05: Complaint Management

The system shall:

- Accept simulated customer complaints.
- Validate complaint categories and descriptions.
- Generate complaint reference numbers.
- Store complaints in SQLite.
- Request explicit user approval before registration.
- Allow users to approve or reject pending registrations.
- Retrieve complaint details and current status.

Complaint registration uses LangGraph's human-in-the-loop interrupt and resume workflow.

### FR-06: Transaction Analysis

The system shall:

- Access synthetic customer, account, and transaction records.
- Retrieve account transaction history.
- Calculate spending summaries.
- Generate category-wise spending summaries.
- Generate monthly spending summaries.
- Validate account references and transaction filters.
- Count only successful debit transactions when calculating spending.

The current implementation does not include automated fraud detection, recurring transaction detection, or unusual transaction identification.

### FR-07: Workflow Execution and Approval

The system shall:

- Execute tool-based tasks through LangGraph.
- Maintain workflow state during agent execution.
- Record actual tool calls and their results.
- Pause complaint registration when approval is required.
- Resume the workflow following user approval or rejection.
- Present execution status through the Streamlit interface.

### FR-08: Conversation Management

The system shall:

- Maintain conversation state using LangGraph thread identifiers.
- Support follow-up questions within a conversation.
- Preserve relevant messages during agent interactions.
- Support separate conversation threads for different application workflows.
- Display agent execution history through the Activity page.

Conversation persistence is managed through the configured LangGraph checkpointer.

## 5. User Interface Requirements

The application uses Streamlit with a modular, banking-inspired interface.

### Main Navigation

1. Dashboard
2. AI Assistant
3. Loans
4. Transactions
5. Support
6. Activity
7. Settings

### Dashboard

- Welcome section.
- Demo account count.
- Transaction count.
- Active complaint count.
- Navigation shortcuts.
- Quick access to major banking features.

### AI Assistant

- Interactive chat interface.
- Suggested questions.
- Conversation management.
- Structured result presentation.
- Expandable RAG source information.
- Agent activity display.
- Complaint approval and rejection interface.

### Loans

- EMI calculator.
- Loan product comparison.
- Preliminary eligibility assessment.
- Structured calculation results.

### Transactions

- Transaction history.
- Spending summaries.
- Category-wise spending analysis.
- Monthly spending analysis.

### Support

- Simulated complaint registration.
- Human approval and rejection.
- Complaint tracking.
- Complaint status display.

### Activity

- Actual agent tool execution history.
- Tool names and execution status.
- Tool input arguments.
- Tool results.

### Settings

- Current application theme information.
- Light and Dark theme support through the main application interface.

## 6. Non-functional Requirements

- Maintain modular and maintainable Python code.
- Keep presentation, agent, tool, database, and retrieval responsibilities separate.
- Prefer free or low-cost hosted model services.
- Store API credentials in environment variables.
- Validate user inputs and tool arguments.
- Handle database and model-service errors.
- Use synthetic customer and transaction data.
- Record agent tool execution activity for transparency.
- Preserve human approval for complaint registration.
- Avoid exposing API credentials in application output.
- Clearly distinguish simulated banking results from real financial decisions.

## 7. Implemented Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Frontend | Streamlit |
| LLM provider | Groq |
| Agent orchestration | LangGraph |
| LLM integration | LangChain |
| Embedding provider | OpenRouter |
| Embedding integration | LangChain OpenAI integration |
| Vector search | FAISS |
| Document processing | PyPDF |
| Text splitting | LangChain Text Splitters |
| Database | SQLite |
| Environment configuration | Python dotenv |

The application uses hosted language-model and embedding services to avoid the resource requirements of running large models locally.

## 8. High-Level Architecture

The application follows a modular architecture consisting of the following layers:

1. **Presentation Layer:** Streamlit pages and shared UI components.
2. **Agent Layer:** LangGraph orchestration, tool selection, execution, and conversation state.
3. **Tool Layer:** Banking calculations, loan operations, complaint management, transaction analysis, and knowledge retrieval.
4. **Knowledge Layer:** Document loading, chunking, embeddings, FAISS indexing, and retrieval.
5. **Data Layer:** SQLite database, synthetic banking records, and local vector storage.
6. **Configuration Layer:** Environment-based API and model configuration.

### Agent Execution Flow

User Request → LangGraph Agent → LLM Tool Selection → Tool Execution → Result Processing → Human Approval if Required → Response Generation → Streamlit Presentation.

### RAG Execution Flow

Knowledge Documents → Document Loading → Text Splitting → Embedding Generation → FAISS Vector Index → Similarity Retrieval → Knowledge Tool → Agent Response.

### Complaint Approval Flow

Complaint Request → Validation → Approval Interrupt → User Decision → Workflow Resume → Complaint Registration or Cancellation → Result Presentation.

The approval process prevents complaint registration from proceeding without explicit user confirmation.

## 9. Project Structure

The project is organized into modular directories to separate application responsibilities.

```text
Bankbot_v1_5/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── agents/
│   └── graph.py
│
├── database/
│   ├── db.py
│   ├── complaint_repository.py
│   └── transaction_repository.py
│
├── tools/
│   ├── complaint_tools.py
│   ├── loan_tools.py
│   ├── transaction_tools.py
│   └── knowledge_tool.py
│
├── rag/
│   └── ...
│
├── ui/
│   ├── common.py
│   ├── dashboard.py
│   ├── assistant.py
│   ├── loans.py
│   ├── transactions.py
│   ├── support.py
│   ├── activity.py
│   └── settings.py
│
├── tests/
│   └── ...
│
├── knowledge/
│   └── ...
│
└── vector_store/
    └── faiss_index/
```

The tree above illustrates the main architectural organization. Additional implementation files, data files, and test modules may exist within the directories.

## 10. Development Roadmap and Implementation Status

**Phase 1 — Requirements and Architecture**
- Requirements and architecture defined.
- Project scope and technology stack established.

**Status:** Completed.

**Phase 2 — Project Setup and UI Foundation**
- Independent project environment created.
- Dependencies configured.
- Streamlit dashboard implemented.
- Navigation and theme switching implemented.
- Seven modular application pages completed.

**Status:** Completed.

**Phase 3 — Knowledge and RAG Layer**
- Ready Bank knowledge documents prepared.
- Document loading and text splitting implemented.
- OpenRouter embeddings integrated.
- FAISS vector index created.
- Semantic retrieval integrated.
- Knowledge retrieval exposed through an agent tool.

**Status:** Completed.

**Phase 4 — Agent Foundation**
- LangGraph agent implemented.
- LLM tool selection configured.
- Tool execution integrated.
- Conversation state and thread management implemented.
- RAG tool integrated with the agent.

**Status:** Completed.

**Phase 5 — Banking Tools**
- EMI calculation implemented.
- Loan eligibility assessment implemented.
- Loan comparison implemented.
- Structured calculation results integrated.

**Status:** Completed for the implemented loan capabilities.

**Phase 6 — Banking Workflows**
- Complaint registration and tracking implemented.
- Human approval and rejection integrated.
- SQLite customer, account, and transaction data implemented.
- Transaction history and spending analysis implemented.
- Agent activity tracking integrated.

**Status:** Completed for the implemented workflows.

**Phase 7 — Evaluation and Reliability**
- Individual banking tools tested.
- Database operations validated.
- Transaction analysis tested.
- RAG retrieval and agent integration tested.
- Complaint approval workflow tested.
- UI integration verified.

**Status:** Core implementation and integration testing completed.

**Phase 8 — Portfolio Release**
- Application integration completed.
- Dashboard metrics integrated.
- README and architecture documentation prepared.
- Final project review and repository preparation.

**Status:** Documentation and final release preparation.

## 11. Evaluation Strategy

The implementation has been evaluated across the following areas:

- RAG retrieval and relevance.
- Knowledge-grounded agent responses.
- Tool selection and execution.
- EMI calculation correctness.
- Loan eligibility validation.
- Loan comparison results.
- Database operations.
- Transaction spending calculations.
- Complaint approval and cancellation.
- Structured result presentation.
- Agent activity visibility.
- Streamlit navigation and theme behavior.

Evaluation is based on functional tests and integration checks. Formal benchmark targets for retrieval precision, recall, latency, and cost have not been established.

## 12. Safety and Data Boundaries

- Ready Bank is a fictional institution.
- All customer, account, and transaction records are synthetic.
- No real financial transactions are executed.
- No real loan applications are submitted.
- Loan eligibility results are estimates, not official decisions.
- Complaint registration requires explicit user approval.
- API credentials are loaded through environment variables.
- The application does not provide access to real bank accounts.
- Database operations are limited to the simulated application environment.

## 13. Definition of Project Success

BankBot v1.5 demonstrates a functional Agentic AI banking assistant when a user can:

1. Ask banking questions and receive knowledge-based responses.
2. Request loan calculations and receive deterministic estimates.
3. Check preliminary loan eligibility.
4. Compare available loan products.
5. Register simulated complaints with explicit approval.
6. Track complaint status.
7. Review synthetic transaction records.
8. Analyze spending through summaries and category-wise and monthly breakdowns.
9. Interact with the agent across conversation turns.
10. Observe actual tool execution through the Activity interface.
11. Navigate a modular banking dashboard with Light and Dark themes.

The final deliverable demonstrates a working Agentic AI application combining RAG, LangGraph tool orchestration, deterministic banking tools, SQLite persistence, and human-in-the-loop approval rather than a conventional document-question-answering chatbot.

---

**End of Document**