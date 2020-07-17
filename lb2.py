
import math
import copy

import matplotlib.pyplot as plt


class Node :

	def __init__(self, name, time, nxt) :
		self.name = name
		self.time = time
		self.next = nxt



	
class Blob :

	def __init__(self, n) :

		self.nodes = n

	def time(self) :

		total = 0

		for node in self.nodes :

			total += node.time

		return total

	def length(self) :

		return len(self.nodes)

	def merge(self, other) :

		cNodes = copy.deepcopy(self.nodes)

		for node in other.nodes :

			cNodes.append(node)


		return Blob(cNodes)

	def split(self) :

		if self.length() == 1 :

			n = self.nodes[0]

			return [Blob([Node(n.name, n.time / 2, True)]), Blob([Node(n.name, n.time / 2, n.next)])]

		elif self.length() == 2 :

			return [Blob([self.nodes[0]]), Blob([self.nodes[1]])]

		elif self.length() > 2 :

			half = self.time() / 2

			splitI = int()

			counter = 0

			for i, node in enumerate(self.nodes) :
				
				lastCounter = counter

				counter += node.time

				if counter >= half :

					if abs(counter) < abs(lastCounter) :

						splitI = i

					else :

						splitI = i - 1

					break

			return [Blob(self.nodes[:splitI]), Blob(self.nodes[splitI:])]


	def splitRating(self) :

		return self.time() - abs(self.split()[0].time() - self.split()[1].time())

	



class Line :

	def __init__(self, blobs, n) :

		self.blobs = blobs

		self.n = n

	def bottleneck(self) :

		bn = self.blobs[0]

		for blob in self.blobs :

			if blob.time() > bn.time() :

				bn = blob

		return bn

	

	def length(self) :

		return len(self.blobs)

	def leadTime(self) :

		lt = 0

		for blob in self.blobs :

			lt += blob.time()

		return lt

	def mean(self) :

		return self.leadTime() / self.length()


	def standardDeviation(self) :

		squareDifferenceSum = 0

		for blob in self.blobs :

			squareDifferenceSum += math.pow(blob.time() - self.mean(), 2)

		return math.sqrt(squareDifferenceSum / self.length())

	
	def split(self) :

		bestI = 0

		for i, blob in enumerate(self.blobs) :

			if blob.splitRating() > self.blobs[bestI].splitRating() :

				bestI = i

		bestBlob = self.blobs[bestI]

		print("Split:", ' '.join([n.name for n in bestBlob.nodes]))

		self.blobs.pop(bestI)


		for i, blob in enumerate(bestBlob.split()) :

			self.blobs.insert(bestI + i, blob)

	def merge(self) :

		minI = 0

		
		for i in range(len(self.blobs) - 1) :

		
			if (self.blobs[i].time() + self.blobs[i + 1].time() < self.blobs[minI].time() + self.blobs[minI + 1].time()) and self.blobs[i].nodes[-1].next == True  :

				minI = i

		print("Merge:", ' '.join([n.name for n in self.blobs[minI].nodes]), '-', ' '.join([n.name for n in self.blobs[minI + 1].nodes]))
		mergedBlob = self.blobs[minI].merge(self.blobs[minI + 1])

		
		
		self.blobs.pop(minI)
		self.blobs.pop(minI)

		

		self.blobs.insert(minI, mergedBlob)


	
	def setup(self) :

		while self.length() > self.n :

			self.merge()

		while self.length() < self.n : 

			self.split()

	def balance(self) :

		print(self.n)
		
		lastSD = self.standardDeviation()
		currentSD = lastSD - 1

		while currentSD < lastSD :

			
			lastSD = self.standardDeviation()

			self.merge()
			self.split()

			currentSD = self.standardDeviation()

			print(currentSD, lastSD)



	def seatsPerHour(self) :

		maxTime = self.blobs[0].time()

		for blob in self.blobs :

			if blob.time() > maxTime :

				maxTime = blob.time()

		return round(3600 / maxTime)



	
	def efficiency(self) :

		return round((self.seatsPerHour() / (3600 / (self.leadTime() / self.n))) * 100)



	


	def output(self) :

		print("--------------------------------------------")
		for blob in self.blobs :

			print(str(blob.time()) + ('*' if blob.time() == self.bottleneck().time() else ''))

			for node in blob.nodes :

				print('\t' + node.name + ' ' + str(node.time))

		print()
		print("Standard Deviation:", round(self.standardDeviation(), 2), "| Bottleneck:", self.bottleneck().time())
		print(self.n, "operators running at", self.efficiency(), "percent efficiency")
		print("---------------------------------------------")

x = list()
y = list()

lines = list()

for i in range(5, 20) :

	blobs = list()


	#186810
	blobs.append(Blob([Node("LABEL/TRACKS", 95, True)]))
	blobs.append(Blob([Node("LOADING FRAMES", 58, False)]))
	blobs.append(Blob([Node("BACK FOAM", 39, True)]))
	blobs.append(Blob([Node("CUSHION FOAM", 43, False)]))
	blobs.append(Blob([Node("BACK COVER", 186, True)]))
	blobs.append(Blob([Node("CUSHION COVER", 100, False)]))
	blobs.append(Blob([Node("ARMS", 66, True)]))
	blobs.append(Blob([Node("TESTER", 28, False)]))
	blobs.append(Blob([Node("PACKAGING A", 69, True)]))
	blobs.append(Blob([Node("PACKAGING B", 132, None)]))


	line = Line(blobs, i)

	line.setup()


	line.balance()


	line.output()

	lines.append(line)

	x.append(line.n)
	y.append(line.efficiency())
	

lines.sort(key = lambda l: l.efficiency(), reverse = True)
for line in lines :

	print(line.n, "operators running", line.seatsPerHour(), "seats per hour at", line.efficiency(), "percent efficiency")

plt.plot(x, y)
plt.xlabel("Operators")
plt.ylabel("Efficiency")
plt.show()