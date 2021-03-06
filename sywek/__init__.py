from flask import Flask, redirect, send_file, url_for, session, jsonify, request, g, render_template, send_from_directory
from flask_session import Session
from .db import close_db
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .controller import GCStorageController
import os


def Create_app(test_config=None, renew_database=False):

    def _registerBP(flaskApp):
        from .blueprint.api_bp import bp as apiBP
        flaskApp.register_blueprint(apiBP, url_prefix='/api')

    app = Flask(__name__, instance_relative_config=True, static_folder="./dist",
                template_folder="./dist")

    # append flask cors

    # load ../config.py
    app.config.from_object('config')
    if test_config is None:
        # Loading instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Loding test config.
        app.config.from_mapping(test_config)

    if app.env == 'development':
        cors = CORS(app, resources={
            r"/*": {"origins": "*"}}, supports_credentials=True)

    # Ensure dic are exists
    try:
        os.makedirs(app.instance_path)
    except:
        pass

    @app.route('/')
    def routes_index():
        return render_template("index.html")
        #return redirect(url_for('blog.routes_blogIndex')) #this was not good  redirect 3 times.#################

    @app.route('/<path:path>')
    def routes_jsFile(path):
        return send_from_directory('./dist/', path)

    @app.route('/image/<path:path>')
    def routs_image(path):

        _flag, _blobInfo = GCStorageController.downloadBlob(
            'sywek_net_bucket', 'image/{}'.format(path))
        if _flag:
            return send_file(_blobInfo['data'], mimetype=_blobInfo['contentType'])

        return None

    _registerBP(app)

    import sywek.db as sywekDb
    sywekDb.init_app(app)
    sywekDb.init_db(app)

    session = Session(app)

    # session.app.session_interface.db.drop_all()
    # session.app.session_interface.db.create_all()

    @app.teardown_request
    def teardown_app_request(e=None):
        close_db()

    @app.errorhandler(Exception)
    def flask_errorhandler(e):
        return 'error!!!'

    return app
