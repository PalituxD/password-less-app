import logging
import os
from datetime import datetime, timezone

from common.models import BaseModel
from common.services_connection import dynamodb
from pynamodb.attributes import MapAttribute
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

TABLE = os.getenv("PY_TABLE_USERS")

LOGGER = logging.getLogger(__name__)

dynamodb_connection = dynamodb()


class Audit(MapAttribute):
    modified_by = UnicodeAttribute()
    created_date = UTCDateTimeAttribute()
    modified_date = UTCDateTimeAttribute()
    created_by = UnicodeAttribute()


class Location(MapAttribute):
    latitude = UnicodeAttribute(null=True)
    longitude = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)


class ContactInfo(MapAttribute):
    email = UnicodeAttribute(null=True)
    cellphone = UnicodeAttribute(null=True)
    country_phone_code = UnicodeAttribute(null=True)


class UserModel(BaseModel):
    """
    A DynamoDB User
    """

    class Meta:
        table_name = TABLE
        region = dynamodb_connection['region']
        host = dynamodb_connection['host']

    username = UnicodeAttribute(hash_key=True, null=False)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    birthdate = UTCDateTimeAttribute(null=True)
    level = UnicodeAttribute(null=True)
    state = UnicodeAttribute(null=True)
    status = UnicodeAttribute(null=True)
    contact_info = ContactInfo()
    location = Location()
    audit = Audit()

    @classmethod
    def find_by_hash_key(cls, hash_key):
        try:
            return UserModel.get(hash_key)
        except UserModel.DoesNotExist:
            return None

    def save(self, condition=None, **expected_values):
        self.audit = Audit()
        self.audit.created_date = datetime.now(tz=timezone.utc)
        self.audit.modified_date = datetime.now(tz=timezone.utc)
        self.audit.created_by = 'PY'
        self.audit.modified_by = 'PY'
        self.state = 'CREATED'
        self.status = 'UNATTRIBUTED'
        self.contact_info = ContactInfo()
        self.location = Location()
        super(UserModel, self).save(condition)

    def update(self, new_data):
        actions = []

        if 'first_name' in new_data and self.first_name != new_data['first_name']:
            actions.append(UserModel.first_name.set(new_data['first_name']))

        if 'last_name' in new_data and self.last_name != new_data['last_name']:
            actions.append(UserModel.last_name.set(new_data['last_name']))

        if 'birthdate' in new_data and self.birthdate != new_data['birthdate']:
            actions.append(UserModel.birthdate.set(new_data['birthdate']))

        if 'level' in new_data and self.level != new_data['level']:
            actions.append(UserModel.level.set(new_data['level']))

        if 'state' in new_data and self.state != new_data['state']:
            actions.append(UserModel.state.set(new_data['state']))

        if 'status' in new_data and self.status != new_data['status']:
            actions.append(UserModel.status.set(new_data['status']))

        if 'latitude' in new_data and self.location.latitude != new_data['latitude']:
            actions.append(UserModel.location.latitude.set(new_data['latitude']))
        if 'longitude' in new_data and self.location.longitude != new_data['longitude']:
            actions.append(UserModel.location.longitude.set(new_data['longitude']))
        if 'city' in new_data and self.location.city != new_data['city']:
            actions.append(UserModel.location.city.set(new_data['city']))

        if 'email' in new_data and self.contact_info.email != new_data['email']:
            actions.append(UserModel.contact_info.email.set(new_data['email']))
        if 'cellphone' in new_data and self.contact_info.cellphone != new_data['cellphone']:
            actions.append(UserModel.contact_info.cellphone.set(new_data['cellphone']))
        if 'country_phone_code' in new_data and self.contact_info.country_phone_code != new_data['country_phone_code']:
            actions.append(UserModel.contact_info.country_phone_code.set(new_data['country_phone_code']))

        if len(actions) > 0:
            actions.append(UserModel.audit.modified_by.set('PY'))
            actions.append(UserModel.audit.modified_date.set(datetime.now(tz=timezone.utc)))
            super(UserModel, self).update(actions=actions)
        else:
            LOGGER.info(f"Nothing changed did not update for: {self.username}\n")

    def key(self):
        return "username"

    def key_value(self):
        return {"S": str(self.username)}
