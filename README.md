# FastMCP Server

A small [MCP](https://modelcontextprotocol.io/) server implemented in Python.
It exposes tools over Server-Sent Events (SSE) and listens on port `8080` by
default.

## Requirements

- Python 3.9 or later
- Internet access for `fetch_weather_data`

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run the server

Start the server with:

```powershell
python main.py
```

The server starts on `http://localhost:8080` using SSE transport. To use a
different port, set the `PORT` environment variable before starting it:

```powershell
$env:PORT = "9000"
python main.py
```

The application also loads values from a `.env` file in the project directory.
For example:

```dotenv
PORT=9000
```

## Available tools

| Tool | Parameters | Description |
| --- | --- | --- |
| `add` | `a: int`, `b: int` | Adds two integers. |
| `get_secret_word` | None | Returns a randomly selected word. |
| `fetch_weather_data` | `city: str` | Retrieves current weather data for a city from [wttr.in](https://wttr.in). |

`fetch_weather_data` requires outbound HTTPS access to `wttr.in` and times out
after 10 seconds if the request does not complete.

## Testing the weather tool

With the server running, the MCP smoke test can be run with:

```powershell
python test
```

The test connects to the SSE endpoint at `http://localhost:8080/sse`, performs
the MCP handshake, calls `fetch_weather_data` for London, and prints the tool
response without the surrounding JSON-RPC envelope or terminal color codes.
The server does not expose a REST-style `/tool/...` endpoint; MCP clients use
the advertised endpoint and JSON-RPC messages to call tools.

## Logging and errors

The server logs startup, shutdown, and tool calls to standard output. If a
weather request fails, the server logs the underlying request error and
returns `Error fetching weather data.`.