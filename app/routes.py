import logging

import flask
from flask import Response
from flask.views import MethodView

from app.service.resources.aggregate import AggregateResources


class UserAPI(MethodView):

    def get(self, user):
        if user is None:
            # return a list of users
            return Response('No user defined', status=404)
        else:
            # expose a single user
            # Create an instance of the AggregateResources with the user
            git_resource = AggregateResources(user)

            # Call the process_resources() before the aggregate_results(), this method does all the work processes
            git_resource.process_resources()
            # Create a response with aggregate data and display errors if available. Errors are null if not available
            res = {
                'aggregate_data': git_resource.aggregate_results(),
                'errors': git_resource.get_resource_errors()
            }
            return flask.jsonify(res)

    # def post(self):
    #     # create a new user
    #     pass
    #
    # def delete(self, user_id):
    #     # delete a single user
    #     pass
    #
    # def put(self, user_id):
    #     # update a single user
    #     pass

# Create Application Factory
def create_app(import_name):
    app = flask.Flask(import_name)
    user_view = UserAPI.as_view('user_api')
    app.add_url_rule('/users/', defaults={'user': None},
                     view_func=user_view, methods=['GET', ])
    # app.add_url_rule('/users/', view_func=user_view, methods=['POST', ])
    app.add_url_rule('/users/<user>', view_func=user_view,
                     methods=['GET'])
    return app


app = create_app("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)
