.PHONY:all
all:
	python game.py

.PHONY:clean
clean:
	rm -f *.pyc ply/*.pyc
