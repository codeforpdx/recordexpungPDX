.PHONY: install run clean

install:
	pipenv install '-e .'

run: install
	pipenv run flask run

clean:
	find . -type f -name \*~ | xargs rm
	find . -type f -name \*pyc | xargs rm
	rm -rf src/backend/*.egg-info

test:
	pipenv run pytest
