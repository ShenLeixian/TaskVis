from waitress import serve
# from viznet import app
from visrec.src import app

serve(app, host='0.0.0.0', port=8888)