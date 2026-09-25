from django.test import TestCase
from django.urls import reverse


class RoutesTests(TestCase):
    def test_home_and_static(self):
        standard_paths = [
            "/",
            "/about/",
            "/faq/",
            "/help/",
            "/help/viz/",
            "/history/",
            "/publications/",
            "/roadmap/",
            "/termsOfUse/",
            "/status/",
            "/brown/",
        ]
        for path in standard_paths:
            with self.subTest(path=path):
                resp = self.client.get(path)
                self.assertEqual(resp.status_code, 200)

        for path in [
            "/side_stuff/brown_classic/",
            "/side_stuff/brown_classic/joe/",
        ]:
            with self.subTest(path=path):
                resp = self.client.get(path)
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.headers.get("Location", "").startswith(reverse("search")))

    def test_display_and_visualizations(self):
        base_id = "n1"
        paths = [
            "/display/",
            f"/display/{base_id}/",
            f"/display/{base_id}/publications/",
            f"/display/{base_id}/viz/",
            f"/display/{base_id}/viz/coauthor/",
            f"/display/{base_id}/viz/coauthor_treemap/",
            f"/display/{base_id}/viz/collab/",
            f"/display/{base_id}/viz/publications/",
            f"/display/{base_id}/viz/research/",
        ]
        for path in paths:
            with self.subTest(path=path):
                resp = self.client.get(path)
                self.assertEqual(resp.status_code, 200)

    def test_display_json_format_param(self):
        resp = self.client.get("/display/abc/?format=json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/json")
        self.assertEqual(resp.json(), {"id": "abc"})

    def test_reports(self):
        self.assertEqual(self.client.get("/reports/subject-lib/").status_code, 200)
        self.assertEqual(self.client.get("/reports/subject-lib/abc/").status_code, 200)

    def test_search(self):
        self.assertEqual(self.client.get("/search/").status_code, 200)
        self.assertEqual(self.client.get("/search/advanced/").status_code, 200)
        # facets returns JSON
        resp = self.client.get("/search_facets/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/json")
        self.assertIn("facets", resp.json())

    def test_legacy_people_organizations(self):
        self.assertEqual(self.client.get("/people/").status_code, 200)
        self.assertEqual(self.client.get("/ous/").status_code, 200)

    def test_file_old_image_returns_404(self):
        resp = self.client.get("/file/1/foo.png/")
        self.assertEqual(resp.status_code, 404)

    def test_individual_redirect(self):
        resp = self.client.get("/individual/n123/")
        self.assertEqual(resp.status_code, 200)

    def test_individual_export_json_single(self):
        resp = self.client.get("/individual/n123.json/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/json")
        self.assertEqual(resp.json().get("id"), "n123")
        self.assertEqual(resp.json().get("format"), "json")

    def test_individual_export_json_double(self):
        resp = self.client.get("/individual/n123/n123.json/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/json")
        self.assertEqual(resp.json().get("id"), "n123")
        self.assertEqual(resp.json().get("id2"), "n123")
        self.assertEqual(resp.json().get("format"), "json")

    def test_edit_fast_search_json(self):
        resp = self.client.get("/edit/fast/search/?q=foo")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/json")
        self.assertEqual(resp.json().get("query"), "foo")
        self.assertIsInstance(resp.json().get("results"), list)
