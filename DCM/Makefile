# Makefile for running the Pacemaker

PYTHON=python3  
SCRIPT=./Code/PacemakerUI.py 
CACHE_DIR=./Languages

run:
	$(PYTHON) $(SCRIPT)

clean:
	rm -f *.pyc
	rm -rf __pycache__
	cd $(CACHE_DIR) && rm -f *.pyc && rm -rf __pycache__

.PHONY: run clean
