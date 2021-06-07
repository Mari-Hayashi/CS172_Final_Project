import time

GLOBAL_START = time.time()
class TimeHandler:

    # static variables
    count_id = 1
    default_id = f"TimeHandler Object" 


    def __init__(self, name=None, verbose=False):
        if not name: 
            self.name = f"{TimeHandler.default_id} #{TimeHandler.count_id}"
            TimeHandler.count_id += 1
        else:
            self.name = f"{name}"
        self.verbose = verbose
        self.start_time = None
        self.end_time = None



    def set_name(self, name):
        self.name = f"{name}"
        


    def start(self, desc=None):
        
        # define prompt
        self.start_time = time.time()
        default_start_prompt = f"{self.name:30} {'start':50} {'GLOBAL_TIME:':15} {self.start_time - GLOBAL_START:.2f} seconds" 

        # record times
        if self.verbose and not desc:
            print(f"{default_start_prompt}")
        elif self.verbose and desc:
            print(f"{self.name:30} {desc:50} {'GLOBAL_TIME:':15} {self.start_time - GLOBAL_START:.2f} seconds")



    def end(self, desc=None):

        # define prompts
        self.end_time = time.time()
        default_end_prompt1 = f"{self.name:30} {'end':50} {'GLOBAL_TIME:':15} {self.end_time - GLOBAL_START:.2f} {'seconds':20} {'ELAPSED:':10} {self.end_time - self.start_time:.2f} seconds"

        # record times
        if self.verbose and not desc:
            print(f"{default_end_prompt1}")
        elif self.verbose and desc:
            print(f"{self.name:30} {desc:50} {'GLOBAL_TIME:':15} {self.end_time - GLOBAL_START:.2f} {'seconds':20} {'ELAPSED:':10} {self.end_time - self.start_time:.2f} seconds")



