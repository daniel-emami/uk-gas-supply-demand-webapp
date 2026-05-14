# Gas Model UK

Gas Model UK is a small runnable monorepo for modelling UK natural gas supply and demand flows.

It uses this deliberately simple architecture:

```text
Scrapers → Transform layer → Excel storage → FastAPI API layer → React frontend
```

The frontend never scrapes or reads Excel directly. It calls the FastAPI backend, and the backend reads Excel and returns JSON.



## Requirements

- Python 3.12.x
- uv
- Node.js 20+ recommended for the frontend

## Repository layout

```text
gas-model-uk/
  README.md
  pyproject.toml
  .gitignore
  data/
    gas_flows.xlsx
  backend/
    GasModelUk/
      Api/
      Cli/
      Config/
      Constants/
      Exceptions/
      Extract/
      Models/
      Orchestration/
      Storage/
      Transform/
      Utilities/
  frontend/
  tests/
```

## Quick run

From the repository root, in terminal 1:

```bash
source .venv/bin/activate
gas-model-uk run-etl --start-date 2026-01-01 --end-date 2026-01-07
gas-model-uk run-api --excel-path data/gas_flows.xlsx
```

In terminal 2:

```bash
cd frontend
npm run dev
```

Then open the Vite URL, usually `http://localhost:5173`.

## Backend setup: macOS/Linux

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
uv sync
```

Run the API with the Excel file:

```bash
gas-model-uk run-api
```

Run the API against the real ETL output workbook path instead:

```bash
gas-model-uk run-api --excel-path data/gas_flows.xlsx
```

Run the ETL manually:

```bash
gas-model-uk run-etl --start-date 2026-01-01 --end-date 2026-01-07
```

The ETL writes successful categories to `data/gas_flows.xlsx` by default.

## Backend setup: Windows PowerShell

From the repository root:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
uv sync
```

Run the API:

```powershell
gas-model-uk run-api
```

Run the API with the real ETL output workbook path:

```powershell
gas-model-uk run-api --excel-path data/gas_flows.xlsx
```

Run the ETL manually:

```powershell
gas-model-uk run-etl --start-date 2026-01-01 --end-date 2026-01-07
```

## Frontend setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

The frontend development server proxies `/api` requests to `http://localhost:8000`.

## API endpoints

All endpoints support optional date filters:

- `start_date=YYYY-MM-DD`
- `end_date=YYYY-MM-DD`

Endpoints:

```text
GET /api/gas-flows
GET /api/gas-flows/demand
GET /api/gas-flows/storage
GET /api/gas-flows/lng
GET /api/gas-flows/production
GET /api/gas-flows/cross-border-flows
```

Example:

```bash
curl "http://localhost:8000/api/gas-flows?start_date=2026-01-01&end_date=2026-01-07"
```

## Data model notes

- Excel is the only intended storage backend.
- `gas_day` is the canonical date column and is stored as `YYYY-MM-DD`.
- Each row is one gas day, not a timestamp.
- Values are in `mcm/d`.
- Excel stores only lowest-level transformed data.
- Aggregate totals are calculated in Python before the API response is returned.
- Missing numeric values are represented as `NaN` in Python/Pandas, blank cells in Excel, and `null` in API JSON.

## Current scraper status

The ETL scraper layer now targets National Gas publication endpoints configured in `backend/GasModelUk/Constants/scraper_registry.py`.

- Demand, storage, LNG, and cross-border flows share the `NationalGridPublicationScraper` template.
- Production remains separate because it splits the response into NCS and UKCS datasets.
- Some National Gas publication IDs map to the same output field. For example, two Isle of Grain LNG IDs are summed into `isle_of_grain`.


## Development helpers

Lint focused backend areas with Ruff:

```bash
uv run ruff check backend/GasModelUk/Extract
```

The repository has a Ruff config, but a full-repo Ruff pass still needs unrelated cleanup in older files.

Run the backend tests with:

```bash
PYTHONPATH=backend python -m unittest discover -s tests
```
