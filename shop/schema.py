import graphene
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Item
from django.db.models import Q


class ItemType(DjangoObjectType):    
    class Meta:
        model = Item

class ItemInput(InputObjectType):
    id = graphene.Int(required=True)
    @property
    def is_valid(self):
        return isinstance(self.id,int)

class Query(graphene.ObjectType):
    items = graphene.List(ItemType,
    search=graphene.String(),
    first=graphene.Int(),
    skip=graphene.Int()
    )
    item = graphene.Field(ItemType, where=ItemInput())
    itemscounter = graphene.Int()
    def resolve_item(self,info,where):
        if where.is_valid:
            return Item.objects.get(id=where.id)
    def resolve_itemscounter(self,info):
        return len(Item.objects.all())
    def resolve_items(self, info,search=None, first=None, skip=None ,**kwargs):
        items = Item.objects.all()
        if search:
            filter = (
                Q(title__icontains=search) | Q(description__icontains=search)
            )
            items = items.filter(filter)
        if skip:
            items = items[skip:]
        if first:
            items = items[:first]
        return items

class CreateItem(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    price = graphene.Int()
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        price = graphene.Int()
    def mutate(self, info,description,title,price):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError('You must be a staff!')
        item = Item(title=title,price=price, description=description)
        item.save()
        return CreateItem(
            id=item.id,
            title=item.title,
            description=item.description,
            price=item.price
        )

class DeleteItem(graphene.Mutation):
    message = graphene.String()
    id = graphene.Int()
    class Arguments:
        id = graphene.Int()
    def mutate(self, info,id):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError('You must be a staff!')
        item = Item.objects.filter(id=id)
        if not item.exists():
            raise GraphQLError('Item doesn`t exists!')
        item.first().delete()
        return DeleteItem(
            id=id,
            message='Item has been deleted'
        )

class UpdateItem(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    price = graphene.Int()
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        price = graphene.Int()
    def mutate(self, info,id,description=None,title=None,price=None):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError('You must be a staff!')
        item = Item.objects.filter(id=id)
        if not item.exists():
            raise GraphQLError('Item doesn`t exists!')
        item = item.first()
        item.title = title or item.title
        item.price = price or item.price
        item.description = description or item.description
        item.save()
        return UpdateItem(
            id=item.id,
            title=item.title,
            description=item.description,
            price=item.price
        )

class Mutation(graphene.ObjectType):
    create_item = CreateItem.Field()
    delete_item = DeleteItem.Field()
    update_item = UpdateItem.Field()