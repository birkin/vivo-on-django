Experimental conversion of front-end VIVO Rails app to Django.

# running tests...

all:
`uv run ./manage.py test -v 2`

app-only:
`uv run ./manage.py test vivo_app -v 2`

SPARQL integration tests (when online):
`VIVO_API_ONLINE=1 uv run ./manage.py test -v 2`
