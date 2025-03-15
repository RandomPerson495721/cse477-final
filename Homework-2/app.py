import os
import sys

from flask_app import create_app
#TODO: REMOVE ME!
# import pydevd_pycharm
app = create_app()
#
# # Start the debugger if in development mode
# if os.environ.get('FLASK_ENV') == 'development':
#     pydevd_pycharm.settrace('host.docker.internal', port=5678, stdoutToServer = True, stderrToServer = True)
#
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), use_reloader=True)