import graphene

from soaccess.schema import SOUserQuery, WriteStudy, CreateRoom


class Query(SOUserQuery,
            ):
    pass


class Mutations(graphene.ObjectType):

    write_study = WriteStudy.Field()
    create_room = CreateRoom.Field()

    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
