# **Agile Methodology** 

This project was developed following the Agile methodology, with the workflow organized into a series of 4 time-boxed iterations of roughly one week each. Progress was tracked using a Kanban board in GitHub Projects, where user stories were moved through the stages of Open, In Progress, and Done. This iterative approach allowed for flexibility in planning and the ability to adapt to unforeseen challenges, delivering a **potentially shippable increment** each iteration, and the MVP by the deadline.

## Table of contents:
1. [**Sprints Overview**](#sprints-overview)
    * [**Sprint 1**](#sprint-1)
    * [**Sprint 2**](#sprint-2)
    * [**Sprint 3**](#sprint-3)
    * [**Sprint 4**](#sprint-4)
2. [**Scope changes (Agile)**](#scope-changes-agile-user-stories-split)
    * [**Original**](#original-epic-7--user-story-74)
    * [**Split stories**](#split-stories)

***
## Sprints Overview

### **Sprint 1** 
*(2025‑07‑23 – 2025‑07‑30) — Laying the Groundwork*

I started by putting a solid foundation in place. The Django project and core apps were bootstrapped, initial settings landed, and the first domain models—**Post**, **Category**, and **Profile**—took shape. This gave us a shared structure to build on and a running application I could iterate against from day one.

**Highlights**
* Project scaffolding and baseline configuration established.
* First pass at data modeling (Post, Category, Profile).
* Local environments aligned and ready for daily development.

---

### **Sprint 2** 
*(2025‑07‑31 – 2025‑08‑06) — From Structure to Usable Features*

With the basics in place, I shifted quickly into features end‑users could feel. **Post CRUD** matured (create/edit/delete with forms and views), and the site became navigable through a **homepage list** and **post detail** pages. Discoverability improved with **search**, **category filtering**, and **sorting (Newest/Top)**. In parallel, I stood up an early **Heroku pipeline**, so changes were visible outside local machines. First touches on **comments** and **voting** began, accompanied by initial **UI polish**.

**Highlights**
* Post CRUD and core browsing (list/detail) implemented.
* Search, filter, and sorting added for better discovery.
* Heroku deployment pipeline set up (staging visibility).
* Early work on comments and voting; first responsive/UI clean‑ups.

---

### **Sprint 3** 
*(2025‑08‑07 – 2025‑08‑13) — Deepening Interaction and Personalization*

I leaned into community features. **Comments** were rounded out, and **personalization** took off with **avatar upload** and **Saved Posts** (bookmarks). The UI kept evolving: responsive behaviors were refined, and the overall look and feel became more cohesive. On the authentication track, I paved the way for social logins by progressing the **Google** integration so it could be exercised end‑to‑end in the next sprint.

**Highlights**
* Comments completed with an emphasis on authoring and editing.
* Personalization: profile avatars and a dedicated Saved Posts page.
* Continued UI/UX improvements across key pages.
* Groundwork for Google social sign‑in completed.

---

### **Sprint 4** 
*(2025‑08‑14 – 2025‑08‑16) — Ship the MVP*

The final sprint was about pulling threads together and shipping confidently. **Google social login** was integrated and refined, while **Facebook** and **X (Twitter)** were investigated thoroughly—then deliberately **de‑scoped** for the MVP due to external platform requirements. I finalized **admin moderation**, completed **end‑to‑end testing**, and executed the **Heroku production deployment**. Documentation was refreshed to reflect the final state.

**Highlights**
* Google social login integrated and polished.
* FB/X investigated; de‑scoped for MVP (external requirements).
* Admin moderation finalized; end‑to‑end QA completed.
* Production deployment to Heroku; docs updated.

***
## **Scope changes (Agile): User stories split**
Due to the Facebook and X constraints described in the [README](README.md), User Story 7.4 was split by platform. Google remained in scope and was completed; Facebook and X were moved to the backlog..

### Original (Epic 7 · User Story 7.4):
* As a user, I can log in again after initial registration using the same social media account, so that I don't have to enter my website password.
    * Acceptance Criteria:
        * A user who has already registered via Google/Facebook/X can log in again using the same social media button.
        * The user is logged in directly without re-registration.
        * The user's login status is maintained as long as they do not explicitly log out.

---
### Split stories:

User Story 7.4a
* As a user, I can log in again after initial registration using the same Google account, so that I don't have to enter my website password.
    * A user who has already registered via Google can log in again using the same social media button
    * The user is logged in directly without re-registration.
    * The user's login status is maintained as long as they do not explicitly log out.

User Story 7.4b
* As a user, I can log in again after initial registration using the same Facebook account, so that I don't have to enter my website password.
    * Acceptance Criteria:
        * A user who has already registered via Facebook can log in again using the same social media button.
        * The user is logged in directly without re-registration.
        * The user's login status is maintained as long as they do not explicitly log out.

User Story 7.4c
* As a user, I can log in again after initial registration using the same X (Twitter) account, so that I don't have to enter my website password.
    * Acceptance Criteria:
        * A user who has already registered X (Twitter) can log in again using the same social media button.
        * The user is logged in directly without re-registration.
        * The user's login status is maintained as long as they do not explicitly log out.
