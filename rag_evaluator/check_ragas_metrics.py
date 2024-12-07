from ragas import metrics

# Print all available metrics
print("Available metrics in RAGAS:")
for metric in dir(metrics):
    if not metric.startswith('_'):
        print(metric)
