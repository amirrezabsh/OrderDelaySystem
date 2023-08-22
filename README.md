# OrderDelaySystem
# Your Django Project Name

[![Python Version](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/downloads/release/python-390/)
[![Django Version](https://img.shields.io/badge/Django-4.2.4-green)](https://docs.djangoproject.com/en/3.2/)

## Description

This project serves as a solution for the Snapp Food code challenge, aiming to manage delays in the delivery of orders to clients efficiently and effectively.

## Features

- Feature 1: The system allows clients to promptly report any delays encountered during the delivery of their orders.
- Feature 2: Agents are provided with the capability to thoroughly investigate delay reports, enabling them to identify and address issues related to order deliveries.
- Feature 3: The system offers a concise summary of the performance of vendors over the previous week, aiding in the assessment and improvement of delivery operations.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.11
- Django 4.2.4
- Docker (optional, for containerization)
- Redis 6.0.16 

### Installation
1. Clone the repository:
```sh
   git clone https://github.com/amirrezabsh/OrderDelaySystem.git
   cd OrderDelaySystem
```
2. Create a virtual environment and activate it:
```sh
python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate
```
3. Install dependencies:
```sh
pip install -r requirements.txt
```
4. Apply migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```
5. Start the development server:
```sh
python manage.py runserver
```
The Django app should now be accessible at http://127.0.0.1:8000/.

### Usage
You can access through the app using endpoints below. Note that all of these endpoints are accessible through `GET` request method.
1. Report delay for an order: `/api/order/report-delay/<int:order_id>/`
2. Assign a delayed order to an agent to investigate the problem: `/api/order/assign-report/<int:agent_id>/`
3. Get vendors orderd by their total delay for the past week: `/api/vendor/weekly-vendors/`
Note: For simplicity `<agent_id>` is just for distincting agents from each other and there is no authentication mechanism for agents.

### Running with Docker
1. Use the docker build command to build your Django image:
```sh
docker build -t your_django_image -f Dockerfile .
```
Replace your_django_image with a meaningful name for your Django image.
2. Once your Django image is built, you can use docker-compose to start your containers:
```sh
docker-compose up
```

### Notes:
- This project is only for SnappFood code challenge and there is no intention to use this project for financial purposes.
- For simplicity all of the `time_stamp` fields in the models are customizable.
