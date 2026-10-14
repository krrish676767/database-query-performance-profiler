# Lab 5: Static Code Analysis — Employee Payroll System

## Student Information
- **Name:** Krrish P Raju
- **SRN:** PES1UG24CS708
- **Course:** UE23CS352B — Software Engineering Lab
- **Assigned Problem Statement:** #44 Employee Payroll System (`employee_payroll_system.py`)
- **Institution:** PES University, Department of Computer Science and Engineering

---

## Deliverables in this Directory

| Deliverable File | Description | Verification / Status |
| :--- | :--- | :--- |
| 💻 [`employee_payroll_system.py`](./employee_payroll_system.py) | **Cleaned & Hardened Python Codebase** | All Bandit security issues eliminated, Flake8 PEP 8 compliant, Pylint score **10.00/10**. |
| 📋 [`issues.md`](./issues.md) | **Completed Issues Identification Table** | Structured register mapping all detected defects, CWE IDs, line numbers, descriptions, and fix strategies. |
| 📝 [`reflection.md`](./reflection.md) | **Static Analysis Reflection Report** | Detailed analysis covering static vs. dynamic analysis, tool comparisons, vulnerability deep dive, and CI/CD quality gates. |
| 📄 [`pylint_report_before.txt`](./pylint_report_before.txt) | **Pylint Baseline Report (Before)** | Original static scan result showing **5.53/10** with 14 defects flagged. |
| 📄 [`pylint_report_after.txt`](./pylint_report_after.txt) | **Pylint Remediated Report (After)** | Verification scan demonstrating **10.00/10** score with 0 warnings. |
| 📄 [`pylint_report.txt`](./pylint_report.txt) | **Pylint Final Deliverable Report** | Verified final clean report (**10.00/10**). |
| 🔒 [`bandit_report_before.txt`](./bandit_report_before.txt) | **Bandit Baseline Report (Before)** | Baseline security scan identifying 5 issues (2 High, 1 Medium, 2 Low). |
| 🔒 [`bandit_report_after.txt`](./bandit_report_after.txt) | **Bandit Remediated Report (After)** | Security scan demonstrating 0 vulnerabilities detected. |
| 🔒 [`bandit_report.txt`](./bandit_report.txt) | **Bandit Final Deliverable Report** | Verified final security report (0 issues). |
| 🎨 [`flake8_report_before.txt`](./flake8_report_before.txt) | **Flake8 Baseline Report (Before)** | Baseline PEP 8 scan flagging line length, bare except, unused variables, and imports. |
| 🎨 [`flake8_report_after.txt`](./flake8_report_after.txt) | **Flake8 Remediated Report (After)** | 0 PEP 8 violations detected (100% clean). |
| 🎨 [`flake8_report.txt`](./flake8_report.txt) | **Flake8 Final Deliverable Report** | Verified final style report. |

---

## Static Code Analysis Summary

| Tool | Target Objective | Baseline (Before) | Post-Remediation (After) | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Bandit** | Eliminate all security vulnerabilities | 5 issues (2 High, 1 Med, 2 Low) | **0 issues identified** | ✅ **Passed** |
| **Pylint** | Achieve code quality score > 9.50 | 5.53 / 10.00 | **10.00 / 10.00** | ✅ **Passed** |
| **Flake8** | Enforce PEP 8 style & formatting | 6 violations | **0 violations** | ✅ **Passed** |

---

## How to Run and Verify

```bash
# 1. Activate virtual environment
source ../venv/bin/activate

# 2. Run the cleaned script
python employee_payroll_system.py

# 3. Verify static analysis tool reports
pylint employee_payroll_system.py
bandit -r employee_payroll_system.py
flake8 employee_payroll_system.py
```
