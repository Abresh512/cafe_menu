#!/usr/bin/env python
"""
Production server runner for Windows
Run with: python run_production.py
"""
from waitress import serve
from app import application

if __name__ == '__main__':
    print("Starting production server on http://localhost:8000")
    print("Press Ctrl+C to stop")
    serve(application, host='0.0.0.0', port=8000)