"""
Base for all sync jobs,
"""
import dramatiq


class Base(object):
    """
    Base class that defines structure for sync jobs.
    
    """
    def extract_workspaces(self):
        raise NotImplementedError

    def extract_projects(self, workspace_id):
        raise NotImplementedError
