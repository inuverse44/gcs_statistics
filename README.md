# GCS Statistics

A Python application for analyzing file volumes in Google Cloud Storage (GCS) buckets and generating statistical information.

## Features

- Collection of file statistics for specified prefixes in GCS buckets
- Statistical visualization (graph generation)
- CSV output of statistical information

## Requirements

- Python 3.x
- Google Cloud Platform account and credentials
- Required Python packages:
  - pandas
  - matplotlib
  - google-cloud-storage
  - PyYAML

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd gcs_statistics
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux
# or
.\venv\Scripts\activate  # For Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Configure the following in `config.yaml`:

- `bucket_name`: Target GCS bucket name
- `prefix_list`: List of prefixes to analyze

## Usage

1. Set up Google Cloud credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

2. Run the application:
```bash
python main.py
```

## Output

- Statistics are saved in the `output` directory
- For each prefix, the following files are generated:
  - CSV file (statistical data)
  - Graph images (visualizations)

## Project Structure

- `main.py`: Main script
- `controller.py`: Process control
- `model.py`: Data models and processing logic
- `view.py`: Data visualization
- `config_loader.py`: Configuration file loader
- `config.yaml`: Configuration file

## Coding Standards

### Python Style Guide
- Follow PEP 8 style guide
- Use type hints for function arguments and return values
- Maximum line length: 88 characters (Black formatter standard)

### Documentation
- All modules should have a docstring at the top describing their purpose
- All functions and classes should have docstrings
- Use Google-style docstring format:
  ```python
  def function_name(param1: type, param2: type) -> return_type:
      """Short description.

      Longer description if needed.

      Args:
          param1: Description of param1
          param2: Description of param2

      Returns:
          Description of return value
      """
  ```

### Naming Conventions
- Use `snake_case` for variables, functions, and methods
- Use `PascalCase` for class names
- Use `UPPER_CASE` for constants
- Use descriptive names that reflect the purpose

### Code Organization
- Group related functionality into classes
- Keep functions focused and single-purpose
- Use type hints for better code clarity and IDE support
- Separate business logic (model), control flow (controller), and presentation (view)

### Error Handling
- Use appropriate exception handling
- Provide meaningful error messages
- Log errors when necessary

### Testing
- Write unit tests for critical functionality
- Use pytest for testing
- Maintain good test coverage

## License

MIT License

## Author

Inuverse44