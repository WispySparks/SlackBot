"""Allows running commands for Doorbell from the command line without using Slack."""

import json

from doorbell import Doorbell


def fake_response(text: str) -> dict:
    """Creates a fake payload for testing Doorbell."""
    return {"event": {"channel": "None", "text": f"@Doorbell {text}", "user": "U05UFPWSEJH"}}


doorbell = Doorbell(False)
print("Started Doorbell!")
print(json.dumps(doorbell.app.client.auth_test().data, indent=4))
try:
    while not doorbell.closed:
        cmd = input("Command: ")
        doorbell.mention_event(fake_response(cmd), print)  # type: ignore
except KeyboardInterrupt:
    doorbell.close()
print("Exited Doorbell.")
