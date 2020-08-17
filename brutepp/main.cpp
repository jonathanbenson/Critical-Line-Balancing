
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

struct Node {
	
	string name;
	double time;
	
	

};


struct Blob {
	
	vector<Node> nodes;
	
	double time();
	
	void merge(Blob);
	
	
};


struct Line {
	
	vector<Blob> blobs;
	
	void merge(unsigned int);
	
	double leadTime();
	
	double bottleneck();
	
	double sph();
	
	double efficiency();
	
};





int main() {
	
	
	// making a connection with the file
	
	ifstream reader;
	
	reader.open("ts\\186847.txt");
	
	
	
	if (!reader.good()) {
		
		cout << "Unable to open file." << endl;
		
	}
	else {
		
		cout << "Opening file successful." << endl;
		
	}
	
	
	
	
	
	// reading the file and populating nodes
	
	vector<Node> tsNodes;
	
	Node tempNode;
	
	while (reader.good()) {
		
		reader >> tempNode.name;
		reader >> tempNode.time;
		
		tsNodes.push_back(tempNode);
		
	}
	
	
	reader.close();
	
	
	
	
	
	// main algorithm
	
	
	
	// creating an initial line with the time study nodes
	// each blob in the line will corrospond to one blob in the line
	Line initialLine;
	Blob tempBlob;
	
	for (int i = 0; i < tsNodes.size(); ++i) {
		
		tempBlob.nodes.clear();
		
		tempBlob.nodes.push_back(tsNodes[i]);
		
		initialLine.blobs.push_back(tempBlob);
		
		cout << initialLine.blobs.back().nodes[0].name << endl;
		
	}
	
	vector<Line> possibleLines;
	
	possibleLines.push_back(initialLine);
	
	// at this point I have a line where each blob corrosponds to one node of the time study
	
	
	
	
	
	return 0;
}



// Node member functions




// Blob member functions

	
double Blob::time() {
	
	double t = 0;
	
	for (int i = 0; i < nodes.size(); ++i) {
		
		t += nodes[i].time;
		
	}
	
	return t;
	
}
	
void Blob::merge(Blob other) {
	
	for (int i = 0; i < other.nodes.size(); ++i) {
		
		nodes.push_back(other.nodes[i]);
	}
}


// Line member functions


	
void Line::merge(unsigned int i) {
	
	blobs[i].merge(blobs[i + 1]);
	
	blobs.erase(blobs.begin() + i + 1);
	
}

double Line::leadTime() {
	
	double lt = 0;
	
	for (int i = 0; i < blobs.size(); ++i) {
		
		lt += blobs[i].time();
		
	}
	
	return lt;
	
}

double Line::bottleneck() {
	
	double bn = blobs[0].time();
	
	for (int i = 0; i < blobs.size(); ++i) {
		
		if (blobs[i].time() > bn) {
			
			bn = blobs[i].time();
			
		}
	}
	
	return bn;
	
}


double Line::sph() {
	
	return 3600 / bottleneck();
	
}

double Line::efficiency() {
	
	double optimalCycleTime = leadTime() / blobs.size();
	
	double optimalSPH = 3600 / optimalCycleTime;
	
	return (sph() / optimalSPH) * 100;
	
}










