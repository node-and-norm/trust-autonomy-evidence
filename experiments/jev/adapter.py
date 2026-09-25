"""Optional TypeSafe boundary. Importing this module never imports the SDK."""
from __future__ import annotations

import json
import math
import os
from importlib.metadata import version

SDK_VERSION = '0.7.1'
DEFAULT_MODEL = 'jev-1.13.0'
LABELS = ('supported', 'partially_supported', 'unsupported', 'indeterminate', 'outside_scope')


def validate_response(raw: bytes, question_ids: set[str]) -> dict:
    """Fail closed on incomplete, nonfinite, or incompatible choice responses."""
    def reject_constant(value):
        raise ValueError('nonfinite JSON number')
    doc = json.loads(raw, parse_constant=reject_constant)
    if not isinstance(doc, dict) or not isinstance(doc.get('model'), str) or not doc['model'].strip():
        raise ValueError('missing resolved model')
    answers = doc.get('answers')
    if not isinstance(answers, dict) or set(answers) != question_ids:
        raise ValueError('answer identifiers differ from request')
    for answer in answers.values():
        if not isinstance(answer, dict) or answer.get('type') != 'choice' or answer.get('choice') not in LABELS:
            raise ValueError('invalid choice')
        probs = answer.get('probabilities')
        if not isinstance(probs, dict) or set(probs) != set(LABELS):
            raise ValueError('probability labels differ from criteria')
        for value in [answer.get('confidence'), *probs.values()]:
            if type(value) not in (float, int) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError('invalid probability or confidence')
        if not math.isclose(sum(probs.values()), 1.0, abs_tol=1e-5):
            raise ValueError('probabilities do not sum to one')
        if probs[answer['choice']] < max(probs.values()):
            raise ValueError('choice is not a maximum probability label')
    return doc


class JevAdapter:
    """A single SDK attempt per case, bounded timeout, official endpoint only."""
    def __init__(self, *, transport=None):
        key = os.environ.get('TYPESAFE_API_KEY', '').strip()
        if not key:
            raise RuntimeError('missing TYPESAFE_API_KEY')
        if version('typesafe-sdk') != SDK_VERSION:
            raise RuntimeError('install experiments/jev/requirements-live.txt')
        from typesafe_sdk import TypeSafeClient, RetryPolicy
        self.sdk_version = version('typesafe-sdk')
        import httpx2
        self.last_raw = None
        self.last_http_status = None
        self.last_request_id = None
        def capture(response):
            self.last_raw = response.read()
            self.last_http_status = response.status_code
            self.last_request_id = response.headers.get('x-typesafe-request-id')
        http_client = httpx2.Client(transport=transport, timeout=30.0,
                                   event_hooks={'response': [capture]})
        self.client = TypeSafeClient(api_key=key, base_url='https://api.typesafe.ai',
                                     timeout=30.0, retry=RetryPolicy(max_retries=0), http_client=http_client)

    def evaluate(self, state: dict, questions: dict, model: str) -> bytes:
        self.last_raw = self.last_http_status = self.last_request_id = None
        result = self.client.system_one(state=state, questions=questions, model=model)
        return result.raw_http_response.content

    def close(self):
        self.client.close()


class MockAdapter:
    """Deliberately uninformative plumbing fixture; never reads the oracle."""
    sdk_version = None

    def evaluate(self, state: dict, questions: dict, model: str) -> bytes:
        return json.dumps({'model': 'mock-only', 'usage': {}, 'answers': {
            q: {'type': 'choice', 'choice': 'indeterminate', 'confidence': 0.0,
                'probabilities': {label: 0.2 for label in LABELS}} for q in questions
        }}, sort_keys=True).encode()

    def close(self):
        pass
