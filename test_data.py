
import pickle
import numpy as np
import sys

print "\n===== test script =====\n"

hoc_path = sys.argv[1]
print "Loading hoc_data from ", hoc_path
hoc_data = np.loadtxt(hoc_path, skiprows=1)

python_path = sys.argv[2]
print "Loading python_data from ", python_path
f = open(python_path, 'rb')
python_data = pickle.load(f)


p_data = np.array(python_data).T

def print_comparison(i):
    print "hoc_data: \t", hoc_data[i]
    print "python_data: \t", p_data[i]
    
print "\n"

max_diff = np.max(p_data - hoc_data)

print "max diff: ", max_diff
if max_diff < 0.001:
    print "TEST PASSED"
else:
    print "FAILED"

k = np.random.randint(0, len(python_data[0]))
print "\nRandom pair (k=%d):" % k
print_comparison(k)

print "\n"
