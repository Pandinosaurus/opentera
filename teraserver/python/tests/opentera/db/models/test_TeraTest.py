from tests.opentera.db.models.BaseModelsTest import BaseModelsTest


class TeraTestTest(BaseModelsTest):

    def test_defaults(self):
        with self._flask_app.app_context():
            pass
