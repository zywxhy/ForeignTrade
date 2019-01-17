from django.test import TestCase

# Create your tests here.
from collections import Counter



dict = {'a':1,'b':5}
dict2 = {'a':2,'c':7}

counter = Counter(dict)
counter.update(dict2)
print(counter)