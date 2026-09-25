# VIVO Django Endpoint Parity Plan (gpt5_conversion_plan)

Date: 2025-09-25 23:27 EDT

## Goals and Scope
- Replicate the production Rails site’s user-visible output endpoint-by-endpoint in Django, changing as little of the appearance and behavior as possible.
- Proceed strictly one endpoint at a time, starting with the home page. Do not “improve” UI/UX until parity is achieved; record improvements in a backlog.
- Keep Django views as thin managers (≤ 50 lines), delegate data-prep to helpers in `vivo_app/lib/`, and prefer deterministic stubs when external data are unavailable.

## How to Run Locally
- Start server: `uv run ./manage.py runserver`
- Open: http://127.0.0.1:8000/
- Run tests (unittest): `uv run ./manage.py test -v 2` (or `uv run -m unittest discover -v`)

## LLM Code Directives (from `pyproject.toml`)
- Use Python 3.12 type-hints everywhere for functions and variables; prefer builtin generics (PEP 585) instead of `typing.Dict` etc.
- Structure standalone scripts with `if __name__ == '__main__': main()` and keep `main()` small; delegate to helpers.
- Use the standard `unittest` framework (not pytest).
- Always use `uv` to run code and tests; do not call `python`/`python3` directly.
- Use `httpx` for all HTTP calls.
- Avoid defining functions inside functions.
- Prefer single-return functions where practical.
- Use present-tense triple-quoted docstrings; opening and closing triple quotes on their own lines.

## Current Code Snapshot (high-level)
- URL routing: `config/urls.py` defines home (`'' → vivo_app.views.home_index`), search, display, visualizations, legacy endpoints, and editor stubs.
- View helpers: `vivo_app/views.py` provides thin view functions and a `render_or_stub()` utility that returns a plain-text stub on template errors or when templates are missing; honors `?format=json`.
- Templates: `vivo_app/templates/` contains `base.html`, `home/index.html`, `display/` and `vivo/` directories, plus error templates `404.html` and `500.html`.
- Static: `vivo_app/static/css/style.css`, `vivo_app/static/js/tabs.js` exist; additional assets can be added as needed for parity.
- Settings: `config/settings.py` sets static dirs, file-based cache, logging, and environment-driven VIVO endpoints. Development default is safe for offline work.

Known quick issue to fix during home-page parity:
- In `vivo_app/templates/home/index.html`, `{% url 'home_publications' %}` does not match the route name defined in `config/urls.py` (`name='publications'`). This currently causes a template reverse error and triggers `render_or_stub()` fallback. Update the template to `{% url 'publications' %}` during the home-page work.

---

# Endpoint-by-Endpoint Parity Plan

We will complete each endpoint in order. “Definition of Done” per endpoint:
- Route resolves and mirrors Rails path and trailing-slash semantics.
- View function ≤ 50 lines and delegates data-prep to `vivo_app/lib/...`.
- Template returns near-identical structure/fields to production (HTML, CSS classes/IDs, and minimal JS behavior as necessary).
- JSON parity for dotted extension and/or `?format=json` where applicable.
- Tests cover HTTP status, key context keys, basic HTML markers, and JSON shape.
- Errors logged; respects `render_or_stub()` and future caching as introduced.

## 1) Home Page Parity (now)
- Target: https://vivo.brown.edu
- Local endpoint: `/` → `vivo_app.views.home_index` → `vivo_app/templates/home/index.html`
- Shared layout: `vivo_app/templates/base.html` + `vivo_app/static/css/style.css` (+ additional CSS/JS as needed)

Plan:
1. Capture production baseline
   - Save a snapshot of production HTML and primary CSS class/ID structure for the home page. Identify critical modules: header/nav, hero/search area, links panels, footer, and any dynamic highlights.
   - Also inspect the Rails source under `vivo-on-django/OBSOLETE/` (e.g., `OBSOLETE/app/views/...`) to understand how the production templates are assembled. Use Rails partials as reference while crafting Django templates.
2. Align header and footer
   - Compare production header/footer with `base.html`. Add classes/containers or minimal elements necessary to match appearance and link structure.
3. Search box parity
   - Ensure the search box (action → `/search/`) and placeholder text match production. Confirm keyboard accessibility and visible focus styles.
4. Quick links / sections
   - Port quick links or home-page sections (e.g., Browse People/Organizations, Publications or other panels) to match production ordering, labels, and link URLs. Use production IDs/classes to minimize CSS divergence.
5. Styles and assets
   - Add or adjust CSS in `static/css/style.css` (or `static/css/home.css` if needed) to approximate production look-and-feel. Do not change global styles beyond what is required for parity.
6. Minimal JS (only if needed)
   - If production home requires simple interactions, add minimal JS under `static/js/` and include via `{% block extra_js %}`. Keep no-JS graceful fallback.
7. Fix current reverse error
   - Update `home/index.html` to use `{% url 'publications' %}` instead of `{% url 'home_publications' %}` to prevent stub fallback.
8. Tests
   - Add/extend `TestCase` tests to assert:
     - `GET /` returns 200
     - Presence of header/nav markers, search form, main sections, and footer markers
     - Links point to expected endpoints (`/search/`, `/people/`, `/ous/`, `/publications/`) where applicable
9. Visual check
   - Run locally and compare against production in a browser. Tweak spacing, fonts, and minor styles to get “as similar as possible” without redesign.

Acceptance criteria:
- Home renders without stub fallback, matches production structure/classes for primary regions (header, search, main panels, footer), and links behave the same.
- No console errors; tests passing.

Deliverables for this step:
- Updated `base.html` and/or `home/index.html`
- Adjusted or new CSS/JS assets under `static/`
- New/updated tests (e.g., `vivo_app/tests/test_home.py`)

## 2) Search Parity (next — do not start now)
- Target: https://vivo.brown.edu/search
- Local endpoint: `/search/` → `vivo_app.views.search` → `vivo_app/templates/search/results.html`
- Plan (to be executed after home is done):
  - Capture production search page structure (query bar, facets, results list, pagination).
  - Implement data-prep in `vivo_app/lib/search.py` (deterministic stubs first, then live integrations later as needed).
  - Match markup/IDs/classes and basic interactions. Keep progressive enhancement (no-JS fallback).
  - Tests for query handling, basic HTML markers, and JSON shape if provided.

## 3) Faculty Page Parity (next after search — do not start now)
- Target: https://vivo.brown.edu/display/pmonti
- Local endpoint: `/display/<id>/` → `vivo_app.views.display_show` → `vivo_app/templates/display/show.html`
- Plan (to be executed after search parity):
  - Align left/right panel structure and section IDs/tabs to production. Reuse includes at `vivo_app/templates/vivo/people/includes/` where possible.
  - Ensure presenter-like context keys provided by `vivo_app/lib/display.py` map to the expected template variables. Start with deterministic stubs; add live lookups later.
  - Tests for panel visibility, tab placeholders, and key HTML markers, as already scaffolded.

---

# Contextual Info for Future LLM Sessions
Update this section as the project progresses.

- Project structure: see `vivo-on-django/` tree; templates under `vivo_app/templates/`, static under `vivo_app/static/`.
- Rails reference: `vivo-on-django/OBSOLETE/` contains the prior Rails codebase. Check `OBSOLETE/app/views/` partials and layouts to mirror production markup, classes/IDs, and section order.
- Key files to check first:
  - `config/urls.py` for route → view mapping
  - `vivo_app/views.py` for thin views and `render_or_stub()` behavior
  - `vivo_app/templates/base.html` and endpoint-specific templates
  - `vivo_app/static/css/style.css` and any endpoint-specific CSS/JS
- Dev commands:
  - Run server: `uv run ./manage.py runserver`
  - Tests: `uv run ./manage.py test -v 2` (or `uv run -m unittest discover -v`)
- External dependencies:
  - Use `httpx` for HTTP if/when live VIVO/Solr calls are introduced. For now, prefer deterministic stubs for parity.
- Settings highlights (`config/settings.py`):
  - Static dirs configured; file-based cache; logs under `logs/django.log`.
  - `DEBUG` controlled via environment; safe defaults in development.
- Patterns and constraints:
  - Keep views ≤ 50 lines; delegate logic to `vivo_app/lib/`.
  - `render_or_stub()` returns a text stub on template errors/missing templates; look for this if pages don’t render.
  - Honor `?format=json` and dotted extensions where applicable.
- Known quick fix queued for home:
  - `home/index.html` URL name mismatch noted above (“publications” vs “home_publications”).

Action: Continue to amend this Contextual Info as new decisions, shortcuts, or pitfalls emerge (e.g., asset naming, partials locations, test utilities).

---

# Working Routine and Checkpoints
- After each endpoint (or substantial subtask), add a short checkpoint:
  - Completed items
  - Any new decisions/assumptions
  - Updated next-two-tasks list
- Keep the “Improvements Backlog” for non-parity enhancements; do not implement them during parity work.

## Improvements Backlog (record only; not to implement yet)
- CSS consolidation and modularization
- JS modularization and accessibility refinements beyond production parity
- Performance/caching improvements across API calls and templates
