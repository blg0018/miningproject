coresets.py

usage: python coresets.py m
example: python coresets.py 1000

In the experiments done in the paper, the values of m used were: {1000, 2000, 5000, 10000, 20000}

Once the lightweight coresets are computed, they are exported to a file called "export.dat" in the same directory.
The resulting coresets are evaluated in a separate k-means++ algorithm and compared for accuracy and performance