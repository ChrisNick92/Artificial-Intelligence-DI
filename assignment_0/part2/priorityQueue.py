import heapq
import random # To test the sorting, see below
import time   # To count the sorting execution

class PriorityQueue():
    def __init__(self):
        self.heap = []
        self.count = 0
    def isEmpty(self):
        return True if self.count == 0 else False
    
    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))
        self.count+=1
    
    def pop(self):
        if self.count != 0:
            self.count-=1
            value = heapq.heappop(self.heap)[1]
            return value
        else:
            print("Queue is empty!")
    
    def update(self, item, priority):
        all_items = [x[1] for x in self.heap]
        if item in all_items:
            idx = all_items.index(item)
            value = self.heap[idx][0]
            if value > priority:
                self.heap[idx][0] = priority
        else:
            self.push(item, priority)
            
def PQSort(unsorted_list):
    sorted = []
    q = PriorityQueue()
    for value in unsorted_list:
        q.push(value, value)
    while q.count != 0:
        sorted.append(q.pop())
    return sorted

# The function test_sorting is created to test the sorting procedure
def test_sorting(test = {"START": 1, "END": 1000000, "K": 100000}):
    """
    Arguments:
    - test: A dictionary with keys START, END, K. The test dictionary
    sets up the configuration of the test. It creates a random list of
    integers of length K selected randomly from the interval [START, END]
    
    The function creates a random list of integers of length K and sorts it
    in ascending order using the PQSort function. It measures the execution
    time and compares the result with implementation of Python's sorting
    function 'sorted'.
    """
    times = {"Custom": 0.0, "Python": 0.0}
    print(f"{5*'-'}> Performing a sorting test <{5*'-'}")
    print(f"- Selecting {test['K']} random integer values from the interval [{test['START']},{test['END']}]")
    x = random.sample(range(test["START"], test["END"]), test["K"])
    print(f"- Sorting...")
    tic = time.time()
    custom_sort = PQSort(x)
    tac = time.time()
    times["Custom"] = tac - tic
    tic = time.time()
    python_sort = sorted(x)
    tac = time.time()
    times["Python"] = tac - tic
    result, bool = (f"- Sorting completed successfully...", True) if custom_sort == python_sort else (f"- Sorting failed...", False)
    print(result)
    if bool:
        print(f"- Time Results: Custom implementation: {times['Custom']:.4f} secs, Python implementation: {times['Python']:.4f} secs")
    

if __name__ == "__main__":
    # This code runs when you invoke the script from the command line
    # It serves only for testing purposes
    # It tests basic operations of the PriorityQueue as well as the sorting procedure
    
    test_1 = {"START": 1, "END": 1000000, "K": 100000}
    test_2 = {"START": 1, "END": 10000000, "K": 1000000}
    
    q = PriorityQueue() # Initialize an empty PriorityQueue
    print(f"- Is the queue empty? {q.isEmpty()}")
    print(f"- Pushing in order the pairs ('task1', 1), ('task1',2), ('task0', 0)...")
    q.push("task1", 1)
    q.push("task1",2)
    q.push("task0",0)
    print(f"- Heap state: {q.heap}")
    print(f"- Performing a pop. Result: {q.pop()}")
    print(f"- Perfoming a pop. Result: {q.pop()}")
    print(f"- Pushing the pairs ('task3', 3), ('task3', 4), ('task2', 0)...")
    q.push("task3", 3)
    q.push("task3", 4)
    q.push("task2",0)
    print(f"- Heap state: {q.heap}")
    print(f"- Performing a pop. Result: {q.pop()}\n")
    
    print(f"{5*'-'}> Testing the sorting <{5*'-'}\n")
    
    # Perfmorming Test 1 for sorting
    test_sorting(test_1)
    # Performing Test 2 for sorting
    test_sorting(test_2)