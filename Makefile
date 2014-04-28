.PHONY:all
all:
	./gamec test.game

.PHONY:ast
ast:
	python ast.py test.game

.PHONY:scan
scan:
	python scan.py test.game

.PHONY:clean
clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py
