'''
Created on Oct 1, 2016
'''
from itertools import chain, combinations

#Class of functional dependencies in which lhs --> rhs implies that 
#the rhs can be determined from the lhs.
class fd:
    def __init__(self,lhs,rhs): #constructs a functional dependency
        self.lhs = frozenset(lhs)
        self.rhs = frozenset(rhs)
    def __str__(self): #Create a string for printing the FD
        return str(list(self.lhs)) +'-->' + str(list(self.rhs))
    def isTrivial(self): #Check if the lhs is part of the rhs, such that the FD is trivial
        return self.lhs >= self.rhs
    def __eq__(self, other): #Compare two FDs
        return (self.lhs == other.lhs) & (self.rhs == other.rhs)
    def __hash__(self): #Making fd hashable
        return hash(self.lhs) * hash(self.rhs)

#Class of closure which stores the closure of the given FDs in a relation.        
class closure:
    def __init__(self,attr,given_fds):
        self.attr = attr
        self.given_fds = set()
        self.clsr = set()
        for i in range(0,len(given_fds)):
            self.given_fds.add(getFD(given_fds[i]))
        self.getclosure()
        
    def getclosure(self): #generates the closure of the given fd
        #add trivial fds to the set of all known fds 
        known_fds = self.given_fds.union(usereflexivity(self.attr))
        #repeat using augmentation and transitivity until the closure does not change anymore
        done = False;
        while done == False:
            all_fds = useaugmentation(known_fds,pset(self.attr))
            all_fds = usetransitivity(all_fds)
            done = len(all_fds)==len(known_fds)
            known_fds = all_fds
        self.clsr = known_fds
        
    def __str__(self):
        toPrint = []
        count = 0
        for f in self.clsr:
            toPrint.append(str(f))
            count += 1
        return str(toPrint) + ' The number of closure is: ' + str(count)

#Create a fd object from the given fd tuple       
def getFD (fd_id):
    a_fd = fd(fd_id[0],fd_id[1])
    return a_fd       

#Generate a list of all possible combinations of attributes in a set
def pset(a_set):
    return list(chain.from_iterable(combinations(a_set,a) for a in range (1, len(a_set)+1)))

#Generate a set of trivial FD for given attributes   
def usereflexivity(r):
    all_ref = set()
    for i in pset(r):
        for j in pset(i):
            all_ref.add(fd(i,j))
    return all_ref

#Generate a set of augmented fd for the set of fiven fd
#f is a set of fd, PS is the powerset of all attributes in the schema
def useaugmentation(f,PS):
    augmented = set()
    for i in f:
        for j in PS:
            augmented.add(fd(i.lhs.union(j),i.rhs.union(j)))
    return augmented

#Generate a set of fds derived from the transitivity rule
#param f: set of fd
def usetransitivity(f):
    trans = set()
    for i in f:
        for j in f:
            if i.rhs == j.lhs:
                trans.add(fd(i.lhs,j.rhs))
    return f.union(trans)

#Find all the superkeys by looking at the rhs of fds in the closure
def superkeys (attr, clsr):
    skey = set()
    for f in clsr:
        if len(f.rhs) == len(attr):
            skey.add(f.lhs)
    return skey


#Check if there is a fd such that lhs is not a skey
def inBCNF(clsr,skeys):
    for f in clsr:
        if (not f.isTrivial()) and (f.lhs not in skeys):
            return False
    return True

def badFd(clsr, skeys):
    sorted_clsr = sorted(clsr,lambda x,y:cmp(len(x.lhs),len(y.lhs)))
    for f in sorted_clsr:
        if ((not f.isTrivial()) and (f.lhs not in skeys)):
            return f

def decomposeRelation(bad_fd, attr, clsr):
    PartOne = bad_fd.lhs | bad_fd.rhs
    PartTwo = (attr - bad_fd.rhs) | bad_fd.lhs
    PartOne_clsr = set()
    PartTwo_clsr = set()
    for f in clsr:
        if (f.lhs <= PartOne) and (f.rhs <= PartOne):
            PartOne_clsr.add(f)
        if (f.lhs <= PartTwo) and (f.rhs <= PartTwo):
            PartTwo_clsr.add(f)
    return (PartOne, PartTwo, PartOne_clsr, PartTwo_clsr)

def decomposeToBCNF(attr, clsr):
    result = attr #convert from list to set in another function
    print 'The relation to be decomposed is: '+ str(list(attr))
    skeys = superkeys(attr,clsr) #return a set of skeys
    if not inBCNF(clsr,skeys):
        print 'This is not in BCNF'
        fd = badFd(clsr,skeys) #return the key to decompose by
        print 'This relation is decomposed using the fd: '+ str(fd)
        (PartOne,PartTwo,PartOne_clsr,PartTwo_clsr) = decomposeRelation(fd,attr,clsr)
        print 'The decomposed relations are: ' + str(list(PartOne)) +' and '+ str(list(PartTwo)) 
        #recurse
        decomposeToBCNF(PartOne,PartOne_clsr)
        decomposeToBCNF(PartTwo,PartTwo_clsr)
    else:
        print 'This is in BCNF, so it is not further decomposed.'
        aList.append(list(result))

def bcnf(attr,allfds):
    global aList
    aList = []
    R = set(attr)
    temp = closure(attr,allfds)
    clsr = temp.clsr
    decomposeToBCNF(R, clsr)
    return 'The decomposed relations in BCNF are: ' + str(aList)
    
    
    
def main():
    fd1 = ([1],[2])
    fd2 = ([2,3],[4,5]) 
    #fd3 = ([6],[7]) #tuples of lists
    allfds =[fd1,fd2] #list of tuples of lists
    print(closure([1,2,3,4,5],allfds))
    print(bcnf([1,2,3,4,5],allfds))


main()