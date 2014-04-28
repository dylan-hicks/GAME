class Dude:
	age = 0.0
	name = ""
	isCool = False
	p = []
	def build(self, a):
		self.age = a
		height = "house"
		self.name = "will"
		self.p = [4.0, 3.0, 2.0, 1.0]
		self.p.append(5.0)
		self.p.insert(int(1.0), 10.0)
		
		j = 0.0
		i = 13.2
		while (j <= 4.0) && (i > 2.1):
			temp = self.p[int(j)]
			print(temp)

			j = j + 1.0
			i = i + 1.0



	def addTen(self):
		self.age = self.age + 10.0
		removed = self.p.pop(int(1.0))
		print(removed)


def main():
	bob = Dude()
	bob.build(12.0)
	bob.addTen()

if __name__ == '__main__':main()