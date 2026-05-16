# Learn - Topic Registry

> This registry maps topics to their byte folders and links them to
> existing dictionary categories where applicable. Start with core
> topics; grow organically as new topics are added.

---

## Spec References

| File                                                | Purpose                                      |
| --------------------------------------------------- | -------------------------------------------- |
| `learn/_config/LEARN_KEYWORD_GENERATOR.md`          | Master keyword generation spec (v1.0)        |
| `.github/prompts/learn-generate-keywords.prompt.md` | Prompt for topic/subtopic keyword processing |
| `learn/_config/LEARN_PROMPT.md`                     | Master content generation spec (v1.0)        |

## Design Considerations

1. **New topic (no folder/index.md):** Use `learn/_config/LEARN_KEYWORD_GENERATOR.md` v1.0 to generate keywords. Create folder + index.md. Group keywords into sub-topic files (5+ keywords per file). Generate content per `LEARN_PROMPT.md`.
2. **Brand-new topic (e.g., Angular):** Analyse where the topic belongs. Generate keywords via `learn/_config/LEARN_KEYWORD_GENERATOR.md`. Create folder + files. Generate content.
3. **New subtopic (e.g., React Hooks, topic exists):** Create file in existing folder. Generate keywords via `learn/_config/LEARN_KEYWORD_GENERATOR.md`. Generate content.
4. **Existing dictionary category (e.g., JVM, JCC):** Scan dictionary `index.md`. Analyse keywords. Map to learn sub-topic files. Generate content.

---

## Registry Format

| Topic        | Folder         | Dictionary Sources           | Status                                       |
| ------------ | -------------- | ---------------------------- | -------------------------------------------- |
| [Topic Name] | [folder-name/] | [CODE1, CODE2, ...] or "new" | planned / scaffolded / generating / complete |

---

## Active Topics

| Topic            | Folder            | Code | Archetype      | ID Range         | Count | Dictionary Sources | Status     | Description                                                                       |
| ---------------- | ----------------- | ---- | -------------- | ---------------- | ----- | ------------------ | ---------- | --------------------------------------------------------------------------------- |
| Java Language    | java/             | JLG  | LANGUAGE       | JLG-001..JLG-062 | 62    | JLG                | scaffolded | The Java language proper: syntax, types, generics, collections, modern features.  |
| Java JVM         | java-jvm/         | JVM  | INFRASTRUCTURE | JVM-001..JVM-132 | 132   | JVM                | scaffolded | Runtime: classloader, bytecode, JIT, GC, JFR, diagnostics, tuning.                |
| Java Concurrency | java-concurrency/ | JCC  | CS-CONCEPT     | JCC-001..JCC-092 | 92    | JCC                | scaffolded | Threading, synchronization, virtual threads, Loom, concurrent collections.        |
| Spring Ecosystem | spring/           | SPR  | FRAMEWORK      | SPR-001..SPR-115 | 115   | SPR                | scaffolded | Spring Framework, Boot, Data, Security, Cloud, WebFlux, Batch.                    |
| SQL              | sql/              | SQL  | LANGUAGE       | SQL-001..SQL-142 | 142   | new                | scaffolded | SQL language: DML, DDL, joins, subqueries, window functions, optimization, admin. |
| Hibernate ORM    | hibernate/        | HIB  | FRAMEWORK      | HIB-001..HIB-115 | 115   | new                | scaffolded | Hibernate ORM and JPA: entity mapping, caching, performance, provider internals.  |

---

## Sub-topic File Mapping

Each topic is split into sub-topic files. Each file MUST contain at
least 5 related keywords (no per-keyword files). Files are grouped by
relatedness and must be self-sufficient.

### Java Language (java/)

| File                                                                                  | Keywords | Levels         | Status |
| ------------------------------------------------------------------------------------- | -------- | -------------- | ------ |
| [Java - Language Core](../java/Java%20-%20Language%20Core.md)                         | 15       | L0 + L1        | stub   |
| [Java - Generics and Collections](../java/Java%20-%20Generics%20and%20Collections.md) | 10       | L2             | stub   |
| [Java - Exceptions and IO](../java/Java%20-%20Exceptions%20and%20IO.md)               | 7        | L2 + L3        | stub   |
| [Java - Modern Features](../java/Java%20-%20Modern%20Features.md)                     | 14       | L3 + L4        | stub   |
| [Java - Production Practice](../java/Java%20-%20Production%20Practice.md)             | 8        | L4             | stub   |
| [Java - Architecture and META](../java/Java%20-%20Architecture%20and%20META.md)       | 8        | L5 + L6 + META | stub   |

### Java JVM (java-jvm/)

| File                                                                                                  | Keywords | Levels         | Status |
| ----------------------------------------------------------------------------------------------------- | -------- | -------------- | ------ |
| [Java JVM - Runtime Foundations](../java-jvm/Java%20JVM%20-%20Runtime%20Foundations.md)               | 25       | L0 + L1        | stub   |
| [Java JVM - Memory and GC Essentials](../java-jvm/Java%20JVM%20-%20Memory%20and%20GC%20Essentials.md) | 22       | L2             | stub   |
| [Java JVM - GC Internals and Tuning](../java-jvm/Java%20JVM%20-%20GC%20Internals%20and%20Tuning.md)   | 28       | L3             | stub   |
| [Java JVM - Production Diagnostics](../java-jvm/Java%20JVM%20-%20Production%20Diagnostics.md)         | 26       | L4             | stub   |
| [Java JVM - Architecture and Strategy](../java-jvm/Java%20JVM%20-%20Architecture%20and%20Strategy.md) | 31       | L5 + L6 + META | stub   |

### Java Concurrency (java-concurrency/)

| File                                                                                                                                        | Keywords | Levels         | Status |
| ------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------- | ------ |
| [Java Concurrency - Foundations](../java-concurrency/Java%20Concurrency%20-%20Foundations.md)                                               | 21       | L0 + L1        | stub   |
| [Java Concurrency - Locks and Coordination](../java-concurrency/Java%20Concurrency%20-%20Locks%20and%20Coordination.md)                     | 18       | L2             | stub   |
| [Java Concurrency - Async and Patterns](../java-concurrency/Java%20Concurrency%20-%20Async%20and%20Patterns.md)                             | 20       | L3             | stub   |
| [Java Concurrency - Virtual Threads and Diagnostics](../java-concurrency/Java%20Concurrency%20-%20Virtual%20Threads%20and%20Diagnostics.md) | 16       | L4             | stub   |
| [Java Concurrency - Architecture and META](../java-concurrency/Java%20Concurrency%20-%20Architecture%20and%20META.md)                       | 17       | L5 + L6 + META | stub   |

### Spring Ecosystem (spring/)

| File                                                                                  | Keywords | Levels         | Status |
| ------------------------------------------------------------------------------------- | -------- | -------------- | ------ |
| [Spring - Core and Foundations](../spring/Spring%20-%20Core%20and%20Foundations.md)   | 23       | L0 + L1        | stub   |
| [Spring - Web and Data](../spring/Spring%20-%20Web%20and%20Data.md)                   | 20       | L2             | stub   |
| [Spring - Internals and Design](../spring/Spring%20-%20Internals%20and%20Design.md)   | 26       | L3             | stub   |
| [Spring - Production and Cloud](../spring/Spring%20-%20Production%20and%20Cloud.md)   | 20       | L4             | stub   |
| [Spring - Architecture and META](../spring/Spring%20-%20Architecture%20and%20META.md) | 26       | L5 + L6 + META | stub   |

### SQL (sql/)

| File                                                                               | Keywords | Levels         | Status |
| ---------------------------------------------------------------------------------- | -------- | -------------- | ------ |
| [SQL - Foundations](../sql/SQL%20-%20Foundations.md)                               | 25       | L0 + L1        | stub   |
| [SQL - Working Queries](../sql/SQL%20-%20Working%20Queries.md)                     | 27       | L2             | stub   |
| [SQL - Design and Optimization](../sql/SQL%20-%20Design%20and%20Optimization.md)   | 32       | L3             | stub   |
| [SQL - Production and Internals](../sql/SQL%20-%20Production%20and%20Internals.md) | 28       | L4             | stub   |
| [SQL - Architecture and META](../sql/SQL%20-%20Architecture%20and%20META.md)       | 30       | L5 + L6 + META | stub   |

### Hibernate ORM (hibernate/)

| File                                                                                                     | Keywords | Levels         | Status |
| -------------------------------------------------------------------------------------------------------- | -------- | -------------- | ------ |
| [Hibernate - Foundations](../hibernate/Hibernate%20-%20Foundations.md)                                   | 22       | L0 + L1        | stub   |
| [Hibernate - Mappings and Queries](../hibernate/Hibernate%20-%20Mappings%20and%20Queries.md)             | 21       | L2             | stub   |
| [Hibernate - Performance and Internals](../hibernate/Hibernate%20-%20Performance%20and%20Internals.md)   | 28       | L3             | stub   |
| [Hibernate - Production and Diagnostics](../hibernate/Hibernate%20-%20Production%20and%20Diagnostics.md) | 22       | L4             | stub   |
| [Hibernate - Architecture and META](../hibernate/Hibernate%20-%20Architecture%20and%20META.md)           | 22       | L5 + L6 + META | stub   |

---

## Usage

To generate keywords for a topic, invoke:

```pwsh
pwsh -File learn/_config/generate-keywords.ps1 -Topic Java -FromDictionary "JVM,JLG"
```

Or via Copilot:

```
@learn-generate-keywords target: JLG
```

Both paths apply the v1.0 specification in
`learn/_config/LEARN_KEYWORD_GENERATOR.md` exactly. This is
non-negotiable.
