import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ecantina_project import constants

# Grand Comics Database Models
#------------------------------------------------------------------
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.image import GCDImage
from api.models.gcd.indiciapublisher import GCDIndiciaPublisher
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.brandgroup import GCDBrandGroup
from api.models.gcd.brand import GCDBrand
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.storytype import GCDStoryType
from api.models.gcd.story import GCDStory
from api.models.gcd.branduse import GCDBrandUse
from api.models.gcd.brandemblemgroup import GCDBrandEmblemGroup

# Comics Cantina Database Models
#------------------------------------------------------------------
from api.models.ec.imagebinaryupload import ImageBinaryUpload
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.imageupload import ImageUpload
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.helprequest import HelpRequest
from api.models.ec.receipt import Receipt
from api.models.ec.promotion import Promotion
from api.models.ec.wishlist import Wishlist
from api.models.ec.pulllist import Pulllist
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.models.ec.tag import Tag
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from api.models.ec.emailsubscription import EmailSubscription
from api.models.ec.unified_shipping_rates import UnifiedShippingRate
from api.models.ec.print_history import PrintHistory
from api.models.ec.subdomain import SubDomain
from api.models.ec.banned_domain import BannedDomain
from api.models.ec.banned_ip import BannedIP
from api.models.ec.banned_word import BannedWord
from api.models.ec.catalog_item import CatalogItem


class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_sample_db
    """
    help = 'Populates the tables neccessary to give us a initial start.'
    
    def handle(self, *args, **options):
        # Defensive Code: Prevent this custom command code from running if
        #                 the application is not in 'Unit Test' mode.
        is_running_unit_tests = len(sys.argv) > 1 and sys.argv[1] == 'test'
        if not is_running_unit_tests:
            self.stdout.write('Cannot run, only acceptable command in unit testing.')
            return
        
        # Get the current time.
        now = datetime.now()
        
        #----------------
        # Administrator
        #----------------
        try:
            user = User.objects.get(email='bmika@icloud.com')
        except User.DoesNotExist:
            user = User.objects.create_user(
                'bmika@icloud.com',  # Username
                'bmika@icloud.com',  # Email
                '123password',
            )
            user.first_name = 'Bart'
            user.last_name = 'Mika'
            user.is_active = True
            user.save()
            user = User.objects.get(email='bmika@icloud.com')

#        #----------------
#        # Image Uploads
#        #----------------
#        try:
#            org_logo = ImageUpload.objects.get(upload_id=1)
#        except ImageUpload.DoesNotExist:
#            org_logo = ImageUpload.objects.create(
#                upload_id = 1,
#                upload_date = now,
#                image = 'upload/bascomics_logo.png',
#                user = user,
#            )
#
#        try:
#            profile = ImageUpload.objects.get(upload_id=2)
#        except ImageUpload.DoesNotExist:
#            profile = ImageUpload.objects.create(
#                upload_id = 2,
#                upload_date = now,
#                image = 'upload/pepe.png',
#                user = user,
#            )
#
#        try:
#            store_logo = ImageUpload.objects.get(upload_id=1)
#        except ImageUpload.DoesNotExist:
#            store_logo = ImageUpload.objects.create(
#                upload_id = 3,
#                upload_date = now,
#                image = 'upload/bascomics_logo.png',
#                user = user,
#            )
        org_logo = None
        profile = None
        store_logo = None

        #-----------------
        # Organization
        #-----------------
        try:
            organization = Organization.objects.get(org_id=1)
        except Organization.DoesNotExist:
            organization = Organization.objects.create(
                org_id=1,
                name='B.A.\'s Comics',
                description = 'Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
                joined = now,
                street_name='Hamilton Rd',
                street_number='426',
                unit_number=None,
                city='London',
                province='Ontario',
                country='Canada',
                postal='N5Z 1R9',
                website='http://www.bacomics.ca',
                email=None,
                phone='5194399636',
                fax=None,
                twitter='bascomics',
                facebook_url=None,
                instagram_url=None,
                linkedin_url=None,
                github_url=None,
                google_url='https://plus.google.com/105760942218297346537/about',
                youtube_url=None,
                flickr_url=None,
                administrator = user,
                logo = org_logo,
                paypal_email = 'rodolfo@theshootingstarpress.com',
            )

        #-----------------
        # Store
        #-----------------
        try:
            store = Store.objects.get(store_id=1)
        except Store.DoesNotExist:
            store = Store.objects.create(
                store_id=1,
                name='Main Store',
                description='Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
                joined=now,
                street_name='Hamilton Rd',
                street_number='426',
                unit_number=None,
                city='London',
                province='Ontario',
                country='Canada',
                postal='N5Z 1R9',
                website='http://www.bacomics.ca',
                email=None,
                phone='5194399636',
                fax=None,
                organization=organization,
                logo=store_logo,
                is_open_monday = True,
                is_open_tuesday = True,
                is_open_wednesday = True,
                is_open_thursday = True,
                is_open_friday = True,
                is_open_saturday = True,
                is_open_sunday = False,
                monday_to = '18:00',
                tuesday_to = '18:00',
                wednesday_to = '18:00',
                thursday_to = '18:00',
                friday_to = '18:00',
                saturday_to = '18:00',
                sunday_to = '18:00',
                monday_from = '08:00',
                tuesday_from = '08:00',
                wednesday_from = '08:00',
                thursday_from = '08:00',
                friday_from = '08:00',
                saturday_from = '08:00',
                sunday_from = '08:00',
                paypal_email = 'rodolfo@theshootingstarpress.com',
            )

        #-----------------
        # Employees
        #-----------------
        try:
            owner = Employee.objects.get(employee_id=1)
        except Employee.DoesNotExist:
            owner = Employee.objects.create(
                employee_id=1,
                joined = datetime.now(),
                role = constants.EMPLOYEE_OWNER_ROLE,
                user = user,
                organization = organization,
                profile=profile,
            )
            # Make "Owner" an employee of that store.
            store.employees.add(owner)
            store.save()
        
        # Create Sections
        try:
            section1 = Section.objects.get(section_id=1)
            section2 = Section.objects.get(section_id=2)
            section3 = Section.objects.get(section_id=3)
            section4 = Section.objects.get(section_id=4)
        except Section.DoesNotExist:
            section1 = Section.objects.create(
                section_id=1,
                name='Downstairs',
                store=store,
                organization = organization,
            )
            section2 = Section.objects.create(
                section_id=2,
                name='Upstairs',
                store=store,
                organization = organization,
            )
            section3 = Section.objects.create(
                section_id=3,
                name='Front Pile',
                store=store,
                organization = organization,
            )
            section4 = Section.objects.create(
                section_id=4,
                name='Back Pile',
                store=store,
                organization = organization,
            )
        sections = Section.objects.filter(store=store)
        

        #-----------------
        # Tag
        #-----------------
        try:
            tag1 = Tag.objects.get(tag_id=1)
            tag2 = Tag.objects.get(tag_id=2)
            tag3 = Tag.objects.get(tag_id=3)
            tag4 = Tag.objects.get(tag_id=4)
            tag5 = Tag.objects.get(tag_id=5)
            tag6 = Tag.objects.get(tag_id=6)
            tag7 = Tag.objects.get(tag_id=7)
            tag8 = Tag.objects.get(tag_id=8)
            tag9 = Tag.objects.get(tag_id=9)
            tag10 = Tag.objects.get(tag_id=10)
        except Tag.DoesNotExist:
            tag1 = Tag.objects.create(
                tag_id=1,
                name = 'Marvel',
                organization_id = 1,
            )
            tag2 = Tag.objects.create(
                tag_id=2,
                name = 'DC',
                organization_id = 1,
            )
            tag3 = Tag.objects.create(
                tag_id=3,
                name = 'Image',
                organization_id = 1,
            )
            tag4 = Tag.objects.create(
                tag_id=4,
                name = 'BOOM!',
                organization_id = 1,
            )
            tag5 = Tag.objects.create(
                tag_id=5,
                name = 'Lucha Comics',
                organization_id = 1,
            )
            tag6 = Tag.objects.create(
                tag_id=6,
                name = 'Dark Horse',
                organization_id = 1,
            )
            tag7 = Tag.objects.create(
                tag_id=7,
                name = 'Dynamite',
                organization_id = 1,
            )
            tag8 = Tag.objects.create(
                tag_id=8,
                name = 'IDW',
                organization_id = 1,
            )
            tag9 = Tag.objects.create(
                tag_id=9,
                name = 'Batman',
                organization_id = 1,
            )
            tag10 = Tag.objects.create(
                tag_id=10,
                name = 'Ice Age',
                organization_id = 1,
            )

        #-----------------
        # GCD Language
        #-----------------
        try:
            english = GCDLanguage.objects.get(language_id=25)
        except GCDLanguage.DoesNotExist:
            english = GCDLanguage.objects.create(
                language_id=25,
                name = 'English',
                code = 'en',
            )

        #-----------------
        # GCD Country
        #-----------------
        try:
            canada = GCDCountry.objects.get(country_id=36)
            united_states = GCDCountry.objects.get(country_id=225)
        except GCDCountry.DoesNotExist:
            canada = GCDCountry.objects.create(
                country_id=36,
                name = 'Canada',
                code = 'en',
            )
            united_states = GCDCountry.objects.create(
                country_id=225,
                name = 'United States',
                code = 'us',
            )

        #-----------------
        # GCD Publisher
        #-----------------
        try:
            marvel = GCDPublisher.objects.get(publisher_id=666)
        except GCDPublisher.DoesNotExist:
            marvel = GCDPublisher.objects.create(
                publisher_id=666,
                name = 'Marvel',
                year_began = 1945,
                year_ended = 2016,
                notes = "",
                url = "http://www.comicscantina.com",
                country = canada,
            )

        #-----------------
        # GCD Brand
        #-----------------
        try:
            brand = GCDBrand.objects.get(brand_id=666)
        except GCDBrand.DoesNotExist:
            brand = GCDBrand.objects.create(
                brand_id = 666,
                issue_count = 1,
#                parent = models.ForeignKey(GCDPublisher, null=True)
#                group = models.ManyToManyField(GCDBrandGroup, blank=True,)
#                images = models.ManyToManyField(GCDImage)
                name = 'Marvel',
                year_began = 2016,
                year_ended = 300,
                year_began_uncertain = False,
                year_ended_uncertain = False,
                notes = '',
                keywords = '',
#                url = '',
                reserved = False,
#                created = models.DateTimeField(auto_now_add=True)
#                modified = models.DateTimeField(auto_now=True)
                deleted = False,
            )

        #-----------------
        # GCD Series
        #-----------------
        try:
            series = GCDSeries.objects.get(publisher_id=666)
        except GCDSeries.DoesNotExist:
            series = GCDSeries.objects.create(
                series_id=666,
                name = 'Winterworld',
                sort_name = 'Winterworld',
                year_began = 2000,
                year_ended = 2016,
                publication_dates = "2014-01-01",
                country = canada,
                language = english,
                publisher = marvel,
                publisher_name = "Marvel",
            )

        #-----------------
        # GCD Issues
        #-----------------
        try:
            issue = GCDIssue.objects.get(issue_id=666)
        except GCDIssue.DoesNotExist:
            issue = GCDIssue.objects.create(
                issue_id = 666,
                number = '12',
                title = 'Continental Union History Book',
                no_title = False,
                volume = 'vol 1',
                no_volume = False,
                display_volume_with_number = 'False',
                isbn = '1234567890',
                no_isbn = True,
                valid_isbn = '987654321',
                variant_of_id = 1,
                variant_name = '',
                barcode = '',
                no_barcode = True,
                rating = '100',
                no_rating = True,
                is_first_issue = True,
                is_last_issue = True,
                publication_date = '2015-01-01',
                key_date = '2014-01-01',
                on_sale_date = '',
                on_sale_date_uncertain = True,
                sort_code = 1,
                indicia_frequency = '',
                price = '',
                page_count = 9.99,
                page_count_uncertain = False,
                editing = '',
                no_editing = False,
                notes = '',
                keywords = '',
                is_indexed = 1,
                reserved = False,
#                created = models.DateTimeField(auto_now_add=True)
#                modified = models.DateTimeField(auto_now=True, db_index=True)
                deleted = False,
                indicia_pub_not_printed = False,
                no_brand = False,
#                small_url = '',
#                medium_url = '',
#                large_url = '',
#                alt_small_url = '',
#                alt_medium_url = '',
#                alt_large_url = '',
                has_alternative = False,
                brand = brand,
                series = series,
#                indicia_publisher = models.ForeignKey(GCDIndiciaPublisher, null=True)
#                images = models.ManyToManyField(GCDImage, blank=True)
                publisher_name = 'Marvel',
                genre = 'History',
                product_name = 'Contentinal Union History',

            )

        #-----------------
        # Category
        #-----------------
        try:
            category1 = Category.objects.get(category_id=1)
            category2 = Category.objects.get(category_id=2)
            category3 = Category.objects.get(category_id=3)
            category4 = Category.objects.get(category_id=4)
            category5 = Category.objects.get(category_id=5)
            category6 = Category.objects.get(category_id=6)
            category7 = Category.objects.get(category_id=7)
        except Category.DoesNotExist:
            category1 = Category.objects.create(
                category_id=1,
                parent_id = 0,
                name = 'Comic',
            )
            category2 = Category.objects.create(
                category_id=2,
                parent_id = 1,
                name = 'Comic - Graphic Novel',
            )
            category3 = Category.objects.create(
                category_id=3,
                parent_id = 1,
                name = 'Comic - Golden Age',
            )
            category4 = Category.objects.create(
                category_id=4,
                parent_id = 1,
                name = 'Comic - Silver Age',
            )
            category5 = Category.objects.create(
                category_id=5,
                parent_id = 1,
                name = 'Comic - Bronze Age',
            )
            category6 = Category.objects.create(
                category_id=6,
                parent_id = 1,
                name = 'Comic - Modern',
            )
            category7 = Category.objects.create(
                category_id=7,
                parent_id = 1,
                name = 'Comic - Trade Paperbacks',
            )
        except Category.DoesNotExist:
            pass
    
        #------------------------
        # Unified Shipping Rates
        #------------------------
        try:
            shipping_rates = UnifiedShippingRate.objects.all()
            if len(shipping_rates) <= 0:
                UnifiedShippingRate.objects.create(
                    shipping_rate_id = 1,
                    country = 124, # Canada
                    comics_rate1 = 10,
                    comics_rate2 = 20,
                    comics_rate3 = 25,
                    comics_rate4 = 30,
                    comics_rate5 = 35,
                    comics_rate6 = 40,
                    comics_rate7 = 50,
                    comics_rate8 = 75,
                    comics_rate9 = 100,
                    comics_rate10 = 140,
                )
        except UnifiedShippingRate.DoesNotExist:
            pass

        #-----------------
        # Brand
        #-----------------
        try:
            brand1 = Brand.objects.get(brand_id=1)
        except Brand.DoesNotExist:
            brand1 = Brand.objects.create(
                brand_id=1,
                name='Galactic Alliance of Humankind',
            )

        #----------
        # Product
        #----------
        try:
            product1 = Product.objects.get(product_id=1)
        except Product.DoesNotExist:
            product1 = Product.objects.create(
                name='Ice Age Now',
                type=constants.COMIC_PRODUCT_TYPE,
                description='The sun enteres a catastrophic cooling phase and threatens humanity.',
                is_sold=False,
                is_listed=False,
                is_new=False,
                is_featured=False,
                sub_price=10.99,
                has_tax=True,
                tax_rate=0.13,
                tax_amount=1.00,
                sub_price_with_tax=12.99,
                discount=0.10,
                discount_type=1,
                price=13.99,
                cost=9.1,
                currency=124,
                language='EN',
#                image='',
#                image = models.ForeignKey(ImageUpload, null=True, blank=True,)
#                image_url = models.URLField(null=True, blank=True)
#                images = models.ManyToManyField(ImageUpload, blank=True, related_name='product_images')
                organization = organization,
                store = store,
                section = section1,
#                tags = None,
                brand = brand1,
                category = category1,
#                qrcode = models.ImageField(upload_to='qrcode', null=True, blank=True)
                is_qrcode_printed = False,
                has_no_shipping = False,
                is_unlimited = False,
            )


        #----------
        # Comics
        #----------
        try:
            comic1 = Comic.objects.get(comic_id=1)
        except Comic.DoesNotExist:
            comic1 = Comic.objects.create(
                comic_id = 1,
                is_cgc_rated = False,
                age = 1, # constants.AGE_OPTIONS
                cgc_rating = 10.0, # constants.CGC_RATING_OPTIONS
                label_colour = 'Yellow', # constants.LABEL_COLOUR_OPTIONS
                condition_rating = 10, # constants.CONDITION_RATING_RATING_OPTIONS
                is_canadian_priced_variant = False,
                is_variant_cover = False,
                is_retail_incentive_variant = False,
                is_newsstand_edition = False,
                organization = organization,
                product = product1,
                issue = issue,
            )

        #------------
        #TODO: Continue adding here ...
        
        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "ec_brands", "primarykey": "brand_id",},
#            {"tablename": "ec_comic_catalog_items", "primarykey": "catalog_comic_id",},
            {"tablename": "ec_comics", "primarykey": "comic_id",},
            {"tablename": "ec_customers", "primarykey": "customer_id",},
            {"tablename": "ec_employees", "primarykey": "employee_id",},
            {"tablename": "ec_categories", "primarykey": "category_id",},
            {"tablename": "ec_unified_shipping_rates", "primarykey": "shipping_rate_id",},
#            {"tablename": "ec_email_subscriptions", "primarykey": "subscription_id",},
            {"tablename": "ec_help_requests", "primarykey": "help_id",},
            {"tablename": "ec_image_uploads", "primarykey": "upload_id",},
            {"tablename": "ec_org_shipping_preferences", "primarykey": "shipping_pref_id",},
            {"tablename": "ec_org_shipping_rates", "primarykey": "shipping_rate_id",},
            {"tablename": "ec_organizations", "primarykey": "org_id",},
            {"tablename": "ec_products", "primarykey": "product_id",},
            {"tablename": "ec_promotions", "primarykey": "promotion_id",},
            {"tablename": "ec_pulllists", "primarykey": "pulllist_id",},
            {"tablename": "ec_pulllists_subscriptions", "primarykey": "subscription_id",},
            {"tablename": "ec_receipts", "primarykey": "receipt_id",},
            {"tablename": "ec_sections", "primarykey": "section_id",},
            {"tablename": "ec_stores", "primarykey": "store_id",},
            {"tablename": "ec_store_shipping_preferences", "primarykey": "shipping_pref_id",},
            {"tablename": "ec_store_shipping_rates", "primarykey": "shipping_rate_id",},
            {"tablename": "ec_tags", "primarykey": "tag_id",},
            {"tablename": "ec_wishlists", "primarykey": "wishlist_id",},
            # Grand Comics Database Tables
            {"tablename": "gcd_brands", "primarykey": "brand_id",},
            {"tablename": "gcd_brand_emblem_groups", "primarykey": "brand_emblem_group_id",},
            {"tablename": "gcd_brand_groups", "primarykey": "brand_group_id",},
            {"tablename": "gcd_brand_uses", "primarykey": "brand_use_id",},
            {"tablename": "gcd_countries", "primarykey": "country_id",},
            {"tablename": "gcd_images", "primarykey": "image_id",},
            {"tablename": "gcd_indicia_publishers", "primarykey": "indicia_publisher_id",},
            {"tablename": "gcd_issues", "primarykey": "issue_id",},
            {"tablename": "gcd_languages", "primarykey": "language_id",},
            {"tablename": "gcd_publishers", "primarykey": "publisher_id",},
            {"tablename": "gcd_series", "primarykey": "series_id",},
            {"tablename": "gcd_stories", "primarykey": "story_id",},
            {"tablename": "gcd_story_types", "primarykey": "story_type_id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)