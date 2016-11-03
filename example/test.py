from ontospy import *
try:
	G = Graph("pizza.owl")
except:
	print "Error"
print G.classes
