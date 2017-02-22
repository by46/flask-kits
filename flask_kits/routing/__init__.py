import hashlib
import os.path

from flask import current_app
from werkzeug.routing import Rule


class KitRule(Rule):
    KNAPSACK = {}

    def build(self, values, append_unknown=True):
        if self.endpoint == 'static' and current_app.has_static_folder and 'filename' in values:
            filename = values.get('filename')
            if filename in KitRule.KNAPSACK:
                values['v'] = KitRule.KNAPSACK.get(filename)
            else:
                static_file_path = os.path.join(current_app.static_folder, filename)
                static_file_path = os.path.normpath(static_file_path)
                if os.path.exists(static_file_path):
                    with open(static_file_path, 'rb') as f:
                        version = hashlib.sha1(f.read()).hexdigest()[:8]
                        KitRule.KNAPSACK[filename] = version
                        values['v'] = version

        return super(KitRule, self).build(values, append_unknown=append_unknown)
