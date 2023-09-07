# HTTPX WS

<p align="center">
    <em>WebSockets support for HTTPX</em>
</p>

[![build](https://github.com/frankie567/httpx-ws/workflows/Build/badge.svg)](https://github.com/frankie567/httpx-ws/actions)
[![codecov](https://codecov.io/gh/frankie567/httpx-ws/branch/main/graph/badge.svg?token=fL49kIvrj6)](https://codecov.io/gh/frankie567/httpx-ws)
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
[![PyPI version](https://badge.fury.io/py/httpx-ws.svg)](https://badge.fury.io/py/httpx-ws)
[![Downloads](https://pepy.tech/badge/httpx-ws)](https://pepy.tech/project/httpx-ws)

<p align="center">
<a href="https://github.com/sponsors/frankie567"><img src="https://md-buttons.francoisvoron.com/button.svg?text=Buy%20me%20a%20coffee%20%E2%98%95%EF%B8%8F&bg=ef4444&w=200&h=50"></a>
</p>

---

**Documentation**: <a href="https://frankie567.github.io/httpx-ws/" target="_blank">https://frankie567.github.io/httpx-ws/</a>

**Source Code**: <a href="https://github.com/frankie567/httpx-ws" target="_blank">https://github.com/frankie567/httpx-ws</a>

---

## Installation

> **Warning**
>
> This is a very young project. Expect bugs 🐛

```bash
pip install httpx-ws
```

## Features

* [X] Sync and async client
* [X] Helper methods to send text, binary and JSON data
* [X] Helper methods to receive text, binary and JSON data
* [X] Automatic ping/pong answers
* [X] HTTPX transport to test WebSockets defined in ASGI apps
* [X] Automatic keepalive ping

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://francoisvoron.com"><img src="https://avatars.githubusercontent.com/u/1144727?v=4?s=100" width="100px;" alt="François Voron"/><br /><sub><b>François Voron</b></sub></a><br /><a href="#maintenance-frankie567" title="Maintenance">🚧</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=frankie567" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://kousikmitra.github.io"><img src="https://avatars.githubusercontent.com/u/15109533?v=4?s=100" width="100px;" alt="Kousik Mitra"/><br /><sub><b>Kousik Mitra</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/commits?author=kousikmitra" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/davidbrochart"><img src="https://avatars.githubusercontent.com/u/4711805?v=4?s=100" width="100px;" alt="David Brochart"/><br /><sub><b>David Brochart</b></sub></a><br /><a href="#platform-davidbrochart" title="Packaging/porting to new platform">📦</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ysmu"><img src="https://avatars.githubusercontent.com/u/17018576?v=4?s=100" width="100px;" alt="ysmu"/><br /><sub><b>ysmu</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Aysmu" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://samforeman.me"><img src="https://avatars.githubusercontent.com/u/5234251?v=4?s=100" width="100px;" alt="Sam Foreman"/><br /><sub><b>Sam Foreman</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Asaforem2" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://maparent.ca/"><img src="https://avatars.githubusercontent.com/u/202691?v=4?s=100" width="100px;" alt="Marc-Antoine Parent"/><br /><sub><b>Marc-Antoine Parent</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Amaparent" title="Bug reports">🐛</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=maparent" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Development

### Setup environment

We use [Hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build. Ensure it's installed on your system.

### Run unit tests

You can run all the tests with:

```bash
hatch run test
```

### Format the code

Execute the following command to apply linting and check typing:

```bash
hatch run lint
```

## License

This project is licensed under the terms of the MIT license.
