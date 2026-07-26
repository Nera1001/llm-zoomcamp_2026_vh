"""Deployment manifest — import the pipelines and notebooks you want to deploy and list them in __all__."""

from rest_api_pipeline import load
import agent_traces_dashboard

__all__ = ["load", "agent_traces_dashboard"]
