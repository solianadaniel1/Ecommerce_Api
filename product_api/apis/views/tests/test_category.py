from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models.category import Category
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class CategoryViewSetTest(APITestCase):
    def setUp(self):
        """Set up initial test data."""
        # Create an admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", username="admintest", password="password123"
        )
        
        # Create a regular user
        self.regular_user = get_user_model().objects.create_user(
            email="user@example.com", username="usertest", password="password123"
        )
        
        # Create some categories
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Clothing", parent_category=self.category1)
        
        # Create JWT token for authentication
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.user_token = str(RefreshToken.for_user(self.regular_user).access_token)

    def test_create_category_admin(self):
        """Test creating a category by an admin user."""
        url = reverse('category-list')  
        data = {
            "name": "Books"
        }
        
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)  # Ensure the category count has increased
        
    def test_create_category_regular_user(self):
        """Test creating a category by a regular user should fail."""
        url = reverse('category-list')  
        data = {
            "name": "Toys"
        }
        
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        # Check if the response is unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_retrieve_category(self):
        """Test retrieving a single category."""
        url = reverse('category-detail', args=[self.category1.id]) 
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category1.name)
        
    def test_update_category(self):
        """Test updating an existing category by admin."""
        url = reverse('category-detail', args=[self.category1.id])  
        data = {
            "name": "Updated Electronics"
        }
        
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the category is updated
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, "Updated Electronics")
        
    def test_delete_category(self):
        """Test deleting a category by admin."""
        url = reverse('category-detail', args=[self.category2.id])  
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check if the category is deleted
        self.assertEqual(Category.objects.count(), 1)
        
    def test_filter_categories(self):
        """Test filtering categories."""
        url = reverse('category-list')  
        response = self.client.get(url, {'name': 'Electronics'}, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
      
    def test_search_categories(self):
        """Test searching categories."""
        url = reverse('category-list')  
        response = self.client.get(url, {'search': 'Clothing'}, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
    def test_ordering_categories(self):
        """Test ordering categories by name."""
        url = reverse('category-list')  
        response = self.client.get(url, {'ordering': 'name'}, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        print(response.data)
        self.assertTrue(len(response.data) > 0, "No data found in response.")
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     