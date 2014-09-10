.PHONY:all
all: gamec

.PHONY:serve
serve: demo_programs/serve.game.py
	python demo_programs/serve.game.py

demo_programs/serve.game.py: demo_programs/serve.game gamec
	./gamec -o demo_programs/serve.game

.PHONY:mid_range
mid_range: demo_programs/mid_range.game.py
	python demo_programs/mid_range.game.py

demo_programs/mid_range.game.py: demo_programs/mid_range.game gamec
	./gamec -o demo_programs/mid_range.game

.PHONY:avg_aces
avg_aces: demo_programs/avg_aces.game.py
	python demo_programs/avg_aces.game.py

demo_programs/avg_aces.game.py: demo_programs/avg_aces.game gamec
	./gamec -o demo_programs/avg_aces.game

.PHONY:sykes
sykes: demo_programs/sykes.game.py
	python demo_programs/sykes.game.py

demo_programs/sykes.game.py: demo_programs/sykes.game gamec
	./gamec -o demo_programs/sykes.game

.PHONY:curry
curry: demo_programs/curry.game.py
	python demo_programs/curry.game.py

demo_programs/curry.game.py: demo_programs/curry.game gamec
	./gamec -o demo_programs/curry.game

gamec:
	make -C DevOps

clean:
	rm -f parsetab.py *.out *.pyc ply/*.pyc test.game test.game.py *.game.py *.game.temp demo_programs/*.game.py
