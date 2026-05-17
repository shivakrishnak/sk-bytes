---
title: "Java - Language Core"
topic: Java Language
subtopic: Language Core
layout: default
parent: Java Language
grand_parent: "Learn"
nav_order: 1
permalink: /learn/java/language-core/
category: Java Language
code: JLG
folder: learn/java/
difficulty_range: easy
status: in-progress
version: 1
generated_from: LEARN_KEYWORD_GENERATOR.md v1.0
archetype: LANGUAGE
mode: MODE_NEW
provenance: "user request via /learn: add java - java language"
keywords:
  - JLG-001 What Is Java - Orientation
  - JLG-002 The JVM Ecosystem - Where Java Fits
  - JLG-003 Java Editions and Distributions
  - JLG-004 Installing the JDK - First Run
  - JLG-005 Primitive Types and Wrappers
  - JLG-006 Variables, Statements, Expressions
  - JLG-007 Control Flow Constructs
  - JLG-008 Classes, Methods, Fields
  - JLG-009 Constructors and Object Lifecycle
  - JLG-010 Inheritance, Interfaces, Polymorphism
  - JLG-011 Packages and Visibility Modifiers
  - JLG-012 String Concatenation in Loop Anti-Pattern
  - JLG-013 Java Is Not Slow - Killing the Performance Myth
  - JLG-014 Inventory CLI - Phase 1 (Java Basics)
  - JLG-015 Top 10 Java Interview Questions - Basics
---

## Keywords

1. [JLG-001 What Is Java - Orientation](#jlg-001-what-is-java---orientation)
2. [JLG-002 The JVM Ecosystem - Where Java Fits](#jlg-002-the-jvm-ecosystem---where-java-fits)
3. [JLG-003 Java Editions and Distributions](#jlg-003-java-editions-and-distributions)
4. [JLG-004 Installing the JDK - First Run](#jlg-004-installing-the-jdk---first-run)
5. [JLG-005 Primitive Types and Wrappers](#jlg-005-primitive-types-and-wrappers)
6. [JLG-006 Variables, Statements, Expressions](#jlg-006-variables-statements-expressions)
7. [JLG-007 Control Flow Constructs](#jlg-007-control-flow-constructs)
8. [JLG-008 Classes, Methods, Fields](#jlg-008-classes-methods-fields)
9. [JLG-009 Constructors and Object Lifecycle](#jlg-009-constructors-and-object-lifecycle)
10. [JLG-010 Inheritance, Interfaces, Polymorphism](#jlg-010-inheritance-interfaces-polymorphism)
11. [JLG-011 Packages and Visibility Modifiers](#jlg-011-packages-and-visibility-modifiers)
12. [JLG-012 String Concatenation in Loop Anti-Pattern](#jlg-012-string-concatenation-in-loop-anti-pattern)
13. [JLG-013 Java Is Not Slow - Killing the Performance Myth](#jlg-013-java-is-not-slow---killing-the-performance-myth)
14. [JLG-014 Inventory CLI - Phase 1 (Java Basics)](#jlg-014-inventory-cli---phase-1-java-basics)
15. [JLG-015 Top 10 Java Interview Questions - Basics](#jlg-015-top-10-java-interview-questions---basics)

---

# JLG-001 What Is Java - Orientation

**TL;DR** - Java is a statically typed, compiled-to-bytecode language that runs on any platform via the JVM.

---

### 🟢 What it is

**Java** is a general-purpose, object-oriented programming
language created by James Gosling at Sun Microsystems (1995).
Source code compiles to platform-independent bytecode executed
by the Java Virtual Machine (JVM).

---

### 🎯 Why it exists

Before Java, writing cross-platform software meant recompiling
for every target OS. C and C++ programs crashed differently on
Windows, Solaris, and Linux. Enterprises needed one binary that
ran everywhere without rewriting. Applets aside, the real draw
was "write once, run anywhere" for server-side systems. This is
exactly why Java exists.

---

### 🧠 Mental Model

> Java is like a recipe written in a universal cookbook format.
> Any chef (JVM) in any kitchen (OS) can follow it without
> translation.

**Memory hook:** Source -> bytecode -> any JVM -> runs.

---

### ⚙️ How it works

1. You write `.java` source files in a text editor or IDE.
2. `javac` compiles source into `.class` files (bytecode).
3. The JVM loads `.class` files, verifies bytecode safety,
   and interprets or JIT-compiles them to native code.
4. The program runs identically on any OS with a JVM.

---

### ✏️ Minimal Example

**BAD:**

```c
// C - platform-specific compilation
// gcc -o app app.c  (Linux binary)
// cl app.c          (Windows binary)
// Two binaries for two platforms
```

Why it's wrong: each OS needs its own build.

**GOOD:**

```java
// Java - one compilation, any platform
// javac App.java -> App.class
// java App       (runs on any JVM)
public class App {
    public static void main(String[] args) {
        System.out.println("Hello, JVM");
    }
}
```

Why it's right: one `.class` file runs everywhere.

---

### ⚡ When to use / Not to use

**Use when:**

- Building long-lived server applications that must run
  on multiple operating systems.
- You need a mature ecosystem with strong tooling and
  libraries.

**Avoid when:**

- Writing OS kernel code or hardware drivers (use C/Rust).
- Building a quick script or prototype (use Python).

---

### ⚠️ One Gotcha

**Misconception:** Java is only for enterprise bloatware.
**Reality:** Java powers Android apps, Apache Kafka,
Elasticsearch, Minecraft, and most big-data tooling.
The language itself is lean; frameworks add the weight.

---

### 📇 Revision Card

1. Java compiles to bytecode, not native - the JVM is the
   platform.
2. "Write once, run anywhere" is the core value proposition.
3. Java is not slow - the JIT compiler optimizes hot paths
   to near-native speed.

---

---

# JLG-002 The JVM Ecosystem - Where Java Fits

**TL;DR** - The JVM runs Java, Kotlin, Scala, and Clojure - it is a platform, not just a runtime.

---

### 🟢 What it is

The **JVM ecosystem** is the collection of languages,
frameworks, build tools, and libraries that target the Java
Virtual Machine. Java is the primary language, but Kotlin,
Scala, Groovy, and Clojure also compile to JVM bytecode.

---

### 🎯 Why it exists

No language can be perfect for every task. Developers wanted
functional programming (Scala), null-safe conciseness (Kotlin),
or Lisp-style metaprogramming (Clojure) while keeping access to
the massive Java library ecosystem. The JVM specification is
language-agnostic by design - any language that emits valid
bytecode can ride the JVM's garbage collector, JIT compiler, and
threading model. This is exactly why the JVM ecosystem exists.

---

### 🧠 Mental Model

> The JVM is an airport. Java, Kotlin, and Scala are different
> airlines. They all use the same runways (bytecode), terminals
> (class libraries), and air traffic control (GC, JIT).

**Memory hook:** Many languages, one runtime, shared libraries.

---

### ⚙️ How it works

1. Each JVM language has its own compiler (javac, kotlinc,
   scalac) that emits `.class` files.
2. All `.class` files contain the same bytecode format
   defined by the JVM Specification.
3. At runtime, the JVM loads classes regardless of source
   language - a Kotlin class can call a Java library and
   vice versa.

---

### ✏️ Minimal Example

**BAD:**

```text
// Thinking JVM = Java only
"We can't use that library, it's written in Kotlin"
// Wrong - Kotlin .class files are JVM bytecode
```

Why it's wrong: JVM bytecode is language-neutral.

**GOOD:**

```kotlin
// Kotlin calling a Java standard library class
import java.time.LocalDate
fun main() {
    val today = LocalDate.now()
    println("Today: $today")
}
```

Why it's right: Kotlin uses java.time seamlessly because
both run on the JVM.

---

### ⚡ When to use / Not to use

**Use when:**

- You want to mix languages within one project (Java
  services calling Kotlin libraries).
- You need mature, battle-tested runtime infrastructure
  (GC, JIT, monitoring via JFR/JMX).

**Avoid when:**

- Targeting WebAssembly or bare-metal embedded systems.
- Startup latency under 50ms is critical (consider
  GraalVM native-image or Go).

---

### ⚠️ One Gotcha

**Misconception:** Kotlin will replace Java on the JVM.
**Reality:** Kotlin is popular for Android and new backend
services, but the JVM specification evolves with Java as
its reference language. Both coexist by design.

---

### 📇 Revision Card

1. The JVM is a platform - Java is just one of many
   languages that target it.
2. All JVM languages share the same bytecode, GC, JIT,
   and class library ecosystem.
3. Cross-language interop is nearly seamless because
   bytecode is the common contract.

---

---

# JLG-003 Java Editions and Distributions

**TL;DR** - Java SE is the core platform; distributions like Temurin and Corretto deliver the JDK.

---

### 🟢 What it is

**Java editions** define scope: SE (Standard Edition) for
general-purpose development, EE (Enterprise Edition, now
Jakarta EE) for server-side APIs, and ME (Micro Edition)
for embedded devices. **Distributions** are packaged JDK
builds from vendors like Eclipse Temurin, Amazon Corretto,
and Oracle JDK.

---

### 🎯 Why it exists

Oracle open-sourced the JDK under OpenJDK, but "OpenJDK" is
a source project, not a downloadable installer. Enterprises
need tested, signed binaries with predictable update schedules
and optional commercial support. Multiple vendors now ship
their own OpenJDK builds with different support windows. This
is exactly why distributions exist.

---

### 🧠 Mental Model

> Java SE is the recipe. OpenJDK is the open-source recipe
> book. Temurin, Corretto, and Oracle JDK are different
> bakeries all baking the same recipe - slightly different
> packaging, same cake.

**Memory hook:** One spec, many vendors, same bytecode.

---

### ⚙️ How it works

1. The JCP (Java Community Process) publishes a Java SE
   specification for each major version.
2. OpenJDK implements that specification as open-source
   code.
3. Vendors (Eclipse, Amazon, Azul, Oracle) build, test,
   and ship their own binaries from the OpenJDK source.
4. You pick a distribution based on support policy, update
   cadence, and licensing.

---

### ✏️ Minimal Example

**BAD:**

```text
# Downloading "Java" without knowing the source
# Ends up with Oracle JDK and a commercial license
wget oracle.com/java/jdk-21.tar.gz
```

Why it's wrong: Oracle JDK has specific license terms
that may require a commercial subscription.

**GOOD:**

```text
# Explicit choice: Eclipse Temurin (free, TCK-tested)
# sdkman manages multiple JDK distributions
sdk install java 21.0.3-tem
java -version
```

Why it's right: deliberate vendor choice with known
license terms.

---

### ⚡ When to use / Not to use

**Use when:**

- Setting up a new project or CI pipeline - always choose
  the distribution explicitly.
- You need LTS support (Java 21, 17, 11 are LTS releases).

**Avoid when:**

- Evaluating language features only - any distribution
  of the same version behaves identically.
- You are already locked into a vendor-provided JDK
  through your cloud platform.

---

### ⚠️ One Gotcha

**Misconception:** All JDK downloads are free forever.
**Reality:** Oracle JDK changed its license multiple times
(2018, 2021, 2023). Always verify the license of the
distribution you download. Temurin and Corretto are free
under open-source licenses.

---

### 📇 Revision Card

1. Java SE is the specification; OpenJDK is the reference
   implementation; distributions are the installable builds.
2. Pick LTS versions (21, 17, 11) for production stability.
3. Always verify your JDK distribution's license terms
   before deploying to production.

---

---

# JLG-004 Installing the JDK - First Run

**TL;DR** - Install a JDK distribution, set JAVA_HOME, and run javac plus java to verify.

---

### 🟢 What it is

**Installing the JDK** means downloading a distribution
(typically Eclipse Temurin), setting the `JAVA_HOME`
environment variable, adding `$JAVA_HOME/bin` to your
`PATH`, and verifying with `java -version`.

---

### 🎯 Why it exists

You cannot compile or run Java without a JDK. The JDK
contains `javac` (compiler), `java` (launcher), and the
standard library. A JRE (Java Runtime Environment) runs
programs but cannot compile them. Modern JDK distributions
bundle both. New developers often download the wrong
package or forget to set `JAVA_HOME`, causing cryptic
"command not found" errors. This is exactly why a
deliberate install step matters.

---

### 🧠 Mental Model

> Installing the JDK is like setting up a workbench.
> `JAVA_HOME` is the label on the bench so every tool
> (Maven, Gradle, your IDE) knows where to find it.

**Memory hook:** No JAVA_HOME, no build.

---

### ⚙️ How it works

1. Download a JDK distribution (e.g., Temurin 21 LTS).
2. Extract or install to a known path.
3. Set `JAVA_HOME` to point to that path.
4. Add `$JAVA_HOME/bin` to your system `PATH`.
5. Verify: `java -version` and `javac -version`.

---

### ✏️ Minimal Example

**BAD:**

```bash
# Installing without setting JAVA_HOME
sudo apt install openjdk-21-jdk
mvn compile
# ERROR: JAVA_HOME is not set
```

Why it's wrong: build tools need `JAVA_HOME` explicitly.

**GOOD:**

```bash
# Using SDKMAN for managed install
sdk install java 21.0.3-tem
# SDKMAN sets JAVA_HOME automatically
java -version
# openjdk version "21.0.3" ...
javac -version
# javac 21.0.3
```

Why it's right: one command handles install, PATH, and
JAVA_HOME.

---

### ⚡ When to use / Not to use

**Use when:**

- Starting any Java project from scratch.
- Setting up CI pipelines - pin the exact JDK version.

**Avoid when:**

- Your IDE or container image already bundles a JDK
  (verify with `java -version` first).
- You only need to run a pre-built JAR and already
  have a compatible JRE.

---

### ⚠️ One Gotcha

**Misconception:** Any JDK version will work for any project.
**Reality:** Source-level features depend on the compiler
version. A project using records (Java 16+) will not
compile on JDK 11. Always match JDK version to the
project's `sourceCompatibility`.

---

### 📇 Revision Card

1. Install a specific JDK distribution and version - never
   just "Java".
2. JAVA_HOME must point to the JDK root directory.
3. Pin JDK versions in CI - drift between dev and CI causes
   subtle compilation failures.

---

---

# JLG-005 Primitive Types and Wrappers

**TL;DR** - Java has eight primitives stored on the stack; their wrapper classes enable nullability and generics.

---

### 🟢 What it is

**Primitive types** are Java's eight built-in value types:
`byte`, `short`, `int`, `long`, `float`, `double`, `char`,
and `boolean`. Each has a corresponding **wrapper class**
(`Integer`, `Long`, etc.) that is a heap-allocated object.

---

### 🎯 Why it exists

Generics in Java only work with reference types - you cannot
write `List<int>`. Wrapper classes bridge this gap by boxing
primitives into objects. But boxing has a cost: heap allocation,
GC pressure, and cache misses. Understanding when autoboxing
happens silently is critical to avoiding performance traps in
tight loops. This is exactly why primitives and wrappers exist
as separate concepts.

---

### 🧠 Mental Model

> A primitive is a coin in your pocket - fast to grab, fixed
> size. A wrapper is that same coin in a labeled display case -
> visible to collectors (generics), but heavier to carry.

**Memory hook:** Primitive = value on stack. Wrapper = object
on heap.

---

### ⚙️ How it works

1. Declare a primitive: `int count = 42;` - stored directly
   in the stack frame (or as a field in an object).
2. Autoboxing converts primitive to wrapper automatically:
   `Integer boxed = count;`
3. Unboxing converts wrapper back: `int raw = boxed;`
4. Wrappers can be `null`; primitives cannot.

---

### ✏️ Minimal Example

**BAD:**

```java
// Autoboxing in a tight loop - hidden allocation
Long sum = 0L;
for (int i = 0; i < 1_000_000; i++) {
    sum += i; // creates a new Long each iteration
}
```

Why it's wrong: autoboxing creates ~1M objects; GC
pressure and ~5x slower than primitive `long`.

**GOOD:**

```java
// Use primitive in hot loops
long sum = 0L;
for (int i = 0; i < 1_000_000; i++) {
    sum += i; // no boxing, stack-only
}
```

Why it's right: zero allocations in the loop.

---

### ⚡ When to use / Not to use

**Use when:**

- Performance-critical loops and math: always primitives.
- Collections and generics: wrappers are required
  (`List<Integer>`, not `List<int>`).

**Avoid when:**

- Using wrappers where primitives suffice - unnecessary
  heap allocations.
- Comparing wrappers with `==` instead of `.equals()`
  (identity vs equality trap).

---

### ⚠️ One Gotcha

**Misconception:** `Integer a == Integer b` compares values.
**Reality:** `==` on wrappers compares object identity.
`Integer.valueOf(127) == Integer.valueOf(127)` is `true`
(cached), but `Integer.valueOf(128) == Integer.valueOf(128)`
is `false`. Always use `.equals()`.

---

### 📇 Revision Card

1. Eight primitives live on the stack; wrappers live on
   the heap.
2. Autoboxing is invisible but not free - watch tight loops.
3. Never compare wrappers with == (identity trap above 127).

---

---

# JLG-006 Variables, Statements, Expressions

**TL;DR** - Variables hold typed values; expressions produce values; statements perform actions.

---

### 🟢 What it is

A **variable** is a named storage location with a declared
type. An **expression** evaluates to a value (`2 + 3`, method
calls). A **statement** is a complete instruction that performs
an action (`int x = 5;`, `if (...) { ... }`).

---

### 🎯 Why it exists

Java is statically typed. Every variable must declare its type
before use, and the compiler enforces type safety at compile
time. This catches entire categories of bugs (passing a String
where an int is expected) before the program ever runs. Without
this distinction, the compiler cannot verify correctness. This
is exactly why Java separates declarations, expressions, and
statements explicitly.

---

### 🧠 Mental Model

> A variable is a labeled jar. The label says what can go in
> (type). An expression is the act of measuring ingredients.
> A statement is a complete recipe step: "pour 200ml into jar."

**Memory hook:** Declaration = type + name. Expression = value.
Statement = action.

---

### ⚙️ How it works

1. **Declaration:** `int count;` - allocates space of type
   `int` named `count`.
2. **Initialization:** `count = 0;` - assigns a value.
3. **Expression evaluation:** `count + 1` produces a value
   but does not store it.
4. **Statement execution:** `count = count + 1;` evaluates
   the expression and stores the result.

---

### ✏️ Minimal Example

**BAD:**

```java
// Using a variable before initialization
int total;
System.out.println(total); // compile error
```

Why it's wrong: local variables must be initialized before
use in Java.

**GOOD:**

```java
int total = 0;
total = total + 5; // statement with expression
System.out.println(total); // prints 5
```

Why it's right: variable is declared, initialized, then used.

---

### ⚡ When to use / Not to use

**Use when:**

- Declaring variables as close to first use as possible
  for readability.
- Using `final` for variables that should not change
  after initialization.

**Avoid when:**

- Declaring all variables at the top of a method (C-style)
  - reduces readability.
- Reusing a variable for different purposes within the
  same scope - confuses readers.

---

### ⚠️ One Gotcha

**Misconception:** `final` means the object is immutable.
**Reality:** `final` only prevents reassignment of the
variable. A `final List<String>` can still have elements
added or removed. The reference is fixed; the object is not.

---

### 📇 Revision Card

1. Java is statically typed - every variable declares its
   type at compile time.
2. Local variables must be explicitly initialized before use.
3. `final` prevents reassignment, not mutation of the object.

---

---

# JLG-007 Control Flow Constructs

**TL;DR** - if/else, switch, for, while, and do-while direct the execution path through a Java program.

---

### 🟢 What it is

**Control flow constructs** are language statements that
determine which code runs and how many times. Java provides
conditional branching (`if`, `switch`), bounded loops (`for`,
enhanced for-each), and condition-checked loops (`while`,
`do-while`).

---

### 🎯 Why it exists

Without control flow, programs execute linearly from top to
bottom. Real programs need decisions ("if balance < 0, reject")
and repetition ("process each order in the queue"). Every
algorithm is built from sequencing, selection, and iteration.
This is exactly why control flow constructs exist.

---

### 🧠 Mental Model

> Control flow is a railroad switch. The train (execution)
> follows one track until it hits a junction. The switch
> condition decides which track to take.

**Memory hook:** if = junction, for = loop track, break = exit
ramp.

---

### ⚙️ How it works

1. **if/else:** evaluates a boolean expression; executes one
   branch.
2. **switch:** matches a value against cases; falls through
   unless `break` or arrow syntax is used.
3. **for:** initializes a counter, checks a condition each
   iteration, increments after each pass.
4. **enhanced for-each:** iterates over arrays or Iterables
   without an explicit index.
5. **while/do-while:** repeats while a condition holds;
   `do-while` guarantees at least one execution.

---

### ✏️ Minimal Example

**BAD:**

```java
// Missing break causes fall-through
switch (day) {
    case "MON": System.out.println("Monday");
    case "TUE": System.out.println("Tuesday");
    // Both print if day == "MON"
}
```

Why it's wrong: fall-through is almost never intentional.

**GOOD:**

```java
// Arrow syntax (Java 14+) prevents fall-through
switch (day) {
    case "MON" -> System.out.println("Monday");
    case "TUE" -> System.out.println("Tuesday");
    default    -> System.out.println("Other");
}
```

Why it's right: arrow cases do not fall through.

---

### ⚡ When to use / Not to use

**Use when:**

- Using enhanced for-each for all Iterable traversals
  (cleaner, no off-by-one risk).
- Using switch expressions (Java 14+) when mapping a
  value to a result.

**Avoid when:**

- Nesting more than 2-3 levels of if/else - extract to
  methods or use early returns.
- Using a loop index only to access elements sequentially
  (use for-each instead).

---

### ⚠️ One Gotcha

**Misconception:** `for (int i = 0; i <= list.size(); ...)`
is correct.
**Reality:** Using `<=` instead of `<` causes
`IndexOutOfBoundsException` on the last iteration. This
off-by-one error is the most common loop bug in Java.

---

### 📇 Revision Card

1. Arrow-case switch (Java 14+) eliminates fall-through bugs.
2. Prefer enhanced for-each over indexed for when you only
   need elements.
3. Off-by-one: use `< size()`, never `<= size()`.

---

---

# JLG-008 Classes, Methods, Fields

**TL;DR** - A class defines a blueprint; fields hold state; methods define behavior.

---

### 🟢 What it is

A **class** is a template for creating objects. **Fields** are
variables declared in the class body that hold per-object state.
**Methods** are functions defined inside the class that operate
on that state.

---

### 🎯 Why it exists

Procedural code scatters data and functions across unrelated
files. When a system grows, tracking which function modifies
which global variable becomes impossible. Classes bundle related
data (fields) with the operations that act on that data
(methods), giving each concept a single home. This is exactly
why classes exist.

---

### 🧠 Mental Model

> A class is a cookie cutter. Fields are the shape properties
> (size, flavor). Methods are the actions (bake, frost). Each
> cookie (object) has its own field values but shares the same
> methods.

**Memory hook:** Class = blueprint. Object = instance built
from the blueprint.

---

### ⚙️ How it works

1. Define a class with fields and methods.
2. Create an instance with `new ClassName()`.
3. The JVM allocates heap memory for the object's fields.
4. Call methods on the instance: `obj.methodName()`.
5. The garbage collector reclaims memory when no references
   remain.

---

### ✏️ Minimal Example

**BAD:**

```java
// Public fields - no encapsulation
class Account {
    public double balance;
}
// Anyone can set balance to -9999
```

Why it's wrong: no validation, no control over state
changes.

**GOOD:**

```java
class Account {
    private double balance;
    public void deposit(double amount) {
        if (amount <= 0) throw
            new IllegalArgumentException("positive");
        balance += amount;
    }
    public double getBalance() { return balance; }
}
```

Why it's right: state is protected; changes go through
validated methods.

---

### ⚡ When to use / Not to use

**Use when:**

- Modeling a concept with both state and behavior.
- You need encapsulation to protect invariants.

**Avoid when:**

- The concept is pure data with no behavior - consider a
  `record` (Java 16+) instead.
- A static utility method with no state suffices - do not
  create a class just for namespacing.

---

### ⚠️ One Gotcha

**Misconception:** More classes always means better design.
**Reality:** Over-abstraction creates "class explosion" -
dozens of tiny classes with one method each. A class should
represent a coherent concept, not a single function.

---

### 📇 Revision Card

1. Fields hold state; methods define behavior; classes
   bundle both.
2. Make fields private and expose behavior through methods.
3. Prefer records for pure data carriers (Java 16+).

---

---

# JLG-009 Constructors and Object Lifecycle

**TL;DR** - Constructors initialize objects at creation time; the garbage collector reclaims them when unreachable.

---

### 🟢 What it is

A **constructor** is a special method called when `new` creates
an object. It has the same name as the class, no return type,
and sets the object's initial state. The **object lifecycle** is
creation (constructor), use (method calls), and destruction
(garbage collection when no references remain).

---

### 🎯 Why it exists

An object in an invalid state causes bugs downstream. If you
create an `Account` without initializing the owner name, every
method that reads the name gets `null`. Constructors enforce
that objects are born valid by requiring initial values upfront.
This is exactly why constructors exist.

---

### 🧠 Mental Model

> A constructor is the hospital birth room. Every object must
> pass through it exactly once, and it leaves with its identity
> bracelet (required fields) attached. No object escapes
> without initialization.

**Memory hook:** new = allocate + construct. No new = no object.

---

### ⚙️ How it works

1. `new Account("Alice")` allocates heap memory.
2. The JVM calls the matching constructor.
3. The constructor sets field values and may validate
   arguments.
4. The fully initialized object reference is returned.
5. When no variable holds a reference to the object, the
   GC eventually reclaims it.

---

### ✏️ Minimal Example

**BAD:**

```java
class User {
    String name;
    // No constructor - name is null by default
}
User u = new User();
u.name.length(); // NullPointerException
```

Why it's wrong: the object was born in an invalid state.

**GOOD:**

```java
class User {
    private final String name;
    User(String name) {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException();
        this.name = name;
    }
    String getName() { return name; }
}
User u = new User("Alice"); // always valid
```

Why it's right: the constructor guarantees a valid name.

---

### ⚡ When to use / Not to use

**Use when:**

- Enforcing required fields at object creation.
- Making fields `final` so the object is immutable
  after construction.

**Avoid when:**

- The class has many optional parameters - use a builder
  pattern instead of a constructor with 10 arguments.
- You need a static factory method for caching or
  returning subtypes.

---

### ⚠️ One Gotcha

**Misconception:** `finalize()` is where you clean up resources.
**Reality:** `finalize()` is deprecated since Java 9 and
removed in later versions. Use try-with-resources and
`AutoCloseable` for deterministic cleanup.

---

### 📇 Revision Card

1. Constructors guarantee objects are born in a valid state.
2. Prefer `final` fields set in the constructor for
   immutability.
3. Never rely on `finalize()` - use try-with-resources.

---

---

# JLG-010 Inheritance, Interfaces, Polymorphism

**TL;DR** - Inheritance shares behavior via extends; interfaces define contracts; polymorphism lets one reference hold many types.

---

### 🟢 What it is

**Inheritance** lets a subclass extend a parent class, reusing
its fields and methods. An **interface** defines a contract
(method signatures) without implementation. **Polymorphism**
means a variable of type `Animal` can hold a `Dog` or `Cat`
and call the correct overridden method at runtime.

---

### 🎯 Why it exists

Without polymorphism, every new type requires rewriting the
calling code with if/else chains: "if Dog, bark; if Cat, meow."
Adding a new animal means editing every caller. Polymorphism
inverts this: callers program to the `Animal` interface, and
each subtype provides its own behavior. New types require zero
changes to existing code. This is exactly why inheritance and
interfaces exist.

---

### 🧠 Mental Model

> A USB port is an interface. Any device (mouse, keyboard,
> drive) that implements the USB contract plugs in and works.
> The computer does not care which device it is - it calls the
> same methods.

**Memory hook:** Program to the interface, not the
implementation.

---

### ⚙️ How it works

1. Define an interface: `interface Movable { void move(); }`.
2. Implement it: `class Car implements Movable { ... }`.
3. Declare a variable of the interface type: `Movable m;`.
4. Assign any implementation: `m = new Car();`.
5. Call `m.move()` - the JVM dispatches to `Car.move()`
   at runtime (dynamic dispatch via vtable).

---

### ✏️ Minimal Example

**BAD:**

```java
// Type-checking with instanceof chains
void feed(Object animal) {
    if (animal instanceof Dog)
        ((Dog) animal).eatKibble();
    else if (animal instanceof Cat)
        ((Cat) animal).eatFish();
    // Every new animal = another branch
}
```

Why it's wrong: violates the open/closed principle; fragile
to new types.

**GOOD:**

```java
interface Animal { void eat(); }
class Dog implements Animal {
    public void eat() { /* kibble */ }
}
class Cat implements Animal {
    public void eat() { /* fish */ }
}
void feed(Animal a) { a.eat(); }
```

Why it's right: adding `Bird` requires zero changes to
`feed()`.

---

### ⚡ When to use / Not to use

**Use when:**

- Multiple types share a behavioral contract (interface).
- You want callers decoupled from concrete implementations.

**Avoid when:**

- Inheritance is used just to reuse code - prefer
  composition ("has-a" over "is-a").
- Deep inheritance hierarchies (>2-3 levels) make code
  hard to follow.

---

### ⚠️ One Gotcha

**Misconception:** A class can extend multiple classes in Java.
**Reality:** Java supports single class inheritance only. Use
interfaces for multiple contracts. A class can implement many
interfaces but extend at most one class.

---

### 📇 Revision Card

1. Interfaces define contracts; classes provide
   implementations.
2. Polymorphism eliminates if/else type-checking chains.
3. Single inheritance only - prefer composition over deep
   hierarchies.

---

---

# JLG-011 Packages and Visibility Modifiers

**TL;DR** - Packages namespace classes to avoid collisions; access modifiers control who can see what.

---

### 🟢 What it is

A **package** is a namespace that groups related classes
(e.g., `java.util`, `com.acme.billing`). **Visibility
modifiers** (`public`, `protected`, package-private, `private`)
control access to classes, fields, and methods.

---

### 🎯 Why it exists

Without packages, two teams writing a `User` class collide.
Without access control, any code can reach into any class's
internals, making refactoring impossible - changing a field
name breaks unknown callers. Packages give structure; modifiers
enforce encapsulation boundaries. This is exactly why packages
and visibility modifiers exist.

---

### 🧠 Mental Model

> A package is a department in an office building. `private` is
> a locked desk drawer. Package-private is an unlocked drawer
> visible to the department. `protected` adds access for
> sub-departments. `public` is the lobby - open to everyone.

**Memory hook:** private < package-private < protected < public.

---

### ⚙️ How it works

1. Declare a package: `package com.acme.billing;` at the
   top of the file.
2. The directory structure must match: `com/acme/billing/`.
3. Classes without a modifier are package-private (visible
   only within the same package).
4. `public` classes are visible everywhere; `private`
   members are visible only within the declaring class.

---

### ✏️ Minimal Example

**BAD:**

```java
// Exposing internal helper as public
package com.acme.billing;
public class InvoiceHelper {
    public static double calcTax(double amt) {
        return amt * 0.2;
    }
}
// Any package can call InvoiceHelper.calcTax
```

Why it's wrong: an internal helper leaks into the public API.

**GOOD:**

```java
package com.acme.billing;
class InvoiceHelper { // package-private
    static double calcTax(double amt) {
        return amt * 0.2;
    }
}
// Only classes in com.acme.billing can see this
```

Why it's right: encapsulation hides the implementation detail.

---

### ⚡ When to use / Not to use

**Use when:**

- Making every class and member as restrictive as possible
  by default (start private, widen only when needed).
- Organizing code by feature or domain, not by layer.

**Avoid when:**

- Using the default (empty) package - it cannot be imported
  by other packages and breaks in modular Java.
- Making everything `public` "just in case" - this creates
  an unmaintainable public API.

---

### ⚠️ One Gotcha

**Misconception:** `protected` means "only subclasses."
**Reality:** `protected` means subclasses AND any class in
the same package. Package-level access is always included.

---

### 📇 Revision Card

1. Start with the most restrictive access modifier; widen
   only when proven necessary.
2. Package-private (no modifier) is the sensible default for
   internal classes.
3. `protected` includes same-package access - not just
   subclasses.

---

---

# JLG-012 String Concatenation in Loop Anti-Pattern

**TL;DR** - Using += on Strings inside loops creates O(n^2) garbage; use StringBuilder instead.

---

### 🟢 What it is

The **String concatenation in loop anti-pattern** occurs when
code uses `+` or `+=` to build a string inside a loop. Because
Java Strings are immutable, each concatenation allocates a new
String object, copying all previous content.

---

### 🎯 Why it exists

New Java developers write `result += item` inside loops because
it reads naturally. But each iteration creates a new String
copying all prior characters. For n items of average length m,
this is O(n^2 \* m) work and memory. A `StringBuilder` appends
in amortized O(1) per call. This is exactly why the anti-pattern
must be recognized and avoided.

---

### 🧠 Mental Model

> String += in a loop is like rewriting an entire letter by hand
> every time you add one sentence. StringBuilder is a notepad
> where you just keep writing at the end.

**Memory hook:** Immutable String + loop = quadratic copy storm.

---

### ⚙️ How it works

1. `String s = "a"; s += "b";` compiles to creating a new
   String "ab" (the old "a" becomes garbage).
2. Inside a loop with 10,000 iterations, this creates
   10,000 intermediate String objects.
3. `StringBuilder` maintains an internal `char[]` buffer
   and doubles its capacity when full (amortized O(1)).
4. Call `sb.toString()` once at the end.

---

### ✏️ Minimal Example

**BAD:**

```java
String csv = "";
for (String name : names) {
    csv += name + ","; // new String each iteration
}
// O(n^2) allocations for n names
```

Why it's wrong: quadratic time and memory; GC pressure
grows with each iteration.

**GOOD:**

```java
StringBuilder sb = new StringBuilder();
for (String name : names) {
    sb.append(name).append(',');
}
String csv = sb.toString(); // one final allocation
```

Why it's right: linear time, one allocation at the end.

---

### ⚡ When to use / Not to use

**Use when:**

- Building strings in any loop or recursive method.
- Concatenating more than 3-4 values dynamically.

**Avoid when:**

- Concatenating a fixed number of literals - the compiler
  optimizes `"a" + "b" + "c"` at compile time.
- Using `String.join()` or `Collectors.joining()` which
  handle the builder internally.

---

### ⚠️ One Gotcha

**Misconception:** The compiler always optimizes `+=` into
StringBuilder.
**Reality:** The compiler optimizes single-expression
concatenation but typically cannot optimize `+=` across loop
iterations. Each iteration still creates intermediary objects.

---

### 📇 Revision Card

1. String is immutable - every `+=` allocates a new object.
2. Use `StringBuilder` for any loop-based string building.
3. For joining collections, `String.join()` or
   `Collectors.joining()` is even cleaner.

---

---

# JLG-013 Java Is Not Slow - Killing the Performance Myth

**TL;DR** - The JIT compiler optimizes hot bytecode to native code, making Java competitive with C++ for server workloads.

---

### 🟢 What it is

The myth that **Java is slow** persists from the 1990s when
Java ran as a pure interpreter. Modern Java uses Just-In-Time
(JIT) compilation: the HotSpot JVM profiles running bytecode
and compiles frequently executed paths ("hot spots") to
optimized native machine code at runtime.

---

### 🎯 Why it exists

Early Java (1.0-1.2) was genuinely slow - bytecode was
interpreted line by line. Applets felt sluggish. The reputation
stuck. But HotSpot (introduced in Java 1.3, 2000) changed
everything. Today, long-running server applications see JIT
optimizations (inlining, escape analysis, loop unrolling) that
sometimes outperform static compilers because the JIT has
runtime profile data. This myth must die because it causes
teams to reject Java for workloads it excels at.

---

### 🧠 Mental Model

> Java starts as a tourist reading a phrasebook (interpreter).
> After visiting the same cafe 100 times, it speaks fluent
> local (JIT-compiled native code). C++ starts fluent but
> never learns the waiter's shortcuts.

**Memory hook:** JIT = the more you run it, the faster it gets.

---

### ⚙️ How it works

1. The JVM starts interpreting bytecode.
2. The profiler counts method invocations and loop
   iterations.
3. When a threshold is reached, the C1 compiler produces
   fast but unoptimized native code.
4. For very hot methods, the C2 compiler applies aggressive
   optimizations (inlining, devirtualization, escape
   analysis).
5. The result: server-side Java throughput is typically
   within 5-20% of equivalent C++ for sustained workloads.

---

### ✏️ Minimal Example

**BAD:**

```text
"Java is interpreted, so it's always slower than C."
// This was true in 1996. It has been false for 20+ years.
```

Why it's wrong: ignores JIT compilation entirely.

**GOOD:**

```bash
# Observing JIT compilation at runtime
java -XX:+PrintCompilation -jar app.jar
#  42  1  b  com.acme.Service::process (hot)
# The "b" flag means compiled to native code
```

Why it's right: demonstrates that Java compiles hot methods
to native code at runtime.

---

### ⚡ When to use / Not to use

**Use when:**

- Long-running server workloads where JIT has time to
  optimize (web servers, message processors).
- Throughput matters more than startup time.

**Avoid when:**

- Sub-100ms cold start is required (serverless, CLI tools)
  - consider GraalVM native-image.
- Real-time systems with hard latency guarantees where
  GC pauses are unacceptable.

---

### ⚠️ One Gotcha

**Misconception:** Java's startup time proves it is slow.
**Reality:** Startup includes class loading and JIT warm-up,
not steady-state performance. Benchmarking a 100ms task
measures startup, not throughput. Measure sustained
throughput, not cold-start latency.

---

### 📇 Revision Card

1. JIT compilation turns hot bytecode into optimized native
   code at runtime.
2. Benchmark steady-state throughput, not startup time.
3. For cold-start-sensitive workloads, use GraalVM
   native-image.

---

---

# JLG-014 Inventory CLI - Phase 1 (Java Basics)

**TL;DR** - Build a command-line inventory tracker using classes, loops, and arrays to practice Java basics.

---

### 🟢 What it is

**Inventory CLI Phase 1** is a hands-on practice exercise.
You build a command-line application that stores product names
and quantities, supports add/list/search operations, and runs
in a read-eval-print loop. It uses only L0-L1 concepts: classes,
arrays, loops, conditionals, and basic I/O.

---

### 🎯 Why it exists

Reading about classes and loops does not build skill. Typing
code, hitting errors, and debugging builds muscle memory. This
exercise ties together every L0-L1 concept into a single
coherent program that you can extend in later phases. This is
exactly why practice exercises exist at every level.

---

### 🧠 Mental Model

> Phase 1 is building a bicycle with training wheels. You
> already have the parts (classes, arrays, loops). Now you
> assemble them into something that moves.

**Memory hook:** Theory is input. Code is output. Build to
learn.

---

### ⚙️ How it works

1. Create a `Product` class with `name` (String) and
   `quantity` (int) fields, plus a constructor.
2. Create an `Inventory` class with a `Product[]` array
   and methods: `add(Product)`, `listAll()`, `search(name)`.
3. Create a `Main` class with a `Scanner`-based loop:
   read commands, dispatch to Inventory methods.
4. Handle edge cases: full array, product not found,
   invalid input.
5. Run, test manually, and fix bugs.

---

### ✏️ Minimal Example

**BAD:**

```java
// All logic in main - no classes, no structure
public static void main(String[] args) {
    String[] names = new String[100];
    int[] qtys = new int[100];
    // 200 lines of spaghetti follows
}
```

Why it's wrong: no encapsulation, impossible to extend.

**GOOD:**

```java
class Product {
    private final String name;
    private int quantity;
    Product(String name, int qty) {
        this.name = name;
        this.quantity = qty;
    }
    String getName() { return name; }
    int getQuantity() { return quantity; }
}
```

Why it's right: data and behavior are bundled; each class
has a clear responsibility.

---

### ⚡ When to use / Not to use

**Use when:**

- You have studied L0-L1 concepts and want to integrate
  them.
- You want a project skeleton to extend in later phases.

**Avoid when:**

- You have not yet learned classes and constructors -
  study JLG-008 and JLG-009 first.
- You are already comfortable building CLI applications
  and want a bigger challenge.

---

### ⚠️ One Gotcha

**Misconception:** The exercise is too simple to teach
anything.
**Reality:** Most production bugs come from basics: null
checks, off-by-one loops, missing input validation. A
simple exercise done well builds the habits that prevent
those bugs.

---

### 📇 Revision Card

1. Build the Product class first, then Inventory, then Main.
2. Validate all user input - never trust Scanner output.
3. This skeleton grows into Phase 2 (Collections) and
   Phase 3 (Streams + Records).

---

---

# JLG-015 Top 10 Java Interview Questions - Basics

**TL;DR** - Master these ten foundational questions to survive any Java basics interview screen.

---

### 🟢 What it is

This keyword collects the ten most commonly asked **Java
interview questions** at the basics level. Each question maps
directly to an L0-L1 concept covered elsewhere in this file.
The goal is pattern recognition: know the question shape,
recall the precise answer, deliver it in under 60 seconds.

---

### 🎯 Why it exists

Interview prep scattered across blog posts is inconsistent and
often wrong. This distills the ten questions that appear in
virtually every Java phone screen, linked to the authoritative
concepts from this learn file. Knowing these cold frees mental
bandwidth for harder questions. This is exactly why a curated
recall card exists.

---

### 🧠 Mental Model

> Interview questions are combination locks. Each has a specific
> sequence of concepts. If you know the sequence (key concepts),
> the lock opens instantly.

**Memory hook:** Know the ten locks. Practice the ten sequences.

---

### ⚙️ How it works

1. **"What is the JVM?"** -> JLG-001, JLG-002: bytecode
   runtime, platform independence.
2. **"Primitive vs wrapper?"** -> JLG-005: stack vs heap,
   autoboxing, == vs equals.
3. **"final keyword?"** -> JLG-006: prevents reassignment,
   not mutation.
4. **"== vs .equals()?"** -> JLG-005, JLG-021: identity vs
   value comparison.
5. **"String immutability?"** -> JLG-012: why += in loops is
   quadratic.

---

### ✏️ Minimal Example

**BAD:**

```text
Q: "Is Java pass-by-value or pass-by-reference?"
A: "Java is pass-by-reference for objects."
// WRONG - this fails the interview
```

Why it's wrong: Java is always pass-by-value. For objects,
the value passed is the reference (a copy of the pointer).

**GOOD:**

```text
Q: "Is Java pass-by-value or pass-by-reference?"
A: "Java is always pass-by-value. For objects,
    it passes a copy of the reference. Reassigning
    the parameter inside a method does not affect
    the caller's variable."
```

Why it's right: precise, demonstrates understanding of
the mechanism.

---

### ⚡ When to use / Not to use

**Use when:**

- Preparing for a phone screen or first-round interview.
- You want a quick self-test of foundational knowledge.

**Avoid when:**

- You are preparing for a system design or architecture
  interview - these are basics-level only.
- You are already senior and need L4+ interview prep
  (see JLG-054, JLG-059).

---

### ⚠️ One Gotcha

**Misconception:** Memorizing answers is sufficient.
**Reality:** Interviewers follow up with "why?" and "what
happens if...?" Understanding the underlying mechanism
(from the linked keywords) is what separates a pass from
a fail.

---

### 📇 Revision Card

1. Java is always pass-by-value (references are copied,
   not aliased).
2. == compares identity for objects; .equals() compares
   value.
3. Know the WHY behind each answer - interviewers probe
   beyond the surface.
