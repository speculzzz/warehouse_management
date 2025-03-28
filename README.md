# Warehouse Management

Simple console-based warehouse management application using Python and SQLAlchemy. 
It is a part of Homework for the OTUS course and is intended for educational purposes.

## Features

- Product inventory management
- Order processing
- Data persistence with SQLite
- **MIT License**: Open-source and free to use.

## Requirements

- Python 3.11 or higher
- SQLAlchemy 2.0+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/speculzzz/warehouse_management.git
   cd warehouse_management
   ```
2. Create virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the application  

```bash
make warehouse
```

### Testing

Run the pytest:
```bash
make pytest
```
Checking test coverage
```bash
make coverage
```

## Project Structure

- `domain/`: Domain components.
- `infrastructure/`: Domain components.
- `tests/`: Test files.
- `Makefile`: Automation for the local operations.
- `main.py`: Main application.
- `warehouse.db`: SQLite database (created by main application).

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

- **speculzzz** (speculzzz@gmail.com)

---

Feel free to use it!