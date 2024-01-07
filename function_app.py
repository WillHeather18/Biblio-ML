import azure.functions as func
import json
import subprocess

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ML")
def ML(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse input data from HTTP request
        ratings = req.params.get('ratings')
        num_recommendations = req.params.get('num')
        if not ratings or not num_recommendations:
            req_body = req.get_json()
            ratings = req_body.get('ratings', ratings)
            num_recommendations = req_body.get('num', num_recommendations)

        # Convert input to JSON string
        python_file = "Hybrid.py"

        result = subprocess.run(["python", python_file, ratings, num_recommendations], capture_output=True, text=True)
        if result.returncode != 0:
            return func.HttpResponse(result.stderr, status_code=400)

        # Return the recommendations as a JSON response
        return func.HttpResponse(result.stdout, status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)