# Interview Prep & Learning Courses

A collection of hands-on, tutorial-style courses for learning Python, LangChain, LangGraph, Flask, JavaScript, TypeScript, and React. Each chapter is a runnable file with deep explanations, examples, and interview tips.

## Courses

### Python (`python_course/`)
Fundamentals from variables to practical projects. 9 chapters.

```bash
python python_course/ch1_variables_and_types.py
```

| Chapter | Topic |
|---------|-------|
| ch1 | Variables & Types |
| ch2 | Control Flow (if/else, loops) |
| ch3 | Data Structures (lists, dicts, tuples, sets) |
| ch4 | Functions (*args, **kwargs, lambda, decorators) |
| ch5 | Classes & OOP |
| ch6 | File I/O & Exceptions |
| ch7 | Advanced Features (generators, dataclasses, type hints) |
| ch8 | Modules, Packages & Virtual Environments |
| ch9 | Practical Mini-Projects |

### LangChain (`langchain_course/`)
From basics to a full RAG pipeline. 10 chapters.

```bash
python langchain_course/ch1_basics.py
```

| Chapter | Topic |
|---------|-------|
| ch1 | Basics (LLM connection, Runnables, invoke/stream/batch) |
| ch2 | Messages & Prompts |
| ch3 | Output Parsers |
| ch4 | Chains & LCEL |
| ch5 | Document Loaders |
| ch6 | Text Splitters |
| ch7 | Embeddings (HuggingFace) |
| ch8 | Vector Stores (ChromaDB) |
| ch9 | RAG Chain |
| ch10 | Capstone: Web Scraping RAG |

### LangGraph (`langgraph_course/`)
Agents, state management, and multi-agent workflows. 8 chapters.

```bash
python langgraph_course/ch1_what_is_langgraph.py
```

| Chapter | Topic |
|---------|-------|
| ch1 | What is LangGraph (graphs, nodes, edges, state) |
| ch2 | State Deep Dive (reducers, MessagesState) |
| ch3 | Conditional Edges (branching, loops) |
| ch4 | Tool-Calling Agents (ReAct, create_react_agent) |
| ch5 | Human-in-the-Loop (interrupt, checkpoints) |
| ch6 | Building a Custom Agent |
| ch7 | Multi-Agent Workflows |
| ch8 | Capstone: Research Agent |

### Flask (`flask_course/`)
Web development from hello world to a full app. 10 chapters.

```bash
python flask_course/ch1_hello_flask.py
```

| Chapter | Topic |
|---------|-------|
| ch1 | Hello Flask (app, routes, running server) |
| ch2 | Routes & URLs |
| ch3 | Templates (Jinja2) |
| ch4 | Forms & Validation |
| ch5 | Databases (SQLAlchemy) |
| ch6 | REST API |
| ch7 | Blueprints |
| ch8 | Middleware & Error Handlers |
| ch9 | Authentication |
| ch10 | Capstone: Bookmark Manager |

### JavaScript (`javascript_course/`)
JS from scratch, with Python comparisons throughout. 9 chapters.

```bash
node javascript_course/ch1_variables_and_types.js
```

| Chapter | Topic |
|---------|-------|
| ch1 | Variables & Types (let/const/var, == vs ===) |
| ch2 | Control Flow |
| ch3 | Functions (arrow functions, callbacks, closures) |
| ch4 | Arrays & Objects (map/filter/reduce, destructuring, spread) |
| ch5 | DOM & Events |
| ch6 | Async JavaScript (promises, async/await, fetch) |
| ch7 | ES6+ Features (modules, classes, generators) |
| ch8 | Error Handling |
| ch9 | Practical Projects |

### TypeScript (`typescript_course/`)
Type safety on top of JavaScript. 8 chapters.

```bash
npx tsx typescript_course/ch1_intro_and_basic_types.ts
```

| Chapter | Topic |
|---------|-------|
| ch1 | Intro & Basic Types |
| ch2 | Arrays, Objects & Interfaces |
| ch3 | Functions |
| ch4 | Unions, Intersections & Narrowing |
| ch5 | Generics |
| ch6 | Classes |
| ch7 | Utility Types |
| ch8 | Enums & Advanced Patterns |

### React (`react_course/`)
Components, hooks, and a full app with TypeScript. 10 chapters.

```bash
# Setup: npm create vite@latest myapp -- --template react-ts
# Copy chapter files into src/ and import in App.tsx
```

| Chapter | Topic |
|---------|-------|
| ch1 | Intro & JSX |
| ch2 | Props |
| ch3 | State & useState |
| ch4 | useEffect |
| ch5 | Events & Forms |
| ch6 | Lists & Conditional Rendering |
| ch7 | Custom Hooks |
| ch8 | Context & useReducer |
| ch9 | React Router |
| ch10 | Capstone: Task Manager |

## Interview Prep

Interactive quizzes with study guide mode — 30 questions each with detailed answers and interview tips.

```bash
# Python basics interview prep
python python_course/interview_python_basics.py          # quiz mode
python python_course/interview_python_basics.py study    # study guide

# LLM & Agents interview prep
python langchain_course/interview_llms_and_agents.py          # quiz mode
python langchain_course/interview_llms_and_agents.py study    # study guide
```

## Learning Order

**Backend path:** Python → Flask → LangChain → LangGraph

**Frontend path:** JavaScript → TypeScript → React
