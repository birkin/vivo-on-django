# VIVO Django Conversion Plan

## Current Status: Phase 2 (Routes & Tests) - Initial scaffolding complete

## Completed Tasks
- [x] Created OBSOLETE directory with Rails files
- [x] Set up project structure with Django 5.2
- [x] Configured pyproject.toml with dependencies
- [x] Set up basic Django settings with environment variables
- [x] Configured static and media file handling
- [x] Set up file-based caching
- [x] Created initial URL routing structure
- [x] Implemented base template and basic styling
- [x] Set up initial views for all routes
- [x] Created database and ran initial migrations
- [x] Created superuser for admin interface
- [x] Configured comprehensive logging
- [x] Set up custom error pages (404, 500)
- [x] Cleaned up imports and fixed linting issues

## Scope Update (2025-08-24)
- Focus shifted away from authentication/user management; those pieces remain in code but are not a priority.
- Primary goal: replicate the Rails web experience as closely as possible.
- Test-first approach: map Rails routes to Django, create Django TestCase tests for each endpoint, then implement views to pass tests.
- Views should be thin managers (<50 lines) and delegate to helpers in `vivo_app/lib/`.
- Use Django's file-based cache; ignore Shibboleth, data migration, DRF, and deployment for now.

## Project Structure
```
vivo-on-django/
├── pyproject.toml
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vivo_app/
│   ├── __init__.py
│   ├── apps.py
│   ├── views.py
│   ├── lib/
│   │   ├── __init__.py
│   │   └── visualization.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── display/
│   │   ├── edit/
│   │   └── home/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
└── docs/
    └── routes_mapping.md
```

## Phase 0: Backup Existing Project
1. [x] Create an `OBSOLETE` directory
2. [x] Copy all existing Rails files to `OBSOLETE/` while preserving directory structure
3. [x] This provides a reference point and safety net during the conversion

## Phase 1: Project Setup - COMPLETED
1. [x] Initialize Django project structure
2. [x] Set up `pyproject.toml` with dependencies
3. [x] Configure basic settings (debug, static files, templates)
4. [x] Set up file-based cache
5. [x] Configure logging
6. [x] Set up error pages (404, 500, etc.)
7. [x] Implement basic authentication views
   - [x] User registration
   - [x] User login/logout
   - [x] Navigation updates
   - [x] Styling for auth forms
   - [x] Error handling and messages

## Phase 2: Core Functionality
1. **URL Routing**
   - Convert Rails routes to Django URL patterns
   - Organize URLs by functional area (display, edit, search, etc.)
   - Implement direct view function calls in `urls.py`

2. **View Layer**
   - Create function-based views in `views.py`
   - Keep views under 50 lines each
   - Move business logic to `lib/` modules
   - Implement error handling and logging

3. **Templates**
   - Set up base template with common layout
   - Create template directories mirroring Rails structure
   - Convert ERB templates to Django template language

## Phase 3: Feature Implementation

### Display Functionality
- Individual profiles
- Visualizations (coauthor, collab, publications)
- File/image serving

### Edit Functionality
- Profile editing
- Research area management
- Web links management

### Search
- Basic search functionality
- Advanced search interface
- Search facets

### Reports
- Subject librarian reports
- Export functionality

## Phase 4: Testing & Refinement
- Implement basic tests for critical paths
- Test URL routing and view responses
- Verify template rendering
- Test search functionality

## Implementation Notes

### Runtime and Typing (Python 3.12)
- Runtime: Python 3.12 for this project.
- Typing style: prefer builtin generics (PEP 585), e.g., `dict[str, Any]`, `list[int]`, `set[str]`; avoid `typing.Dict`, `typing.List`, etc.
- Optionals/Unions: prefer `str | None` over `Optional[str]` where reasonable.
- Keep typing imports minimal (e.g., import only `Any` if needed).
- Continue using `uv run` for all project commands (e.g., `uv run ./manage.py test -v 2`).

### URL Structure
Note: The following is illustrative. The actual, authoritative URL patterns live in `config/urls.py` and use trailing slashes and legacy regex routes (e.g., `individual` export) with correct ordering.
```python
# config/urls.py
urlpatterns = [
    # Display
    path('individual/<str:id>', views.individual_redirect),
    path('display/<str:id>', views.display_show, name='display_show'),
    path('display/<str:id>/publications', views.display_publications, name='display_publications'),
    
    # Edit
    path('edit/<int:faculty_id>', views.edit_profile, name='edit_profile'),
    path('edit/overview/<int:faculty_id>/update', views.overview_update, name='overview_update'),
    
    # Search
    path('search', views.search, name='search'),
    path('search/advanced', views.advanced_search, name='advanced_search'),
    
    # Home and static pages
    path('', views.home_index, name='home'),
    path('about', views.home_about, name='about'),
    
    # Catch-all for 404
    re_path(r'^.*$', views.page_not_found, name='page_not_found')
]
```

### View Structure Example
```python
# vivo_app/views.py
def display_show(request, id):
    """Handle display show view."""
    try:
        context = display_lib.get_display_context(id)
        return render(request, 'display/show.html', context)
    except Exception as e:
        logger.error(f"Error in display_show: {str(e)}")
        return render(request, 'error.html', {'error': str(e)}, status=500)

# vivo_app/lib/display.py
def get_display_context(id):
    """Get context for display show view."""
    # Business logic here
    return {
        'profile': get_profile(id),
        'publications': get_publications(id)
    }
```

### Template Structure
```
templates/
  base.html
  display/
    show.html
    publications.html
  edit/
    profile.html
    research.html
  home/
    index.html
    about.html
    faq.html
```

## Dependencies
- Django 5.2
- trio (for optional async/concurrency support)
- python-dotenv (for environment variables)

## Next Steps - Immediate Focus
1. **Route Mapping & Test Scaffolding** — Completed (initial pass)
   - [x] Populate `docs/routes_mapping.md` with a Rails→Django endpoint map
   - [x] Expand `config/urls.py` to include Rails routes (legacy `individual/*` regex, `edit/fast/search/`, `home/brown`, `help/viz`, `status`, `side_stuff/brown_classic/*`)
   - [x] Add thin manager functions in `vivo_app/views.py` for new routes; add `render_or_stub()` and `?format=json` handling
   - [x] Create Django `TestCase` tests for key endpoints (URL resolution + minimal response assertions)

2. **Core Functionality**
   - [ ] Add Solr search helpers under `vivo_app/lib/` and connect them to views
   - [ ] Build visualization helpers in `lib/visualization.py`
   - [ ] Create base templates for all referenced pages to remove 500s progressively
   - [ ] Add simple file-based caching on expensive calls

3. **Testing & Quality**
   - Use Django’s built-in test runner and `TestCase` (no pytest / no DRF)
   - Add tests incrementally per route as logic/templates land
   - Keep views <50 lines, move helpers to `vivo_app/lib/`

## Progress Checkpoint (2025-08-24 09:12 EDT)

- Completed: `docs/routes_mapping.md` populated with Rails→Django mapping
- Completed: `config/urls.py` updated with missing routes and legacy `individual` regex patterns; ensured export regex routes are ordered before the generic redirect so `/individual/<id>.json/` returns JSON
- Completed: Stub views added in `vivo_app/views.py`; introduced `render_or_stub()` to avoid template 500s; wired error handlers to use it; `?format=json` honored across views
- Completed: Added `vivo_app/tests/test_routes.py` covering home, display, search, reports, legacy `individual` (both patterns), and editor fast search; all tests pass
- Completed: Fixed `vivo_app/admin.py` to use related name `profile` (not `userprofile`); removed `vivo_app/tests.py` to avoid unittest discovery conflict
- Note: Tests are run via `uv` (e.g., `uv run ./manage.py test -v 2`)

-- Next: Begin endpoint-by-endpoint parity work; no code changes now.

## Progress Checkpoint (2025-08-24 12:15 EDT)

- Completed: Initial `display_show` parity scaffolding
  - Added helper `vivo_app/lib/display.py` with `get_type_for_id()` and `build_display_context()`
  - Updated view `vivo_app/views.py` `display_show()` to delegate to helper (≤ 50 lines), preserving `?format=json` fallback for unknown IDs
  - Created template `vivo_app/templates/display/show.html` with minimal faculty/org/unknown sections
  - Added tests `vivo_app/tests/test_display.py` for people/org JSON and basic HTML markers; included unknown-type HTML test
  - Test run completed successfully via `uv run ./manage.py test -v 2`

- Things to remember
  - Type detection uses ID-prefix guesses for now; replace with a Solr lookup during a later pass
  - Keep views thin; continue delegating data-prep to `lib/`

- Next two specific tasks
  1. Implement `display_publications` data-prep in `vivo_app/lib/display.py` and enhance `display_publications()` view/template for parity
  2. Start porting faculty page sections (left/right panels), reusing `vivo_app/templates/vivo/people/*` where feasible; add minimal includes and tests

## Known Issues
- Many templates are placeholders or missing; several views will 500 until templates are added
- Some unused imports may exist while scaffolding; will be cleaned up as features land
- Static files need to be properly collected and served in production

## Next Work Session Plan: Endpoint-by-Endpoint Parity

Goal: Reproduce the Rails user experience exactly, one endpoint at a time.

Process per endpoint:
- [analyze-data-prep] Read Rails route, controller/module helpers, and any POROs to understand data-prep for the endpoint.
- [implement-data-prep] Implement equivalent data-prep in Django, placing logic in `vivo_app/lib/` helpers; keep view functions <50 lines as managers.
- [analyze-response] Review Rails templates (HTML/ERB), CSS, and JS to capture the expected structure/behavior; recognize that live data/APIs may be unavailable in dev.
- [template-parity] Create/update Django templates to mirror Rails output as closely as possible with the available data/context.
- [tests] Add/extend `TestCase` assertions to validate context keys, JSON output (when applicable), and basic HTML structure where feasible.

Constraints and preferences:
- Do not implement improvements that could change the user-visible output; instead, add them to this plan under an "Improvements Backlog" for later consideration.
- Proceed strictly one view-function at a time to keep focus and parity high.
- Keep using `uv run` for all commands.

### Definition of Done per Endpoint
- [ ] Route resolves and matches Rails path and trailing-slash semantics
- [ ] View function is ≤ 50 lines and delegates data-prep to `vivo_app/lib/...`
- [ ] Template returns near-identical structure/fields to the Rails ERB for that endpoint
- [ ] JSON parity supported for dotted extension (e.g., `.json`) and `?format=json` where applicable
- [ ] Tests cover HTTP status, key context keys, JSON shape, and minimal HTML markers
- [ ] Errors logged; respects `render_or_stub()` and caching when introduced

### Mock Data Strategy
- When live API/DB/Solr data are unavailable, use minimal, deterministic stubs in tests (not in views). Prefer representative structures derived from Rails templates. Do not ship fixtures that alter UI output; parity remains the priority.

### Session Checkpoint Routine
- After each endpoint (or a significant subtask), update this plan with:
  - Completed work
  - Any new “things to remember” (decisions, assumptions, follow-ups)
  - Next broad steps (if they’ve changed)
  - The next two “specific-things” to work on
- While working, when you reach a third distinct “specific-thing,” pause and perform the same update before proceeding (rolling checkpoint).
- Continue to use `uv run` for commands.

## Progress Checkpoint (2025-08-24 12:49 EDT)

- Completed: Minimal faculty page panels
  - Created `vivo_app/templates/vivo/people/includes/left_panel.html` and `vivo_app/templates/vivo/people/includes/right_panel.html`
  - Integrated into `vivo_app/templates/display/show.html` for people profiles
  - Added test `vivo_app/tests/test_display.py::DisplayShowTests.test_display_people_panels_render`
  - Test run completed successfully via `uv run ./manage.py test -v 2`

- Notes
  - Reviewed Rails parity in `OBSOLETE/app/views/faculty/_show_left_panel.html.erb`, `_show_right_panel.html.erb`, and `OBSOLETE/app/views/faculty/show.html.erb`
  - Will align structure (classes/IDs) and tabs progressively to match Rails while keeping views thin

- Next two specific tasks
  1. Align left/right panel includes with Rails structure (e.g., `col-md-3/col-md-9`, `#individual-intro`, `#section_overview`) and add minimal tab button markup in left panel
  2. Extend `vivo_app/lib/display.py::build_display_context()` to provide minimal additional fields (e.g., `title`, `email`, and flags like `has_publications`) using deterministic stubs

## Progress Checkpoint (2025-08-24 13:09 EDT)

- Completed: Extended display context for people profiles
  - Updated `vivo_app/lib/display.py::build_display_context()` to include:
    - `presenter.faculty.display_name`, `title`, `email`, `overview`, `thumbnail`, `hidden`, `cv_link`
    - collections: `affiliations`, `research_areas`, `on_the_web`
    - presenter flags: `has_publications`, `has_research`, `has_background`, `has_affiliations`, `has_teaching`, `has_details`
  - Verified via `uv run ./manage.py test -v 2` — all tests passing

- Notes
  - Keys mirror Rails presenter usage in `faculty/_show_left_panel.html.erb` and `faculty/_show_right_panel.html.erb`; values are deterministic stubs for offline parity.

- Next two specific tasks
  1. Add minimal right-panel tab placeholders (Publications, Research, Background, Affiliations, Teaching) with proper IDs only (no behavior yet)
  2. Gate left-panel tab buttons via presenter flags to match Rails conditions (e.g., show Publications only when `has_publications`)

## Progress Checkpoint (2025-08-24 13:22 EDT)

- Completed: Right-panel tab placeholders and left-panel tab gating
  - Added minimal sections with IDs: `tabPublications`, `tabResearch`, `tabBackground`, `tabAffiliations`, `tabTeaching` in `vivo_app/templates/vivo/people/includes/right_panel.html`
  - Gated left-panel tab buttons in `vivo_app/templates/vivo/people/includes/left_panel.html` via presenter flags (`has_*`) and `edit_mode`
  - Verified all tests pass via `uv run ./manage.py test -v 2`

- Next two specific tasks
  1. Add tests asserting tab button visibility based on flags and presence of placeholder sections
  2. Begin wiring basic tab switching behavior (progressive enhancement; minimal JS/no data changes)

## Progress Checkpoint (2025-08-24 13:52 EDT)
 
- Completed: Tab-visibility tests and progressive enhancement for tab switching
  - Added tests in `vivo_app/tests/test_display.py`:
    - `test_display_people_panels_render` asserts default left-panel button gating and presence of right-panel placeholders (`#tabOverview`, `#tabPublications`, `#tabResearch`, `#tabBackground`, `#tabAffiliations`, `#tabTeaching`).
    - `test_display_people_tab_buttons_all_off` patches `vivo_app.views.build_display_context` to turn all flags off; only Overview button remains.
    - `test_display_people_tab_buttons_edit_mode_shows_all` patches with `edit_mode=True`; all buttons visible.
  - Implemented minimal JS for tab switching: `vivo_app/static/js/tabs.js` (progressive enhancement; no-JS fallback shows all sections).
  - Wired script via `{% block extra_js %}` in `vivo_app/templates/display/show.html`.
  - Test run completed successfully via `uv run ./manage.py test -v 2`.
 
- Notes
  - JS only runs when `#people-right-panel` and `#tabButtons` are present; server-side gating remains authoritative.
  - Maintains graceful fallback: without JS, all tab sections remain visible.
 
- Next two specific tasks
  1. Extract right-panel tab sections into individual includes (e.g., `vivo_app/templates/vivo/people/includes/tabs/*.html`) mirroring Rails partials, without changing markup or content.
  2. Add minimal CSS to style the active tab button (using existing `.active`), matching Rails look while avoiding structural changes.

## Progress Checkpoint (2025-08-24 13:57 EDT)

- Completed: Extracted right-panel tabs into includes and added minimal active-tab CSS
  - Extracted `#tabOverview`, `#tabPublications`, `#tabResearch`, `#tabBackground`, `#tabAffiliations`, `#tabTeaching` into includes under `vivo_app/templates/vivo/people/includes/tabs/`.
  - Updated `vivo_app/templates/vivo/people/includes/right_panel.html` to include the new partials, preserving IDs and structure.
  - Added minimal CSS for active tab button in `vivo_app/static/css/style.css` to visibly indicate the active state.
  - Test run completed successfully via `uv run ./manage.py test -v 2`.

- Next two specific tasks
  1. Extend `vivo_app/static/js/tabs.js` to support URL hash deep-linking for tab state (initial selection, update hash on click, handle `#All`).
  2. Add minimal focus styles for tab buttons to improve keyboard accessibility, aligning with Rails look without structural changes.

### Improvements Backlog (record only; do not implement yet)
- To be populated as we review each Rails endpoint (e.g., CSS consolidation, JS modularization, accessibility fixes, minor performance tweaks) — deferred to avoid altering user experience during parity phase.
