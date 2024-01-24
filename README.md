# Python Application for scraping Autoria.com
https://auto.ria.com/uk/car/used/

- [Installation](#Installation)
- [To-do](#To-do)


## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/Tarasidze/theatre-api-service
   ```
2. **Create environment:**
   ```
   python -m venv venv
   ```
      and activate it:
   - on windows
        ```shell
        venv\Scripts\activate 
        ```
   - on macOS or Linux:
        ```bash
        source venv/bin/activate 
        ```
   ```
3. **Raname  .env-EXAMPLE to .env file and define your password:**
   ```
    POSTGRES_DB="db_autoria"
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="best pass"
    POSTGRES_HOST="db_auto"
    POSTGRES_PORT="5432"
   ```
4. **Run command:**
   ```
   docker-compose up --build
   ```

## To-do

- add checking database
- fix docker-compose (some trouble in container network)
- add more logging
    




