from ... config import PROJECT_PATH

def get_stop_words(file_path = PROJECT_PATH + "portrayal/resource/stop_words.txt"):
	stop_words = set()

	file = open(file_path, "r")  
	for line in file:  
	    stop_words.add(line[0 : -1])

	file.close()  

	return stop_words