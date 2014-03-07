.PHONY:all
all:
	python test.py

.PHONY:clean
clean:
	rm -f *.pyc ply/*.pyc
