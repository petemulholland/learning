import datetime
import random


# exercise 11-2
def histogram(s):
    d = dict() 
    for c in s: 
        d[c] = d.get(c, 0) + 1
        
    return d


# exercise 11-3
def print_hist(h): 
    for c in sorted(h.keys()): 
        print c, h[ c]


# exercise 11-4
def reverse_lookup(d, v): 
    keys = []
    for k in d: 
        if d[k] == v: 
            keys.append(k)

    return keys

# exercise 11-5
def invert_dict(d): 
    inverse = dict() 
    for key in d: 
        val = d[key] 
        inverse.setdefault(val, []).append(key)
      
    return inverse

def test_invert_dict():
    hist = histogram('brontosaurus')
    print reverse_lookup(hist, 2)
    inv = invert_dict(hist)
    print inv

# exercise 11-6
def fibonacci(n): 
    if n == 0: 
        return 0 
    elif n == 1: 
        return 1 
    else: 
        return fibonacci(n-1) + fibonacci(n-2)


known = {0: 0, 1: 1} 
def fibonacci_memo(n): 
    if n in known: 
        return known[n] 
    res = fibonacci_memo(n-1) + fibonacci_memo(n-2) 
    known[n] = res 
    return res

def compare_fibonacci():
    test = 25
    start = time.time()
    fibonacci(test)
    elapsed = time.time() - start
    print "fibonacci({0}) took: {1}".format(test, elapsed)

    start = time.time()
    fibonacci_memo(test)
    elapsed = time.time() - start
    print "fibonacci_memo({0}) took: {1}".format(test, elapsed)

indent = 0
# exercise 11-7
def ack(m, n):
    global indent
    indent += 1
    print "{0}ack({1}, {2})".format('  ' * indent, m, n), 
    if m == 0:
        a = n + 1
        print "returning {0}".format(a)
        indent -= 1
        return a
    elif m > 0 and n == 0:
        a = ack(m - 1, 1)
        print "returning {0}".format(a)
        indent -= 1
        return a
    elif m > 0  and n > 0:
        a = ack(m - 1, ack(m, n - 1))
        print "returning {0}".format(a)
        indent -= 1
        return a
    else:
        return None

def test_ack():
    for i in range(4):
        for j in range(5):
            a = ack(i, j)
            #print "ack({0}, {1}): {2}".format(i,j,a) 

# exercise 11-9
def has_duplicates(t):
    ds = dict()
    for d in t:
        if d not in ds:
            ds[d] = 1
        else:
            return True
    
    return False

def ex_11_9():
    t = [1, 2, 3]
    print has_duplicates(t)
    t.append(1)
    print has_duplicates(t)
    

# exercise 11-10
def read_word_dict():
    """Read the words in words.txt and return a dictionary
    that contains the words as keys"""
    d = dict()
    fin = open('..\words.txt')
    for line in fin:
        word = line.strip().lower()
        d[word] = word

    return d

def rotate_word(s, n):
    start = 0

    result = ''
    for c in s:
        if not c.isalpha():
            print c, " is not an alpha char"
            break

        if c.isupper():
            start = ord('A')
        else:
            start = ord('a')

        i = ord(c) - start
        result += chr((i + n) % 26 + start)

    return result

def find_word_pairs(word, words):
    for i in range(1,26):
        rot = rotate_word(word, i)
        if rot in words:
            print word, i, rot

def ex_11_10():
    words = read_word_dict()

    for word in words:
        find_word_pairs(word, words)

if __name__ == '__main__':
    #print histogram('brontosaurus')
    #print_hist(histogram('brontosaurus'))
    #test_invert_dict()
    #compare_fibonacci()
    #test_ack()
    #ex_11_9()
    ex_11_10()
