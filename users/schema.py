from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, logout, login
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from shop.models import *

def doResetStuff(user):
    ### 
    ## Should send an email with a token 
    ## TODO
    ###
    print(user.email)

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem

class CartType(DjangoObjectType):
    cartitem = graphene.Field(CartItemType)
    def resolve_cartitem(self,info):
        return self.cartitem
    class Meta:
        model = Cart

class UserType(DjangoObjectType):
    cart = graphene.Field(CartType)
    def resolve_cart(self,info):
        return Cart.objects.get(user=self)
    class Meta:
        model = get_user_model()
        # only_fields = ('first_name', 'last_name', 'email','username','cart')
        only_fields = ('email','username','cart')

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class LoginUser(graphene.Mutation):
    message = graphene.String()
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    def mutate(self,info,username,password):
        user = authenticate(username=username,password=password)
        if user is not None:
            login(info.context, user)
            return LoginUser(message="Logged in successfully .!")
        return LoginUser(message="There was an issue with your request .!")
    
class LogoutUser(graphene.Mutation):
    message = graphene.String()
    def mutate(self,info):
        logout(info.context)
        return LogoutUser(message="Logged out successfully .!")
        
class RequestResetPassword(graphene.Mutation):
    message = graphene.String()
    class Arguments:
        email = graphene.String(required=True)
    def mutate(self,info,email):
        user = get_user_model().objects.filter(email=email)
        if user.exists():
            doResetStuff(user.first())
        return LoginUser(message="If the email exists an email will be sent. !")
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    request_reset_password = RequestResetPassword.Field()

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)
    def resolve_me(self,info):
        if info.context.user.is_authenticated:
            return get_user_model().objects.get(id=info.context.user.id)
        raise GraphQLError('You must be logged in!')
    def resolve_users(self, info):
        print(info.context.user)
        return get_user_model().objects.all()