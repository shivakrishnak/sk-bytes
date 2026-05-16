---
title: Learn
layout: default
nav_order: 2
has_children: true
permalink: /learn/
---

# Learn

Multi-keyword study files grouped by topic. Each keyword is
routed to one of three templates (SIMPLE / INTERMEDIATE /
COMPLEX) based on its level. Word targets:

| Tier         | Sections | Words       |
| ------------ | -------- | ----------- |
| SIMPLE       | 9        | 400-700     |
| INTERMEDIATE | 13       | 900-1,300   |
| COMPLEX      | 16       | 1,400-2,000 |

## How to read

1. Pick a topic from the sidebar.
2. Open the topic's `index.md` for the sub-topic file table.
3. Each INTERMEDIATE / COMPLEX keyword states its `Prereq` and
   `Next` titles in the Learning Ladder section.

## Topics

| Topic                                 | Code | Archetype      | Status                     | Folder                    |
| ------------------------------------- | ---- | -------------- | -------------------------- | ------------------------- |
| [Java Language](java/)                | JLG  | LANGUAGE       | scaffolded (62 kw, stubs)  | `learn/java/`             |
| [Java JVM](java-jvm/)                 | JVM  | INFRASTRUCTURE | scaffolded (132 kw, stubs) | `learn/java-jvm/`         |
| [Java Concurrency](java-concurrency/) | JCC  | CS-CONCEPT     | scaffolded (92 kw, stubs)  | `learn/java-concurrency/` |
| [Spring Ecosystem](spring/)            | SPR  | FRAMEWORK      | scaffolded (115 kw, stubs) | `learn/spring/`           |

## Spec

See [LEARN_PROMPT v1.0](/learn/_config/LEARN_PROMPT/) for the
master generation specification, including the three templates
and the Code Example Taxonomy.

Any topic / sub-topic / keyword list is generated through
[LEARN_KEYWORD_GENERATOR v1.0](/learn/_config/LEARN_KEYWORD_GENERATOR/).
No ad-hoc lists.
