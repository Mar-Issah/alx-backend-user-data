#!/usr/bin/env python3
""" Module to manage the API authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
         Validates whether an endpoint requires authentication.

        Parameters:
        - path (str): The path of the endpoint to be checked for auth req.
        - excluded_paths (List[str]): List of paths  excl from auth checks

        Returns:
        - bool: True if auth is req for the given path, False otherwise.

        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if len(path) == 0:
            return True

        slash_path = True if path[len(path) - 1] == '/' else False

        temp_path = path
        if not slash_path:
            temp_path += '/'

        for exc in excluded_paths:
            len_exc = len(exc)
            if len_exc == 0:
                continue

            if exc[len_exc - 1] != '*':
                if temp_path == exc:
                    return False
            else:
                if exc[:-1] == path[:len_exc - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method that validate all requests to secure the API """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates current user """
        return None
