# UML Use-Case Diagram Specification - Database Query Performance Profiler

**Course:** PES University - Dept. of CSE  
**Lab:** Lab 1: Requirements Engineering & UML Use-Case Modelling  
**Problem Statement #44:** Developer Tools & IT Operations - Database Query Performance Profiler  

---

## 1. Actors & System Boundaries

### Actors
1. **Database Administrator (DBA) [Primary Actor]**
   - Responsible for database schema management, index creation, storage tuning, and overall database health.
   - Primary goals: Identify missing indexes, eliminate table scan overhead, and export DDL migration scripts.
2. **Backend Lead [Primary Actor]**
   - Responsible for application query efficiency, API response latencies, and service performance SLA compliance.
   - Primary goals: Monitor slow query trends, set performance alert thresholds, and receive weekly optimization digests.
3. **Host Database / Log Collector [Secondary System Actor]**
   - External database engines (PostgreSQL, MySQL) emitting slow query logs (`pg_stat_statements`, `slow_query_log`) and execution plans (`EXPLAIN`).

### System Boundary
- **System:** `Database Query Performance Profiler`

---

## 2. Mandatory Relationships Specification

### Includes (`«include»`)
1. **`UC-02` (Parse SQL Execution Plans) «include» `UC-03` (Recommend Optimal Index Definitions)**
   - **Rationale:** Parsing an EXPLAIN plan unconditionally triggers the automatic analysis and calculation of missing index column candidates.
2. **`UC-04` (Generate Weekly Performance Digest) «include» `UC-02` (Parse SQL Execution Plans)**
   - **Rationale:** Compiling the weekly performance digest unconditionally requires retrieving and parsing the execution plans of the top slow queries accumulated over the 7-day period.

### Extends (`«extend»`)
1. **`UC-07` (Receive Real-Time Performance Alerts) «extend» `UC-01` (Ingest & Normalize Slow Query Logs)**
   - **Extension Point:** `Threshold Breach`
   - **Condition:** Executed when an ingested query log record exceeds configured runtime or scan count alert thresholds (e.g., query duration > 500ms).
2. **`UC-06` (Export Index DDL Script) «extend» `UC-03` (Recommend Optimal Index Definitions)**
   - **Extension Point:** `Export Requested`
   - **Condition:** Executed when a DBA or Backend Lead explicitly chooses to export/copy the generated `CREATE INDEX` DDL statement for schema migration.

---

## 3. Mermaid UML Use-Case Diagram

```mermaid
graph LR
    subgraph Actors
        DBA["👤 Database Administrator (DBA)"]
        BL["👤 Backend Lead"]
        HDB["🖥️ Host Database System"]
    end

    subgraph System Boundary: Database Query Performance Profiler
        UC1("(UC-01) Ingest & Normalize<br>Slow Query Logs")
        UC2("(UC-02) Parse SQL Execution Plans<br>& Analyze Access Paths")
        UC3("(UC-03) Recommend Optimal<br>Index Definitions")
        UC4("(UC-04) Generate Weekly<br>Performance Digest")
        UC5("(UC-05) Configure Performance<br>Alert Thresholds")
        UC6("(UC-06) Export Index<br>DDL Script")
        UC7("(UC-07) Receive Real-Time<br>Performance Alerts")
    end

    %% Actor to Use Case Connections
    HDB --> UC1
    DBA --> UC2
    DBA --> UC3
    DBA --> UC6
    BL --> UC4
    BL --> UC5
    BL --> UC7
    DBA --> UC4

    %% Include Relationships
    UC2 -- "«include»" --> UC3
    UC4 -- "«include»" --> UC2

    %% Extend Relationships
    UC7 -. "«extend»<br>(Threshold Breach)" .-> UC1
    UC6 -. "«extend»<br>(Export Requested)" .-> UC3
```

---

## 4. PlantUML Use-Case Specification

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Database Administrator (DBA)" as DBA
actor "Backend Lead" as BL
actor "Host Database System" as HDB << System >>

rectangle "Database Query Performance Profiler" {
  usecase "(UC-01) Ingest & Normalize Slow Query Logs" as UC1
  usecase "(UC-02) Parse SQL Execution Plans" as UC2
  usecase "(UC-03) Recommend Optimal Index Definitions" as UC3
  usecase "(UC-04) Generate Weekly Performance Digest" as UC4
  usecase "(UC-05) Configure Alert Thresholds" as UC5
  usecase "(UC-06) Export Index DDL Script" as UC6
  usecase "(UC-07) Receive Real-Time Performance Alerts" as UC7
}

HDB --> UC1
DBA --> UC2
DBA --> UC3
DBA --> UC6
DBA --> UC4
BL --> UC4
BL --> UC5
BL --> UC7

UC2 ..> UC3 : <<include>>
UC4 ..> UC2 : <<include>>
UC7 ..> UC1 : <<extend>> \n (Condition: Threshold Breach)
UC6 ..> UC3 : <<extend>> \n (Condition: Export Requested)
@enduml
```

---

## 5. ASCII System Representation

```
+-----------------------------------------------------------------------------------------------+
|                        DATABASE QUERY PERFORMANCE PROFILER SYSTEM                              |
|                                                                                               |
|   +-------------------+                                                                       |
|   |  Host DB System   | ---> [ (UC-01) Ingest & Normalize Slow Query Logs ]                       |
|   +-------------------+                                 ^                                     |
|                                                         : <<extend>> (Threshold Breach)       |
|                                                         :                                     |
|                                         [ (UC-07) Receive Real-Time Alerts ] <--- [Backend Lead]
|                                                                                      ^        |
|                                                                                      |        |
|   +---------------------+               [ (UC-05) Configure Alert Thresholds ] ------+        |
|   | Database Admin (DBA)|                                                            |        |
|   +---------------------+               [ (UC-04) Generate Weekly Digest ] ----------+        |
|          |                                              |                                     |
|          +----------------------------------------------+                                     |
|          |                                              | «include»                           |
|          v                                              v                                     |
|   [ (UC-02) Parse SQL Execution Plans ] ---------------------------------+                    |
|          |                                                               |                    |
|          | «include»                                                     |                    |
|          v                                                               |                    |
|   [ (UC-03) Recommend Optimal Index Definitions ] <----------------------+                    |
|          ^                                                                                    |
|          : <<extend>> (Export Requested)                                                      |
|          :                                                                                    |
|   [ (UC-06) Export Index DDL Script ] -----------------------------> [Database Admin (DBA)]   |
+-----------------------------------------------------------------------------------------------+
```
