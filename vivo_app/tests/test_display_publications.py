from django.test import TestCase


class DisplayPublicationsTests(TestCase):
    def test_publications_json_people(self):
        resp = self.client.get("/display/n7/publications/?format=json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/json")
        data = resp.json()
        self.assertEqual(data.get("id"), "n7")
        self.assertEqual(data.get("type"), "PEOPLE")
        pubs = data.get("publications")
        self.assertIsInstance(pubs, list)
        self.assertGreaterEqual(len(pubs), 2)
        self.assertIn("Sample Publication 1 for n7", pubs[0].get("title", ""))

    def test_publications_html_people(self):
        resp = self.client.get("/display/n7/publications/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Publications", resp.content)
        self.assertIn(b"Sample Publication", resp.content)

    def test_publications_json_org(self):
        resp = self.client.get("/display/org123/publications/?format=json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("id"), "org123")
        self.assertEqual(data.get("type"), "ORGANIZATION")
        self.assertIsInstance(data.get("publications"), list)

    def test_publications_json_unknown(self):
        resp = self.client.get("/display/x999/publications/?format=json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("id"), "x999")
        # unknown type returns None
        self.assertIsNone(data.get("type"))
        self.assertIsInstance(data.get("publications"), list)
        self.assertEqual(len(data.get("publications")), 0)

    def test_publications_html_unknown(self):
        resp = self.client.get("/display/x999/publications/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"No publications yet.", resp.content)
