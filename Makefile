.PHONY:all
all:
	./gamec -o test.game

.PHONY:temp
temp:
	python temp.py test2.game

.PHONY:test
test: temp
	python test.game.py

.PHONY:ast
ast:
	python ast.py test.game

.PHONY:scan
scan:
	python scan2.py test.game

.PHONY:clean
clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py
