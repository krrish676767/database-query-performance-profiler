# Database Query Performance Profiler

[![Domain](https://img.shields.io/badge/Domain-Developer%20Tools%20%26%20IT%20Operations-blue.svg)](#)
[![PES University](https://img.shields.io/badge/PES%20University-Dept.%20of%20CSE-red.svg)](#)
[![Lab Assignment](https://img.shields.io/badge/Lab-Lab%201%3A%20Requirements%20Engineering-green.svg)](#)

A database observability and profiling tool that ingests slow query logs, parses SQL execution plans (`EXPLAIN`), identifies missing index candidates, and generates weekly performance optimization digests.

---

## 📌 Problem Context & Overview
In modern cloud backend architectures, unoptimized database queries and missing table indexes are primary drivers of elevated API latency, CPU spikes, and database failure under load. The **Database Query Performance Profiler** provides continuous database observability for engineering teams. By automatically ingesting slow query logs from database instances (PostgreSQL and MySQL) and analyzing their execution plan node trees, the system highlights expensive sequential scans and calculates precise single/composite index creation definitions.

### Target Stakeholders / Actors
- **Database Administrator (DBA):** Optimizes database schemas, manages index lifecycles, and maintains host DB stability.
- **Backend Lead:** Monitors service performance SLAs, configures query latency alert thresholds, and reviews performance digests.

---

## 📁 Repository Deliverables Index

This repository contains all completed deliverables for **Lab 1: Requirements Engineering & UML Use-Case Modelling (Problem Statement #44)**:

| Deliverable File | Description | Criteria Satisfied |
| :--- | :--- | :--- |
| 📄 [`REQUIREMENTS.md`](./REQUIREMENTS.md) | **Complete Requirements Table** | Exactly 5 Functional Requirements (FR-001 to FR-005) & 2 Non-Functional Requirements (NFR-001 & NFR-002) detailing ID, Type, Description, Priority, Acceptance Criteria (Pass/Fail), and Rationale. |
| 📊 [`USE_CASE_DIAGRAM.md`](./USE_CASE_DIAGRAM.md) | **UML Use-Case Diagram & Specification** | Complete Use-Case model mapping all primary actors, 7 use cases, explicit `«include»` relationships, and `«extend»` relationships with trigger conditions (Mermaid, PlantUML & ASCII). |
| 📝 [`USE_CASE_SPECIFICATION.md`](./USE_CASE_SPECIFICATION.md) | **1-Page Use-Case Flow Specification** | Detailed specification for core use case `UC-02: Parse SQL Execution Plans & Recommend Missing Indexes` including Preconditions, Postconditions, Main Success Scenario, and 2 Alternate Flows. |

---

## 🚀 GitHub Repository Submission Guide

To submit this lab assignment to your GitHub account:

1. **Initialize Git Repository:**
   ```bash
   cd C:\Users\Akshay\.gemini\antigravity\scratch\database-query-performance-profiler
   git init
   git add .
   git commit -m "Initial submission for Lab 1 Requirements Engineering & UML Use-Case Modelling"
   ```

2. **Push to Remote GitHub Repository:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/database-query-performance-profiler.git
   git push -u origin main
   ```

3. **Verify Submitted Files on GitHub:**
   - Confirm `README.md`, `REQUIREMENTS.md`, `USE_CASE_DIAGRAM.md`, and `USE_CASE_SPECIFICATION.md` render cleanly in the GitHub web interface.
