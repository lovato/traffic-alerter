# -*- encoding: utf-8 -*-

"""Run the server in development mode."""

#for Flask
#from traffic_alerter.server import app
#app.run(host='0.0.0.0', debug=True)

from traffic_alerter import app
app.main()
