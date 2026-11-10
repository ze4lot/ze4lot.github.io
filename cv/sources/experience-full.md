# Professional experience — full source material

Comprehensive work-history facts, context, and previous portfolio wording. This file is supporting material; the copy used for the CV is in `../experience.md`.

## Nord Partner (part of PIB Group)

| Field | Details |
|---|---|
| Period | January 2024 – May 2026 |
| Role (current CV) | Senior Engineer / Architect |
| Role (older portfolio) | Lead Backend Developer / System Architect |
| Industry | Insurance & Brokerage |
| Location in portfolio | Toruń, Poland |
| Website | [nordpartner.pl](https://nordpartner.pl/) |

### Project and business context

- The IT colleague at Nord brought Maciej into the project to help rescue an unstable legacy system and build a new platform.
- Two interconnected workstreams ran in parallel: **maintenance and repair of the existing system** and **architecture plus implementation of a replacement system**.
- The existing platform was critical to brokers' day-to-day workflows and could not simply be abandoned before the replacement was available.
- Source data came from a legacy database. The business planned to switch eventually to a central database supplied by an external provider.
- This planned replacement of the data source was an architectural requirement from the outset, not an unexpected later change.

### Legacy maintenance and analysis

- Analyzed existing application code, undocumented business logic, relational data, and dependencies between workflows.
- Investigated and fixed defects in the legacy platform while users continued operating it.
- The legacy system contained significant code-quality problems and almost no documentation.
- User/broker-entered data was not consistently clean; data integrity and cross-system mismatches had to be diagnosed and handled.
- The findings from investigating the legacy code and database informed the target system's business rules and adapter contracts.
- Work included identifying inconsistent data handling and implementing incremental corrections without disrupting existing operations.

### Replacement platform — architecture

- Designed and implemented the new application, while preserving the ability to work against the old database during transition.
- The central architectural decision was to separate business logic/processes from legacy data access using the **Repository Pattern** and adapters.
- The data access abstraction was meant to enable changing the underlying source to the future external, centralized provider without forcing business process code to depend directly on the legacy schema.
- Made other architectural and implementation decisions pragmatically to fit business expectations and reduce long-term maintenance complexity.
- Applied **event-driven workflows** selectively to integration and data-processing activities — external API integrations, data fetchers, synchronizers, migrators, and importers — with optimization and maintainability in mind.
- The specifics of queues and asynchronous guarantees have not been established; don't automatically describe the system as queue-driven or fully asynchronous.

### Technology choice — FilamentPHP

- Selected **FilamentPHP** to remove much of the burden of developing a custom frontend: administration panels, tables, and similar interfaces were supplied by the framework.
- This allowed the implementation to concentrate on the system's business logic and data flows.
- FilamentPHP was a deliberate productivity/maintenance decision, not merely a technology listed in the stack.

### Delivery and quality

- Implemented automated **CI/CD** with integrated code quality tooling.
- Introduced AI-assisted tools during the work on this project, before the later Bikeparks work.
- Responsible for both architecture and hands-on technical implementation.

### Collaboration and responsibility boundaries

- Nord's internal IT colleague primarily coordinated the project and represented technical work to the business, gathering feedback and facilitating contact.
- Maciej was responsible for architectural design and technical implementation.
- Do **not** present this role as full project ownership, project management, or people management; business-facing coordination was handled by the colleague.

### Full technical stack as listed in the portfolio

PHP 8.4 · Laravel 13 · Filament 5 · JavaScript · Vite · Tailwind CSS 4 · Redis · Laravel Horizon · Laravel Reverb · Docker.

### Previous portfolio wording (preserved)

## Nord Partner (part of PIB Group)

| Field | Details |
|---|---|
| Period | **01.2024 – 2026** |
| Position | Lead Backend Developer / System Architect |
| Sector | Insurance / brokerage |
| Location | Toruń, Poland |
| Website | [nordpartner.pl](https://nordpartner.pl/) |

### Selected work

- Led architectural refactoring of a customer portal for insurance brokers built on multiple integrated systems.
- Designed an integration layer to handle inconsistent internal and external data.
- Reworked data flows to introduce a clearer, more consistent structure across previously disconnected components.

### Responsibilities

- Defined system architecture and integration strategy across multiple data sources.
- Introduced clearer domain boundaries and improved consistency across the platform.
- Translated insurance-sector business requirements into system designs and integration patterns.
- Refactored core functionality to improve maintainability and predictability.
- Investigated inconsistent domain logic and data-handling behavior.
- Supported technical decision-making and aligned implementations with long-term architecture.
- Cooperated with stakeholders on business and technology trade-offs.

### Technologies

PHP 8.4 · Laravel 13 · Filament 5 · JavaScript · Vite · Tailwind CSS 4 · Redis · Laravel Horizon · Laravel Reverb · Docker.

### Factual reconciliation

- Earlier portfolio: **Jan 2024 – Present**; older screenshot: **Jan 2025 – Current**. The user has since accepted **Jan 2024 – May 2026** in the newly drafted entry.
- Current accepted position: **Senior Engineer / Architect**. Older portfolio position: **Lead Backend Developer / System Architect**.
- No team size, hard performance figure, delivery KPI, or guaranteed completion of the data-provider migration was supplied.

---

## Other roles — source material from portfolio

---

## ONWELO

| Field | Details |
|---|---|
| Period | **04.2024 – 01.2025** |
| Position | Technical Coordinator |
| Sector | IT services / consulting |
| Locations | Kraków, Warszawa, Poland |
| Website | [onwelo.com](https://onwelo.com/) |

### Selected work

- Conducted a technical and security audit of a legacy insurance system using PHP 5.6 and delivered targeted security improvements.
- Supported technical planning and process modeling for a new social media product.

### Responsibilities

- Assessed legacy applications with respect to technical design and risk.
- Supported workflow modeling and architecture-oriented planning.
- Coordinated smaller technical tasks, implementation support, and validations.
- Consulted on business processes and design choices for digital products.

### Technologies

PHP 5.6 / 8.2 · JavaScript · PostgreSQL · Nginx · Docker.

---

## Fashion Trends Group

| Field | Details |
|---|---|
| Period | **04.2022 – 03.2023** |
| Position | Team Leader & Senior Software Developer |
| Sector | Retail / distribution / internal IT |
| Locations | Kraków, Skawina, Poland |
| Website | [ftggroup.com](https://ftggroup.com/) |

### Selected work

- Led a development team in day-to-day execution and technical growth.
- Worked directly with business units to align software delivery with operational needs.
- Improved the reliability of internal systems through refactoring and integration work.

### Responsibilities

- Provided technical leadership and mentoring to developers.
- Coordinated implementation priorities in collaboration with business departments.
- Refactored and extended core business systems with an emphasis on stability and maintainability.
- Supported development standards and day-to-day delivery quality.

### Technologies

PHP 8.x · Laravel 9 · MySQL · Redis · Nginx · Docker.

---

## Quad/Graphics

| Field | Details |
|---|---|
| Period | **10.2020 – 03.2022** |
| Position | Senior Software Developer |
| Sector | Marketing / print systems |
| Location | Texas, USA |
| Website | [quad.com](https://www.quad.com/) |

### Selected work

- Took over a legacy project initially developed by an offshore team.
- Stabilized and refactored critical parts of the application and helped bring the project to production readiness.

### Responsibilities

- Assumed ownership of an inherited, incomplete project under delivery pressure.
- Refactored legacy implementation to improve maintainability and operational stability.
- Worked with a wider team to align code changes and technical decisions with business requirements.

### Technologies

PHP 7.4 / 8.0 · Laravel 7.x / 8.x · MongoDB 4.4 · Docker · Nginx · Microsoft Azure.

---

## KISS digital

| Field | Details |
|---|---|
| Period | **04.2016 – 05.2020** |
| Position | Senior Software Developer & Team Leader |
| Sector | Software house |
| Location | Kraków, Poland |
| Website | [kissdigital.com](https://kissdigital.com/) |

### Selected projects

| Project | Involvement |
|---|---|
| **Olimp Premium Club** | Designed business processes and backend architecture; worked on API design and selected mobile application tasks. |
| **Haddad PLM** | Co-designed and supervised development of a product lifecycle management system. |
| **Other commercial projects** | Delivered web applications, e-commerce platforms, and marketing-oriented products. |

### Responsibilities

- Designed software architectures and led backend implementation across projects.
- Led and mentored developers; promoted technical standards and improved tooling.
- Worked with stakeholders to translate business needs into actionable software requirements.
- Supervised engineering quality across custom applications and digital products.

### Technologies

PHP 5.6 / 7.x · Laravel 5.x / 6.x · Symfony 4.x · Vue.js 2.x · JavaScript · jQuery · HTML5 · MySQL · Apache · Nginx · CSS3 / SASS.

---

## Centrum Nowej Technologii

| Field | Details |
|---|---|
| Period | **04.2013 – 06.2015** |
| Position | CTO & Programmer |
| Sector | E-commerce / custom software |
| Location | Kraków, Poland |
| Website | [nowetechnologie.pl](http://www.nowetechnologie.pl/) |

### Selected work

- Led redevelopment of the **Profit Shop** e-commerce platform.
- Separated frontend and backend concerns to support reuse, onboarding, and customization.
- Introduced technologies and architectural changes aimed at easier maintenance and faster delivery.
- Developed websites and tailored commercial applications.

### Responsibilities

- Directed the technical development of the company's core product.
- Modernized the platform architecture to make deployments and customizations easier.
- Combined architecture decisions with hands-on programming and project delivery.

### Technologies

PHP 5.4 · Kohana 3.x · Laravel 4.x · HTML5 · JavaScript · jQuery · MySQL · Apache · CSS3 / LESS / SASS.

---

## AKRA Polska

| Field | Details |
|---|---|
| Period | **12.2012 – 04.2013** |
| Position | PHP Developer |
| Sector | Interactive agency |
| Location | Kraków, Poland |
| Website | [akra.net](https://akra.net/) |

### Selected work

- Took over an unfinished stock-photo platform.
- Migrated the application from CakePHP 1.x to CakePHP 2.x.
- Implemented missing functionality and completed the work needed for launch.

### Responsibilities

- Recovered an incomplete legacy project and stabilized its technical foundation.
- Worked on migration, backend features, and production delivery.

### Technologies

PHP 5.4 · CakePHP 1.x / 2.x · HTML5 · jQuery · MySQL · Apache · CSS / LESS.

---

## EURA7

| Field | Details |
|---|---|
| Period | **10.2011 – 04.2013** |
| Position | PHP Developer |
| Sector | Digital / interactive agency |
| Location | Kraków, Poland |
| Website | [eura7.com](https://www.eura7.com/) |

### Selected work and responsibilities

- Developed marketing websites and maintained existing client-facing applications.
- Delivered features, bug fixes, and changes for projects with different business needs.
- Implemented frontend and multimedia-related functionality alongside backend work.

### Technologies

PHP 5.4 · Zend Framework 1.12 · HTML5 · ActionScript / Flash · JavaScript · jQuery · MySQL · Apache · CSS / LESS.

---

## MKI.PL

| Field | Details |
|---|---|
| Period | **06.2010 – 08.2012** |
| Position | Junior PHP Developer |
| Sector | Web development / e-commerce |
| Location | Kraków, Poland |

### Selected work and responsibilities

- Built websites, e-commerce components, and small business applications.
- Maintained existing projects and delivered new features and bug fixes.
- Developed commercial programming practices while collaborating with more experienced developers.

### Technologies

PHP 5.3 · Symfony 1.x · Yii 1.x · Doctrine 1.x · PostgreSQL · Apache · CSS.

---

## INDEXO

| Field | Details |
|---|---|
| Period | **03.2010 – 05.2010** |
| Position | Trainee Coder |
| Sector | Digital agency |
| Location | Kraków, Poland |

### Selected work and responsibilities

- Supported website implementation and minor application changes.
- Assisted senior developers with bug fixes and early commercial coding tasks.

### Technologies

PHP 5.2 · Zend Framework 1 · jQuery · MySQL · CSS.

---

## Freelance & Consulting

| Field | Details |
|---|---|
| Period | **2010 – present** |
| Position | Freelance Consultant & Lead Developer |
| Sector | Cross-industry software consulting |
| Website | [Portfolio](https://ze4lot.github.io/) |

### Scope of work

- Designed backend architectures for custom applications and business systems.
- Provided technical direction and guidance on maintainability and system evolution.
- Refactored and stabilized legacy applications.
- Translated business requirements into technical plans and design decisions.
- Supported clients in evaluating technical risk, solution options, and architecture.
- Led smaller projects end to end, from analysis through implementation.
- Worked across different stacks depending on project requirements.

### Technologies

PHP · Laravel · Symfony · JavaScript · MySQL · PostgreSQL · Redis · Docker.
