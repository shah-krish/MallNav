import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services import store_service


STORES = "/api/v1/stores/"
STORE_A = {
    "id": "store-a",
    "name": "Store A",
    "category": "Dining",
    "zone": "A",
    "coordinates": [1, 2],
}
STORE_B = {**STORE_A, "id": "store-b", "name": "Store B"}
UPDATE = {"name": "Updated name"}


class StorePermissionsTests(IsolatedAsyncioTestCase):
    def setUp(self):
        self.db = Mock(spec=Session)
        self.app = FastAPI()
        self.app.include_router(api_router, prefix="/api/v1")
        self.app.dependency_overrides[get_db] = lambda: self.db

        config = patch.multiple(
            settings,
            JWT_SECRET="local-test-signing-key-for-store-permissions",
            JWT_ALGORITHM="HS256",
            ACCESS_TOKEN_EXPIRE_MINUTES=30,
        )
        config.start()
        self.addCleanup(config.stop)

        services = patch.multiple(
            store_service,
            get_stores=Mock(return_value=[STORE_A, STORE_B]),
            get_store_by_id=Mock(side_effect=lambda db, store_id: {
                "store-a": STORE_A,
                "store-b": STORE_B,
            }.get(store_id)),
            create_store=Mock(return_value=STORE_A),
            update_store=Mock(return_value={**STORE_A, **UPDATE}),
            delete_store=Mock(return_value=None),
        )
        services.start()
        self.addCleanup(services.stop)

    async def test_anonymous_shoppers_can_list_and_read_stores(self):
        self.assertEqual(await self.request("GET", STORES), 200)
        self.assertEqual(await self.request("GET", STORES + "store-a"), 200)

    async def test_anonymous_writes_return_401(self):
        await self.assert_write_statuses((401, 401, 401))
        self.assert_no_store_writes()

    async def test_invalid_and_expired_tokens_return_401(self):
        self.account(UserRole.OPERATOR)
        with patch.object(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", -1):
            expired = create_access_token({"sub": "staff-user", "role": "OPERATOR"})

        for case, token in (("invalid", "invalid-token"), ("expired", expired)):
            with self.subTest(token=case):
                self.assertEqual(await self.request("PATCH", STORES + "store-a", UPDATE, token), 401)

        self.assert_no_store_writes()

    async def test_token_for_a_missing_account_returns_401(self):
        self.db.execute.return_value.scalar_one_or_none.return_value = None
        token = create_access_token({"sub": "staff-user", "role": "OPERATOR"})

        self.assertEqual(await self.request("PATCH", STORES + "store-a", UPDATE, token), 401)
        self.assert_no_store_writes()

    async def test_tenant_cannot_write_directly_even_for_their_assigned_store(self):
        token = self.account(UserRole.TENANT, store_id="store-a")

        await self.assert_write_statuses((403, 403, 403), token)
        self.assertEqual(await self.request("PATCH", STORES + "store-b", UPDATE, token), 403)
        self.assert_no_store_writes()

    async def test_current_role_overrides_the_role_in_an_older_token(self):
        token = self.account(UserRole.OPERATOR)
        self.account(UserRole.TENANT, store_id="store-a")

        self.assertEqual(await self.request("PATCH", STORES + "store-a", UPDATE, token), 403)
        self.assert_no_store_writes()

    async def test_operator_can_create_update_and_delete(self):
        token = self.account(UserRole.OPERATOR)

        await self.assert_write_statuses((201, 200, 204), token)
        store_service.create_store.assert_called_once()
        store_service.update_store.assert_called_once()
        store_service.delete_store.assert_called_once()

    def account(self, role, store_id=None):
        user = User(id="staff-user", role=role, store_id=store_id)
        self.db.execute.return_value.scalar_one_or_none.return_value = user
        return create_access_token({"sub": user.id, "role": role.value, "store_id": store_id})

    def assert_no_store_writes(self):
        store_service.create_store.assert_not_called()
        store_service.update_store.assert_not_called()
        store_service.delete_store.assert_not_called()

    async def assert_write_statuses(self, statuses, token=None):
        writes = (
            ("POST", STORES, STORE_A),
            ("PATCH", STORES + "store-a", UPDATE),
            ("DELETE", STORES + "store-a", None),
        )
        for (method, path, body), expected in zip(writes, statuses):
            with self.subTest(method=method):
                self.assertEqual(await self.request(method, path, body, token), expected)

    async def request(self, method, path, body=None, token=None):
        # Send the app a request in memory, without a server or HTTP test dependency.
        headers = []
        if body is not None:
            headers.append((b"content-type", b"application/json"))
        if token is not None:
            headers.append((b"authorization", f"Bearer {token}".encode()))
        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "headers": headers,
            "query_string": b"",
        }
        messages = []

        async def receive():
            return {"type": "http.request", "body": json.dumps(body).encode() if body is not None else b""}

        async def send(message):
            messages.append(message)

        await self.app(scope, receive, send)
        return next(message["status"] for message in messages if message["type"] == "http.response.start")
