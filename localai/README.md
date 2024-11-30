# LocalAI Setup with Cross-Encoder

This guide explains how to set up LocalAI with a cross-encoder model for reranking.

## Installation

1. Install LocalAI using Homebrew:
```bash
brew install localai
```

## Installing Cross-Encoder Model

1. First, create a models directory:
```bash
mkdir -p models
```

2. Download the cross-encoder model using LocalAI's pull command:
```bash
local-ai models install cross-encoder
```

3. The model will be downloaded to the default models directory. Make sure your `models.yaml` is configured as shown in the Configuration section.

## Installing Models from LocalAI Gallery

LocalAI provides a gallery of pre-configured models at [LocalAI Gallery](https://localai.io/gallery.html). To install any model from the gallery:

1. Browse the gallery at https://localai.io/gallery.html to find the model you want to install
2. Use the following command to install the model:
```bash
local-ai models install MODEL_NAME
```

For example:
- Install cross-encoder: `local-ai models install cross-encoder`
- Install llama2: `local-ai models install llama2`
- Install stable-diffusion: `local-ai models install stable-diffusion`

The models will be automatically downloaded and configured in your LocalAI installation.

## Running Models

After installing a model, you can run it directly using:
```bash
local-ai run MODEL_NAME
```

For example:
- Run cross-encoder: `local-ai run cross-encoder`
- Run llama2: `local-ai run llama2`
- Run stable-diffusion: `local-ai run stable-diffusion`

This will start the LocalAI server with the specified model. The API will be available at `http://localhost:8080`.

You can also specify a custom port and other options:
```bash
local-ai run MODEL_NAME --address localhost:8081
```

## Configuration

1. Create a config directory and set up the models.yaml:
```bash
mkdir -p config
```

2. The `config/models.yaml` should contain:
```yaml
models:
  - name: cross-encoder
    parameters:
      model: cross-encoder
      type: reranker
      backend: rerankers
    url: https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2
```

## Running LocalAI

1. Start LocalAI with the configuration:
```bash
local-ai --config config/models.yaml
```

The server will be available at `http://localhost:8080`

## Testing

You can use the provided `test_localai.py` script to test the setup.
