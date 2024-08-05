from django.test import Client, TestCase
from .models import Post, Like, User, Following
from django.utils import timezone
from django.urls import reverse


date = timezone.now()
    
# Create your tests here.
class TestPost(TestCase):
    
    def setUp(self):
        
        # Create a new post and a user.
        self.user = User.objects.create(username='testuser', password='test123')
        self.user2 = User.objects.create(username='testuser2', password='test1234')
        self.post = Post.objects.create(username=self.user.username, content='Test post', created_at=date, likes=0)
        
    def test_valid_post_content(self):
        p = Post.objects.get(username='testuser')
        self.assertEqual(p.content, 'Test post')
        
    def test_invalid_post_content(self):
        p = Post.objects.get(username='testuser')
        self.assertNotEqual(p.content, 'Test post2')
        
    def test_likes_0(self):
        p = Post.objects.get(username='testuser')
        self.assertEqual(p.likes, 0)
        
    def test_likes_1(self):
        p = Post.objects.get(username='testuser')
        p.likes += 1
        p.save()
        self.assertEqual(p.likes, 1)
        
    def test_liked_count_1(self):
        p = Post.objects.get(username='testuser')
        user2 = User.objects.get(username='testuser2')

        if user2 not in p.liked.all():
            p.liked.add(user2)
            p.save()
            self.assertEqual(p.liked.count(), 1)
            
            
    def test_liked_count_0(self):
        p = Post.objects.get(username='testuser')
        user2 = User.objects.get(username='testuser2')

        p.liked.add(user2)
        p.save()
            
        if user2 in p.liked.all():
            p.liked.remove(user2)
            p.save()
            self.assertEqual(p.liked.count(), 0)

        

class TestFollowing(TestCase):
    
    def setUp(self):
        # Create a new user.
        self.user = User.objects.create(username='testuser', password='test123')
        self.user2 = User.objects.create(username='testuser2', password='test1234')
        
    
    def test_following_exists(self):
        Following.objects.create(user=self.user2)
        f = Following.objects.get(user=self.user2)
        self.assertIsNotNone(f)
        
    def test_following_count_1(self):
        following = Following.objects.create(user=self.user2)
        self.user.followings.add(following)
        self.user.save()
        followings = self.user.followings.all()
        self.assertEqual(followings.count(), 1)
        
    def test_following_count_0(self):
        following = Following.objects.create(user=self.user2)
        self.user.followings.add(following)
        self.user.save()
        followings = self.user.followings.all()
        self.user.followings.remove(following)
        self.user.save()
        followings = self.user.followings.all()
        self.assertEqual(followings.count(), 0)
        
        

class TestClient(TestCase):
    
    def setUp(self):
        
        # Create a user for testing
        self.credentials = {
            'username': 'testuser',
            'password': 'test123'
        }
        
        self.user = User.objects.create_user(**self.credentials)
        
        # Create a client for testing
        self.client = Client()
        
        # urls
        self.index_url = reverse('network:index')
        self.login_url = reverse('network:login')
        self.following_url = reverse('network:following')
        
        
    def test_index(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')
        
    def test_login(self):
        # Access the login page (GET request)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        # Log in with valid credentials (POST request)
        response = self.client.post(self.login_url, self.credentials, follow=True)
        # Check if the user is logged in
        self.assertTrue(response.context['user'].is_authenticated)
        
    def test_invalid_login(self):
        # Log in with invalid credentials (POST request)
        response = self.client.post(self.login_url, {'username': 'testuser2', 'password': 'test1234'}, follow=True)
        # Check if the login failed
        self.assertTrue(b'Invalid username and/or password.' in response.content)
      
        
        
    def test_following(self):
        # Log in to access the following page
        self.client.post(self.login_url, self.credentials, follow=True)
        # Access the following page (GET request)
        response = self.client.get(self.following_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/following.html')
        # Check if following is displayed
        self.assertIn('Following', str(response.content))
        
    def test_new_post_form(self):
        # Log in to access the new post form
        self.client.post(self.login_url, self.credentials, follow=True)
        # Access the new post form (GET request)
        response = self.client.get(reverse('network:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')
        # Check if the form is displayed
        self.assertIn('New Post', str(response.content))
        
        
    def test_profile(self):
        # Log in the user
        self.client.login(username='testuser', password='test123')

        # Make a GET request to the user profile page
        response = self.client.get(reverse('network:profile', kwargs={'username': 'testuser'}))

        # Check that the response is OK (status code 200)
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'network/profile.html')
        # Check if the user's information is displayed
        self.assertIn(self.credentials['username'], str(response.content))

        # Check if certain content is present in the response
        self.assertContains(response, "Profile: testuser")
            
        
        