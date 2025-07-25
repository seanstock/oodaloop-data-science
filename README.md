```


..#######...#######..########.....###....##........#######...#######..########.....########...######.
.##.....##.##.....##.##.....##...##.##...##.......##.....##.##.....##.##.....##....##.....##.##....##
.##.....##.##.....##.##.....##..##...##..##.......##.....##.##.....##.##.....##....##.....##.##......
.##.....##.##.....##.##.....##.##.....##.##.......##.....##.##.....##.########.....##.....##..######.
.##.....##.##.....##.##.....##.#########.##.......##.....##.##.....##.##...........##.....##.......##
.##.....##.##.....##.##.....##.##.....##.##.......##.....##.##.....##.##...........##.....##.##....##
..#######...#######..########..##.....##.########..#######...#######..##...........########...######.
                                                                                    
                                     
```

# ooda

A command-line tool to scaffold a data science project structure, optimized for a collaborative workflow between a user and an AI agent in a Databricks environment.

This project reimagines the role of data science through the lens of the OODA loop: Observe, Orient, Decide, Act. Rather than treating analysis as an end, it frames data work as part of a continuous cycle of perception and adaptation. The goal is not just insight, but action—executed faster, with greater clarity, and in closer contact with reality.

## Overview

`ooda` quickly sets up a standardized directory structure and template files, allowing you to bypass manual setup and begin analysis immediately. It establishes a clear, interactive workflow where the user handles project setup and data access, and the agent assists with analysis, planning, and code generation.

## Features

- Creates a standard project directory structure (`docs`, `notebooks`, `metadata`, `sql`, `.cursor/rules`).
- Generates template files, including a pre-populated `analysis_brief.md` to kickstart the project.
- Creates a `.env` file to securely store your Databricks credentials.
- Provides a starter Jupyter notebook (`exploration.ipynb`) with boilerplate for a `databricks-connect` session.
- Includes pre-configured `.mdc` rule files to guide the agent's personality and workflow.

## Installation

To install the package from the project root, run:
```bash
pip install -e .
```

## Workflow

The `ooda` tool is designed for an interactive session between you (the user) and an AI agent.

### 1. Project Initialization (User)

Create and navigate to a new, empty directory for your project, then run the initializer.
```bash
mkdir my-new-ds-project && cd my-new-ds-project
ooda init
```

### 2. Authentication (User)

Configure your Databricks credentials. This command helps you set up the `.env` file.
```bash
ooda auth
```
Follow the prompts to set your `DATABRICKS_HOST` and `DATABRICKS_TOKEN`. You can also manually edit the `.env` file to add your `WAREHOUSE_ID`, `CATALOG`, and `SCHEMA`.

### 3. Analysis Brief (User)

Open `docs/analysis_brief.md` and edit it to describe the project goals, hypotheses, and data sources. The template is pre-populated with examples.

### 4. Generate Analysis Plan (Agent)

Once the brief is ready, instruct the agent to create the analysis plan.
**User Prompt:** *"create the analysis plan"*

The agent will read the brief, generate a detailed `docs/analysis_plan.md`, and then offer to refine it based on table metadata.

### 5. Data Exploration (User & Agent)
- **User:** Use `ooda list-catalog` and `ooda expand-table <table_name>` to explore available data and generate schema files in the `metadata/` directory.
- **Agent:** With the metadata available, the agent can now write targeted SQL queries (saved to `sql/`) and perform analysis in `notebooks/exploration.ipynb`.

## Command Reference

| Command | Description |
|---|---|
| `ooda init` | Initializes the project structure in the current directory. |
| `ooda auth` | Interactively sets Databricks credentials in the `.env` file. |
| `ooda list-catalog` | Lists available tables in your configured Databricks catalog. |
| `ooda expand-table <table_name>`| Fetches the schema for a table and saves it to `metadata/`. |

## Project Structure

The `init` command will generate the following structure in your project directory:
```
.
├── .cursor/
│   └── rules/
│       ├── KnowledgeBase.mdc
│       ├── PracticalModifications.mdc
│       └── PrimaryWorkflow.mdc
├── docs/
│   ├── analysis_brief.md
│   └── analysis_plan.md
├── metadata/
├── notebooks/
│   └── exploration.ipynb
├── sql/
└── .env
``` 