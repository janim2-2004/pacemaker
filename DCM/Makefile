# Makefile for running the Pacemaker

PYTHON=python3  
SCRIPT=main.py 
LANG_DIR=./Languages

run:
	$(PYTHON) $(SCRIPT)

clean:
	rm -f *.pyc
	rm -rf __pycache__
	cd $(CODE_DIR) && rm -f *.pyc && rm -rf __pycache__\

.PHONY: run clean
