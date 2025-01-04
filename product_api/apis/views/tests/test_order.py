from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from order.models import Order
from rest_framework_simplejwt.tokens import RefreshToken
from product.models.product import Product

class OrderViewSetTest(APITestCase):
    def setUp(self):
        """
        Set up the test environment. Create a user and a few orders.
        """
        # Create users
        self.user1 = get_user_model().objects.create_user(username='user1',email="user1@example.com",  password='password123')
        self.user2 = get_user_model().objects.create_user(username='user2',email="user2@example.com", password='password123')

       # Create products
        self.product1 = Product.objects.create(name="Product1", price=100, stock_quantity=2) 
        self.product2 = Product.objects.create(name="Product2", price=200, stock_quantity=3)
        self.product3 = Product.objects.create(name="Product3", price=300, stock_quantity=4)

        # Create orders for user1 and user2
        self.order1 = Order.objects.create(user=self.user1, product=self.product1, order_status="Pending", quantity=1, shipping_address="Address1",total_price=4.55)
        self.order2 = Order.objects.create(user=self.user1, product=self.product2, order_status="Shipped", quantity=2, shipping_address="Address2", total_price=800)
        self.order3 = Order.objects.create(user=self.user2, product=self.product3, order_status="Delivered", quantity=3, shipping_address="Address3", total_price=89)

        # Obtain a token for user1 and user2
        self.token_user1 = RefreshToken.for_user(self.user1).access_token
        self.token_user2 = RefreshToken.for_user(self.user2).access_token

    def test_create_order(self):
        """
        Test creating an order. Only authenticated users can create orders.
        """
        url = '/api/orders/'
        data = {
            'product': self.product1.id,
            'order_status': 'Pending',
            'quantity': 1,
            'shipping_address': 'Address4',
            'total_price': 4.55
        }
        response = self.client.post(
            url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token_user1}'
        )
        # Test creation for user1
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product'], self.product1.id)
        self.assertEqual(response.data['user'], self.user1.id)

        # Test creation for unauthenticated user
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_access_permissions(self):
        """
        Test that users can only access their own orders.
        """
        url = f'/api/orders/{self.order1.id}/'
        
        # Test user1 accessing their own order
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test user2 trying to access user1's order
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user2}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_orders(self):
        """
        Test filtering orders by user, order_status, etc.
        """
        url = '/api/orders/?user={}'.format(self.user1.id)
        
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test searching orders by product name
        url = '/api/orders/?search=Product1'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
      

    def test_order_update(self):
        """
        Test updating an order. Users can only update their own orders.
        """
        url = f'/api/orders/{self.order1.id}/'
        data = {
            'order_status': 'Shipped',
            'quantity': 3,
        }

        # Test user1 updating their own order
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_status'], 'Shipped')
        self.assertEqual(response.data['quantity'], 3)

        # Test user2 trying to update user1's order
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token_user2}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_delete(self):
        """
        Test deleting an order. Users can only delete their own orders.
        """
        url = f'/api/orders/{self.order1.id}/'

        #Check if the order exists:
        order_exists = Order.objects.filter(id=self.order1.id).exists()
        print(f"Order exists: {order_exists}")
        
        # Test user1 deleting their own order
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Test user2 trying to delete user1's order
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user2}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_ordering(self):
        """
        Test ordering orders by user and other fields.
        """
        url = '/api/orders/?ordering=user'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
       