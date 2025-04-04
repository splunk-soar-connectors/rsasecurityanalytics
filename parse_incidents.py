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


def parse_incidents(incidents, base_connector):
    results = []

    for incident in incidents:
        try:
            container = {}
            artifacts = []
            results.append({"container": container, "artifacts": artifacts})

            container["data"] = incident
            container["name"] = "{} - {}".format(incident["id"], incident["name"])
            container["description"] = incident["summary"]
            container["source_data_identifier"] = incident["id"]

            for alert in incident["alerts"]:
                artifact = {}
                artifacts.append(artifact)
                artifact.update(artifact_common)

                cef = {}
                event_id_list = []
                artifact["cef"] = cef
                artifact["label"] = "alert"
                cef["events"] = event_id_list
                artifact["source_data_identifier"] = alert["id"]
                artifact["name"] = "alert - {}".format(alert["name"])
                artifact["cef_types"] = {"incidentId": ["rsa incident id"], "alertId": ["rsa alert id"]}

                for key in alert:
                    if key == "related_links":
                        continue

                    elif key == "events":
                        continue

                    elif key in cef_keys:
                        cef[cef_keys[key]] = alert[key]
                        continue

                    cef[key] = alert[key]

                for event in alert["events"]:
                    artifact = {}
                    artifacts.append(artifact)
                    artifact.update(artifact_common)

                    cef = {}
                    artifact["cef"] = cef
                    artifact["label"] = "event"
                    cef["alertId"] = alert["id"]
                    artifact["cef_types"] = {"sessionId": ["netwitness session ids"], "alertId": ["rsa alert id"]}

                    for key in event:
                        if not event[key]:
                            continue

                        if key == "destination" or key == "source":
                            device = event[key]["device"]
                            for d_key in device:
                                if d_key in cef_keys and device[d_key]:
                                    cef[f"{key}{cef_keys[d_key]}"] = device[d_key]

                            if event[key]["user"]:
                                cef[f"{key}UserName"] = event[key]["user"]["username"]

                        elif key == "related_links":
                            for link in event[key]:
                                if link["type"] == "investigate_original_event":
                                    event_id = link["url"].split("/")[-1]
                                    cef["sessionId"] = event_id
                                    event_id_list.append(event_id)
                                    artifact["source_data_identifier"] = event_id
                                    artifact["name"] = f"event - {event_id}"

                        elif key == "data":
                            if event[key][0]["filename"]:
                                cef["fileName"] = event[key][0]["filename"]
                            if event[key][0]["size"]:
                                cef["fileSize"] = event[key][0]["size"]
                            if event[key][0]["hash"]:
                                cef["fileHash"] = event[key][0]["hash"]

                        elif key == "domain":
                            cef["destinationDnsDomain"] = event[key]

                        elif key == "timestamp":
                            cef["createTime"] = event[key]

                        elif key == "device":
                            cef["deviceName"] = event[key]
                            artifact["cef_types"]["deviceName"] = ["rsa sa device"]

                        elif key == "file" or key == "size":
                            pass

                        elif key == "detector":
                            pass

                        else:
                            cef[key] = event[key]

        except:
            pass

    return results
