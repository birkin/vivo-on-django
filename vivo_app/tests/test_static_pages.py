"""Regression tests for static home-derived pages."""

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class StaticPageTests(TestCase):
    """Ensure key static pages render expected content and shared search box."""

    def test_static_pages_render_with_shared_search_box(self) -> None:
        pages = [
            (reverse("about"), "About Researchers@Brown"),
            (reverse("help"), "Researchers@Brown Help"),
            (reverse("faq"), "Frequently Asked Questions"),
            (reverse("history"), "VIVO History and Implementation"),
            (reverse("publications"), "Managing Your Publications"),
            (reverse("roadmap"), "Improvements and Roadmap"),
            (reverse("terms"), "Terms of Use"),
            (reverse("help_viz"), "Visualize it!"),
            (reverse("brown"), "Brown University"),
        ]
        for url, heading in pages:
            with self.subTest(url=url):
                response: HttpResponse = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, heading)
                self.assertContains(response, 'id="sticky-nav"')

    def test_brown_classic_redirects_to_search(self) -> None:
        response: HttpResponse = self.client.get(reverse("brown_classic"), {"name": "Jane_Doe"})
        expected_location: str = f"{reverse('search')}?q=Jane+Doe"
        self.assertRedirects(response, expected_location, fetch_redirect_response=False)

    def test_brown_classic_named_path_redirects(self) -> None:
        response: HttpResponse = self.client.get(reverse("brown_classic_named", args=["John_Doe"]))
        expected_location: str = f"{reverse('search')}?q=John+Doe"
        self.assertRedirects(response, expected_location, fetch_redirect_response=False)
