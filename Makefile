.PHONY:all
all: test.game.py
	python test.game.py

test.game.py: test.game syscalls.py
	./gamec -o test.game

clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py *.game.py *.game.temp
