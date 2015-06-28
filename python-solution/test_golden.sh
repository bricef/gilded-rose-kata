#!/bin/bash

diff -u golden.txt <(python texttest_fixture.py)
