**Unreleased**

* Prevents malformed RSA Security Analytics incident timestamps from stalling scheduled ingestion.
* Validates and labels file hashes before adding them to ingested event artifacts.
* Prevents stored credentials from being sent after the RSA Security Analytics server origin changes.
* Returns a clear error when RSA Security Analytics does not provide a valid device list.
* Adds finite timeouts to outbound RSA Security Analytics requests.
* Returns a clear error when RSA Security Analytics responds with a non-object JSON value.
