from ..reproschema_protocol import reproschema_protocol
import pytest


def test_reproschema_protocol():
    protocol = reproschema_protocol()
    schema = {
        "@context": "https://raw.githubusercontent.com/ReproNim/reproschema/"
        + "1.0.0-rc1"
        + "contexts/generic",
        "@type": "reproschema:Protocol",
        "schemaVersion": "1.0.0-rc1",
        "version": "0.0.1",
        "ui": {"allow": [], "shuffle": [], "order": [], "addProperties": []},
    }
    assert protocol.schema is schema
