#!/usr/bin/env python3
"""
Phiên bản đơn giản của conftest để debug
"""
import pytest

@pytest.fixture
def simple_fixture():
    """Simple fixture for debugging"""
    return "test value"
