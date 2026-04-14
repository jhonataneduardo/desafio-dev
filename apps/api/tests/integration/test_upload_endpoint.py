import io
import pytest


class TestUploadCnabEndpoint:
    """Testes de integração para o endpoint POST /api/v1/transactions/import."""

    def test_upload_valid_cnab_returns_201(self, client, cnab_valid_file_content):
        response = client.post(
            "/api/v1/transactions/import",
            files={"file": ("cnab.txt", io.BytesIO(
                cnab_valid_file_content), "text/plain")},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["data"], list)
        assert len(body["data"]) == 2

    def test_upload_valid_cnab_returns_correct_structure(self, client, cnab_valid_file_content):
        response = client.post(
            "/api/v1/transactions/import",
            files={"file": ("cnab.txt", io.BytesIO(
                cnab_valid_file_content), "text/plain")},
        )

        body = response.json()
        transaction = body["data"][0]

        expected_fields = {
            "id", "type", "date", "card_number", "national_id",
            "hour", "store_name", "store_owner", "amount",
            "created_at", "updated_at",
        }
        assert set(transaction.keys()) == expected_fields

    def test_upload_empty_file_returns_error(self, client):
        response = client.post(
            "/api/v1/transactions/import",
            files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
        )

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False

    def test_upload_short_lines_returns_error(self, client):
        short_content = b"short line here"
        response = client.post(
            "/api/v1/transactions/import",
            files={"file": ("bad.txt", io.BytesIO(
                short_content), "text/plain")},
        )

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["error"] is not None

    def test_upload_without_file_returns_422(self, client):
        response = client.post("/api/v1/transactions/import")
        assert response.status_code == 422
