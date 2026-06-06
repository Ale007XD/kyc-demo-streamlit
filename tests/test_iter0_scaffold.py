from __future__ import annotations
import kyc_demo
import kyc_demo.engine
import kyc_demo.store
import kyc_demo.components


def test_import_kyc_demo() -> None:
    assert kyc_demo is not None


def test_version() -> None:
    assert kyc_demo.VERSION == "0.0.0"


def test_submodules() -> None:
    assert kyc_demo.engine is not None
    assert kyc_demo.store is not None
    assert kyc_demo.components is not None
