# Employee Performance Management (Odoo 18 Enterprise)

## Overview
A comprehensive, scalable, and modular Employee Performance Management System built for Odoo 18. This module provides HR teams with the tools to define hierarchical performance metrics (KRA > KPA > KPI), structure performance templates, and conduct seamless performance evaluations for employees.

## Key Features
- **Hierarchical Metrics**: Manage Key Result Areas (KRAs), Key Performance Areas (KPAs), and Key Performance Indicators (KPIs).
- **Flexible Templates**: Create reusable Performance Templates for different roles (e.g., Software Developer, Sales Executive).
- **Review Cycles**: Group performance reviews by periods (Monthly, Quarterly, Yearly).
- **Multi-Level Evaluation**: Support for Employee Self-Reviews and Manager Reviews.
- **Automated Scoring**: Automatically computes KPI, KPA, and KRA scores based on target values, completion values, and custom weightages.
- **Dynamic Dashboard**: Centralized dashboard providing key insights and pending reviews at a glance.

---

## Step-by-Step Usage Guide

### 1. Configure Masters (The Building Blocks)
Before assigning any performance templates, you need to define the underlying structure.
* **KRA Master** (`Employee Performance > Masters > KRA Master`):
  Create top-level Key Result Areas (e.g., "Software Development", "Team Leadership"). Set the overall weightage and review frequency.
* **KPA Master** (`Employee Performance > Masters > KPA Master`):
  Under each KRA, define specific Key Performance Areas. For example, under "Software Development", you might have "Code Quality" and "Feature Delivery".
* **KPI Master** (`Employee Performance > Masters > KPI Master`):
  Under each KPA, define the exact metrics. For example, under "Feature Delivery", you might add "On-Time Delivery Rate". Set the target value, measurement type (percentage, number, etc.), and weightage for the calculation.

### 2. Configure Evaluation Rules
* **Rating Scales** (`Employee Performance > Masters > Rating Scale`):
  Define how scores translate to ratings (e.g., `Needs Improvement: 0-69`, `Good: 70-79`, `Outstanding: 90-100`).
* **Review Cycles** (`Employee Performance > Masters > Review Cycles`):
  Create a period for the review (e.g., "Annual Review 2024" or "Q1 2024"). You will use this cycle to group employee assignments together.

### 3. Create Performance Templates
* **Performance Templates** (`Employee Performance > Masters > Performance Templates`):
  Bundle the KRAs, KPAs, and KPIs you created into a single template that represents a specific job role (e.g., "Senior Python Developer Template").

### 4. Assign to Employees
* **Employee Assignments** (`Employee Performance > Performance > Employee Assignments`):
  Select an employee, their manager, the active Review Cycle, and the appropriate Performance Template. Click **Start Assignment** to change the status to 'Running'.

### 5. Conduct Reviews
* **Self Review** (`Employee Performance > Performance > Self Reviews`):
  The employee opens their assigned review, adds their completed values against the KPI target values, attaches relevant documents, and provides remarks. The system automatically calculates progress and scores based on the weights.
* **Manager Review** (`Employee Performance > Performance > Manager Reviews`):
  The manager reviews the employee's self-assessment, provides an overriding rating if needed, and adds qualitative remarks and suggested improvements.

### 6. Final Evaluation
* **Final Evaluations** (`Employee Performance > Performance > Final Evaluations`):
  Based on the Self and Manager reviews, HR or the Manager can generate the final evaluation. By clicking **Calculate Score**, the system rolls up the scores from KPI to KPA to KRA and outputs a final overall percentage and Performance Rating based on your Rating Scale.

---

## Architecture & Technical details
This module follows a clean architecture model:
- **`models/`**: Clean definitions of data structures, keeping business logic out of model declarations.
- **`services/`**: Complex business logic, like nested score computation (`score_calculator.py`), is handled by abstract service models for better reusability and testing.
- **`views/`**: Implements professional Odoo 18 features including notebooks, kanban dashboards, stat buttons, and web ribbons. `<list>` tags are strictly used for Odoo 18 compatibility.

## Future Scope
The database is structured specifically so that future integrations can be added without altering the core performance models. Expected upcoming integrations:
- **Project & Timesheets**: Link KPIs directly to logged timesheets and task completion rates.
- **CRM & Sales**: Automate sales KPIs by directly fetching invoiced amounts or deals won.
- **Attendance & HR**: Tie punctuality and leave counts directly to performance metrics.
