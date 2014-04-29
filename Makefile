.PHONY:all
all:
	./gamec -o test.game

.PHONY:temp
temp:
	python temp.py test.game

.PHONY:test
test:
	python test.game.py

.PHONY:ast
ast:
	python ast.py test.game

.PHONY:scan
scan:
	python scan.py test.game

.PHONY:clean
clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py
