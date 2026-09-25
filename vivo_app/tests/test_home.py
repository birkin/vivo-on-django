"""
Home page tests for Django VIVO app.

Verifies that the homepage renders and includes key structural markers and links
that we aim to keep aligned with production.
"""

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    """Tests homepage rendering and primary elements."""

    def test_homepage_renders_ok(self):
        """
        Returns 200 and contains primary sections and headings.
        """
        resp: HttpResponse = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        # Key headings/markers
        self.assertContains(resp, "Welcome to Researchers@Brown")
        self.assertContains(resp, "Recent faculty books")
        self.assertContains(resp, "Search for a Researcher")
        self.assertContains(resp, "Did You Know?")
        self.assertContains(resp, "Get a Brown ORCID Identifier!")

    def test_homepage_links(self):
        """
        Contains expected navigation and quick link URLs.
        """
        resp: HttpResponse = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

        # Manage profile link visible on home page
        self.assertContains(resp, "Manage your profile")

        # Search form target
        self.assertContains(resp, f'action="{reverse("search")}"')

        # Advanced search link text and URL
        self.assertContains(resp, "Advanced search&hellip;")
        self.assertContains(resp, reverse("advanced_search"))

        # Quick links
        self.assertContains(resp, reverse("people"))
        self.assertContains(resp, reverse("organizations"))
        self.assertContains(resp, reverse("publications"))

        # Footer
        self.assertContains(resp, reverse("terms"))
        self.assertContains(resp, "vivoweb.org")

    def test_homepage_includes_carousel_markup(self):
        """
        Book carousel renders data-src attributes for lazy loading and anchors.
        """
        resp: HttpResponse = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="books-carousel"')
        self.assertContains(resp, 'class="book-cover"')
        self.assertContains(resp, 'data-src="/static/images/vivo_blank_profile.jpg"')

    def test_alias_parameter_redirects_to_search(self):
        """
        Alias parameter redirects to search with the formatted query.
        """
        response: HttpResponse = self.client.get("/", {"alias": "Nicole_Nugent"})
        expected_location: str = f"{reverse('search')}?q=Nicole+Nugent"
        self.assertRedirects(response, expected_location, fetch_redirect_response=False)
