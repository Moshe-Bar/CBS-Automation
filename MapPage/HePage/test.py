

# list_links=driver.find_elements_by_tag_name('a')

import threading 
import os 
  
def task1(argument): 
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name)) 
    print("ID of process running task 1: {}".format(os.getpid()))
    print(argument) 
  
def task2(argument): 
    print("Task 2 assigned to thread: {}".format(threading.current_thread().name)) 
    print("ID of process running task 2: {}".format(os.getpid())) 
    print(argument) 
  
if __name__ == "__main__": 
  
    # print ID of current process 
    print("ID of process running main program: {}".format(os.getpid())) 
  
    # print name of main thread 
    print("Main thread name: {}".format(threading.current_thread().name)) 
  
    # creating threads 
    t1 = threading.Thread(target=task1,args='hello1' ,name='t1') 
    t2 = threading.Thread(target=task2,args='hello1', name='t2')   
  
    # starting threads 
    t1.start() 
    t2.start() 
  
    # wait until all threads finish 
    t1.join() 
    t2.join() 