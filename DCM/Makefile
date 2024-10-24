# Makefile for running the Pacemaker

PYTHON=python3  
SCRIPT=./Code/PacemakerUI.py 
LANG_DIR=./Languages
CODE_DIR=./Code

run:
	$(PYTHON) $(SCRIPT)

clean:
	rm -f *.pyc
	rm -rf __pycache__
	cd $(CODE_DIR) && rm -f *.pyc && rm -rf __pycache__\
	cd $(LANG_DIR) && rm -f *.pyc && rm -rf __pycache__

.PHONY: run clean
