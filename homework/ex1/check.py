import subprocess
from difflib import SequenceMatcher
import time

t1 = time.time()

######################################################################################################
######################################################################################################
# Change the file name to your ID number .py !!!!!
file='204396493.py'
######################################################################################################
######################################################################################################
temp = file.split('.')
output = temp[0]
output += "-test"
print(output)
try:
    with open("output1.txt", "w+") as output:
        state = subprocess.call(["python3", file, "--task", "fibonacci", "--N", '153'], stdout=output, );
    file1 = "test/ans1.txt"
    file2 = "output1.txt"
    text1 = open(file1, 'r', encoding='utf-8', errors='ignore').read()
    text2 = open(file2, 'r', encoding='utf-8', errors='ignore').read()
    m = SequenceMatcher(None, text1, text2)
    if m.ratio() >= 1:
        print("Test Number 1: Passed")
    elif state==0:
        print("Test Number 1: Failed")
    else:
        print("Test Number 1: crashed")
except:
     print("Test Number 1: crashed")
try:
    with open("output2.txt", "w+") as output:
        state=subprocess.call(["python3", file, "--task", "pi", "--N", '56'], stdout=output, );
    file1 = "test/ans2.txt"
    file2 = "output2.txt"
    text1 = open(file1, 'r', encoding='utf-8', errors='ignore').read()
    text2 = open(file2, 'r', encoding='utf-8', errors='ignore').read()
    m = SequenceMatcher(None, text1, text2)
    if m.ratio() >= 1:
        print("Test Number 2: Passed")
    elif state == 0:
        print("Test Number 2: Failed")
    else:
        print("Test Number 2: crashed")
except:
    print("Test Number 2: crashed")
try:
    with open("output3.txt", "w+") as output:
        state=subprocess.call(["python3", file, "--task", "prime", "--N", '2'], stdout=output, );
    file1 = "test/ans3.txt"
    file2 = "output3.txt"
    text1 = open(file1, 'r', encoding='utf-8', errors='ignore').read()
    text2 = open(file2, 'r', encoding='utf-8', errors='ignore').read()
    m = SequenceMatcher(None, text1, text2)
    if m.ratio() >= 1:
        print("Test Number 3: Passed")
    elif state == 0:
        print("Test Number 3: Failed")
    else:
        print("Test Number 3: crashed")
except:
    print("Test Number 3: Your program crashed")