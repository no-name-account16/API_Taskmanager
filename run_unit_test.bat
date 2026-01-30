@echo off
cd backend
pytest unit_test_main.py --cov=. --cov-report=html --cov-report=term



@REM - Use below to find missing tests .
@REM pytest unit_test_main.py --cov=main --cov-report=term-missing