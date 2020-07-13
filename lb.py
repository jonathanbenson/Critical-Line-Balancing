
import math
import copy

import matplotlib.pyplot as plt


class Node :

	def __init__(self, name, time, next) :


		self.name = name
		self.time = time
		self.next = next

		

	def split(self, n) :
        
		nodes = list()

		for i in range(n) :
            
			nodes.append(Node(self.name, self.time/n, self.next if i == n - 1 else True))

		return nodes

	def __add__(self, other) :

		return Node(self.name + ' ' + other.name if other.name not in self.name else self.name, self.time + other.time, other.next)

	

class Line :

	def __init__(self, nodes, n) :

		self.nodes = nodes

		self.n = n

	def setup(self) :

		while len(self.nodes) > self.n :

			self.merge()

		while len(self.nodes) < self.n : 

			self.split()


	def leadTime(self) :
        # lead time based on the provided nodes (never changes during splits/merges)

		lt = 0

		for node in self.nodes :

			lt += node.time

		return lt

	def mean(self) :

		return self.leadTime() / len(self.nodes)


	def standardDeviation(self) :

		squareDifferenceSum = 0

		for node in self.nodes :

			squareDifferenceSum += math.pow(node.time - self.mean(), 2)

		return math.sqrt(squareDifferenceSum / len(self.nodes))



	def split(self) :

		maxI = 0

		for i, node in enumerate(self.nodes) :
            
			if node.time > self.nodes[maxI].time :

				maxI = i

		maxNode = self.nodes[maxI]

		self.nodes.pop(maxI)

		splitNodes = maxNode.split(2)

		for i, node in enumerate(splitNodes) :

			self.nodes.insert(maxI + i, node)


	def merge(self) :

		minI = 0

		for i in range(len(self.nodes) - 1) :

			if (self.nodes[i].time + self.nodes[i + 1].time < self.nodes[minI].time + self.nodes[minI + 1].time) and self.nodes[i].next == True  :

				minI = i

		mergedNode = self.nodes[minI] + self.nodes[minI + 1]

		self.nodes.pop(minI)
		self.nodes.pop(minI)

		self.nodes.insert(minI, mergedNode)


	def balance(self) :

		

		
		
		lastSD = self.standardDeviation()
		currentSD = lastSD - 1

		while currentSD < lastSD :
			
			lastSD = self.standardDeviation()

			self.merge()
			self.split()
			
			
			currentSD = self.standardDeviation()

			

	def smooth(self) :
		# any stations that are repeated and have different times, it averages them out
		
		counts = dict()
		totals = dict()

		for node in self.nodes :

			try :

				counts[node.name] += 1

			except KeyError :

				counts[node.name] = 1

			try :

				totals[node.name] += node.time

			except KeyError :

				totals[node.name] = node.time

		
		for i in range(len(self.nodes)) :

			self.nodes[i].time = totals[self.nodes[i].name] / counts[self.nodes[i].name]

		
	

	def __str__(self) :



		output = str()


		     
		for node in self.nodes :

			output += node.name + ' ' + str(node.time) + '\n'

			

		output += str(len(self.nodes)) + " operators running " + str(self.seatsPerHour()) + " seats an hour at " + str(self.efficiency()) + "% efficiency\n"
		output += "Standard Deviation : " + str(self.standardDeviation()) + '\n'

		output += "----------------------------------------------\n"

		return output


	def seatsPerHour(self) :

		maxTime = self.nodes[0].time

		for node in self.nodes :

			if node.time > maxTime :

				maxTime = node.time

		return round(3600 // maxTime)



	def efficiency(self) :

		optimalSeatsPerHour = 3600 / (self.leadTime() / self.n)

		return round((self.seatsPerHour() / optimalSeatsPerHour) * 100)


x = list()
y = list()

lines = list()

for i in range(5, 20) :

    
	nodes = list()

	'''
	#186771
	nodes.append(Node("BELLOWS", 79, True))
	nodes.append(Node("TRACKS", 105, True))
	nodes.append(Node("EVC", 119, True))
	nodes.append(Node("BACK FRAME", 124, False))
	nodes.append(Node("BACK FOAM", 41, True))
	nodes.append(Node("BACK COVER", 110, False))
	nodes.append(Node("CUSHION FOAM", 40, True))
	nodes.append(Node("CUSHION COVER", 115, False))
	nodes.append(Node("RODS/DIALS", 113, True))
	nodes.append(Node("ARMS/SB", 114, True))
	nodes.append(Node("TESTER", 35, False))
	nodes.append(Node("PACKING 1", 95, True))
	nodes.append(Node("PACKING 2", 69, True))
	nodes.append(Node("PACKING 3", 45, None))
	'''

	'''
	#186530
	nodes.append(Node("SWITCH/LABELS", 43, True))
	nodes.append(Node("LOAD FRAMES", 23, False))
	nodes.append(Node("BACK FOAM", 24, True))
	nodes.append(Node("BACK COVER", 95, False))
	nodes.append(Node("CUSHION FOAM", 24, True))
	nodes.append(Node("CUSHION COVER", 69, False))
	nodes.append(Node("LEFT ARM", 27, True))
	nodes.append(Node("RIGHT ARM", 27, True))
	nodes.append(Node("TESTER", 42, False))
	nodes.append(Node("PACKAGING 1", 87, True))
	nodes.append(Node("PACKAGING 2", 40, None))
	'''

	'''
	#186984
	nodes.append(Node("TRACKS/LABELS", 86, True))
	nodes.append(Node("SWITCH/LOAD", 67, False))
	nodes.append(Node("BACK FOAM", 37, True))
	nodes.append(Node("BACK COVER", 81, False))
	nodes.append(Node("CUSHION FOAM", 41, True))
	nodes.append(Node("CUSHION COVER", 55, False))
	nodes.append(Node("LEFT ARM", 29, True))
	nodes.append(Node("RIGHT ARM", 27, True))
	nodes.append(Node("TESTER", 84, False))
	nodes.append(Node("PACKAGING 1", 56, True))
	nodes.append(Node("PACKAGING 2", 61, True))
	nodes.append(Node("PACKAGING 3", 139, None))
	'''

	'''
	#186755
	nodes.append(Node("BELLOWS", 98, True))
	nodes.append(Node("TRACKS", 68, True))
	nodes.append(Node("EVC", 107, False))
	nodes.append(Node("BACK FRAME", 146, False))
	nodes.append(Node("BACK FOAM", 32, True))
	nodes.append(Node("BACK COVER", 142, False))
	nodes.append(Node("CUSHION FOAM", 37, True))
	nodes.append(Node("CUSHION COVER", 106, False))
	nodes.append(Node("RODS/DIALS", 131, False))
	nodes.append(Node("LEFT ARM", 61, True))
	nodes.append(Node("RIGHT ARM", 63, True))
	nodes.append(Node("TESTER", 22, True))
	nodes.append(Node("HEAD REST", 45, False))
	nodes.append(Node("QUALITY INSPECTION", 39, True))
	nodes.append(Node("PACKAGING 1", 38, True))
	nodes.append(Node("PACKAGING 2", 26, True))
	nodes.append(Node("PACKAGING 3", 35, None))
	'''

	'''
	#186810
	nodes.append(Node("LABEL/TRACKS", 95, False))
	nodes.append(Node("LOAD/FRAME", 58, False))
	nodes.append(Node("BACK FOAM", 39, True))
	nodes.append(Node("CUSHION FOAM", 43, False))
	nodes.append(Node("BACK COVER", 186, True))
	nodes.append(Node("CUSHION COVER", 100, False))
	nodes.append(Node("LEFT ARM", 33, True))
	nodes.append(Node("RIGHT ARM", 33, False))
	nodes.append(Node("TESTER", 28, False))
	nodes.append(Node("PACKAGING A", 69, True))
	nodes.append(Node("PACKAGING B", 132, None))
	'''

	#187085
	nodes.append(Node("BELLOWS", 86, True))
	nodes.append(Node("TRACKS", 83, False))
	nodes.append(Node("EVC", 89, False))
	nodes.append(Node("BACK FRAME", 36, False))
	nodes.append(Node("BACK FOAM", 53, True))
	nodes.append(Node("BACK COVER", 139, False))
	nodes.append(Node("CUSHION FOAM", 42, True))
	nodes.append(Node("CUSHION COVER", 74, False))
	nodes.append(Node("RODS/DIALS", 77, False))
	nodes.append(Node("LEFT ARM", 39, True))
	nodes.append(Node("RIGHT ARM", 36, True))
	nodes.append(Node("TESTER", 49, False))
	nodes.append(Node("QUALITY INSPECTION", 93, True))
	nodes.append(Node("PACKAGING 1", 51, True))
	nodes.append(Node("PACKAGING 2", 36, True))
	nodes.append(Node("PACKAGING 3", 88, None))
	


	line = Line(nodes, i)

	line.setup()


	line.balance()

	line.smooth()

	x.append(i)
	y.append(line.seatsPerHour())

	print(line, end = "")

	lines.append(line)


lines.sort(key = lambda line: line.efficiency(), reverse = True)

for line in lines :

	print("%d people running %d seats an hour at %d percent efficiency" % (line.n, line.seatsPerHour(), line.efficiency()))

plt.plot(x, y)
plt.show()
