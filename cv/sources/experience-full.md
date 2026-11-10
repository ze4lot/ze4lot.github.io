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
| Period | April 2024 – January 2025 |
| Position | Technical Coordinator |
| Sectors | IT Consulting / Insurance / E-commerce |
| Locations | Kraków, Warszawa, Poland |
| Website | [onwelo.com](https://onwelo.com/) |

### Project 1 — Nord Partner: Legacy PHP modernization and security

**Client and context**

- Nord Partner commissioned ONWELO to perform a security audit, fix defects, and release an updated version of its existing insurance application.
- The system was a largely undocumented legacy PHP application with technical debt and defects.
- This assignment was where Maciej met Paweł from Nord Partner, with whom he later worked directly on legacy maintenance and development of its successor platform.
- PHP was substantially outdated. The starting version may have been around 5.2, with modernization reportedly reaching 7.4 and later 8.x; **exact migration versions remain unconfirmed**.

**Technical ownership and collaboration**

- Maciej owned the backend work and some server/infrastructure tasks.
- A second developer was responsible for frontend changes; they cooperated closely.
- The work encompassed understanding the legacy implementation, auditing security, fixing problems, modernizing the runtime and dependencies, preparing documentation, and releasing the updated application.

**Legacy upgrade strategy**

- Upgraded the PHP runtime, requiring compatibility work across the application.
- Updated dependencies where newer, compatible releases existed.
- Replaced libraries and dependencies that could not reasonably be upgraded.
- Rewrote portions of code or functionality where dependencies could not be preserved.
- Fixed application defects alongside the modernization.
- Prepared documentation for previously undocumented areas of the system.
- Handled some required server configuration/infrastructure changes.

**Delivery and independent verification**

- Prepared and delivered an updated release.
- The project concluded successfully: the updated application passed demanding security and penetration tests conducted by an independent specialized external company.
- This result should not be described as the user's personal performance of those external penetration tests; the external company did them.

### Project 2 — Social platform: E-commerce process modeling

**Project context**

- A different unit of ONWELO was working on a large social-media platform with adult-oriented educational content and webinars.
- A related e-commerce capability was planned for the platform.
- Maciej was invited to contribute because of his e-commerce domain and engineering experience.

**Role and contribution**

- Worked with business departments and another architect to analyze and design business processes for the planned e-commerce component.
- Modeled the end-to-end customer purchasing journey.
- Covered order handling, after-purchase service, back-office operations, and warehouse/logistics workflows.
- The contribution was process analysis and design, **not programming or implementation**.
- No final implementation or successful deployment of the e-commerce subsystem has been established.

### Technical stack recorded in the older portfolio

PHP 5.6 / 8.2 · JavaScript · PostgreSQL · Nginx · Docker.

### Positioning retained for the CV

- Business process design and cross-functional collaboration first.
- Hands-on backend modernization and selective infrastructure responsibility.
- Security remediation and independently validated release as an outcome.

---

## Fashion Trends Group

| Field | Details |
|---|---|
| Period | April 2022 – March 2023 |
| Position | Team Leader & Senior Software Developer |
| Industry | Fashion retail / e-commerce / internal business systems |
| Locations | Kraków, Skawina, Poland |
| Website | [ftggroup.com](https://ftggroup.com/) |

### Context — existing ERP and product operations

- FTG operated a large street-fashion retail business.
- A heavily loaded, difficult-to-extend **Comarch ERP** supported much of the organization. Its limitations restricted further digitalization and process automation.
- An independent **PIM** platform was being built as a complementary system to take over business responsibilities that were difficult to implement or maintain within ERP.
- Maciej joined **shortly after PIM development had started**, not at the initial project conception. The team needed experienced technical leadership and delivery organization.

### PIM — business workflows and system boundaries

- The product lifecycle started with selected input information retrieved from Comarch ERP.
- Different business departments then worked on the product inside PIM, enriching details such as descriptions, technical attributes, and images.
- PIM also covered product-related pricing, customer assignments, warehouses, labeling, identification, and operational data.
- After product preparation was complete, processed product information was passed to ERP.
- Separate information flows supported warehouse operations, including labeling, identification and scanner-based processes.
- This was an **ERP-adjacent application**: it complemented and relieved Comarch rather than replacing the entire ERP.
- The precise transport used between systems (API vs direct database vs file-based import/export) was not established.

### Existing customer-service platform

- Alongside the evolving PIM, Maciej maintained and developed an already-existing customer-service platform.

### Hands-on technical leadership

- Acted as a **hands-on technical lead** while continuing to program.
- Provided experience, guidance, support and mentoring to a younger, motivated group of developers who lacked consistent senior engineering support.
- Helped developers with technical decisions and day-to-day delivery rather than functioning as their formal HR manager.
- Defined, refined and distributed work items, passed on requirements, assets, and feedback, and co-managed the backlog.
- Cooperated closely with the Head of IT, project managers, and a designer, with additional collaboration with warehouse, accounting and service departments.
- Discussed functionality with business stakeholders, represented the development team and helped deliver agreed functionality together.

### Process and delivery turnaround

- On arrival, the main challenge combined organizational chaos with insufficient technical guidance.
- Jira was available, but the team did not have an effective way to use and organize it.
- Introduced **pragmatic, team-adapted Scrum practices**, sprint cadence, daily meetings, planning, structured Jira work and a **release calendar**.
- Established a clear schedule and intake process for business requests. Stakeholders could no longer continuously introduce ad-hoc tasks that derailed planned work.
- This reduced interruptions and context switching, made delivery more predictable, helped the IT department regain control over its workload and **lowered stress/pressure on the IT team**.
- Invested in team integration and improving trust and relationships, alongside technical mentorship.
- Outcomes are qualitative; no numeric productivity, throughput or team-size metrics were provided.

### Technologies recorded in the portfolio

PHP 8.x · Laravel 9 · MySQL · Redis · Nginx · Docker.

### Delivery tooling

Jira · Scrum-inspired planning · sprints · daily meetings · release calendar.

### Earlier portfolio wording (preserved for reference)

- Led a development team in day-to-day execution and technical growth.
- Worked directly with business units to align software delivery with operational needs.
- Improved reliability of internal systems through refactoring and integration work.
- Mentored developers, aligned business expectations with implementation, and supported technical standards and delivery quality.

### Positioning boundaries

- Do not claim Maciej designed the entire PIM architecture from scratch: he joined shortly after the initial build began.
- Do not claim he was the direct people manager responsible for hiring, performance appraisals or budgets.
- The main impact was delivering senior technical guidance and predictable execution while remaining hands-on; avoid unverified quantitative impact.

---

## Quad/Graphics

| Field | Details |
|---|---|
| Period | October 2020 – March 2022 |
| Position | Senior Software Developer |
| Industry | Enterprise Marketing / Print / Retail |
| Location | Texas, USA (as listed in the original portfolio) |
| Website | [quad.com](https://www.quad.com/) |

### Business context

- The application supported creating, managing, previewing and approving promotional flyers for large US retail chains.
- Flyers could have **regional variants (“zones”)**: the assortment and promotional content could differ by geographical area while sharing the same overall campaign.
- The workflow accepted **Excel imports** containing product and promotional data. Users could review and edit imported data in a dedicated interface with a flyer preview.
- The application allowed managing zone-specific changes and approvals, then exported the processed data back to **Excel** for the downstream production department.
- **MongoDB** was used as a local application database.

### Project recovery

- The original application was outsourced to an external vendor, but the delivered version could not initially be run successfully; once running, substantial functionality was broken.
- The inherited Laravel code contained poor separation of concerns, extremely large controller methods with extensive inline arrays and other maintainability issues.
- Quad/Graphics set up a **new senior-only engineering recovery team based in Poland** to salvage and deliver the product.
- The engineers operated as a **self-organizing technical team**, supported by a project manager and with unusually direct access to high-level business stakeholders.
- Avoid attributing unverified dishonest intent to the previous vendor; the supported technical claim is that the code was non-functional and poorly structured.

### Maciej's direct technical contribution

- Took responsibility for substantial **application architecture recovery**.
- Updated the Laravel application and its environment as necessary to get the product running.
- Cleaned up the inherited codebase and reorganized it into modules.
- Refactored application models and introduced abstractions to reduce coupling and improve maintainability.
- This foundational work helped the team move beyond basic recovery into building and fixing business functionality.
- After stabilization, actively implemented new features alongside the other senior developers.
- Work was selected and shared informally within the autonomous team, drawing on individual interests and strengths; there was no claim of formal team leadership.

### Production launch and ongoing delivery

- The senior team reached a **production launch quickly**, despite known product limitations and defects.
- A separate **downstream validation team** reviewed exported Excel files before those files were used by the next department.
- When that team detected issues, it corrected the files for ongoing operations and reported problems back to engineering.
- Engineering used this feedback loop to fix defects and improve the application incrementally after deployment.
- This was a pragmatic phased delivery under pressure, with manual verification as a safeguard; do not describe the launch as defect-free.
- Business stakeholders were available to engineering directly for rapid clarification and prioritization.

### Technologies from existing portfolio

PHP 7.4 / 8.0 · Laravel 7.x / 8.x · MongoDB 4.4 · Docker · Nginx · Microsoft Azure.

### Summary of contributions

Application recovery · Laravel modernization · modular refactoring · model refactoring · abstractions · enterprise Excel workflows · regional content management · senior engineering collaboration · production delivery.

---

## KISS digital

| Field | Details |
|---|---|
| Period | April 2016 – May 2020 |
| Position | Senior Software Developer & Team Leader |
| Industry | Software house / custom software / digital products |
| Location | Kraków, Poland |
| Website | [kissdigital.com](https://kissdigital.com/) |

### General context and career development

- Joined as a software developer at a conventional software house and worked on **approximately a dozen or more client projects**, ranging from small commercial tasks to multi-component business applications.
- Became a respected, **informal senior engineer and technical leader**, earning trust through experience, initiative, sound judgement, and willingness to take responsibility beyond assigned coding tasks.
- Was frequently assigned complex, ambiguous or architecture-heavy projects instead of routine implementation tasks.
- Comfortable communicating directly with clients, proposing solutions, explaining technical tradeoffs and pushing back when needed.
- His influence and leadership were based on technical credibility and relationships rather than formal organizational authority or a dedicated people-management remit.
- Helped other developers tackle difficult technical problems and participated in architectural decisions.

### Olimp Premium Club — mobile loyalty platform

**Business need**

- Client wanted a mobile loyalty program in which customers earned points from product purchases and redeemed them for products/rewards available in the mobile application.
- Maciej was the primary technical owner of the solution, involved from business concept onward.
- Proposed functional and technical approaches; materially shaped the mobile application's workflows and API-facing behavior.
- **Independently designed and implemented the entire backend** and defined API contracts for the mobile app.
- Architecture covered loyalty points, customer actions, scanned codes and reward redemption.

**Strategy-based fraud detection**

- Designed and implemented an additional fraud-detection subsystem to identify misuse of loyalty mechanics in real time or during user actions.
- Detector used several programmed strategies/patterns, including:
  - Mass or suspiciously broad product scanning.
  - Attempts to reuse already-consumed codes.
  - Excessive scanning frequency.
- Detection and verification rules determined whether an operation could proceed or needed additional proof, e.g. a receipt image.
- This was a **rule-based strategy engine**, not machine learning; avoid implying it was AI.

**Receipt image recognition and manual verification**

- Mobile app submitted a photograph of a purchase receipt.
- Backend integrated a third-party image-to-text / receipt-reading service through a simple API.
- The system interpreted the returned information sufficiently to decide whether the receipt appeared acceptable or required review by a human moderator.
- Maciej implemented the integration and backend verification workflow; **did not invent or implement OCR technology**.
- The provider was later discovered to have relied on human transcription behind its API rather than genuine automated OCR. The client-facing feature is accurately described as external receipt recognition/verification, not proprietary OCR implementation.
- Do not claim perfect automatic recognition or identify provider personnel by nationality.

### Haddad — Product Lifecycle Management (PLM)

**Business purpose**

- An application functioning as a virtual apparel-design studio, integrating activities distributed across the lifecycle of new clothing products.
- Supported material selection and ordering, product/detailed apparel design, application of brand identification (e.g. Nike and Converse), and handoffs among departments and users.
- Work progressed toward factory orders and production; final product documentation included costing and campaign associations.
- Similar in business domain to a PIM, but centered on apparel product development and design workflows rather than simple catalog enrichment.

**Team and technical solution**

- Delivered with a **two-developer core team**: Maciej owned backend development, another engineer owned frontend development.
- Application was frontend-heavy and relied on a deliberately focused backend for persistent shared state and synchronization.
- Backend preserved users' work and allowed the next person or department to continue from the appropriate project state/view.
- Supported **real-time collaborative editing** with live state updates aided by **WebSockets**.
- Maciej designed and developed the backend and worked directly with the frontend developer to define data contracts and state behavior.
- Avoid asserting specific concurrency algorithms, conflict resolution, event sourcing or CRDT/OT technologies: these were not established.

### Other client work

- Built or contributed to numerous smaller web applications, e-commerce solutions, promotional/digital campaigns and other commercial client projects.
- Specific small campaign names intentionally omitted from final CV; the focus is diversity and continuity of delivery across multiple clients rather than enumerating every engagement.

### Company-level technical leadership and Agile introduction

- Actively contributed to adopting **Scrum and Jira** at a time when both were new to the company.
- Explained to colleagues how to write useful **user stories** and **technical tasks**, including how the two differ.
- Supported the introduction of more structured requirements and development workflows.
- Worked comfortably with clients, defended necessary technical decisions and supported colleagues on complicated topics.
- Informal role: **do not invent direct reporting lines, hiring/firing authority, performance management responsibility, or formal engineering-management title**.

### Technologies recorded in the original portfolio

PHP 5.6 / 7.x · Laravel 5.x / 6.x · Symfony 4.x · Vue.js 2.x · JavaScript · jQuery · HTML5 · MySQL · Apache · Nginx · CSS3 / SASS.

Additional confirmed domain technology: WebSockets, Jira, Scrum.

---

## Centrum Nowej Technologii

| Field | Details |
|---|---|
| Period | April 2013 – June 2015 |
| Position | CTO & Programmer |
| Industry | E-commerce / custom software / software house |
| Location | Kraków, Poland |
| Website | [nowetechnologie.pl](http://www.nowetechnologie.pl/) |

### Role and context

- Worked as a hands-on programmer who regularly took initiative beyond routine implementation, similar to his later experience at KISS digital.
- Held the title **CTO & Programmer**, but no direct report structure, executive budget ownership, or formal people-management remit has been established; do not infer those from the title.
- Combined development of the company's own product, **Profit Shop**, with typical external custom-software projects delivered by a software house.
- Contributed to technical decisions and architectural improvements, while actively programming.

### Profit Shop — reusable e-commerce platform

- **Profit Shop** was a product for launching online stores for multiple client businesses.
- Over time, client-specific adaptation and existing-store maintenance/upgrades were becoming increasingly difficult as the shared product and customized presentation layer grew more complex.
- Maciej proposed separating the shared business/application **core** from store-specific presentation and design.
- The resulting architecture divided a shared **backend** from a **frontend layer** composed of templates and styles (including CSS).
- The frontend was made **configurable/parameterized**; adjustments to colors, fonts and other visual elements became much easier and less invasive.
- The aim was to avoid repeated extensive modifications of the shared platform for every new storefront.
- The redesign was **implemented and adopted in ordinary delivery**, rather than remaining a proof of concept.
- User reports it **dramatically reduced the time** required both for setting up new customer stores and upgrading existing deployments. No numerical measurements or percentages available; final CV should use a qualitative claim.
- This was separation of concerns and configurability within an e-commerce platform; do **not** characterize it as microservices, headless commerce, or an entirely new standalone frontend application without evidence.

### Additional custom projects

- Beyond Profit Shop, built and contributed to various conventional software-house client projects, including websites and tailored commercial applications.
- No individual smaller client projects were selected for the final CV because the platform architecture and delivery outcome are the strongest differentiators.

### Legacy portfolio wording

- Led redevelopment of the Profit Shop e-commerce platform.
- Separated frontend and backend concerns to support reuse, onboarding, and customization.
- Introduced technologies and architectural changes aimed at easier maintenance and faster delivery.
- Developed websites and tailored commercial applications.
- Combined architecture decisions with hands-on programming and project delivery.

### Technologies recorded in portfolio

PHP 5.4 · Kohana 3.x · Laravel 4.x · HTML5 · JavaScript · jQuery · MySQL · Apache · CSS3 / LESS / SASS.

---

## AKRA Polska

| Field | Details |
|---|---|
| Period | December 2012 – April 2013 |
| Position | PHP Developer |
| Industry | Interactive agency / software development / digital media |
| Location | Kraków, Poland |
| Website | [akra.net](https://akra.net/) |

### Project context

- Took over an unfinished **stock photography platform**.
- Migrated the inherited application from **CakePHP 1.x to CakePHP 2.x**.
- Implemented missing functionality and fixed existing problems to prepare the product for launch.
- Worked on backend functionality, modernization and production-delivery preparation.

### Recollection and verification limits

- No reliable recollection of why the project had been left incomplete or why this assignment was undertaken.
- The original portfolio reports work needed for launch, but there is **no explicit confirmation that the application ultimately went live**.
- No additional system architecture or project outcomes were supplied. Keep the final CV concise.

### Technologies from original portfolio

PHP 5.4 · CakePHP 1.x / 2.x · HTML5 · jQuery · MySQL · Apache · CSS / LESS.

---

## EURA7

| Field | Details |
|---|---|
| Period | October 2011 – April 2013 |
| Position | PHP Developer |
| Industry | Digital / interactive agency |
| Location | Kraków, Poland |
| Website | [eura7.com](https://www.eura7.com/) |

### Experience

- Worked primarily on conventional implementation and maintenance of marketing websites, interactive solutions and commercial web applications.
- Delivered frontend and backend features, fixes and client-requested changes in multiple agency projects.
- The user recalls this period as principally routine hands-on development rather than architecture, ownership or technical leadership.
- No particular large project or notable business outcome was identified; final CV intentionally uses a single concise bullet.

### Technologies recorded in the original portfolio

PHP 5.4 · Zend Framework 1.12 · HTML5 · ActionScript / Flash · JavaScript · jQuery · MySQL · Apache · CSS / LESS.

---

## MKI.PL

| Field | Details |
|---|---|
| Period | June 2010 – August 2012 |
| Position | Junior PHP Developer |
| Industry | Web Development / E-commerce |
| Location | Kraków, Poland |

### Work and context

- Early commercial PHP role involving creation and maintenance of websites, e-commerce components and small business applications.
- Typical work included implementing new functionality, making minor changes, fixing defects and maintaining existing client projects.
- Worked with more experienced developers and gained practical knowledge of commercial software development.
- User does **not** remember additional specifics from this period; the details above originate from the earlier portfolio. Do not infer specific client engagements, leadership or measurable results.

### Technologies recorded in original portfolio

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
