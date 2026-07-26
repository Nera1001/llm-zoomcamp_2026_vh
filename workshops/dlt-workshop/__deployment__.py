"""Deployment manifest for the agent traces pipeline and dashboard."""

from rest_api_pipeline import load
import agent_traces_dashboard

__all__ = [
    "load",
    "agent_traces_dashboard",
]
