import os
import requests

def process(app, request, func, next_url="http://localhost:" + str(os.getenv("SWITCHBOARD_PORT")) + "/sink_to"):
    reply = "no_reply"

    if request.args.get("m") and request.args.get("listener_id"):
        listener_id = request.args.get("listener_id")

        reply = func(request.args.get("m"))
        args = request.args.copy()
        args["m"] = reply

        app.logger.debug("will pass output " + reply + " to " + next_url)

        # FIXME: hacky way to not wait on reply
        try:
            requests.get(
                next_url, params=args, timeout=0.0000000001,
            )
        except requests.exceptions.ReadTimeout:
            pass

    return reply
