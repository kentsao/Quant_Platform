# Quant Platform Prototype

## Overview

This is a prototype for an investment strategy platform. The goal is to allow users to:

* Register and log in securely.
* (Future) Create, share, and rent investment strategies.
* (Future) Backtest strategies using historical data.
* (Future) Visualize strategy performance.
* (Future) Use an LLM Agent to assist with users.
* (Future) Simulate investments.

This prototype focuses on building the foundational backend with user authentication and basic API structure.

## Current Features

* **User Authentication:**
    * User registration with username, email, and password.
    * Secure password hashing using bcrypt.
    * User login to obtain an access token (JWT).

## Technologies Used

* **Backend:** Python, FastAPI
* **Database:** SQLite
* **Security:** JWT (via `fastapi.security`), `python-jose`, `passlib`
* **Data:** `yfinance` (for future stock data)
* **UI (Basic for testing):** HTML, JavaScript
* **Database Interaction:** SQLAlchemy
* **Data Validation:** Pydantic

## Setup Instructions

1.  **Clone the repository**
2.  **Create a Conda environment**
3.  **Install dependencies:**
4.  **Run the backend:**
5.  **Access the basic UI:**
6.  **Test the API:** 

## API Endpoints

## Future Development

* Implement the `Strategy` model and API endpoints for creating, sharing, and retrieving strategies.
* Integrate `yfinance` to fetch stock and bond data.
* Develop the backtesting engine using `Backtrader`.
* Create visualizations for strategy performance using `Plotly` or `Matplotlib`.
* Explore the integration of an LLM for strategy recommendations and a simplified UI for elderly users.
* Implement the simulation investment system.
* Design the strategy rental and payment system.

## Notes

* **Security:** The `SECRET_KEY` in `backend/services/token_service.py` should be changed to a strong, random value in a production environment.
* This is a prototype and is under active development.