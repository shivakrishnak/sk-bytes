---
title: Java
layout: default
has_children: true
parent: Bytes
nav_order: 1
permalink: /bytes/java/
---

# Java

Sub-topic files for the Java topic. Each file groups 5+ related
keywords following the 14-section template per keyword. Coverage
spans L0..L6 + META per `bytes/_config/BYTES_KEYWORD_GENERATOR.md`
v1.0.

## Files

| File | Difficulty | Keyword Count | Keywords |
| ---- | ---------- | ------------- | -------- |
| [Java - Basics](Java - Basics.md) | easy | 11 | Java Language Overview, Variables and Data Types, Operators and Control Flow, Classes and Objects, Inheritance, Interfaces, Abstract Classes, Access Modifiers, Static and Final, Enums, Packages and Imports |
| [Java - Collections](Java - Collections.md) | medium | 12 | Collections Framework Overview, ArrayList, LinkedList, HashMap, TreeMap, LinkedHashMap and LinkedHashSet, HashSet, Queue and Deque, PriorityQueue, Iterator and ListIterator, Comparable and Comparator, equals and hashCode Contract |
| [Java - Exceptions and IO](Java - Exceptions and IO.md) | medium | 9 | Exception Hierarchy, Checked vs Unchecked Exceptions, Try-Catch-Finally, Try-with-Resources, Custom Exceptions, File IO Streams, NIO and NIO 2, Serialization, Logging Frameworks |
| [Java - Java 8 Features](Java - Java 8 Features.md) | medium | 8 | Lambda Expressions, Functional Interfaces, Method References, Stream API, Collectors, Optional, Default and Static Methods on Interfaces, DateTime API |
| [Java - Java 11 to 17](Java - Java 11 to 17.md) | medium | 8 | var Local Variable Type Inference, Text Blocks, Switch Expressions, Records, Sealed Classes, Pattern Matching for instanceof, JPMS Modules, HttpClient |
| [Java - Java 21 and Beyond](Java - Java 21 and Beyond.md) | hard | 8 | Virtual Threads, Structured Concurrency, Scoped Values, Pattern Matching for switch, Record Patterns, Sequenced Collections, String Templates, Foreign Function and Memory API |
| [Java - JVM Internals](Java - JVM Internals.md) | hard | 10 | JVM Architecture, JDK vs JRE vs JVM, Bytecode and Class Files, Class Loading and ClassLoaders, Runtime Data Areas, Stack vs Heap Memory, Metaspace, JIT Compilation, Escape Analysis, GraalVM and Native Image |
| [Java - Garbage Collection](Java - Garbage Collection.md) | hard | 9 | GC Fundamentals, GC Roots and Reachability, Generational Hypothesis, Serial and Parallel GC, G1 GC, ZGC, Shenandoah GC, Reference Types, GC Tuning and Logs |
| [Java - Diagnostics and Security](Java - Diagnostics and Security.md) | hard | 7 | Java Flight Recorder, Thread Dumps, Heap Dumps and Analysis, JVM Performance Tuning, GC Selection Framework, Java Security Manager, Java Version Migration |

## Spec

- Content spec: `bytes/_config/BYTES_PROMPT.md` v1.0
- Keyword spec: `bytes/_config/BYTES_KEYWORD_GENERATOR.md` v1.0
- Validator: `bytes/_config/validate-byte.py`