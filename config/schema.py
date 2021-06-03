import graphene

from soaccess.schema import SOUserQuery, WriteLog


class Query(SOUserQuery,
            ):
    pass


class Mutations(graphene.ObjectType):

    write_log = WriteLog.Field()

    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
