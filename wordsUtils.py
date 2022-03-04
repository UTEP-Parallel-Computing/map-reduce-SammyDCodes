import os
import re
import timeit

# DOCUMENT_PATH = "./documents"
DOCUMENT_PATH = "./"
words = ["hate", "love", "death", "night", "sleep", "time", "henry", "hamlet","you", "my", "blood", "poison", "macbeth", "king", "heart", "honest"]

def countWord(string, word):
    # Count word's occurrences with given string
    return len(re.findall(word,string))

def countWords(string, words_dict):
    # Iterate by words in words list, count the occurrences
    # of each word and update their countings
    for w in words_dict.keys():
        words_dict[w] += countWord(string,w)
    return words_dict

def getTextFileDirs(DOCUMENT_PATH):
    # Load text files
    file_dirs = [DOCUMENT_PATH+"/"+f for f in os.listdir(DOCUMENT_PATH)  \
                if ".txt" in f]
    return file_dirs

def makeWordsDict(words, words_dict = {}):
    # Generate dictionary to store words count
    for w in words:
        words_dict[w] = 0
    return words_dict

def countDocument(file_dir):
    # Count words with given file directory
    
    # Initialize a dictionary to store counting corresponds to words
    words_dict = makeWordsDict(words).copy()
    
    # Initialize a dictionary to store time usage
    time_dict = {"Read":0, "Count":0}
    
    # Time the file reading process
    strat_read_time = timeit.default_timer()
    
    # Read file
    text_file = open(file_dir,"r")
    lines = text_file.readlines()
    text_file.close()
    
    end_read_time = timeit.default_timer()
    
    # Time the counting process
    start_count_time = timeit.default_timer()
    
    # Count words line by line
    for line in lines:
            words_dict = countWords(line.lower(), words_dict)
    end_count_time = timeit.default_timer()
    
    # Compute each time period
    time_dict["Read"] = end_read_time - strat_read_time
    time_dict["Count"] = end_count_time - start_count_time
    
    return words_dict, time_dict

def updateCountAndTime(local_count,local_time, other_count, other_time):
    for word in other_count.keys():
        local_count[word] += other_count[word]
    for time in other_time.keys():
        local_time[time] += other_time[time]
    return local_count, local_time

def countMultipleFiles(filedirs):
    # Count multiple files
    
    # Initialize words count storage
    total_words_dict = makeWordsDict(words).copy()
    total_time_dict = {"Read":0, "Count":0}
    
    for f in filedirs:
        # count words for file f
        current_count_dict, current_time_dict = countDocument(f)
        total_words_dict, total_time_dict = updateCountAndTime(total_words_dict, total_time_dict, \
                                current_count_dict, current_time_dict)

    return total_words_dict, total_time_dict
