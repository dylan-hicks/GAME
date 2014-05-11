.PHONY:all
all: test.game.py
	python test.game.py

test.game.py: test.game syscalls.py gamec game.py
	./gamec -o test.game

.PHONY:serve
serve: serve.game.py
	python serve.game.py

serve.game.py:
	./gamec -o serve.game

.PHONY:mid_range
mid_range: mid_range.game.py
	python mid_range.game.py

mid_range.game.py:
	./gamec -o mid_range.game

.PHONY:avg_aces
avg_aces: avg_aces.game.py
	python avg_aces.game.py

avg_aces.game.py:
	./gamec -o avg_aces.game

.PHONY:sykes
sykes: sykes.game.py
	python sykes.game.py

sykes.game.py:
	./gamec -o sykes.game

.PHONY:sykes2
sykes2: sykes2.game.py
	python sykes2.game.py

sykes2.game.py:
	./gamec -o sykes2.game

.PHONY:curry
curry: curry.game.py
	python curry.game.py

curry.game.py:
	./gamec -o curry.game

gamec:
	make -C DevOps

clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py *.game.py *.game.temp
