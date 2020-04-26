from flask import Flask
import threading
import subprocess
import multiprocessing
import signal

'''
Assumptions : 
1)A, B, C are the known users and are stored in a quota dictionary
2)In case of parallel requests, timestamp information is tagged in the incoming object and a helper class has got the user_id uniquely into this  code is assumed

Drawbacks:
1)Have implemented only the decrement mode for quota and it doesnt get reset when a connection is closed (these require functions for handling each case, in class hierarchy)
2)Maintaining parallelism helper class is intended  for getting thread info per user session

Usage : 
>python3 rate_limiting.py
>open the browser window at http://localhost:5000/ 
>Input username as A,B or C in terminal and webpage shows the number of connections granted and the quota remaining for this user
Refresh the page to enter uname again and see that counter decreases 
'''

lock_user_quota = threading.Lock() #Lock that  holds quota for each user and is accessed only with this
user_quota_dict = {'A' : 200,  'B' : 200, 'C' : 200}
allowed_value = 0

'''
#Class design:

Class parallel_helper(object):
	def __init__(self, call_object_authorized, session_id):
		self.called_user_id = call_object_authorized + session_id + timestamp
	def runUserThread:
		app.run(self.called_user_id) 

Class quota_set_reset(object):
	def identifyOpeningConnection(action):
		increment counter and open connection if possible, else prompt out
	def identifyClosingConnection(action):
		Decrement quota and close connection

@app.route("/")
def function_that_app_does(user_id):
	connection_set_or_reset = quota_set_reset(user_id)
	return connection_set_or_reset
		
'''

#Use Flask to start webpage, python3 <filename.py> will satrt, then we input the user info now, get it from webpage itself using Flask input method and decrement  the quota ?
app = Flask(__name__)


@app.route("/")
def quota_allowance_code():
	user_id = input("Enter uname (allowed are A, B, C)   ")
	print("Uname {0}".format(user_id))
	if user_id in user_quota_dict:
		print("You are known")
		allowed_value = user_quota_dict[user_id]
		with lock_user_quota : # Use global lock on user_quota_dict to make it thread safe
			if user_quota_dict[user_id] <= 0:
				return("You are not allowed any more connections and have been given {0} connections".format(allowed_value))
			user_quota_dict[user_id] -= 1
		return "You are allowed 1 connections and have {0} more ".format(user_quota_dict[user_id])
	else:
		return "Sorry, wrong user"
	

if __name__ == "__main__":
    app.run()
    #call_object_authorized, session_id = get_from_webpage
    #parallel_thread_obj = parallel_helper(call_object_authorized, session_id)
    #thread.start_new_thread(parallel_thread_obj.runUserThread(), ())
    
