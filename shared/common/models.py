import abc

from dynamodb_json import json_util as json
from pynamodb.models import Model


class BaseModel(Model):
    __metaclass__ = abc.ABCMeta

    def get_json(self):
        json_data = self._get_json()
        data = json_data[1]["attributes"]
        data[self.key()] = self.key_value()
        return json.loads(data)

    @abc.abstractmethod
    def key(self):
        pass

    @abc.abstractmethod
    def key_value(self):
        pass
