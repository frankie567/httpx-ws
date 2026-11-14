# Changelog

Add user-facing changes under Unreleased using [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
categories. Earlier release notes are available in [GitHub Releases](https://github.com/frankie567/httpx-ws/releases).

## [Unreleased]

## [0.10.0] - 2026-11-14

### Changed

- Require Python 3.11 or later and support Python 3.15.
- Require AnyIO 4.10 or later for `AsyncWebSocketSession` ([#145](https://github.com/frankie567/httpx-ws/issues/145)).
- Raise `TimeoutError` instead of `queue.Empty` when a synchronous receive times out ([#139](https://github.com/frankie567/httpx-ws/pull/139)).

### Fixed

- Return `bytes` consistently from synchronous and asynchronous `receive_bytes()`.
- Enforce the configured limit on incoming WebSocket message size (Backported from [httpx2#1085](https://github.com/pydantic/httpx2/pull/1085)).
- Unblock synchronous WebSocket shutdown when the receive queue is full (Backported from [httpx2#1123](https://github.com/pydantic/httpx2/pull/1123)).
- Stop synchronous keepalive during WebSocket shutdown (Backported from [httpx2#1228](https://github.com/pydantic/httpx2/pull/1228), regression test from [httpx2#1229](https://github.com/pydantic/httpx2/pull/1229)).
- Ignore unsolicited and duplicate WebSocket pongs (Backported from [httpx2#1122](https://github.com/pydantic/httpx2/pull/1122)).
- Translate ASGI WebSocket read errors during shutdown (Backported from [httpx2#1233](https://github.com/pydantic/httpx2/pull/1233)).

## [0.9.0] - 2026-03-28

### Changed

- Exceptions propagating out of the async WebSocket context are wrapped in an `ExceptionGroup`.

### Fixed

- Avoid hanging on async WebSocket context exit when an AnyIO task is cancelled.
- Close AnyIO queues when the ASGI transport exits.

[Unreleased]: https://github.com/frankie567/httpx-ws/compare/v0.10.0...HEAD
[0.10.0]: https://github.com/frankie567/httpx-ws/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/frankie567/httpx-ws/releases/tag/v0.9.0
