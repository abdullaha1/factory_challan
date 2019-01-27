"""Contains handlers for all integrations.
"""

from master_data.sync.asana import Asana
from master_data.sync.jira import Jira

INTEGRATION_MAPPER = {
    "asana": Asana,
    "jira": Jira,
}
