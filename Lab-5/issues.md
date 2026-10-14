# Lab 5: Static Code Analysis — Issues Identification & Resolution Table

## Student Metadata
- **Student Name:** Krrish P Raju
- **SRN:** PES1UG24CS708
- **Course:** UE23CS352B — Software Engineering Lab
- **Lab Topic:** Lab 5: Static Code Analysis (Pylint, Bandit, Flake8)
- **Assigned Problem Statement:** #44 Employee Payroll System (`employee_payroll_system.py`)
- **Repository:** [`krrish676767/database-query-performance-profiler`](https://github.com/krrish676767/database-query-performance-profiler)

---

## Static Code Analysis Summary

| Metric | Baseline Scan (Before) | Post-Fix Scan (After) | Target Required |
| :--- | :---: | :---: | :---: |
| **Bandit Issues** | 5 (2 High, 1 Medium, 2 Low) | **0 Issues** | All resolved |
| **Pylint Score** | **5.53 / 10.00** | **10.00 / 10.00** | > 9.50 / 10.00 |
| **Flake8 Violations** | 6 PEP 8 violations | **0 Violations** | All resolved |

---

## Detailed Issues Register

The table below documents all identified programming issues, security vulnerabilities, logical bugs, and style defects detected across **Bandit**, **Pylint**, and **Flake8**, prioritized by severity.

| Issue | Tool & Code | Severity / Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Insecure Dynamic Code Execution (`eval`)** | Bandit `B307` / Pylint `W0123` | **High / Medium** (CWE-78) | 42 | Evaluation of arbitrary deduction expression using `eval(deduction_expr)` enables Remote Code Execution (RCE) and code injection if expressions originate from untrusted input. | Replaced `eval()` with an Abstract Syntax Tree (`ast.parse`) safe recursive evaluator `_eval_safe_node()` that whitelists only basic arithmetic binary operators (`+`, `-`, `*`, `/`) and approved numeric constants. |
| **Weak Cryptographic Hash Algorithm (MD5)** | Bandit `B324` | **High** (CWE-327) | 47 | Use of MD5 (`hashlib.md5`) for generating employee identity tokens is vulnerable to collision attacks and is deprecated for security-sensitive cryptographic applications. | Upgraded hashing mechanism to secure SHA-256 (`hashlib.sha256`) with explicit UTF-8 encoding. |
| **Shell Command Injection via `os.system`** | Bandit `B605` | **High** (CWE-78) | 58 | Invoking the shell through `os.system("echo ... " + filename)` allows shell injection if file paths contain shell metacharacters (e.g., `;`, `&&`, `\|`). | Removed shell execution entirely. Replaced with safe, native Python string formatting and `print()` function. |
| **Insecure Pseudo-Random Token Generation** | Bandit `B311` | **Low** (CWE-330) | 51 | Use of standard library `random.randint()` relies on the Mersenne Twister PRNG, which is deterministic and unsuited for generating security or financial tokens. | Switched to cryptographically secure `secrets.SystemRandom().randint(1000, 9999)` for unpredictable token generation. |
| **Silent Exception Swallowing / Bare `except:`** | Bandit `B110` / Pylint `W0702` / Flake8 `E722` | **Medium** (CWE-703, Code Smell) | 26 | Bare `except:` clause catches all exceptions including system-exiting signals (`KeyboardInterrupt`, `SystemExit`) and silently executes `pass`, hiding unexpected bugs. | Replaced error suppression with explicit defensive validation (`if emp_id not in payroll_records or penalty < 0: return False`) and proper business logic handling. |
| **Mutable Default Argument in Function Definition** | Pylint `W0102` | **Bug / Logic Defect** | 15 | `transaction_logs=[]` creates a mutable list default that is evaluated once when the function is defined and persists/accumulates across multiple function calls. | Changed the default parameter to `None` and initialized `transaction_logs = []` conditionally inside the function body. |
| **Unsafe File I/O & Missing Encoding Specification** | Pylint `W1514`, `R1732` | **Resource Defect** | 55 | Calling raw `open()` without a context manager risks leaving file handles open if an exception occurs; omitted encoding causes platform-dependent character corruption. | Replaced with `with open(filename, "w", encoding="utf-8") as f:` to guarantee deterministic closing and consistent encoding. |
| **Unused Import (`math`)** | Pylint `W0611` / Flake8 `F401` | **Code Smells** | 6 | `import math` was imported at the module level but never utilized in any calculation. | Removed `import math` to reduce namespace pollution and memory footprint. |
| **Dead Local Variables (`statutory_buffer`, `base`)** | Pylint `W0612` / Flake8 `F841` | **Code Quality** | 31, 41 | Variables were assigned numerical values but never read or passed downstream in execution flows. | Removed unused variables completely from function scopes. |
| **Non-Idiomatic Singleton Comparison** | Pylint `C0121` / Flake8 `E711` | **Code Style** | 32 | Comparison `payroll_records.get(emp_id) == None` violates Python PEP 8 recommendations for singletons. | Refactored expression to use the identity operator `payroll_records.get(emp_id) is None`. |
| **Simplifiable Conditional Return Pattern** | Pylint `R1703`, `R1705` | **Maintainability** | 34 | Redundant `if condition: return True else: return False` block with unnecessary `else` branch. | Simplified to direct boolean expression evaluation: `return payroll_records[emp_id]["base_salary"] >= min_base`. |
| **Function Naming Style Violation (camelCase)** | Pylint `C0103` | **Code Style** | 15 | `processSalary` violated PEP 8 `snake_case` naming guidelines for functions. | Renamed function to `process_salary`, and added a backward-compatible alias `processSalary = process_salary`. |
| **Missing Module and Function Docstrings** | Pylint `C0116` | **Documentation** | Multiple | Functions lacked descriptive docstrings explaining parameters, return values, and behavior. | Added clear, PEP 257-compliant docstrings to all top-level functions and helper routines. |
| **Outdated `%` String Formatting** | Pylint `C0209` | **Modernization** | 19 | String interpolation using `%` specifier syntax is legacy and less readable. | Upgraded to modern Python 3 formatted string literals (f-strings). |
| **PEP 8 Line Length Limit Exceeded (> 79 chars)** | Flake8 `E501` | **Style / Readability** | 19, 88 | Lines exceeded PEP 8 standard maximum line length of 79 characters. | Broken long strings and docstrings into multi-line wrapped statements strictly under 79 characters. |
