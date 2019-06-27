from random import randint
from auExamples import mymap4sets, mymap5sets, mymap6sets, mymap4ToF3sets, computerMap6, computerMap7
import math
import time
import itertools
import operator

#June 25, 2019: We use sets of ascending tuples to represent monotone functions (antichains) in Python.

def subset(G, F):
	g = frozenset(G)
	f = frozenset(F)
	return g.issubset(f)

assert(subset((0, 3), (0, 1, 3)))

def purgeSets(L):
	#Input: a set of tuples of nonnegative integers in increasing order
	#Output: interpreting the tuples as sets, a set of tuples defining the same monotone function, and having no superfluous tuples.
	for F in L:
		for G in L:
			if F != G and subset(F, G):
				L = frozenset([H for H in L if H!=G])
	return frozenset(L)

assert(
	purgeSets(
		frozenset([(0, 3), (1, 3), (2, 3), (0,), (1,), (2,)])
	) == frozenset([(0,), (1,), (2,)])
)

def join(F, G):
	return purgeSets(F.union(G))

assert(join(frozenset([(0, 1), (1, 2)]), set([(0, 1, 3)])) == frozenset([(0, 1), (1, 2)]))

def hamweight(w, n): #returns a list of all binary words of length n with hamming weight w
	assert(type(w) is int)
	assert(type(n) is int)
	if w < 0 or n < 0:
		return []
	if w == 0 and n == 0:
		return [()]
	return [(0,) + x for x in hamweight(w, n-1)] + [(1,) + x for x in hamweight(w-1, n-1)]

assert(hamweight(0, 1) == [(0,)])
assert(hamweight(1, 1) == [(1,)])
assert(hamweight(0, 5) == [x + (0,) for x in hamweight(0, 5-1)]) #and other values besides 5
assert(hamweight(1,0) == [])
assert(
	hamweight(2, 3) == [(0, 1, 1), (1, 0, 1), (1, 1, 0)]
)

def linearizationOfInclusionOrderForBinaryWords(n):
	return reduce(operator.add, [hamweight(i, n) for i in range(0, n+1)])

assert(
	reduce(operator.add, [(1, 2), (3, 4), (5, 6)]) == (1, 2, 3, 4, 5, 6)
)
assert(
	linearizationOfInclusionOrderForBinaryWords(3) == [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
)

def dominated(x, y):
	assert(type(x) is tuple)
	assert(type(y) is tuple)
	return all([x[i]<=y[i] for i in range(0, len(x))])

def injectiveSets(amap):
	assert(type(amap) is dict)
	return all(amap[k] != amap[l] for k in amap for l in amap if k != l)

def total(amap, k):
	assert(type(amap) is dict)
	assert(type(k) is int)
	if len(amap) != 2**k:
		return False
	return all(seq in amap for seq in itertools.product((0, 1), repeat=k))

def trueDict(three, x):
	assert(type(x) is tuple)
	assert(type(three) is int)
	return tuple(i for i in x if i != three) #without the "tuple" cast it becomes a generator object somehow.

def setTrue(three, L):
	assert(type(L) is frozenset) #sometimes set, sometimes frozenset!
	return frozenset([trueDict(three, F) for F in L])

assert(setTrue(3, frozenset([(0, 2, 3), (0, 1)])) == frozenset([(0, 2), (0, 1)]))

def setFalse(three, L):
	return frozenset([F for F in L if not three in F])

assert(setFalse(3, frozenset([(0, 2, 3), (0, 1)])) == frozenset([(0, 1)]))

words3 = linearizationOfInclusionOrderForBinaryWords(3)
words4 = linearizationOfInclusionOrderForBinaryWords(4)
words5 = linearizationOfInclusionOrderForBinaryWords(5)
words6 = linearizationOfInclusionOrderForBinaryWords(6)
words7 = linearizationOfInclusionOrderForBinaryWords(7)

#Comment out the ones we do not want among the following:
words = words3
words = words4
words = words5
words = words6
words = words7

def antichainorderSets(I, J):
	return all(
		[
			any(
				[subset(G, F) for G in J]
			) for F in I
		]
	)

assert(
	antichainorderSets(
		frozenset([(0,1,2),(0,3)]),
		frozenset([(0,1),(2,),(3,)])
	)
)

def isotonicSets(mymap):
	return all(antichainorderSets(mymap[i], mymap[j]) for i in mymap for j in mymap if dominated(i, j))

def updegreeSets(f, f4):
	degree = 0
	for g in f4:
		if antichainorderSets(f, g):
			degree += 1
	return degree


def basicCheck(u, i, g, words, setofmonotonefunctions):
	binarylength = len(words[0])
	veryBasic = all(
		not(
			(g[j] == u) or (dominated(words[j], words[i]) and not antichainorderSets(g[j], u))
		) for j in range(0, i)
	)
	if not veryBasic:
		#print "not veryBasic"
		return veryBasic
	#for j in range(0, i): # g[j] is an earlier value of g and we need g[i] above g[j] if words[i] is above words[j]
	#	if g[j] == u:
	#		return False
	#	if dominated(words[j],words[i]):
	#		if not antichainorder(g[j],u):
	#			return False
	#	#The following may be a good idea long term, but it is slow short term:
	#	updegreeOfJoinij = 2**(binarylength-sum([max(words[j][k],words[i][k]) for k in range(0, binarylength)]))
	#	enoughSpaceAbove = False
	#	v = join(g[j],u)
	#	#print "the join of " + str(g[j]) + " and " + str(u) + " was " + str(v)
	#	#for v in setofmonotonefunctions:#it is bad if v, the join of g[j] and u, is too high up. I.e. if all elements above g[j] and u have too small updegree.
	#	if updegreeSets(v,setofmonotonefunctions) < updegreeOfJoinij:
	#		#print theupdegree(v)
	#		#print updegreeOfJoinij
	#		#print words[i]
	#		#print words[j]
	#		return False
	return True


def ontoAdequate(L,setofmonotonefunctions):
	if setofmonotonefunctions == f4sets:
		setVar = 3
	else:
		setVar = 2
	myset = set()
	for F in L:
		myset.add(
			tuple(
				purgeSets(
					setTrue(setVar, L[F])
				),
			)
		)
		# https://stackoverflow.com/a/34375589/803990 well problem with that is what if the tuple has smaller length... so i use hash instead of len(tup), tup[0], tup[1]
		myset.add(tuple(purgeSets(setFalse(setVar, L[F])))) #
	#if (setofmonotonefunctions == f4 and len(myset))>=15: # in the context of binarylength=5 it seems 18 is usually achieved.
	#	print "Onto a set of size " + str(len(myset))
	#	for u in f3:
	#		print u, (tuple(u) in myset)
	if (setofmonotonefunctions == f4sets and len(myset)>=20) or (setofmonotonefunctions == f3sets and len(myset)>5):
		pass
		##print myset
		#print "Onto a set of size " + str(len(myset))
		#if setofmonotonefunctions == f4sets:
		#	for u in f3sets:
		#		print u, (tuple(u) in myset)
		#		#print "Is " + str(u) + " in " + str(myset) + " ?"
		##print L
		##print words
		#print
	if (setofmonotonefunctions == f4sets and len(myset) >= 19) or (setofmonotonefunctions == f3sets and len(myset) >= 5): #where 20 is the size of f3 and 6 the size of f2
		return True
	print "Onto a set of size " + str(len(myset))
	if setofmonotonefunctions == f4sets:
		for u in f3sets:
			print u, (tuple(u) in myset)
			#print "Is " + str(u) + " in " + str(myset) + " ?"
	return False


def recursiveEmbedding(gOld, setofmonotonefunctions, words, i):
	binarylength = len(words[0])
	g = gOld
	if i>0 and g[i-1] == frozenset([()]):
		#print "already reached top"
		return
	if i>=0:#to adjust printing frequency
		hashy = hash(str(g)) % 100
		if hashy >= 99: #to reduce printing frequency
			print str(i) + ", Hash " + str(hash(str(g)) % 100)
			#print "We are still at " + str(g[0:24])
		if (
			(setofmonotonefunctions == f4sets and binarylength == 7 and (i>=117 or (i>=117 and ontoAdequate(g, setofmonotonefunctions))))
			or
			(setofmonotonefunctions == f4sets and binarylength == 6 and (i>=64 or (i>=63 and ontoAdequate(g, setofmonotonefunctions))))#easily find one with i=63(really 64) but it's not ontoAdequate
			or
			(setofmonotonefunctions == f4sets and binarylength == 5 and (i>=32 or (i>=2 and ontoAdequate(g, setofmonotonefunctions))))#easily find i=32 but ontoAdequacy only 18
			or
			(setofmonotonefunctions == f4sets and binarylength == 4 and (i>=16 or (i>=2 and ontoAdequate(g, setofmonotonefunctions))))#onto 14 easily achieved
			or
			(setofmonotonefunctions == f3sets and binarylength == 5 and (i>=18 or (i>=17 and ontoAdequate(g, setofmonotonefunctions)))) #this doesn't make that sense as these can't be 1:1 #i=17 ontoadequate is easy for words5
			or
			(setofmonotonefunctions == f3sets and binarylength == 4 and (i>=16 or (i>=16 and ontoAdequate(g, setofmonotonefunctions))))
		):
			print "A sample function for i=" + str(i)
			for j in range(0, i+1):
				print words[j], ": ", g[j]
			print g
			print
	
	mytime = time.time()
	for l in range(0, len(setofmonotonefunctions)): # u is a potential value for g[i]
		if binarylength == 6 and l>96:
			return # this is to see if we can embed 2^6 into the "small" functions in F4
		if i<2:
			tabs = "\t"*i
			print tabs + str(round(100*l/float(len(setofmonotonefunctions)), 2)) + " per cent done at i=" + str(i)
		u = setofmonotonefunctions[l]
		newtime = time.time()

		#Some time-out seems to be necessary for words7. The following is a heuristic choice of time-out function.
		if (
			newtime - mytime > 1000000/float(i**2)
		):
			break

		#print u
		#we should move on if u is not one of the minimal covers of the join of all g[j] it needs to be above.
		if u == []:
			continue
		#updegreei = 2**(binarylength-sum(words[i]))

		#comment out this if want to get large embedding, even if provably can't extend all the way:
		#if setofmonotonefunctions == f4 and theupdegree(u) < updegreei: #can add: if the updegree, updegreei and level of current ontoness do not suffice for ultimate ontoness then continue?
		#	continue
		#	#print str(u) + " was too big as a target for " + str(words[i])

		if not basicCheck(u, i, g, words, setofmonotonefunctions):
			continue
		badU = False
		#for uu in setofmonotonefunctions: #this may seem slow, but we really don't want to go into the recursive step unless we are pretty sure it's a good idea.
		#	#but it is not neccessarily clear that this uu business is even a valid thing to check for.
		#	if uu != u and basicCheck(uu,i,g,words,setofmonotonefunctions) and antichainorder(uu,u):
		#		badU = True
		#		break
		if not badU:
			g[i] = u
			if i == len(words) - 1:
				if ontoAdequate(g, setofmonotonefunctions):#this actually tries to check for onto f3 behavior
					print "Success"
					raise SystemExit
				continue # i.e., keep looking by going sideways rather than up in the tree of possible embeddings
			if i<len(words)-1:
				#print "g is " + str(g)
				recursiveEmbedding(g, setofmonotonefunctions, words, i+1)
	#we are here if we looked through all u, the embedding is total, but not onto. so then we want to just return.

def probabilityForF4(F, words):
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

def fsets(n): # returns the list of all antichains on n letters
	if n == 0:
		return [
			frozenset([]),
			frozenset([()])
		]
	return [
		join(
			frozenset([t + (n-1,) for t in F]),
			G
		) for F in fsets(n-1) for G in fsets(n-1) if antichainorderSets(G, F)
	]


f3sets = fsets(3)
f4sets = fsets(4)
#Dedekind numbers:
assert(len(fsets(0)) == 2)
assert(len(fsets(1)) == 3)
assert(len(fsets(2)) == 6)
assert(len(f3sets) == 20)
assert(len(f4sets) == 168)

f4sets = sorted(f4sets, key = lambda F: (probabilityForF4(F, words7), -updegreeSets(F, f4sets)))


def isotonyReportSets():
	print "Is mymap4sets isotonic? " + str(isotonicSets(mymap4sets))
	print "Is mymap5sets isotonic? " + str(isotonicSets(mymap5sets))
	print "Is mymap6sets isotonic? " + str(isotonicSets(mymap6sets))
	print "Is mymap4ToF3sets isotonic? " + str(isotonicSets(mymap6sets))
	print "Is computerMap7 isotonic? " + str(isotonicSets(computerMap7))
	print "Is computerMap6 isotonic? " + str(isotonicSets(computerMap6))
	print
	print "Is mymap4sets ontoAdequate? " + str(ontoAdequate(mymap4sets, f4sets))
	print "Is mymap5sets ontoAdequate? " + str(ontoAdequate(mymap5sets, f4sets))
	print "Is mymap6sets ontoAdequate? " + str(ontoAdequate(mymap6sets, f4sets))
	print "Is mymap4ToF3sets ontoAdequate? " + str(ontoAdequate(mymap6sets, f3sets))
	print "Is computerMap7 ontoAdequate? " + str(ontoAdequate(computerMap7, f4sets))
	print "Is computerMap6 ontoAdequate? " + str(ontoAdequate(computerMap6, f3sets))
	print
	print "Is mymap4sets injective? " + str(injectiveSets(mymap4sets))
	print "Is mymap5sets injective? " + str(injectiveSets(mymap5sets))
	print "Is mymap6sets injective? " + str(injectiveSets(mymap6sets))
	print "Is mymap4ToF3sets injective? " + str(injectiveSets(mymap4ToF3sets))
	print "Is computerMap7 injective? " + str(injectiveSets(computerMap7))
	print "Is computerMap6 injective? " + str(injectiveSets(computerMap6))
	print
	print "Is mymap4sets total? " + str(total(mymap4sets, 4))
	print "Is mymap5sets total? " + str(total(mymap5sets, 5))
	print "Is mymap6sets total? " + str(total(mymap6sets, 6))
	print "Is mymap4ToF3sets total? " + str(total(mymap4ToF3sets, 4))
	print "Is mymap4ToF3sets total on words5? " + str(total(mymap4ToF3sets, 5))
	print "Is computerMap7 total? " + str(total(computerMap7, 7))
	print "Is computerMap6 total? " + str(total(computerMap6, 6))
	print "Cardinality of domain of computerMap7: " + str(len(computerMap7))
	print "Cardinality of domain of computerMap6: " + str(len(computerMap6))
	print
isotonyReportSets()


g = [frozenset([()]) for w in words]

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
#g[0]=set([(0,1,2)])
#recursiveEmbedding(g,f3sets,words,1)
#raise SystemExit #works!

#to embed into f4minus:
g[0] = frozenset([(0, 1, 2, 3)])
recursiveEmbedding(g, f4sets, words, 1)
raise SystemExit

recursiveEmbedding(g, f4, words, 0)
raise SystemExit

recursiveEmbedding(g, f3minus, words, 0)
raise SystemExit

