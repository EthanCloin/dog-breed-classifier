# Dev Setup

1. setup .env with auth values

```bash
cp .env.template .env
```

Update the placeholder values with the API_KEY and SECRET you received via DMs.
Do not at any time commit those values to git!

1. create and activate the venv for your Python interpreter

```bash
python -m venv .venv
source .venv/bin/activate
```

You may need to alter these steps if you are not on MacOS, check [official docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

1. install dependencies from the requirements file

```bash
pip install -r requirements.txt
```

# Resources

access the digital ocean droplet

```bash
ssh -i path/to/privatekey root@161.35.143.5
```

maybe alternative easier way to use a model image?
https://www.docker.com/blog/build-machine-learning-apps-with-hugging-faces-docker-spaces/
