import graphene

import users.schema
import shop.schema


class Query(users.schema.Query,shop.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation,shop.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)