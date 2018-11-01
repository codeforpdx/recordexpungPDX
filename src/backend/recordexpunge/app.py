from flask import Flask

from .config import app_config

def create_app(env_name):
  """
  Create app
  """

  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return '''
    recordexpungPDX
    A project to automate expunging qualifying criminal records.
    This project is done in conjunction with the Multnomah County Public Defender's Office.
    '''

  return app
