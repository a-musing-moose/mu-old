import sqlalchemy as sa

from asyncio import coroutine
from jsonschema import validate


class DoesNotExist(Exception):
    def __init__(self):
        super(DoesNotExist, self).__init__("does not exist")


class MultipleObjectsFound(Exception):
    def __init__(self):
        super(MultipleObjectsFound, self).__init__("multiple objects found")


class ModelManager(object):

    qs = None
    model_map = {}
    schema = None

    def __init__(self, engine):
        self.engine = engine

    def get_queryset(self):
        if self.qs is None:
            raise Exception("query set not defined")
        return self.qs

    def _validate(self, obj):
        if self.schema is None:
            return
        validate(obj, self.schema)

    def _get_clause(self, column, value, operator):
        if operator == '$eq':
            return column == value
        elif operator == '$ne':
            return column != value
        elif operator == '$gt':
            return column > value
        elif operator == '$gte':
            return column >= value
        elif operator == '$lt':
            return column < value
        elif operator == '$lte':
            return column <= value
        raise Exception("{0} is an unsupported operator".format(operator))

    def _get_column(self, key):
        error_message = "{0} is not a valid filter key".format(key)
        segments = key.split(".")
        model_name = ".".join(segments[0:-1])
        column_name = segments[-1]
        if model_name not in self.model_map:
            raise Exception(error_message)
        model = self.model_map[model_name]

        if column_name in model.c:
            return getattr(model.c, column_name)
        raise Exception(error_message)

    def _build_query(self, criteria, limit=None, offset=None):
        query = self.get_queryset().select(use_labels=True)
        clauses = []
        for key, value in criteria.items():
            column = self._get_column(key)
            if type(value) == dict:
                for operator, v in value.items():
                    clauses.append(
                        self._get_clause(column, v, operator)
                    )
            else:
                clauses.append(
                    self._get_clause(column, value, "$eq")
                )
        query = query.where(sa.sql.expression.and_(*clauses))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(limit)
        return query

    @coroutine
    def _execute(self, query):
        with (yield from self.engine) as connection:
            result = yield from connection.execute(query)
        return result

    def _build_object(self, row):
        return dict(row.items())

    @coroutine
    def get(self, criteria):
        query = self._build_query(criteria, limit=1)
        rows = yield from self._execute(query)
        if rows.rowcount == 1:
            row = yield from rows.fetchone()
            return self._build_object(row)
        elif rows.rowcount > 1:
            raise MultipleObjectsFound()
        else:
            raise DoesNotExist()

    @coroutine
    def find(self, criteria, limit=None, offset=None):
        query = self._build_query(criteria, limit, offset)
        rows = yield from self._execute(query)
        objects = []
        for row in rows:
            objects.append(self._build_object(row))
        return objects

    def create(self, obj):
        raise Exception('not implemented')
