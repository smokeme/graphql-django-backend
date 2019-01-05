from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)
class CartItem(models.Model):
    quantity = models.IntegerField()
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")
    cartitem = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)



class OrderItem(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)
    quantity = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
class Order(models.Model):
    items = models.ForeignKey(OrderItem,on_delete=models.CASCADE)
    total = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    charge = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)


# type CartItem {
#   id: ID! @unique
#   quantity: Int! @default(value: 1)
#   item: Item
#   user: User!
# }

# type OrderItem {
#   id: ID! @unique
#   title: String!
#   description: String!
#   image: String
#   largeImage: String
#   price: Int!
#   quantity: Int! @default(value: 1)
#   user: User
#   createdAt: DateTime!
#   updatedAt: DateTime!
# }

# type Order {
#   id: ID! @unique
#   items: [OrderItem!]!
#   total: Int!
#   user: User!
#   charge: String!
#   createdAt: DateTime!
#   updatedAt: DateTime!
# }
# type User {
#   id: ID! @unique
#   name: String!
#   email: String! @unique
#   password: String!
#   resetToken: String
#   resetTokenExpiry: Float
#   permissions: [Permission]
#   cart: [CartItem!]!
# }
# type Item {
#   id: ID! @unique
#   title: String!
#   description: String!
#   image: String
#   largeImage: String
#   price: Int!
#   createdAt: DateTime!
#   updatedAt: DateTime!
#   user: User!
# }