# OpenLit with Observability

This implementation demonstrates how to use OpenLit with comprehensive observability features, including distributed tracing and metrics monitoring.

## Features

- Distributed tracing using OpenTelemetry
- Metrics monitoring with Prometheus
- Performance tracking for model inference
- Detailed span attributes for debugging
- Error tracking and monitoring
- Cost tracking with custom pricing configuration

## Setup

### Option 1: Using Docker Compose (Recommended)

1. Start all services using docker-compose:
```bash
docker-compose up -d
```

This will start:
- OpenTelemetry Collector
- Prometheus
- Grafana
- OpenLIT services

Access the services:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- OpenTelemetry UI: http://localhost:16686

To stop all services:
```bash
docker-compose down
```

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start a local OpenTelemetry collector:
```bash
docker run -p 4317:4317 otel/opentelemetry-collector
```

3. Start Prometheus:
```bash
docker run -p 9090:9090 prom/prometheus
```

## Usage

Run the inference script:
```bash
python openlit_inference.py
```

## Monitoring

1. **Traces**: Access traces through your OpenTelemetry backend (e.g., Jaeger, Zipkin)
   - Default endpoint: http://localhost:16686 (if using Jaeger)

2. **Metrics**: Access Prometheus metrics
   - Metrics endpoint: http://localhost:8000
   - Prometheus UI: http://localhost:9090
   - Grafana Dashboard: http://localhost:3000

## Available Metrics

1. **Inference Requests**
   - Counter: `inference_requests_total`
   - Description: Total number of inference requests

2. **Token Usage**
   - Counter: `token_usage_total`
   - Labels: `type` (prompt/completion)
   - Description: Total tokens used

3. **Cost Tracking**
   - Counter: `cost_total`
   - Labels: `type` (prompt/completion)
   - Description: Total cost in USD

## Configuration

### Custom Pricing

The pricing configuration is stored in `assets/pricing.json`. You can modify this file to update the pricing for different models and operations.

Example pricing structure for Llama-3.2:
```json
{
  "chat": {
    "llama-3.2": {
      "promptPrice": 0.1,
      "completionPrice": 0.2,
      "contextWindow": 8192,
      "trainingPrice": 0.0008,
      "embeddingPrice": 0.0001,
      "fineTuningPrice": 0.0016
    }
  }
}
```

## Trace Attributes

The implementation captures the following span attributes:

1. **Model Initialization**
   - model.name
   - model.loaded

2. **Text Generation**
   - prompt.length
   - max_tokens
   - output.length
   - duration

## Best Practices

1. **Resource Management**
   - Monitor memory usage
   - Track GPU utilization
   - Set appropriate batch sizes

2. **Error Handling**
   - All errors are captured in traces
   - Error status and messages are properly attributed
   - Prometheus metrics track error rates

3. **Performance Optimization**
   - Use trace data to identify bottlenecks
   - Monitor latency distributions
   - Track resource utilization patterns
