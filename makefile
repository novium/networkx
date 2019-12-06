PYTHON := python3
TEST_DIR := networkx/testing

.PHONY: test
test:
	$(PYTHON) -m unittest discover $(TEST_DIR)

.PHONY: coverage
coverage:
	coverage run -m unittest discover $(TEST_DIR)
	coverage html
