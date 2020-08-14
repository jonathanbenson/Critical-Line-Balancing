

class Node :

    def __init__(self, name, time) :

        self.name = name
        self.time = time

class Blob :

    def __init__(self, initialNode) :

        self.nodes = list()

        self.nodes.append(initialNode)
        

    def time(self) :

        t = 0

        for node in self.nodes :

            t += node.time

        return t

    def merge(self, other) :

        self.nodes.extend(other.nodes)


class Line :

    def __init__(self, initialBlobs) :

        self.blobs = initialBlobs

    def merge(self, i) :

        self.blobs[i].merge(self.blobs[i + 1])

        self.blobs.pop(i + 1)

    def leadTime(self) :

        lt = 0

        for blob in self.blobs :

            lt += blob.time()

        return lt

    
    def bottleneck(self) :
        ''' returns the time of the slowest blob '''
        
        m = self.blobs[0].time()

        for b in self.blobs :

            if m < b.time() :

                m = b.time()

        return m


    def sph(self) :

        return 3600 / self.bottleneck()

    def efficiency(self) :

        optimalCycleTime = self.leadTime() / len(self.blobs)

        optimalSPH = 3600 / optimalCycleTime
        
        return self.sph() / optimalSPH


    

while True :

    try :

        reader = open("ts/" + input("Enter the 6-digit seat number:") + ".txt", 'r')

    except :

        print("Error.")
        continue

    break


fLines = reader.readlines()




tsNodes = list()

for fLine in fLines :

    splitLine = fLine.split('\t')

    tsNodes.append(Node(splitLine[0], float(splitLine[1])))


reader.close()



initialLine = Line([Blob(node) for node in tsNodes])

possibleLines = list()
possibleLines.append(initialLine)





































        
