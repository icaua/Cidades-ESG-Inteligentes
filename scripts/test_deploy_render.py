import io
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from urllib.parse import urlsplit, parse_qs
from deploy_render import trigger


class RenderHookTests(unittest.TestCase):
    hook = "https://api.render.com/deploy/srv-test?key=test-only"
    image = "ghcr.io/icaua/cidades-esg-inteligentes@sha256:" + "a" * 64

    def test_digest_and_deploy_id(self):
        response = io.BytesIO(b'{"deploy":{"id":"dep-example"}}')
        response.status = 200
        with patch("deploy_render.urlopen", return_value=response) as request:
            result = trigger(self.hook, self.image)
        self.assertEqual(result["deploy_id"], "dep-example")
        query = parse_qs(urlsplit(request.call_args.args[0].full_url).query)
        self.assertEqual(query["imgURL"], [self.image])

    def test_mutable_image_is_rejected(self):
        with self.assertRaises(ValueError):
            trigger(self.hook, "ghcr.io/icaua/cidades-esg-inteligentes:latest")

    def test_hook_without_key_is_rejected(self):
        with self.assertRaises(ValueError):
            trigger("https://api.render.com/deploy/srv-test", self.image)

    def test_secret_not_exposed_on_error(self):
        with patch("deploy_render.urlopen", side_effect=HTTPError(self.hook, 401, "error", {}, None)):
            with self.assertRaises(RuntimeError) as result:
                trigger(self.hook, self.image)
        self.assertNotIn("test-only", str(result.exception))
        self.assertTrue(result.exception.__suppress_context__)
