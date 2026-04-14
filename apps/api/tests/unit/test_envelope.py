from presentation.responses.envelope import ResponseEnvelope


class TestResponseEnvelope:
    """Testes para o envelope genérico de resposta da API."""

    def test_success_envelope(self):
        envelope = ResponseEnvelope(success=True, data={"key": "value"})
        assert envelope.success is True
        assert envelope.data == {"key": "value"}
        assert envelope.error is None
        assert envelope.message is None

    def test_error_envelope(self):
        envelope = ResponseEnvelope(
            success=False,
            data=None,
            error="Something went wrong",
            message="Internal server error",
        )
        assert envelope.success is False
        assert envelope.data is None
        assert envelope.error == "Something went wrong"
        assert envelope.message == "Internal server error"

    def test_data_defaults_to_none(self):
        envelope = ResponseEnvelope(success=True)
        assert envelope.data is None

    def test_error_defaults_to_none(self):
        envelope = ResponseEnvelope(success=True)
        assert envelope.error is None

    def test_message_defaults_to_none(self):
        envelope = ResponseEnvelope(success=True)
        assert envelope.message is None

    def test_generic_type_with_list(self):
        envelope = ResponseEnvelope[list](success=True, data=[1, 2, 3])
        assert envelope.data == [1, 2, 3]

    def test_generic_type_with_dict(self):
        envelope = ResponseEnvelope[dict](success=True, data={"a": 1})
        assert envelope.data == {"a": 1}

    def test_generic_type_with_string(self):
        envelope = ResponseEnvelope[str](success=True, data="hello")
        assert envelope.data == "hello"

    def test_model_dump_json_mode(self):
        envelope = ResponseEnvelope(
            success=True, data="test", message="ok"
        )
        result = envelope.model_dump(mode="json")
        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["data"] == "test"
        assert result["message"] == "ok"
        assert result["error"] is None

    def test_model_dump_contains_all_keys(self):
        envelope = ResponseEnvelope(success=False)
        result = envelope.model_dump(mode="json")
        expected_keys = {"success", "data", "error", "message"}
        assert set(result.keys()) == expected_keys

    def test_envelope_with_nested_data(self):
        nested_data = {
            "transactions": [
                {"id": 1, "amount": 100.0},
                {"id": 2, "amount": 200.0},
            ],
            "total": 300.0,
        }
        envelope = ResponseEnvelope(success=True, data=nested_data)
        assert envelope.data["total"] == 300.0
        assert len(envelope.data["transactions"]) == 2
