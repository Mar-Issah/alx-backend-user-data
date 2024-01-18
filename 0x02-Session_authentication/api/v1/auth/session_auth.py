#!/usr/bin/env python3
""" Module of Session Auth"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Session Authentication Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user ID.

        Parameters:
        - user_id (str): User ID for which the session ID is created.

        Returns:
        - str: The generated session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user ID based on a session ID.

        Parameters:
        - session_id (str): Session ID for which the user ID is retrieved.

        Returns:
        - str: The user ID associated with the given session ID."""

        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a session cookie value.

        Parameters:
        - request: Optional request object.

        Returns:
        - User: Instance of User class based on the session cookie.
        """

        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session, logging the user out.

        Parameters:
        - request: Optional request object.

        Returns:
        - bool: True if the session was successfully destroyed,
          False otherwise.
        """

        if request is None:
            return False

        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False

        user_id = self.user_id_for_session_id(sess_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[sess_id]
        except Exception:
            pass

        return True
