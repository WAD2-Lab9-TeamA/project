from django.test import TestCase

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders


# Create your tests here.

class IndexPageTests(TestCase):

    def test_index_contains_hello_message(self):
        # Check if there is the message to find deals e.g "Find deals near you"..
        response = self.client.get(reverse('index'))
        self.assertIn(b'Find deals near you', response.content)

    def test_index_using_template(self):
        # Check the template used to render index page
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'studeals/index.html')

    def test_index_has_title(self):
        # Check to make sure that the title tag has been used
        response = self.client.get(reverse('index'))
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)

class ContactUsPageTests(TestCase):

    def test_about_contains_create_message(self):
        # Check if in the contact us page is there - and has some info about the page
        response = self.client.get(reverse('contact'))
        self.assertIn(b'students can share and get easy access to local student deals.', response.content)


    def test_contact_us_contain_image(self):
        # Check if is there are images of creators on contact us page
        response = self.client.get(reverse('contact'))
        self.assertIn(b'img src="https://graph.facebook.com/100000506448980/picture?type=large', response.content)
        self.assertIn(b'img src="https://graph.facebook.com/100000465603694/picture?type=large', response.content)
        self.assertIn(b'https://graph.facebook.com/100013098992415/picture?type=large', response.content)

    def test_has_link_to_github(self):
        # Check if link to github is on page, link added to provide user with additional info on the web app
        response = self.client.get(reverse('contact'))
        self.assertIn(b'https://github.com/WAD2-Lab9-TeamA/project',response.content)

    def test_contact_us_using_template(self):
        # Check the template used to render contact us page
        response = self.client.get(reverse('contact'))

        self.assertTemplateUsed(response, 'studeals/contact.html')



class ModelTests(TestCase):

    def setUp(self):
        #Populate offers
        try:
            from populate_app import populate
            populate()
        except ImportError:
            print('The module populate_app does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')


    def get_offers(self, title):
        #function to get offers
        from studeals.models import Offer
        try:
            ofr = Offer.objects.get(title=title)
        except Offer.DoesNotExist:
            ofr = None
        return ofr

    def test_cookie_offer_added(self):
        #test cookie offer has been added
        ofr = self.get_offers('Double Chocolate Cookies')
        self.assertIsNotNone(ofr)

    def test_cookie_offer_with_promo(self):
        #test promo
        ofr = self.get_offers('Double Chocolate Cookies')
        self.assertEquals(ofr.price, '1.00')

    def test_cookie_offer_with_expiry_date(self):
        #test expiration
        ofr = self.get_offers('Double Chocolate Cookies')
        self.assertEquals(ofr.expiration_date, '2018-03-30')

class ViewTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_offers(self):
        response = self.client.get('/offers')
        self.assertEqual(response.status_code, 200)

    def test_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)






    # Testing all forms exist
    def Test_Contact_Form_Exists(self):

        try:
            from forms import ContactUsForm
            from forms import UserProfileForm
            from forms import PasswordResetForm
            from forms import PasswordResetRequestForm
            from forms import PasswordUpdateForm
            from forms import OfferForm

        except ImportError:
            print('The module forms does not exist')
        except NameError:
            print('The class for a form does not exist or is not correct')
        except:
            print('Something else went wrong :-(')

    pass



class PermissionsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.user.save()

    def test_permissions_overview(self):
        #User not logged in (guest)
        #Shouldn't be able to add offer
        #Redirect to login expected followed by add-offer
        response = self.client.get(reverse('add_offer'))
        self.assertRedirects(response, '/login/?next=/add-offer')

        #Logged in user that should be able to see this page
        #self.client.login(username='user', password='pass')
        #self.assertRedirects(response, 'add-offer')

# Create your tests here.
