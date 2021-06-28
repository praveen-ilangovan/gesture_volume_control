# Makefile for Gesture Volume Control

# make check -> to run mypy
# make run -> to run the module

# Python installer
PYTHON = py

# Runs by default when no target is specified
.DEFAULT_GOAL = all

help:
	${PYTHON} -m src --help

check:
	mypy src

run:
	${PYTHON} -m src

all: check run