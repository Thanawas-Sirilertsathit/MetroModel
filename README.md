# Metro Model (Weather x Bangkok train lines)

[![Run Vitest](https://github.com/Thanawas-Sirilertsathit/MetroModel/actions/workflows/vitest.yml/badge.svg)](https://github.com/Thanawas-Sirilertsathit/MetroModel/actions/workflows/vitest.yml) [![Run Unittest](https://github.com/Thanawas-Sirilertsathit/MetroModel/actions/workflows/pytest.yml/badge.svg)](https://github.com/Thanawas-Sirilertsathit/MetroModel/actions/workflows/pytest.yml)

A web application that integrates with Data Analytics models for predicting number of passengers for each train line in Bangkok for commuters in Bangkok. The data that we work on is from March 2025 up to now using sensors to collect weather data every hour. User can predict the value by using our custom predict by input values manually.

## Objectives
- Focus on commuters who use train lines in Bangkok to travel.
- Become a decision making tool for commuters who want to travel without crowding condition.

## Data Analytics models
- Naive Bayes to predict Passenger Rating (Very Low, Low, Moderate, Crowded, Dense and Very Dense)
- Quantile Regression receives output from Naive Bayes and predicts the number of passenger in that hour.

## Sensors for Data acquisition
- DHT-11 temperature and humidity sensor
- BMP280 temperature and pressure sensor

## Data that we used
- Historical weather data from [Weatherapi](https://www.weatherapi.com/history/q/bangkok-2366981?loc=2366981)
- Ministry of transportation data for number of passenger records since January 2021 upto Febuary 2025
- Data from sensors that we acquired

## Testing
- [Test Plan](../../wiki/Test-Plan)
- [Test Scenarios](../../wiki/Test-Scenarios)
- [Test Cases](../../wiki/Test-Cases)

## Pages
- HomePage: Show all train lines with search bar to filter train lines
- DetailPage: Graph showing passenger count or other attributes
- PredictPage: Custom prediction from manual inputs

## Current features
- Predict passenger congestion from manually input data
- Predict passenger congestion from sensor data and historical weather data then show as graph

## Staged Release (Future features)
- Get weather forecast data from future and predict passenger congestion
- Prescriptive analysis for passenger data (Analyze when you should go out using the train line)

## How to run
**Follow the instructions in [Installation guide](INSTALLATION.md) if this is your first time.**

1. Activate Virtual Environment

      **macOS/Linux**

      ```bash
      source .venv/bin/activate
      ```
   
      **Windows**

      ```bash
      .venv\Scripts\activate
      ```

2. Backend part
    - Navigate to the backend directory (`\MetroModel\backend`)
    - Open the terminal and run this command
      ```bash
      python manage.py runserver
      ```

3. Frontend part
    - Navigate to the backend directory (`\MetroModel\frontend`)
    - Open the terminal and run this command
      ```bash
      npm run serve
      ```

4. Connect to site (Default Host for frontend is `127.0.0.1:8080`)

5. To stop the application press Ctrl+C in the terminal then deactivate the venv:
      ```bash
      deactivate
      ```
