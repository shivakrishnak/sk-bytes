---
title: "Java Concurrency - Foundations"
topic: Java Concurrency
subtopic: Foundations
keywords:
  - Why Concurrency Exists
  - Sequential vs Concurrent vs Parallel
  - The Shared Mutable State Problem
  - Concurrency in the Java Ecosystem
  - Processes vs Threads - The OS View
  - Concurrency vs Parallelism Distinction
  - Thread and Runnable
  - Thread Lifecycle and States
  - synchronized Keyword
  - volatile Keyword
  - wait, notify, notifyAll
  - Thread.sleep vs Object.wait
  - Race Condition
  - Deadlock
  - Atomicity, Visibility, Ordering
  - Thread.start vs Thread.run Anti-Pattern
  - Synchronized Means Slow is Wrong - Lock Reality
  - jstack and Thread Dumps
  - Top 10 Java Concurrency Interview Questions
  - Thread Safety Exercise - Broken Counter
  - Concurrent Chat - Phase 1 (Raw Threads)
difficulty_range: easy
status: draft
version: 1
layout: default
parent: "Java Concurrency"
grand_parent: "Learn"
nav_order: 1
permalink: /learn/java-concurrency/foundations/
---

## Keywords

1. [Why Concurrency Exists](#why-concurrency-exists)
2. [Sequential vs Concurrent vs Parallel](#sequential-vs-concurrent-vs-parallel)
3. [The Shared Mutable State Problem](#the-shared-mutable-state-problem)
4. [Concurrency in the Java Ecosystem](#concurrency-in-the-java-ecosystem)
5. [Processes vs Threads - The OS View](#processes-vs-threads---the-os-view)
6. [Concurrency vs Parallelism Distinction](#concurrency-vs-parallelism-distinction)
7. [Thread and Runnable](#thread-and-runnable)
8. [Thread Lifecycle and States](#thread-lifecycle-and-states)
9. [synchronized Keyword](#synchronized-keyword)
10. [volatile Keyword](#volatile-keyword)
11. [wait, notify, notifyAll](#wait-notify-notifyall)
12. [Thread.sleep vs Object.wait](#threadsleep-vs-objectwait)
13. [Race Condition](#race-condition)
14. [Deadlock](#deadlock)
15. [Atomicity, Visibility, Ordering](#atomicity-visibility-ordering)
16. [Thread.start vs Thread.run Anti-Pattern](#threadstart-vs-threadrun-anti-pattern)
17. [Synchronized Means Slow is Wrong - Lock Reality](#synchronized-means-slow-is-wrong---lock-reality)
18. [jstack and Thread Dumps](#jstack-and-thread-dumps)
19. [Top 10 Java Concurrency Interview Questions](#top-10-java-concurrency-interview-questions)
20. [Thread Safety Exercise - Broken Counter](#thread-safety-exercise---broken-counter)
21. [Concurrent Chat - Phase 1 (Raw Threads)](#concurrent-chat---phase-1-raw-threads)

---

---

# Why Concurrency Exists

**TL;DR** - Concurrency exists because CPUs wait idle during I/O and single cores hit physics limits.

### 🟢 What it is

**Concurrency** is a programming model that allows multiple tasks to make progress within overlapping time periods, even on a single core.

### 🎯 Why it exists

Before concurrency, programs ran sequentially: read from disk, wait 10ms, then process. During that 10ms wait the CPU does nothing - millions of wasted cycles. As clock speeds plateaued around 2005, hardware added cores instead of speed. Sequential code cannot use those cores. This is exactly why concurrency exists.

### 🧠 Mental Model

> A restaurant kitchen with one chef (single core) can still handle multiple orders concurrently - start soup simmering, chop vegetables while it heats, plate another dish while chopping pauses. Not parallel (one chef) but concurrent (overlapping progress).

**Memory hook:** "Concurrency is about DEALING with many things at once; parallelism is about DOING many things at once."

### ⚙️ How it works

1. A task reaches a blocking point (I/O, network, sleep).
2. The scheduler suspends that task and switches to another ready task.
3. When the blocking operation completes, the original task becomes runnable again.
4. The CPU stays busy instead of idling during waits.

### ✏️ Minimal Example

**BAD:**

```java
// Sequential: total time = fetchA + fetchB
String a = fetchFromServiceA(); // 200ms wait
String b = fetchFromServiceB(); // 200ms wait
// Total: 400ms elapsed
```

Why it's wrong: CPU idles 400ms total while waiting for network.

**GOOD:**

```java
// Concurrent: total time = max(fetchA, fetchB)
Future<String> a = executor.submit(
    () -> fetchFromServiceA());
Future<String> b = executor.submit(
    () -> fetchFromServiceB());
String result = a.get() + b.get(); // ~200ms total
```

Why it's right: both fetches overlap; CPU switches between tasks during I/O waits.

### ⚡ When to use / Not to use

**Use when:**
- Tasks spend significant time waiting (I/O-bound work).
- Multiple independent operations can overlap.

**Avoid when:**
- Work is purely CPU-bound AND single-threaded is fast enough.
- Added complexity outweighs the latency gain.

### ⚠️ One Gotcha

**Misconception:** "Concurrency makes code faster."
**Reality:** Concurrency makes code faster ONLY when tasks have idle waits that can overlap. Pure computation on one core gains nothing from concurrency - it adds overhead.

### 📇 Revision Card

1. Concurrency overlaps waits; it does not magically speed up computation.
2. Hardware stopped getting faster (clock speed plateau ~2005) so programs must use multiple cores.
3. The trap: adding concurrency to CPU-bound work adds overhead without speedup.

---

---

# Sequential vs Concurrent vs Parallel

**TL;DR** - Sequential is one task at a time; concurrent is interleaved progress; parallel is simultaneous execution on multiple cores.

### 🟢 What it is

**Sequential**, **concurrent**, and **parallel** are three execution models describing how tasks relate in time: one-after-another, overlapping, or truly simultaneous.

### 🎯 Why it exists

Engineers confuse concurrent and parallel constantly, leading to wrong design choices. If you think "concurrent = parallel," you will assume adding threads always speeds things up. Understanding the distinction prevents wasted effort and broken architectures. This is exactly why this classification exists.

### 🧠 Mental Model

> Sequential: one checkout lane. Concurrent: one cashier juggling multiple customers (scan item, wait for payment, serve next). Parallel: multiple cashiers each serving a customer simultaneously.

**Memory hook:** "Concurrent = structure. Parallel = execution. You can be concurrent on one core, but parallel requires multiple."

### ⚙️ How it works

1. Sequential: task B starts only after task A finishes entirely.
2. Concurrent: tasks A and B alternate execution slices on one core via context switching.
3. Parallel: tasks A and B execute at the exact same instant on different cores.
4. Concurrency is a design choice; parallelism is a runtime capability (requires hardware).

### ✏️ Minimal Example

**BAD:**

```java
// Thinking "concurrent" means "parallel"
// Single-core machine: threads do NOT run simultaneously
Thread t1 = new Thread(cpuWork);
Thread t2 = new Thread(cpuWork);
t1.start(); t2.start();
// On 1 core: SLOWER than sequential (context switch cost)
```

Why it's wrong: on a single core, CPU-bound threads interleave with overhead, not speedup.

**GOOD:**

```java
// Concurrent structure for I/O tasks (works on 1 core)
Thread t1 = new Thread(() -> fetchFromNetwork());
Thread t2 = new Thread(() -> readFromDisk());
t1.start(); t2.start();
// Both block on I/O; one core handles both efficiently
```

Why it's right: concurrency helps I/O-bound tasks regardless of core count because waits overlap.

### ⚡ When to use / Not to use

**Use when:**
- Distinguishing whether your workload benefits from threads (I/O overlap) vs cores (CPU parallelism).
- Designing systems that must run on varying hardware (1 core in container vs 8 cores bare-metal).

**Avoid when:**
- Overcomplicating a single-user script with no blocking.
- The system is already meeting latency requirements sequentially.

### ⚠️ One Gotcha

**Misconception:** "More threads = more parallelism."
**Reality:** Thread count > core count means concurrency (interleaving), not parallelism. 100 threads on 4 cores = 4 parallel, 96 waiting.

### 📇 Revision Card

1. Concurrent = overlapping progress (structure). Parallel = simultaneous (requires hardware).
2. Concurrency helps I/O-bound work on ANY core count; parallelism helps CPU-bound work only with multiple cores.
3. Adding threads beyond core count does not add parallelism - it adds context-switch overhead.

---

---

# The Shared Mutable State Problem

**TL;DR** - When multiple threads read and write the same variable without coordination, results become unpredictable.

### 🟢 What it is

The **shared mutable state problem** is the fundamental difficulty of concurrent programming: two or more threads accessing the same writable data without synchronization, producing corrupted or inconsistent results.

### 🎯 Why it exists

A single counter variable, `count++`, looks atomic but is three CPU operations: read, increment, write. Two threads executing this simultaneously can both read the same value and write back the same incremented value - losing one update entirely. Every multi-threaded bug trace back to some form of this problem. This is exactly why the shared mutable state problem is the first thing you must understand.

### 🧠 Mental Model

> Two people editing the same Google Doc paragraph offline. Both download version 5, both edit, both upload. One person's changes overwrite the other's. The "shared mutable state" is the paragraph; the "threads" are the editors; the "race" is who uploads last.

**Memory hook:** "Shared + Mutable + Concurrent = Bug. Remove any ONE and you are safe."

### ⚙️ How it works

1. Thread A reads variable X (value = 5).
2. Thread B reads variable X (value = 5) - before A writes.
3. Thread A writes X = 6.
4. Thread B writes X = 6 (not 7) - lost update.
5. Final value: 6 instead of expected 7.

### ✏️ Minimal Example

**BAD:**

```java
int count = 0;
// Two threads both doing this 1,000,000 times:
count++; // NOT atomic: read -> increment -> write
// Expected: 2,000,000. Actual: ~1,500,000 (varies!)
```

Why it's wrong: `count++` is three operations; threads interleave between them.

**GOOD:**

```java
AtomicInteger count = new AtomicInteger(0);
// Two threads both doing this 1,000,000 times:
count.incrementAndGet(); // atomic single operation
// Result: exactly 2,000,000 every time
```

Why it's right: AtomicInteger uses hardware CAS to make increment truly atomic.

### ⚡ When to use / Not to use

**Use when:**
- Understanding WHY synchronized/volatile/Atomic classes exist (they solve this).
- Diagnosing flaky tests or production data corruption.

**Avoid when:**
- You can eliminate sharing (thread confinement) or mutability (immutable objects).
- Single-threaded context where no races are possible.

### ⚠️ One Gotcha

**Misconception:** "I only write once, so it is safe."
**Reality:** Even a single write + single read from different threads is unsafe without a happens-before edge. The reading thread may never SEE the write (visibility problem).

### 📇 Revision Card

1. Three conditions cause bugs: shared + mutable + concurrent. Remove any one to be safe.
2. `count++` is NOT atomic - it is read, modify, write (three operations).
3. Visibility is as dangerous as atomicity: writes can be invisible to other threads without happens-before.

---

---

# Concurrency in the Java Ecosystem

**TL;DR** - Java provides threads, synchronization primitives, java.util.concurrent, and virtual threads as a layered concurrency toolkit.

### 🟢 What it is

**Concurrency in the Java ecosystem** is the layered set of APIs and runtime features - from low-level `Thread` and `synchronized` through `java.util.concurrent` (JDK 5+) to virtual threads (JDK 21) - that enable safe multi-threaded programming.

### 🎯 Why it exists

Java was one of the first mainstream languages to include threads in the language specification (1995). As concurrency grew harder, the ecosystem evolved: raw threads were error-prone, so `java.util.concurrent` added structured abstractions (2004). Thread-per-request could not scale to millions of connections, so virtual threads arrived (2023). This is exactly why understanding the ecosystem layers matters.

### 🧠 Mental Model

> Java concurrency is like transportation infrastructure built in layers: first dirt roads (raw threads), then highways with traffic rules (synchronized), then managed transit systems (Executors, j.u.c), then hyperloop (virtual threads). Each layer exists because the previous one could not scale.

**Memory hook:** "JDK 1: threads. JDK 5: java.util.concurrent. JDK 21: virtual threads. Three eras, each 10x simpler."

### ⚙️ How it works

1. Layer 1 (JDK 1.0): Thread, Runnable, synchronized, wait/notify - manual, error-prone.
2. Layer 2 (JDK 5): ExecutorService, Future, ConcurrentHashMap, locks, atomics - structured and safe.
3. Layer 3 (JDK 8): CompletableFuture, parallel streams - composition and declarative parallelism.
4. Layer 4 (JDK 21): Virtual threads, structured concurrency - millions of threads without pool tuning.

### ✏️ Minimal Example

**BAD:**

```java
// Raw threads (JDK 1 style) - manual lifecycle management
Thread t = new Thread(() -> doWork());
t.start();
t.join(); // blocks caller, no timeout, no error handling
```

Why it's wrong: no resource management, no result handling, no thread reuse.

**GOOD:**

```java
// ExecutorService (JDK 5+) - managed lifecycle
try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> f = exec.submit(() -> doWork());
    String result = f.get(5, TimeUnit.SECONDS);
}
```

Why it's right: managed pool, timeout support, automatic cleanup, works with virtual threads.

### ⚡ When to use / Not to use

**Use when:**
- Building any Java application that handles concurrent requests or background tasks.
- Choosing the right abstraction layer for your JDK version.

**Avoid when:**
- A simple single-threaded script suffices.
- Reactive frameworks (Reactor/RxJava) already manage concurrency for you.

### ⚠️ One Gotcha

**Misconception:** "Virtual threads replace everything else."
**Reality:** Virtual threads replace thread-per-request pools but do not replace synchronization. You still need locks/atomics for shared mutable state.

### 📇 Revision Card

1. Three eras: raw threads (JDK 1), java.util.concurrent (JDK 5), virtual threads (JDK 21).
2. Each layer solves the previous layer's scaling problem but does NOT eliminate shared-state coordination.
3. Start with the highest abstraction available for your JDK version.

---

---

# Processes vs Threads - The OS View

**TL;DR** - Processes have isolated memory spaces; threads share memory within a process, making communication fast but synchronization mandatory.

### 🟢 What it is

A **process** is an OS-level execution unit with its own memory space. A **thread** is a lightweight execution unit within a process that shares the process's memory with other threads.

### 🎯 Why it exists

The distinction determines everything about concurrency design. Processes cannot accidentally corrupt each other's data (isolated memory), but communicating between them is expensive (IPC). Threads share memory (fast communication) but can corrupt each other trivially. Choosing wrong means either impossible-to-debug corruption or needless overhead. This is exactly why understanding the OS view matters.

### 🧠 Mental Model

> Processes are separate apartments in a building - each has its own kitchen, bathroom, locks. Threads are roommates in one apartment - they share the kitchen and can trip over each other.

**Memory hook:** "Processes: safe but slow to share. Threads: fast but dangerous to share."

### ⚙️ How it works

1. OS creates a process with its own virtual memory space (heap, stack, code segment).
2. Each process has at least one thread (the main thread).
3. Additional threads share the process's heap but get their own stack.
4. Context switch between processes is expensive (TLB flush, cache invalidation); between threads is cheaper (same address space).

### ✏️ Minimal Example

**BAD:**

```java
// Spawning a process for parallel work within same app
Runtime.getRuntime().exec("java -cp . Worker");
// Separate process: no shared memory, complex IPC needed
// 50-100ms startup, OS resources per process
```

Why it's wrong: process isolation makes data sharing expensive; overkill for in-app parallelism.

**GOOD:**

```java
// Thread shares heap memory - direct, fast communication
Thread worker = new Thread(() -> {
    sharedQueue.add(result); // shared data structure
});
worker.start();
```

Why it's right: threads share memory directly - zero-copy communication within the process.

### ⚡ When to use / Not to use

**Use when:**
- Threads: work needs fast shared data access within one JVM.
- Processes: work needs fault isolation (crash one, others survive).

**Avoid when:**
- Threads: tasks are untrusted (a thread crash kills the JVM).
- Processes: you need nanosecond-level communication latency.

### ⚠️ One Gotcha

**Misconception:** "Threads are always better because they are lighter."
**Reality:** Thread failures crash the entire process. For fault-tolerant systems (microservices), process isolation is a feature not a cost.

### 📇 Revision Card

1. Processes: isolated memory (safe, slow IPC). Threads: shared memory (fast, needs synchronization).
2. Threads share heap but have separate stacks.
3. One bad thread can crash the entire JVM process - isolation has value.

---

---

# Concurrency vs Parallelism Distinction

**TL;DR** - Concurrency is structuring code to handle multiple tasks; parallelism is executing multiple tasks simultaneously on hardware.

### 🟢 What it is

**Concurrency** is a program design that enables dealing with multiple things at once. **Parallelism** is a runtime execution mode where multiple things happen at the same physical instant.

### 🎯 Why it exists

The confusion causes engineers to throw threads at CPU-bound problems expecting speedup on single-core containers, or to avoid concurrency entirely for I/O-bound services that desperately need it. Knowing the distinction lets you make the right design choice for the actual workload. This is exactly why this distinction is taught separately.

### 🧠 Mental Model

> Concurrency: a juggler keeping three balls in the air (one hand, many balls - STRUCTURE). Parallelism: three jugglers each with one ball (many hands, simultaneous - EXECUTION).

**Memory hook:** "Concurrency is about the CODE structure. Parallelism is about the HARDWARE executing."

### ⚙️ How it works

1. Concurrency: program is structured with multiple tasks that can make progress independently.
2. On one core: tasks interleave (concurrent but not parallel).
3. On multiple cores: tasks can run simultaneously (concurrent AND parallel).
4. Parallelism without concurrency is possible (SIMD instructions) but uncommon in application code.

### ✏️ Minimal Example

**BAD:**

```java
// Assuming parallelism = concurrency
// 1-core container, CPU-bound work:
IntStream.range(0, 1000)
    .parallel() // requests parallelism
    .map(x -> cpuHeavy(x))
    .sum();
// On 1 core: SLOWER (fork/join overhead, no parallelism)
```

Why it's wrong: parallel stream requests parallelism but hardware has only one core.

**GOOD:**

```java
// Concurrent structure for I/O (works on 1+ cores):
List<CompletableFuture<String>> futures =
    urls.stream()
        .map(url -> CompletableFuture.supplyAsync(
            () -> fetch(url)))
        .toList();
// 1 core: overlaps I/O waits (concurrent, not parallel)
// 4 cores: overlaps AND runs fetches simultaneously
```

Why it's right: concurrent structure benefits from ANY core count because I/O waits overlap.

### ⚡ When to use / Not to use

**Use when:**
- Deciding whether your workload is I/O-bound (concurrency helps) or CPU-bound (parallelism needed).
- Explaining performance gains (or lack thereof) to your team.

**Avoid when:**
- The workload is trivially small and sequential is adequate.
- Over-engineering a discussion about a simple single-threaded tool.

### ⚠️ One Gotcha

**Misconception:** "If my code is concurrent, it is parallel."
**Reality:** Concurrency on a single core is interleaving, not simultaneous execution. Parallelism requires multiple hardware execution units.

### 📇 Revision Card

1. Concurrency = structure (design). Parallelism = execution (runtime + hardware).
2. I/O-bound: concurrency helps on ANY core count. CPU-bound: only parallelism (multiple cores) helps.
3. parallel() without available cores adds overhead, not speed.

---

---

# Thread and Runnable

**TL;DR** - Thread is the execution vehicle; Runnable is the task definition - separating what to do from who does it.

### 🟢 What it is

**Thread** is a Java class representing an OS-level thread of execution. **Runnable** is a functional interface defining the task a thread executes - separating task logic from thread lifecycle.

### 🎯 Why it exists

Early Java forced you to extend Thread to define work, coupling lifecycle management with business logic. Runnable separates the two: define WHAT to do (Runnable) independently from HOW it executes (Thread, pool, virtual thread). This separation enables reuse and flexible execution. This is exactly why Runnable exists alongside Thread.

### 🧠 Mental Model

> Thread is a delivery truck. Runnable is the package. You do not build a new truck for every package - you put packages on available trucks. Separating them lets you reuse trucks (thread pools).

**Memory hook:** "Runnable = the work. Thread = the worker. Keep them separate."

### ⚙️ How it works

1. Implement `Runnable` (or pass a lambda) defining the task logic.
2. Create a `Thread` passing the Runnable, or submit it to an executor.
3. Call `thread.start()` - the JVM asks the OS for a new thread.
4. The OS schedules the thread; it calls `run()` on the Runnable.
5. When `run()` returns, the thread terminates and its resources are freed.

### ✏️ Minimal Example

**BAD:**

```java
// Extending Thread - couples task to thread lifecycle
class MyTask extends Thread {
    public void run() { process(); }
}
new MyTask().start();
// Cannot reuse with Executor. Cannot extend another class.
```

Why it's wrong: extending Thread wastes the single inheritance slot and couples task to execution.

**GOOD:**

```java
// Runnable separates task from execution
Runnable task = () -> process();
// Works with Thread:
new Thread(task).start();
// Works with pool:
executor.submit(task);
// Works with virtual thread:
Thread.startVirtualThread(task);
```

Why it's right: one task definition, three execution options - true separation.

### ⚡ When to use / Not to use

**Use when:**
- Defining any concurrent task (always prefer Runnable/Callable over extending Thread).
- You need the task reusable across execution contexts.

**Avoid when:**
- You need a return value (use Callable<T> instead of Runnable).
- Direct thread creation in production (use executors for lifecycle management).

### ⚠️ One Gotcha

**Misconception:** "Thread and Runnable are interchangeable choices."
**Reality:** Always prefer Runnable (or Callable). Extending Thread is an anti-pattern - it wastes inheritance, prevents executor reuse, and couples concerns.

### 📇 Revision Card

1. Runnable = task definition. Thread = execution vehicle. Always separate them.
2. Never extend Thread in production code - implement Runnable or Callable instead.
3. Runnable works with Thread, ExecutorService, and virtual threads - maximum flexibility.

---

---

# Thread Lifecycle and States

**TL;DR** - A thread moves through NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED states driven by scheduling and synchronization.

### 🟢 What it is

The **thread lifecycle** is the set of states a Java thread passes through from creation to death, governed by Thread.State enum values that represent OS scheduling and JVM synchronization decisions.

### 🎯 Why it exists

When debugging deadlocks or performance issues, thread dumps show state labels. Without understanding the lifecycle, "BLOCKED" and "WAITING" look the same - but they have completely different causes and fixes. Knowing states lets you read thread dumps correctly. This is exactly why thread lifecycle knowledge exists.

### 🧠 Mental Model

> A thread's life is like an airport journey: NEW (ticket bought, not at airport), RUNNABLE (in the terminal ready to board), BLOCKED (waiting for a gate held by another plane), WAITING (parked at gate waiting for signal), TERMINATED (arrived, journey over).

**Memory hook:** "NEW -> RUNNABLE -> (BLOCKED|WAITING|TIMED_WAITING)* -> TERMINATED"

### ⚙️ How it works

1. NEW: Thread object created but `start()` not yet called.
2. RUNNABLE: `start()` called. Thread is either running or ready to run (OS decides).
3. BLOCKED: Thread tries to enter a `synchronized` block held by another thread.
4. WAITING: Thread called `wait()`, `join()`, or `LockSupport.park()` indefinitely.
5. TIMED_WAITING: Same as WAITING but with a timeout (sleep, timed wait).
6. TERMINATED: `run()` completed or threw an uncaught exception.

### ✏️ Minimal Example

**BAD:**

```java
Thread t = new Thread(() -> work());
t.run(); // WRONG: executes in CURRENT thread, not new
// Thread t never leaves NEW state
```

Why it's wrong: `run()` is just a method call; `start()` creates the OS thread.

**GOOD:**

```java
Thread t = new Thread(() -> work());
// State: NEW
t.start();
// State: RUNNABLE (or running)
t.join(); // caller enters WAITING until t finishes
// t state: TERMINATED
```

Why it's right: `start()` transitions thread through proper lifecycle; `join()` is proper waiting.

### ⚡ When to use / Not to use

**Use when:**
- Reading thread dumps during deadlock/hang investigation.
- Understanding why a thread is not progressing (BLOCKED vs WAITING).

**Avoid when:**
- You are using high-level abstractions (ExecutorService) that manage lifecycle for you.
- Obsessing over states when the real issue is business logic.

### ⚠️ One Gotcha

**Misconception:** "RUNNABLE means the thread is executing right now."
**Reality:** RUNNABLE includes both running AND ready-to-run. A RUNNABLE thread may be waiting for a CPU time slice from the OS scheduler.

### 📇 Revision Card

1. Six states: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.
2. BLOCKED = waiting for a monitor lock. WAITING = waiting for a signal. Different causes, different fixes.
3. RUNNABLE does not mean running - it means eligible to run when the OS schedules it.

---

---

# synchronized Keyword

**TL;DR** - synchronized ensures only one thread at a time executes a critical section by acquiring an exclusive monitor lock.

### 🟢 What it is

The **synchronized** keyword is Java's built-in mutual exclusion mechanism: it acquires an intrinsic monitor lock on an object, allowing only one thread to execute the guarded code block at any time.

### 🎯 Why it exists

Without synchronization, two threads modifying the same field produce corrupted data (the shared mutable state problem). The language needed a built-in way to make code regions mutually exclusive - simple enough that every Java developer can use it, automatic enough that unlock cannot be forgotten. This is exactly why synchronized exists.

### 🧠 Mental Model

> synchronized is a bathroom door lock. Only one person enters at a time. Others wait in line. When the person exits, the next in line enters. The "lock" is not the door (code) - it is the object you synchronize ON.

**Memory hook:** "synchronized(object) = acquire the lock THAT object holds. Wrong object = wrong lock = no protection."

### ⚙️ How it works

1. Thread reaches `synchronized(obj)` block.
2. If no other thread holds obj's monitor: acquire it, enter block.
3. If another thread holds it: current thread state becomes BLOCKED.
4. When holding thread exits the block: monitor released, one waiting thread wakes.
5. synchronized also establishes happens-before: writes by exiting thread are visible to entering thread.

### ✏️ Minimal Example

**BAD:**

```java
// Synchronizing on different objects - NO protection
private int count;
void inc() {
    synchronized(new Object()) { // NEW lock each call!
        count++;
    }
}
```

Why it's wrong: each call locks a different object - threads never contend - no mutual exclusion.

**GOOD:**

```java
private int count;
private final Object lock = new Object();
void inc() {
    synchronized(lock) { // SAME lock every call
        count++;
    }
}
```

Why it's right: all threads compete for the SAME lock object, guaranteeing mutual exclusion.

### ⚡ When to use / Not to use

**Use when:**
- Simple mutual exclusion with automatic unlock on exit (including exceptions).
- You need both atomicity AND visibility guarantees.

**Avoid when:**
- You need try-lock, timed-lock, or interruptible-lock (use ReentrantLock).
- The critical section is read-heavy (use ReadWriteLock for reader concurrency).

### ⚠️ One Gotcha

**Misconception:** "synchronized makes the method slow."
**Reality:** Uncontended synchronized costs ~20 nanoseconds (JVM optimizes with thin/biased locks). It is only slow under HIGH contention from many threads.

### 📇 Revision Card

1. synchronized acquires the monitor of a SPECIFIC object - wrong object = no protection.
2. Automatically releases on block exit (even exceptions) - cannot forget to unlock.
3. Uncontended cost is ~20ns. Only contention makes it expensive.

---

---

# volatile Keyword

**TL;DR** - volatile guarantees visibility of writes across threads and prevents instruction reordering but does NOT provide atomicity for compound operations.

### 🟢 What it is

The **volatile** keyword marks a field so that every read comes from main memory and every write flushes to main memory immediately, preventing CPU caches from hiding updates between threads.

### 🎯 Why it exists

Without volatile, the JVM and CPU may cache a field in a register or reorder reads/writes for performance. Thread A writes `running = false` but Thread B's CPU cache still holds `true` - an infinite loop. volatile forces cross-thread visibility without the weight of synchronized. This is exactly why volatile exists.

### 🧠 Mental Model

> volatile is a shared whiteboard in an office. Without it, each person has a personal notepad (CPU cache) that might be stale. With volatile, everyone reads/writes the whiteboard directly - always seeing the latest value.

**Memory hook:** "volatile = always read from shared memory, never from local cache."

### ⚙️ How it works

1. Write to a volatile field: JVM inserts a store fence - flushes write to main memory.
2. Read from a volatile field: JVM inserts a load fence - reads from main memory.
3. Prevents reordering: instructions before a volatile write cannot be moved after it (release semantics).
4. Does NOT make compound operations (read-modify-write) atomic.

### ✏️ Minimal Example

**BAD:**

```java
volatile int count = 0;
// Two threads:
count++; // STILL not atomic!
// volatile ensures visibility but count++ is STILL
// read + increment + write (three operations)
```

Why it's wrong: volatile does not make `count++` atomic - races still occur.

**GOOD:**

```java
volatile boolean running = true;
// Thread 1 (producer):
running = false; // visible to all threads immediately
// Thread 2 (consumer):
while (running) { // guaranteed to see the update
    doWork();
}
```

Why it's right: single-writer boolean flag - volatile is sufficient (no compound operation).

### ⚡ When to use / Not to use

**Use when:**
- Single-writer, multiple-reader flag (shutdown signal, configuration toggle).
- You need visibility guarantee without mutual exclusion.

**Avoid when:**
- Compound operations (increment, check-then-act) - use AtomicInteger or synchronized.
- Multiple writers - volatile provides no atomicity for read-modify-write.

### ⚠️ One Gotcha

**Misconception:** "volatile makes everything thread-safe."
**Reality:** volatile provides VISIBILITY only. It does NOT provide atomicity. `volatile counter++` is still a race condition.

### 📇 Revision Card

1. volatile = visibility (always read main memory) + ordering (no reordering past the fence).
2. volatile does NOT provide atomicity. `count++` on volatile is still broken.
3. Perfect for: single-writer boolean flags. Wrong for: counters, check-then-act.

---

---

# wait, notify, notifyAll

**TL;DR** - wait() releases the monitor and sleeps until another thread calls notify/notifyAll on the same object, enabling thread coordination.

### 🟢 What it is

**wait()**, **notify()**, and **notifyAll()** are Object methods that enable threads to coordinate: one thread waits for a condition, another thread signals when the condition is met.

### 🎯 Why it exists

Busy-waiting (spinning in a loop checking a condition) wastes CPU. You need a way for a thread to say "wake me up when something changes" without burning cycles. wait() suspends the thread and releases the lock; notify() wakes it up when the condition may be satisfied. This is exactly why wait/notify exists.

### 🧠 Mental Model

> wait() is sitting in a waiting room and releasing your number ticket. notify() is the receptionist calling "next!" - one person wakes up. notifyAll() is yelling "everyone check if it is your turn!" - all wake up and re-check.

**Memory hook:** "wait releases the lock and sleeps. notify wakes ONE. notifyAll wakes ALL. Always re-check the condition after waking."

### ⚙️ How it works

1. Thread A acquires the monitor (synchronized) and checks a condition.
2. Condition is false: Thread A calls `obj.wait()` - releases monitor, enters WAITING.
3. Thread B acquires the same monitor, changes the condition, calls `obj.notify()`.
4. Thread A wakes up, re-acquires the monitor, re-checks the condition (spurious wakeups!).
5. If condition now true: proceed. If not: wait again (loop).

### ✏️ Minimal Example

**BAD:**

```java
synchronized(lock) {
    if (!ready) lock.wait(); // WRONG: 'if' not 'while'
    process();
}
// Bug: spurious wakeup or notify from unrelated condition
// -> process() runs with ready still false
```

Why it's wrong: single `if` check does not handle spurious wakeups or stolen signals.

**GOOD:**

```java
synchronized(lock) {
    while (!ready) { lock.wait(); } // re-check after wake
    process();
}
// Correct: loop re-checks condition after every wakeup
```

Why it's right: `while` loop handles spurious wakeups and ensures condition is truly met.

### ⚡ When to use / Not to use

**Use when:**
- Simple producer-consumer patterns with pre-JDK5 code.
- You need to understand legacy code that uses wait/notify.

**Avoid when:**
- Modern code: prefer `Condition` (from ReentrantLock) or `BlockingQueue`.
- Complex coordination: use CountDownLatch, CyclicBarrier, or Semaphore.

### ⚠️ One Gotcha

**Misconception:** "notify() guarantees the right thread wakes up."
**Reality:** notify() wakes an ARBITRARY waiting thread. If multiple threads wait on the same object for different conditions, the wrong thread may wake. Use notifyAll() or separate Condition objects.

### 📇 Revision Card

1. ALWAYS wait in a while loop (never if) - spurious wakeups are real.
2. wait() RELEASES the monitor; you must hold it first (synchronized required).
3. Prefer BlockingQueue or Condition in modern code over raw wait/notify.

---

---

# Thread.sleep vs Object.wait

**TL;DR** - sleep() pauses the current thread without releasing locks; wait() pauses AND releases the monitor lock enabling other threads to proceed.

### 🟢 What it is

**Thread.sleep(ms)** suspends the current thread for a duration without releasing any held locks. **Object.wait()** suspends the thread AND releases the object's monitor lock, allowing other threads to enter the synchronized block.

### 🎯 Why it exists

Confusing sleep and wait causes deadlocks. If Thread A holds a lock and calls sleep() inside synchronized, no other thread can acquire that lock for the entire sleep duration - blocking all progress. wait() exists specifically to RELEASE the lock while waiting, enabling cooperative multi-threading. This is exactly why the distinction matters critically.

### 🧠 Mental Model

> sleep() is falling asleep in the bathroom with the door locked - nobody else can enter. wait() is stepping into the waiting room and leaving the bathroom unlocked - others can use it while you wait.

**Memory hook:** "sleep HOLDS the lock (blocks everyone). wait RELEASES the lock (lets others work)."

### ⚙️ How it works

1. `Thread.sleep(1000)`: current thread pauses 1s. Any held monitors remain held.
2. `obj.wait()`: current thread releases obj's monitor, enters WAITING state.
3. `obj.wait(1000)`: same but wakes after timeout (TIMED_WAITING).
4. After sleep: thread re-enters RUNNABLE (still holds locks).
5. After wait wakeup: thread must RE-ACQUIRE the monitor before proceeding.

### ✏️ Minimal Example

**BAD:**

```java
synchronized(lock) {
    Thread.sleep(5000); // Holds lock for 5 seconds!
    // Every other thread needing this lock: BLOCKED
}
```

Why it's wrong: sleep inside synchronized blocks all other threads from the lock for the duration.

**GOOD:**

```java
synchronized(lock) {
    while (!condition) {
        lock.wait(5000); // Releases lock while waiting
    }
    // Other threads can enter synchronized(lock) blocks
}
```

Why it's right: wait releases the lock, allowing other threads to make progress and signal the condition.

### ⚡ When to use / Not to use

**Use when:**
- sleep: fixed delay outside any lock (rate limiting, backoff).
- wait: coordinating between threads inside synchronized blocks.

**Avoid when:**
- sleep inside synchronized (creates unnecessary blocking).
- wait without a condition variable (pointless wake without check).

### ⚠️ One Gotcha

**Misconception:** "sleep and wait are both just pausing."
**Reality:** sleep is SELFISH (holds all locks, blocks others). wait is COOPERATIVE (releases lock, lets others work). In synchronized code, using sleep instead of wait can deadlock the system.

### 📇 Revision Card

1. sleep: pause + HOLD locks. wait: pause + RELEASE the monitor.
2. Never call sleep() inside synchronized - use wait() if you need to pause while holding a monitor.
3. wait requires synchronized (must hold the monitor to release it); sleep does not.

---

---

# Race Condition

**TL;DR** - A race condition occurs when program correctness depends on unpredictable thread scheduling order.

### 🟢 What it is

A **race condition** is a defect where the behavior of code depends on the relative timing of thread execution - sometimes producing correct results, sometimes incorrect, depending on which thread runs first.

### 🎯 Why it exists

Race conditions are the most common concurrency bug. They pass all tests (tests run sequentially or get lucky with timing), then fail in production under load when timing varies. They exist because shared mutable state combined with concurrent access creates timing-dependent outcomes. This is exactly why understanding races is foundational.

### 🧠 Mental Model

> Two people approaching a single parking spot from different directions. If they arrive at different times: no problem. If they arrive simultaneously: crash. The "race" is that correctness depends on arrival ORDER, which is unpredictable.

**Memory hook:** "If correctness depends on WHO runs first, it is a race. If races SOMETIMES work, they ALWAYS ship bugs."

### ⚙️ How it works

1. Two threads access shared state without synchronization.
2. Thread scheduling determines interleaving (OS-controlled, non-deterministic).
3. Some interleavings produce correct results (lucky).
4. Some interleavings produce incorrect results (race triggered).
5. Under load: more interleavings explored, more races surface.

### ✏️ Minimal Example

**BAD:**

```java
// Check-then-act race:
if (map.containsKey(key)) {     // Thread A checks
    // Thread B removes key HERE (between check and act)
    return map.get(key);        // Thread A acts: null!
}
```

Why it's wrong: gap between check and act allows another thread to invalidate the check.

**GOOD:**

```java
// Atomic check-and-act:
return map.computeIfAbsent(key, k -> createValue());
// ConcurrentHashMap: check + insert is ONE atomic operation
// No gap for another thread to interfere
```

Why it's right: computeIfAbsent makes the check-and-act atomic - no interleaving possible.

### ⚡ When to use / Not to use

**Use when:**
- Diagnosing flaky tests or intermittent production bugs.
- Reviewing code for thread safety (check-then-act is the #1 pattern to look for).

**Avoid when:**
- Single-threaded code (no races possible).
- Already using proper atomic operations or synchronized blocks.

### ⚠️ One Gotcha

**Misconception:** "If my tests pass, there is no race condition."
**Reality:** Races are probabilistic. A test may pass 999 times and fail on the 1000th run. Load testing and tools like jcstress expose races that unit tests miss.

### 📇 Revision Card

1. Race = correctness depends on unpredictable scheduling. Tests rarely catch them.
2. Check-then-act is the #1 race pattern. Fix: make check+act atomic (computeIfAbsent, synchronized).
3. Races get MORE likely under load (more interleavings explored) - production finds what tests miss.

---

---

# Deadlock

**TL;DR** - Deadlock occurs when two or more threads each hold a lock the other needs, creating a permanent circular wait.

### 🟢 What it is

A **deadlock** is a state where two or more threads are permanently blocked, each waiting to acquire a lock held by another thread in the group, forming a cycle that can never resolve.

### 🎯 Why it exists

Deadlocks are one of the hardest concurrency bugs: the program does not crash or throw exceptions - it simply stops making progress silently. They require four conditions simultaneously (mutual exclusion, hold-and-wait, no preemption, circular wait). Understanding these conditions lets you prevent them by breaking any one. This is exactly why deadlock understanding is essential.

### 🧠 Mental Model

> Two people in a narrow hallway face-to-face. Each says "you go first" while blocking the other's path. Neither moves. Forever. The "hallway" is the shared resource; the "blocking" is holding one lock while waiting for another.

**Memory hook:** "Lock A then lock B in one thread; lock B then lock A in another = deadlock. Always lock in the SAME order."

### ⚙️ How it works

1. Thread 1 acquires lock A, then attempts to acquire lock B.
2. Thread 2 acquires lock B, then attempts to acquire lock A.
3. Thread 1 holds A, waits for B (held by Thread 2).
4. Thread 2 holds B, waits for A (held by Thread 1).
5. Neither can proceed: circular wait. System hangs forever.

### ✏️ Minimal Example

**BAD:**

```java
// Thread 1:                    // Thread 2:
synchronized(lockA) {           synchronized(lockB) {
    synchronized(lockB) {           synchronized(lockA) {
        transfer();                     transfer();
    }                               }
}                               }
// Opposite lock ordering = deadlock
```

Why it's wrong: threads acquire locks in opposite order, creating a cycle.

**GOOD:**

```java
// BOTH threads: always lock A first, then B
synchronized(lockA) {
    synchronized(lockB) {
        transfer();
    }
}
// Consistent ordering = no cycle possible
```

Why it's right: consistent lock ordering eliminates circular wait - one of the four required conditions.

### ⚡ When to use / Not to use

**Use when:**
- Reviewing multi-lock code for safety (enforce consistent ordering).
- Diagnosing hangs: take a thread dump (jstack shows deadlock cycle directly).

**Avoid when:**
- Single-lock scenarios (deadlock impossible with one lock).
- You can restructure to eliminate nested locking entirely.

### ⚠️ One Gotcha

**Misconception:** "Deadlocks are rare in practice."
**Reality:** Deadlocks are common in production systems with multiple services locking shared resources (database row locks, distributed locks). jstack detects JVM-level deadlocks automatically.

### 📇 Revision Card

1. Four conditions: mutual exclusion, hold-and-wait, no preemption, circular wait. Break any ONE to prevent.
2. Fix: always acquire locks in the same global order across all threads.
3. Diagnosis: `jstack <pid>` prints "Found one Java-level deadlock" with the cycle.

---

---

# Atomicity, Visibility, Ordering

**TL;DR** - Thread safety requires atomicity (all-or-nothing), visibility (writes seen by others), and ordering (no surprise reordering).

### 🟢 What it is

**Atomicity**, **visibility**, and **ordering** are the three pillars of thread safety in the Java Memory Model. Violating any one causes concurrency bugs even if the other two are satisfied.

### 🎯 Why it exists

Engineers often fix only atomicity (adding synchronized) and miss visibility issues (stale cache reads) or ordering issues (compiler reordering). The three pillars give a checklist: for ANY shared variable, ask "is it atomic? visible? ordered?" If any answer is no, you have a potential bug. This is exactly why the three-pillar model exists.

### 🧠 Mental Model

> Three locks on a safe: Atomicity (no one can see a half-completed operation), Visibility (everyone sees the latest value), Ordering (events happen in the sequence you expect). Open any ONE lock and the safe is compromised.

**Memory hook:** "Atomic = all-or-nothing. Visible = I see your latest write. Ordered = no surprise reordering."

### ⚙️ How it works

1. Atomicity: operation completes entirely or not at all. `count++` is NOT atomic (read+modify+write).
2. Visibility: after Thread A writes a value, Thread B can read the updated value. Without volatile/synchronized, CPU caches may serve stale data.
3. Ordering: compiler/CPU reorders instructions for performance. Without memory barriers, Thread B may see operations in a different order than Thread A performed them.

### ✏️ Minimal Example

**BAD:**

```java
boolean ready = false; // not volatile
int answer = 0;
// Thread 1:
answer = 42;
ready = true;
// Thread 2:
if (ready) System.out.println(answer);
// May print 0! Reordering + visibility issue
```

Why it's wrong: without volatile, Thread 2 may see ready=true but answer=0 (reordered or cached).

**GOOD:**

```java
volatile boolean ready = false;
int answer = 0;
// Thread 1:
answer = 42;
ready = true; // volatile write: flushes answer too
// Thread 2:
if (ready) System.out.println(answer);
// Always prints 42: volatile establishes happens-before
```

Why it's right: volatile write of ready creates a happens-before edge that also publishes answer.

### ⚡ When to use / Not to use

**Use when:**
- Reviewing any shared state for thread safety (checklist: A, V, O).
- Choosing between volatile (visibility+ordering) and synchronized (all three).

**Avoid when:**
- State is thread-confined (no sharing = no need for these guarantees).
- Using immutable objects (no writes = no visibility/ordering concern).

### ⚠️ One Gotcha

**Misconception:** "synchronized only provides atomicity."
**Reality:** synchronized provides ALL three: atomicity (mutual exclusion), visibility (happens-before on monitor exit), and ordering (no reordering across lock boundaries). That is why it is the safest default.

### 📇 Revision Card

1. Three pillars: Atomicity (all-or-nothing), Visibility (see latest write), Ordering (no surprise reorder).
2. volatile gives visibility + ordering. synchronized gives all three.
3. Missing ANY pillar = bug. Check all three for every shared variable.

---

---

# Thread.start vs Thread.run Anti-Pattern

**TL;DR** - Calling run() executes the task in the CURRENT thread; only start() creates a new OS thread for concurrent execution.

### 🟢 What it is

The **Thread.start() vs Thread.run()** distinction is that `start()` creates a new OS thread and invokes `run()` on it, while calling `run()` directly just executes the method synchronously in the calling thread - no concurrency at all.

### 🎯 Why it exists

This is one of the most common beginner mistakes. The code compiles, runs without errors, and produces correct results - but executes sequentially. Under load, the expected parallelism never happens, latency multiplies, and the developer blames Java threading for being "broken." This is exactly why this anti-pattern is called out explicitly.

### 🧠 Mental Model

> start() is mailing a letter (separate delivery person carries it). run() is walking the letter over yourself (you do it, nobody else involved). Both deliver the letter, but only start() frees you to do other work.

**Memory hook:** "start() = new thread. run() = same thread. If you call run(), you have zero concurrency."

### ⚙️ How it works

1. `thread.start()`: JVM asks OS to create a new native thread. OS schedules it. `run()` executes on NEW thread.
2. `thread.run()`: ordinary method call. Executes in CALLING thread. No new thread created.
3. Both execute the same code - but start() enables concurrency.
4. You cannot call start() twice (throws IllegalThreadStateException).

### ✏️ Minimal Example

**BAD:**

```java
Thread t = new Thread(() -> heavyCompute());
t.run(); // Runs in main thread! No concurrency.
// Main thread blocks until heavyCompute() finishes.
```

Why it's wrong: `run()` is just a method call - no new thread, no concurrency.

**GOOD:**

```java
Thread t = new Thread(() -> heavyCompute());
t.start(); // New OS thread created. Main continues.
doOtherWork(); // Runs concurrently with heavyCompute
t.join();  // Wait for completion when needed
```

Why it's right: `start()` creates a real concurrent thread - main thread is free to continue.

### ⚡ When to use / Not to use

**Use when:**
- ALWAYS use start() for concurrent execution.
- Testing: deliberately calling run() for single-threaded test of task logic.

**Avoid when:**
- NEVER call run() expecting concurrent behavior.
- Never call start() twice on the same Thread object.

### ⚠️ One Gotcha

**Misconception:** "My code works fine with run() so it must be concurrent."
**Reality:** run() works sequentially by coincidence. It produces correct results but with zero concurrency. Performance tests reveal the problem; functional tests do not.

### 📇 Revision Card

1. start() = new OS thread + concurrent. run() = same thread + sequential.
2. The bug is invisible: run() compiles, runs, produces correct output - but no concurrency.
3. You cannot start() a thread twice - create a new Thread instance for re-execution.

---

---

# Synchronized Means Slow is Wrong - Lock Reality

**TL;DR** - Uncontended synchronized costs ~20 nanoseconds; it only becomes expensive under high thread contention for the same lock.

### 🟢 What it is

The **"synchronized is slow" myth** is the incorrect belief that using synchronized inherently makes code slow, when in reality the JVM heavily optimizes uncontended locks to near-zero cost.

### 🎯 Why it exists

This myth causes developers to either avoid synchronization (creating race conditions) or use complex lock-free code prematurely (creating maintainability nightmares). The JVM uses biased locking (pre-JDK 15), thin locks, and lock coarsening to make uncontended synchronized nearly free. The cost comes from CONTENTION, not from the keyword itself. This is exactly why debunking this myth matters.

### 🧠 Mental Model

> synchronized is like a turnstile. One person passing through: zero delay (uncontended). A crowd all pushing through at once: slow (contended). The turnstile is not "slow" - the crowd is the problem.

**Memory hook:** "Contention is expensive. synchronized is cheap. Do not confuse the lock with the crowd."

### ⚙️ How it works

1. Uncontended lock: JVM uses thin lock (CAS on object header) - ~20ns.
2. Slightly contended: JVM spins briefly hoping the holder releases soon.
3. Heavily contended: OS-level blocking (thread suspended, context switch) - microseconds.
4. JVM lock coarsening: merges adjacent synchronized blocks on the same object to reduce acquire/release overhead.

### ✏️ Minimal Example

**BAD:**

```java
// Avoiding synchronized out of fear -> race condition:
private int count;
public void increment() { count++; } // BROKEN: race
// "synchronized is slow" -> lost data
```

Why it's wrong: fear of synchronized creates a worse problem (data corruption).

**GOOD:**

```java
// Use synchronized; optimize ONLY if profiling shows
// contention:
private int count;
public synchronized void increment() { count++; }
// Cost: ~20ns uncontended. Correct always.
```

Why it's right: correctness first. Optimize only when profiling shows lock contention as the bottleneck.

### ⚡ When to use / Not to use

**Use when:**
- Default choice for protecting shared mutable state (correct first, fast later).
- Profiling shows no contention issue.

**Avoid when:**
- Profiling PROVES contention is the bottleneck AND you need finer-grained control (then use ReentrantLock, read-write locks, or atomics).
- High-contention hot paths where lock-free alternatives are measured to be faster.

### ⚠️ One Gotcha

**Misconception:** "Lock-free code is always faster than synchronized."
**Reality:** Lock-free code under contention can be SLOWER (spinning wastes CPU) than synchronized (which suspends threads, saving CPU cycles for useful work).

### 📇 Revision Card

1. Uncontended synchronized: ~20ns (JVM optimizes with thin locks).
2. The cost is CONTENTION (many threads fighting for one lock), not the keyword itself.
3. Correctness first. Profile. Optimize only when contention is proven.

---

---

# jstack and Thread Dumps

**TL;DR** - jstack captures all thread states and stack traces in a running JVM for diagnosing deadlocks and hangs.

### 🟢 What it is

**jstack** is a JDK diagnostic tool that prints the stack trace and state (RUNNABLE, BLOCKED, WAITING) of every thread in a target JVM process - a "thread dump."

### 🎯 Why it exists

When a Java application hangs or has degraded throughput, you need to know what every thread is doing RIGHT NOW. Is it stuck waiting for a lock? Blocked on I/O? In an infinite loop? jstack answers these questions instantly without restarting the application. This is exactly why jstack is the first tool you reach for during a hang.

### 🧠 Mental Model

> jstack is a freeze-frame photograph of everyone in a building: who they are (thread name), where they are (stack trace), and what they are waiting for (lock/state). Take three photos seconds apart to see who is stuck vs who is moving.

**Memory hook:** "Hung app? jstack <pid> three times, 5 seconds apart. Threads in the same state all three times = the problem."

### ⚙️ How it works

1. Run `jstack <pid>` (or `jcmd <pid> Thread.print`).
2. JVM halts all threads briefly at a safepoint.
3. Captures each thread's name, state, stack frames, and held/waiting locks.
4. Outputs text showing lock dependencies - deadlocks are reported automatically.
5. Compare multiple dumps: stuck threads appear identically across dumps.

### ✏️ Minimal Example

**BAD:**

```java
// Guessing at the problem without evidence:
// "It's probably the database connection pool"
// Restart. Hope it doesn't happen again.
// (It will.)
```

Why it's wrong: restarting without diagnosis means the problem will recur.

**GOOD:**

```bash
# Take 3 thread dumps 5 seconds apart:
jstack 12345 > dump1.txt
sleep 5
jstack 12345 > dump2.txt
sleep 5
jstack 12345 > dump3.txt
# Compare: threads stuck in same state = root cause
# "Found one Java-level deadlock" = automatic detection
```

Why it's right: evidence-based diagnosis identifies the exact stuck threads and lock cycles.

### ⚡ When to use / Not to use

**Use when:**
- Application hangs (zero throughput).
- High latency with many BLOCKED threads (contention).
- Suspected deadlock.

**Avoid when:**
- Performance problems that are not thread-related (GC, memory).
- Need historical data (use JFR for continuous profiling).

### ⚠️ One Gotcha

**Misconception:** "One thread dump is enough."
**Reality:** A single dump is a snapshot - a thread might be RUNNABLE for 1ms between long BLOCKED periods. Three dumps 5s apart reveal which threads are PERSISTENTLY stuck (the real problem).

### 📇 Revision Card

1. `jstack <pid>` or `jcmd <pid> Thread.print` - captures all thread states and stacks.
2. Three dumps, 5 seconds apart. Threads stuck in same state across all three = the problem.
3. JVM automatically reports deadlock cycles in jstack output.

---

---

# Top 10 Java Concurrency Interview Questions

**TL;DR** - The essential concurrency interview questions test understanding of thread safety, synchronization mechanisms, and production debugging ability.

### 🟢 What it is

The **top Java concurrency interview questions** are the recurring questions that test whether a candidate truly understands thread safety, JMM basics, and can diagnose production concurrency issues - not memorized definitions.

### 🎯 Why it exists

Concurrency is the #1 topic where interviewers separate "studied it" from "used it." A candidate who can explain WHY double-checked locking broke before Java 5, or HOW to diagnose a deadlock in production, demonstrates real understanding. Knowing the questions helps you prepare; knowing the WHY behind answers ensures you can handle follow-ups. This is exactly why these questions are catalogued.

### 🧠 Mental Model

> Interview questions are probes into connected understanding. The interviewer asks "What is volatile?" but they actually test: "Do you know that volatile gives visibility but NOT atomicity, AND can you give a scenario where this distinction matters?"

**Memory hook:** "Every interview answer needs: WHAT it is + WHY it exists + WHEN it breaks."

### ⚙️ How it works

1. Q: "Difference between volatile and synchronized?" A: volatile = visibility + ordering; synchronized = atomicity + visibility + ordering.
2. Q: "What causes deadlock?" A: Circular wait with hold-and-wait. Fix = consistent lock ordering.
3. Q: "Is HashMap thread-safe?" A: No. Use ConcurrentHashMap (lock striping) or Collections.synchronizedMap (single lock).
4. Q: "How do you detect a deadlock in production?" A: jstack prints the cycle automatically.
5. Q: "Can you have a race without a crash?" A: Yes - silent data corruption is worse than a crash.

### ✏️ Minimal Example

**BAD:**

```java
// Weak interview answer:
// "volatile makes a variable thread-safe"
// WRONG: volatile does not provide atomicity.
// Interviewer: "Is volatile int count; count++ safe?"
// If you answer yes: interview over.
```

Why it's wrong: conflating visibility with atomicity reveals shallow understanding.

**GOOD:**

```java
// Strong answer demonstrates connected knowledge:
// "volatile provides visibility and ordering via
// memory barriers, but NOT atomicity. So
// volatile int count; count++; is still a race.
// For atomic increment: AtomicInteger or synchronized.
// volatile is correct for single-writer flags."
```

Why it's right: shows the boundary (what it does NOT do) which proves deep understanding.

### ⚡ When to use / Not to use

**Use when:**
- Preparing for Java interviews (mid to senior level).
- Self-assessing your concurrency understanding.

**Avoid when:**
- Memorizing answers without understanding - follow-ups will expose gaps.
- Using these as a checklist for production design (real design needs deeper analysis).

### ⚠️ One Gotcha

**Misconception:** "Knowing definitions is enough for interviews."
**Reality:** Interviewers ask follow-ups: "When would you NOT use this?" and "How would you debug this in production?" Definitions without production context fail interviews.

### 📇 Revision Card

1. Every answer needs: WHAT + WHY + WHEN IT BREAKS.
2. The five core topics: volatile vs synchronized, deadlock, race conditions, thread-safe collections, thread pools.
3. Strongest signal: explaining what a mechanism does NOT do (boundaries reveal mastery).

---

---

# Thread Safety Exercise - Broken Counter

**TL;DR** - A hands-on exercise demonstrating how an unsynchronized counter loses increments and how different fixes (synchronized, AtomicInteger, LongAdder) trade off.

### 🟢 What it is

The **broken counter exercise** is a practical demonstration where multiple threads increment a shared counter, revealing lost updates, and exploring three fix strategies with different performance characteristics.

### 🎯 Why it exists

Reading about race conditions is abstract. Running code that produces 1,834,721 instead of 2,000,000 makes the problem visceral. Trying three different fixes and benchmarking them builds intuition about when to use which synchronization tool. This is exactly why hands-on exercises exist.

### 🧠 Mental Model

> This exercise is a controlled crash: deliberately break something to learn how it breaks, then fix it three ways to learn the trade-offs between correctness tools.

**Memory hook:** "Broken counter: the first exercise every concurrent programmer must run with their own hands."

### ⚙️ How it works

1. Create a shared `int counter = 0`.
2. Launch N threads, each incrementing counter M times.
3. Expected result: N * M. Actual result: less (lost updates).
4. Fix 1: `synchronized` - correct, simple, contention under load.
5. Fix 2: `AtomicInteger.incrementAndGet()` - correct, lock-free, better scaling.
6. Fix 3: `LongAdder.increment()` - correct, cell-striped, best throughput under high contention.

### ✏️ Minimal Example

**BAD:**

```java
static int counter = 0;
// 10 threads, each: for(i=0; i<100_000; i++) counter++;
// Expected: 1,000,000  Actual: ~800,000 (varies!)
```

Why it's wrong: `counter++` is not atomic; threads overwrite each other's increments.

**GOOD:**

```java
static AtomicInteger counter = new AtomicInteger(0);
// 10 threads, each: for(i=0; i<100_000; i++)
//   counter.incrementAndGet();
// Result: exactly 1,000,000 every run
```

Why it's right: AtomicInteger uses hardware CAS for true atomic increment.

### ⚡ When to use / Not to use

**Use when:**
- Learning concurrency (first exercise to run).
- Benchmarking synchronization primitives for your specific contention level.

**Avoid when:**
- Production code: use the appropriate atomic/lock class directly (do not re-derive).
- Already proficient and want to study higher-level patterns.

### ⚠️ One Gotcha

**Misconception:** "AtomicInteger is always the best choice for counters."
**Reality:** Under very high contention (many threads), LongAdder outperforms AtomicInteger significantly because it distributes updates across cache-line-aligned cells.

### 📇 Revision Card

1. `int counter; counter++` loses updates under concurrency - always.
2. Three fixes by contention level: synchronized (simple), AtomicInteger (lock-free), LongAdder (high contention).
3. Run it yourself: seeing 800,000 instead of 1,000,000 teaches more than any textbook paragraph.

---

---

# Concurrent Chat - Phase 1 (Raw Threads)

**TL;DR** - Build a multi-client chat server using raw threads to experience thread lifecycle, shared state, and synchronization challenges firsthand.

### 🟢 What it is

**Concurrent Chat Phase 1** is a project exercise where you build a TCP chat server handling multiple clients with one thread per connection, encountering real concurrency problems (shared client list, broadcasting, disconnection) and solving them with basic synchronization.

### 🎯 Why it exists

Tutorials explain concurrency in isolation. Building a chat server forces you to combine everything: thread creation, shared mutable state (client list), synchronization (broadcasting to all), cleanup (disconnection), and error handling - in one small but realistic project. This is exactly why project-based learning cements concepts.

### 🧠 Mental Model

> Phase 1 is "concurrency boot camp" - a simple project that exercises every concept from this subtopic in combination: threads, shared state, synchronized, lifecycle, and failure handling.

**Memory hook:** "One thread per client. One synchronized list of clients. Broadcast to all. Handle disconnect gracefully."

### ⚙️ How it works

1. Server accepts connections in a loop; spawns a new Thread per client.
2. Each client thread reads messages and broadcasts to all others.
3. Client list (shared state) must be synchronized for add/remove/iterate.
4. Client disconnection: remove from list, close socket, thread terminates.
5. Broadcast: iterate synchronized list, write to each client's output stream.

### ✏️ Minimal Example

**BAD:**

```java
// Unsynchronized client list:
List<Socket> clients = new ArrayList<>();
// Thread A: clients.add(newClient);
// Thread B: for(Socket s : clients) send(s, msg);
// ConcurrentModificationException or missed clients!
```

Why it's wrong: ArrayList is not thread-safe; concurrent add + iterate throws or loses messages.

**GOOD:**

```java
List<Socket> clients =
    Collections.synchronizedList(new ArrayList<>());
void broadcast(String msg) {
    synchronized(clients) { // must sync for iteration
        for (Socket s : clients) send(s, msg);
    }
}
```

Why it's right: synchronized iteration prevents ConcurrentModificationException and ensures all current clients receive the message.

### ⚡ When to use / Not to use

**Use when:**
- Learning concurrency fundamentals through building.
- Understanding WHY thread pools (Phase 2) and async (Phase 3) exist.

**Avoid when:**
- Production chat systems (use Netty, WebSocket frameworks).
- You have already built concurrent servers and need advanced patterns.

### ⚠️ One Gotcha

**Misconception:** "Thread-per-connection works fine for production."
**Reality:** Each thread consumes ~1MB stack memory. 10,000 clients = 10GB just for stacks. Phase 2 (executors) and Phase 4 (virtual threads) solve this scalability problem.

### 📇 Revision Card

1. One thread per client + synchronized shared list = simplest working chat server.
2. Always synchronize iteration over shared collections (not just add/remove).
3. This design breaks at scale (~10K connections) - Phase 2 introduces pooling as the solution.
