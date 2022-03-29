import os
from types import TracebackType
from typing import Any, Dict, Optional, Text, Type

from constants.app_constants import (ADMIN_AUTH_SOURCE, MONGODB_AUTH_SOURCE,
                                     MONGODB_PASSWORD, MONGODB_URL,
                                     MONGODB_USERNAME)
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDB:
    """
    MongoDB Connection class
    """
    connection = None

    def __init__(self, dbname: Text):
        """
        Initialize connection

        Args:
            dbname (Text): name of database
        """
        if self.connection is None:
            self.connection = MongoClient(
                os.getenv(MONGODB_URL),
                username=os.getenv(MONGODB_USERNAME),
                password=os.getenv(MONGODB_PASSWORD),
                authSource=os.getenv(MONGODB_AUTH_SOURCE) or ADMIN_AUTH_SOURCE,
                connect=False,
            )

        self.client = self.connection
        self.db = self.client[dbname]

    def collection(self, name: Text) -> Collection:
        """
        Returns collection object for given collection name

        Args:
            name (Text): collection name

        Returns:
            Collection: collection object
        """
        if name is not None:
            return self.db[name]
        return None

    @classmethod
    def insert(cls, collection: Collection, data: Dict[Text, Any]) -> Any:
        """
        Inserts record into the given collection

        Args:
            collection (Collection): collection
            data (Dict[Text, Any]): data dict

        Returns:
            Any: boolean
        """
        try:
            collection.insert_one(data)
        except Exception:
            pass

    @classmethod
    def get_collection(cls, database: Text, name: Text) -> Collection:
        """
        Gets collection belonging to default db and returns it.

        Args:
            name (Text): name of collection

        Returns:
            Collection: collection object
        """
        obj = cls(database)
        return obj.db[name]

    def __exit__(self,
                 _exc: Optional[Type[BaseException]],
                 _value: Optional[Exception],
                 _tb: Optional[TracebackType],
                 ) -> bool:
        """
        Destroys open connection

        Args:
            _exc (Optional[Type[BaseException]]): exc type
            _value (Optional[Exception]): exc value
            _tb (Optional[TracebackType]): traceback

        Returns:
            bool: flag
        """
        if self.client is not None:
            self.client.close()
