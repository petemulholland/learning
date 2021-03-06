import random

def sumall(*args):
    sum = 0
    for num in args:
        sum += num

    return sum

def ex_12_01():
    print "sumall(1, 2, 3)", sumall(1, 2, 3)
    print "sumall(1, 2, 3, 4)", sumall(1, 2, 3, 4)
    print "sumall(1, 2, 3, 4, 5)", sumall(1, 2, 3, 4, 5)
    print "sumall(1, 2, 3, 4, 5, 6)", sumall(1, 2, 3, 4, 5, 6)


def sort_by_length_random(words): 
    t = [] 
    word_ct = len(words)
    for word in words: 
        t.append((len(word), random.randint(0,word_ct), word)) 
        
    t.sort( reverse = True) 
    
    res = [] 
    for length, rnd, word in t: 
        res.append( word) 
        
    return res


def ex_12_02():
    words = ['John', 'Eric', 'Graham', 'Gerry', 'Terry', 'Peter', 'Michael', 'Mick']

    t = sort_by_length_random(words)
    for x in t:
        print x

    print

def most_frequent(t):
    l = tuple(t)
    d = dict()
    for letter in l:
        if letter.isalpha():
            if not d.has_key(letter):
                d[letter] = 1
            else:
                d[letter] += 1

    t2 = zip(d.values(), d.keys())
    t2.sort(reverse=True)

    return t2


def ex_12_03():
    print most_frequent("The quick brown fox jumps over the lazy dog")


def read_words():
    fin = open('..\words.txt') 
    words = []
    for line in fin: 
        word = line.strip()
        words.append(word)

    return words

def make_histogram(s):
    """Make a map from letters to number of times they appear in s.
    s: string
    Returns: map from letter to frequency
    """
    hist = {}
    for x in s:
        hist[x] = hist.get(x, 0) + 1
    return hist

def print_anagrams(anas):
    for ana in anas.values():
        if len(ana) > 1:
            print ana

def get_anagrams():
    # for each word read in:
    #   create a histogram of the word and sort
    #   get a tuple from the histogram
    #   use histogram as dict key and add word to list for that key
    # TODO: read in words
    words = read_words()
    anas = dict()
    for word in words:
        hist = make_histogram(word)
        h1 = hist.items() # list of tuples
        h1.sort() # sort the list
        key = tuple(h1) # make a tuple of tuples
        anas[key] = anas.get(key, []) + [word]

        #if len(anas[key]) > 2: # ?? for debugging to catch anagrams?
        #    pass

    return anas

def ex_12_04_1():
    anas = get_anagrams()
    print_anagrams(anas)

def order_anagrams_by_word_count(anas):
    o = [] # list?
    for key, val in anas.items(): # add everything to a list of tuples with first tuple element as word count.
        o.append((len(val), key, val))

    o.sort(reverse=True) # order the collection by word count desc

    # now I want to strip out the vals as ordered.
    l = []
    for count, key, val in o:
        l.append(val)

    return l


def ex_12_04_2():
    anas = get_anagrams()
    lanas = order_anagrams_by_word_count(anas)
    for l in lanas:
        print l

def get_letter_count(hist):
    count = 0
    for letter, num in hist:
        count += num

    return count

def ex_12_04_3():
    anas = get_anagrams()
    word_count = 0
    o = [] # list?
    for key, val in anas.items(): # pick out values with a 8 letter count
        if get_letter_count(key) == 8:
            o.append((len(val), key, val))

    o.sort(reverse=True) # order the collection by word count desc
    for wcount, key, val in o:
        if word_count == 0:
            word_count = wcount

        if wcount < word_count:
            break

        print val

def count_diffs(word1, word2):
    diffs = 0
    for l1, l2 in zip(word1, word2):
        if l1 != l2:
            diffs += 1
        if diffs > 2:
            break
    return diffs

def find_metathesis_pairs(anas):
    mps = []
    for i in range(len(anas) - 1):
        word1 = anas[i]
        for word2 in anas[i+1:]:
            diffs = count_diffs(word1, word2)
            if diffs == 2:
                mps.append((word1, word2))
    return mps

def ex_12_05():
    # metathesis pairs:
    # go thru all anagrams and get word where there are only 2 differences
    anas = get_anagrams()
    mps = []
    for ana in anas.values():
        if len(ana) > 1:
            pairs = find_metathesis_pairs(ana)
            if len(pairs) > 0:
                mps.extend(pairs)

    for pair in mps:
        print pair

childless = []
reduced = dict()

def get_children(word, dictionary):
    children = []
    for i in range(len(word)):
        part1 = ""
        part2 = ""
        if i > 0:
            part1 = word[:i]
        if i < len(word):
            part2 = word[i+1:]
        child = part1 + part2

        if len(child) > 0 and child in dictionary and child not in children:
            children.append(child)
    
    return children

def is_reducible(word, dictionary, reduction):
    global childless, reduced

    if len(word) == 1:
        reduction.append(word)
        return True
    
    if word in childless:
        return False

    if word in reduced:
        reduction.extend(reduced[word])
        return True

    children = get_children(word, dictionary)
    if len(children) == 0:
        childless.append(word)
        return False

    for child in children:
        reduct = []
        if is_reducible(child, dictionary, reduct):
            reduction.append(word)
            reduction.extend(reduct)
            reduced[word] = reduction
            return True

    return False

def ex_12_06():
    words = read_words()
    words.append("i")
    words.append("a")
    for word in words:    
        reduction = []
        if is_reducible(word, words, reduction):
            print word, reduction
    pass


if __name__ == '__main__':
    #ex_12_01()
    #ex_12_02()
    #ex_12_02()
    #ex_12_03()
    #ex_12_04_1()
    #ex_12_04_2()
    #ex_12_04_3()
    #ex_12_05()
    ex_12_06()
