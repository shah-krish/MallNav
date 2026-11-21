from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import patch, sentinel

from fastapi import HTTPException, status

from app.api.v1.endpoints import auth
from app.models.user import User, UserRole
from app.schemas.user import UserLogin


class LoginUserTests(TestCase):
    def setUp(self):
        self.credentials = UserLogin(email="login-test@example.com", password="test-password")

        authenticate = patch.object(auth.user_service, "authenticate_user")
        self.authenticate_user = authenticate.start()
        self.addCleanup(authenticate.stop)

        create_token = patch.object(auth, "create_access_token", return_value="test-token")
        self.create_token = create_token.start()
        self.addCleanup(create_token.stop)

    def test_invalid_credentials_return_401_without_creating_a_token(self):
        self.authenticate_user.return_value = None

        with self.assertRaises(HTTPException) as error:
            auth.login_user(sentinel.db, self.credentials)

        self.assertEqual(error.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.create_token.assert_not_called()

    def test_visitor_with_valid_credentials_returns_403_without_creating_a_token(self):
        self.authenticate_user.return_value = self.make_user(UserRole.VISITOR)

        with self.assertRaises(HTTPException) as error:
            auth.login_user(sentinel.db, self.credentials)

        self.assertEqual(error.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.create_token.assert_not_called()

    def test_tenant_login_uses_the_saved_store_assignment(self):
        self.assert_staff_login(UserRole.TENANT, store_id="test-store")

    def test_operator_can_log_in_without_a_store_assignment(self):
        self.assert_staff_login(UserRole.OPERATOR, store_id=None)

    def make_user(self, role: UserRole, store_id: str | None = None) -> User:
        return User(
            id="test-user",
            email=self.credentials.email,
            role=role,
            store_id=store_id,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

    def assert_staff_login(self, role: UserRole, store_id: str | None):
        user = self.make_user(role, store_id)
        self.authenticate_user.return_value = user

        result = auth.login_user(sentinel.db, self.credentials)

        self.authenticate_user.assert_called_once_with(
            sentinel.db, self.credentials.email, self.credentials.password
        )
        self.create_token.assert_called_once_with(
            {"sub": user.id, "role": role.value, "store_id": store_id}
        )
        self.assertEqual(result.access_token, "test-token")
        self.assertEqual(result.token_type, "bearer")
        self.assertEqual(result.user.role, role)
        self.assertEqual(result.user.store_id, store_id)
