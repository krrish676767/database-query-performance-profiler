# Use-Case Specification: Parse SQL Execution Plans & Recommend Missing Indexes

**Course:** PES University - Dept. of CSE  
**Lab:** Lab 1: Requirements Engineering & UML Use-Case Modelling  
**Problem Statement #44:** Developer Tools & IT Operations - Database Query Performance Profiler  

---

## 1. Use-Case Header & Overview

| Document Attribute | Details |
| :--- | :--- |
| **Use Case ID** | **UC-02** |
| **Use Case Name** | **Parse SQL Execution Plans & Recommend Missing Indexes** |
| **Primary Actor(s)** | Database Administrator (DBA), Backend Lead |
| **Secondary Actor(s)**| Host Database Engine (PostgreSQL / MySQL) |
| **Brief Description** | The system ingests raw or JSON-formatted `EXPLAIN` execution plans for slow queries, parses execution node trees, detects high-cost access methods (e.g., sequential table scans on large tables), cross-references existing schema indexes, and computes optimal single or composite index recommendations with estimated execution cost reduction. |
| **Trigger** | A DBA or Backend Lead selects a slow query fingerprint from the profiler dashboard, OR an automated batch profiling job processes newly ingested slow queries. |

---

## 2. Preconditions & Postconditions

### Preconditions
1. The profiler system has successfully ingested a slow query log entry containing the parameterized query string and execution metrics.
2. The user (DBA/Backend Lead) is authenticated and authorized to access database performance metrics.
3. Database schema metadata (existing table definitions, column types, and current indexes) is synchronized with the profiler repository.

### Postconditions
1. **Success Postcondition:**
   - The SQL execution plan JSON tree is parsed, indexed node costs are calculated, and candidate missing indexes (including composite column orders) are saved to the profiler database.
   - The query profile status updates from `"Pending Analysis"` to `"Index Recommended"`.
   - Generated SQL `CREATE INDEX` DDL statements are made available for visual inspection and one-click export.
2. **Failure Postcondition:**
   - The raw execution plan text is marked as `"Malformed/Unparseable"`, an error event is logged in the profiler diagnostic log, and the user is prompted to upload a valid `EXPLAIN (FORMAT JSON)` payload.

---

## 3. Main Success Scenario (Basic Flow)

| Step # | Actor Action | System Response |
| :---: | :--- | :--- |
| **1** | The Database Administrator (DBA) selects a flagged slow query fingerprint (e.g., `SELECT * FROM orders WHERE tenant_id = $1 AND status = $2 ORDER BY created_at DESC`) from the profiler dashboard. | The system retrieves the latest execution metrics and raw/JSON `EXPLAIN` plan tree associated with the query fingerprint. |
| **2** | The DBA clicks **"Analyze Execution Plan & Recommend Index"**. | The system invokes the SQL Plan Parser module to construct an Abstract Syntax Tree (AST) of the query execution plan nodes. |
| **3** | *(Include UC-03)* | The system traverses the execution tree, identifying high-cost nodes such as `Seq Scan` (PostgreSQL) or `ALL` access type (MySQL) on tables with > 100,000 rows. |
| **4** | System internal evaluation. | The system extracts filtering columns from `WHERE` clauses, join keys from `JOIN ... ON` clauses, and sorting columns from `ORDER BY` clauses. |
| **5** | System internal evaluation. | The system cross-references candidate columns against existing database indexes stored in schema metadata to prevent duplicate index definitions. |
| **6** | System internal evaluation. | The system calculates column selectivity and computes the optimal index definition (e.g., composite B-Tree index ordering high-cardinality equality columns first: `CREATE INDEX idx_orders_tenant_status_created ON orders (tenant_id, status, created_at DESC);`). |
| **7** | System displays analysis output. | The system renders an interactive execution node visualizer highlighting high-cost sequential scans in red, displays the calculated cost reduction percentage (e.g., *94% cost reduction*), and presents the recommended `CREATE INDEX` DDL statement. |
| **8** | The DBA reviews the recommended index definition and clicks **"Export DDL"** *(Triggers UC-06)*. | The system copies the validated `CREATE INDEX` statement to the clipboard and marks the query profile status as `"Remediation Pending"`. |

---

## 4. Alternate Flows

### Alternate Flow 1 (Alt-1): Execution Plan Syntax Malformed or Incomplete
*This flow occurs if the ingested EXPLAIN plan cannot be parsed into a valid JSON node tree (Step 2 of Main Flow).*

- **2a.** The SQL Plan Parser detects invalid syntax or truncated text in the ingested `EXPLAIN` plan string.
- **2b.** The system flags the query entry with status `"Malformed Execution Plan"` and logs a parser exception event.
- **2c.** The system displays an alert modal on the dashboard: *"Unable to parse execution plan. Please provide raw EXPLAIN (FORMAT JSON) output."*
- **2d.** The DBA manually pastes the output of `EXPLAIN (FORMAT JSON, ANALYZE) <query>` into the manual input form and clicks **"Re-parse Plan"**.
- **2e.** The system validates the newly provided JSON payload and resumes the Main Success Scenario at **Step 3**.

### Alternate Flow 2 (Alt-2): Existing Index Present but Unused (Stale Statistics)
*This flow occurs when an index covering the query columns already exists, but the query planner performed a sequential scan (Step 5 of Main Flow).*

- **5a.** The system discovers that an existing index (e.g., `idx_orders_tenant`) already covers the filtered `WHERE` columns.
- **5b.** The system inspects database statistics metadata and identifies that index statistics are stale or outdated (`last_analyze_timestamp > 14 days ago`).
- **5c.** Instead of recommending a redundant index, the system generates a maintenance recommendation: `"Existing index 'idx_orders_tenant' is unused due to stale table statistics. Recommended action: Run ANALYZE orders;"`.
- **5d.** The DBA acknowledges the maintenance recommendation, and the use case ends with postcondition status `"Maintenance Action Required"`.

---

## 5. Non-Functional Constraints Specific to Use Case
- **Response Time:** Execution plan parsing and index recommendation generation must complete within **1.5 seconds** for plans containing up to 500 execution tree nodes.
- **Accuracy:** Composite index column order recommendation must follow standard indexing heuristics (Equality columns first, Range/Sort columns last).
