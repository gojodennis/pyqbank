---
description: Solve NEET/JEE exam preparation inefficiencies by delivering a data-driven, targeted practice platform that identifies knowledge gaps, personalizes question selection, and provides intelligent feedback—eliminating reliance on multiple textbooks and unfocused study patterns.
---

# Product Requirements Document
## PYQ Question Bank with Smart Search

---

## 1. Executive Summary

**Product Name:** PYQ Question Bank with Smart Search

**Vision:** Solve NEET/JEE exam preparation inefficiencies by delivering a data-driven, targeted practice platform that identifies knowledge gaps, personalizes question selection, and provides intelligent feedback—eliminating reliance on multiple textbooks and unfocused study patterns.

**Target Users:** NEET/JEE aspirants (India, competitive exam prep market)

**Success Metric:** 40% improvement in weak topic accuracy within 60 days of active use

---

## 2. Problem Statement

### Current Pain Points
- **Information Overload:** Students buy 5+ books but practice randomly without structured progression
- **Gap Identification:** No easy way to identify NCERT gaps or weak topics until mock exams
- **Inefficient Practice:** Generic question papers don't adapt to individual weak areas
- **Lack of Feedback Loop:** Manual grading is tedious; students don't get immediate, actionable feedback
- **Bio Complexity:** Theoretical subjects like Biology need explanation beyond text (lack of audio/visual aids)

### Market Opportunity
- 1M+ NEET/JEE aspirants annually in India
- 80% rely on offline coaching + multiple books (fragmented, untracked)
- Existing platforms (Toppr, Unacademy) focus on live classes, not targeted PYQ practice with weak topic filtering

---

## 3. Product Goals & Objectives

| Goal | Objective |
|------|-----------|
| **Targeted Practice** | Enable students to practice exclusively on weak topics identified via analytics |
| **Time Efficiency** | Reduce study prep time by 30% through intelligent question filtering |
| **Instant Feedback** | Provide AI-powered grading + explanations within seconds of submission |
| **Data Transparency** | Show accuracy trends, weak topic clusters, and progress on personalized dashboards |
| **Accessibility** | Multi-platform (Telegram, Web/React) with voice notes for Biology concepts |
| **Scale PYQ Coverage** | Index 10+ years of NEET/JEE papers (2000+ questions, tagged by topic/difficulty) |

---

## 4. Core Features

### 4.1 Question Database & Indexing
**Feature:** Smart PYQ Parser & Search Engine

**Functionality:**
- Parse PDF question papers (NEET/JEE from 2013–2024) into structured database
- Auto-tag questions by: topic (Organic Chemistry, Plant Physiology, etc.), subtopic, difficulty level (Easy/Medium/Hard), year, exam type (NEET/JEE Main/Advanced)
- Implement dual search: keyword search (Whoosh) + semantic/vector search (FAISS) for concept-based retrieval
- Allow manual tagging for edge cases and refinement

**User Stories:**
- "As a student, I want to search 'enzyme inhibition' and get all related Biology questions from past 5 years"
- "As a student, I want to find Medium difficulty Inorganic Chemistry questions from NEET 2022–2024"

---

### 4.2 Personalized Mock Test Generator
**Feature:** Smart Mock Test Builder with Weak Topic Prioritization

**Functionality:**
- Pull accuracy data from Google Sheets (manual submission or auto-sync from past attempts)
- Filter weak topics (accuracy < 60%) and generate custom mocks with:
  - 70% questions from weak topics
  - 30% from moderate/strong topics (to reinforce)
- Timed interface with real exam format (3-hour countdown, section-wise navigation)
- Support section-wise mocks (Chemistry only, Biology only) or full-length

**User Stories:**
- "As a student with 45% accuracy in Organic Chemistry, I want a 1-hour focused mock with 8 Organic Chem questions"
- "As a student, I want to generate a mock 30 minutes before my commute and get timed feedback"

---

### 4.3 Intelligent Grading & Feedback
**Feature:** Auto-Grading with AI-Powered Explanations

**Functionality:**
- Match student MCQ answers against answer keys using fuzzy matching (tolerate typos: "NADH" vs "nadh")
- Calculate accuracy score and flag weak areas per question
- Integrate GPT-4o for on-demand explanations:
  - Summarize concept from question context
  - Explain why correct answer is right, why others are wrong
  - Suggest NCERT reference chapters
- Store explanations for offline access (reduce API costs)

**User Stories:**
- "As a student, after submitting a mock, I want instant scores + auto-generated explanations for wrong answers"
- "As a student, I want explanations linked to NCERT Chapter 5, Plant Physiology for reference"

---

### 4.4 Analytics & Progress Dashboard
**Feature:** Data-Driven Insights & Trend Analysis

**Functionality:**
- Matplotlib/Plotly dashboards showing:
  - Accuracy by topic (heatmap: topics vs. accuracy %)
  - Accuracy trends over time (line chart: 30-day rolling accuracy)
  - Weak topic clusters (bar chart: top 5 worst-performing topics)
  - Section-wise breakdown (Chem vs Bio vs Physics)
  - Mock completion history with dates
- Export reports as PDF or share with mentors
- Gamification: streak badges, percentile ranking (if multi-user mode)

**User Stories:**
- "As a student, I want to see that my Organic Chemistry accuracy improved from 40% to 65% over 2 weeks"
- "As a student, I want to identify that 'Electrode Potentials' is my weakest topic across all attempts"

---

### 4.5 Voice Notes for Complex Topics
**Feature:** Audio Explanations for Biology & Theory-Heavy Subjects

**Functionality:**
- Allow students to record voice notes (max 5 mins per question) explaining concepts in their own words
- Allow mentors/tutors to upload pre-recorded voice explanations for tricky topics
- Integrate text-to-speech (gTTS or Google Cloud TTS) for auto-generated explanations
- Voice notes indexed and searchable by topic
- Support multilingual (Hindi + English) for broader accessibility

**User Stories:**
- "As a student, I want to listen to a 2-minute explanation of 'Krebs Cycle' by a top mentor before attempting questions"
- "As a student, I want to record my own explanation of a Biology concept and replay it while revising"

---

### 4.6 Multi-Platform Access
**Feature:** Telegram Bot + Web App

**Platform A: Telegram Bot**
- Commands: `/search [topic]`, `/mock [difficulty]`, `/stats`, `/voice [topic]`
- Lightweight, fast access during commute
- Push notifications for weak topic reminders
- Group mode: share mocks with friends, compare stats

**Platform B: React Web App**
- Full dashboard, detailed analytics, voice note upload
- Responsive design (mobile-first, works on all devices)
- OAuth login (Google/GitHub for future multi-user features)

---

## 5. Recommended Technology Stack

### 5.1 Backend & Data Processing

| Layer | Technology | Why |
|-------|-----------|-----|
| **PDF Parsing** | PyPDF2 + Pydantic | Lightweight, reliable PDF extraction; Pydantic for structured data validation |
| **Full-Text Search** | Whoosh | Fast keyword search, offline capability, minimal dependencies |
| **Vector/Semantic Search** | FAISS (Facebook AI Similarity Search) | Efficient similarity search on embeddings; scales to 10K+ vectors; runs on CPU |
| **NLP & Tagging** | spaCy (small model: en_core_web_sm) + custom regex | Fast, accurate topic extraction; minimal overhead |
| **Database** | PostgreSQL + pgvector extension | Reliable ACID transactions; pgvector for vector storage; alternative: Supabase (managed) |
| **Embeddings Model** | Sentence-Transformers (all-MiniLM-L6-v2) | Lightweight (80MB), accurate for question tagging; free, open-source |
| **API/Backend Framework** | FastAPI + Uvicorn | Async-first, fast, automatic OpenAPI docs; ideal for real-time feedback |
| **AI Explanations** | OpenAI GPT-4o (cached prompts) | Cost optimization via prompt caching; avoid repetitive API calls |

### 5.2 Frontend

| Layer | Technology | Why |
|-------|-----------|-----|
| **Web App** | React 18 + TypeScript | Type safety, component reusability, large ecosystem |
| **Styling** | Tailwind CSS | Utility-first, rapid UI development, responsive design |
| **Charts/Analytics** | Plotly.js (React wrapper) or Recharts | Interactive, publication-quality visuals; Recharts is lighter |
| **State Management** | Zustand or TanStack Query | Lightweight, no boilerplate; Query for server state |
| **Testing** | Vitest + React Testing Library | Fast, modern test runner; RTL for component tests |

### 5.3 Bot & Real-Time

| Layer | Technology | Why |
|-------|-----------|-----|
| **Telegram Bot** | python-telegram-bot | Official library, well-maintained, simple webhook/polling |
| **WebSocket (optional)** | Socket.io | Real-time mock submissions, live leaderboards |
| **Task Queue** | Celery + Redis | Async grading, batch explanations; background jobs |

### 5.4 Audio & Multimedia

| Layer | Technology | Why |
|-------|-----------|-----|
| **Text-to-Speech** | gTTS (Google TTS) free tier or Azure TTS | Free/low-cost; quality sufficient for educational content |
| **Voice Storage** | AWS S3 or Cloudflare R2 | Cost-efficient object storage; CDN delivery for fast playback |
| **Audio Processing** | librosa | Feature extraction, noise detection; optional for advanced audio analytics |

### 5.5 Analytics & Monitoring

| Layer | Technology | Why |
|-------|-----------|-----|
| **Charts/Dashboards** | Matplotlib (Python) + Seaborn + Plotly (JS) | Native Python for backend reports; Plotly for interactive web dashboards |
| **Logging/Monitoring** | Prometheus + Grafana | Open-source, self-hosted monitoring; optional but recommended for scale |
| **Data Sheet Integration** | google-sheets-api (Python) | Direct sync with Google Sheets for accuracy logs; zero setup |

---

## 6. Technology Justification: Why This Stack is Efficient

### 6.1 Cost Efficiency
- **Whoosh + FAISS:** Free, open-source alternatives to paid search platforms (Elasticsearch, Pinecone)
- **Sentence-Transformers:** No API cost for embeddings (vs. OpenAI embeddings @ $0.02 per 1M tokens)
- **gTTS:** Free tier for voice generation (vs. AWS Polly @ $16 per 1M chars)
- **PostgreSQL:** Free, self-hosted (vs. Firebase @ $0.06/100K reads)

### 6.2 Performance
- **FAISS:** Vector search in <50ms for 10K questions; scales to millions
- **FastAPI:** 5–10x faster than Flask; async I/O for concurrent requests
- **Whoosh:** Instant keyword search (<5ms for indexed terms)
- **pgvector:** Native vector support; no need for separate vector DB

### 6.3 Scalability
- **Telegram Bot:** Polling via webhooks; handles 1000+ concurrent users
- **Redis Queue:** Async grading; prevents API timeouts during traffic spikes
- **S3/R2:** Unlimited storage for voice notes and PDFs
- **Read Replicas:** PostgreSQL replicas for read-heavy analytics queries

### 6.4 Developer Experience
- **FastAPI + React:** Modern, type-safe, large community
- **python-telegram-bot:** Minimal boilerplate, excellent docs
- **Pydantic:** Runtime type validation; auto-generates OpenAPI specs

---

## 7. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interaction Layer                       │
├──────────────────────────┬──────────────────────────────────────┤
│  Telegram Bot            │       React Web App                   │
│  - /search topic         │  - Dashboard, Mock Interface         │
│  - /mock difficulty      │  - Voice Note Upload                 │
│  - /stats                │  - Analytics Charts                  │
└──────────────────────────┴──────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
├──────────┬──────────────┬──────────────┬────────────────────────┤
│ Question │ Mock Engine  │ Grading      │ Analytics              │
│ Search   │ Builder      │ Service      │ Service                │
└──────────┴──────────────┴──────────────┴────────────────────────┘
     ↓           ↓              ↓                ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Data & Processing Layer                         │
├────────────┬─────────────┬──────────────┬───────────────────────┤
│ PostgreSQL │ FAISS Index │ Celery Queue │ Google Sheets API     │
│ + pgvector │ (Embeddings)│ (Redis)      │ (Weak Topics Log)     │
└────────────┴─────────────┴──────────────┴───────────────────────┘
     ↓           ↓              ↓                ↓
┌─────────────────────────────────────────────────────────────────┐
│                  External Services                               │
├────────────┬─────────────┬──────────────┬───────────────────────┤
│ PDF        │ OpenAI      │ gTTS / S3    │ Telegram API          │
│ Ingestion  │ GPT-4o      │ (Voice)      │ (Webhook/Polling)     │
└────────────┴─────────────┴──────────────┴───────────────────────┘
```

---

## 8. MVP Scope & Roadmap

### Phase 1: MVP (4 weeks)
- [ ] PDF parser for 3 years of NEET PDFs (600 questions)
- [ ] PostgreSQL + Whoosh keyword search (no vector search yet)
- [ ] Basic Telegram bot: `/search`, `/info [qid]`
- [ ] Manual Google Sheets input for weak topics
- [ ] Simple GPT-based explanation API
- [ ] Basic accuracy dashboard (Matplotlib PNG export)

### Phase 2: Smart Mocks (4 weeks)
- [ ] FAISS vector search integration
- [ ] Mock test generator with weak topic filtering
- [ ] Auto-grading engine with fuzzy matching
- [ ] React web app alpha (basic dashboard)

### Phase 3: Analytics & Polish (3 weeks)
- [ ] Plotly interactive dashboards
- [ ] Voice notes (gTTS + S3 storage)
- [ ] Telegram group mode + leaderboards
- [ ] Mobile-responsive React UI
- [ ] Performance optimization (caching, pagination)

### Phase 4: Scale & Monetization (Ongoing)
- [ ] Add JEE Advanced papers (2000+ questions)
- [ ] Multi-language support (Hindi explanations)
- [ ] Mentor dashboard (mark explanations, track student progress)
- [ ] Freemium model: free mock + paid analytics/voice notes

---

## 9. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **PDF parsing accuracy** | Manual validation of parsed questions; regex + spaCy NLP for edge cases |
| **GPT API costs** | Prompt caching, batch processing, store explanations in DB |
| **Vector search latency** | FAISS CPU optimization; pre-compute embeddings; caching top queries |
| **Data privacy** | Use Supabase or self-hosted PostgreSQL with encryption; no user data sent to third parties (only optional GPT calls) |
| **Telegram bot scalability** | Use webhooks + async Celery; start with polling if webhooks unavailable |

---

## 10. Success Metrics & KPIs

| Metric | Target | Timeline |
|--------|--------|----------|
| **Weak topic improvement** | 40% accuracy gain in weak areas | 60 days |
| **Mock completion rate** | 60% of users complete ≥1 mock/week | 30 days |
| **Session duration** | Avg 45 mins per session (vs. 30 for books) | 14 days |
| **Repeat usage** | 50% DAU (daily active users) | 21 days |
| **Feedback quality** | 85% of explanations rated helpful | Ongoing |
| **Time savings** | Students report 30% less prep time | 60 days |

---

## 11. Open Questions for Stakeholders

1. **Monetization:** Freemium (search free, mocks paid) or subscription ($5/month)?
2. **User base:** Internal testing (coaching institute) or open beta on app stores?
3. **Mentor involvement:** Will mentors curate voice notes, or auto-generated only?
4. **Future scope:** AI tutor (chat-based concept learning) post-MVP?
5. **JEE vs. NEET:** Focus on NEET first, or split efforts equally?

---

## 12. Appendix: Tech Stack Summary Table

| Component | Primary | Secondary | Rationale |
|-----------|---------|-----------|-----------|
| PDF Parsing | PyPDF2 | pdfplumber | Reliable, lightweight |
| Search | Whoosh + FAISS | Elasticsearch | Open-source, cost-effective |
| NLP | spaCy | NLTK | Production-grade, fast |
| Backend | FastAPI | Django | Async, modern, fast |
| Database | PostgreSQL | MongoDB | ACID, pgvector extension |
| Frontend | React | Vue | Large ecosystem, hiring pool |
| Charts | Plotly.js | D3.js | Interactive, beginner-friendly |
| Bot | python-telegram-bot | Aiogram | Official, simpler API |
| TTS | gTTS | Azure TTS | Free tier available |
| Async Queue | Celery + Redis | RQ | Industry standard, reliable |

---

**Document Version:** 1.0  
**Last Updated:** Jan 2025  
**Status:** Ready for Development Kickoff