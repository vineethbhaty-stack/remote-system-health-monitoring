"""
POX controller component for the Remote System Health Monitoring project.

This project uses POX's built-in learning-switch controller:
    forwarding.l2_learning

Save this file as:
    ~/pox/pox/project_controller.py

Start it from ~/pox with:
    python3 pox.py project_controller

This wrapper loads the same built-in POX learning-switch component used
during the project tests. It does not implement a separate controller.
"""

from forwarding.l2_learning import launch as launch_learning_switch


def launch(**kwargs):
    launch_learning_switch(**kwargs)
