#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `poku` package."""

from unittest.mock import Mock, patch
import pytest


from poku import poku
import requests
import configargparse


def test_parse_consumer():
    """ Test that a consumer argument is handled and received """
    args = poku.parse_args(['--consumer', 'abc'])
    assert args.consumer == 'abc'


def test_no_consumer():
    """ Test that missing out the consumer argument causes a system exit """
    with pytest.raises(SystemExit):
        args = poku.parse_args([])


@patch('poku.poku.requests.get')
def test_get_request_token(mock_get):
    """ Test if successful token requests return expected token """
    mock_get.return_value.ok = True
    mock_get.return_value.json = lambda: {'code': 'b'}

    token = poku.get_response_token('abc')
    assert token == 'b'


@patch('poku.poku.requests.get')
def test_get_request_token_not_ok(mock_get):
    """ Test that unsuccessful token requests return None """
    mock_get.return_value.ok = False

    token = poku.get_response_token('abc')
    assert token is None


def test_generate_auth_url():
    token = 'hello'
    expected_url = ('https://getpocket.com/auth/authorize'
                    '?request_token={0}'
                    '&redirect_uri=https://getpocket.com').format(token)

    url = poku.generate_auth_url(token)
    assert url == expected_url
