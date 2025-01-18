# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
@app.route('/')
def hello():
	count = 21
	return f"""<html>
	           <h1>Hello James!</h1>
	           <p>My favorite number is {count}.</p>
	           </html>
	        """