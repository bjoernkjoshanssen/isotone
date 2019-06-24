from random import randint

import math
import time
import itertools
import operator

hat0 = [(0,1,2)]
hat1 = [(0,),(1,),(2,)]
p = [(0,)]
q = [(1,)]
r = [(2,)]
maj = [(0,1),(0,2),(1,2)]
emptyset = [()]
one = emptyset
a000 = hat0
a001 = [(0,1)]
a010 = [(0,2)]
a100 = [(1,2)]
a011 = [(0,1),(0,2)]
a101 = [(0,1),(1,2)]
a110 = [(0,2),(1,2)]
a111 = maj
b000 = maj
b001 = [(2,),(0,1)]
b010 = [(1,),(0,2)]
b100 = [(0,),(1,2)]
b011 = [(1,),(2,)]
b101 = [(0,),(2,)]
b110 = [(0,),(1,)]
b111 = hat1

f3minus = [ #19 elements
	hat0, a001, a010,
	a011, a100, a101,
	a110, maj,  b001,
	b010, b011, b100,
	b101, b110, hat1,
	p,q,r,
	one]

f3 = [[], #20 elements
	hat0, a001, a010,
	a011, a100, a101,
	a110, maj,  b001,
	b010, b011, b100,
	b101, b110, hat1,
	p,q,r,
	one]

mymap4Prelim = [
	[(1,1,1,1), hat1, emptyset],
	[(1,1,1,0), b110],
	[(1,1,0,1), b101],
	[(1,0,1,1), b011],
	[(1,1,0,0), p, b100],
	[(1,0,1,0), q, b010],
	[(1,0,0,1), r, b001],
	[(1,0,0,0), hat0, maj],
	[(0,1,1,1), maj],
	[(0,1,1,0), a110],
	[(0,1,0,1), a101],
	[(0,0,1,1), a011],
	[(0,1,0,0), hat0, a100],
	[(0,0,1,0), hat0, a010],
	[(0,0,0,1), hat0, a001],
	[(0,0,0,0), hat0]
]
for i in range(0, len(mymap4Prelim)):
	if len(mymap4Prelim[i]) == 2: #if we didn't bother to write the same thing twice
		mymap4Prelim[i] = [mymap4Prelim[i][0], mymap4Prelim[i][1], mymap4Prelim[i][1]]
mymap4 = mymap4Prelim



def subset(G, F): # (0,1) subset of (0,1,2)
	g = set(G)
	f = set(F)
	return g.issubset(f)
	#or maybe:
	#return all((a in F) for a in G) # a bit slower... 21.55 seconds vs. 20.37 seconds

def purge(L):
	#input: [(0, 3), (1, 3), (2, 3), (0,), (1,), (2,)]
	#output: [(0,), (1,), (2,)]
	for F in L:
		for G in L:
			if F != G and subset(F,G):
				L = [H for H in L if H != G]
	return L

#print purge([(0, 3), (1, 3), (2, 3), (0,), (1,), (2,)])

def joinwiths(a,b): #takes a and b and returns s\wedge a \vee b
	return purge([F+(3,) for F in a] + b)


def total(amap,k):
	if len(amap) != 2**k:
		return False
	for seq in itertools.product((0,1),repeat=k):
		okay = False
		for i in range(0, len(amap)):
			if amap[i][0] == seq:
				okay = True
		if not okay:
			return False
	return True

def onto(amap,aset): #adequate map onto aset
	isOnto = True
	for thing in aset:
		okay = False
		for i in range(0, len(amap)):
			if amap[i][1] == thing:
				okay = True
			if amap[i][2] == thing:
				okay = True
		if not okay:
			print "missing " + str(thing)
			isOnto = False
	return isOnto

def ontoDirect(amap,aset):
	isOnto = True
	for thing in aset:
		okay = False
		for i in range(0, len(amap)):
			#if amap[i][1] == thing:
			if amap[i] == thing:
				okay = True
		if not okay:
			print "missing " + str(thing)
			isOnto =  False
	return isOnto

def trueDict(three, x):
	return tuple(i for i in x if i != three) #without the "tuple" cast it becomes a generator object somehow.

def setTrue(three, L):
	return [trueDict(three, F) for F in L]

#print setTrue(3, [(0,2,3),(0,1)])
#raise SystemExit

def setFalse(three, L):
	return [F for F in L if not three in F]

mymap6 = [
	[(0,0,0,0,0,0), a000, hat0],
	[(0,0,0,0,0,1), a000, r],
	[(0,0,0,0,1,0), a000, q],
	[(0,0,0,0,1,1), a000, b011],
	[(0,0,0,1,0,0), a000, p],
	[(0,0,0,1,0,1), a000, b101],
	[(0,0,0,1,1,0), a000, b110],
	[(0,0,0,1,1,1), a000, b111],
	[(0,0,1,0,0,0), a001, b000],
	[(0,0,1,0,0,1), a001, b001],
	[(0,0,1,0,1,0), a001, b010],
	[(0,0,1,0,1,1), a001, b011],
	[(0,0,1,1,0,0), a001, b100],
	[(0,0,1,1,0,1), a001, b101],
	[(0,0,1,1,1,0), a001, b110],
	[(0,0,1,1,1,1), a001, b111],
	[(0,1,0,0,0,0), a010, b000],
	[(0,1,0,0,0,1), a010, b001],
	[(0,1,0,0,1,0), a010, b010],
	[(0,1,0,0,1,1), a010, b011],
	[(0,1,0,1,0,0), a010, b100],
	[(0,1,0,1,0,1), a010, b101],
	[(0,1,0,1,1,0), a010, b110],
	[(0,1,0,1,1,1), a010, b111],
	[(0,1,1,0,0,0), a011, b000],
	[(0,1,1,0,0,1), a011, b001],
	[(0,1,1,0,1,0), a011, b010],
	[(0,1,1,0,1,1), a011, b011],
	[(0,1,1,1,0,0), a011, b100],
	[(0,1,1,1,0,1), a011, b101],
	[(0,1,1,1,1,0), a011, b110],
	[(0,1,1,1,1,1), a011, b111],
	[(1,0,0,0,0,0), a100, b000],
	[(1,0,0,0,0,1), a100, b001],
	[(1,0,0,0,1,0), a100, b010],
	[(1,0,0,0,1,1), a100, b011],
	[(1,0,0,1,0,0), a100, b100],
	[(1,0,0,1,0,1), a100, b101],
	[(1,0,0,1,1,0), a100, b110],
	[(1,0,0,1,1,1), a100, b111],
	[(1,0,1,0,0,0), a101, b000],
	[(1,0,1,0,0,1), a101, b001],
	[(1,0,1,0,1,0), a101, b010],
	[(1,0,1,0,1,1), a101, b011],
	[(1,0,1,1,0,0), a101, b100],
	[(1,0,1,1,0,1), a101, b101],
	[(1,0,1,1,1,0), a101, b110],
	[(1,0,1,1,1,1), a101, b111],
	[(1,1,0,0,0,0), a110, b000],
	[(1,1,0,0,0,1), a110, b001],
	[(1,1,0,0,1,0), a110, b010],
	[(1,1,0,0,1,1), a110, b011],
	[(1,1,0,1,0,0), a110, b100],
	[(1,1,0,1,0,1), a110, b101],
	[(1,1,0,1,1,0), a110, b110],
	[(1,1,0,1,1,1), a110, b111],
	[(1,1,1,0,0,0), a111, b000],
	[(1,1,1,0,0,1), a111, b001],
	[(1,1,1,0,1,0), a111, b010],
	[(1,1,1,0,1,1), a111, b011],
	[(1,1,1,1,0,0), a111, b100],
	[(1,1,1,1,0,1), a111, b101],
	[(1,1,1,1,1,0), a111, b110],
	[(1,1,1,1,1,1), a111, one], #one, not b111
]

mymap5 = [#use words abc dec. replace b001,b010,b100 by r,q,p and b111 by one
	[(0,0,0,0,0),a000,a000],#was b000
	[(0,0,0,0,1),a000,q],#b010
	[(0,0,0,1,0),a000,p],#b100
	[(0,0,0,1,1),a000,b110],
	[(0,0,1,0,0),a001,r],#b001
	[(0,0,1,0,1),a001,b011],
	[(0,0,1,1,0),a001,b101],
	[(0,0,1,1,1),a001,b111],
	[(0,1,0,0,0),a010,b000],
	[(0,1,0,0,1),a010,b010],
	[(0,1,0,1,0),a010,b100],
	[(0,1,0,1,1),a010,b110],
	[(0,1,1,0,0),a011,b001],
	[(0,1,1,0,1),a011,b011],
	[(0,1,1,1,0),a011,b101],
	[(0,1,1,1,1),a011,b111],
	[(1,0,0,0,0),a100,b000],
	[(1,0,0,0,1),a100,b010],
	[(1,0,0,1,0),a100,b100],
	[(1,0,0,1,1),a100,b110],
	[(1,0,1,0,0),a101,b001],
	[(1,0,1,0,1),a101,b011],
	[(1,0,1,1,0),a101,b101],
	[(1,0,1,1,1),a101,b111],
	[(1,1,0,0,0),a110,b000],
	[(1,1,0,0,1),a110,b010],
	[(1,1,0,1,0),a110,b100],
	[(1,1,0,1,1),a110,b110],
	[(1,1,1,0,0),a111,b001],
	[(1,1,1,0,1),a111,b011],
	[(1,1,1,1,0),a111,b101],
	[(1,1,1,1,1),a111,one],#b111
]


myMap4ToF3 = [
	[(0,0,0,0),a000],
	[(0,0,1,0),a001],
	[(0,1,0,0),a010],
	[(0,1,1,0),a011],
	[(1,0,0,0),a100],
	[(1,0,1,0),maj],
	[(1,1,0,0),a110],
	[(1,1,1,0),b111],
	[(0,0,0,1),a101],
	[(0,0,1,1),b001],
	[(0,1,0,1),b010],
	[(0,1,1,1),b011],
	[(1,0,0,1),b100],
	[(1,0,1,1),b101],
	[(1,1,0,1),b110],
	[(1,1,1,1),one],
]



def compareHumanComputer():
	computermap6 = [
		[(0, 0, 0, 0, 0, 0),  [(0, 1, 2, 3)]],
		[(0, 0, 0, 0, 0, 1),  [(0, 1, 2)]],
		[(0, 0, 0, 0, 1, 0),  [(0, 1, 3)]],
		[(0, 0, 0, 1, 0, 0),  [(1, 2, 3)]],
		[(0, 0, 1, 0, 0, 0),  [(0, 2, 3)]],
		[(0, 1, 0, 0, 0, 0),  [(0, 1, 3), (0, 1, 2)]],
		[(1, 0, 0, 0, 0, 0),  [(0, 2, 3), (0, 1, 2)]],
		[(0, 0, 0, 0, 1, 1),  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]],
		[(0, 0, 0, 1, 0, 1),  [(1, 2, 3), (0, 1, 2)]],
		[(0, 0, 1, 0, 0, 1),  [(0, 2)]],
		[(0, 1, 0, 0, 0, 1),  [(0, 1)]],
		[(1, 0, 0, 0, 0, 1),  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]],
		[(0, 0, 0, 1, 1, 0),  [(0, 1, 3), (1, 2, 3)]],
		[(0, 0, 1, 0, 1, 0),  [(0, 1, 3), (0, 2, 3)]],
		[(0, 1, 0, 0, 1, 0),  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]],
		[(1, 0, 0, 0, 1, 0),  [(0, 2, 3), (0, 1)]],
		[(0, 0, 1, 1, 0, 0),  [(0, 2, 3), (1, 2, 3)]],
		[(0, 1, 0, 1, 0, 0),  [(1, 2, 3), (0, 1)]],
		[(1, 0, 0, 1, 0, 0),  [(1, 2, 3), (0, 2)]],
		[(0, 1, 1, 0, 0, 0),  [(0, 1, 3), (0, 2)]],
		[(1, 0, 1, 0, 0, 0),  [(0, 2, 3), (1, 2)]],
		[(1, 1, 0, 0, 0, 0),  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]],
		[(0, 0, 0, 1, 1, 1),  [(0, 2, 3), (1, 2, 3), (0, 1)]],
		[(0, 0, 1, 0, 1, 1),  [(0, 1), (0, 2)]],
		[(0, 1, 0, 0, 1, 1),  [(1, 2, 3), (0, 1), (0, 2)]],
		[(1, 0, 0, 0, 1, 1),  [(0, 2, 3), (0, 1), (1, 2)]],
		[(0, 0, 1, 1, 0, 1),  [(0, 2), (1, 2)]],
		[(0, 1, 0, 1, 0, 1),  [(0, 1), (1, 2)]],
		[(1, 0, 0, 1, 0, 1),  [(0, 1, 3), (1, 2, 3), (0, 2)]],
		[(0, 1, 1, 0, 0, 1),  [(0, 3), (0, 1), (0, 2)]],
		[(1, 0, 1, 0, 0, 1),  [(0, 1, 3), (0, 2), (1, 2)]],
		[(1, 1, 0, 0, 0, 1),  [(2, 3), (0, 1)]],
		[(0, 0, 1, 1, 1, 0),  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]],
		[(0, 1, 0, 1, 1, 0),  [(1, 3), (0, 1)]],
		[(1, 0, 0, 1, 1, 0),  [(0, 1), (0, 2), (1, 2)]],
		[(0, 1, 1, 0, 1, 0),  [(2, 3), (0, 1, 3), (0, 2)]],
		[(1, 0, 1, 0, 1, 0),  [(2, 3), (0, 1), (1, 2)]],
		[(1, 1, 0, 0, 1, 0),  [(1, 3), (0, 2, 3), (0, 1)]],
		[(0, 1, 1, 1, 0, 0),  [(2, 3), (0, 1), (0, 2)]],
		[(1, 0, 1, 1, 0, 0),  [(2, 3), (0, 2), (1, 2)]],
		[(1, 1, 0, 1, 0, 0),  [(1, 3), (0, 1), (0, 2)]],
		[(1, 1, 1, 0, 0, 0),  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]],
		[(0, 0, 1, 1, 1, 1),  [(2, 3), (0, 1), (0, 2), (1, 2)]],
		[(0, 1, 0, 1, 1, 1),  [(1, 3), (0, 1), (0, 2), (1, 2)]],
		[(1, 0, 0, 1, 1, 1),  [(0, 3), (0, 1), (0, 2), (1, 2)]],
		[(0, 1, 1, 0, 1, 1),  [(0, 3), (2, 3), (0, 1), (0, 2)]],
		[(1, 0, 1, 0, 1, 1),  [(2,), (0, 1)]],
		[(1, 1, 0, 0, 1, 1),  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]],
		[(0, 1, 1, 1, 0, 1),  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]],
		[(1, 0, 1, 1, 0, 1),  [(0, 1, 3), (2,)]],
		[(1, 1, 0, 1, 0, 1),  [(2, 3), (1,), (0, 2)]],
		[(1, 1, 1, 0, 0, 1),  [(0, 3), (2,), (0, 1)]],
		[(0, 1, 1, 1, 1, 0),  [(1, 3), (2, 3), (0, 1), (0, 2)]],
		[(1, 0, 1, 1, 1, 0),  [(1, 3), (2,), (0, 1)]],
		[(1, 1, 0, 1, 1, 0),  [(1,), (0, 2)]],
		[(1, 1, 1, 0, 1, 0),  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]],
		[(1, 1, 1, 1, 0, 0),  [(1,), (2,)]],
		[(0, 1, 1, 1, 1, 1),  [(0, 3), (1, 3), (2,), (0, 1)]],
		[(1, 0, 1, 1, 1, 1),  [(0, 3), (1,), (2,)]],
		[(1, 1, 0, 1, 1, 1),  [(2, 3), (0,), (1,)]],
		[(1, 1, 1, 0, 1, 1),  [(1, 3), (0,), (2,)]],
		[(1, 1, 1, 1, 0, 1),  [(0,), (1,), (2,)]],
		[(1, 1, 1, 1, 1, 0),  [(3,), (1,), (2,)]],
		[(1, 1, 1, 1, 1, 1),  [()]]
	]



	print "Let's compare the human-discovered mymap6 to the computer-found one."
	#for myword in itertools.product((0,1),repeat=6):
	for k in range(0, len(mymap6)):
		for l in range(0, len(computermap6)):
			if mymap6[k][0] == computermap6[l][0]:
				print "Human:" +str((mymap6[k][0],joinwiths(mymap6[k][2],mymap6[k][1])))
				print "Compu:" +str((computermap6[l][0], computermap6[l][1]))
				print
				if joinwiths(mymap6[k][2],mymap6[k][1]) == computermap6[l][1]:
					print "Eureka"
	#print "Or maybe:"
	#for k in range(0, len(mymap6)):
	#	print (mymap6[k][0],joinwiths(mymap6[k][1],mymap6[k][2]))


#def hypercubeorder(x,y): #same as "dominated()"
#	if len(x) != len(y):
#		print "Cannot compare distinct length words."
#		raise SystemExit
#	#print "\t\tComparing " + str(x) + " to " + str(y)
#	for i in range(0,len(x)):
#		if x[i] > y[i]:
#			return False
#	return True

def antichainorder(I,J): #might be much faster to just use a lookup table here?
	return all(
		[
			any(
				[subset(G, F) for G in J]
			) for F in I
		]
	)
	#check whether each element of I contains an element of J
	#for F in I:
	#	okay = False
	#	for G in J:
	#		if subset(G, F):
	#			okay = True
	#			break
	#	if not okay:
	#		return False
	#return True

def checkIsotonic(mymap):
	for i in range(0, len(mymap)):
		for j in range(0, len(mymap)):
			if i != j:
				#print "\t" + str(j)
				if dominated(mymap[i][0],mymap[j][0]):
					#print
					#print str(mymap[i][0]) + " <= " + str(mymap[j][0]),
					if not antichainorder(mymap[i][1],mymap[j][1]) or not antichainorder(mymap[i][2],mymap[j][2]):
						print "Failed"
						print mymap[i]
						print mymap[j]
						raise SystemExit
					#print ": OK."
	print "The map is isotonic."

def checkIsotonicDirect(mymap):
	for i in range(0, len(mymap)):
		for j in range(0, len(mymap)):
			if i != j:
				if dominated(mymap[i][0],mymap[j][0]):
					#print
					#print str(mymap[i][0]) + " <= " + str(mymap[j][0]),
					if not antichainorder(mymap[i][1],mymap[j][1]):
						print "Failed"
						print mymap[i]
						print mymap[j]
						raise SystemExit
					#print ": OK."
	print "The map is isotonic."

def isotonyReport():
	print "Is mymap4 onto? " + str(onto(mymap4, f3minus)) + "\n"
	print "Is mymap5 onto? " + str(onto(mymap5, f3minus)) + "\n"
	print "Is mymap6 onto? " + str(onto(mymap6, f3minus)) + "\n"

	print "Is mymap4 total? " + str(total(mymap4, 4)) + "\n"
	print "Is myMap4ToF3 total? " + str(total(myMap4ToF3, 4)) + "\n"

	print "Is mymap5 total? " + str(total(mymap5, 5)) + "\n"
	print "Is mymap6 total? " + str(total(mymap6, 6)) + "\n"

	print "mymap4 isotonic: "
	checkIsotonic(mymap4)
	print "myMap4ToF3 isotonic: "
	checkIsotonicDirect(myMap4ToF3)
	print "mymap5 isotonic: "
	checkIsotonic(mymap5)
	print "mymap6 isotonic: "
	checkIsotonic(mymap6)

def dominated(x,y):
	return all([x[i]<=y[i] for i in range(0, len(x))])
	#for i in range(0, len(x)):
	#	if x[i] > y[i]:
	#		return False
	#return True

def reportembedding(g):
	print
	for k in range(0, len(words)):
		print " g(" + str(words[k]) + ") = " +str(g[k])
	print str(g)
	#print ontoDirect(g,f4)

def updegree(a,b):
	degree = 0
	for aa in f3:
		for bb in f3:
			if antichainorder(bb,aa):
				if antichainorder(a,aa) and antichainorder(b,bb):
					degree += 1
	return degree

def updegreeF3(a):
	degree = 0
	for aa in f3:
		if antichainorder(a,aa):
			degree += 1
	return degree


#def printupdegreesF3():
#	for a in f3:
#		print "[" + str(a) + ", "+str(updegreeF3(a)) + "]"

#printupdegreesF3()
#raise SystemExit

updegreesF3 = [
	[[], 20],
	[[(0, 1, 2)], 19],
	[[(0, 1)], 14],
	[[(0, 2)], 14],
	[[(1, 2)], 14],
	[[(0, 1), (0, 2)], 11],
	[[(0, 1), (1, 2)], 11],
	[[(0, 2), (1, 2)], 11],
	[[(0, 1), (0, 2), (1, 2)], 9],
	[[(0,)], 6],
	[[(1,)], 6],
	[[(2,)], 6],
	[[(2,), (0, 1)], 5],
	[[(1,), (0, 2)], 5],
	[[(0,), (1, 2)], 5],
	[[(1,), (2,)], 3],
	[[(0,), (2,)], 3],
	[[(0,), (1,)], 3],
	[[(0,), (1,), (2,)], 2],
	[[()], 1]
]

#def printupdegrees():
#	print "Updegrees:"
#	for a in f3:
#		for b in f3:
#			if antichainorder(b,a):
#				print "[" + str(joinwiths(a,b)) + ", " + str(updegree(a,b)) + "],"

#using Output of printupdegrees():
updegrees = [
	[[()], 1],
	[[(3,), (0,), (1,), (2,)], 2],
	[[(0,), (1,), (2,)], 3],
	[[(3,), (1,), (2,)], 3],
	[[(3,), (0,), (2,)], 3],
	[[(3,), (0,), (1,)], 3],
	[[(0, 3), (1,), (2,)], 5],
	[[(1, 3), (0,), (2,)], 5],
	[[(2, 3), (0,), (1,)], 5],
	[[(3,), (2,), (0, 1)], 5],
	[[(3,), (1,), (0, 2)], 5],
	[[(3,), (0,), (1, 2)], 5],
	[[(1,), (2,)], 6],
	[[(0,), (2,)], 6],
	[[(0,), (1,)], 6],
	[[(3,), (0,)], 6],
	[[(3,), (1,)], 6],
	[[(3,), (2,)], 6],
	[[(0, 3), (1, 3), (2,), (0, 1)], 9],
	[[(0, 3), (2, 3), (1,), (0, 2)], 9],
	[[(1, 3), (2, 3), (0,), (1, 2)], 9],
	[[(3,), (0, 1), (0, 2), (1, 2)], 9],
	[[(1, 3), (2,), (0, 1)], 11],
	[[(2, 3), (1,), (0, 2)], 11],
	[[(0, 3), (2,), (0, 1)], 11],
	[[(2, 3), (0,), (1, 2)], 11],
	[[(0, 3), (1,), (0, 2)], 11],
	[[(1, 3), (0,), (1, 2)], 11],
	[[(1, 3), (2, 3), (0,)], 11],
	[[(0, 3), (2, 3), (1,)], 11],
	[[(0, 3), (1, 3), (2,)], 11],
	[[(3,), (0, 1), (0, 2)], 11],
	[[(3,), (0, 1), (1, 2)], 11],
	[[(3,), (0, 2), (1, 2)], 11],
	[[(2,), (0, 1)], 14],
	[[(1,), (0, 2)], 14],
	[[(2, 3), (1,)], 14],
	[[(1, 3), (2,)], 14],
	[[(0,), (1, 2)], 14],
	[[(2, 3), (0,)], 14],
	[[(0, 3), (2,)], 14],
	[[(1, 3), (0,)], 14],
	[[(0, 3), (1,)], 14],
	[[(3,), (0, 1)], 14],
	[[(3,), (0, 2)], 14],
	[[(3,), (1, 2)], 14],
	[[(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], 17],
	[[(0, 1, 3), (2,)], 19],
	[[(0, 2, 3), (1,)], 19],
	[[(1, 2, 3), (0,)], 19],
	[[(3,), (0, 1, 2)], 19],
	[[(0,)], 20],
	[[(1,)], 20],
	[[(2,)], 20],
	[[(3,)], 20],
	[[(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], 21],
	[[(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], 21],
	[[(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], 21],
	[[(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], 21],
	[[(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], 21],
	[[(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], 21],
	[[(1, 3), (2, 3), (0, 1), (0, 2)], 26],
	[[(0, 3), (2, 3), (0, 1), (1, 2)], 26],
	[[(0, 3), (1, 3), (0, 2), (1, 2)], 26],
	[[(2, 3), (0, 1), (0, 2), (1, 2)], 27],
	[[(1, 3), (0, 1), (0, 2), (1, 2)], 27],
	[[(1, 3), (2, 3), (0, 1), (1, 2)], 27],
	[[(1, 3), (2, 3), (0, 2), (1, 2)], 27],
	[[(0, 3), (0, 1), (0, 2), (1, 2)], 27],
	[[(0, 3), (2, 3), (0, 1), (0, 2)], 27],
	[[(0, 3), (2, 3), (0, 2), (1, 2)], 27],
	[[(0, 3), (1, 3), (0, 1), (0, 2)], 27],
	[[(0, 3), (1, 3), (0, 1), (1, 2)], 27],
	[[(0, 3), (1, 3), (2, 3), (0, 1)], 27],
	[[(0, 3), (1, 3), (2, 3), (0, 2)], 27],
	[[(0, 3), (1, 3), (2, 3), (1, 2)], 27],
	[[(2, 3), (0, 1), (0, 2)], 35],
	[[(2, 3), (0, 1), (1, 2)], 35],
	[[(1, 3), (0, 1), (0, 2)], 35],
	[[(1, 3), (0, 2), (1, 2)], 35],
	[[(1, 3), (2, 3), (0, 1)], 35],
	[[(1, 3), (2, 3), (0, 2)], 35],
	[[(0, 3), (0, 1), (1, 2)], 35],
	[[(0, 3), (0, 2), (1, 2)], 35],
	[[(0, 3), (2, 3), (0, 1)], 35],
	[[(0, 3), (2, 3), (1, 2)], 35],
	[[(0, 3), (1, 3), (0, 2)], 35],
	[[(0, 3), (1, 3), (1, 2)], 35],
	[[(0, 1), (0, 2), (1, 2)], 36],
	[[(1, 3), (2, 3), (1, 2)], 36],
	[[(0, 3), (2, 3), (0, 2)], 36],
	[[(0, 3), (1, 3), (0, 1)], 36],
	[[(2, 3), (0, 1, 3), (0, 2), (1, 2)], 37],
	[[(1, 3), (0, 2, 3), (0, 1), (1, 2)], 37],
	[[(0, 3), (1, 2, 3), (0, 1), (0, 2)], 37],
	[[(0, 3), (1, 3), (2, 3), (0, 1, 2)], 37],
	[[(0, 3), (1, 3), (2, 3)], 39],
	[[(0, 3), (0, 1), (0, 2)], 39],
	[[(1, 3), (0, 1), (1, 2)], 39],
	[[(2, 3), (0, 2), (1, 2)], 39],
	[[(2, 3), (0, 1)], 48],
	[[(1, 3), (0, 2)], 48],
	[[(0, 3), (1, 2)], 48],
	[[(1, 2, 3), (0, 1), (0, 2)], 50],
	[[(0, 2, 3), (0, 1), (1, 2)], 50],
	[[(0, 1, 3), (0, 2), (1, 2)], 50],
	[[(2, 3), (0, 1, 3), (0, 2)], 50],
	[[(2, 3), (0, 1, 3), (1, 2)], 50],
	[[(1, 3), (0, 2, 3), (0, 1)], 50],
	[[(1, 3), (0, 2, 3), (1, 2)], 50],
	[[(1, 3), (2, 3), (0, 1, 2)], 50],
	[[(0, 3), (1, 2, 3), (0, 1)], 50],
	[[(0, 3), (1, 2, 3), (0, 2)], 50],
	[[(0, 3), (2, 3), (0, 1, 2)], 50],
	[[(0, 3), (1, 3), (0, 1, 2)], 50],
	[[(0, 1), (0, 2)], 53],
	[[(0, 1), (1, 2)], 53],
	[[(0, 2), (1, 2)], 53],
	[[(1, 3), (2, 3)], 53],
	[[(0, 3), (2, 3)], 53],
	[[(0, 3), (1, 3)], 53],
	[[(0, 3), (0, 1)], 53],
	[[(0, 3), (0, 2)], 53],
	[[(1, 3), (0, 1)], 53],
	[[(1, 3), (1, 2)], 53],
	[[(2, 3), (0, 2)], 53],
	[[(2, 3), (1, 2)], 53],
	[[(0, 2, 3), (1, 2, 3), (0, 1)], 73],
	[[(0, 1, 3), (1, 2, 3), (0, 2)], 73],
	[[(0, 1, 3), (0, 2, 3), (1, 2)], 73],
	[[(2, 3), (0, 1, 3), (0, 1, 2)], 73],
	[[(1, 3), (0, 2, 3), (0, 1, 2)], 73],
	[[(0, 3), (1, 2, 3), (0, 1, 2)], 73],
	[[(0, 2, 3), (0, 1)], 78],
	[[(0, 1, 3), (0, 2)], 78],
	[[(1, 2, 3), (0, 1)], 78],
	[[(0, 1, 3), (1, 2)], 78],
	[[(1, 2, 3), (0, 2)], 78],
	[[(0, 2, 3), (1, 2)], 78],
	[[(2, 3), (0, 1, 3)], 78],
	[[(1, 3), (0, 2, 3)], 78],
	[[(0, 3), (1, 2, 3)], 78],
	[[(0, 3), (0, 1, 2)], 78],
	[[(1, 3), (0, 1, 2)], 78],
	[[(2, 3), (0, 1, 2)], 78],
	[[(0, 1)], 84],
	[[(0, 2)], 84],
	[[(1, 2)], 84],
	[[(0, 3)], 84],
	[[(1, 3)], 84],
	[[(2, 3)], 84],
	[[(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], 114],
	[[(0, 1, 3), (0, 2, 3), (0, 1, 2)], 123],
	[[(0, 1, 3), (1, 2, 3), (0, 1, 2)], 123],
	[[(0, 2, 3), (1, 2, 3), (0, 1, 2)], 123],
	[[(0, 1, 3), (0, 2, 3), (1, 2, 3)], 123],
	[[(0, 1, 3), (0, 1, 2)], 134],
	[[(0, 2, 3), (0, 1, 2)], 134],
	[[(0, 1, 3), (0, 2, 3)], 134],
	[[(1, 2, 3), (0, 1, 2)], 134],
	[[(0, 1, 3), (1, 2, 3)], 134],
	[[(0, 2, 3), (1, 2, 3)], 134],
	[[(0, 1, 2)], 148],
	[[(0, 1, 3)], 148],
	[[(0, 2, 3)], 148],
	[[(1, 2, 3)], 148],
	[[(0, 1, 2, 3)], 167],
	[[], 168]
]
def theupdegree(u):
	for i in range(0, len(updegrees)):
		if updegrees[i][0] == u:
			return updegrees[i][1]

def theupdegreeF3(u):
	for i in range(0, len(updegreesF3)):
		if updegreesF3[i][0] == u:
			return updegreesF3[i][1]

def basicCheck(u,i,g,words,setofmonotonefunctions):
	#binarylength = len(words[0])
	return all(
		not(
			(g[j] == u) or (dominated(words[j],words[i]) and not antichainorder(g[j],u))
		) for j in range(0,i)
	)

	#for j in range(0, i): # g[j] is an earlier value of g and we need g[i] above g[j] if words[i] is above words[j]
	#	if g[j] == u:
	#		return False
	#	if dominated(words[j],words[i]):
	#		if not antichainorder(g[j],u):
	#			return False
	#	#The following may be a good idea long term, but it is slow short term:
	#	#updegreeOfJoinij = 2**(binarylength-sum([max(words[j][k],words[i][k]) for k in range(0, binarylength)]))
	#	#enoughSpaceAbove = False
	#	#for v in setofmonotonefunctions:#it is bad if v, the join of g[j] and u, is too high up. I.e. if all elements above g[j] and u have too small updegree.
	#	#	if antichainorder(u,v) and antichainorder(g[j],v) and theupdegree(v) >= updegreeOfJoinij:
	#	#		enoughSpaceAbove = True
	#	#		break
	#	#if not enoughSpaceAbove:
	#	#	return False
	#return True


def ontoAdequate(L,setofmonotonefunctions):
	if setofmonotonefunctions == f4:
		setVar = 3
	else:
		setVar = 2
	myset = set()
	for F in L:
		myset.add(
			tuple(
				sorted(
					purge(
						setTrue(setVar, F)
					),
					key=lambda tup: hash(tup)
				)
			)
		)
		# https://stackoverflow.com/a/34375589/803990 well problem with that is what if the tuple has smaller length... so i use hash instead of len(tup), tup[0], tup[1]
		myset.add(tuple(sorted(list(set(setFalse(setVar, F))), key=lambda tup: hash(tup)))) #
	#if (setofmonotonefunctions == f4 and len(myset))>=15: # in the context of binarylength=5 it seems 18 is usually achieved.
	#	print "Onto a set of size " + str(len(myset))
	#	for u in f3:
	#		print u, (tuple(u) in myset)
	if (setofmonotonefunctions == f4 and len(myset)>=20) or (setofmonotonefunctions == f3 and len(myset)>5):
		#print myset
		print "Onto a set of size " + str(len(myset))
		if setofmonotonefunctions == f4:
			for u in f3:
				print u, (tuple(u) in myset)
				#print "Is " + str(u) + " in " + str(myset) + " ?"
		#print L
		#print words
		print
	if (setofmonotonefunctions == f4 and len(myset) >= 20) or (setofmonotonefunctions == f3 and len(myset) >= 6): #where 20 is the size of f3 and 6 the size of f2
		return True


def recursiveEmbedding(gOld, setofmonotonefunctions, words, i):
	binarylength = len(words[0])
	g = gOld
	if i>0 and g[i-1] == [()]:
		#print "already reached top"
		return
	if i>=0:#to adjust printing frequency
		hashy = hash(str(g)) % 100
		if hashy >= 99: #to reduce printing frequency
			print str(i) + ", Hash " + str(hash(str(g)) % 100)
			#print "We are still at " + str(g[0:24])
		if (
			(setofmonotonefunctions == f4 and binarylength == 7 and (i>=117 or (i>=117 and ontoAdequate(g,setofmonotonefunctions))))
			or
			(setofmonotonefunctions == f4 and binarylength == 6 and (i>=64 or (i>=63 and ontoAdequate(g,setofmonotonefunctions))))#easily find one with i=63(really 64) but it's not ontoAdequate
			or
			(setofmonotonefunctions == f4 and binarylength == 5 and (i>=32 or (i>=2 and ontoAdequate(g,setofmonotonefunctions))))#easily find i=32 but ontoAdequacy only 18
			or
			(setofmonotonefunctions == f4 and binarylength == 4 and (i>=16 or (i>=2 and ontoAdequate(g,setofmonotonefunctions))))#onto 14 easily achieved
			or
			(setofmonotonefunctions == f3 and binarylength == 5 and (i>=18 or (i>=17 and ontoAdequate(g,setofmonotonefunctions)))) #this doesn't make that sense as these can't be 1:1 #i=17 ontoadequate is easy for words5
			or
			(setofmonotonefunctions == f3 and binarylength == 4 and (i>=16 or (i>=16 and ontoAdequate(g,setofmonotonefunctions))))
		):
			print "A sample function for i=" + str(i)
			for j in range(0, i+1):
				print words[j], ": ", g[j]
			print g
			print
			#print "OntoAdequate, i=" + str(i) #ontoadequate, i=107 easily found
			
			#raise SystemExit
		#print words[0:i+1]
		#raise SystemExit
	#print "i is " + str(i)
	
	mytime = time.time()
	for l in range(0, len(setofmonotonefunctions)): # u is a potential value for g[i]
		if i==1:
			print str(round(100*l/float(len(setofmonotonefunctions)),2)) + " per cent done"
		u = setofmonotonefunctions[l]
		newtime = time.time()
		#30/i takes 40 secs.
		#40/i takes 70 secs and produces nothing.
		#50/i as well (when not printing to screen)
		#100/i finds 97 (sometimes) and takes 100 seconds
		#200/i finds 98 (sometimes) and takes 300 seconds
		#400/i finds 106 and then somehow got stuck


		#if (i==1 and l != 6):
		#	continue # just because we've not looked at that much!

		#comment this out if you want to try all possibilities with no time-out.
		if (
			#l<i-105 or 
			(l>len(setofmonotonefunctions)*(1000/i)/float(4) or newtime - mytime > 10000/float(i))
		):# with newtime-mytime>60, it is done in 79 secs. With 1000/i, it finds examples with i=107 in 1308 seconds.
			#the "l<i" clause is weird... just trying something...
			#with 2000/i, it takes >2000 seconds but does not find as good an example!
			#500/i is not as good either, gives only i=98 and 700 seconds.
			#maybe 1000/i**2,1000/math.sqrt(i) is better? no, very bad.
			#print "i="+str(i)+" timed out"
			#amazingly, using 1000/float(i**2) [as opposed to without the float] we find another useful example. 1000000/float(i**3) is ok not great so is 1000/float(i*math.sqrt(i)
			break


		#use the following if you want to "perturb" the system a little:
		#not clear how it helps...
		#if randint(0,1000) == 1:
		#	break

		#print u
		#we should move on if u is not one of the minimal covers of the join of all g[j] it needs to be above.
		if u == []:
			continue
		updegreei = 2**(binarylength-sum(words[i]))

		#comment out this if want to get large embedding, even if provably can't extend all the way:
		#if setofmonotonefunctions == f4 and theupdegree(u) < updegreei: #CAN ADD: IF THE UPDEGREE, UPDEGREEI AND LEVEL OF CURRENT ONTONESS DO NOT SUFFICE FOR ULTIMATE ONTONESS THEN CONTINUE?
		#	continue
		#	#print str(u) + " was too big as a target for " + str(words[i])

		#if setofmonotonefunctions == f3 and theupdegreeF3(u) < updegreei:
		#	#print "the updegreeF3 of u=" + str(u) + " is " + str(theupdegreeF3(u))
		#	continue

		if not basicCheck(u,i,g,words,setofmonotonefunctions):
			continue
		badU = False
		#for uu in setofmonotonefunctions: #this may seem slow, but we really don't want to go into the recursive step unless we are pretty sure it's a good idea.
		#	#but it is not neccessarily clear that this uu business is even a valid thing to check for.
		#	if uu != u and basicCheck(uu,i,g,words,setofmonotonefunctions) and antichainorder(uu,u):
		#		badU = True
		#		break
		if not badU:
			g[i] = u
			#reportembedding(g)
			if i == len(words) - 1:
				#reportembedding(g)
				if ontoAdequate(g,setofmonotonefunctions):#this actually tries to check for onto f3 behavior
					print "Success"
					raise SystemExit
				continue # i.e., keep looking by going sideways rather than up in the tree of possible embeddings
			if i<len(words)-1:
				#print "g is " + str(g)
				recursiveEmbedding(g, setofmonotonefunctions, words, i+1)
	#we are here if we looked through all u, the embedding is total, but not onto. so then we want to just return.

def hamweight(w,n): #returns a list of all binary words of length n with hamming weight w
	if w == 0 and n==0:
		return [()]
	if w == 1 and n==0:
		return []
	if w == 0 and n == 1:
		return [(0,)]
	if w == 1 and n == 1:
		return [(1,)]
	if w == 0:
		return [x + (0,) for x in hamweight(w,n-1)]
	if w > 0 and n>0:
		return [x + (1,) for x in hamweight(w-1,n-1)] + [x + (0,) for x in hamweight(w,n-1)]
	return []

#def testhamweight():
#	for w in range(0, 5):
#		print
#		for n in range(w, 5):
#			print "Words of length " + str(n) + " having Hamming weight " + str(w) + ": "+ str(hamweight(w,n))
#	raise SystemExit

def linearizationOfInclusionOrderForBinaryWords(n):
	#Example: reduce(operator.add, [[1,2], [3,4], [5,6]]) == [1,2,3,4,5,6].
	return reduce(operator.add, [hamweight(i,n) for i in range(0, n+1)])

def probabilityForF4(F,words):
	count = 0
	for x in words:
		someAisGood = False
		for A in F:
			thisAisGood = True
			for i in A:
				if x[i] == 0:
					thisAisGood = False
					break #A was bad
			if thisAisGood:
				someAisGood = True
		if someAisGood:
			count += 1
			#print "satisfying assignment for " + str(F) + ": " + str(x)
	return count

words3 = linearizationOfInclusionOrderForBinaryWords(3)
words4 = linearizationOfInclusionOrderForBinaryWords(4)
words5 = linearizationOfInclusionOrderForBinaryWords(5)
words6 = linearizationOfInclusionOrderForBinaryWords(6)
words7 = linearizationOfInclusionOrderForBinaryWords(7)
#Equivalent to: words7 = hamweight(0, 7) + hamweight(1, 7) + hamweight(2, 7) + hamweight(3, 7) + hamweight(4, 7) + hamweight(5, 7) + hamweight(6, 7) + hamweight(7, 7)

words = words3 #0.64 seconds into f4
words = words4 #6.31 seconds into f4
words = words5 #42.23 seconds into f4... but only 1 seconds into f4minus after some June 18, 2019 retooling
words = words6 #366 seconds into f4. 817 seconds (15 minutes) into f4minus after some June 18, 2019 retooling; but that was before introducing the "purge".
words = words7 #well... there may be none... or maybe find one in 3000 seconds or 1 hour?

#print joinwiths(maj, a000)

#print probabilityForF4([(0, 1, 3), (0, 1, 2)], words)
#raise SystemExit

f4 = sorted([joinwiths(a,b) for a in f3 for b in f3 if antichainorder(b,a)],key = lambda F: probabilityForF4(F, words)) #sorting by probability helps guide our greedy algorithm in the right direction, hopefully!

#print len(f4)
#print f4
#raise SystemExit

#f4minus = f4[1:len(f4)] #not a good idea as the indexing gets messed up!
#print len(f4minus)

#def testjoinwiths():
#	print "Here are the " + str(len(f4)) + " elements of F4"
#	for ac in f4:
#		print str(ac)
#	#raise SystemExit

g = [one for w in words]

#to start with a promising beginning, perhaps:
#g[0:106] = [[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(1, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 1)], [(0, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3)], [(0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 3)], [(0, 2, 3), (1, 2, 3)], [(0, 3), (0, 1, 2)], [(1, 2, 3), (0, 2)], [(2, 3), (0, 1, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3)], [(0, 1), (0, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 3), (0, 1), (0, 2)], [(0, 2), (1, 2)], [(0, 3), (0, 2)], [(2, 3), (0, 2)], [(2, 3), (0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(2, 3), (1, 2)], [(1, 3), (0, 2)], [(0, 1), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3)], [(0, 3), (1, 2, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (2, 3)], [(2, 3), (0, 1)], [(2, 3), (0, 1, 3), (1, 2)], [(0, 3), (1, 3)], [(1, 3), (0, 1), (0, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(0, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3), (0, 1, 2)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(1, 3), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(0,), (1, 2)], [(1, 2, 3), (0,)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(2, 3), (0,)], [(0, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(2,)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 1, 3), (2,)], [(2,), (0, 1)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (2,)], [(1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3)], [(0, 3), (1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0,)], [(0, 3), (1, 3), (2,)], [(1, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(3,), (0, 2), (1, 2)], [(0, 3), (2, 3), (1,), (0, 2)], [(3,), (0, 1), (0, 2), (1, 2)], [(1, 3), (2, 3), (0,), (1, 2)], [(0,), (2,)], [(1, 3), (0,), (2,)], [(2, 3), (0,), (1,)], [(3,), (0,), (1, 2)], [(3,), (2,), (0, 1)], [(0, 3), (1,), (2,)]]
#print g
#recursiveEmbedding(g,f4,words,90)#for prefix of length 95 we verify in 35 seconds that no better than 106 exists. for 94 in 122 seconds.
#raise SystemExit

#for guided search with the ontoAdequate, i=108 example:
#g=[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(1, 2, 3)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 1)], [(0, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (1, 2, 3)], [(0, 1, 3), (0, 2)], [(0, 3)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3)], [(1, 2, 3), (0, 2)], [(2, 3), (0, 1, 3)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 1), (1, 2)], [(0, 1), (0, 2), (1, 2)], [(0, 3), (0, 1)], [(0, 1, 3), (0, 2), (1, 2)], [(0, 2), (1, 2)], [(2, 3), (0, 2)], [(2, 3), (0, 1), (0, 2)], [(2, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(1, 3), (0, 1), (0, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(2, 3), (0, 1, 3), (0, 1, 2)], [(0, 3), (1, 2, 3)], [(2, 3), (0, 1, 3), (0, 2)], [(0, 3), (2, 3)], [(1, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (1, 2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 3)], [(0, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (1, 2)], [(0, 3), (2, 3), (0, 2)], [(1, 3), (2, 3), (0, 1)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3)], [(1, 3), (2, 3), (0, 2)], [(0, 3), (0, 1), (1, 2)], [(1, 3), (0, 2, 3), (0, 1), (1, 2)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(0,), (1, 2)], [(2,), (0, 1)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(1, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1), (1, 2)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2,), (0, 1)], [(1, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (1,), (0, 2)], [(0, 1, 3), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(1,), (2,)], [(0, 3), (1,), (0, 2)], [(1, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1,)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2,)], [(0,), (2,)], [(2, 3), (1,)], [(0, 3), (2, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(0,), (1,)], [(1, 3), (0,), (2,)], [(0, 3), (1,), (2,)], [(2, 3), (0,), (1,)], [(0,), (1,), (2,)], [(1, 3), (2, 3), (0,), (1, 2)], [(3,), (2,), (0, 1)], [(3,), (0,), (2,)], [(3,), (1,), (2,)], [(3,), (0,), (1,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]
#recursiveEmbedding(g,f4,words,98)#for prefix of length 95 we verify in 35 seconds that no better than 106 exists. for 94 in 122 seconds.
#raise SystemExit

#g = [[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(1, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 2, 3), (0, 1, 2)], [(0, 1)], [(0, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(0, 2, 3), (0, 1)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3)], [(0, 1, 3), (0, 2)], [(0, 3)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(2, 3)], [(0, 3), (0, 1, 2)], [(2, 3), (0, 1, 3)], [(1, 2, 3), (0, 2)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(1, 3), (0, 2, 3)], [(0, 2, 3), (1, 2)], [(0, 1), (0, 2)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(1, 2, 3), (0, 1), (0, 2)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1), (0, 2)], [(0, 3), (0, 1)], [(0, 2, 3), (0, 1), (1, 2)], [(2, 3), (0, 2)], [(0, 3), (0, 2)], [(2, 3), (0, 1), (0, 2)], [(0, 2), (1, 2)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(2, 3), (1, 2)], [(0, 1), (0, 2), (1, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 1, 2)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (2, 3)], [(2, 3), (0, 1, 3), (0, 2)], [(1, 3), (0, 2)], [(0, 3), (1, 3)], [(2, 3), (0, 1, 3), (1, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3), (0, 1)], [(0, 3), (2, 3), (0, 1, 2)], [(1, 3), (2, 3)], [(2, 3), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2)], [(1, 3), (0, 2), (1, 2)], [(1, 3), (0, 2, 3), (0, 1), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(2,), (0, 1)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1)], [(2, 3), (0, 1), (1, 2)], [(0,), (1, 2)], [(0, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(2,)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (0, 2), (1, 2)], [(1, 3), (2,), (0, 1)], [(1,), (0, 2)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3), (0, 1), (1, 2)], [(2, 3), (1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1, 2)], [(0, 1, 3), (2,)], [(2, 3), (0,)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2)], [(1, 3), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(1,), (2,)], [(0, 3), (2, 3), (1,), (0, 2)], [(0, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0,), (1, 2)], [(3,), (0, 1), (0, 2), (1, 2)], [(0, 3), (1,), (2,)], [(0,), (2,)], [(1, 3), (0,), (2,)], [(3,), (2,), (0, 1)], [(0,), (1,)], [(3,), (0,), (2,)], [(0, 3), (2, 3), (1,)], [(0,), (1,), (2,)], [(2, 3), (0,), (1,)], [(0, 3), (1, 3), (2,)], [(3,), (1,), (2,)], [(3,), (0,), (1,), (2,)], [(3,), (1,), (0, 2)], [(1, 3), (2, 3), (0,)], [(3,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]
#recursiveEmbedding(g,f4,words,103)
#raise SystemExit

#To embed into f3:
#g[0]=[(0,1,2)]
#recursiveEmbedding(g,f3,words,1)
#raise SystemExit #works!

#to embed into f4minus:
g[0] = [(0,1,2,3,)]
recursiveEmbedding(g,f4,words,1)
raise SystemExit

recursiveEmbedding(g,f4,words,0)
raise SystemExit

recursiveEmbedding(g, f3minus,words, 0)
raise SystemExit


"""Here's an example of embedding the first 94 of the 128 binary strings into F4.
Is it something worth analyzing? It proves that monotone functions can be at least somewhat complicated.

Saving schedule:
11:40am June 21, 2019: 98
12:03pm June 21, 2019: 106
12:51pm realized we can tack on some of the top elements and get at least 108.
1:04pm converted that insight into an example for i=112. (112/128 = 7/8.)
1:42pm found one for i=112 which is onto a set of size 19 (missing only one of the "letters" p,q,r) hence we get a good complexity lower bound:
1:58pm found one which is ontoAdequate (ont a set of size 20) for i=107:
2:21pm found one for i=108, ontoAdequate.
note also that the ontoAdequate ones are more likely to be structurally similar to perfect i=128 ones.
so maybe use one of those for a "guided search" run.
3:20pm For embedding 2^6 into F4 we automatically found the following ontoAdequate example, perhaps mirroring the one in the paper:
Saturday
i=112 onto example for 2^7, F4 and i=113 example
i=116 example found (not onto)
12:23pm i=116 example found (onto)

Onto a set of size 20
[] True
[(0, 1, 2)] True
[(0, 1)] True
[(0, 2)] True
[(0, 1), (0, 2)] True
[(1, 2)] True
[(0, 1), (1, 2)] True
[(0, 2), (1, 2)] True
[(0, 1), (0, 2), (1, 2)] True
[(2,), (0, 1)] True
[(1,), (0, 2)] True
[(1,), (2,)] True
[(0,), (1, 2)] True
[(0,), (2,)] True
[(0,), (1,)] True
[(0,), (1,), (2,)] True
[(0,)] True
[(1,)] True
[(2,)] True
[()] True

A sample function for i=116
(0, 0, 0, 0, 0, 0, 0) :  [(0, 1, 2, 3)]
(0, 0, 0, 0, 0, 0, 1) :  [(0, 1, 2)]
(0, 0, 0, 0, 0, 1, 0) :  [(0, 1, 3)]
(0, 0, 0, 0, 1, 0, 0) :  [(0, 2, 3)]
(0, 0, 0, 1, 0, 0, 0) :  [(1, 2, 3)]
(0, 0, 1, 0, 0, 0, 0) :  [(0, 1, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 0) :  [(0, 1, 3), (0, 2, 3)]
(1, 0, 0, 0, 0, 0, 0) :  [(0, 2, 3), (0, 1, 2)]
(0, 0, 0, 0, 0, 1, 1) :  [(0, 1)]
(0, 0, 0, 0, 1, 0, 1) :  [(0, 2)]
(0, 0, 0, 1, 0, 0, 1) :  [(1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 1) :  [(0, 2, 3), (0, 1)]
(1, 0, 0, 0, 0, 0, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]
(0, 0, 0, 0, 1, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
(0, 0, 0, 1, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3)]
(0, 0, 1, 0, 0, 1, 0) :  [(0, 1, 3), (0, 2)]
(0, 1, 0, 0, 0, 1, 0) :  [(0, 3)]
(1, 0, 0, 0, 0, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]
(0, 0, 0, 1, 1, 0, 0) :  [(2, 3)]
(0, 0, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1, 2)]
(0, 1, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3)]
(1, 0, 0, 0, 1, 0, 0) :  [(1, 2, 3), (0, 2)]
(0, 0, 1, 1, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3)]
(1, 0, 0, 1, 0, 0, 0) :  [(0, 2, 3), (1, 2)]
(0, 1, 1, 0, 0, 0, 0) :  [(0, 1), (0, 2)]
(1, 0, 1, 0, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 2)]
(1, 1, 0, 0, 0, 0, 0) :  [(0, 2, 3), (1, 2, 3), (0, 1)]
(0, 0, 0, 0, 1, 1, 1) :  [(1, 2, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 0, 1, 1) :  [(1, 2, 3), (0, 1)]
(0, 0, 1, 0, 0, 1, 1) :  [(0, 3), (0, 1), (0, 2)]
(0, 1, 0, 0, 0, 1, 1) :  [(0, 3), (0, 1)]
(1, 0, 0, 0, 0, 1, 1) :  [(0, 2, 3), (0, 1), (1, 2)]
(0, 0, 0, 1, 1, 0, 1) :  [(2, 3), (0, 2)]
(0, 0, 1, 0, 1, 0, 1) :  [(0, 3), (0, 2)]
(0, 1, 0, 0, 1, 0, 1) :  [(2, 3), (0, 1), (0, 2)]
(1, 0, 0, 0, 1, 0, 1) :  [(0, 2), (1, 2)]
(0, 0, 1, 1, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (1, 2)]
(0, 1, 0, 1, 0, 0, 1) :  [(1, 3), (0, 2, 3), (0, 1)]
(1, 0, 0, 1, 0, 0, 1) :  [(2, 3), (1, 2)]
(0, 1, 1, 0, 0, 0, 1) :  [(0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2), (1, 2)]
(1, 1, 0, 0, 0, 0, 1) :  [(2, 3), (0, 1)]
(0, 0, 0, 1, 1, 1, 0) :  [(2, 3), (0, 1, 3), (0, 1, 2)]
(0, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 2)]
(0, 1, 0, 0, 1, 1, 0) :  [(0, 3), (2, 3)]
(1, 0, 0, 0, 1, 1, 0) :  [(2, 3), (0, 1, 3), (0, 2)]
(0, 0, 1, 1, 0, 1, 0) :  [(1, 3), (0, 2)]
(0, 1, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3)]
(1, 0, 0, 1, 0, 1, 0) :  [(2, 3), (0, 1, 3), (1, 2)]
(0, 1, 1, 0, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 0, 1, 0) :  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]
(1, 1, 0, 0, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1)]
(0, 0, 1, 1, 1, 0, 0) :  [(0, 3), (2, 3), (0, 1, 2)]
(0, 1, 0, 1, 1, 0, 0) :  [(1, 3), (2, 3)]
(1, 0, 0, 1, 1, 0, 0) :  [(2, 3), (0, 2), (1, 2)]
(0, 1, 1, 0, 1, 0, 0) :  [(0, 3), (2, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 1, 0, 0) :  [(0, 3), (0, 2), (1, 2)]
(1, 1, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 0, 0) :  [(1, 3), (0, 1), (0, 2)]
(1, 0, 1, 1, 0, 0, 0) :  [(1, 3), (0, 2), (1, 2)]
(1, 1, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3), (0, 1), (1, 2)]
(1, 1, 1, 0, 0, 0, 0) :  [(1, 3), (0, 1), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2)]
(0, 0, 1, 0, 1, 1, 1) :  [(0, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 0, 1, 1, 1) :  [(2,), (0, 1)]
(0, 0, 1, 1, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 0, 1, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1)]
(1, 0, 0, 1, 0, 1, 1) :  [(2, 3), (0, 1), (1, 2)]
(0, 1, 1, 0, 0, 1, 1) :  [(0,), (1, 2)]
(1, 0, 1, 0, 0, 1, 1) :  [(0, 3), (2,), (0, 1)]
(1, 1, 0, 0, 0, 1, 1) :  [(0, 3), (2, 3), (0, 1), (1, 2)]
(0, 0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 0, 1, 1, 0, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 0, 1) :  [(2,)]
(0, 1, 1, 0, 1, 0, 1) :  [(2, 3), (0,), (1, 2)]
(1, 0, 1, 0, 1, 0, 1) :  [(0, 3), (1, 3), (0, 2), (1, 2)]
(1, 1, 0, 0, 1, 0, 1) :  [(1, 3), (2,), (0, 1)]
(0, 1, 1, 1, 0, 0, 1) :  [(1,), (0, 2)]
(1, 0, 1, 1, 0, 0, 1) :  [(1, 3), (2, 3), (0, 2), (1, 2)]
(1, 1, 0, 1, 0, 0, 1) :  [(1, 3), (2, 3), (0, 1), (1, 2)]
(1, 1, 1, 0, 0, 0, 1) :  [(2, 3), (1,), (0, 2)]
(0, 0, 1, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2)]
(0, 1, 0, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1, 2)]
(1, 0, 0, 1, 1, 1, 0) :  [(0, 1, 3), (2,)]
(0, 1, 1, 0, 1, 1, 0) :  [(2, 3), (0,)]
(1, 0, 1, 0, 1, 1, 0) :  [(0, 3), (2,)]
(1, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 1, 0) :  [(0, 3), (1, 3), (0, 1), (0, 2)]
(1, 0, 1, 1, 0, 1, 0) :  [(1, 3), (2,)]
(1, 1, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)]
(1, 1, 1, 0, 0, 1, 0) :  [(0, 3), (1, 3), (2,), (0, 1)]
(0, 1, 1, 1, 1, 0, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)]
(1, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)]
(1, 1, 0, 1, 1, 0, 0) :  [(1,), (2,)]
(1, 1, 1, 0, 1, 0, 0) :  [(0, 3), (2, 3), (1,), (0, 2)]
(1, 1, 1, 1, 0, 0, 0) :  [(0, 3), (1,), (0, 2)]
(0, 0, 1, 1, 1, 1, 1) :  [(1, 3), (2, 3), (0,), (1, 2)]
(0, 1, 0, 1, 1, 1, 1) :  [(3,), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 1, 1) :  [(0, 3), (1,), (2,)]
(0, 1, 1, 0, 1, 1, 1) :  [(0,), (2,)]
(1, 0, 1, 0, 1, 1, 1) :  [(1, 3), (0,), (2,)]
(1, 1, 0, 0, 1, 1, 1) :  [(3,), (2,), (0, 1)]
(0, 1, 1, 1, 0, 1, 1) :  [(0,), (1,)]
(1, 0, 1, 1, 0, 1, 1) :  [(3,), (0,), (2,)]
(1, 1, 0, 1, 0, 1, 1) :  [(0, 3), (2, 3), (1,)]
(1, 1, 1, 0, 0, 1, 1) :  [(0,), (1,), (2,)]
(0, 1, 1, 1, 1, 0, 1) :  [(2, 3), (0,), (1,)]
(1, 0, 1, 1, 1, 0, 1) :  [(0, 3), (1, 3), (2,)]
(1, 1, 0, 1, 1, 0, 1) :  [(3,), (1,), (2,)]
(1, 1, 1, 0, 1, 0, 1) :  [(3,), (0,), (1,), (2,)]
(1, 1, 1, 1, 0, 0, 1) :  [(3,), (1,), (0, 2)]
(0, 1, 1, 1, 1, 1, 0) :  [(1, 3), (2, 3), (0,)]
(1, 0, 1, 1, 1, 1, 0) :  [(3,), (2,)]
(1, 1, 0, 1, 1, 1, 0) :  [()]
[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(1, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 2, 3), (0, 1, 2)], [(0, 1)], [(0, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(0, 2, 3), (0, 1)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3)], [(0, 1, 3), (0, 2)], [(0, 3)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(2, 3)], [(0, 3), (0, 1, 2)], [(2, 3), (0, 1, 3)], [(1, 2, 3), (0, 2)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(1, 3), (0, 2, 3)], [(0, 2, 3), (1, 2)], [(0, 1), (0, 2)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(1, 2, 3), (0, 1), (0, 2)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1), (0, 2)], [(0, 3), (0, 1)], [(0, 2, 3), (0, 1), (1, 2)], [(2, 3), (0, 2)], [(0, 3), (0, 2)], [(2, 3), (0, 1), (0, 2)], [(0, 2), (1, 2)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(2, 3), (1, 2)], [(0, 1), (0, 2), (1, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 1, 2)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (2, 3)], [(2, 3), (0, 1, 3), (0, 2)], [(1, 3), (0, 2)], [(0, 3), (1, 3)], [(2, 3), (0, 1, 3), (1, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3), (0, 1)], [(0, 3), (2, 3), (0, 1, 2)], [(1, 3), (2, 3)], [(2, 3), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2)], [(1, 3), (0, 2), (1, 2)], [(1, 3), (0, 2, 3), (0, 1), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(2,), (0, 1)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1)], [(2, 3), (0, 1), (1, 2)], [(0,), (1, 2)], [(0, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(2,)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (0, 2), (1, 2)], [(1, 3), (2,), (0, 1)], [(1,), (0, 2)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3), (0, 1), (1, 2)], [(2, 3), (1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1, 2)], [(0, 1, 3), (2,)], [(2, 3), (0,)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2)], [(1, 3), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(1,), (2,)], [(0, 3), (2, 3), (1,), (0, 2)], [(0, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0,), (1, 2)], [(3,), (0, 1), (0, 2), (1, 2)], [(0, 3), (1,), (2,)], [(0,), (2,)], [(1, 3), (0,), (2,)], [(3,), (2,), (0, 1)], [(0,), (1,)], [(3,), (0,), (2,)], [(0, 3), (2, 3), (1,)], [(0,), (1,), (2,)], [(2, 3), (0,), (1,)], [(0, 3), (1, 3), (2,)], [(3,), (1,), (2,)], [(3,), (0,), (1,), (2,)], [(3,), (1,), (0, 2)], [(1, 3), (2, 3), (0,)], [(3,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]


Friday:

A sample function for i=63
(0, 0, 0, 0, 0, 0) :  [(0, 1, 2, 3)]
(0, 0, 0, 0, 0, 1) :  [(0, 1, 2)]
(0, 0, 0, 0, 1, 0) :  [(0, 1, 3)]
(0, 0, 0, 1, 0, 0) :  [(1, 2, 3)]
(0, 0, 1, 0, 0, 0) :  [(0, 2, 3)]
(0, 1, 0, 0, 0, 0) :  [(0, 1, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0) :  [(0, 2, 3), (0, 1, 2)]
(0, 0, 0, 0, 1, 1) :  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]
(0, 0, 0, 1, 0, 1) :  [(1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 1) :  [(0, 2)]
(0, 1, 0, 0, 0, 1) :  [(0, 1)]
(1, 0, 0, 0, 0, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]
(0, 0, 0, 1, 1, 0) :  [(0, 1, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 0) :  [(0, 1, 3), (0, 2, 3)]
(0, 1, 0, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 1, 0) :  [(0, 2, 3), (0, 1)]
(0, 0, 1, 1, 0, 0) :  [(0, 2, 3), (1, 2, 3)]
(0, 1, 0, 1, 0, 0) :  [(1, 2, 3), (0, 1)]
(1, 0, 0, 1, 0, 0) :  [(1, 2, 3), (0, 2)]
(0, 1, 1, 0, 0, 0) :  [(0, 1, 3), (0, 2)]
(1, 0, 1, 0, 0, 0) :  [(0, 2, 3), (1, 2)]
(1, 1, 0, 0, 0, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]
(0, 0, 0, 1, 1, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1)]
(0, 0, 1, 0, 1, 1) :  [(0, 1), (0, 2)]
(0, 1, 0, 0, 1, 1) :  [(1, 2, 3), (0, 1), (0, 2)]
(1, 0, 0, 0, 1, 1) :  [(0, 2, 3), (0, 1), (1, 2)]
(0, 0, 1, 1, 0, 1) :  [(0, 2), (1, 2)]
(0, 1, 0, 1, 0, 1) :  [(0, 1), (1, 2)]
(1, 0, 0, 1, 0, 1) :  [(0, 1, 3), (1, 2, 3), (0, 2)]
(0, 1, 1, 0, 0, 1) :  [(0, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 0, 1) :  [(0, 1, 3), (0, 2), (1, 2)]
(1, 1, 0, 0, 0, 1) :  [(2, 3), (0, 1)]
(0, 0, 1, 1, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
(0, 1, 0, 1, 1, 0) :  [(1, 3), (0, 1)]
(1, 0, 0, 1, 1, 0) :  [(0, 1), (0, 2), (1, 2)]
(0, 1, 1, 0, 1, 0) :  [(2, 3), (0, 1, 3), (0, 2)]
(1, 0, 1, 0, 1, 0) :  [(2, 3), (0, 1), (1, 2)]
(1, 1, 0, 0, 1, 0) :  [(1, 3), (0, 2, 3), (0, 1)]
(0, 1, 1, 1, 0, 0) :  [(2, 3), (0, 1), (0, 2)]
(1, 0, 1, 1, 0, 0) :  [(2, 3), (0, 2), (1, 2)]
(1, 1, 0, 1, 0, 0) :  [(1, 3), (0, 1), (0, 2)]
(1, 1, 1, 0, 0, 0) :  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]
(0, 0, 1, 1, 1, 1) :  [(2, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 0, 1, 1, 1) :  [(1, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 1) :  [(0, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 1, 0, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 1, 1) :  [(2,), (0, 1)]
(1, 1, 0, 0, 1, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 1, 0, 1) :  [(0, 1, 3), (2,)]
(1, 1, 0, 1, 0, 1) :  [(2, 3), (1,), (0, 2)]
(1, 1, 1, 0, 0, 1) :  [(0, 3), (2,), (0, 1)]
(0, 1, 1, 1, 1, 0) :  [(1, 3), (2, 3), (0, 1), (0, 2)]
(1, 0, 1, 1, 1, 0) :  [(1, 3), (2,), (0, 1)]
(1, 1, 0, 1, 1, 0) :  [(1,), (0, 2)]
(1, 1, 1, 0, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 1, 1, 0, 0) :  [(1,), (2,)]
(0, 1, 1, 1, 1, 1) :  [(0, 3), (1, 3), (2,), (0, 1)]
(1, 0, 1, 1, 1, 1) :  [(0, 3), (1,), (2,)]
(1, 1, 0, 1, 1, 1) :  [(2, 3), (0,), (1,)]
(1, 1, 1, 0, 1, 1) :  [(1, 3), (0,), (2,)]
(1, 1, 1, 1, 0, 1) :  [(0,), (1,), (2,)]
(1, 1, 1, 1, 1, 0) :  [(3,), (1,), (2,)]
(1, 1, 1, 1, 1, 1) :  [()]
[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(1, 2, 3)], [(0, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 2)], [(0, 1)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (1, 2, 3)], [(0, 1, 3), (0, 2, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (0, 1)], [(0, 2, 3), (1, 2, 3)], [(1, 2, 3), (0, 1)], [(1, 2, 3), (0, 2)], [(0, 1, 3), (0, 2)], [(0, 2, 3), (1, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 1), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 2), (1, 2)], [(0, 1), (1, 2)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(0, 3), (0, 1), (0, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(1, 3), (0, 1)], [(0, 1), (0, 2), (1, 2)], [(2, 3), (0, 1, 3), (0, 2)], [(2, 3), (0, 1), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(2, 3), (0, 1), (0, 2)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(2,), (0, 1)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 1, 3), (2,)], [(2, 3), (1,), (0, 2)], [(0, 3), (2,), (0, 1)], [(1, 3), (2, 3), (0, 1), (0, 2)], [(1, 3), (2,), (0, 1)], [(1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(1,), (2,)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1,), (2,)], [(2, 3), (0,), (1,)], [(1, 3), (0,), (2,)], [(0,), (1,), (2,)], [(3,), (1,), (2,)], [()]]

Onto a set of size 20
[] True
[(0, 1, 2)] True
[(0, 1)] True
[(0, 2)] True
[(0, 1), (0, 2)] True
[(1, 2)] True
[(0, 1), (1, 2)] True
[(0, 2), (1, 2)] True
[(0, 1), (0, 2), (1, 2)] True
[(2,), (0, 1)] True
[(1,), (0, 2)] True
[(1,), (2,)] True
[(0,), (1, 2)] True
[(0,), (2,)] True
[(0,), (1,)] True
[(0,), (1,), (2,)] True
[(0,)] True
[(1,)] True
[(2,)] True
[()] True


A sample function for i=108
(0, 0, 0, 0, 0, 0, 0) :  [(0, 1, 2, 3)]
(0, 0, 0, 0, 0, 0, 1) :  [(0, 1, 2)]
(0, 0, 0, 0, 0, 1, 0) :  [(0, 1, 3)]
(0, 0, 0, 0, 1, 0, 0) :  [(0, 2, 3)]
(0, 0, 0, 1, 0, 0, 0) :  [(0, 1, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 0, 0) :  [(1, 2, 3)]
(0, 1, 0, 0, 0, 0, 0) :  [(0, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 0) :  [(0, 1, 3), (0, 2, 3)]
(0, 0, 0, 0, 0, 1, 1) :  [(0, 1)]
(0, 0, 0, 0, 1, 0, 1) :  [(0, 2)]
(0, 0, 0, 1, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 0, 1) :  [(1, 2, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 1) :  [(0, 2, 3), (0, 1)]
(0, 0, 0, 0, 1, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
(0, 0, 0, 1, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3)]
(0, 1, 0, 0, 0, 1, 0) :  [(0, 1, 3), (0, 2)]
(1, 0, 0, 0, 0, 1, 0) :  [(0, 3)]
(0, 0, 0, 1, 1, 0, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 1, 0, 0) :  [(0, 2, 3), (1, 2, 3)]
(0, 1, 0, 0, 1, 0, 0) :  [(1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3)]
(0, 0, 1, 1, 0, 0, 0) :  [(1, 2, 3), (0, 1)]
(0, 1, 0, 1, 0, 0, 0) :  [(0, 3), (0, 1, 2)]
(1, 0, 0, 1, 0, 0, 0) :  [(0, 2, 3), (1, 2, 3), (0, 1)]
(0, 1, 1, 0, 0, 0, 0) :  [(0, 2, 3), (1, 2)]
(1, 0, 1, 0, 0, 0, 0) :  [(1, 3), (0, 2, 3)]
(1, 1, 0, 0, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 1) :  [(1, 2, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 0, 1, 1) :  [(0, 2, 3), (0, 1), (1, 2)]
(0, 0, 1, 0, 0, 1, 1) :  [(0, 1), (1, 2)]
(0, 1, 0, 0, 0, 1, 1) :  [(0, 1), (0, 2), (1, 2)]
(1, 0, 0, 0, 0, 1, 1) :  [(0, 3), (0, 1)]
(0, 0, 0, 1, 1, 0, 1) :  [(0, 1, 3), (0, 2), (1, 2)]
(0, 0, 1, 0, 1, 0, 1) :  [(0, 2), (1, 2)]
(0, 1, 0, 0, 1, 0, 1) :  [(2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 1) :  [(2, 3), (0, 1), (0, 2)]
(0, 0, 1, 1, 0, 0, 1) :  [(2, 3), (0, 1)]
(0, 1, 0, 1, 0, 0, 1) :  [(0, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 1, 0, 0, 1) :  [(1, 3), (0, 2, 3), (0, 1)]
(0, 1, 1, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (1, 2)]
(1, 0, 1, 0, 0, 0, 1) :  [(1, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 0, 1) :  [(0, 3), (1, 2, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 1, 1, 0) :  [(2, 3), (0, 1, 3), (0, 1, 2)]
(0, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3)]
(0, 1, 0, 0, 1, 1, 0) :  [(2, 3), (0, 1, 3), (0, 2)]
(1, 0, 0, 0, 1, 1, 0) :  [(0, 3), (2, 3)]
(0, 0, 1, 1, 0, 1, 0) :  [(1, 3), (0, 1)]
(0, 1, 0, 1, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 2)]
(1, 0, 0, 1, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1)]
(0, 1, 1, 0, 0, 1, 0) :  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 1, 0) :  [(0, 3), (1, 3)]
(1, 1, 0, 0, 0, 1, 0) :  [(0, 3), (0, 2), (1, 2)]
(0, 0, 1, 1, 1, 0, 0) :  [(2, 3), (0, 1), (1, 2)]
(0, 1, 0, 1, 1, 0, 0) :  [(0, 3), (2, 3), (0, 2)]
(1, 0, 0, 1, 1, 0, 0) :  [(1, 3), (2, 3), (0, 1)]
(0, 1, 1, 0, 1, 0, 0) :  [(2, 3), (0, 2), (1, 2)]
(1, 0, 1, 0, 1, 0, 0) :  [(1, 3), (2, 3)]
(1, 1, 0, 0, 1, 0, 0) :  [(1, 3), (2, 3), (0, 2)]
(0, 1, 1, 1, 0, 0, 0) :  [(0, 3), (0, 1), (1, 2)]
(1, 0, 1, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3), (0, 1), (1, 2)]
(1, 1, 0, 1, 0, 0, 0) :  [(0, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 1, 0, 0, 0, 0) :  [(1, 3), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 1) :  [(2, 3), (0, 1), (0, 2), (1, 2)]
(0, 0, 1, 0, 1, 1, 1) :  [(0,), (1, 2)]
(0, 1, 0, 0, 1, 1, 1) :  [(2,), (0, 1)]
(1, 0, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2)]
(0, 0, 1, 1, 0, 1, 1) :  [(1, 3), (2, 3), (0, 1), (1, 2)]
(0, 1, 0, 1, 0, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 1, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (1, 2)]
(0, 1, 1, 0, 0, 1, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 0, 0, 1, 1) :  [(0, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 0, 1) :  [(1, 3), (2,), (0, 1)]
(0, 1, 0, 1, 1, 0, 1) :  [(0, 3), (2, 3), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 0, 1) :  [(2, 3), (1,), (0, 2)]
(0, 1, 1, 0, 1, 0, 1) :  [(0, 1, 3), (2,)]
(1, 0, 1, 0, 1, 0, 1) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 0, 1, 0, 1) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)]
(0, 1, 1, 1, 0, 0, 1) :  [(0, 3), (2, 3), (0, 1), (1, 2)]
(1, 0, 1, 1, 0, 0, 1) :  [(1,), (2,)]
(1, 1, 0, 1, 0, 0, 1) :  [(0, 3), (1,), (0, 2)]
(1, 1, 1, 0, 0, 0, 1) :  [(1, 3), (0,), (1, 2)]
(0, 0, 1, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)]
(0, 1, 0, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2)]
(1, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1)]
(0, 1, 1, 0, 1, 1, 0) :  [(0, 3), (2,)]
(1, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3)]
(1, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 1, 0) :  [(0, 3), (1, 3), (2,), (0, 1)]
(1, 0, 1, 1, 0, 1, 0) :  [(0, 3), (1,)]
(1, 1, 0, 1, 0, 1, 0) :  [(2, 3), (0,), (1, 2)]
(1, 1, 1, 0, 0, 1, 0) :  [(0, 3), (1, 3), (2,)]
(0, 1, 1, 1, 1, 0, 0) :  [(0,), (2,)]
(1, 0, 1, 1, 1, 0, 0) :  [(2, 3), (1,)]
(1, 1, 0, 1, 1, 0, 0) :  [(0, 3), (2, 3), (1,), (0, 2)]
(1, 1, 1, 0, 1, 0, 0) :  [(1, 3), (2, 3), (0, 2), (1, 2)]
(1, 1, 1, 1, 0, 0, 0) :  [(0,), (1,)]
(0, 0, 1, 1, 1, 1, 1) :  [(1, 3), (0,), (2,)]
(0, 1, 0, 1, 1, 1, 1) :  [(0, 3), (1,), (2,)]
(1, 0, 0, 1, 1, 1, 1) :  [(2, 3), (0,), (1,)]
(0, 1, 1, 0, 1, 1, 1) :  [(0,), (1,), (2,)]
(1, 0, 1, 0, 1, 1, 1) :  [(1, 3), (2, 3), (0,), (1, 2)]
(1, 1, 0, 0, 1, 1, 1) :  [(3,), (2,), (0, 1)]
(0, 1, 1, 1, 0, 1, 1) :  [(3,), (0,), (2,)]
(1, 0, 1, 1, 0, 1, 1) :  [(3,), (1,), (2,)]
(1, 1, 0, 1, 0, 1, 1) :  [(3,), (0,), (1,), (2,)]
(1, 1, 1, 0, 0, 1, 1) :  [()]
[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(1, 2, 3)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 1)], [(0, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (1, 2, 3)], [(0, 1, 3), (0, 2)], [(0, 3)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3)], [(1, 2, 3), (0, 2)], [(2, 3), (0, 1, 3)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 1), (1, 2)], [(0, 1), (0, 2), (1, 2)], [(0, 3), (0, 1)], [(0, 1, 3), (0, 2), (1, 2)], [(0, 2), (1, 2)], [(2, 3), (0, 2)], [(2, 3), (0, 1), (0, 2)], [(2, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(1, 3), (0, 1), (0, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(2, 3), (0, 1, 3), (0, 1, 2)], [(0, 3), (1, 2, 3)], [(2, 3), (0, 1, 3), (0, 2)], [(0, 3), (2, 3)], [(1, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (1, 2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 3)], [(0, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (1, 2)], [(0, 3), (2, 3), (0, 2)], [(1, 3), (2, 3), (0, 1)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3)], [(1, 3), (2, 3), (0, 2)], [(0, 3), (0, 1), (1, 2)], [(1, 3), (0, 2, 3), (0, 1), (1, 2)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(0,), (1, 2)], [(2,), (0, 1)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(1, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1), (1, 2)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2,), (0, 1)], [(1, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (1,), (0, 2)], [(0, 1, 3), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(1,), (2,)], [(0, 3), (1,), (0, 2)], [(1, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1,)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2,)], [(0,), (2,)], [(2, 3), (1,)], [(0, 3), (2, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(0,), (1,)], [(1, 3), (0,), (2,)], [(0, 3), (1,), (2,)], [(2, 3), (0,), (1,)], [(0,), (1,), (2,)], [(1, 3), (2, 3), (0,), (1, 2)], [(3,), (2,), (0, 1)], [(3,), (0,), (2,)], [(3,), (1,), (2,)], [(3,), (0,), (1,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]

OntoAdequate, i=108



A sample function for i=112
(0, 0, 0, 0, 0, 0, 0) :  [(0, 1, 2, 3)]
(0, 0, 0, 0, 0, 0, 1) :  [(0, 1, 2)]
(0, 0, 0, 0, 0, 1, 0) :  [(0, 1, 3)]
(0, 0, 0, 0, 1, 0, 0) :  [(0, 2, 3)]
(0, 0, 0, 1, 0, 0, 0) :  [(1, 2, 3)]
(0, 0, 1, 0, 0, 0, 0) :  [(0, 1, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 0) :  [(0, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 0) :  [(0, 1, 3), (0, 2, 3)]
(0, 0, 0, 0, 0, 1, 1) :  [(0, 1)]
(0, 0, 0, 0, 1, 0, 1) :  [(0, 2)]
(0, 0, 0, 1, 0, 0, 1) :  [(1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
(0, 0, 0, 1, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3)]
(0, 0, 1, 0, 0, 1, 0) :  [(0, 2, 3), (0, 1)]
(0, 1, 0, 0, 0, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 1, 0) :  [(0, 3)]
(0, 0, 0, 1, 1, 0, 0) :  [(0, 2, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1, 2)]
(0, 1, 0, 0, 1, 0, 0) :  [(1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3)]
(0, 0, 1, 1, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 0, 0, 0) :  [(0, 2, 3), (1, 2)]
(1, 0, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3)]
(0, 1, 1, 0, 0, 0, 0) :  [(0, 1), (0, 2)]
(1, 0, 1, 0, 0, 0, 0) :  [(0, 2, 3), (1, 2, 3), (0, 1)]
(1, 1, 0, 0, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 1) :  [(1, 2, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 0, 1, 1) :  [(1, 2, 3), (0, 1)]
(0, 0, 1, 0, 0, 1, 1) :  [(0, 3), (0, 1)]
(0, 1, 0, 0, 0, 1, 1) :  [(0, 2, 3), (0, 1), (1, 2)]
(1, 0, 0, 0, 0, 1, 1) :  [(0, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 1, 0, 1) :  [(0, 2), (1, 2)]
(0, 0, 1, 0, 1, 0, 1) :  [(0, 3), (0, 2)]
(0, 1, 0, 0, 1, 0, 1) :  [(2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 1) :  [(2, 3), (0, 1, 3), (0, 2)]
(0, 0, 1, 1, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (1, 2)]
(0, 1, 0, 1, 0, 0, 1) :  [(2, 3), (1, 2)]
(1, 0, 0, 1, 0, 0, 1) :  [(1, 3), (0, 2)]
(0, 1, 1, 0, 0, 0, 1) :  [(0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 0, 1) :  [(2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1)]
(0, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 1, 0) :  [(0, 3), (2, 3)]
(0, 0, 1, 1, 0, 1, 0) :  [(2, 3), (0, 1)]
(0, 1, 0, 1, 0, 1, 0) :  [(2, 3), (0, 1, 3), (1, 2)]
(1, 0, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3)]
(0, 1, 1, 0, 0, 1, 0) :  [(1, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 1, 0) :  [(0, 3), (0, 2), (1, 2)]
(0, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 1, 0, 0) :  [(2, 3), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 0, 0) :  [(1, 3), (2, 3)]
(0, 1, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 1, 0, 0) :  [(0, 3), (2, 3), (0, 1)]
(1, 1, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 0, 0) :  [(2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3), (0, 1)]
(1, 1, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2), (1, 2)]
(1, 1, 1, 0, 0, 0, 0) :  [(1, 3), (0, 1), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 1) :  [(0,), (1, 2)]
(0, 0, 1, 0, 1, 1, 1) :  [(1, 2, 3), (0,)]
(0, 1, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2)]
(0, 0, 1, 1, 0, 1, 1) :  [(0, 3), (2, 3), (0, 1), (1, 2)]
(0, 1, 0, 1, 0, 1, 1) :  [(2, 3), (0, 1), (1, 2)]
(1, 0, 0, 1, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2)]
(0, 1, 1, 0, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 1, 1) :  [(2, 3), (0,)]
(1, 1, 0, 0, 0, 1, 1) :  [(0, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 0, 1, 1, 0, 1) :  [(2,)]
(1, 0, 0, 1, 1, 0, 1) :  [(1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 0, 1, 0, 1) :  [(2, 3), (0,), (1, 2)]
(1, 0, 1, 0, 1, 0, 1) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 1, 0, 1) :  [(0, 1, 3), (2,)]
(0, 1, 1, 1, 0, 0, 1) :  [(2,), (0, 1)]
(1, 0, 1, 1, 0, 0, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 1, 0, 0, 1) :  [(1, 3), (2,)]
(1, 1, 1, 0, 0, 0, 1) :  [(1, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1)]
(0, 1, 0, 1, 1, 1, 0) :  [(0, 3), (2,)]
(1, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3)]
(0, 1, 1, 0, 1, 1, 0) :  [(0, 3), (1,), (0, 2)]
(1, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 1, 0) :  [(2, 3), (1,), (0, 2)]
(1, 0, 1, 1, 0, 1, 0) :  [(1, 3), (2, 3), (0,)]
(1, 1, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3), (2,)]
(1, 1, 1, 0, 0, 1, 0) :  [(1, 3), (0,), (1, 2)]
(0, 1, 1, 1, 1, 0, 0) :  [(0,), (2,)]
(1, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)]
(1, 1, 0, 1, 1, 0, 0) :  [(3,), (0, 2), (1, 2)]
(1, 1, 1, 0, 1, 0, 0) :  [(0, 3), (1, 3), (2,), (0, 1)]
(1, 1, 1, 1, 0, 0, 0) :  [(1,), (2,)]
(0, 0, 1, 1, 1, 1, 1) :  [(1, 3), (2, 3), (0,), (1, 2)]
(0, 1, 0, 1, 1, 1, 1) :  [(1, 3), (0,), (2,)]
(1, 0, 0, 1, 1, 1, 1) :  [(2, 3), (0,), (1,)]
(0, 1, 1, 0, 1, 1, 1) :  [(0,), (1,), (2,)]
(1, 0, 1, 0, 1, 1, 1) :  [(3,), (0,), (1, 2)]
(1, 1, 0, 0, 1, 1, 1) :  [(0, 3), (1,), (2,)]
(0, 1, 1, 1, 0, 1, 1) :  [(3,), (1,), (2,)]
(1, 0, 1, 1, 0, 1, 1) :  [(3,), (0,), (1,)]
(1, 1, 0, 1, 0, 1, 1) :  [(3,), (2,), (0, 1)]
(1, 1, 1, 0, 0, 1, 1) :  [(3,), (0,), (2,)]
(0, 1, 1, 1, 1, 0, 1) :  [(3,), (0,), (1,), (2,)]
(1, 0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (1,), (0, 2)]
(1, 1, 0, 1, 1, 0, 1) :  [(3,), (2,)]
(1, 1, 1, 0, 1, 0, 1) :  [()]
[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(1, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 1)], [(0, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3)], [(0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 3)], [(0, 2, 3), (1, 2, 3)], [(0, 3), (0, 1, 2)], [(1, 2, 3), (0, 2)], [(2, 3), (0, 1, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3)], [(0, 1), (0, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 3), (0, 1), (0, 2)], [(0, 2), (1, 2)], [(0, 3), (0, 2)], [(2, 3), (0, 2)], [(2, 3), (0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(2, 3), (1, 2)], [(1, 3), (0, 2)], [(0, 1), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3)], [(0, 3), (1, 2, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (2, 3)], [(2, 3), (0, 1)], [(2, 3), (0, 1, 3), (1, 2)], [(0, 3), (1, 3)], [(1, 3), (0, 1), (0, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(0, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3), (0, 1, 2)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(1, 3), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(0,), (1, 2)], [(1, 2, 3), (0,)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(2, 3), (0,)], [(0, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(2,)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 1, 3), (2,)], [(2,), (0, 1)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (2,)], [(1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3)], [(0, 3), (1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0,)], [(0, 3), (1, 3), (2,)], [(1, 3), (0,), (1, 2)], [(0,), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(3,), (0, 2), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(1,), (2,)], [(1, 3), (2, 3), (0,), (1, 2)], [(1, 3), (0,), (2,)], [(2, 3), (0,), (1,)], [(0,), (1,), (2,)], [(3,), (0,), (1, 2)], [(0, 3), (1,), (2,)], [(3,), (1,), (2,)], [(3,), (0,), (1,)], [(3,), (2,), (0, 1)], [(3,), (0,), (2,)], [(3,), (0,), (1,), (2,)], [(0, 3), (2, 3), (1,), (0, 2)], [(3,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]

Onto a set of size 19
[] True
[(0, 1, 2)] True
[(0, 1)] True
[(0, 2)] True
[(0, 1), (0, 2)] True
[(1, 2)] True
[(0, 1), (1, 2)] True
[(0, 2), (1, 2)] True
[(0, 1), (0, 2), (1, 2)] True
[(2,), (0, 1)] True
[(1,), (0, 2)] True
[(1,), (2,)] True
[(0,), (1, 2)] True
[(0,), (2,)] True
[(0,), (1,)] True
[(0,), (1,), (2,)] True
[(0,)] True
[(1,)] False
[(2,)] True
[()] True

A sample function for i=112
(0, 0, 0, 0, 0, 0, 0) :  [(0, 1, 2, 3)]
(0, 0, 0, 0, 0, 0, 1) :  [(0, 1, 2)]
(0, 0, 0, 0, 0, 1, 0) :  [(0, 1, 3)]
(0, 0, 0, 0, 1, 0, 0) :  [(0, 2, 3)]
(0, 0, 0, 1, 0, 0, 0) :  [(1, 2, 3)]
(0, 0, 1, 0, 0, 0, 0) :  [(0, 1, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 0) :  [(0, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 0) :  [(0, 1, 3), (0, 2, 3)]
(0, 0, 0, 0, 0, 1, 1) :  [(0, 1)]
(0, 0, 0, 0, 1, 0, 1) :  [(0, 2)]
(0, 0, 0, 1, 0, 0, 1) :  [(1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
(0, 0, 0, 1, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3)]
(0, 0, 1, 0, 0, 1, 0) :  [(0, 2, 3), (0, 1)]
(0, 1, 0, 0, 0, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 1, 0) :  [(0, 3)]
(0, 0, 0, 1, 1, 0, 0) :  [(0, 2, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1, 2)]
(0, 1, 0, 0, 1, 0, 0) :  [(1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3)]
(0, 0, 1, 1, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 0, 0, 0) :  [(0, 2, 3), (1, 2)]
(1, 0, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3)]
(0, 1, 1, 0, 0, 0, 0) :  [(0, 1), (0, 2)]
(1, 0, 1, 0, 0, 0, 0) :  [(0, 2, 3), (1, 2, 3), (0, 1)]
(1, 1, 0, 0, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 1) :  [(1, 2, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 0, 1, 1) :  [(1, 2, 3), (0, 1)]
(0, 0, 1, 0, 0, 1, 1) :  [(0, 3), (0, 1)]
(0, 1, 0, 0, 0, 1, 1) :  [(0, 2, 3), (0, 1), (1, 2)]
(1, 0, 0, 0, 0, 1, 1) :  [(0, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 1, 0, 1) :  [(0, 2), (1, 2)]
(0, 0, 1, 0, 1, 0, 1) :  [(0, 3), (0, 2)]
(0, 1, 0, 0, 1, 0, 1) :  [(2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 1) :  [(2, 3), (0, 1, 3), (0, 2)]
(0, 0, 1, 1, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (1, 2)]
(0, 1, 0, 1, 0, 0, 1) :  [(2, 3), (1, 2)]
(1, 0, 0, 1, 0, 0, 1) :  [(1, 3), (0, 2)]
(0, 1, 1, 0, 0, 0, 1) :  [(0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 0, 1) :  [(2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1)]
(0, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 1, 0) :  [(0, 3), (2, 3)]
(0, 0, 1, 1, 0, 1, 0) :  [(2, 3), (0, 1)]
(0, 1, 0, 1, 0, 1, 0) :  [(2, 3), (0, 1, 3), (1, 2)]
(1, 0, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3)]
(0, 1, 1, 0, 0, 1, 0) :  [(1, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 1, 0) :  [(0, 3), (0, 2), (1, 2)]
(0, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 1, 0, 0) :  [(2, 3), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 0, 0) :  [(1, 3), (2, 3)]
(0, 1, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 1, 0, 0) :  [(0, 3), (2, 3), (0, 1)]
(1, 1, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 0, 0) :  [(2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3), (0, 1)]
(1, 1, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2), (1, 2)]
(1, 1, 1, 0, 0, 0, 0) :  [(1, 3), (0, 1), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 1) :  [(0,), (1, 2)]
(0, 0, 1, 0, 1, 1, 1) :  [(1, 2, 3), (0,)]
(0, 1, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2)]
(0, 0, 1, 1, 0, 1, 1) :  [(0, 3), (2, 3), (0, 1), (1, 2)]
(0, 1, 0, 1, 0, 1, 1) :  [(2, 3), (0, 1), (1, 2)]
(1, 0, 0, 1, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2)]
(0, 1, 1, 0, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 1, 1) :  [(2, 3), (0,)]
(1, 1, 0, 0, 0, 1, 1) :  [(0, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 0, 1, 1, 0, 1) :  [(2,)]
(1, 0, 0, 1, 1, 0, 1) :  [(1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 0, 1, 0, 1) :  [(2, 3), (0,), (1, 2)]
(1, 0, 1, 0, 1, 0, 1) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 1, 0, 1) :  [(0, 1, 3), (2,)]
(0, 1, 1, 1, 0, 0, 1) :  [(2,), (0, 1)]
(1, 0, 1, 1, 0, 0, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 1, 0, 0, 1) :  [(1, 3), (2,)]
(1, 1, 1, 0, 0, 0, 1) :  [(1, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1)]
(0, 1, 0, 1, 1, 1, 0) :  [(0, 3), (2,)]
(1, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3)]
(0, 1, 1, 0, 1, 1, 0) :  [(0, 3), (1,), (0, 2)]
(1, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 1, 0) :  [(2, 3), (1,), (0, 2)]
(1, 0, 1, 1, 0, 1, 0) :  [(1, 3), (2, 3), (0,)]
(1, 1, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3), (2,)]
(1, 1, 1, 0, 0, 1, 0) :  [(1, 3), (0,), (1, 2)]
(0, 1, 1, 1, 1, 0, 0) :  [(0,), (2,)]
(1, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)]
(1, 1, 0, 1, 1, 0, 0) :  [(3,), (0, 2), (1, 2)]
(1, 1, 1, 0, 1, 0, 0) :  [(0, 3), (1, 3), (2,), (0, 1)]
(1, 1, 1, 1, 0, 0, 0) :  [(1,), (2,)]
(0, 0, 1, 1, 1, 1, 1) :  [(1, 3), (2, 3), (0,), (1, 2)]
(0, 1, 0, 1, 1, 1, 1) :  [(1, 3), (0,), (2,)]
(1, 0, 0, 1, 1, 1, 1) :  [(2, 3), (0,), (1,)]
(0, 1, 1, 0, 1, 1, 1) :  [(0,), (1,), (2,)]
(1, 0, 1, 0, 1, 1, 1) :  [(3,), (0,), (1, 2)]
(1, 1, 0, 0, 1, 1, 1) :  [(0, 3), (1,), (2,)]
(0, 1, 1, 1, 0, 1, 1) :  [(3,), (1,), (2,)]
(1, 0, 1, 1, 0, 1, 1) :  [(3,), (0,), (1,)]
(1, 1, 0, 1, 0, 1, 1) :  [(3,), (2,), (0, 1)]
(1, 1, 1, 0, 0, 1, 1) :  [(3,), (0,), (2,)]
(0, 1, 1, 1, 1, 0, 1) :  [(3,), (0,), (1,), (2,)]
(1, 0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (1,), (0, 2)]
(1, 1, 0, 1, 1, 0, 1) :  [(3,), (2,)]
(1, 1, 1, 0, 1, 0, 1) :  [()]
[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(1, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 1)], [(0, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3)], [(0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 3)], [(0, 2, 3), (1, 2, 3)], [(0, 3), (0, 1, 2)], [(1, 2, 3), (0, 2)], [(2, 3), (0, 1, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3)], [(0, 1), (0, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 3), (0, 1), (0, 2)], [(0, 2), (1, 2)], [(0, 3), (0, 2)], [(2, 3), (0, 2)], [(2, 3), (0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(2, 3), (1, 2)], [(1, 3), (0, 2)], [(0, 1), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3)], [(0, 3), (1, 2, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (2, 3)], [(2, 3), (0, 1)], [(2, 3), (0, 1, 3), (1, 2)], [(0, 3), (1, 3)], [(1, 3), (0, 1), (0, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(0, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3), (0, 1, 2)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(1, 3), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(0,), (1, 2)], [(1, 2, 3), (0,)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(2, 3), (0,)], [(0, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(2,)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 1, 3), (2,)], [(2,), (0, 1)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (2,)], [(1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3)], [(0, 3), (1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0,)], [(0, 3), (1, 3), (2,)], [(1, 3), (0,), (1, 2)], [(0,), (2,)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(3,), (0, 2), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(1,), (2,)], [(1, 3), (2, 3), (0,), (1, 2)], [(1, 3), (0,), (2,)], [(2, 3), (0,), (1,)], [(0,), (1,), (2,)], [(3,), (0,), (1, 2)], [(0, 3), (1,), (2,)], [(3,), (1,), (2,)], [(3,), (0,), (1,)], [(3,), (2,), (0, 1)], [(3,), (0,), (2,)], [(3,), (0,), (1,), (2,)], [(0, 3), (2, 3), (1,), (0, 2)], [(3,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]


A sample function for i=106
(0, 0, 0, 0, 0, 0, 0) :  [(0, 1, 2, 3)]
(0, 0, 0, 0, 0, 0, 1) :  [(0, 1, 2)]
(0, 0, 0, 0, 0, 1, 0) :  [(0, 1, 3)]
(0, 0, 0, 0, 1, 0, 0) :  [(0, 2, 3)]
(0, 0, 0, 1, 0, 0, 0) :  [(1, 2, 3)]
(0, 0, 1, 0, 0, 0, 0) :  [(0, 1, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 0) :  [(0, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 0) :  [(0, 1, 3), (0, 2, 3)]
(0, 0, 0, 0, 0, 1, 1) :  [(0, 1)]
(0, 0, 0, 0, 1, 0, 1) :  [(0, 2)]
(0, 0, 0, 1, 0, 0, 1) :  [(1, 2, 3), (0, 1, 2)]
(0, 0, 1, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (0, 1, 2)]
(0, 1, 0, 0, 0, 0, 1) :  [(0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
(0, 0, 0, 1, 0, 1, 0) :  [(0, 1, 3), (1, 2, 3)]
(0, 0, 1, 0, 0, 1, 0) :  [(0, 2, 3), (0, 1)]
(0, 1, 0, 0, 0, 1, 0) :  [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)]
(1, 0, 0, 0, 0, 1, 0) :  [(0, 3)]
(0, 0, 0, 1, 1, 0, 0) :  [(0, 2, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1, 2)]
(0, 1, 0, 0, 1, 0, 0) :  [(1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3)]
(0, 0, 1, 1, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 0, 0, 0) :  [(0, 2, 3), (1, 2)]
(1, 0, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3)]
(0, 1, 1, 0, 0, 0, 0) :  [(0, 1), (0, 2)]
(1, 0, 1, 0, 0, 0, 0) :  [(0, 2, 3), (1, 2, 3), (0, 1)]
(1, 1, 0, 0, 0, 0, 0) :  [(0, 1, 3), (1, 2, 3), (0, 2)]
(0, 0, 0, 0, 1, 1, 1) :  [(1, 2, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 0, 1, 1) :  [(1, 2, 3), (0, 1)]
(0, 0, 1, 0, 0, 1, 1) :  [(0, 3), (0, 1)]
(0, 1, 0, 0, 0, 1, 1) :  [(0, 2, 3), (0, 1), (1, 2)]
(1, 0, 0, 0, 0, 1, 1) :  [(0, 3), (0, 1), (0, 2)]
(0, 0, 0, 1, 1, 0, 1) :  [(0, 2), (1, 2)]
(0, 0, 1, 0, 1, 0, 1) :  [(0, 3), (0, 2)]
(0, 1, 0, 0, 1, 0, 1) :  [(2, 3), (0, 2)]
(1, 0, 0, 0, 1, 0, 1) :  [(2, 3), (0, 1, 3), (0, 2)]
(0, 0, 1, 1, 0, 0, 1) :  [(0, 1, 3), (0, 2, 3), (1, 2)]
(0, 1, 0, 1, 0, 0, 1) :  [(2, 3), (1, 2)]
(1, 0, 0, 1, 0, 0, 1) :  [(1, 3), (0, 2)]
(0, 1, 1, 0, 0, 0, 1) :  [(0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 0, 1) :  [(2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 0, 1) :  [(0, 1, 3), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 2, 3)]
(0, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1)]
(0, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 2, 3), (0, 2)]
(1, 0, 0, 0, 1, 1, 0) :  [(0, 3), (2, 3)]
(0, 0, 1, 1, 0, 1, 0) :  [(2, 3), (0, 1)]
(0, 1, 0, 1, 0, 1, 0) :  [(2, 3), (0, 1, 3), (1, 2)]
(1, 0, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3)]
(0, 1, 1, 0, 0, 1, 0) :  [(1, 3), (0, 1), (0, 2)]
(1, 0, 1, 0, 0, 1, 0) :  [(0, 3), (1, 2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 0, 1, 0) :  [(0, 3), (0, 2), (1, 2)]
(0, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 2, 3), (0, 1, 2)]
(0, 1, 0, 1, 1, 0, 0) :  [(2, 3), (0, 2), (1, 2)]
(1, 0, 0, 1, 1, 0, 0) :  [(1, 3), (2, 3)]
(0, 1, 1, 0, 1, 0, 0) :  [(0, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 1, 0, 0) :  [(0, 3), (2, 3), (0, 1)]
(1, 1, 0, 0, 1, 0, 0) :  [(2, 3), (0, 1, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 0, 0) :  [(2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 1, 0, 0, 0) :  [(1, 3), (0, 2, 3), (0, 1)]
(1, 1, 0, 1, 0, 0, 0) :  [(1, 3), (0, 2), (1, 2)]
(1, 1, 1, 0, 0, 0, 0) :  [(1, 3), (0, 1), (0, 2), (1, 2)]
(0, 0, 0, 1, 1, 1, 1) :  [(0,), (1, 2)]
(0, 0, 1, 0, 1, 1, 1) :  [(1, 2, 3), (0,)]
(0, 1, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 0, 0, 1, 1, 1) :  [(0, 3), (2, 3), (0, 1), (0, 2)]
(0, 0, 1, 1, 0, 1, 1) :  [(0, 3), (2, 3), (0, 1), (1, 2)]
(0, 1, 0, 1, 0, 1, 1) :  [(2, 3), (0, 1), (1, 2)]
(1, 0, 0, 1, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2)]
(0, 1, 1, 0, 0, 1, 1) :  [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)]
(1, 0, 1, 0, 0, 1, 1) :  [(2, 3), (0,)]
(1, 1, 0, 0, 0, 1, 1) :  [(0, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 0, 1) :  [(0, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 0, 1, 1, 0, 1) :  [(2,)]
(1, 0, 0, 1, 1, 0, 1) :  [(1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 0, 1, 0, 1) :  [(2, 3), (0,), (1, 2)]
(1, 0, 1, 0, 1, 0, 1) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)]
(1, 1, 0, 0, 1, 0, 1) :  [(0, 1, 3), (2,)]
(0, 1, 1, 1, 0, 0, 1) :  [(2,), (0, 1)]
(1, 0, 1, 1, 0, 0, 1) :  [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 1, 0, 0, 1) :  [(1, 3), (2,)]
(1, 1, 1, 0, 0, 0, 1) :  [(1, 3), (2,), (0, 1)]
(0, 0, 1, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1)]
(0, 1, 0, 1, 1, 1, 0) :  [(0, 3), (2,)]
(1, 0, 0, 1, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3)]
(0, 1, 1, 0, 1, 1, 0) :  [(0, 3), (1,), (0, 2)]
(1, 0, 1, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
(1, 1, 0, 0, 1, 1, 0) :  [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)]
(0, 1, 1, 1, 0, 1, 0) :  [(2, 3), (1,), (0, 2)]
(1, 0, 1, 1, 0, 1, 0) :  [(1, 3), (2, 3), (0,)]
(1, 1, 0, 1, 0, 1, 0) :  [(0, 3), (1, 3), (2,)]
(1, 1, 1, 0, 0, 1, 0) :  [(1, 3), (0,), (1, 2)]
(0, 1, 1, 1, 1, 0, 0) :  [(0, 3), (1, 3), (2,), (0, 1)]
(1, 0, 1, 1, 1, 0, 0) :  [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)]
(1, 1, 0, 1, 1, 0, 0) :  [(3,), (0, 2), (1, 2)]
(1, 1, 1, 0, 1, 0, 0) :  [(0, 3), (2, 3), (1,), (0, 2)]
(1, 1, 1, 1, 0, 0, 0) :  [(3,), (0, 1), (0, 2), (1, 2)]
(0, 0, 1, 1, 1, 1, 1) :  [(1, 3), (2, 3), (0,), (1, 2)]
(0, 1, 0, 1, 1, 1, 1) :  [(0,), (2,)]
(1, 0, 0, 1, 1, 1, 1) :  [(1, 3), (0,), (2,)]
(0, 1, 1, 0, 1, 1, 1) :  [(2, 3), (0,), (1,)]
(1, 0, 1, 0, 1, 1, 1) :  [(3,), (0,), (1, 2)]
(1, 1, 0, 0, 1, 1, 1) :  [(3,), (2,), (0, 1)]
(0, 1, 1, 1, 0, 1, 1) :  [(0, 3), (1,), (2,)]
(1, 0, 1, 1, 0, 1, 1) :  [()]
[[(0, 1, 2, 3)], [(0, 1, 2)], [(0, 1, 3)], [(0, 2, 3)], [(1, 2, 3)], [(0, 1, 3), (0, 1, 2)], [(0, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3)], [(0, 1)], [(0, 2)], [(1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2, 3)], [(0, 1, 3), (1, 2, 3)], [(0, 2, 3), (0, 1)], [(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2)], [(0, 3)], [(0, 2, 3), (1, 2, 3)], [(0, 3), (0, 1, 2)], [(1, 2, 3), (0, 2)], [(2, 3), (0, 1, 3)], [(0, 1, 3), (1, 2, 3), (0, 1, 2)], [(0, 2, 3), (1, 2)], [(1, 3), (0, 2, 3)], [(0, 1), (0, 2)], [(0, 2, 3), (1, 2, 3), (0, 1)], [(0, 1, 3), (1, 2, 3), (0, 2)], [(1, 2, 3), (0, 1), (0, 2)], [(1, 2, 3), (0, 1)], [(0, 3), (0, 1)], [(0, 2, 3), (0, 1), (1, 2)], [(0, 3), (0, 1), (0, 2)], [(0, 2), (1, 2)], [(0, 3), (0, 2)], [(2, 3), (0, 2)], [(2, 3), (0, 1, 3), (0, 2)], [(0, 1, 3), (0, 2, 3), (1, 2)], [(2, 3), (1, 2)], [(1, 3), (0, 2)], [(0, 1), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2)], [(0, 1, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3)], [(0, 3), (1, 2, 3), (0, 1)], [(0, 3), (1, 2, 3), (0, 2)], [(0, 3), (2, 3)], [(2, 3), (0, 1)], [(2, 3), (0, 1, 3), (1, 2)], [(0, 3), (1, 3)], [(1, 3), (0, 1), (0, 2)], [(0, 3), (1, 2, 3), (0, 1), (0, 2)], [(0, 3), (0, 2), (1, 2)], [(0, 3), (1, 2, 3), (0, 1, 2)], [(2, 3), (0, 2), (1, 2)], [(1, 3), (2, 3)], [(0, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1)], [(2, 3), (0, 1, 3), (0, 2), (1, 2)], [(2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (0, 2, 3), (0, 1)], [(1, 3), (0, 2), (1, 2)], [(1, 3), (0, 1), (0, 2), (1, 2)], [(0,), (1, 2)], [(1, 2, 3), (0,)], [(0, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (2, 3), (0, 1), (0, 2)], [(0, 3), (2, 3), (0, 1), (1, 2)], [(2, 3), (0, 1), (1, 2)], [(0, 3), (1, 3), (0, 1), (0, 2)], [(0, 3), (1, 3), (0, 1), (0, 2), (1, 2)], [(2, 3), (0,)], [(0, 3), (2,), (0, 1)], [(0, 3), (2, 3), (0, 2), (1, 2)], [(2,)], [(1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2)], [(0, 1, 3), (2,)], [(2,), (0, 1)], [(1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(1, 3), (2,)], [(1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1)], [(0, 3), (2,)], [(0, 3), (1, 3), (2, 3)], [(0, 3), (1,), (0, 2)], [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)], [(0, 3), (1, 3), (2, 3), (0, 2), (1, 2)], [(2, 3), (1,), (0, 2)], [(1, 3), (2, 3), (0,)], [(0, 3), (1, 3), (2,)], [(1, 3), (0,), (1, 2)], [(0, 3), (1, 3), (2,), (0, 1)], [(0, 3), (1, 3), (2, 3), (0, 1), (1, 2)], [(3,), (0, 2), (1, 2)], [(0, 3), (2, 3), (1,), (0, 2)], [(3,), (0, 1), (0, 2), (1, 2)], [(1, 3), (2, 3), (0,), (1, 2)], [(0,), (2,)], [(1, 3), (0,), (2,)], [(2, 3), (0,), (1,)], [(3,), (0,), (1, 2)], [(3,), (2,), (0, 1)], [(0, 3), (1,), (2,)], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()], [()]]

Why doesn't it assign the value ((0,),(1,),(2,),(3,))? Because we earlier said, that is a dead-end, and we are trying to get to 128 not just say 108.

Can we have a self-dual embedding in some sense?
F_2^- consists of 1,pvq,p,q,pq.
We embed 00,01,10,11 into pq,q,p,pvq
"""