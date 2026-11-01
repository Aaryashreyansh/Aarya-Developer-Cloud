# Testing

Install dependencies and run:

```bash
pip install -r requirements.txt
pytest -q
```

The test suite covers health, provider discovery, request validation, adapter routing, and missing-key behavior. Live provider tests are intentionally excluded so CI never needs real API credentials or incurs model charges.
