---
title: "Bikeparks.pl — Engineering Case Study"
language: en
status: draft
reviewed: 2026-11-10
public_url: "https://bikeparks.pl/"
---

# Bikeparks.pl

**Independent digital product | Product direction, architecture, and hands-on engineering**  
**2026–present** · [bikeparks.pl](https://bikeparks.pl/)

## Short CV version (recommended: 3 bullets)

- Architected and launched Bikeparks.pl, a cycling-infrastructure discovery platform built with PHP/Symfony, PostgreSQL, Redis, and Docker, following modular-monolith principles and explicit domain boundaries.
- Owned end-to-end technical decisions: data modeling, backend, SQL performance, testing strategy, infrastructure, deployments, and product prioritization.
- Designed a controlled AI-assisted development process: scoped engineering tasks, coding agents, reviewed pull requests, automated tests, and human acceptance; separately, explored LLM-based extraction and verification of external data.

## Portfolio / interview version

### The product

Bikeparks.pl organizes information about bike parks, pump tracks, singletracks, and associated riding tracks. The public platform supports discovery of destinations and their facilities; additional capabilities continue to evolve.

Rather than treating the site as a static directory, I designed it as a structured product with canonical domain data, moderation processes, media management, and room for external research and enrichment.

### Architecture and ownership

I own product and engineering direction, from identifying needs and shaping domain concepts to architecture, implementation, review, infrastructure, and release decisions.

The backend is a **Symfony modular monolith**. Domain and application rules are intentionally separated from framework and infrastructure adapters. The platform uses PostgreSQL, Doctrine, Redis, RabbitMQ, Nginx, and Docker-based environments.

Key engineering concerns include data integrity, clear boundaries between modules, traceability of imported information, high-quality read models, and pragmatic operation on modest infrastructure.

### Working with AI agents

I use coding agents as part of a structured software delivery process rather than simply generating snippets. Work is decomposed into explicit issues and acceptance criteria; agents prepare changes and tests; implementation is reviewed against architectural constraints and product requirements before merge or deployment.

Human accountability remains central: I retain responsibility for priorities, domain decisions, risk, QA interpretation, and release approval.

### Performance engineering

The platform's evolving Explore capability requires queries across places, tracks, geography, dates, and operating-status information. I work with PostgreSQL execution plans, targeted benchmarks, controlled query budgets, and iterative SQL optimization.

**Important distinction:** the Operational Statuses V1 work and its newer Explore integration are still under development/review as of 10 Nov 2026. Do not describe them as publicly shipped. Benchmark results should be presented as test-environment measurements, never as measured production improvements.

### External intelligence experimentation

A separate intelligence pipeline researches external material, uses language models to extract candidate facts, and validates outputs before possible review. This experimentation is architecturally isolated from the canonical application and does not grant an LLM uncontrolled write access to production domain data.

Do not confuse a validated machine-generated candidate with a confirmed true fact.

## Stack (curate per audience)

PHP 8.x · Symfony · PostgreSQL · Doctrine · Redis · RabbitMQ · Docker Compose · Linux · Nginx · GitHub · automated testing · SQL plan analysis · AI coding agents · local LLM experimentation.

## Evidence to gather before final publishing

- A current and dated catalog snapshot, with a source and definition for each metric.
- Screenshots or references for production-delivered functionality.
- One or two reproducible SQL benchmark comparisons with dataset size, scenario, and environment clearly labeled.
- Current unit/integration/E2E test counts only if tied to a specific commit.
- A short example of the agent workflow showing the human review and acceptance boundary.

## Positioning

The strongest story is not “AI built my website.” It is: **an experienced software architect uses AI-assisted delivery while maintaining domain ownership, system quality, and reliable operational practices.**
