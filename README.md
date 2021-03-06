# Parallel-Computing-MapReduce
---
### Motivation
For this assignment you will write a parallel map reduce program. The program will search for a set of words among a set of documents that constitute the works of Shakespeare. The set of words is listed below. The assignment should use the map-reduce design pattern to split up the work. You should have functions that count the number of a specific word within a specific document and combine the individual word counts.

### Idea
We count words by using MapReduce model. MapReduce is a programming model and an associated implementation for processing and generating big data sets with a parallel, distributed algorithm on a cluster \[[[1]]]. First, we assign documents to threads and count them seprately (Map). And then we sum up the counting result (Reduce). We assign work by documents since this will avoid the overhead problem, in other words, each document will only be copied once by one thread and be counted (If we assign work by "words", then each document will be copied once by each thread. Then there will be num_threads*num_documents copy work.).
![model](model.png)
Number of documents assigned to each file is: num_files/num_threads.

### Approaches
We have two types of APIs can be used to develop parallel program: OpenMP and MPI.
- __OpenMP__ (Open Multi-Processing) is an application programming interface (API) that supports multi-platform __shared-memory__ multiprocessing programming on many platforms. \[[[2]]]
- __MPI__ (Message Passing Interface) is a standardized and portable message-passing standard designed to function on parallel computing architectures. \[[[3]]]

Generally, OpenMP is used for parallelism _**within a (multi-core) node**_ while MPI is used for parallelism _**between nodes**_. \[[[4]]] In reality, some peple make efforts to translate OpenMP into MPI and extend OpenMP for non-shared memory systems.
#### Approcah 1: OpenMP

##### Program Descrition
This program contains two scripts `wordsUtils.py` and `parallelCount.py`.
- `wordsUtils.py` contains the helper functions to:
  - `getTextFileDirs` Read the text file lists with default file directory
  - `makeWordsDict` Genrate words counting dictionary with given default set of words
  - `countDocument` Count words by given file directory
- `parallelCount.py` contains parallel method which is developed by __OpenMP__.

##### Command to run the code
```
OMP_NUM_THREADS=8 python parallelCount.py
```

##### Result
Sample output:
```
Start Parallel
===========================
Thread 1 starts work.
Thread 2 starts work.
Thread 3 starts work.
Thread 4 starts work.
Thread 5 starts work.
Thread 0 starts work.
Thread 6 starts work.
Thread 7 starts work.
Thread 2 has done it's work on file ./documents/shakespeare1.txt
Thread 1 has done it's work on file ./documents/shakespeare3.txt
Thread 3 has done it's work on file ./documents/shakespeare4.txt
Thread 7 has done it's work on file ./documents/shakespeare8.txt
Thread 5 has done it's work on file ./documents/shakespeare7.txt
Thread 4 has done it's work on file ./documents/shakespeare5.txt
Thread 6 has done it's work on file ./documents/shakespeare6.txt
Thread 0 has done it's work on file ./documents/shakespeare2.txt
===========================

Resulting wordcounts
hate: 332
love: 3070
death: 1016
night: 1402
sleep: 470
time: 1806
henry: 661
hamlet: 475
you: 23306
my: 14203
blood: 1009
poison: 139
macbeth: 288
king: 4545
heart: 1458
honest: 434

===========================
Number of Threads: 8
Total Parallel Operation Time: 0.509950088
Total File Read Time: 0.04300667700000005
Total Words Count Time: 2.3074974860000004
===========================
```

\# of files | \# of Threads | Total Time Usage (Seconds) | Cumulative File Read Time | Cumulative Words Count Time
--- | --- | --- | --- | --- 
8 | 1 | 2.091615451 | 0.02756350599999996 | 1.978922616
8 | 2 | 1.330601013 | 0.03238631999999972 | 1.955139615 
8 | 4 | 0.77256599 | 0.03461293600000001 | 2.163536268
8 | 8 | 0.509950088 | 0.04300667700000005 | 2.3074974860000004
8 | 16 | 0.50859671 | 0.047722181999999974 | 2.296346835

#### Approach 2: MPI
##### Program Description
This program contains two scripts `wordsUtils.py` and `parallelCountMPI.py`.
- `wordsUtils.py` contains the helper functions to:
  - `getTextFileDirs` Read the text file lists with default file directory
  - `countMultipleFiles` Count words by given file lists
  - `updateCountAndTime` Update count and time dictionary with another count and time dictionary
- `parallelCountMPI.py` contains parallel method which is developed by __MPI__.

##### Command to run the code
```
mpirun -n 8 python parallelCountMPI.py
```

##### Result
Sample output:
```
Thread 2 received ['./documents/shakespeare1.txt'].
Thread 1 received ['./documents/shakespeare3.txt'].
Thread 3 received ['./documents/shakespeare4.txt'].
Thread 7 received ['./documents/shakespeare8.txt'].
Thread 5 received ['./documents/shakespeare7.txt'].
Thread 4 received ['./documents/shakespeare5.txt'].
Thread 6 received ['./documents/shakespeare6.txt'].
Thread 0 distributing
Thread 0 recieved from 1
Thread 0 recieved from 2
Thread 0 recieved from 3
Thread 0 recieved from 4
Thread 0 recieved from 5
Thread 0 recieved from 6
Thread 0 recieved from 7

===========================
Resulting wordcounts
hate: 332
love: 3070
death: 1016
night: 1402
sleep: 470
time: 1806
henry: 661
hamlet: 475
you: 23306
my: 14203
blood: 1009
poison: 139
macbeth: 288
king: 4545
heart: 1458
honest: 434

===========================
Number of Threads: 8
Total Parallel Operation Time: 0.46529664099999996
Total File Read Time: 0.030713549999999992
Total Words Count Time: 2.365410769
===========================
```
\# of files | \# of Threads | Total Time Usage (Seconds) | Cumulative File Read Time | Cumulative Words Count Time
--- | --- | --- | --- | --- 
8 | 1 | 1.851867927 | 0.027945872999999774 | 1.8208808309999998
8 | 2 | 1.20986934 | 0.024782368000000013 | 1.902784849
8 | 4 | 0.638393521 | 0.025561805999999937 | 1.9428939769999998
8 | 8 | 0.4511724180000001 | 0.03617735 | 2.310217706
8 | 16 | 0.618557641 | 0.051035142000000006 | 3.224813266

#### Analysis
1. My cpu contains 8 cores.
   - When # of Threads <= 8:
     - __The increase threads usage decreases the total time usage__:
    This is because: total_time = max({threads_time_usage}). 
     As long as we use more threads, each thread will handle less amount of files. The computation time of each thread will decrease. Therefore, the maximum computation time of threads will decrease, the total time usage of our parallel program will decrease.
     - __The increase threads usage increases cumulative time usage for reading file but decreases the reading time overall__
     The increase of cumulative time usage is due to the system requires more time to allocate the distributed memory as long as there are more threads have been involved. However, the average time usage, in other words, real time usage decreases. This is because the more threads have been used make each thread take care of less number files. Reading less files make each thread spent less file reading time.
     - __The increase threads usage increases cumulative time usage for counting file but decreases the counting time overall__
     The increase of cumulative time usage is due to the system requires more time to allocate the computing resources. However, the average time usage, in other words, real time usage decreases. This is because the more threads have been used make each thread take care of less number of files. Counting less files make each thread spent less file counting time.
   - When # of Threads > 8:
     - For __OpenMP__: Time usages are not changing. This is because our implemented threads are more than the number of processors. Excessed number of threads will be assigned to processor and run after the previous thread is finished. However, we have 8 files in total. Therefore, the excessed number of threads have no assigned work. So, the total time does not change (maybe slightly increase since it requires more resource allocation work).
     - For __MPI__: Time usage increases. This is because we only have 8 files, the excessed number of run time environments (threads) have no work to do. However, the excessed threads require more communication time. So, the total time usage increases.

## Result Analysis
1) What problems you encountered completing the assignment and how you overcame them?
```
A: I first worte a dictionary initialization function which has a default input dictionary. It causes a problem since each method, which used this function, will refer to the same dictionary object. This generates weird result. To solve it, everytime when I call this dictionary initialization function, I make a shallow copy of it.
```
2) Any problems you weren't able to overcome or any bugs still left in the program?
```
A: No.
```
3) About how long it took you to complete the assignment?
```
A: About 6 hours.
```

4) Any observations or comments you had while doing the assignment?
```
A: None
```
5) Output from the cpuInfoDump.sh program
```
I'm doing this homework by using my own computer, therefore I used different bash commands. The returned results:
Intel(R) Core(TM) i9-9980HK CPU @ 2.40GHz
physicalcpu: 8
logicalcpu: 16
```

### References
<a id="1">[1]</a> MapReduce - Wikipedia. (2022). Retrieved 1 March 2022, from https://en.wikipedia.org/wiki/MapReduce
<a id="2">[2]</a> OpenMP - Wikipedia. (2017). Retrieved 1 March 2022, from https://en.wikipedia.org/wiki/OpenMP
<a id="3">[3]</a> Message Passing Interface - Wikipedia. (2021). Retrieved 1 March 2022, from https://en.wikipedia.org/wiki/Message_Passing_Interface
<a id="4">[4]</a> MPI and OpenMP with Python ??? Deep Learning Garden. (2017). Retrieved 1 March 2022, from https://deeplearning.lipingyang.org/2017/02/17/python-and-mpi/

### Developer
Sammy (Siyu) Deng