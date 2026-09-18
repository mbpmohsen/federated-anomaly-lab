# Federated Anomaly Lab

A research-oriented project exploring anomaly detection in federated learning
under heterogeneous (non-IID) client distributions and malicious behavior.

## Research Question

Can a federated anomaly detection system distinguish legitimate client
heterogeneity from malicious behavior?

## Status

🚧 Work in progress — Phase 0: Project Bootstrap

## Development Setup

Clone the repository:

```bash
git clone https://github.com/mbpmohsen/federated-anomaly-lab.git
cd federated-anomaly-lab
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install the project with development dependencies:

```
pip install -e ".[dev]"
```

Run code-quality checks:

```
ruff check .
ruff format --check .
```

Run tests:

```
pytest
```