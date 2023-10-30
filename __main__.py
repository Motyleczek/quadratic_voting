from .website import Website    # this will work because of flutter bullshit, im sure
from .website.views import views

# TODO is this needed
# from .sql_queries_module.sql_queries import sql_queries

from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == '__main__':
    website = Website()
    website.app.register_blueprint(views, url_prefix='/')
    
    # TODO is this needed
    # website.app.register_blueprint(sql_queries, url_prefix='/')

    website.app.run(host="0.0.0.0", debug=(
        os.environ["APP_DEBUG"]).lower() == "true", port=int(os.environ["APP_PORT"]))