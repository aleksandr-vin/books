all: build

build-in-docker:
	docker build --tag book .
	docker run --rm --tty \
		--volume $(shell pwd):/book/ \
		book

build:
	python book.py
	pandoc -t epub3 -o output.epub book.html
