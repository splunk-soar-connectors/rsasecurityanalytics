# File: parse_incidents.py
#
# Copyright (c) 2017-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
container_common = {
    "description": "Container added by Phantom",
}

artifact_common = {
    "type": "network",
    "run_automation": False,  # Set this to false here, the app will set it to true for the correct (last) artifact
    "description": "Artifact added by Phantom",
}

cef_keys = {
    "netbios_name": "HostName",
    "port": "Port",
    "mac_address": "MacAddress",
    "ip_address": "Address",
    "groupby_destination_ip": "alertDestinations",
    "groupby_destination_port": "alertDestinationPorts",
    "groupby_source_ip": "alertSources",
    "groupby_source_port": "alertSourcePorts",
    "groupby_domain": "alertDestinationDomains",
    "timestamp": "createTime",
    "id": "alertId",
}


def _log_parse_error(base_connector, record_type, identifier, error):
    message = f"Failed to parse {record_type} '{identifier}', skipping it. Error: {error}"
    if base_connector:
        base_connector.debug_print(message)
        base_connector.save_progress(message)


def _parse_alert(alert):
    artifact = dict(artifact_common)
    cef = {}
    event_ids = []
    artifact.update(
        {
            "cef": cef,
            "label": "alert",
            "source_data_identifier": alert["id"],
            "name": f"alert - {alert['name']}",
            "cef_types": {"incidentId": ["rsa incident id"], "alertId": ["rsa alert id"]},
        }
    )
    cef["events"] = event_ids

    for key, value in alert.items():
        if key in {"related_links", "events"}:
            continue
        cef[cef_keys.get(key, key)] = value

    return artifact, event_ids


def _parse_event(alert, event, event_ids):
    artifact = dict(artifact_common)
    cef = {"alertId": alert["id"]}
    artifact.update(
        {
            "cef": cef,
            "label": "event",
            "cef_types": {"sessionId": ["netwitness session ids"], "alertId": ["rsa alert id"]},
        }
    )

    for key, value in event.items():
        if not value:
            continue

        if key in {"destination", "source"}:
            device = value.get("device") or {}
            for device_key, device_value in device.items():
                if device_key in cef_keys and device_value:
                    cef[f"{key}{cef_keys[device_key]}"] = device_value

            user = value.get("user")
            if isinstance(user, dict) and user.get("username"):
                cef[f"{key}UserName"] = user["username"]

        elif key == "related_links":
            for link in value:
                if link.get("type") == "investigate_original_event" and link.get("url"):
                    event_id = link["url"].split("/")[-1]
                    cef["sessionId"] = event_id
                    event_ids.append(event_id)
                    artifact["source_data_identifier"] = event_id
                    artifact["name"] = f"event - {event_id}"

        elif key == "data":
            data = value[0] if isinstance(value, list) and value else {}
            if data.get("filename"):
                cef["fileName"] = data["filename"]
            if data.get("size"):
                cef["fileSize"] = data["size"]
            if data.get("hash"):
                cef["fileHash"] = data["hash"]

        elif key == "domain":
            cef["destinationDnsDomain"] = value
        elif key == "timestamp":
            cef["createTime"] = value
        elif key == "device":
            cef["deviceName"] = value
            artifact["cef_types"]["deviceName"] = ["rsa sa device"]
        elif key not in {"file", "size", "detector"}:
            cef[key] = value

    return artifact


def parse_incidents(incidents, base_connector):
    results = []

    for incident in incidents:
        try:
            container = {}
            artifacts = []
            container["data"] = incident
            container["name"] = "{} - {}".format(incident["id"], incident["name"])
            container["description"] = incident["summary"]
            container["source_data_identifier"] = incident["id"]
        except Exception as error:
            identifier = incident.get("id") if isinstance(incident, dict) else incident
            _log_parse_error(base_connector, "incident", identifier, error)
            continue

        results.append({"container": container, "artifacts": artifacts})
        for alert in incident.get("alerts") or []:
            try:
                alert_artifact, event_ids = _parse_alert(alert)
            except Exception as error:
                identifier = alert.get("id") if isinstance(alert, dict) else alert
                _log_parse_error(base_connector, "alert", identifier, error)
                continue

            artifacts.append(alert_artifact)
            for event in alert.get("events") or []:
                try:
                    artifacts.append(_parse_event(alert, event, event_ids))
                except Exception as error:
                    identifier = event.get("id") if isinstance(event, dict) else event
                    _log_parse_error(base_connector, "event", identifier, error)

    return results
