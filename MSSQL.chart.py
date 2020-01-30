from re import search
from bases.FrameworkServices.LogService import LogService

update_every = 5
retries = 3


ORDER = ['login_failed']

CHARTS = {
    'login_failed': {
        'options': [None, 'Failed Authentications', 'count', 'Authentication',
                    'mssql.failed_auth', 'line'],
        'lines': [
            ["count", "failed-count", 'absolute', 1, 1]
        ]},
}


class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        self.log_path = self.configuration.get('path', '/var/logs/syslog')
        self.order = ORDER
        self.definitions = CHARTS

    def _get_data(self):
        try:
            count = 0
            for line in self._get_raw_data():
                if search(r'sqlservr.+Login failed', line):
                    count += 1
            return {"count": count}
        except (ValueError, AttributeError):
            return None
