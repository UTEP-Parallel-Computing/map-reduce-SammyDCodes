def parallelCountDocuments(file_dirs):
    # Create shared dictionary to store the counting result of words
    sharedDict = pymp.shared.dict()    # Declare a shared dictionary
    sharedDict = makeWordsDict(words,sharedDict)    # Initialize the elements within shared dict
    
    # Create shared dict which tracks the time usage of reading file and counting words
    sharedTime = pymp.shared.dict()
    sharedTime["Read"] = 0
    sharedTime["Count"] = 0
    
    print("Start Parallel\n===========================")
    
    # Start timing the whole paralleling computation time
    start = timeit.default_timer()
    
    with pymp.Parallel() as p:
        num_threads = p.num_threads      # Get the total number of threads have been used
        dictLock = p.lock      # Create a lock
        for i in p.range(len(file_dirs)):
            
            print(f"Thread {p.thread_num} starts work.")
            
            count_dict, read_time, count_time = countDocument(file_dirs[i]) # Count document
            
            # Update shared data
            dictLock.acquire()
            
            # Update words' counts
            for key in sharedDict.keys():
                sharedDict[key] += count_dict[key]
            # Update file reading time and words counting time
            sharedTime['Read'] += read_time
            sharedTime['Count'] += count_time
            dictLock.release()
            
            print(f"Thread {p.thread_num} has done it's work on file {file_dirs[i]}")
            
    stop = timeit.default_timer()
    print("===========================\n")
    total_time_usage = stop-start
    sharedTime["Total"] = total_time_usage
    return sharedDict, sharedTime, num_threads

def main():
    # Get directory for each text file
    file_dirs = getTextFileDirs(DOCUMENT_PATH)
    # Parallel counts the occurrences of given word
    count_result, time_usage, num_threads = parallelCountDocuments(file_dirs)
    
    total_time = time_usage["Total"]
    read_time = time_usage["Read"]
    count_time = time_usage["Count"]
    # Print out the counting results by words
    print("Resulting wordcounts")
    for w,c in count_result.items():
        print(f"{w}: {c}")
    print("\n===========================")
    print(f"Number of Threads: {num_threads}\nTotal Parallel Operation Time: {total_time}\nTotal File Read Time: {read_time}\nTotal Words Count Time: {count_time}")
    print("===========================\n")

if __name__=="__main__":
    import pymp
    import timeit
    from wordsUtils import getTextFileDirs, makeWordsDict, countDocument, DOCUMENT_PATH, words

    # execute only if run as a script
    main()
    

