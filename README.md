# Simple *Streamlit* project template

The purpose of this repository is to provide an initial project template for
[Streamlit](https://streamlit.io/) apps that simplifies and speeds up development.

## Development

### Get the template

To use the tamplate first clone this repository.

```bash
git clone https://github.com/pixpack/streamlit-base.git my-streamlit-app
```

Move into the templates directory.

```bash
cd my-streamlit-app
```

On Github you can also click the `Use this template` button to automatically create
your own repository based on this template.

### Create the development environment

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

On Linux, macOS.

```bash
source .venv/bin/activate
```

On Windows (Powershell).

```bash
.venv/Scripts/Activate.ps1
```

Get the development dependencies.

```bash
python -m pip install --upgrade pip && \
pip install -r requirements-dev.txt
```

### Edit the code

Start editing the app files in the `app` directory with your favourite editor.

For more information on how to develop Streamlit apps, check [Streamlit documentation](https://docs.streamlit.io/).

### Run the app

Start the app with the `streamlit run` command.

```bash
streamlit run app/main.py
```

## Testing

Run the tests.

```bash
pytest
```

For more information on testing, visit [pytest documentation](https://docs.pytest.org/).

## Deployment

The template is set up with Docker to deploy the app.

### Configuration

Configure the streamlit `config.toml` to your needs.
> When changing the default ports in the configuration, remember to also change
> them in `docker run` command.

Build the Docker image.

```bash
docker build -t streamlit-app .
```

Run the container.

```bash
docker run -dp 8501:8501 streamlit-app
```

## Contributing

Contributions are very welcome.

To contribute:

1. Create an issue you would like to work on.
2. Fork the repository.
3. Create a pull request and attach the issue.

## Acknowledgments

The initial streamlit config comes from the great
[Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit)
repository.
