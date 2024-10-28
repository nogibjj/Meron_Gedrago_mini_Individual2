# Makefile for Rust Project


all: check build format lint test

check:
	cargo check

build:
	cargo build

format:
	cargo fmt

lint:
	cargo clippy

test:
	cargo test

release:
	cargo build --release


#Makefile for python 
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=main --cov=mylib test_*.py

format:	
	black *.py 

lint:
	ruff check *.py mylib/*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

		
all: install lint test format 
