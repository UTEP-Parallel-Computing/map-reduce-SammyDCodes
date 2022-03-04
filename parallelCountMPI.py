def parallelCount(file_dirs):

    # get the world communicator
    comm = MPI.COMM_WORLD

    # get our rank (process #)
    rank = comm.Get_rank()

    # get the size of the communicator in # processes
    size = comm.Get_size()
    
    # get counting file list
    golablDocNames = getTextFileDirs(file_dirs)
    
    # record time
    total_time_start = timeit.default_timer()
    
    # thread 0 distributes the work
    if rank == 0:
        print('Thread 0 distributing')
        docsPerThread = len(golablDocNames) / size
        
        # first setup thread 0s slice of the list
        localList = golablDocNames[:int( docsPerThread )]
        
        for process in range(1, size):
            #start and end of slice we're sending
            startOfSlice = int( docsPerThread * process )
            endOfSlice = int( docsPerThread * (process + 1) )
            
            sliceToSend = golablDocNames[startOfSlice:endOfSlice]
            comm.send(sliceToSend, dest=process, tag=0)
            
        # count its assigned files
        words_dict, time_dict = countMultipleFiles(localList)
        
        # loop to receive updates from other threads
        for process in range(1,size):
            recvd_count,recvd_time = comm.recv(source=process, tag=1)
            print(f'Thread 0 recieved from {process}')
            words_dict, time_dict = updateCountAndTime(words_dict, time_dict, recvd_count, recvd_time)
            
        total_time_end = timeit.default_timer()
        
        # update total computation time.
        time_dict["Total"] = total_time_end - total_time_start
        
        total_time = time_dict["Total"]
        read_time = time_dict["Read"]
        count_time = time_dict["Count"]
        # Print out the counting results by words
        print("\n===========================")
        print("Resulting wordcounts")
        for w,c in words_dict.items():
            print(f"{w}: {c}")
        print("\n===========================")
        print(f"Number of Threads: {size}\nTotal Parallel Operation Time: {total_time}\nTotal File Read Time: {read_time}\nTotal Words Count Time: {count_time}")
        print("===========================\n")
            
    #everyone else receives that message
    else:
        # receive assigned file names from thread 0 with tag of 0
        localList = comm.recv(source=0, tag=0)
        print(f"Thread {rank} received {localList}.")
        
        # counts file
        words_dict, time_dict = countMultipleFiles(localList)
        
        # send data back to thread 0
        comm.send([words_dict,time_dict], dest=0, tag=1)
            
def main():
    parallelCount(DOCUMENT_PATH)

if __name__=="__main__":
    from mpi4py import MPI
    import timeit
    from wordsUtils import getTextFileDirs, DOCUMENT_PATH,  \
                       countMultipleFiles, updateCountAndTime
    main()