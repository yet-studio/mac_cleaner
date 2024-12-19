"""Tests for data protection mechanisms."""

import pytest

from src.infrastructure.security.data_protection_mechanisms import (
    DataProtectionMechanisms,
)


def test_data_protection_init():
    """Test data protection initialization."""
    protection = DataProtectionMechanisms()
    assert protection is not None
    assert protection.key is not None


def test_encryption():
    """Test data encryption."""
    protection = DataProtectionMechanisms()
    test_data = "Test data"
    encrypted = protection.encrypt_data(test_data)
    assert encrypted != test_data.encode()


def test_decryption():
    """Test data decryption."""
    protection = DataProtectionMechanisms()
    test_data = "Test data"
    encrypted = protection.encrypt_data(test_data)
    decrypted = protection.decrypt_data(encrypted)
    assert decrypted == test_data
