---
title: "Spring - Core and Foundations"
topic: Spring Ecosystem
subtopic: Core and Foundations
layout: default
parent: Spring Ecosystem
grand_parent: "Learn"
nav_order: 1
permalink: /learn/spring/core-and-foundations/
category: Spring Ecosystem
code: SPR
folder: learn/spring/
difficulty_range: easy
status: complete
version: 1
generated_from: LEARN_KEYWORD_GENERATOR.md v1.0
archetype: FRAMEWORK
mode: MODE_NEW
provenance: "user request via /learn: spring ecosystem"
keywords:
  - SPR-001 The Enterprise Java Problem Before Spring
  - SPR-002 What Is the Spring Ecosystem
  - SPR-003 Spring vs Java EE (Jakarta EE) - The Big Picture
  - SPR-004 Spring Project Landscape Map
  - SPR-005 Spring Boot - What Problem It Solves
  - SPR-006 When Spring Is Overkill Anti-Pattern
  - SPR-007 Your First Spring Boot Application (Hands-On)
  - SPR-008 Inversion of Control (IoC) Container
  - SPR-009 Dependency Injection - Constructor vs Field vs Setter
  - SPR-010 Spring Bean and Bean Scope
  - SPR-011 ApplicationContext
  - SPR-012 Stereotype Annotations (@Component Family)
  - SPR-013 Spring Boot Starters
  - SPR-014 application.properties and application.yml
  - SPR-015 Spring Boot Auto-Configuration Basics
  - SPR-016 Embedded Server (Tomcat, Jetty, Netty)
  - SPR-017 Spring Initializr (start.spring.io)
  - SPR-018 "Spring Does Magic" is Wrong - Convention over Configuration
  - SPR-019 Hardcoded Configuration Anti-Pattern
  - SPR-020 Top 10 Spring Interview Questions (Basics)
  - SPR-021 Spring Boot DevTools and Live Reload
  - SPR-022 REST API Phase 1 - Spring Boot CRUD
  - SPR-023 Spring Boot Project Setup Exercise
---

## Keywords

1. [SPR-001 The Enterprise Java Problem Before Spring](#spr-001-the-enterprise-java-problem-before-spring)
2. [SPR-002 What Is the Spring Ecosystem](#spr-002-what-is-the-spring-ecosystem)
3. [SPR-003 Spring vs Java EE (Jakarta EE) - The Big Picture](#spr-003-spring-vs-java-ee-jakarta-ee---the-big-picture)
4. [SPR-004 Spring Project Landscape Map](#spr-004-spring-project-landscape-map)
5. [SPR-005 Spring Boot - What Problem It Solves](#spr-005-spring-boot---what-problem-it-solves)
6. [SPR-006 When Spring Is Overkill Anti-Pattern](#spr-006-when-spring-is-overkill-anti-pattern)
7. [SPR-007 Your First Spring Boot Application (Hands-On)](#spr-007-your-first-spring-boot-application-hands-on)
8. [SPR-008 Inversion of Control (IoC) Container](#spr-008-inversion-of-control-ioc-container)
9. [SPR-009 Dependency Injection - Constructor vs Field vs Setter](#spr-009-dependency-injection---constructor-vs-field-vs-setter)
10. [SPR-010 Spring Bean and Bean Scope](#spr-010-spring-bean-and-bean-scope)
11. [SPR-011 ApplicationContext](#spr-011-applicationcontext)
12. [SPR-012 Stereotype Annotations (@Component Family)](#spr-012-stereotype-annotations-component-family)
13. [SPR-013 Spring Boot Starters](#spr-013-spring-boot-starters)
14. [SPR-014 application.properties and application.yml](#spr-014-applicationproperties-and-applicationyml)
15. [SPR-015 Spring Boot Auto-Configuration Basics](#spr-015-spring-boot-auto-configuration-basics)
16. [SPR-016 Embedded Server (Tomcat, Jetty, Netty)](#spr-016-embedded-server-tomcat-jetty-netty)
17. [SPR-017 Spring Initializr (start.spring.io)](#spr-017-spring-initializr-startspringio)
18. [SPR-018 "Spring Does Magic" is Wrong - Convention over Configuration](#spr-018-spring-does-magic-is-wrong---convention-over-configuration)
19. [SPR-019 Hardcoded Configuration Anti-Pattern](#spr-019-hardcoded-configuration-anti-pattern)
20. [SPR-020 Top 10 Spring Interview Questions (Basics)](#spr-020-top-10-spring-interview-questions-basics)
21. [SPR-021 Spring Boot DevTools and Live Reload](#spr-021-spring-boot-devtools-and-live-reload)
22. [SPR-022 REST API Phase 1 - Spring Boot CRUD](#spr-022-rest-api-phase-1---spring-boot-crud)
23. [SPR-023 Spring Boot Project Setup Exercise](#spr-023-spring-boot-project-setup-exercise)

---

# SPR-001 The Enterprise Java Problem Before Spring

**TL;DR** - Enterprise Java before Spring drowned developers in XML, boilerplate, and vendor lock-in.

### 🟢 What it is

**The Enterprise Java Problem** is the set of pain points - heavyweight EJB containers, verbose XML descriptors, tight vendor coupling, and slow development cycles - that plagued enterprise Java before Spring.

### 🎯 Why it exists

In the early 2000s, building a Java web app meant writing an EJB with a home interface, a remote interface, a bean class, and XML deployment descriptors - just to persist one object. Testing required a running application server. Switching from WebLogic to WebSphere meant rewriting deployment configs. This is exactly why **the enterprise Java problem** exists - it created the demand for something better.

### 🧠 Mental Model

> Imagine building a house where the building code requires 50 forms per room and you cannot test whether the door opens without constructing the entire neighborhood first.

**Memory hook:** J2EE was a tax on simplicity - Spring was the tax refund.

### ⚙️ How it works

1. Developer writes a business class (the actual logic).
2. J2EE forces wrapping it in multiple interfaces, XML descriptors, and container-specific config.
3. The app server (WebLogic, WebSphere) compiles, deploys, and manages the lifecycle.
4. Testing requires the full server to be running - no unit tests in isolation.
5. Changing vendors means rewriting deployment descriptors and sometimes code.

### ✏️ Minimal Example

**BAD:**

```java
// J2EE 1.4 - just to expose a service
public class OrderServiceBean
    implements SessionBean {
  public void ejbCreate() {}
  public void ejbRemove() {}
  public void ejbActivate() {}
  public void ejbPassivate() {}
  public void setSessionContext(
      SessionContext ctx) {}
  public Order createOrder(Item item) {
    return new Order(item);
  }
}
```

Why it's wrong: 80% ceremony, 20% logic. Untestable without a container.

**GOOD:**

```java
// Spring - same capability
@Service
public class OrderService {
  public Order createOrder(Item item) {
    return new Order(item);
  }
}
```

Why it's right: pure business logic, testable with `new OrderService()`, zero XML.

### ⚡ When to use / Not to use

**Use when:**

- You need to understand why Spring's design choices exist (historical context powers better decisions)
- You are evaluating whether legacy J2EE code should be migrated

**Avoid when:**

- You are starting a greenfield project (start with Spring Boot directly)
- You are comparing modern Jakarta EE 10+ which fixed most of these issues

### ⚠️ One Gotcha

**Misconception:** "Jakarta EE is still the same mess as J2EE."
**Reality:** Jakarta EE 10+ adopted many Spring ideas (CDI, annotations, embedded servers). The gap narrowed, but Spring's ecosystem momentum remains larger.

### 📇 Revision Card

1. J2EE forced massive boilerplate and vendor lock-in for simple operations
2. The core pain: untestable code, XML overload, container dependency
3. Spring did not invent new ideas - it made existing ideas (IoC, POJO-based) practical

---

---

# SPR-002 What Is the Spring Ecosystem

**TL;DR** - Spring is a family of projects that simplifies every layer of Java application development.

### 🟢 What it is

The **Spring Ecosystem** is a collection of interrelated projects - Spring Framework (core IoC/DI), Spring Boot (opinionated auto-configuration), Spring Data (database access), Spring Security (authentication/authorization), Spring Cloud (distributed systems), and others - all sharing a common programming model built on dependency injection and convention over configuration.

### 🎯 Why it exists

Building a production Java application requires solving dozens of cross-cutting problems: dependency management, web serving, database access, security, caching, messaging, monitoring. Without a unifying ecosystem, teams stitch together incompatible libraries, write glue code, and maintain custom integration layers. Each integration decision multiplies configuration and testing surface. This is exactly why **the Spring Ecosystem** exists - one coherent family where every piece is designed to work together.

### 🧠 Mental Model

> Think of Spring as a modular tool chest. The chest itself (Spring Framework) holds tools in organized drawers. Spring Boot is the quick-start guide that picks the right tools for common jobs. Each drawer (Data, Security, Cloud) is optional - take only what you need.

**Memory hook:** Spring Framework is the engine, Spring Boot is the ignition key.

### ⚙️ How it works

1. Spring Framework provides the IoC container, AOP, and core abstractions.
2. Spring Boot layers opinionated defaults and auto-configuration on top.
3. Specialized projects (Data, Security, Cloud) plug into the container as starters.
4. You add a starter dependency - Boot auto-configures the integration.
5. All projects share the same lifecycle, configuration model, and testing support.

### ✏️ Minimal Example

**BAD:**

```xml
<!-- Manually wiring 4 libraries with
     incompatible versions -->
<dependency>
  <groupId>org.hibernate</groupId>
  <artifactId>hibernate-core</artifactId>
  <version>5.6.15</version>
</dependency>
<dependency>
  <groupId>com.zaxxer</groupId>
  <artifactId>HikariCP</artifactId>
  <version>4.0.3</version><!-- conflict? -->
</dependency>
```

Why it's wrong: manual version management, no guaranteed compatibility.

**GOOD:**

```xml
<!-- One starter, versions managed by Boot -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>
    spring-boot-starter-data-jpa
  </artifactId>
</dependency>
```

Why it's right: Boot's BOM manages Hibernate, HikariCP, and JDBC driver versions in harmony.

### ⚡ When to use / Not to use

**Use when:**

- You are building any non-trivial Java backend (REST APIs, microservices, batch jobs)
- You need tested integration between web, data, security, and messaging layers

**Avoid when:**

- A simple CLI tool or library with no framework needs
- You need the smallest possible binary (consider Micronaut or Quarkus for serverless)

### ⚠️ One Gotcha

**Misconception:** "Spring and Spring Boot are the same thing."
**Reality:** Spring Framework is the foundational IoC container. Spring Boot is an opinionated layer that auto-configures it. You can use Spring Framework without Boot (rare today, but possible for legacy apps).

### 📇 Revision Card

1. Spring is a project family - Framework (core), Boot (opinions), Data/Security/Cloud (specializations)
2. Starters bundle compatible dependencies so you never manage version conflicts manually
3. Spring Boot is not Spring - it is an opinionated auto-configuration layer on top of Spring Framework

---

---

# SPR-003 Spring vs Java EE (Jakarta EE) - The Big Picture

**TL;DR** - Spring innovates fast via open-source leadership; Jakarta EE standardizes slowly via committee consensus.

### 🟢 What it is

**Spring vs Java EE (Jakarta EE)** is the fundamental architectural choice for enterprise Java: Spring's opinionated, community-driven ecosystem versus Jakarta EE's specification-driven, multi-vendor standard. Both solve the same problems (DI, web, persistence, security) with different governance models and velocity.

### 🎯 Why it exists

Two competing philosophies emerged for enterprise Java. Sun/Oracle created J2EE as a vendor-neutral specification implemented by application servers. Rod Johnson created Spring as a practical reaction to J2EE's complexity. Today, Jakarta EE (post-Oracle transfer to Eclipse Foundation) and Spring coexist, each influencing the other. Understanding the difference matters because your choice affects hiring, library availability, migration paths, and long-term support. This is exactly why **this comparison** exists.

### 🧠 Mental Model

> Jakarta EE is a constitution - many parties agree on the rules, and any vendor can implement them. Spring is a benevolent dictatorship - VMware (now Broadcom) decides fast, ships fast, and the community follows or forks.

**Memory hook:** Jakarta EE = standard by committee. Spring = standard by adoption.

### ⚙️ How it works

1. Jakarta EE defines specifications (JAX-RS, CDI, JPA) that multiple vendors implement.
2. Spring provides its own implementations (Spring MVC, Spring DI, Spring Data JPA) that wrap or replace spec APIs.
3. Jakarta EE requires a certified application server (WildFly, Payara, Open Liberty).
4. Spring Boot embeds the server (Tomcat, Jetty) - no external container needed.
5. In practice, most Spring apps use JPA (a Jakarta spec) underneath Spring Data.

### ✏️ Minimal Example

**BAD:**

```java
// Jakarta EE - requires external server
// with CDI + JAX-RS configured
@Path("/orders")
@RequestScoped
public class OrderResource {
  @Inject OrderService service;
  @GET @Produces(MediaType.APPLICATION_JSON)
  public List<Order> list() {
    return service.findAll();
  }
}
// Deploy as WAR to WildFly/Payara
```

Why it's wrong: not wrong per se, but requires external server setup and WAR packaging.

**GOOD:**

```java
// Spring Boot - self-contained JAR
@RestController
@RequestMapping("/orders")
public class OrderController {
  private final OrderService service;
  OrderController(OrderService svc) {
    this.service = svc;
  }
  @GetMapping
  List<Order> list() {
    return service.findAll();
  }
}
// java -jar app.jar  (server embedded)
```

Why it's right: runs anywhere Java is installed, no external container, constructor injection by default.

### ⚡ When to use / Not to use

**Use when:**

- Choosing Spring: you want fast innovation cycles, large library ecosystem, embedded deployment
- Choosing Jakarta EE: you need vendor portability guarantees or your organization mandates certified servers

**Avoid when:**

- Choosing Jakarta EE purely for "standard" credibility when your team already knows Spring
- Choosing Spring when regulatory requirements mandate certified application server deployments

### ⚠️ One Gotcha

**Misconception:** "Jakarta EE is dead."
**Reality:** Jakarta EE 10+ is actively developed under the Eclipse Foundation with modern features (CDI 4.0, REST improvements). It is smaller than Spring's ecosystem but far from dead - especially in regulated industries.

### 📇 Revision Card

1. Spring moves fast via Broadcom/VMware; Jakarta EE moves carefully via Eclipse Foundation consensus
2. Spring embeds the server; Jakarta EE traditionally deploys to external servers
3. They share JPA, Bean Validation, and JSON-B specs - the divide is governance and velocity, not capability

---

---

# SPR-004 Spring Project Landscape Map

**TL;DR** - Spring has 20+ projects; know the six core ones and add the rest as needed.

### 🟢 What it is

The **Spring Project Landscape Map** is a mental inventory of the major Spring projects, grouped by concern: core (Framework, Boot), data (Data, Batch), web (MVC, WebFlux), security (Security), cloud (Cloud, Cloud Data Flow), and support (Session, AMQP, Kafka, GraphQL).

### 🎯 Why it exists

New Spring developers see a wall of project names and freeze. Which ones matter? Which are optional? Without a map, teams either import everything (bloated classpath, slow startup) or miss a project that already solves their exact problem. Knowing the landscape prevents reinventing the wheel and prevents unnecessary dependencies. This is exactly why **the Spring Project Landscape Map** exists.

### 🧠 Mental Model

> Picture a city map. Downtown (Spring Framework + Boot) is where everyone lives. The neighborhoods around it (Data, Security, Cloud) are where specialists work. The suburbs (AMQP, GraphQL, Vault) are where you go only when your job requires it.

**Memory hook:** Framework = foundation, Boot = builder, everything else = neighborhood you visit when you need it.

### ⚙️ How it works

1. **Spring Framework** - IoC container, AOP, MVC, transaction management. The foundation.
2. **Spring Boot** - Auto-configuration, starters, embedded server, Actuator. The fast lane.
3. **Spring Data** - Repository abstraction over JPA, MongoDB, Redis, Elasticsearch, and more.
4. **Spring Security** - Authentication, authorization, OAuth 2.0, CSRF protection.
5. **Spring Cloud** - Service discovery, config server, circuit breaker, gateway for distributed systems.
6. **Spring Batch** - Chunk-based processing for ETL, reports, data migration at scale.

### ✏️ Minimal Example

**BAD:**

```xml
<!-- Importing every starter "just in case" -->
<dependency>
  <artifactId>spring-boot-starter-web
  </artifactId></dependency>
<dependency>
  <artifactId>spring-boot-starter-data-jpa
  </artifactId></dependency>
<dependency>
  <artifactId>spring-boot-starter-security
  </artifactId></dependency>
<dependency>
  <artifactId>spring-boot-starter-batch
  </artifactId></dependency>
<dependency>
  <artifactId>spring-cloud-starter-gateway
  </artifactId></dependency>
<!-- App is a simple CRUD API -->
```

Why it's wrong: unused starters add classpath bloat, slower startup, and surprise auto-configuration.

**GOOD:**

```xml
<!-- Only what a CRUD API actually needs -->
<dependency>
  <artifactId>spring-boot-starter-web
  </artifactId></dependency>
<dependency>
  <artifactId>spring-boot-starter-data-jpa
  </artifactId></dependency>
```

Why it's right: minimal surface area - add Security or Batch only when the requirement appears.

### ⚡ When to use / Not to use

**Use when:**

- Starting a new project (consult the map to pick only what you need)
- Evaluating whether a custom solution already exists as a Spring project

**Avoid when:**

- Your application is a simple library with no Spring dependency
- You are building for a framework-agnostic open-source library

### ⚠️ One Gotcha

**Misconception:** "You need Spring Cloud for any microservice."
**Reality:** Spring Cloud is for distributed system patterns (service discovery, config server, circuit breakers). A single Spring Boot microservice behind a load balancer does not need Spring Cloud at all.

### 📇 Revision Card

1. Six core projects cover 90% of use cases: Framework, Boot, Data, Security, Cloud, Batch
2. Add starters incrementally - never import what you do not actively use
3. Spring Cloud is for distributed patterns, not a prerequisite for microservices

---

---

# SPR-005 Spring Boot - What Problem It Solves

**TL;DR** - Spring Boot eliminates manual configuration by applying opinionated defaults and auto-configuration.

### 🟢 What it is

**Spring Boot** is an opinionated framework built on Spring Framework that auto-configures beans, embeds a web server, manages dependency versions, and provides production-ready features (health checks, metrics) - so developers focus on business logic instead of infrastructure wiring.

### 🎯 Why it exists

Before Spring Boot, creating a Spring web application meant: choosing compatible library versions, writing dozens of `@Bean` definitions in Java config (or worse, XML), configuring a DataSource, setting up a transaction manager, packaging as a WAR, and deploying to an external Tomcat. A "hello world" REST endpoint required 15-20 minutes of setup. Multiply that across dozens of microservices and the configuration tax became crushing. This is exactly why **Spring Boot** exists.

### 🧠 Mental Model

> Spring Framework gives you every LEGO brick ever made. Spring Boot gives you a pre-assembled kit with instructions - you can swap pieces, but the default build already works.

**Memory hook:** Spring = all the parts. Boot = the assembly instructions with sensible defaults.

### ⚙️ How it works

1. You add a starter (e.g., `spring-boot-starter-web`) to your build file.
2. Boot's auto-configuration scans the classpath for known libraries.
3. For each detected library, it registers beans with sensible defaults (e.g., embedded Tomcat on port 8080).
4. Your `application.properties` overrides any default you dislike.
5. `@SpringBootApplication` triggers component scanning, auto-configuration, and starts the embedded server.

### ✏️ Minimal Example

**BAD:**

```java
// Pre-Boot Spring: manual everything
@Configuration
public class WebConfig {
  @Bean
  public DispatcherServlet dispatcherServlet() {
    return new DispatcherServlet();
  }
  @Bean
  public ServletRegistrationBean<
      DispatcherServlet> registration(
      DispatcherServlet ds) {
    return new ServletRegistrationBean<>(
        ds, "/*");
  }
  // + DataSource, TransactionManager,
  //   EntityManagerFactory...
}
```

Why it's wrong: dozens of beans manually defined for standard behavior.

**GOOD:**

```java
@SpringBootApplication
public class App {
  public static void main(String[] args) {
    SpringApplication.run(App.class, args);
  }
}
// That is it. Tomcat starts on 8080.
```

Why it's right: auto-configuration handles DispatcherServlet, Tomcat, Jackson, and error handling.

### ⚡ When to use / Not to use

**Use when:**

- Building any new Spring-based application (REST API, batch job, event consumer)
- You want embedded deployment (JAR) instead of WAR-to-server

**Avoid when:**

- You need a non-Spring lightweight framework (Micronaut, Quarkus for cold-start-sensitive serverless)
- You are writing a shared library that should not pull in a framework

### ⚠️ One Gotcha

**Misconception:** "Spring Boot hides what is happening - it is magic."
**Reality:** Every auto-configuration class is a regular `@Configuration` with `@ConditionalOn...` annotations. Run with `--debug` to see exactly which configurations activated and which were skipped.

### 📇 Revision Card

1. Boot auto-configures beans by scanning classpath libraries and applying conditional defaults
2. `application.properties` overrides any default - nothing is locked
3. Run with `--debug` to see every auto-configuration decision (activated or skipped)

---

---

# SPR-006 When Spring Is Overkill Anti-Pattern

**TL;DR** - Using Spring for trivial programs adds startup cost, classpath complexity, and cognitive overhead.

### 🟢 What it is

The **When Spring Is Overkill Anti-Pattern** is the mistake of reaching for a full Spring Boot application when the problem requires only a plain Java class, a simple script, or a lightweight library. Adding a framework to a problem that does not need one creates unnecessary complexity.

### 🎯 Why it exists

Spring is so productive for medium-to-large applications that teams start using it for everything: CLI tools, one-off scripts, tiny Lambda functions, pure libraries. The result is a 30MB JAR with 5-second startup for a program that could be 50KB and start instantly. Worse, new team members must understand Spring's DI model to modify a 200-line utility. This is exactly why **recognizing when Spring is overkill** matters.

### 🧠 Mental Model

> You do not drive an 18-wheeler to pick up groceries. A sedan (plain Java) handles the job faster, cheaper, and with easier parking. The truck (Spring Boot) is for when you are hauling freight across the country.

**Memory hook:** If your app has no web layer, no DI graph, and no config management - you do not need Spring.

### ⚙️ How it works

1. Developer creates a Spring Boot project for a small task.
2. Boot pulls in 50+ transitive dependencies.
3. Startup takes 2-5 seconds for JVM + context initialization.
4. The actual logic is 1-2 classes with no dependency injection needs.
5. Maintenance burden: Spring version upgrades, security patches for unused libraries.

### ✏️ Minimal Example

**BAD:**

```java
// Spring Boot app just to read a CSV
@SpringBootApplication
public class CsvParser {
  public static void main(String[] args) {
    SpringApplication.run(
        CsvParser.class, args);
  }
  @Bean CommandLineRunner run() {
    return args -> {
      Files.lines(Path.of("data.csv"))
           .forEach(System.out::println);
    };
  }
}
// 30MB JAR, 3s startup, 50+ deps
```

Why it's wrong: Spring adds zero value here - no DI, no web, no config.

**GOOD:**

```java
// Plain Java - same result
public class CsvParser {
  public static void main(String[] args)
      throws Exception {
    Files.lines(Path.of("data.csv"))
         .forEach(System.out::println);
  }
}
// 5KB class, instant startup, zero deps
```

Why it's right: no framework overhead for a problem that does not need a framework.

### ⚡ When to use / Not to use

**Use when:**

- Evaluating whether a new project genuinely needs dependency injection, web serving, or config management
- Building CLI tools, simple scripts, or pure computation libraries

**Avoid when:**

- The application has multiple collaborating services, external config, or a web layer
- You need Spring's testing, security, or data access integrations

### ⚠️ One Gotcha

**Misconception:** "Starting with Spring Boot is always safe because I might need it later."
**Reality:** Adding Spring later is straightforward (annotate the main class, add a starter). Removing it from a project built on Spring assumptions is much harder. Start light, graduate to Spring when the complexity demands it.

### 📇 Revision Card

1. Spring is overkill when there is no DI graph, no web layer, and no external configuration
2. A Spring Boot JAR pulls 50+ dependencies and adds seconds of startup for the IoC container
3. It is easier to add Spring later than to remove it - start with plain Java and graduate

---

---

# SPR-007 Your First Spring Boot Application (Hands-On)

**TL;DR** - A working Spring Boot app needs one class, one annotation, and one starter dependency.

### 🟢 What it is

**Your First Spring Boot Application** is the minimal project that proves the framework works: a single `@SpringBootApplication` class with one REST endpoint, built and run as a self-contained JAR without any external server.

### 🎯 Why it exists

Every framework has a "hello world" moment where the developer confirms the toolchain works end to end. For Spring Boot, this moment should take under five minutes. If it takes longer, something is wrong with the setup - not the framework. Getting this first win fast builds confidence and reveals the feedback loop (edit, restart, verify) that the developer will use daily. This is exactly why **a hands-on first app** exists.

### 🧠 Mental Model

> Building your first Spring Boot app is like test-driving a car. You do not need to understand the engine to turn the key, press the gas, and confirm it moves. Deeper understanding comes from driving, not from reading the manual.

**Memory hook:** One class, one annotation, one endpoint - that is your proof of life.

### ⚙️ How it works

1. Generate a project at start.spring.io (or via IDE) with `spring-boot-starter-web`.
2. Write a `@SpringBootApplication` main class.
3. Add a `@RestController` with a `@GetMapping` returning a string.
4. Run `mvn spring-boot:run` or `./gradlew bootRun`.
5. Open `http://localhost:8080/hello` and see the response.

### ✏️ Minimal Example

**BAD:**

```java
// Forgetting @SpringBootApplication
// and creating a manual servlet
public class App {
  public static void main(String[] args) {
    // nothing starts - no container,
    // no component scanning
  }
}
```

Why it's wrong: without `@SpringBootApplication`, no auto-configuration, no embedded server, nothing happens.

**GOOD:**

```java
@SpringBootApplication
public class App {
  public static void main(String[] args) {
    SpringApplication.run(App.class, args);
  }
}

@RestController
class HelloController {
  @GetMapping("/hello")
  String hello() {
    return "Spring Boot is running";
  }
}
```

Why it's right: `@SpringBootApplication` triggers component scanning and auto-configuration; `@RestController` registers the endpoint.

### ⚡ When to use / Not to use

**Use when:**

- Learning Spring Boot for the first time (verify your toolchain works)
- Prototyping a new service idea quickly

**Avoid when:**

- You already have a working project template in your organization
- You need to evaluate framework alternatives (build the same app in each)

### ⚠️ One Gotcha

**Misconception:** "The controller must be in the same file as the main class."
**Reality:** The controller can be in any package at or below the main class's package. `@SpringBootApplication` scans its own package and all sub-packages by default.

### 📇 Revision Card

1. `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`
2. The main class's package defines the root of component scanning
3. `spring-boot-starter-web` brings Tomcat, Jackson, and Spring MVC - nothing else needed

---

---

# SPR-008 Inversion of Control (IoC) Container

**TL;DR** - The IoC container creates, wires, and manages object lifecycles so your code never calls `new` on dependencies.

### 🟢 What it is

The **Inversion of Control (IoC) Container** is the heart of the Spring Framework. Instead of your code creating its own dependencies (`new OrderRepository()`), the container creates them, injects them where needed, and manages their lifecycle (creation, initialization, destruction).

### 🎯 Why it exists

When class A creates class B directly, A is tightly coupled to B's concrete implementation. You cannot test A without B. You cannot swap B for a mock or a different implementation without editing A's source code. In a system with hundreds of classes, this creates a rigid dependency graph that resists change. The IoC container breaks this coupling by moving object creation out of business code. This is exactly why **the IoC container** exists.

### 🧠 Mental Model

> Imagine a restaurant. Without IoC, each chef grows their own vegetables, raises their own cattle, and mills their own flour. With IoC, a supply manager (the container) delivers ingredients to each chef's station. Chefs declare what they need - they never source it themselves.

**Memory hook:** "Don't call us, we'll call you" - the Hollywood Principle applied to object creation.

### ⚙️ How it works

1. You define beans (objects the container manages) via annotations or configuration.
2. The container reads these definitions at startup and builds a dependency graph.
3. It creates beans in the correct order (dependencies first).
4. It injects dependencies via constructor, setter, or field injection.
5. It manages the bean's full lifecycle: creation, `@PostConstruct`, use, `@PreDestroy`, destruction.

### ✏️ Minimal Example

**BAD:**

```java
// Tight coupling - OrderService creates its
// own repository
public class OrderService {
  private final OrderRepo repo =
      new JdbcOrderRepo(
          new HikariDataSource());
  // Cannot test without a real database
}
```

Why it's wrong: `OrderService` is permanently bound to `JdbcOrderRepo` and a real DataSource.

**GOOD:**

```java
@Service
public class OrderService {
  private final OrderRepo repo;
  // Container injects the dependency
  OrderService(OrderRepo repo) {
    this.repo = repo;
  }
}
// In tests: new OrderService(mockRepo)
```

Why it's right: `OrderService` depends on an interface, not a concrete class. Testable, swappable, decoupled.

### ⚡ When to use / Not to use

**Use when:**

- Your application has multiple collaborating objects with dependencies between them
- You need testability (mock injection) and configuration flexibility

**Avoid when:**

- The program is a single-class script with no dependencies
- You are writing a library that should not impose a container on consumers

### ⚠️ One Gotcha

**Misconception:** "IoC means Spring creates everything. I cannot use `new` at all."
**Reality:** Use `new` freely for value objects, DTOs, and data structures. IoC manages service-layer objects with dependencies - not every object in your system.

### 📇 Revision Card

1. IoC inverts who creates objects: the container creates and injects, not your business code
2. The benefit is decoupling - classes depend on interfaces, not concrete implementations
3. Use `new` for value objects; use IoC for services with dependencies

---

---

# SPR-009 Dependency Injection - Constructor vs Field vs Setter

**TL;DR** - Constructor injection is the default and best choice; field and setter injection have narrow valid uses.

### 🟢 What it is

**Dependency Injection (DI)** is the mechanism by which the IoC container supplies a bean's dependencies. Spring supports three injection styles: constructor injection (dependencies as constructor parameters), setter injection (`@Autowired` on setters), and field injection (`@Autowired` directly on fields).

### 🎯 Why it exists

The IoC container knows what to inject but needs a delivery mechanism. Constructor injection makes dependencies explicit and enforces immutability. Setter injection allows optional dependencies and reconfiguration. Field injection is the most concise but hides dependencies and prevents compile-time checking. Teams need a clear policy on which style to use and when. This is exactly why **understanding the three DI styles** matters.

### 🧠 Mental Model

> Constructor injection is like a birth certificate - the name is set at creation and cannot change. Setter injection is like a changeable name tag. Field injection is like whispering the name into someone's ear while they sleep - it works, but nobody can verify it happened.

**Memory hook:** Constructor = required + immutable. Setter = optional. Field = hidden.

### ⚙️ How it works

1. **Constructor:** Spring resolves all parameters, calls the constructor once, bean is fully initialized and immutable.
2. **Setter:** Spring creates the bean first (no-arg constructor), then calls each `@Autowired` setter.
3. **Field:** Spring creates the bean, then uses reflection to set private fields directly (bypassing the constructor).

### ✏️ Minimal Example

**BAD:**

```java
@Service
public class OrderService {
  @Autowired
  private OrderRepo repo;  // field injection
  @Autowired
  private PaymentGateway pay; // hidden deps

  // No way to see required deps from outside
  // Cannot create with 'new' in tests
}
```

Why it's wrong: dependencies are invisible, object can exist in an uninitialized state, reflection-dependent.

**GOOD:**

```java
@Service
public class OrderService {
  private final OrderRepo repo;
  private final PaymentGateway pay;

  // constructor injection - explicit, final
  OrderService(OrderRepo repo,
               PaymentGateway pay) {
    this.repo = repo;
    this.pay = pay;
  }
}
// Test: new OrderService(mockRepo, mockPay)
```

Why it's right: dependencies are explicit in the API, `final` guarantees immutability, testable with `new`.

### ⚡ When to use / Not to use

**Use when:**

- Constructor injection: always the default for required dependencies
- Setter injection: genuinely optional dependencies with sensible defaults (rare)

**Avoid when:**

- Field injection: in production code (acceptable only in test classes for brevity)
- Constructor with 7+ parameters (this signals the class has too many responsibilities)

### ⚠️ One Gotcha

**Misconception:** "You must add `@Autowired` on the constructor."
**Reality:** Since Spring 4.3, if a bean has exactly one constructor, Spring uses it automatically - no `@Autowired` needed.

### 📇 Revision Card

1. Constructor injection is the Spring team's recommended default - explicit, immutable, testable
2. Field injection hides dependencies and makes testing without the container impossible
3. Since Spring 4.3, `@Autowired` on a single constructor is optional

---

---

# SPR-010 Spring Bean and Bean Scope

**TL;DR** - A Spring bean is a container-managed object; its scope controls how many instances exist.

### 🟢 What it is

A **Spring Bean** is any object created, configured, and managed by the Spring IoC container. **Bean Scope** determines the lifecycle and sharing: `singleton` (one instance per container - the default), `prototype` (new instance per injection), `request` (one per HTTP request), `session` (one per HTTP session), and `application` (one per `ServletContext`).

### 🎯 Why it exists

Without scope control, every component would be a singleton or every component would be a new instance - neither is universally correct. A `DataSource` should be a singleton (shared connection pool). A shopping cart should be session-scoped (per user). A request-scoped audit context should not leak between HTTP requests. Scoping lets the container match object lifecycle to business requirements. This is exactly why **bean scope** exists.

### 🧠 Mental Model

> Singleton scope is the office coffee machine - everyone shares one. Prototype scope is a paper cup - everyone gets a fresh one. Session scope is a personal desk - yours for the duration of your visit.

**Memory hook:** Default is singleton. If you need a fresh instance, you must explicitly say so.

### ⚙️ How it works

1. Container reads the bean definition and its scope annotation.
2. For `singleton`: creates the instance once at startup, caches it, returns the same instance on every injection.
3. For `prototype`: creates a new instance every time the bean is requested.
4. For `request`/`session`: creates and destroys instances tied to the HTTP lifecycle via a proxy.

### ✏️ Minimal Example

**BAD:**

```java
@Component  // default singleton
public class ShoppingCart {
  private List<Item> items = new ArrayList<>();
  public void add(Item i) { items.add(i); }
}
// All users share one cart - data leaks!
```

Why it's wrong: a singleton shopping cart is shared across all HTTP requests and all users.

**GOOD:**

```java
@Component
@Scope("session")
public class ShoppingCart {
  private List<Item> items = new ArrayList<>();
  public void add(Item i) { items.add(i); }
}
// Each user session gets its own cart
```

Why it's right: session scope creates one cart per user session, matching the business requirement.

### ⚡ When to use / Not to use

**Use when:**

- `singleton`: stateless services, repositories, utility beans (95% of cases)
- `prototype`/`request`/`session`: stateful objects whose lifecycle must match a context boundary

**Avoid when:**

- Using `prototype` for services (you lose container lifecycle management)
- Injecting a prototype bean into a singleton (the prototype is created once and never refreshed)

### ⚠️ One Gotcha

**Misconception:** "Injecting a prototype into a singleton gives me a new prototype each time."
**Reality:** The prototype is resolved once at singleton creation time and cached. Use `ObjectProvider<T>` or `@Lookup` to get a fresh prototype on each call.

### 📇 Revision Card

1. Default scope is singleton - one instance per container, shared everywhere
2. Session and request scopes use proxies to match object lifecycle to HTTP lifecycle
3. Prototype injected into singleton resolves once - use `ObjectProvider<T>` for fresh instances

---

---

# SPR-011 ApplicationContext

**TL;DR** - ApplicationContext is the smart IoC container that manages beans, events, resources, and environment.

### 🟢 What it is

The **ApplicationContext** is Spring's central interface and the advanced IoC container. It extends `BeanFactory` with enterprise features: automatic bean detection via component scanning, event publication, internationalization (i18n), environment abstraction (profiles, properties), and resource loading.

### 🎯 Why it exists

A basic `BeanFactory` can create and inject beans, but real applications need more: they need to publish events between components, load external configuration from files and environment variables, activate different behaviors per environment (dev/staging/prod), and resolve classpath resources. Wrapping all of this into one cohesive interface avoids scattering infrastructure code throughout the application. This is exactly why **ApplicationContext** exists.

### 🧠 Mental Model

> `BeanFactory` is a vending machine - put in a coin, get a product. `ApplicationContext` is a hotel concierge - it stocks the minibar (beans), delivers messages (events), speaks multiple languages (i18n), and adjusts the room settings for each guest (profiles).

**Memory hook:** `BeanFactory` = lazy and minimal. `ApplicationContext` = eager and full-featured.

### ⚙️ How it works

1. `SpringApplication.run()` creates an `ApplicationContext` implementation (typically `AnnotationConfigServletWebServerApplicationContext` for web apps).
2. It scans for `@Component`, `@Configuration`, and `@Bean` definitions.
3. It resolves properties from `application.properties`, environment variables, and command-line arguments.
4. It creates all singleton beans eagerly (unlike `BeanFactory` which is lazy).
5. It publishes `ApplicationStartedEvent`, `ApplicationReadyEvent`, etc. to registered listeners.

### ✏️ Minimal Example

**BAD:**

```java
// Manually creating a BeanFactory
DefaultListableBeanFactory factory =
    new DefaultListableBeanFactory();
factory.registerSingleton(
    "repo", new OrderRepo());
// No scanning, no events, no profiles,
// no property resolution
```

Why it's wrong: bypasses all the enterprise features Spring provides.

**GOOD:**

```java
@SpringBootApplication
public class App {
  public static void main(String[] args) {
    ApplicationContext ctx =
        SpringApplication.run(
            App.class, args);
    // ctx manages beans, events, profiles
    OrderService svc =
        ctx.getBean(OrderService.class);
  }
}
```

Why it's right: `SpringApplication.run` creates a full-featured context with auto-configuration and component scanning.

### ⚡ When to use / Not to use

**Use when:**

- Building any Spring application (it is the default, created automatically by Spring Boot)
- You need event-driven communication between beans

**Avoid when:**

- You need lazy initialization of everything (use `spring.main.lazy-initialization=true` instead of downgrading to `BeanFactory`)
- You are writing framework-agnostic library code

### ⚠️ One Gotcha

**Misconception:** "I should call `ctx.getBean()` whenever I need a dependency."
**Reality:** Calling `getBean()` in business code is the Service Locator anti-pattern. Let the container inject dependencies via constructors. Reserve `getBean()` for framework bootstrapping or dynamic scenarios.

### 📇 Revision Card

1. ApplicationContext = BeanFactory + events + environment + i18n + resource loading
2. Spring Boot creates it automatically - you rarely interact with it directly
3. Calling `getBean()` in business code is an anti-pattern - use constructor injection instead

---

---

# SPR-012 Stereotype Annotations (@Component Family)

**TL;DR** - Stereotype annotations mark classes for container detection and communicate architectural intent.

### 🟢 What it is

**Stereotype Annotations** are Spring's family of class-level markers - `@Component`, `@Service`, `@Repository`, `@Controller`, `@RestController` - that tell the IoC container to auto-detect and register a class as a bean during component scanning. Each carries the same technical effect as `@Component` but communicates a different architectural role.

### 🎯 Why it exists

Without stereotypes, every bean requires a manual `@Bean` method in a configuration class. With hundreds of beans, that configuration file becomes unmanageable. Component scanning with stereotype annotations lets the container find beans automatically. The specializations (`@Service`, `@Repository`, `@Controller`) add semantic meaning: a developer reading `@Repository` immediately knows this class handles data access. This is exactly why **stereotype annotations** exist.

### 🧠 Mental Model

> Stereotype annotations are like job title badges in a company. Everyone is an employee (`@Component`), but your badge says "Engineer" (`@Service`), "Warehouse" (`@Repository`), or "Front Desk" (`@Controller`). The badge gets you into the building (component scanning) and tells people your role.

**Memory hook:** `@Component` = generic. `@Service` = business logic. `@Repository` = data access. `@Controller` = web layer.

### ⚙️ How it works

1. `@SpringBootApplication` includes `@ComponentScan` which scans the base package and sub-packages.
2. Any class annotated with `@Component` (or its specializations) is registered as a bean.
3. `@Repository` adds automatic exception translation (JDBC exceptions become Spring's `DataAccessException`).
4. `@Controller` marks a class as a Spring MVC handler (template rendering). `@RestController` adds `@ResponseBody` to every method.

### ✏️ Minimal Example

**BAD:**

```java
// Using @Component for everything
@Component
public class OrderService { }

@Component
public class OrderRepository { }

@Component
public class OrderController { }
// Works, but hides architectural intent
```

Why it's wrong: technically functional but loses layer semantics. A new developer cannot tell which layer each class belongs to without reading the code.

**GOOD:**

```java
@Service
public class OrderService { }

@Repository
public class OrderRepository { }

@RestController
public class OrderController { }
// Architecture is self-documenting
```

Why it's right: each annotation communicates the class's layer, and `@Repository` enables exception translation.

### ⚡ When to use / Not to use

**Use when:**

- Marking any class that the container should manage (service, repository, controller)
- You want self-documenting architecture via annotation semantics

**Avoid when:**

- Third-party classes you cannot annotate (use `@Bean` in a `@Configuration` class instead)
- Classes that should not be singletons by default (consider `@Scope` or `@Bean` with explicit scope)

### ⚠️ One Gotcha

**Misconception:** "`@Service` adds transactional behavior automatically."
**Reality:** `@Service` has no technical effect beyond `@Component`. Transactions require `@Transactional` explicitly. The annotation is purely a semantic marker.

### 📇 Revision Card

1. All stereotypes do what `@Component` does - register a bean via component scanning
2. Use the right stereotype for the right layer: `@Service`, `@Repository`, `@Controller`
3. Only `@Repository` has extra behavior (exception translation) - the rest are purely semantic

---

---

# SPR-013 Spring Boot Starters

**TL;DR** - Starters are curated dependency bundles that give you a working feature with one line in your build file.

### 🟢 What it is

A **Spring Boot Starter** is a Maven/Gradle dependency that bundles a coherent set of libraries, auto-configuration classes, and transitive dependencies for a specific capability (web, data-jpa, security, test). Adding one starter pulls in everything needed for that feature with tested, compatible versions.

### 🎯 Why it exists

Before starters, adding JPA support meant manually declaring Hibernate, a JDBC driver, HikariCP, Spring ORM, and Spring TX - then hoping the versions were compatible. A version mismatch between Hibernate and Spring ORM could waste hours. Starters eliminate this by bundling known-compatible versions managed by Spring Boot's parent BOM. This is exactly why **Spring Boot Starters** exist.

### 🧠 Mental Model

> A starter is like a meal kit delivered to your door. Instead of shopping for 15 ingredients and hoping they combine into a dish, you get a tested recipe with pre-measured, compatible ingredients.

**Memory hook:** One starter = one feature = all compatible dependencies.

### ⚙️ How it works

1. You add `spring-boot-starter-data-jpa` to your build file.
2. Maven/Gradle resolves the starter POM which declares transitive dependencies: Hibernate, HikariCP, Spring Data JPA, Spring TX.
3. All versions are managed by `spring-boot-dependencies` BOM (Bill of Materials).
4. Boot's auto-configuration detects these libraries on the classpath and configures them.
5. You write zero infrastructure code - just a repository interface and an `application.properties` with the database URL.

### ✏️ Minimal Example

**BAD:**

```xml
<!-- Manual: 5 dependencies, 5 versions -->
<dependency>
  <groupId>org.hibernate.orm</groupId>
  <artifactId>hibernate-core</artifactId>
  <version>6.4.4</version>
</dependency>
<dependency>
  <groupId>com.zaxxer</groupId>
  <artifactId>HikariCP</artifactId>
  <version>5.1.0</version>
</dependency>
<!-- + spring-orm, spring-tx, JDBC driver -->
```

Why it's wrong: manual version coordination, easy to create incompatible combinations.

**GOOD:**

```xml
<!-- One starter, zero version declarations -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>
    spring-boot-starter-data-jpa
  </artifactId>
</dependency>
```

Why it's right: BOM manages all versions; auto-configuration wires the DataSource, EntityManager, and TransactionManager.

### ⚡ When to use / Not to use

**Use when:**

- Adding any standard capability to a Spring Boot project (web, data, security, test)
- You want guaranteed version compatibility without manual management

**Avoid when:**

- You need a specific older version of a library that conflicts with Boot's BOM (override carefully)
- Building a library that should not pull in Spring Boot's opinionated stack

### ⚠️ One Gotcha

**Misconception:** "Starters contain application code I need to understand."
**Reality:** Starters contain only dependency declarations and auto-configuration metadata. They are POMs (or Gradle modules) with no business logic. The actual code lives in the libraries they pull in.

### 📇 Revision Card

1. Starters are dependency bundles - one line gives you a tested, compatible feature set
2. The BOM (`spring-boot-dependencies`) manages all transitive versions
3. Starters contain no code - just dependency declarations and auto-configuration triggers

---

---

# SPR-014 application.properties and application.yml

**TL;DR** - Spring Boot's externalized config files let you change behavior without recompiling code.

### 🟢 What it is

**application.properties** (or **application.yml**) is Spring Boot's primary externalized configuration file, placed in `src/main/resources`. It configures server ports, database URLs, logging levels, feature flags, and any custom property - all read at startup and injectable into beans via `@Value` or `@ConfigurationProperties`.

### 🎯 Why it exists

Hardcoding a database URL or server port in Java source means recompiling to change environments. Environment-specific behavior (dev vs staging vs prod) should never require code changes. Externalized configuration separates what changes between environments from what stays constant. This is exactly why **application.properties** exists - it is Spring Boot's primary knob panel.

### 🧠 Mental Model

> `application.properties` is the dashboard of your car. You adjust the mirrors, seat, and climate without opening the hood. The engine (your code) stays untouched - only the settings change.

**Memory hook:** Code defines behavior. Properties configure behavior.

### ⚙️ How it works

1. Spring Boot loads `application.properties` (or `.yml`) from `src/main/resources` at startup.
2. Properties override auto-configuration defaults (e.g., `server.port=9090`).
3. Profile-specific files (`application-dev.properties`) override base properties when the profile is active.
4. Environment variables and command-line arguments override file properties (highest precedence).
5. `@Value("${server.port}")` or `@ConfigurationProperties` injects values into beans.

### ✏️ Minimal Example

**BAD:**

```java
@RestController
public class DbController {
  // Hardcoded - cannot change per env
  String url = "jdbc:postgresql://prod:5432/db";
}
```

Why it's wrong: the production URL is baked into the class file. Changing it requires recompilation and redeployment.

**GOOD:**

```properties
# application.properties
spring.datasource.url=\
  jdbc:postgresql://localhost:5432/dev
server.port=8081
logging.level.root=INFO
```

```java
// No hardcoded values in code
@Value("${spring.datasource.url}")
private String dbUrl;
```

Why it's right: change the URL per environment without touching code. Override with `--spring.datasource.url=...` at runtime.

### ⚡ When to use / Not to use

**Use when:**

- Configuring anything that changes between environments (URLs, ports, credentials, feature flags)
- You prefer YAML's nested structure (use `application.yml`) or flat key-value (use `.properties`)

**Avoid when:**

- Storing secrets in plain text (use environment variables, Vault, or Spring Cloud Config instead)
- Defining behavior that belongs in code (business rules are not configuration)

### ⚠️ One Gotcha

**Misconception:** "YAML is better than properties."
**Reality:** Both are functionally equivalent. YAML is easier to read for deeply nested config. Properties are simpler for flat keys. Pick one per project and be consistent - mixing both in the same project causes confusion.

### 📇 Revision Card

1. application.properties externalizes config so environment changes never require recompilation
2. Precedence: command-line > env vars > profile-specific file > base file > defaults
3. Never store secrets in properties files - use environment variables or a secrets manager

---

---

# SPR-015 Spring Boot Auto-Configuration Basics

**TL;DR** - Auto-configuration registers beans automatically based on classpath contents and conditional annotations.

### 🟢 What it is

**Spring Boot Auto-Configuration** is the mechanism that detects libraries on your classpath and automatically configures beans for them. If `HikariCP` is present, Boot creates a `DataSource`. If `Jackson` is present, Boot configures JSON serialization. Each auto-configuration class is a standard `@Configuration` guarded by `@ConditionalOn...` annotations.

### 🎯 Why it exists

Without auto-configuration, every Spring application would need explicit `@Bean` definitions for DataSource, EntityManagerFactory, RestTemplate, Jackson ObjectMapper, and dozens of other infrastructure objects. This boilerplate is identical across projects. Auto-configuration eliminates it by applying sensible defaults that you can override with properties or your own `@Bean` definitions. This is exactly why **auto-configuration** exists.

### 🧠 Mental Model

> Auto-configuration is a smart butler. When you bring home groceries (add a library to classpath), the butler unpacks them, puts them in the right cupboard (registers beans), and sets the table (wires dependencies). If you already set the table yourself (`@Bean`), the butler steps back.

**Memory hook:** Library on classpath + no user bean = auto-configured. User bean present = auto-config backs off.

### ⚙️ How it works

1. `@EnableAutoConfiguration` (included in `@SpringBootApplication`) triggers the mechanism.
2. Spring reads `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` to find candidate classes.
3. Each candidate is a `@Configuration` class with `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, etc.
4. If conditions pass, the configuration's `@Bean` methods execute. If a condition fails, the class is skipped entirely.
5. Run with `--debug` to see the auto-configuration report showing every positive and negative match.

### ✏️ Minimal Example

**BAD:**

```java
// Manually configuring what Boot does
// automatically
@Configuration
public class JacksonConfig {
  @Bean
  public ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(
            new JavaTimeModule());
  }
}
// Redundant - Boot already does this
```

Why it's wrong: Boot auto-configures `ObjectMapper` with `JavaTimeModule` if Jackson is on the classpath. This duplicates effort and may conflict.

**GOOD:**

```properties
# Override just the part you want to change
spring.jackson.serialization.\
  write-dates-as-timestamps=false
spring.jackson.default-property-inclusion=\
  non_null
```

Why it's right: use properties to tune the auto-configured bean rather than replacing it entirely.

### ⚡ When to use / Not to use

**Use when:**

- Starting any Spring Boot application (it is on by default)
- You want sensible defaults without manual configuration

**Avoid when:**

- You need full control over a bean's creation (define your own `@Bean` - auto-config backs off)
- You want to exclude specific auto-configurations (`@SpringBootApplication(exclude = ...)`)

### ⚠️ One Gotcha

**Misconception:** "Auto-configuration is magic I cannot debug."
**Reality:** Run `--debug` and read the CONDITIONS EVALUATION REPORT. Every positive match and every negative match is printed with the exact condition that passed or failed.

### 📇 Revision Card

1. Auto-configuration = `@Configuration` + `@ConditionalOn...` annotations applied to classpath-detected libraries
2. Define your own `@Bean` to override any auto-configured bean (`@ConditionalOnMissingBean` backs off)
3. `--debug` prints the full conditions evaluation report showing every auto-config decision

---

---

# SPR-016 Embedded Server (Tomcat, Jetty, Netty)

**TL;DR** - Spring Boot embeds the web server inside your JAR so deployment is just `java -jar app.jar`.

### 🟢 What it is

An **Embedded Server** in Spring Boot is a web server (Tomcat, Jetty, or Netty) that runs inside your application process. Instead of packaging a WAR and deploying it to an external server, you build a fat JAR containing both your code and the server. `spring-boot-starter-web` brings Tomcat by default; swapping to Jetty or Netty requires a dependency exclusion and a different starter.

### 🎯 Why it exists

Traditional deployment meant installing Tomcat on a server, configuring it separately, then deploying WARs. This created two independently versioned, independently configured artifacts that had to stay in sync. Containers and cloud platforms expect a single self-contained process. An embedded server makes your application the deployment unit - no external server to install, configure, or version-manage. This is exactly why **embedded servers** exist in Spring Boot.

### 🧠 Mental Model

> Traditional deployment: you ship a painting (WAR) and the museum (Tomcat) hangs it. Embedded: you ship a framed painting with its own display stand - it works anywhere you place it.

**Memory hook:** WAR deployment = "install server, then deploy." Embedded = "just run the JAR."

### ⚙️ How it works

1. `spring-boot-starter-web` includes `spring-boot-starter-tomcat` (embedded Tomcat).
2. At startup, `ServletWebServerFactory` creates an embedded Tomcat instance.
3. Spring registers `DispatcherServlet` into the embedded server programmatically.
4. The server binds to `server.port` (default 8080) and starts accepting requests.
5. `spring-boot-starter-webflux` uses Netty (reactive, non-blocking) instead of Tomcat.

### ✏️ Minimal Example

**BAD:**

```xml
<!-- Packaging as WAR for external Tomcat -->
<packaging>war</packaging>
<!-- Requires: install Tomcat, configure
     server.xml, deploy WAR to webapps/ -->
```

Why it's wrong: two deployment artifacts, external server management, harder containerization.

**GOOD:**

```xml
<!-- Default: executable JAR with embedded
     Tomcat -->
<packaging>jar</packaging>
<!-- Run: java -jar target/app.jar -->
```

```properties
# Tune the embedded server via properties
server.port=9090
server.tomcat.threads.max=200
```

Why it's right: single artifact, single command to run, configurable via properties.

### ⚡ When to use / Not to use

**Use when:**

- Building microservices, containerized apps, or any cloud-native deployment
- You want a single self-contained deployable artifact

**Avoid when:**

- Your organization mandates a shared, centrally managed Tomcat (WAR deployment still supported via `SpringBootServletInitializer`)
- You need features only available in a full Tomcat installation (rare)

### ⚠️ One Gotcha

**Misconception:** "Embedded Tomcat is a toy server - not production-grade."
**Reality:** Embedded Tomcat is the exact same Tomcat codebase as standalone Tomcat. Netflix, Uber, and most Spring Boot shops run embedded Tomcat in production at massive scale.

### 📇 Revision Card

1. `spring-boot-starter-web` = embedded Tomcat; swap to Jetty/Netty via dependency exclusion
2. Embedded server makes your JAR the deployment unit - no external server to manage
3. Embedded Tomcat is the same codebase as standalone Tomcat - fully production-grade

---

---

# SPR-017 Spring Initializr (start.spring.io)

**TL;DR** - Spring Initializr generates a ready-to-run project skeleton with your chosen dependencies in seconds.

### 🟢 What it is

**Spring Initializr** (at start.spring.io) is a web tool and API that generates Spring Boot project skeletons. You select a build tool (Maven/Gradle), language (Java/Kotlin/Groovy), Spring Boot version, and dependencies (starters), then download a ZIP with a buildable, runnable project structure.

### 🎯 Why it exists

Manually creating a Spring Boot project from scratch requires writing a `pom.xml` (or `build.gradle`), directory structure, main class, properties file, and test class. Getting the parent BOM version, dependency coordinates, and directory layout right is tedious and error-prone - especially for beginners. Initializr automates the entire scaffolding step. This is exactly why **Spring Initializr** exists.

### 🧠 Mental Model

> Initializr is a project vending machine. Insert your requirements (Java 21, web, JPA, security), press the button, and out comes a fully structured project with the correct build file, directory layout, and main class.

**Memory hook:** start.spring.io = new project in 30 seconds.

### ⚙️ How it works

1. Visit start.spring.io or use the IDE plugin (IntelliJ, VS Code).
2. Choose metadata: group, artifact, name, Java version.
3. Select starters (web, data-jpa, security, actuator, etc.).
4. Click Generate - Initializr produces a ZIP with `pom.xml`/`build.gradle`, `src/main/java`, `src/main/resources/application.properties`, and a test file.
5. Unzip, open in IDE, run `mvn spring-boot:run`.

### ✏️ Minimal Example

**BAD:**

```xml
<!-- Hand-written pom.xml with typos -->
<parent>
  <groupId>org.springframwork.boot</groupId>
  <!-- typo: springframwork -->
  <artifactId>spring-boot-starter-parent
  </artifactId>
  <version>3.2.5</version>
</parent>
```

Why it's wrong: manual pom.xml writing invites typos, wrong versions, and missing plugins.

**GOOD:**

```bash
# CLI equivalent of start.spring.io
curl https://start.spring.io/starter.zip \
  -d dependencies=web,data-jpa \
  -d javaVersion=21 \
  -d type=maven-project \
  -o my-app.zip
unzip my-app.zip
```

Why it's right: zero typos, correct BOM version, proper directory structure, ready to run.

### ⚡ When to use / Not to use

**Use when:**

- Starting any new Spring Boot project (always)
- You want to quickly prototype with specific starters

**Avoid when:**

- Your organization has a custom project template/archetype (use that instead)
- You are adding features to an existing project (add starters to the existing build file)

### ⚠️ One Gotcha

**Misconception:** "I must use the web UI."
**Reality:** Initializr has a REST API, a CLI (`spring init`), and IDE integrations (IntelliJ new project wizard, VS Code Spring Boot extension). The web UI is just one entry point.

### 📇 Revision Card

1. start.spring.io generates a correct, buildable project skeleton in seconds
2. Available via web UI, REST API, CLI, and IDE plugins
3. Use it for every new project - never hand-write the initial build file

---

---

# SPR-018 "Spring Does Magic" is Wrong - Convention over Configuration

**TL;DR** - Spring Boot is not magic; it applies convention over configuration with fully debuggable conditionals.

### 🟢 What it is

**"Spring Does Magic" is Wrong** is a misconception-busting keyword. Developers who see beans appear without explicit wiring assume Spring is opaque. In reality, Spring Boot applies **convention over configuration**: it uses `@ConditionalOn...` annotations to make predictable decisions, and every decision is visible in the auto-configuration report.

### 🎯 Why it exists

When developers cannot explain where a bean came from, they lose confidence and debugging ability. "It just works" is fine until it stops working - then "magic" becomes terror. Understanding that every auto-configured bean is a regular `@Configuration` class with documented conditions restores control. This is exactly why **debunking the magic narrative** matters.

### 🧠 Mental Model

> Spring Boot is not a magician pulling rabbits from a hat. It is an efficient assistant following a checklist: "If library X is on the classpath AND no user bean exists AND property Y is not false - then configure bean Z." Every step is logged.

**Memory hook:** No magic - just conditionals. Run `--debug` and the "magic" reveals itself.

### ⚙️ How it works

1. Boot reads auto-configuration classes listed in `AutoConfiguration.imports`.
2. Each class is guarded by `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`.
3. If all conditions pass, the `@Bean` methods run. If any condition fails, the entire class is skipped.
4. The `CONDITIONS EVALUATION REPORT` (activated by `--debug`) lists every positive and negative match.
5. You can read the source of any auto-configuration class - they are regular Spring code.

### ✏️ Minimal Example

**BAD:**

```java
// "I don't know where this DataSource
//  came from"
@Autowired DataSource ds;
// Developer cannot debug connection issues
// because they don't know who configured it
```

Why it's wrong: ignorance of auto-configuration leads to helplessness when things break.

**GOOD:**

```bash
# Run with --debug to see the truth
java -jar app.jar --debug
# Output includes:
# DataSourceAutoConfiguration matched:
#   - @ConditionalOnClass found
#     javax.sql.DataSource
#   - @ConditionalOnMissingBean did not
#     find DataSource bean
```

Why it's right: the report shows exactly which class configured the DataSource and which conditions were met.

### ⚡ When to use / Not to use

**Use when:**

- Debugging unexpected bean creation or missing beans
- Onboarding new team members who are confused by auto-configuration

**Avoid when:**

- You have already memorized the common auto-configuration classes (but `--debug` remains useful for edge cases)
- The issue is in your own explicit configuration, not auto-configuration

### ⚠️ One Gotcha

**Misconception:** "I need to read Spring Boot source code to understand auto-configuration."
**Reality:** `--debug` gives you the answers without reading source. For deeper understanding, the auto-configuration classes are well-documented and typically short (50-100 lines each).

### 📇 Revision Card

1. Every auto-configured bean is a `@Configuration` class with `@ConditionalOn...` guards
2. `--debug` prints the CONDITIONS EVALUATION REPORT - positive and negative matches
3. Convention over configuration means predictable defaults, not hidden behavior

---

---

# SPR-019 Hardcoded Configuration Anti-Pattern

**TL;DR** - Hardcoding configuration values in source code prevents environment portability and forces redeployment for changes.

### 🟢 What it is

The **Hardcoded Configuration Anti-Pattern** is embedding environment-specific values (database URLs, API keys, port numbers, feature flags) directly in Java source code instead of externalizing them in properties files, environment variables, or a configuration server.

### 🎯 Why it exists

Hardcoding is the fastest way to make something work locally. But the moment the same code must run in staging or production with different database URLs, timeouts, or feature flags, hardcoded values force recompilation. In CI/CD pipelines, this means separate builds per environment - breaking the "build once, deploy anywhere" principle. This is exactly why **avoiding hardcoded configuration** is non-negotiable in production systems.

### 🧠 Mental Model

> Hardcoding configuration is like printing your home address on your business card as the meeting location. When you move offices, every card must be reprinted. Externalized config is like putting "see calendar invite for location" - the card never changes, only the meeting invite does.

**Memory hook:** If changing a value requires recompiling Java, it is hardcoded and wrong.

### ⚙️ How it works

1. Developer writes `String url = "jdbc:postgresql://prod:5432/db"` in a service class.
2. The code compiles fine and works in production.
3. A new staging environment needs a different URL.
4. Developer must edit the source, recompile, and redeploy - or maintain a branch per environment.
5. The correct approach: move the value to `application.properties` and inject with `@Value`.

### ✏️ Minimal Example

**BAD:**

```java
@Service
public class NotificationService {
  // Hardcoded - changes need recompile
  private String apiUrl =
      "https://api.prod.notify.com/v2";
  private int timeoutMs = 5000;
  private boolean enabled = true;
}
```

Why it's wrong: three values that will differ across environments, all requiring recompilation to change.

**GOOD:**

```java
@Service
public class NotificationService {
  @Value("${notification.api.url}")
  private String apiUrl;
  @Value("${notification.timeout-ms:5000}")
  private int timeoutMs;
  @Value("${notification.enabled:true}")
  private boolean enabled;
}
```

```properties
# application-prod.properties
notification.api.url=\
  https://api.prod.notify.com/v2
notification.timeout-ms=3000
```

Why it's right: values externalized, defaults provided with `:`, overridable per environment.

### ⚡ When to use / Not to use

**Use when:**

- Any value that differs between dev, staging, and production environments
- Feature flags, timeouts, URLs, rate limits, retry counts

**Avoid when:**

- True constants that are invariant across all environments (e.g., `Math.PI`)
- Internal algorithm parameters that are not configurable by operators

### ⚠️ One Gotcha

**Misconception:** "Using `@Value` everywhere is fine."
**Reality:** For more than 2-3 related properties, use `@ConfigurationProperties` with a typed POJO. It gives you type safety, validation, IDE auto-completion, and documentation - `@Value` strings give you none of that.

### 📇 Revision Card

1. Anything that changes per environment must be externalized - never compiled into the JAR
2. Use `@Value("${key:default}")` for simple cases, `@ConfigurationProperties` for groups
3. "Build once, deploy anywhere" is impossible with hardcoded configuration

---

---

# SPR-020 Top 10 Spring Interview Questions (Basics)

**TL;DR** - Master these ten foundational Spring concepts and you will answer most junior-level interview questions.

### 🟢 What it is

**Top 10 Spring Interview Questions** is a curated set of the most frequently asked Spring questions at the junior-to-mid level: IoC, DI injection styles, bean scopes, auto-configuration, `@SpringBootApplication`, stereotype annotations, profiles, `application.properties` precedence, starters, and the difference between Spring and Spring Boot.

### 🎯 Why it exists

Spring interviews follow predictable patterns. Interviewers probe whether candidates understand the framework's foundations - not just how to use it, but why it works the way it does. Knowing these ten concepts deeply covers roughly 80% of basic Spring interview territory. This is exactly why **a focused interview question set** exists.

### 🧠 Mental Model

> Think of Spring interview prep as learning the ten most common traffic signs before a driving test. You might encounter unusual signs, but knowing these ten means you will not fail the basics.

**Memory hook:** IoC, DI, scopes, auto-config, stereotypes, profiles, properties, starters, Boot vs Framework, `@SpringBootApplication`.

### ⚙️ How it works

1. **What is IoC?** The container manages object creation (SPR-008).
2. **Constructor vs field injection?** Constructor is preferred - immutable, testable (SPR-009).
3. **What are bean scopes?** singleton (default), prototype, request, session (SPR-010).
4. **How does auto-configuration work?** `@ConditionalOn...` classes triggered by classpath (SPR-015).
5. **What does `@SpringBootApplication` do?** Combines `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan` (SPR-007).

### ✏️ Minimal Example

**BAD:**

```text
Q: What is Spring IoC?
A: "Spring manages objects for you."
// Too vague - shows no understanding
```

Why it's wrong: no mechanism, no why, no contrast with the alternative.

**GOOD:**

```text
Q: What is Spring IoC?
A: "Instead of classes creating their
   own dependencies with 'new', the
   IoC container creates them and
   injects them via constructors. This
   decouples classes from concrete
   implementations, making them testable
   and swappable."
```

Why it's right: explains what, how, and why in four sentences.

### ⚡ When to use / Not to use

**Use when:**

- Preparing for a Spring-focused technical interview
- Reviewing foundational Spring knowledge before learning advanced topics

**Avoid when:**

- Interviewing for a staff/principal role (deeper topics expected: AOP, proxy mechanism, custom auto-configuration)
- You already have extensive Spring production experience

### ⚠️ One Gotcha

**Misconception:** "Memorizing definitions is enough for Spring interviews."
**Reality:** Good interviewers follow up with "why" and "when not to." Knowing that constructor injection is preferred is insufficient - you must explain why (immutability, testability, fail-fast on missing deps).

### 📇 Revision Card

1. Ten core concepts cover 80% of basic Spring interview questions
2. Always explain WHY, not just WHAT - interviewers test understanding depth
3. Each concept maps to a specific SPR keyword in this topic for deeper study

---

---

# SPR-021 Spring Boot DevTools and Live Reload

**TL;DR** - DevTools accelerates development by auto-restarting the application and refreshing the browser on code changes.

### 🟢 What it is

**Spring Boot DevTools** is a development-time module that provides automatic application restart on classpath changes, LiveReload browser integration, sensible development defaults (disabled caching, verbose logging), and remote debugging support. It is automatically disabled in production JARs.

### 🎯 Why it exists

Without DevTools, every code change requires manually stopping the app, rebuilding, and restarting - a cycle that typically takes 5-15 seconds for small apps and longer for large ones. DevTools cuts this to 1-3 seconds by using two classloaders: a base classloader (libraries, unchanged) and a restart classloader (your code, reloaded). The browser auto-refreshes via LiveReload. This is exactly why **DevTools** exists.

### 🧠 Mental Model

> DevTools is a hot-swap pit crew. When you change a tire (your code), the crew swaps only that tire and sends the car back on track. Without DevTools, you tow the entire car back to the garage and rebuild it.

**Memory hook:** DevTools = fast restart via two classloaders + automatic browser refresh.

### ⚙️ How it works

1. Add `spring-boot-devtools` as a development dependency.
2. When you save a file, the IDE recompiles the class.
3. DevTools detects the classpath change and restarts only the restart classloader (your classes).
4. The base classloader (third-party JARs) stays loaded - this makes restart faster.
5. LiveReload triggers the browser to refresh automatically.

### ✏️ Minimal Example

**BAD:**

```xml
<!-- DevTools in production -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-devtools</artifactId>
  <!-- No scope - included in prod JAR -->
</dependency>
```

Why it's wrong: DevTools in production causes unexpected restarts and security risks.

**GOOD:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-devtools</artifactId>
  <scope>runtime</scope>
  <optional>true</optional>
</dependency>
<!-- Auto-disabled in packaged JARs -->
```

Why it's right: `optional=true` prevents transitive inclusion. Boot automatically disables DevTools when running from a packaged JAR.

### ⚡ When to use / Not to use

**Use when:**

- Active development with frequent code-test cycles
- You want browser auto-refresh during UI or API development

**Avoid when:**

- Production deployment (it auto-disables, but verify)
- You use JRebel or DCEVM for true hot-swap without restart

### ⚠️ One Gotcha

**Misconception:** "DevTools does hot-swap like JRebel."
**Reality:** DevTools does a fast restart (kills and recreates the restart classloader). It is not true hot-swap. Structural changes (new methods, changed signatures) trigger a full restart, while JRebel can handle them without restart.

### 📇 Revision Card

1. DevTools uses two classloaders: base (libraries) stays loaded, restart (your code) reloads
2. Automatically disabled in production JARs - safe to leave in the build file
3. Not true hot-swap - it is a fast restart (1-3s vs 5-15s without DevTools)

---

---

# SPR-022 REST API Phase 1 - Spring Boot CRUD

**TL;DR** - Build a complete CRUD REST API with `@RestController`, `@GetMapping`, and response DTOs in under 50 lines.

### 🟢 What it is

**REST API Phase 1** is the hands-on exercise of building a basic CRUD (Create, Read, Update, Delete) REST API using Spring Boot. It covers `@RestController`, HTTP method mappings (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`), path variables, request bodies, and proper HTTP status codes.

### 🎯 Why it exists

REST APIs are the most common output of Spring Boot applications. Every Spring developer must know how to expose CRUD endpoints, map HTTP verbs to methods, parse path variables and request bodies, and return appropriate status codes. This exercise builds that muscle memory with a concrete working example. This is exactly why **a CRUD exercise** exists.

### 🧠 Mental Model

> A REST controller is a switchboard operator. HTTP requests arrive with a verb (GET/POST/PUT/DELETE) and a path (/orders/42). The operator routes each request to the right handler method and sends back the response.

**Memory hook:** `@RestController` = `@Controller` + `@ResponseBody` on every method.

### ⚙️ How it works

1. `@RestController` marks the class as a REST endpoint handler.
2. `@RequestMapping("/api/orders")` sets the base path.
3. `@GetMapping("/{id}")` maps `GET /api/orders/42` to a method with `@PathVariable`.
4. `@PostMapping` maps `POST /api/orders` with `@RequestBody` for the JSON payload.
5. Return `ResponseEntity<T>` to control the HTTP status code (201 Created, 204 No Content, etc.).

### ✏️ Minimal Example

**BAD:**

```java
@RestController
public class OrderController {
  @GetMapping("/orders")
  // Returns void, no status control
  void getOrder() {
    System.out.println("order");
  }
}
```

Why it's wrong: returns nothing to the client, prints to console instead of responding, no status code control.

**GOOD:**

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
  private final OrderService svc;
  OrderController(OrderService svc) {
    this.svc = svc;
  }

  @GetMapping("/{id}")
  ResponseEntity<Order> get(
      @PathVariable Long id) {
    return svc.find(id)
        .map(ResponseEntity::ok)
        .orElse(ResponseEntity
            .notFound().build());
  }

  @PostMapping
  ResponseEntity<Order> create(
      @RequestBody Order order) {
    Order saved = svc.save(order);
    return ResponseEntity
        .status(HttpStatus.CREATED)
        .body(saved);
  }
}
```

Why it's right: proper HTTP verbs, path variables, status codes (200/201/404), constructor injection.

### ⚡ When to use / Not to use

**Use when:**

- Building any HTTP API with Spring Boot
- Learning the request-response cycle of Spring MVC

**Avoid when:**

- You need GraphQL or gRPC (different Spring modules)
- The endpoint is a server-side rendered HTML page (`@Controller` with Thymeleaf instead)

### ⚠️ One Gotcha

**Misconception:** "`@GetMapping` and `@RequestMapping(method = GET)` are different."
**Reality:** `@GetMapping` is a composed annotation that is exactly equivalent to `@RequestMapping(method = RequestMethod.GET)`. It is syntactic sugar, nothing more.

### 📇 Revision Card

1. `@RestController` = `@Controller` + `@ResponseBody` - returns JSON/XML directly, not view names
2. Use `ResponseEntity<T>` to control HTTP status codes explicitly
3. `@GetMapping("/{id}")` + `@PathVariable` extracts path segments into method parameters

---

---

# SPR-023 Spring Boot Project Setup Exercise

**TL;DR** - Verify your Spring Boot toolchain by generating, building, running, and testing a minimal project end to end.

### 🟢 What it is

The **Spring Boot Project Setup Exercise** is a structured checklist that validates your development environment works correctly: JDK version, build tool (Maven/Gradle), IDE configuration, project generation via Initializr, successful build, application startup, endpoint test with curl/browser, and test execution.

### 🎯 Why it exists

Toolchain problems discovered mid-project are costly and demoralizing. A developer who cannot generate, build, and run a Spring Boot app has a setup issue that will block all further learning. This exercise catches those issues in five minutes rather than after hours of debugging. This is exactly why **a setup exercise** exists at the start of every Spring learning path.

### 🧠 Mental Model

> This exercise is a preflight checklist. Pilots do not skip checks because they have flown before. Running this checklist confirms JDK, build tool, IDE, and network access are all working before you begin real development.

**Memory hook:** Generate, build, run, test - four steps to prove your setup works.

### ⚙️ How it works

1. **Generate:** go to start.spring.io, select Java 21, Spring Boot 3.x, add `spring-boot-starter-web`. Download.
2. **Build:** `mvn clean package` (or `./gradlew build`). Verify BUILD SUCCESS.
3. **Run:** `java -jar target/app.jar`. Verify "Started Application in X seconds" in console.
4. **Test:** `curl http://localhost:8080` (should return the default error page or your endpoint).
5. **Unit test:** `mvn test` runs the auto-generated `@SpringBootTest` context load test.

### ✏️ Minimal Example

**BAD:**

```bash
# Skipping verification
mvn spring-boot:run
# "It started? Good enough."
# No test run, no JAR packaging verified
```

Why it's wrong: partial verification misses packaging issues, test classpath problems, or port conflicts.

**GOOD:**

```bash
# Full verification pipeline
mvn clean package
java -jar target/demo-0.0.1-SNAPSHOT.jar &
sleep 5
curl -s http://localhost:8080/hello
# Expect: "Spring Boot is running"
kill %1
mvn test
# Expect: BUILD SUCCESS, all tests pass
```

Why it's right: validates build, package, run, endpoint, and test execution end to end.

### ⚡ When to use / Not to use

**Use when:**

- Setting up Spring Boot for the first time on a new machine
- After upgrading JDK, Maven/Gradle, or IDE versions

**Avoid when:**

- You have a CI pipeline that validates this on every commit (but still useful for local dev changes)
- You are working in an existing, proven project

### ⚠️ One Gotcha

**Misconception:** "If `mvn spring-boot:run` works, my setup is fine."
**Reality:** `spring-boot:run` uses the Maven classloader, not the packaged JAR. Issues with fat-JAR packaging, missing resources, or classpath conflicts only surface when you run `java -jar`. Always test the packaged JAR.

### 📇 Revision Card

1. Four steps: generate (Initializr), build (mvn package), run (java -jar), test (mvn test)
2. Always test the packaged JAR, not just `spring-boot:run` - packaging issues hide otherwise
3. A failing setup exercise saves hours of debugging later - never skip it
