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

| Topic            | Folder            | Dictionary Sources | Status  | Description                                                                   |
| ---------------- | ----------------- | ------------------ | ------- | ----------------------------------------------------------------------------- |
| Java             | java/             | JVM, JLG           | planned | Core Java language, OOP, collections, modern Java features, JVM internals, GC |
| Java Concurrency | java-concurrency/ | JCC                | planned | Threading, synchronization, virtual threads, concurrent collections           |

---

## Sub-topic File Mapping

Each topic is split into sub-topic files. Each file MUST contain at
least 5 related keywords (no per-keyword files). Files are grouped by
relatedness and must be self-sufficient.

### Java (java/)

### Java Concurrency (java-concurrency/)

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
