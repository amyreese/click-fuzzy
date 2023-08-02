install:
	python -m pip install -Ue .[dev]

.venv:
	python -m venv .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to activate virtualenv'

venv: .venv

test:
	python -m unittest -v click_fuzzy
	python -m mypy -p click_fuzzy

lint:
	python -m flake8 click_fuzzy
	python -m ufmt check click_fuzzy

format:
	python -m ufmt format click_fuzzy

release: lint test clean
	flit publish

clean:
	rm -rf .mypy_cache build dist html *.egg-info

distclean: clean
	rm -rf .venv
