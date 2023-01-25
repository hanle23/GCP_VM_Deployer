from context import deployable
import unittest

compute, service = deployable.authorize()
assert compute != None
assert service != None


class DeployTestCase(unittest.TestCase):
    def test_list_projects(self):
        projects = deployable.list_projects(service)
        self.assertIsInstance(projects, list)
        self.assertIsNotNone(projects)

    def test_choose_zone(self):
        zone = deployable.choose_zone(compute)
        self.assertTrue(zone.startswith("us-east"))

    def test_isValid(self):
        name = "bda-123456789"
        self.assertTrue(deployable.isValid(name))

    def test_get_student_txt(self):
        student_list = deployable.get_student_id_txt("test_file.txt")
        self.assertNotEqual(0, len(student_list))
        self.assertIsNotNone(student_list)

    def test_create_instance(self):
        zone = deployable.choose_zone(compute)
        projects = ["testing-project-322415", "testing-project-322416"]
        for project in projects:
            deployable.create_instance(compute, project, zone)
            names = deployable.get_instance_names(compute, project)
            self.assertIn("bda-db-1", names)
            deployable.delete_instance(compute, project, zone)


if __name__ == '__main__':
    unittest.main(verbosity=2)
