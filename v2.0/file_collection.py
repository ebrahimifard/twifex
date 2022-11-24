from pathlib import Path
import os


class FileCollection:
    def __init__(self):
        self._temp_json_repo = []
        self.json_repos = {}

    def _json_collector(self, path):
        """It collects path of json files for a given directory path"""
        for p in os.listdir(Path(path)):
            if (Path(path) / p).is_dir():
                self._json_collector(Path(path) / p)
            elif (Path(path) / p).is_file():
                if (Path(path) / p).suffix.lower() == ".json":
                    self._temp_json_repo.append(Path(path) / p)

    def collect_json(self, path):
        """It adds paths of new and non-redundant json files for a given directory path
        to the existing list of json paths"""
        if path in self.json_repos.keys():
            print("json files in the indicated path have already been collected")
        elif sum([Path(explored_path) in Path(path).parents for explored_path in self.json_repos.keys()]):
            print("json files in the indicated path have already been collected")
        else:
            self._json_collector(path)
            self.json_repos[path] = self._temp_json_repo

    def get_all_json(self):
        """It returns a list containing paths of all json files"""
        jsons = set()
        for path, json_list in self.json_repos.items():
            for json_path in json_list:
                jsons.add(json_path)
        return list(jsons)
