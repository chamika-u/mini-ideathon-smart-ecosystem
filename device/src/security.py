from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceCredential:
    device_id: str
    secret: str
    revoked: bool = False


class CredentialStore:
    def __init__(self, credentials: list[DeviceCredential]):
        self._credentials = {item.device_id: item for item in credentials}

    def authenticate(self, device_id: str, secret: str) -> bool:
        credential = self._credentials.get(device_id)
        return bool(credential and not credential.revoked and credential.secret == secret)


class ServerCertificateValidator:
    def __init__(self, trusted_fingerprint: str):
        self.trusted_fingerprint = trusted_fingerprint

    def validate(self, fingerprint: str) -> bool:
        return fingerprint == self.trusted_fingerprint
