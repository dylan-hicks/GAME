.PHONY:all
all:
	python game.py test.game

.PHONY:ast
ast:
	python ast.py test.game

.PHONY:clean
clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py
