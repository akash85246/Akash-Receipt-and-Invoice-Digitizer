#!/bin/bash
source venv/bin/activate
daphne -b 127.0.0.1 -p 8000 backend.asgi:application