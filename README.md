# Run Locally

1. Create and activate the venv for your Python interpreter. Python 3.10 is required for tensorflow compatibility

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

   You may need to provide a different path to `source` if you are not on MacOS, check [official docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for detailed instructions

1. install dependencies from the requirements file

   ```bash
   pip install -r requirements.txt
   ```

1. run the flask app

   ```bash
   python run.py
   ```
