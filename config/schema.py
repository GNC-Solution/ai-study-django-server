import graphene

from soaccess.schema import SOUserQuery, WriteStudy, CreateRoom, UsePhone


class Query(SOUserQuery,
            ):
    pass


class Mutations(graphene.ObjectType):

    write_study = WriteStudy.Field()
    use_phone = UsePhone.Field()
    create_room = CreateRoom.Field()

    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
