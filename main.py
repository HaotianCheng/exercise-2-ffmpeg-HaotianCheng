import queue
import subprocess
import threading
import os

inputQueue = queue.Queue()

completePool = []
currentDirectory = os.getcwd()
inputDirectoryPath = currentDirectory + "\\InputVideos"
for filename in os.listdir(inputDirectoryPath):
    file_720_2Mbps_30fps = (filename, "hd720", "2M", "30")
    file_480_1Mbps_30fps = (filename, "hd480", "1M", "30")
    inputQueue.put(file_720_2Mbps_30fps)
    inputQueue.put(file_480_1Mbps_30fps)

def generateName(filelist):
    name = filelist[0][:-4]
    for i in filelist[1:]:
        name += "_"
        name += i  
    return name

def processVideo():
    while not inputQueue.empty():
        file = inputQueue.get()
        filename = file[0]
        filePath = "InputVideos\\" + filename
        outputFilePath = "OutputVideos\\" + generateName(file) + ".mp4"
        threadName = threading.currentThread().getName()
        print("Processing: " + str(file) + " on " + threadName + "\n")
        subprocess.call("ffmpeg -i " + filePath + " -c:a copy -s " + file[1] + " -b:v " + file[2] + " -r " + file[3] + " " + outputFilePath, shell=True)
        # time.sleep(10)
        print( str(file) + " complete\n")
        completePool.append(file)

    print(threadName + " done\n")

threadOne = threading.Thread(name = "One", target = processVideo)
threadTwo = threading.Thread(name = "Two", target = processVideo)
threadThree = threading.Thread(name = "Three", target = processVideo)

threadOne.start()
threadTwo.start()
threadThree.start()
