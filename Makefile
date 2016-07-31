.PHONY: docs, test

docs:
	${MAKE} -C ../docs html

test:
	py.test --flake8 --isort --cov=mu

watch:
	ptw --flake8 --isort --onpass "say Passed" --onfail "say Failed"
