# Problem Definition

## Research Question

Can a federated anomaly detection system distinguish legitimate client
heterogeneity from malicious behavior?

## Domain

Residential electricity consumption time-series data.

## Dataset

London Smart Meter Dataset from the Low Carbon London project.

The complete dataset contains electricity consumption readings from 5,567
London households collected at 30-minute intervals between November 2011
and February 2014.

The initial experiments will use a deterministic subset of households to
keep development and experimentation computationally manageable.

## Federated Client

Each household represents one federated client.

Raw household consumption data remains local to that client during
federated training.

## Sample

A sample initially represents one day of electricity consumption:

- Sampling interval: 30 minutes
- Measurements per day: 48
- Initial input shape: `(48, 1)`

## Legitimate Heterogeneity

Different households naturally exhibit different electricity-consumption
distributions.

These differences are considered legitimate client heterogeneity and must
not automatically be treated as anomalous or malicious behavior.

## Anomaly

An anomaly represents an unusual consumption pattern within a client's
time series.

The initial anomaly-detection experiments will use controlled synthetic
anomalies. Their exact definitions will be documented before implementation.

## Malicious Client

A malicious client intentionally manipulates its local training process,
training data, or model update in order to degrade the federated model.

Malicious behavior will be introduced only after establishing centralized,
federated, and non-IID baselines.

## Initial Scope

The first version of the project will prioritize:

1. Reproducibility
2. Small computational requirements
3. Controlled experiments
4. Per-client evaluation
5. Clear separation between legitimate heterogeneity and malicious behavior

Advanced adversarial attacks and robust aggregation methods are explicitly
out of scope until the baseline system is validated.