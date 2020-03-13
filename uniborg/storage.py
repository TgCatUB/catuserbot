# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
from pathlib import Path


FILE_NAME = "data.json"


class Storage:
    class _Guard:
        def __init__(self, storage):
            self._storage = storage

        def __enter__(self):
            self._storage._autosave = False

        def __exit__(self, *args):
            self._storage._autosave = True
            self._storage._save()

    def __init__(self, root):
        self._root = Path(root)
        self._autosave = True
        self._guard = self._Guard(self)
        if (self._root / FILE_NAME).is_file():
            with open(self._root / FILE_NAME) as file_pointer:
                self._data = json.load(file_pointer)
        else:
            self._data = {}

    def bulk_save(self):
        return self._guard

    def __getattr__(self, name):
        if name.startswith('_'):
            raise ValueError('You can only access existing private members')
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self._data[name] = value
            if self._autosave:
                self._save()

    def _save(self):
        if not self._root.is_dir():
            self._root(parents=True, exist_ok=True)
        with open(self._root / FILE_NAME, 'w') as file_pointer:
            json.dump(self._data, file_pointer)
