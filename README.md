# Submitted Pages
<img width="1440" alt="Screenshot 2025-06-17 at 5 22 06 PM" src="https://github.com/user-attachments/assets/f504850d-fb87-4b2c-9acd-659b14bdac57" />
<img width="1440" alt="Screenshot 2025-06-24 at 3 13 13 PM" src="https://github.com/user-attachments/assets/99a71f90-1db0-479a-a626-19e841be8f7c" />
<img width="1440" alt="Screenshot 2025-06-24 at 3 13 32 PM" src="https://github.com/user-attachments/assets/be18318c-56e7-4915-aba0-8cf0893fc75b" />

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
