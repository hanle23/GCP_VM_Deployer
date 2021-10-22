import access
import unittest
from deploy_instance import *
import student_data as data


compute, service = access.authorize()
assert compute != None
assert service != None


class DeployTestCase(unittest.TestCase):
    def test_list_projects(self):
        projects = list_projects(service)
        self.assertIsInstance(projects, list)
        self.assertIsNotNone(projects)

    def test_choose_zone(self):
        zone = choose_zone(compute)
        self.assertTrue(zone.startswith("us-east"))

    def test_namevalid(self):
        name = "bda-123456789"
        self.assertTrue(namevalid(name))

    def test_get_student_txt(self):
        student_list = data.get_student_id_txt("test_file.txt")
        self.assertTrue(student_list)
        self.assertIsNotNone(student_list)

    def test_create_instance(self):
        zone = choose_zone(compute)
        projects = ["testing-project-322415", "testing-project-322416"]
        for project in projects:
            create_instance(compute, project, zone)
            names = get_instance_names(compute, project)
            self.assertIn("bda-db-1", names)
            delete_instance(compute, project, zone)


if __name__ == '__main__':
    unittest.main(verbosity=2)
