PROJECT_NAME = screen_crawling

venv:
	source venv/bin/active

lint:
	pylint $(PROJECT_NAME)

lab:
	jupyter-notebook

close:
	deactivate