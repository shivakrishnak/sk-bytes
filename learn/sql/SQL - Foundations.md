---
title: "SQL - Foundations"
topic: SQL
subtopic: Foundations
layout: default
parent: SQL
nav_order: 1
permalink: /learn/sql/foundations/
category: SQL
code: SQL
folder: learn/sql/
difficulty_range: easy
status: draft
version: 1
generated_from: LEARN_KEYWORD_GENERATOR.md v1.0
archetype: LANGUAGE
mode: MODE_NEW
provenance: "user request via /learn: sql"
keywords:
  - SQL-001 Why Databases Exist
  - SQL-002 The Relational Model - How Tables Think
  - SQL-003 SQL vs NoSQL - The Landscape
  - SQL-004 RDBMS Ecosystem - Postgres, MySQL, SQL Server
  - SQL-005 The Spreadsheet-to-Database Leap
  - SQL-006 ANSI SQL vs Vendor Dialects
  - SQL-007 Installing PostgreSQL - First Database
  - SQL-008 Tables, Rows, and Columns
  - SQL-009 Data Types - Integers, Text, Dates, Booleans
  - SQL-010 CREATE TABLE and DROP TABLE
  - SQL-011 INSERT - Adding Rows
  - SQL-012 SELECT and FROM - Reading Data
  - SQL-013 WHERE - Filtering Rows
  - SQL-014 UPDATE and DELETE - Modifying Data
  - SQL-015 ORDER BY and LIMIT
  - SQL-016 Primary Keys and Uniqueness
  - SQL-017 Foreign Keys and Relationships
  - SQL-018 NULL - The Three-Valued Logic Trap
  - SQL-019 SELECT * in Production Anti-Pattern
  - SQL-020 psql and pgAdmin - First Tools
  - SQL-021 DBeaver - Universal Database Client
  - SQL-022 Online Store DB - Phase 1 (Schema and CRUD)
  - SQL-023 Basic SELECT Exercises
  - SQL-024 Top 10 SQL Interview Questions - Basics
  - SQL-025 SQL Aliases and Expressions
---

## Keywords

1. [SQL-001 Why Databases Exist](#sql-001-why-databases-exist)
2. [SQL-002 The Relational Model - How Tables Think](#sql-002-the-relational-model---how-tables-think)
3. [SQL-003 SQL vs NoSQL - The Landscape](#sql-003-sql-vs-nosql---the-landscape)
4. [SQL-004 RDBMS Ecosystem - Postgres, MySQL, SQL Server](#sql-004-rdbms-ecosystem---postgres-mysql-sql-server)
5. [SQL-005 The Spreadsheet-to-Database Leap](#sql-005-the-spreadsheet-to-database-leap)
6. [SQL-006 ANSI SQL vs Vendor Dialects](#sql-006-ansi-sql-vs-vendor-dialects)
7. [SQL-007 Installing PostgreSQL - First Database](#sql-007-installing-postgresql---first-database)
8. [SQL-008 Tables, Rows, and Columns](#sql-008-tables-rows-and-columns)
9. [SQL-009 Data Types - Integers, Text, Dates, Booleans](#sql-009-data-types---integers-text-dates-booleans)
10. [SQL-010 CREATE TABLE and DROP TABLE](#sql-010-create-table-and-drop-table)
11. [SQL-011 INSERT - Adding Rows](#sql-011-insert---adding-rows)
12. [SQL-012 SELECT and FROM - Reading Data](#sql-012-select-and-from---reading-data)
13. [SQL-013 WHERE - Filtering Rows](#sql-013-where---filtering-rows)
14. [SQL-014 UPDATE and DELETE - Modifying Data](#sql-014-update-and-delete---modifying-data)
15. [SQL-015 ORDER BY and LIMIT](#sql-015-order-by-and-limit)
16. [SQL-016 Primary Keys and Uniqueness](#sql-016-primary-keys-and-uniqueness)
17. [SQL-017 Foreign Keys and Relationships](#sql-017-foreign-keys-and-relationships)
18. [SQL-018 NULL - The Three-Valued Logic Trap](#sql-018-null---the-three-valued-logic-trap)
19. [SQL-019 SELECT \* in Production Anti-Pattern](#sql-019-select--in-production-anti-pattern)
20. [SQL-020 psql and pgAdmin - First Tools](#sql-020-psql-and-pgadmin---first-tools)
21. [SQL-021 DBeaver - Universal Database Client](#sql-021-dbeaver---universal-database-client)
22. [SQL-022 Online Store DB - Phase 1 (Schema and CRUD)](#sql-022-online-store-db---phase-1-schema-and-crud)
23. [SQL-023 Basic SELECT Exercises](#sql-023-basic-select-exercises)
24. [SQL-024 Top 10 SQL Interview Questions - Basics](#sql-024-top-10-sql-interview-questions---basics)
25. [SQL-025 SQL Aliases and Expressions](#sql-025-sql-aliases-and-expressions)

---

# SQL-001 Why Databases Exist

**TL;DR** - Databases replace fragile files with structured, concurrent, queryable storage that keeps data correct.

---

### 🟢 What it is

A **database** is a system that stores, organizes, and retrieves
data with guarantees about correctness, durability, and
concurrent access that files and spreadsheets cannot provide.

---

### 🎯 Why it exists

Picture a growing company tracking orders in CSV files on a
shared drive. Two people edit the same file simultaneously and
one overwrites the other's changes. A third person deletes a
row by accident - no undo. Someone asks "what were total sales
last quarter?" and the answer requires manually opening twelve
files and hoping the columns match. The data has no enforced
structure, no protection against contradictions, and no way to
answer questions without manual labor. This is exactly why
databases exist.

---

### 🧠 Mental Model

> A database is a warehouse with a strict receiving clerk. Every
> item gets inspected, catalogued, and shelved by rules - not
> tossed into a pile on the floor.

**Memory hook:** Files are piles. Databases are warehouses
with inventory control.

---

### ⚙️ How it works

1. You define a schema - the shape of your data (tables,
   columns, types, constraints) - before storing anything.
2. The database engine enforces those rules on every write,
   rejecting invalid data at the door.
3. Concurrent users read and write simultaneously through
   transactions that isolate their changes from each other.
4. Queries let you ask complex questions across millions of
   rows in seconds, without writing loops or opening files.
5. The engine persists data to disk with crash recovery, so
   a power failure does not corrupt your records.

---

### ✏️ Minimal Example

**BAD:**

```python
# Storing orders in a flat file
with open("orders.csv", "a") as f:
    # No type check, no duplicate check,
    # no concurrent-write safety
    f.write("101,,2024-13-45,bad-date\n")
```

Why it's wrong: nothing stops invalid data, duplicate IDs,
or two processes writing at the same instant.

**GOOD:**

```sql
CREATE TABLE orders (
    id    INTEGER PRIMARY KEY,
    total NUMERIC(10,2) NOT NULL CHECK (total > 0),
    placed DATE NOT NULL
);

-- Database rejects bad data automatically
INSERT INTO orders (id, total, placed)
VALUES (101, 59.99, '2024-03-15');
```

Why it's right: the schema enforces types, rejects nulls,
and the primary key prevents duplicate IDs.

---

### ⚡ When to use / Not to use

**Use when:**

- Multiple users or services need to read and write the
  same data concurrently without losing changes.
- You need to query, filter, or aggregate data rather than
  just store and retrieve whole files.

**Avoid when:**

- You are storing opaque binary blobs (images, video) with
  no need to query their contents.
- A single config file or static JSON is sufficient and
  will never be edited concurrently.

---

### ⚠️ One Gotcha

**Misconception:** "My app is small, so I can just use files
and switch to a database later."
**Reality:** Migrating from files to a database after
launch means rewriting every read/write path, inventing a
migration for existing data, and fixing every bug where
file-based code assumed no concurrency. Starting with a
database (even SQLite) costs almost nothing upfront.

---

### 📇 Revision Card

1. Databases enforce structure, reject bad data, and handle
   concurrent access - files do none of these.
2. The cost is learning SQL and managing a server (or using
   embedded SQLite for zero setup).
3. "I'll add a database later" is the migration nobody wants
   to do under production pressure.

---

---

# SQL-002 The Relational Model - How Tables Think

**TL;DR** - The relational model organizes data into tables of rows and columns with set-based operations.

---

### 🟢 What it is

The **relational model** is a mathematical framework, proposed
by Edgar F. Codd in 1970, that represents data as relations
(tables), where each row is a tuple (a fact) and each column
is an attribute (a property).

---

### 🎯 Why it exists

Early databases stored data in rigid hierarchical trees or
tangled network graphs. Changing the structure meant rewriting
application code. Programmers had to know the physical storage
layout to retrieve anything. Codd's insight was radical: separate
the logical view of data from its physical storage, represent
everything as flat tables, and let a declarative language handle
retrieval. This is exactly why the relational model exists.

---

### 🧠 Mental Model

> Think of a well-organized spreadsheet where every sheet has a
> title, every column has a strict type, and you can ask questions
> across sheets by matching values - but you never touch the
> underlying file format.

**Memory hook:** Tables are structured facts. Queries are
questions you ask those facts.

---

### ⚙️ How it works

1. Data lives in tables. Each table holds one kind of entity
   (customers, orders, products).
2. Every row represents one instance of that entity. Rows are
   unordered - there is no "row 5" by position.
3. Every column has a name and a data type. All values in a
   column share that type.
4. A primary key (one or more columns) uniquely identifies
   each row. No two rows share the same key.
5. You retrieve data with set-based operations (select, join,
   filter) rather than procedural loops.

---

### ✏️ Minimal Example

**BAD:**

```text
# Flat file - one blob of denormalized data
Alice,101,Widget,3,alice@co.com
Alice,102,Gadget,1,alice@co.com
```

Why it's wrong: Alice's email is duplicated. Change it in
one line but not the other and you have contradictory data.

**GOOD:**

```sql
-- Separate tables, linked by customer_id
CREATE TABLE customers (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product     TEXT NOT NULL,
    qty         INTEGER NOT NULL
);
```

Why it's right: each fact is stored once. The foreign key
links orders to customers without duplicating email.

---

### ⚡ When to use / Not to use

**Use when:**

- Your data has clear entities with relationships (customers
  have orders, orders contain products).
- You need to answer ad-hoc questions about your data without
  writing custom code for each question.

**Avoid when:**

- Your data is deeply nested documents with no cross-entity
  relationships (a document store may fit better).
- You are storing time-series sensor readings at millions of
  points per second (a specialized time-series DB is faster).

---

### ⚠️ One Gotcha

**Misconception:** "Rows in a table have a natural order,
like rows in a spreadsheet."
**Reality:** Relational tables are sets - mathematically
unordered. Without an explicit `ORDER BY`, the database may
return rows in any sequence, and that sequence can change
between runs. Never depend on insertion order.

---

### 📇 Revision Card

1. The relational model separates logical structure (tables)
   from physical storage - that is its core power.
2. Every fact is stored exactly once; relationships use keys
   instead of duplication.
3. Tables are sets, not lists - rows have no inherent order.

---

---

# SQL-003 SQL vs NoSQL - The Landscape

**TL;DR** - SQL databases enforce structure and ACID transactions; NoSQL trades those for schema flexibility and horizontal scale.

---

### 🟢 What it is

**SQL vs NoSQL** is the fundamental choice between relational
databases (tables, schemas, SQL queries, ACID guarantees) and
non-relational databases (documents, key-value pairs, graphs,
or wide columns with flexible schemas and eventual consistency).

---

### 🎯 Why it exists

Relational databases dominated for decades, but web-scale
companies hit walls: rigid schemas slowed iteration, JOIN-heavy
queries bottlenecked on single servers, and sharding a relational
database was painful. Projects like Google's Bigtable and
Amazon's Dynamo proved that relaxing relational constraints
could unlock horizontal scalability. Meanwhile, document stores
like MongoDB let teams iterate on schemas without migrations.
Neither approach "won" - each solves different problems. This is
exactly why the SQL vs NoSQL distinction exists.

---

### 🧠 Mental Model

> SQL is a filing cabinet with labeled folders and strict rules
> about what goes where. NoSQL is a storage unit where you toss
> in boxes of any shape and sort them out when you need something.

**Memory hook:** SQL = structure first, flexibility later.
NoSQL = flexibility first, structure later.

---

### ⚙️ How it works

1. SQL databases store data in predefined tables with typed
   columns. You write a schema before inserting data. Changes
   require migrations.
2. NoSQL databases accept data in varied shapes - JSON
   documents, key-value pairs, graph nodes, or wide-column
   families - often without a predefined schema.
3. SQL databases guarantee ACID (Atomicity, Consistency,
   Isolation, Durability) for every transaction.
4. Most NoSQL systems trade strict consistency for availability
   and partition tolerance (the CAP theorem trade-off), offering
   eventual consistency instead.
5. SQL scales vertically (bigger server). NoSQL typically
   scales horizontally (more servers), though modern SQL
   databases (CockroachDB, YugabyteDB) blur this line.

---

### ✏️ Minimal Example

**BAD:**

```text
-- Forcing a document model into relational tables
CREATE TABLE user_profiles (
    id   INTEGER PRIMARY KEY,
    data TEXT  -- JSON blob stuffed into a text column
);
-- No indexing, no type safety, no query power
```

Why it's wrong: you pay the cost of a relational database
but get none of the benefits - no constraints, no joins,
no typed queries.

**GOOD:**

```sql
-- Relational: structured data with enforced integrity
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Or use a document store when schema is fluid:
-- MongoDB: db.users.insertOne({name: "Alice",
--   prefs: {theme: "dark", lang: "en"}})
-- Prefs can vary per user without migrations.
```

Why it's right: pick the model that matches your data shape.
Structured entities with relationships belong in SQL.
Varied, nested documents belong in a document store.

---

### ⚡ When to use / Not to use

**Use SQL when:**

- Your data has well-defined relationships and you need
  complex queries with joins, aggregations, and transactions.
- Data integrity (no orphaned records, no constraint
  violations) is non-negotiable.

**Use NoSQL when:**

- Your schema changes frequently and migrations are
  expensive (early-stage products, rapid prototyping).
- You need horizontal scaling across many commodity servers
  for high write throughput.

---

### ⚠️ One Gotcha

**Misconception:** "NoSQL is faster than SQL."
**Reality:** Speed depends on access patterns, not the label.
A key-value lookup in Redis is faster than a SQL join - but
a SQL indexed query is faster than scanning an entire MongoDB
collection. NoSQL is not inherently faster; it is optimized
for different workloads.

---

### 📇 Revision Card

1. SQL enforces structure and ACID; NoSQL trades those for
   schema flexibility and horizontal scale.
2. The choice depends on data shape and access patterns, not
   on which technology is "newer."
3. "NoSQL is faster" is wrong - access pattern determines
   speed, not the database category.

---

---

# SQL-004 RDBMS Ecosystem - Postgres, MySQL, SQL Server

**TL;DR** - PostgreSQL, MySQL, SQL Server, and SQLite each dominate different niches; choose by workload, not popularity.

---

### 🟢 What it is

The **RDBMS ecosystem** is the landscape of relational database
management systems - each implementing the SQL standard with
its own extensions, performance profile, licensing model, and
operational tooling.

---

### 🎯 Why it exists

A single "universal database" does not exist because workloads
differ wildly. A startup running on a five-dollar VPS has
different needs than a bank processing millions of transactions
per second. An embedded mobile app cannot run a server process.
Each major RDBMS evolved to serve a specific niche: PostgreSQL
for correctness and extensibility, MySQL for web-scale read
throughput, SQL Server for enterprise integration, SQLite for
zero-config embedding. This is exactly why the RDBMS ecosystem
exists.

---

### 🧠 Mental Model

> Choosing a database is like choosing a vehicle. A sedan
> (MySQL) is great for daily commutes, a truck (PostgreSQL)
> hauls anything you throw at it, a luxury SUV (SQL Server)
> comes with every feature pre-installed, and a bicycle
> (SQLite) goes anywhere without fuel.

**Memory hook:** Same SQL language, different engines -
pick the engine that fits the road.

---

### ⚙️ How it works

1. **PostgreSQL** - open-source, standards-compliant, highly
   extensible. Supports JSON, arrays, custom types, full-text
   search, and advanced indexing (GiST, GIN, BRIN).
2. **MySQL** - open-source, optimized for read-heavy web
   workloads. Powers WordPress, Shopify, and much of the
   web. Simpler replication model.
3. **SQL Server** - Microsoft's commercial RDBMS. Deep
   integration with .NET, Azure, and BI tools (SSRS, SSIS).
   Free Developer and Express editions available.
4. **SQLite** - serverless, zero-config, embedded database
   stored as a single file. Runs on phones, browsers, IoT
   devices, and desktop apps. Not designed for concurrent
   multi-user server workloads.
5. All four speak SQL. Switching between them requires
   adapting vendor-specific syntax and features, not
   relearning the language.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Assuming MySQL syntax works everywhere
SELECT * FROM users LIMIT 10;
-- Works in MySQL and PostgreSQL
-- Fails in SQL Server (uses TOP instead)
```

Why it's wrong: vendor-specific syntax makes code
non-portable if you assume one dialect is universal.

**GOOD:**

```sql
-- PostgreSQL / MySQL
SELECT id, name FROM users
ORDER BY id LIMIT 10;

-- SQL Server equivalent
SELECT TOP 10 id, name FROM users
ORDER BY id;

-- Know your dialect. Abstract in app code
-- if portability matters.
```

Why it's right: acknowledging dialect differences prevents
surprises when migrating or supporting multiple backends.

---

### ⚡ When to use / Not to use

**Use when:**

- You are starting a new project and need to pick a
  relational database - match the database to your
  deployment, team skills, and workload profile.
- You need to compare trade-offs between open-source
  (Postgres/MySQL) and commercial (SQL Server) options.

**Avoid when:**

- Your workload is fundamentally non-relational (graph
  traversals, time-series ingestion) - a specialized
  database will outperform any general-purpose RDBMS.
- You need a distributed, multi-region database with
  automatic sharding (consider CockroachDB or Spanner).

---

### ⚠️ One Gotcha

**Misconception:** "PostgreSQL and MySQL are interchangeable -
just pick whichever is more popular."
**Reality:** They differ in transaction isolation defaults,
JSON handling, index types, replication architecture, and
standards compliance. PostgreSQL defaults to serializable-like
behavior for DDL and stricter type coercion. MySQL is more
permissive by default, which can hide data quality bugs.
Choosing based on popularity instead of workload fit leads
to workarounds later.

---

### 📇 Revision Card

1. PostgreSQL for correctness and extensibility, MySQL for
   web-scale reads, SQL Server for .NET/Azure, SQLite for
   embedding.
2. All speak SQL but differ in dialect, defaults, and
   operational characteristics - know your target.
3. Choosing by popularity instead of workload fit creates
   technical debt you pay during every production incident.

---

---

# SQL-005 The Spreadsheet-to-Database Leap

**TL;DR** - Spreadsheets break when data grows, overlaps, or needs concurrent edits - databases solve all three.

---

### 🟢 What it is

**The spreadsheet-to-database leap** is the critical transition
from storing structured data in spreadsheets (Excel, Google
Sheets) to storing it in a relational database - a shift in
tooling, mental model, and data integrity guarantees.

---

### 🎯 Why it exists

Spreadsheets work beautifully for small, single-user datasets.
Then reality arrives. A second person edits the same sheet and
overwrites changes. Someone pastes "N/A" into a numeric column
and breaks every formula downstream. Row 4,327 references a
customer who was deleted from another tab, and nobody notices
for months. The sheet hits 100,000 rows and grinds to a halt.
There is no audit trail, no enforced relationships, and no way
to answer "show me all overdue invoices for customers in
Europe" without a pivot table marathon. This is exactly why the
spreadsheet-to-database leap exists.

---

### 🧠 Mental Model

> A spreadsheet is a notepad - anyone can scribble anywhere. A
> database is a bound ledger with numbered pages, pre-printed
> columns, and a librarian who rejects entries that break the
> rules.

**Memory hook:** Spreadsheets trust humans. Databases trust
constraints.

---

### ⚙️ How it works

1. **Schema enforcement** - a database defines column types
   and constraints upfront. You cannot put text into an
   integer column. A spreadsheet lets you put anything
   anywhere.
2. **Referential integrity** - foreign keys guarantee that
   an order cannot reference a customer that does not exist.
   Spreadsheets have no cross-sheet enforcement.
3. **Concurrent access** - databases handle multiple
   simultaneous writers through transactions and locking.
   Spreadsheets either lock the whole file or silently merge
   with conflict.
4. **Querying power** - SQL lets you filter, join, group,
   and aggregate across millions of rows in milliseconds.
   Spreadsheet formulas do not scale past tens of thousands
   of rows.
5. **Audit and recovery** - databases log transactions and
   support point-in-time recovery. A spreadsheet's undo
   history vanishes when the file closes.

---

### ✏️ Minimal Example

**BAD:**

```text
# Spreadsheet: orders tab
| OrderID | Customer | Email         | Total |
|---------|----------|---------------|-------|
| 101     | Alice    | alice@co.com  | 59.99 |
| 102     | Alice    | alice@co.com  | 24.00 |
| 103     | Bob      | N/A           | oops  |
```

Why it's wrong: email duplicated across rows, "N/A" in
email, "oops" in a money column - no rule prevents any
of this.

**GOOD:**

```sql
CREATE TABLE customers (
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INT NOT NULL
        REFERENCES customers(id),
    total       NUMERIC(10,2) NOT NULL
        CHECK (total > 0)
);
-- "N/A" in email? Rejected. "oops" as total?
-- Rejected. Orphan order? Rejected.
```

Why it's right: the database enforces every rule that the
spreadsheet left to human discipline.

---

### ⚡ When to use / Not to use

**Use a database when:**

- Multiple people need to read and write the same dataset
  without overwriting each other.
- Your data has relationships between entities (customers
  -> orders -> line items) that must stay consistent.

**Stay with a spreadsheet when:**

- You are doing one-off exploratory analysis that will
  not be reused or shared.
- The dataset is small, single-user, and does not need
  enforced integrity.

---

### ⚠️ One Gotcha

**Misconception:** "I'll keep the spreadsheet as the source
of truth and sync it to a database periodically."
**Reality:** Two sources of truth means neither is true.
Every sync introduces lag, conflicts, and drift. Pick one
authoritative store. If you need the database, commit to it.
Export to spreadsheets for reporting, but never import back.

---

### 📇 Revision Card

1. Spreadsheets fail at concurrent writes, enforced types,
   referential integrity, and large-scale queries.
2. The leap is not just tooling - it is a mental shift from
   "cells you can edit" to "facts governed by rules."
3. Two sources of truth (spreadsheet + database) guarantee
   that at least one is wrong at any given moment.

---

---

# SQL-006 ANSI SQL vs Vendor Dialects

**TL;DR** - SQL has a standard; every database bends it, so learn the standard first.

---

### 🟢 What it is

**ANSI SQL** is the ISO/IEC 9075 standard that defines the core grammar, data types, and behavior every relational database should follow - while **vendor dialects** are the proprietary extensions each database adds on top.

---

### 🎯 Why it exists

Imagine writing an application that talks to PostgreSQL today, and next quarter the company acquires a product running on SQL Server. Without a shared grammar, every query is a rewrite. Every function name changes. Every date format breaks. Teams burn weeks translating code that does the same logical thing. A standard grammar lets you write portable queries that work across engines, and isolate vendor-specific pieces to the edges. This is exactly why ANSI SQL exists.

---

### 🧠 Mental Model

> ANSI SQL is like standard traffic rules. Every country follows the basics - stop at red, go at green - but each country adds local quirks like roundabout priority or right-on-red. You drive safely anywhere by knowing the standard, then learning local exceptions.

**Memory hook:** Standard SQL is the passport; dialects are the local customs.

---

### ⚙️ How it works

1. The ISO committee publishes SQL standards (SQL-92, SQL:1999, SQL:2016, SQL:2023). Each defines core features and optional packages.
2. Database vendors implement the core, then add proprietary syntax for features the standard does not cover yet or covers differently.
3. Common divergence points: row-limiting (`LIMIT` vs `TOP` vs `FETCH FIRST`), string concatenation (`||` vs `+` vs `CONCAT`), auto-increment columns, date arithmetic, and identifier quoting.
4. When you write standard-compliant SQL, it runs on most engines. When you use vendor syntax, you lock yourself to that engine.
5. Portability strategy: write core logic in ANSI SQL, isolate vendor-specific pieces (functions, DDL quirks) behind a thin abstraction or migration tool.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- MySQL-only: LIMIT without standard alternative
SELECT name FROM customers
ORDER BY created_at DESC
LIMIT 10;

-- SQL Server-only: TOP without ORDER BY guarantee
SELECT TOP 10 name FROM customers;
```

Why it's wrong: both use vendor-specific row-limiting syntax that fails on the other engine.

**GOOD:**

```sql
-- ANSI SQL:2008 standard row-limiting
SELECT name FROM customers
ORDER BY created_at DESC
FETCH FIRST 10 ROWS ONLY;
```

Why it's right: `FETCH FIRST` is the ISO standard clause, supported by PostgreSQL 8.4+, Oracle 12c+, DB2, and SQL Server 2012+ (via `OFFSET...FETCH`).

---

### ⚡ When to use / Not to use

**Use when:**

- Building an application that may change databases in the future
- Writing queries for a data layer shared across multiple database engines

**Avoid when:**

- You need a vendor-specific optimization (e.g., PostgreSQL `LATERAL JOIN` with specific planner hints) and portability is not a requirement
- The standard syntax is significantly less readable or performant for a well-understood, single-vendor deployment

---

### ⚠️ One Gotcha

**Misconception:** "If it runs on PostgreSQL, it's standard SQL."
**Reality:** PostgreSQL is one of the most standards-compliant databases, but it still has extensions like `ILIKE`, `::` casting, array types, and `SERIAL` that are not part of ANSI SQL. Always check the standard clause name before assuming portability.

---

### 📇 Revision Card

1. ANSI SQL is the shared grammar; vendor dialects add local extensions on top of it
2. The biggest portability traps are row-limiting, date functions, string concatenation, and auto-increment columns
3. "Works on Postgres" does not mean "is standard SQL" - Postgres adds many convenient non-standard features

---

---

# SQL-007 Installing PostgreSQL - First Database

**TL;DR** - Install Postgres, connect with psql, create a database - your SQL lab is open.

---

### 🟢 What it is

**Installing PostgreSQL** means setting up the database server on your machine so you have a local environment to write, test, and break SQL without consequences.

---

### 🎯 Why it exists

Reading SQL syntax from a book is like reading about swimming without a pool. You can memorize SELECT and JOIN, but without a running database you cannot see how queries behave with real data, observe error messages, or build intuition for what the engine actually does. Online SQL playgrounds limit what you can try - no DDL, no extensions, no crash-and-recover cycles. A local PostgreSQL install gives you full control, zero risk, and instant feedback loops. This is exactly why installing PostgreSQL as your first database matters.

---

### 🧠 Mental Model

> PostgreSQL is a workshop bench. The installer is assembling the bench. `psql` is your set of hand tools. `CREATE DATABASE` is clearing a fresh workspace on the bench. Until the bench is built, you cannot build anything else.

**Memory hook:** No database, no practice. Install first, learn everything else second.

---

### ⚙️ How it works

1. **Choose an install method.** Package managers (`apt`, `brew`, `choco`) are simplest for development. Docker (`docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres:16`) gives isolation and easy teardown. Platform installers work but add background services you may not want permanently.
2. **Start the server.** Package installs typically auto-start; Docker starts on `docker run`. Verify with `pg_isready` - it should print "accepting connections".
3. **Connect with psql.** Run `psql -U postgres`. This opens an interactive SQL terminal connected as the default superuser. The prompt `postgres=#` means you are inside the database.
4. **Create your first database.** Run `CREATE DATABASE learn_sql;` then `\c learn_sql` to switch into it. You now have an isolated space for experiments.
5. **Understand pg_hba.conf.** This file controls who can connect and how they authenticate. On a local dev install, the default "trust" or "peer" setting is fine. In any shared environment, you would change this to require passwords.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Connecting without specifying a user
-- on a fresh install with password auth
psql
-- ERROR: role "youruser" does not exist
```

Why it's wrong: the default OS user may not match any PostgreSQL role, causing a confusing connection error.

**GOOD:**

```sql
-- Explicit user, explicit database
psql -U postgres -d postgres

-- Once connected, create your workspace
CREATE DATABASE learn_sql;
\c learn_sql
-- You are now connected to database "learn_sql"
```

Why it's right: specifying `-U postgres` uses the known superuser role, and creating a dedicated database keeps experiments isolated from system catalogs.

---

### ⚡ When to use / Not to use

**Use when:**

- You are learning SQL and need a consequence-free practice environment
- You need to test DDL, extensions, or configuration changes that online sandboxes forbid

**Avoid when:**

- You only need to run a few SELECT queries against sample data - an online playground like db-fiddle may be faster to start
- You are setting up a shared or production database - that requires proper security configuration beyond a dev install

---

### ⚠️ One Gotcha

**Misconception:** "The `postgres` superuser is just for setup; I can use it for everything."
**Reality:** The `postgres` role bypasses all permission checks. Practicing with it hides permission errors you will face in real environments. Create a non-superuser role early (`CREATE ROLE learner LOGIN PASSWORD 'dev';`) and use that for daily practice so you learn how permissions actually work.

---

### 📇 Revision Card

1. Install via package manager or Docker; verify with `pg_isready`; connect with `psql -U postgres`
2. Always create a dedicated database (`CREATE DATABASE learn_sql;`) instead of working in the default `postgres` database
3. Stop using the `postgres` superuser for daily practice - create a regular role so permission errors surface early

---

---

# SQL-008 Tables, Rows, and Columns

**TL;DR** - A table enforces a fixed column schema; rows hold records that obey it.

---

### 🟢 What it is

A **table** is a named structure in a database where every row represents one record and every column defines one attribute with a fixed name and data type - making the column set a contract that all rows must follow.

---

### 🎯 Why it exists

Without tables, data is just a pile of text. Imagine a customer list stored in a plain file where one line has "name, email" and the next has "email, phone, name". Every program reading that file must guess the format. When someone adds a new field, every reader breaks. Tables solve this by declaring the shape of data once - column names, types, order - and the database rejects anything that violates the contract. Queries can rely on the structure instead of parsing guesswork. This is exactly why tables, rows, and columns exist.

---

### 🧠 Mental Model

> A table is a printed form (like a tax form). Columns are the labeled boxes on the form. Rows are completed copies of the form - one per person. The form's design forces everyone to fill in the same fields.

**Memory hook:** Columns are the blueprint; rows are the data stamped from it.

---

### ⚙️ How it works

1. You define a table with `CREATE TABLE`, listing each column with a name and a data type. This declaration is the schema.
2. When you insert a row, the database checks that the values match the column types. Wrong types get rejected, not silently stored.
3. Every row in the same table has the same set of columns. A column may be NULL (empty) for a row, but the column itself always exists in the schema.
4. You query rows by referencing column names. The database knows exactly where each column's data is stored because the schema is fixed.
5. Altering a table (adding or removing columns) changes the contract for all existing and future rows.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- No types, no structure, just dumping data
CREATE TABLE customers (data TEXT);
INSERT INTO customers VALUES
  ('Alice, alice@x.com, 2024-01-15');
INSERT INTO customers VALUES
  ('bob@y.com, Bob');  -- reversed order
```

Why it's wrong: a single TEXT column gives no structure - the database cannot validate fields, enforce order, or filter by email without fragile string parsing.

**GOOD:**

```sql
CREATE TABLE customers (
  id    INTEGER PRIMARY KEY,
  name  VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  joined DATE NOT NULL
);
INSERT INTO customers (id, name, email, joined)
VALUES (1, 'Alice', 'alice@x.com', '2024-01-15');
```

Why it's right: each column has a name, type, and constraint - the database rejects bad data at insert time, and queries can filter by any individual field.

---

### ⚡ When to use / Not to use

**Use when:**

- Your data has a predictable, repeating structure (people, orders, products, events)
- You need the database to enforce data shape so application code does not have to

**Avoid when:**

- Each record has a genuinely different set of fields with no overlap - a document store or key-value model may fit better
- You are storing opaque blobs (images, PDFs) where column-level structure adds no value

---

### ⚠️ One Gotcha

**Misconception:** "A row is like an object in code - I can add any field I want at any time."
**Reality:** Rows are not flexible maps. Every row in a table has the exact same columns. If you need a new attribute, you alter the entire table schema. This rigidity is a feature - it guarantees every query knows the data shape at compile time, enabling the optimizer to plan efficient access.

---

### 📇 Revision Card

1. A table is a schema contract: column names and types declared once, enforced on every row
2. Rows conform to the column set - you cannot have a row with extra or missing columns (NULL is not missing the column, it is the column with no value)
3. Treating a table like a flexible document (single TEXT column, JSON blobs) throws away the database's ability to validate, index, and optimize

---

---

# SQL-009 Data Types - Integers, Text, Dates, Booleans

**TL;DR** - Choosing the right column type prevents bad data, saves storage, and unlocks correct operations.

---

### 🟢 What it is

**Data types** tell the database what kind of value a column holds - integer, text, date, or boolean - so it can validate input, allocate storage efficiently, and enable type-appropriate operations like arithmetic, sorting, and comparison.

---

### 🎯 Why it exists

Store a price as TEXT and you can insert "free", "$9.99", or "nine" into the same column. Now try summing all prices - the database cannot, because it does not know these are numbers. Store a birth date as VARCHAR and sorting gives you alphabetical order ("12-Jan" before "2-Feb") instead of chronological order. Every bug like this comes from the same root cause: the database was not told what the data means. Types give the database that knowledge so it can reject invalid data at the boundary, not after it corrupts downstream queries. This is exactly why data types exist.

---

### 🧠 Mental Model

> Data types are labeled jars in a kitchen. The "sugar" jar accepts only sugar. If someone puts salt in, you catch it immediately - not after the cake tastes wrong.

**Memory hook:** Types are bouncers at the gate - wrong data does not get in.

---

### ⚙️ How it works

1. **INTEGER / BIGINT:** Whole numbers. `INTEGER` holds values up to roughly 2.1 billion. `BIGINT` extends to roughly 9.2 quintillion. Use `INTEGER` for most IDs and counts; `BIGINT` for anything that might exceed 2 billion (event logs, global sequences).
2. **VARCHAR(n) / TEXT:** Character strings. `VARCHAR(n)` enforces a max length, catching data entry errors. `TEXT` (in PostgreSQL) has no practical length limit. Use `VARCHAR` when a natural boundary exists (email: 255, country code: 2). Use `TEXT` for free-form content.
3. **DATE / TIMESTAMP:** `DATE` stores calendar dates without time. `TIMESTAMP` stores date plus time-of-day. `TIMESTAMP WITH TIME ZONE` (recommended default) stores a UTC instant and converts on display. Always store instants in UTC.
4. **BOOLEAN:** `TRUE`, `FALSE`, or `NULL`. Use for binary flags (is_active, email_verified). Avoid encoding booleans as integers (0/1) or strings ('Y'/'N') - you lose type-safe comparisons.

---

### ✏️ Minimal Example

**BAD:**

```sql
CREATE TABLE products (
  id    INTEGER,
  name  TEXT,
  price TEXT,       -- "free" is valid
  added TEXT,       -- "last tuesday" is valid
  active TEXT       -- "maybe" is valid
);
```

Why it's wrong: every column is TEXT, so the database cannot reject nonsense values and arithmetic (`SUM(price)`) fails at query time.

**GOOD:**

```sql
CREATE TABLE products (
  id     INTEGER PRIMARY KEY,
  name   VARCHAR(200) NOT NULL,
  price  NUMERIC(10,2) NOT NULL
           CHECK (price >= 0),
  added  DATE NOT NULL
           DEFAULT CURRENT_DATE,
  active BOOLEAN NOT NULL
           DEFAULT TRUE
);
```

Why it's right: each column uses the narrowest correct type, so `SUM(price)` works, date sorting is chronological, and boolean filters are type-safe.

---

### ⚡ When to use / Not to use

**Use when:**

- You know the domain of valid values for a column (numbers, dates, true/false)
- You want the database to reject invalid data before it enters any table

**Avoid when:**

- The column genuinely contains mixed-format data with no predictable structure (rare in well-designed schemas - often a sign the schema needs rethinking)
- You are storing serialized blobs that the database should not interpret (use `BYTEA` or `JSONB`, not generic `TEXT`)

---

### ⚠️ One Gotcha

**Misconception:** "VARCHAR(255) is a safe default for any text column."
**Reality:** 255 is an artifact of legacy MySQL optimization, not a universal best practice. In PostgreSQL, `VARCHAR(255)` and `VARCHAR(100)` use identical storage. Pick a length that reflects the actual domain constraint (email max: 254 per RFC 5321, country code: 2 or 3). If no natural limit exists, `TEXT` is cleaner than an arbitrary number.

---

### 📇 Revision Card

1. Types let the database validate data at insert time, enable correct operations (SUM, date sorting), and optimize storage
2. Use `NUMERIC` for money (not FLOAT), `TIMESTAMPTZ` for instants (not VARCHAR), `BOOLEAN` for flags (not INTEGER 0/1)
3. VARCHAR(255) is not a magic number - choose lengths from domain constraints, or use TEXT when no natural limit exists

---

---

# SQL-010 CREATE TABLE and DROP TABLE

**TL;DR** - CREATE TABLE defines your data contract; DROP TABLE destroys it irreversibly.

---

### 🟢 What it is

**CREATE TABLE** is the DDL statement that defines a new table's columns, types, and constraints, while **DROP TABLE** permanently removes a table and all its data from the database.

---

### 🎯 Why it exists

Before you can store a single row, the database needs to know the shape of the data. What columns? What types? What constraints? Without `CREATE TABLE`, there is no structure and no contract. On the other side, schemas evolve - tables become obsolete, experiments need cleanup, migrations need to remove old structures. Without `DROP TABLE`, abandoned tables accumulate like dead code, confusing developers and wasting catalog space. Together, these two statements form the lifecycle of every table: birth and death. This is exactly why CREATE TABLE and DROP TABLE exist.

---

### 🧠 Mental Model

> `CREATE TABLE` is blueprinting a filing cabinet - you decide the drawer labels before filing any papers. `DROP TABLE` is throwing the entire cabinet into a shredder, papers included, with no recycling bin.

**Memory hook:** CREATE builds the container; DROP incinerates it.

---

### ⚙️ How it works

1. `CREATE TABLE table_name (column_name TYPE constraints, ...)` registers a new table in the database catalog. The catalog stores column metadata, types, and constraints.
2. Constraints like `NOT NULL`, `PRIMARY KEY`, `CHECK`, and `DEFAULT` are declared inline with columns. The database enforces them on every future INSERT and UPDATE.
3. `CREATE TABLE IF NOT EXISTS` avoids an error when the table already exists - useful in idempotent migration scripts that may run multiple times.
4. `DROP TABLE table_name` removes the table, all its rows, all its indexes, and all dependent objects (unless other objects reference it with foreign keys). There is no undo.
5. `DROP TABLE IF EXISTS` avoids an error when the table is already gone - the mirror guard for cleanup scripts.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- No IF NOT EXISTS - fails on second run
CREATE TABLE orders (
  id INTEGER
);
-- No IF EXISTS - fails if already dropped
DROP TABLE orders;
```

Why it's wrong: running the script twice crashes on the CREATE (table exists) or the DROP (table gone), making the migration non-idempotent.

**GOOD:**

```sql
CREATE TABLE IF NOT EXISTS orders (
  id         INTEGER PRIMARY KEY,
  customer   VARCHAR(100) NOT NULL,
  total      NUMERIC(10,2) NOT NULL
               CHECK (total >= 0),
  ordered_at TIMESTAMPTZ NOT NULL
               DEFAULT NOW()
);

-- Only when intentionally removing:
DROP TABLE IF EXISTS orders;
```

Why it's right: `IF NOT EXISTS` and `IF EXISTS` make the script safe to re-run, and the CREATE includes types, constraints, and defaults that form a meaningful contract.

---

### ⚡ When to use / Not to use

**Use when:**

- Defining a new entity in your schema - every table starts with CREATE TABLE
- Writing migration scripts that must be idempotent (safe to re-run)

**Avoid when:**

- You want to remove only the data but keep the table structure - use `TRUNCATE` or `DELETE` instead of `DROP`
- You are unsure whether other tables have foreign keys pointing to this table - dropping it will fail or cascade-destroy dependent data

---

### ⚠️ One Gotcha

**Misconception:** "DROP TABLE is like DELETE FROM - I can get the data back."
**Reality:** `DELETE` removes rows but the table survives. `DROP` removes the table itself - structure, data, indexes, constraints, everything. There is no `ROLLBACK` after a committed `DROP` (some databases auto-commit DDL). In production, a `DROP TABLE` without a backup is permanent data loss. Always verify backups exist before dropping any table outside a dev environment.

---

### 📇 Revision Card

1. CREATE TABLE defines the column contract (names, types, constraints) - design the schema before inserting data
2. Always use `IF NOT EXISTS` / `IF EXISTS` guards to make scripts idempotent
3. DROP TABLE is irreversible destruction of structure and data - it is not DELETE, and there is no undo after commit

---

---

# SQL-011 INSERT - Adding Rows

**TL;DR** - INSERT adds new rows to a table; always specify column names to prevent silent data corruption.

---

### 🟢 What it is

**INSERT** is the SQL DML statement that adds one or more
new rows to a table. It is the only standard way data
enters a relational database.

---

### 🎯 Why it exists

Without INSERT, a table is an empty container. You could
define the most elegant schema in the world, but it holds
zero value until rows exist. Applications need a
predictable, atomic way to say "put this data here" that
respects constraints, triggers defaults, and participates
in transactions. Flat-file appends give you none of that.
This is exactly why INSERT exists.

---

### 🧠 Mental Model

> INSERT is like filling out a row on a pre-printed form.
> The form (table) defines which boxes (columns) exist.
> You write values in the correct boxes, and the clerk
> (database engine) files it.

**Memory hook:** Column list = contract. No list = fragile.

---

### ⚙️ How it works

1. You specify the target table and, optionally, a column
   list that tells the engine which columns receive values.
2. You provide VALUES (literal data) or a SELECT subquery
   that supplies rows from another table.
3. The engine validates each value against the column's
   data type, NOT NULL constraints, and CHECK constraints.
4. Default values fill any columns you omitted from the
   column list.
5. If all constraints pass, the row is written to the
   table within the current transaction.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- No column list - breaks when schema changes
INSERT INTO orders
VALUES (1, 'Alice', 99.50, '2025-01-15');
```

Why it's wrong: adding a column to the table silently
shifts which value lands in which column.

**GOOD:**

```sql
-- Explicit column list - survives schema changes
INSERT INTO orders
    (customer_name, total, order_date)
VALUES
    ('Alice', 99.50, '2025-01-15');
```

Why it's right: the column list acts as a contract,
so a new column added later does not corrupt data.

Multi-row insert for bulk loading:

```sql
INSERT INTO orders
    (customer_name, total, order_date)
VALUES
    ('Alice', 99.50, '2025-01-15'),
    ('Bob',   45.00, '2025-01-16'),
    ('Carol', 120.00, '2025-01-16');
```

---

### ⚡ When to use / Not to use

**Use when:**

- Adding new records - user signups, order placements,
  log entries.
- Copying data between tables with INSERT INTO ... SELECT.

**Avoid when:**

- You need to change an existing row (use UPDATE instead).
- Bulk-loading millions of rows from a file (use COPY in
  Postgres or LOAD DATA in MySQL for orders-of-magnitude
  faster throughput).

---

### ⚠️ One Gotcha

**Misconception:** Omitting the column list is fine because
"I know the column order."
**Reality:** ALTER TABLE ADD COLUMN changes that order.
Production INSERTs without column lists break silently -
values shift into wrong columns with no error, and you
discover the corruption days later.

---

### 📇 Revision Card

1. Always list columns explicitly - it is a contract between
   your code and the schema.
2. Multi-row VALUES is faster than looping single INSERTs
   because it reduces round trips and lock acquisitions.
3. The silent-shift bug from omitting columns is the single
   most common INSERT mistake in production.

---

---

# SQL-012 SELECT and FROM - Reading Data

**TL;DR** - SELECT chooses which columns to return; FROM chooses which table to read; together they are SQL's foundation.

---

### 🟢 What it is

**SELECT** and **FROM** form the minimal SQL query. FROM
identifies the source table, and SELECT specifies which
columns (or expressions) appear in the result set.

---

### 🎯 Why it exists

Data locked inside a table is useless until you can
retrieve it. Applications need to ask precise questions:
"show me customer names" or "calculate each order's tax."
Before SQL, programmers wrote procedural loops to scan
files record by record. SELECT/FROM lets you declare
_what_ you want and leave the _how_ to the query engine.
This is exactly why SELECT and FROM exist.

---

### 🧠 Mental Model

> FROM is choosing which filing cabinet to open. SELECT is
> choosing which fields on each form to photocopy. You
> always open the cabinet first, then pick the fields.

**Memory hook:** FROM runs first, SELECT runs last.

---

### ⚙️ How it works

1. The engine resolves FROM first - it identifies the table
   and makes all its columns available.
2. Any WHERE, GROUP BY, or HAVING clauses filter and shape
   rows (covered in later keywords).
3. SELECT runs logically last - it projects only the
   requested columns or evaluates expressions.
4. The result set is returned to the client as a temporary
   collection of rows with no guaranteed order.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- SELECT * fetches every column, including BLOBs
-- and columns you will never use
SELECT * FROM customers;
```

Why it's wrong: wastes network bandwidth, breaks when
columns are added, and prevents covering-index
optimizations.

**GOOD:**

```sql
-- Explicit columns: clear intent, stable contract
SELECT customer_id, name, email
FROM   customers;
```

Why it's right: the query declares exactly what the
application needs. Adding a column to the table changes
nothing in this query's output.

Expression example:

```sql
SELECT order_id,
       quantity * unit_price AS line_total
FROM   order_items;
```

---

### ⚡ When to use / Not to use

**Use when:**

- Reading any data from a relational database - literally
  every read operation starts with SELECT FROM.
- Computing derived values with expressions in the SELECT
  list.

**Avoid when:**

- You want to modify data (use INSERT, UPDATE, or DELETE).
- You need SELECT \* in production code (almost never
  justified outside ad-hoc debugging).

---

### ⚠️ One Gotcha

**Misconception:** SELECT runs before FROM because it
appears first in the syntax.
**Reality:** SQL's logical processing order is FROM ->
WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY.
Understanding this order is essential for debugging
column-alias errors: you cannot use a SELECT alias in
the WHERE clause because WHERE executes before SELECT.

---

### 📇 Revision Card

1. FROM identifies the data source; SELECT projects columns
   and evaluates expressions.
2. Logical processing order: FROM first, SELECT near last -
   this explains most "column not found" errors.
3. SELECT \* is a debugging tool, not a production pattern -
   it couples your code to every schema change.

---

---

# SQL-013 WHERE - Filtering Rows

**TL;DR** - WHERE eliminates rows that fail a Boolean predicate before any other processing happens.

---

### 🟢 What it is

**WHERE** is the clause that filters rows from the FROM
source by evaluating a Boolean predicate against each
row. Only rows where the predicate evaluates to TRUE
survive into the result set.

---

### 🎯 Why it exists

Tables hold thousands to billions of rows. Returning all
of them when you only need "orders placed today" buries
the application in irrelevant data, wastes network
bandwidth, and makes the database do unnecessary work.
You need a declarative way to say "give me only the rows
that match these conditions." This is exactly why WHERE
exists.

---

### 🧠 Mental Model

> WHERE is a bouncer at a nightclub door. Every row walks
> up; the bouncer checks the predicate (age >= 21?). Rows
> that pass get in. Rows that fail are turned away before
> they reach the dance floor (SELECT).

**Memory hook:** WHERE is the gatekeeper between FROM
and everything else.

---

### ⚙️ How it works

1. The engine scans (or seeks via an index) the rows
   identified by FROM.
2. For each row, it evaluates the WHERE predicate.
3. Rows yielding TRUE pass through. Rows yielding FALSE
   or UNKNOWN (NULL comparisons) are discarded.
4. Surviving rows proceed to GROUP BY or directly to
   SELECT.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Fetches ALL orders, filters in application code
SELECT order_id, total, status
FROM   orders;
-- app: for row in rows: if row.status == 'shipped' ...
```

Why it's wrong: transferring 10 million rows to filter
in the app wastes bandwidth, memory, and time. The
database has indexes - use them.

**GOOD:**

```sql
SELECT order_id, total
FROM   orders
WHERE  status = 'shipped'
  AND  order_date >= '2025-01-01';
```

Why it's right: the database eliminates non-matching rows
before any data leaves the server, and the engine can use
an index on status or order_date to avoid a full scan.

Compound predicates:

```sql
SELECT product_id, name, price
FROM   products
WHERE  price BETWEEN 10 AND 50
  AND  category IN ('books', 'electronics')
  AND  name LIKE 'Pro%';
```

---

### ⚡ When to use / Not to use

**Use when:**

- You need a subset of rows - date ranges, status checks,
  category membership, pattern matching.
- Reducing data volume before aggregation or joining.

**Avoid when:**

- Filtering on computed aggregates - use HAVING instead
  (WHERE cannot reference aggregate functions).
- Applying row-number or ranking filters - use window
  functions or LIMIT.

---

### ⚠️ One Gotcha

**Misconception:** `WHERE status != 'cancelled'` returns
all non-cancelled rows.
**Reality:** Rows where status is NULL also disappear.
NULL != 'cancelled' evaluates to UNKNOWN, not TRUE.
Three-valued logic means you must write
`WHERE status != 'cancelled' OR status IS NULL`
if you want NULL rows included.

---

### 📇 Revision Card

1. WHERE runs right after FROM - before GROUP BY, HAVING,
   and SELECT in logical order.
2. Any comparison with NULL yields UNKNOWN, which WHERE
   treats as "not true" - rows silently vanish.
3. Push filtering into WHERE (server-side) instead of the
   application to leverage indexes and reduce data transfer.

---

---

# SQL-014 UPDATE and DELETE - Modifying Data

**TL;DR** - UPDATE changes existing rows; DELETE removes them; both destroy data, so a missing WHERE clause is catastrophic.

---

### 🟢 What it is

**UPDATE** modifies column values in existing rows.
**DELETE** removes entire rows from a table. Both are DML
statements that permanently alter data when committed.

---

### 🎯 Why it exists

Data is not static. Customers change addresses. Orders get
cancelled. Inventory quantities shift. Without UPDATE and
DELETE, you would have to drop and recreate entire tables
to fix a single typo. These statements let you surgically
modify or remove specific rows while the rest of the table
remains untouched. This is exactly why UPDATE and DELETE
exist.

---

### 🧠 Mental Model

> UPDATE is using correction fluid on a specific cell in a
> spreadsheet. DELETE is ripping out an entire row. Both are
> permanent unless you have "undo" turned on (transactions).

**Memory hook:** No WHERE = entire table. Always.

---

### ⚙️ How it works

1. The engine identifies rows matching the WHERE predicate
   (identical to how WHERE works in SELECT).
2. For UPDATE, it writes new values into the specified
   columns for each matching row. For DELETE, it marks
   each matching row for removal.
3. Triggers and foreign key constraints fire. A constraint
   violation rolls back the statement.
4. On COMMIT, changes become permanent and visible to other
   transactions.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Missing WHERE - updates EVERY row in the table
UPDATE products
SET    price = 0.00;

-- Missing WHERE - deletes EVERY row
DELETE FROM orders;
```

Why it's wrong: the entire table is affected. This is
the most destructive single-statement mistake in SQL.

**GOOD:**

```sql
-- Always confirm scope with SELECT first
SELECT product_id, name, price
FROM   products
WHERE  product_id = 42;

-- Then apply the change to the same predicate
UPDATE products
SET    price = 29.99
WHERE  product_id = 42;

-- Safe delete with specific predicate
DELETE FROM orders
WHERE  order_id = 1001
  AND  status = 'cancelled';
```

Why it's right: the SELECT-first pattern lets you verify
which rows match before you commit to the mutation.

---

### ⚡ When to use / Not to use

**Use when:**

- Correcting data - fixing typos, updating statuses,
  adjusting quantities.
- Removing invalid or expired records.

**Avoid when:**

- You need an audit trail of changes - consider soft
  deletes (SET deleted_at = NOW()) or an audit log table
  instead of hard DELETE.
- Updating millions of rows in a single statement - batch
  the work to avoid long-running locks and transaction log
  bloat.

---

### ⚠️ One Gotcha

**Misconception:** "I'll just run the UPDATE and fix it
if something goes wrong."
**Reality:** Without a transaction, the change is
committed immediately on most default configurations.
There is no undo button. Wrap destructive statements in
BEGIN / ROLLBACK to preview the effect, then COMMIT only
after verifying the row count.

---

### 📇 Revision Card

1. Always run the equivalent SELECT with the same WHERE
   clause before executing UPDATE or DELETE.
2. A missing WHERE clause affects every row in the table -
   no warning, no confirmation prompt.
3. Wrap destructive operations in explicit transactions
   (BEGIN ... ROLLBACK/COMMIT) to give yourself an undo
   window.

---

---

# SQL-015 ORDER BY and LIMIT

**TL;DR** - ORDER BY sorts results deterministically; LIMIT caps how many rows return; without ORDER BY, row order is random.

---

### 🟢 What it is

**ORDER BY** sorts the result set by one or more columns
or expressions. **LIMIT** (or TOP, FETCH FIRST, depending
on the database) restricts the number of rows returned.

---

### 🎯 Why it exists

Relational databases store rows in no particular order.
The physical layout depends on the storage engine, insert
sequence, page splits, and vacuuming. Two identical queries
can return rows in different orders on different runs.
Applications that display "most recent orders" or "top 10
products" need deterministic sorting and a row cap. This is
exactly why ORDER BY and LIMIT exist.

---

### 🧠 Mental Model

> ORDER BY is sorting a deck of cards by suit and rank.
> LIMIT is picking only the top N cards off the sorted
> deck. Without sorting first, "top N" is meaningless -
> you are just grabbing random cards.

**Memory hook:** No ORDER BY = no guaranteed order. Ever.

---

### ⚙️ How it works

1. The engine completes all FROM, WHERE, GROUP BY, HAVING,
   and SELECT processing first.
2. ORDER BY sorts the entire result set by the specified
   columns. ASC (ascending) is the default; DESC reverses.
3. LIMIT N takes the first N rows from the sorted output.
4. OFFSET M skips the first M rows before taking N - this
   is how naive pagination works.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Pagination with large OFFSET - database must compute
-- and discard 100,000 rows before returning 20
SELECT order_id, total
FROM   orders
ORDER BY created_at DESC
LIMIT  20 OFFSET 100000;
```

Why it's wrong: OFFSET does not skip cheaply. The engine
sorts and counts through all 100,020 rows, discards
100,000, and returns 20. Performance degrades linearly
with page depth.

**GOOD:**

```sql
-- Keyset pagination - seeks directly to the cursor
SELECT order_id, total
FROM   orders
WHERE  created_at < '2025-03-15T10:30:00'
ORDER BY created_at DESC
LIMIT  20;
```

Why it's right: the WHERE clause uses an index to skip
directly past already-seen rows. Performance is constant
regardless of page depth.

Basic sorting with multiple columns:

```sql
SELECT name, department, hire_date
FROM   employees
ORDER BY department ASC,
         hire_date DESC;
```

---

### ⚡ When to use / Not to use

**Use when:**

- Displaying results in a predictable sequence - dates,
  names, rankings, scores.
- Implementing pagination in any user-facing application.

**Avoid when:**

- You only need existence ("does this row exist?") - ORDER
  BY adds unnecessary sorting cost. Use EXISTS or LIMIT 1
  without ORDER BY.
- Deep pagination with OFFSET beyond a few thousand rows -
  switch to keyset (cursor-based) pagination.

---

### ⚠️ One Gotcha

**Misconception:** "My query always returns rows in
insertion order, so I do not need ORDER BY."
**Reality:** That is an accident of the current execution
plan. A parallel worker, an index change, a VACUUM, or a
Postgres upgrade can shuffle the order at any time. The
SQL standard says result order is undefined without ORDER
BY. If order matters, specify it explicitly.

---

### 📇 Revision Card

1. Without ORDER BY, SQL guarantees nothing about row
   order - not even consistency between executions.
2. OFFSET pagination gets slower with every page because
   the engine must process and discard all skipped rows.
3. Keyset (cursor-based) pagination solves the OFFSET
   problem by seeking via an indexed WHERE predicate.

---

---

# SQL-016 Primary Keys and Uniqueness

> Entry stub. Generate full content using LEARN_PROMPT.md v1.0. Template: SIMPLE.

---

---

# SQL-017 Foreign Keys and Relationships

> Entry stub. Generate full content using LEARN_PROMPT.md v1.0. Template: SIMPLE.

---

---

# SQL-018 NULL - The Three-Valued Logic Trap

> Entry stub. Generate full content using LEARN_PROMPT.md v1.0. Template: SIMPLE.

---

---

# SQL-019 SELECT \* in Production Anti-Pattern

> Entry stub. Generate full content using LEARN_PROMPT.md v1.0. Template: SIMPLE.

---

---

# SQL-020 psql and pgAdmin - First Tools

> Entry stub. Generate full content using LEARN_PROMPT.md v1.0. Template: SIMPLE.

---

---

# SQL-021 DBeaver - Universal Database Client

**TL;DR** - One free GUI client connects to every database, so you learn SQL instead of learning tools.

---

### 🟢 What it is

**DBeaver** is a free, open-source, cross-platform database client that connects to PostgreSQL, MySQL, Oracle, SQLite, and dozens more through a single interface.

---

### 🎯 Why it exists

Every database vendor ships its own GUI. PostgreSQL has pgAdmin,
MySQL has Workbench, Oracle has SQL Developer. Each tool has
different shortcuts, different export flows, different quirks.
When you are learning SQL, you waste time relearning the tool
every time you switch databases. Your muscle memory resets. Your
workflows break. Vendor lock-in starts at the GUI level. This is
exactly why DBeaver exists.

---

### 🧠 Mental Model

> DBeaver is a universal TV remote. Instead of keeping five
> remotes on the coffee table - one per database vendor - you
> learn one set of buttons that controls everything.

**Memory hook:** One remote, every database.

---

### ⚙️ How it works

1. Install DBeaver Community Edition (free, open source) from
   dbeaver.io - available on Windows, macOS, and Linux.
2. Create a new connection by selecting your database type.
   DBeaver downloads the correct JDBC driver automatically.
3. Enter connection details (host, port, database, credentials)
   and click "Test Connection" to verify before saving.
4. The Database Navigator tree shows schemas, tables, columns,
   data types, and foreign keys - no SQL needed to explore
   structure.
5. Open a SQL editor with Ctrl+] to write queries. Execute
   with Ctrl+Enter. Results appear in a sortable, filterable
   grid you can export to CSV, JSON, or SQL INSERT statements.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Terminal-only workflow: raw psql
\dt
-- 30 tables scroll past. Which columns
-- does "orders" have again?
\d orders
-- Now manually type the JOIN...
-- Typo in column name. Error. Retype.
```

Why it's wrong: no autocomplete, no visual schema, no way to
see relationships at a glance.

**GOOD:**

```sql
-- In DBeaver: expand tables in navigator,
-- right-click orders > "View Diagram"
-- See all FKs visually. Then in SQL editor:
SELECT c.name, o.order_date, o.total
FROM customers c
  JOIN orders o ON c.id = o.customer_id
WHERE o.total > 100
ORDER BY o.order_date DESC;
-- Ctrl+Enter to run. Export grid to CSV.
```

Why it's right: autocomplete catches typos, ER diagrams show
relationships visually, and export is two clicks.

---

### ⚡ When to use / Not to use

**Use when:**

- Learning SQL and you want visual feedback on schema structure
- Working with multiple database engines in the same project
- You need to quickly explore an unfamiliar database

**Avoid when:**

- Running automated scripts in CI/CD pipelines (use psql or
  mysql CLI instead)
- You need database-specific admin features like replication
  setup or WAL management that only the vendor tool exposes

---

### ⚠️ One Gotcha

**Misconception:** DBeaver's auto-commit is off by default, so
my changes are safe.

**Reality:** DBeaver defaults to auto-commit ON for most
connection types. Every INSERT, UPDATE, or DELETE executes
immediately with no rollback. Toggle auto-commit off manually
(toolbar button) when experimenting with data you care about.

---

### 📇 Revision Card

1. DBeaver connects to any JDBC-compatible database through one
   interface - learn one tool, use it everywhere
2. The ER diagram view (right-click table > View Diagram) reveals
   foreign key relationships without writing SQL
3. Auto-commit is ON by default - toggle it off before running
   UPDATE or DELETE on real data

---

---

# SQL-022 Online Store DB - Phase 1 (Schema and CRUD)

**TL;DR** - Build a four-table e-commerce schema from scratch, then practice every CRUD operation against it.

---

### 🟢 What it is

**Online Store DB - Phase 1** is a hands-on exercise where you design a simple e-commerce database with customers, products, orders, and order items, then run CREATE, INSERT, SELECT, UPDATE, and DELETE queries against it.

---

### 🎯 Why it exists

Reading about tables and keys is passive. You nod along, feel
confident, then freeze when facing a blank SQL editor. The gap
between "I understand SELECT" and "I can design a schema and
populate it" is enormous. Typing real DDL and DML against a
schema you built yourself forces the syntax into muscle memory.
This is exactly why this practice exercise exists.

---

### 🧠 Mental Model

> This exercise is an assembly kit. The instruction manual
> (schema) tells you which pieces connect where. The screws
> and bolts (foreign keys) hold the structure together. You
> cannot skip steps - the orders table needs the customers
> table to exist first.

**Memory hook:** Build the shelves before you stock the products.

---

### ⚙️ How it works

1. Create the `customers` table first - it has no foreign key
   dependencies.
2. Create `products` next - also independent.
3. Create `orders` with a foreign key to `customers` - an order
   belongs to exactly one customer.
4. Create `order_items` last - it references both `orders` and
   `products`.
5. Insert sample data in dependency order: customers first,
   then products, then orders, then order_items.

---

### ✏️ Minimal Example

**BAD:**

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT,
  order_date DATE
);
-- No FK constraint. Nothing stops you from
-- inserting customer_id = 9999 (nonexistent).
-- Orphan rows silently corrupt your data.
```

Why it's wrong: missing foreign keys let invalid data slip in
without any warning.

**GOOD:**

```sql
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price NUMERIC(10,2) NOT NULL
    CHECK (price > 0)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL
    REFERENCES customers(id),
  order_date DATE NOT NULL
    DEFAULT CURRENT_DATE
);

CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INT NOT NULL
    REFERENCES orders(id),
  product_id INT NOT NULL
    REFERENCES products(id),
  quantity INT NOT NULL
    CHECK (quantity > 0)
);

-- Insert in dependency order:
INSERT INTO customers (name, email)
VALUES ('Alice Park', 'alice@example.com');

INSERT INTO products (name, price)
VALUES ('Mechanical Keyboard', 89.99);

INSERT INTO orders (customer_id)
VALUES (1);

INSERT INTO order_items
  (order_id, product_id, quantity)
VALUES (1, 1, 2);
```

Why it's right: foreign keys enforce referential integrity,
CHECK constraints prevent negative prices and zero quantities,
and NOT NULL stops silent blanks.

---

### ⚡ When to use / Not to use

**Use when:**

- You have learned CREATE TABLE, INSERT, SELECT, UPDATE, DELETE
  individually and need to combine them
- You want a reusable sandbox database for later exercises
  covering JOINs, aggregations, and subqueries

**Avoid when:**

- You have not yet covered primary keys and foreign keys
  (complete SQL-016 and SQL-017 first)
- You are looking for a production e-commerce schema (this is
  intentionally simplified for learning)

---

### ⚠️ One Gotcha

**Misconception:** You can DROP tables in any order when
resetting the database.

**Reality:** You must drop in reverse dependency order
(order_items, orders, then products and customers) or use
`DROP TABLE ... CASCADE`. Dropping `customers` first fails
because `orders` still references it via foreign key.

---

### 📇 Revision Card

1. Create tables in dependency order: independent tables first,
   then tables with foreign keys pointing to them
2. Every foreign key column should be NOT NULL unless the
   relationship is genuinely optional
3. DROP order is reversed: children first, parents last - or
   use CASCADE (but understand what it deletes)

---

---

# SQL-023 Basic SELECT Exercises

**TL;DR** - Seven progressively harder SELECT drills turn passive knowledge into confident querying.

---

### 🟢 What it is

**Basic SELECT Exercises** is a set of practice drills covering SELECT, WHERE, ORDER BY, and LIMIT using the online store schema from SQL-022.

---

### 🎯 Why it exists

You have read about SELECT, WHERE, ORDER BY. You can recognize
them in examples. But when someone says "show me all orders over
$50 sorted by date," your fingers hesitate. The only cure for
that hesitation is repetition against a real schema where you can
verify your own results. This is exactly why these exercises
exist.

---

### 🧠 Mental Model

> These drills are scales for a musician. Concert pianists do
> not skip scales because they are "basic" - they play them
> daily because fluency comes from repetition, not
> understanding alone.

**Memory hook:** Scales before sonatas. SELECT drills before
JOIN queries.

---

### ⚙️ How it works

1. Set up the online store schema from SQL-022 with sample data
   (at least 5 customers, 8 products, 10 orders, 15 order
   items).
2. Read each exercise prompt below. Write your query before
   looking at the solution.
3. Run your query and compare results with the expected output.
4. If your result differs, debug before checking the solution.
5. After completing all exercises, modify each query (change the
   filter, sort differently) to reinforce the pattern.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Copying a tutorial query and changing one name
SELECT * FROM products;
-- Feels productive. You learned nothing.
-- SELECT * hides which columns you actually need.
```

Why it's wrong: recognition is not recall - modify the
problem, not just the column name.

**GOOD:**

```sql
-- Write from scratch, check, then compare:
SELECT name, price
FROM products
WHERE price > 50
ORDER BY price ASC;
```

Why it's right: building from a blank editor forces you to
recall syntax instead of pattern-matching from an example.

_Try each exercise below before reading the solution._

**Ex 1:** List all product names and prices.

```sql
SELECT name, price FROM products;
```

**Ex 2:** Find products priced above $50, cheapest first.

```sql
SELECT name, price
FROM products
WHERE price > 50
ORDER BY price ASC;
```

**Ex 3:** Show the 3 most expensive products.

```sql
SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 3;
```

**Ex 4:** Find customers whose name starts with 'A'.

```sql
SELECT name, email
FROM customers
WHERE name LIKE 'A%';
```

**Ex 5:** List orders placed in the last 30 days.

```sql
SELECT id, customer_id, order_date
FROM orders
WHERE order_date >=
  CURRENT_DATE - INTERVAL '30 days'
ORDER BY order_date DESC;
```

**Ex 6:** Find order items where quantity exceeds 3.

```sql
SELECT product_id, quantity
FROM order_items
WHERE quantity > 3
ORDER BY quantity DESC;
```

**Ex 7 (challenge):** List products never ordered. (Hint:
subquery.)

```sql
SELECT name, price
FROM products
WHERE id NOT IN (
  SELECT DISTINCT product_id
  FROM order_items
);
```

---

### ⚡ When to use / Not to use

**Use when:**

- You have completed SQL-012 through SQL-015 and want to test
  yourself without copying from examples
- You can write SELECT but lack confidence building queries
  from scratch

**Avoid when:**

- You have not created the online store schema yet (do SQL-022
  first)
- You are already comfortable with single-table queries and
  ready for JOINs

---

### ⚠️ One Gotcha

**Misconception:** LIMIT grabs the "top N" rows from the table.

**Reality:** Without ORDER BY, LIMIT returns arbitrary rows -
the database picks whichever rows it finds first, and that
order can change between runs. Always pair LIMIT with ORDER BY
to get deterministic results.

---

### 📇 Revision Card

1. WHERE filters rows before ORDER BY sorts them - LIMIT cuts
   after sorting
2. LIKE patterns: `%` matches any sequence of characters, `_`
   matches exactly one character
3. LIMIT without ORDER BY returns unpredictable rows - always
   sort first when limiting results

---

---

# SQL-024 Top 10 SQL Interview Questions - Basics

**TL;DR** - Ten foundational questions that separate candidates who understand databases from those who memorized syntax.

---

### 🟢 What it is

**Top 10 SQL Interview Questions - Basics** is a collection of the most frequently asked beginner SQL interview questions with concise, accurate answers and follow-up traps to watch for.

---

### 🎯 Why it exists

Interviewers ask about primary keys, NULLs, and DELETE vs
TRUNCATE to gauge whether you understand relational concepts or
just memorized syntax. Stumbling on "What is a primary key?"
signals you skipped fundamentals. The answers are not hard, but
giving a crisp, confident response under pressure requires
preparation. This is exactly why this review exists.

---

### 🧠 Mental Model

> Interview questions are spot checks on a construction site.
> The inspector does not test every beam - they pick a few
> critical joints to see if the whole structure is sound. A
> fumbled answer on "What is NULL?" suggests deeper gaps.

**Memory hook:** Five minutes of prep saves five years of
regret.

---

### ⚙️ How it works

1. Read the question and formulate your answer out loud (not
   silently - speaking reveals gaps).
2. Compare with the reference answer below.
3. For each answer, note one detail you missed.
4. Practice the weakest three questions again the next day.
5. For preview topics (JOINs, HAVING), focus on the core
   distinction - detailed coverage comes in later keywords.

---

### ✏️ Minimal Example

**BAD:**

```sql
-- Interview: "What does NULL mean?"
-- Bad answer in code:
SELECT * FROM customers
WHERE email = NULL;
-- Returns zero rows. Always.
-- NULL is not a value you can compare with =.
```

Why it's wrong: treating NULL like a regular value reveals
a fundamental misunderstanding of three-valued logic.

**GOOD:**

```sql
-- Correct approach:
SELECT * FROM customers
WHERE email IS NULL;
-- IS NULL is the only valid NULL test.
```

Why it's right: demonstrates you understand NULL semantics,
not just syntax.

**Q1: What is a primary key?**
A column (or set of columns) that uniquely identifies each row.
It enforces uniqueness and implicitly creates a NOT NULL
constraint. Every table should have one.

**Q2: DELETE vs TRUNCATE?**
DELETE removes rows one at a time, supports WHERE, fires
triggers, and is fully logged for rollback. TRUNCATE removes all
rows by deallocating pages - faster, but no WHERE, typically no
rollback, and no row-level triggers.

**Q3: What is NULL?**
NULL means "unknown" or "missing" - not zero, not empty string.
Any comparison with NULL (including `NULL = NULL`) returns NULL,
not true or false. Use `IS NULL` or `IS NOT NULL` to test.

**Q4: WHERE vs HAVING?**
WHERE filters rows before GROUP BY. HAVING filters groups after
aggregation. You cannot use COUNT or SUM in WHERE. (Depth in a
later keyword.)

**Q5: What is a foreign key?**
A column that references another table's primary key, enforcing
referential integrity. It prevents orphan rows - you cannot
insert an order for a customer that does not exist.

**Q6: INNER JOIN vs OUTER JOIN? (preview)**
INNER JOIN returns only matching rows from both tables. LEFT
JOIN also returns unmatched rows from the left table, filling
the right side with NULLs. (Full coverage in a later keyword.)

**Q7: What does DISTINCT do?**
Removes duplicate rows from results. `SELECT DISTINCT city`
returns each city once. It applies to the entire row, not just
one column.

**Q8: CHAR vs VARCHAR?**
CHAR(n) stores fixed-length strings padded with spaces.
VARCHAR(n) stores variable-length strings up to n characters.
Use VARCHAR for most cases - CHAR wastes space.

**Q9: What does ORDER BY do?**
Sorts results by one or more columns. Default is ascending
(ASC). Without ORDER BY, SQL guarantees no particular row order.

**Q10: Can you SELECT without FROM?**
In most databases, yes. `SELECT 1 + 1;` returns 2 in PostgreSQL
and MySQL. Oracle requires `FROM dual`. Useful for testing
expressions.

---

### ⚡ When to use / Not to use

**Use when:**

- Preparing for junior or mid-level SQL interviews
- Reviewing fundamentals after a break from SQL
- Checking for gaps in your mental model of relational basics

**Avoid when:**

- You need depth on JOINs, subqueries, or aggregation (those
  have dedicated keywords)
- You are preparing for staff or principal-level interviews
  (see SQL-125)

---

### ⚠️ One Gotcha

**Misconception:** Knowing the textbook answer is enough.

**Reality:** Interviewers follow up. "What is a primary key?"
becomes "Can a table have no primary key?" (technically yes, but
it should not). Then: "Surrogate vs natural key?" Practice the
follow-up questions, not just the surface answer.

---

### 📇 Revision Card

1. NULL is not zero or empty string - any comparison with NULL
   yields NULL, not false
2. DELETE is row-by-row with WHERE support; TRUNCATE is bulk
   removal without filtering
3. WHERE filters before GROUP BY; HAVING filters after - never
   use HAVING where WHERE would work

---

---

# SQL-025 SQL Aliases and Expressions

**TL;DR** - Aliases name columns and tables for readability; expressions compute values directly inside SELECT.

---

### 🟢 What it is

**SQL Aliases and Expressions** let you give readable names to columns, tables, and computed values within a query using the AS keyword, and compute new values inline with arithmetic, string functions, and CASE.

---

### 🎯 Why it exists

Without aliases, a query like `SELECT price * quantity` produces
a column labeled `?column?` in PostgreSQL or `Expr1` in SQL
Server. Nobody knows what that means. Table names like
`order_items` clutter multi-table queries when repeated in every
JOIN and WHERE clause. Computed columns have no name at all
until you give them one. This is exactly why aliases exist.

---

### 🧠 Mental Model

> Aliases are name tags at a conference. The person's legal name
> (the real table or column) stays the same, but the tag (alias)
> makes conversation far easier. You say "oi" instead of
> "order_items" for the rest of the query.

**Memory hook:** No alias on a computed column = unnamed column.
Unnamed columns break everything downstream.

---

### ⚙️ How it works

1. Column alias: `SELECT price * quantity AS line_total` gives
   the computed column a name.
2. Table alias: `FROM order_items AS oi` lets you write
   `oi.quantity` instead of `order_items.quantity`.
3. The AS keyword is optional in most databases, but always
   write it for clarity.
4. Aliases defined in SELECT are NOT available in WHERE because
   WHERE executes before SELECT in the logical query order.
   Use the original expression or wrap in a subquery.
5. CASE expressions produce conditional values inline:
   `CASE WHEN price > 100 THEN 'premium' ELSE 'standard' END
AS tier`.

---

### ✏️ Minimal Example

**BAD:**

```sql
SELECT name, price * 1.08
FROM products;
-- Output column: "?column?"
-- What does 1.08 mean? Tax? Markup?
-- Anyone reading this query is guessing.
```

Why it's wrong: unnamed computed columns are unreadable and
break downstream tools that reference column names.

**GOOD:**

```sql
SELECT
  p.name AS product_name,
  p.price AS base_price,
  p.price * 1.08 AS price_with_tax,
  CASE
    WHEN p.price > 100 THEN 'premium'
    WHEN p.price > 30  THEN 'mid-range'
    ELSE 'budget'
  END AS price_tier
FROM products AS p
ORDER BY price_with_tax DESC;
```

Why it's right: every column has a clear name, the table alias
shortens the query, and the CASE expression categorizes inline.

---

### ⚡ When to use / Not to use

**Use when:**

- Computed columns need meaningful names for reports or
  application code
- Multi-table queries where full table names make SQL hard
  to read

**Avoid when:**

- Single-table, single-column queries where the original name
  is already clear (aliasing `name AS name` is noise)
- You are tempted to use single-letter aliases in complex
  queries with 5+ tables (use 2-3 letter abbreviations instead)

---

### ⚠️ One Gotcha

**Misconception:** You can use a column alias in WHERE, like
`WHERE price_with_tax > 50`.

**Reality:** Most databases reject this because WHERE executes
before SELECT in the logical query order. PostgreSQL, MySQL, and
SQL Server all fail on this. Use the original expression in
WHERE (`WHERE price * 1.08 > 50`) or wrap the query in a
subquery and filter the outer query.

---

### 📇 Revision Card

1. Always alias computed columns - unnamed columns produce
   `?column?` or `Expr1` that nothing downstream can reference
2. Table aliases shorten queries and are required when
   self-joining a table to itself
3. Column aliases from SELECT cannot be used in WHERE - the
   logical execution order is FROM, WHERE, SELECT
