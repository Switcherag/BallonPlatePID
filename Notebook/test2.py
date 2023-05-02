from ipyparallel import Client

# create a cluster of 4 engines
rc = Client()
view = rc[:]

# define a function to compute the sum of an array
def compute_sum(arr):
    return sum(arr)

# create a large array
arr = list(range(10000000))

# split the array into 4 equal parts
chunks = [arr[i::4] for i in range(4)]

# distribute the chunks to the engines
view.scatter('chunk', chunks)

# execute the function on each engine in parallel
results = view.apply(compute_sum, 'chunk')

# collect the results and compute the final sum
final_sum = sum(results.get())

print(final_sum)
