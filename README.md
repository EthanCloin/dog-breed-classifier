# Run Locally

1. Create and activate the venv for your Python interpreter. Python 3.10 is required for tensorflow compatibility

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   You may need to provide a different path to `source` if you are not on MacOS, check [official docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for detailed instructions

1. install dependencies from the requirements file

   ```bash
   pip install -r requirements.txt
   ```

1. setup .env with auth values (do not commit to git)

   ```bash
   cp .env.template .env
   ```

1. run the flask app

   ```bash
   python run.py
   ```

NOTE: scraper functionality might be broken after the pathing changes. debugging required.
