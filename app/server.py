"""Rules service for the SmartHome GitOps laboratory (Python standard library)."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.getenv("PORT", "8110"))
RELEASE_MESSAGE = "rules v1"
APP_VERSION = os.getenv("APP_VERSION", "dev")


def evaluate_rules(event):
    """Decide automation actions for simple SmartHome telemetry."""
    if not isinstance(event, dict):
        raise ValueError("Expected a JSON object")
    actions = []
    temperature = event.get("temperature")
    humidity = event.get("humidity")
    motion = event.get("motion")
    if temperature is not None:
        if type(temperature) not in (int, float):
            raise ValueError("temperature must be numeric")
        if temperature >= 30:
            actions.append("enable_cooling")
        elif temperature <= 16:
            actions.append("enable_heating")
    if humidity is not None:
        if type(humidity) not in (int, float):
            raise ValueError("humidity must be numeric")
        if humidity >= 70:
            actions.append("enable_dehumidifier")
    if motion is not None:
        if not isinstance(motion, bool):
            raise ValueError("motion must be boolean")
        if motion:
            actions.append("turn_on_light")
    return {"app": "rules", "actions": actions, "triggered": bool(actions)}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = (json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
        elif self.path in ("/", "/version"):
            self.send_json(200, {"app": "rules", "message": RELEASE_MESSAGE, "version": APP_VERSION})
        elif self.path == "/rules":
            self.send_json(200, {"temperature_hot": 30, "temperature_cold": 16, "humidity_high": 70, "motion_lights": True})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/evaluate":
            return self.send_json(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                return self.send_json(400, {"error": "Content-Length must be in 1..65536"})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            answer = evaluate_rules(payload)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            return self.send_json(400, {"error": str(exc)})
        self.send_json(200, answer)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"rules service on port {PORT}, version={APP_VERSION}", flush=True)
    server.serve_forever()
