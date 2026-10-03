"""Optional pinned SDK boundary; imports remain credential-free."""
import json
import os
from importlib.metadata import version

from experiments.jev.adapter import SDK_VERSION


class Transport:
    def __init__(self, *, transport=None):
        key = os.environ.get('TYPESAFE_API_KEY', '').strip()
        if not key:
            raise RuntimeError('TYPESAFE_API_KEY is not configured')
        if version('typesafe-sdk') != SDK_VERSION:
            raise RuntimeError('Install experiments/jev/requirements-live.txt')
        from typesafe_sdk import TypeSafeClient, RetryPolicy
        import httpx2
        self.sdk_version = SDK_VERSION
        self.expected = None
        self.on_send = None
        self.reset()

        def before(request):
            allowed = ('GET', 'https://api.typesafe.ai/v1/models') if self.expected is None else (
                'POST', 'https://api.typesafe.ai/v1/systemone')
            if (request.method, str(request.url)) != allowed:
                raise ValueError('Unexpected request destination')
            if self.expected is not None:
                if json.loads(request.content) != self.expected:
                    raise ValueError('SDK changed frozen request content')
                # Record actual SDK body before dispatch, never authorization headers.
                if self.on_send:
                    self.on_send(request.content)

        def after(response):
            self.last_http_status = response.status_code
            self.last_request_id = response.headers.get('x-typesafe-request-id')
            self.last_raw = response.read()

        http = httpx2.Client(transport=transport, timeout=30.0, trust_env=False,
                            follow_redirects=False,
                            event_hooks={'request': [before], 'response': [after]})
        self.client = TypeSafeClient(api_key=key, base_url='https://api.typesafe.ai',
                                    timeout=30.0, retry=RetryPolicy(max_retries=0), http_client=http)

    def reset(self):
        self.last_raw = self.last_http_status = self.last_request_id = None

    def evaluate(self, payload, on_send):
        self.reset()
        self.expected, self.on_send = payload, on_send
        return self.client.system_one(**payload).raw_http_response.content

    def preflight(self):
        self.reset()
        self.expected = self.on_send = None
        result = self.client.models.list()
        return [model.name for model in result.models]

    def close(self):
        self.client.close()
