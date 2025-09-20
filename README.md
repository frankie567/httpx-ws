# HTTPX WS

<p align="center">
    <em>WebSockets support for HTTPX</em>
</p>

[![build](https://github.com/frankie567/httpx-ws/workflows/Build/badge.svg)](https://github.com/frankie567/httpx-ws/actions)
[![codecov](https://codecov.io/gh/frankie567/httpx-ws/branch/main/graph/badge.svg?token=fL49kIvrj6)](https://codecov.io/gh/frankie567/httpx-ws)
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors)
[![PyPI version](https://badge.fury.io/py/httpx-ws.svg)](https://badge.fury.io/py/httpx-ws)
[![Downloads](https://pepy.tech/badge/httpx-ws)](https://pepy.tech/project/httpx-ws)

---

**Documentation**: <a href="https://frankie567.github.io/httpx-ws/" target="_blank">https://frankie567.github.io/httpx-ws/</a>

**Source Code**: <a href="https://github.com/frankie567/httpx-ws" target="_blank">https://github.com/frankie567/httpx-ws</a>

---

## Installation

```bash
pip install httpx-ws
```

## Features

- [x] Sync and async client
- [x] Helper methods to send text, binary and JSON data
- [x] Helper methods to receive text, binary and JSON data
- [x] Automatic ping/pong answers
- [x] HTTPX transport to test WebSockets defined in ASGI apps
- [x] Automatic keepalive ping
- [x] `asyncio` and [Trio](https://trio.readthedocs.io/) support through [AnyIO](https://anyio.readthedocs.io/)

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
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/davidbrochart"><img src="https://avatars.githubusercontent.com/u/4711805?v=4?s=100" width="100px;" alt="David Brochart"/><br /><sub><b>David Brochart</b></sub></a><br /><a href="#platform-davidbrochart" title="Packaging/porting to new platform">📦</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=davidbrochart" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ysmu"><img src="https://avatars.githubusercontent.com/u/17018576?v=4?s=100" width="100px;" alt="ysmu"/><br /><sub><b>ysmu</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Aysmu" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://samforeman.me"><img src="https://avatars.githubusercontent.com/u/5234251?v=4?s=100" width="100px;" alt="Sam Foreman"/><br /><sub><b>Sam Foreman</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Asaforem2" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://maparent.ca/"><img src="https://avatars.githubusercontent.com/u/202691?v=4?s=100" width="100px;" alt="Marc-Antoine Parent"/><br /><sub><b>Marc-Antoine Parent</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Amaparent" title="Bug reports">🐛</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=maparent" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.fastapiexpert.com/"><img src="https://avatars.githubusercontent.com/u/7353520?v=4?s=100" width="100px;" alt="Marcelo Trylesinski"/><br /><sub><b>Marcelo Trylesinski</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3AKludex" title="Bug reports">🐛</a> <a href="#research-Kludex" title="Research">🔬</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://lit.link/MtkN1"><img src="https://avatars.githubusercontent.com/u/51289448?v=4?s=100" width="100px;" alt="MtkN1"/><br /><sub><b>MtkN1</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3AMtkN1" title="Bug reports">🐛</a> <a href="#research-MtkN1" title="Research">🔬</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=MtkN1" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.tomchristie.com/"><img src="https://avatars.githubusercontent.com/u/647359?v=4?s=100" width="100px;" alt="Tom Christie"/><br /><sub><b>Tom Christie</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Atomchristie" title="Bug reports">🐛</a> <a href="#research-tomchristie" title="Research">🔬</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dmontagu"><img src="https://avatars.githubusercontent.com/u/35119617?v=4?s=100" width="100px;" alt="David Montague"/><br /><sub><b>David Montague</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Admontagu" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/WSH032"><img src="https://avatars.githubusercontent.com/u/126865849?v=4?s=100" width="100px;" alt="Sean Wang"/><br /><sub><b>Sean Wang</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/commits?author=WSH032" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/agronholm"><img src="https://avatars.githubusercontent.com/u/130003?v=4?s=100" width="100px;" alt="Alex Grönholm"/><br /><sub><b>Alex Grönholm</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Aagronholm" title="Bug reports">🐛</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=agronholm" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ro-oliveira95"><img src="https://avatars.githubusercontent.com/u/27009864?v=4?s=100" width="100px;" alt="Rodrigo de Oliveira Neto"/><br /><sub><b>Rodrigo de Oliveira Neto</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Aro-oliveira95" title="Bug reports">🐛</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=ro-oliveira95" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://tinymind.me/GreyElaina"><img src="https://avatars.githubusercontent.com/u/31543961?v=4?s=100" width="100px;" alt="Elaina"/><br /><sub><b>Elaina</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/commits?author=GreyElaina" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://runsisi.com"><img src="https://avatars.githubusercontent.com/u/2339258?v=4?s=100" width="100px;" alt="runsisi"/><br /><sub><b>runsisi</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Arunsisi" title="Bug reports">🐛</a> <a href="#research-runsisi" title="Research">🔬</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lulingar"><img src="https://avatars.githubusercontent.com/u/4201057?v=4?s=100" width="100px;" alt="Luis Linares"/><br /><sub><b>Luis Linares</b></sub></a><br /><a href="https://github.com/frankie567/httpx-ws/issues?q=author%3Alulingar" title="Bug reports">🐛</a></td>
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
