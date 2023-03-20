from asyncio import sleep
from context import deployable
from googleapiclient import errors
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

    def test_name_valid(self):
        name = "bda-123456789"
        self.assertTrue(deployable.name_valid(name))

    def test_get_student_txt(self):
        student_list = deployable.get_student_id_txt("test_file.txt")
        self.assertNotEqual(0, len(student_list))
        self.assertIsNotNone(student_list)

    def test_create_instance(self):
        zone = deployable.choose_zone(compute)
        projects = ["testing-project-322415", "testing-project-322416"]
        for project in projects:
            deployable.create_static_ip(compute, project, zone)
            response = deployable.get_static_ip(compute, project, zone)
            deployable.create_instance(
                compute, project, zone, response.get('address'))
            names = deployable.get_instance_names(compute, project)
            self.assertIn("bda-db-1", names)
            deployable.delete_instance(compute, project, zone)
            deployable.delete_static_IP(compute, project, zone)

    def test_create_static_ip(self):
        zone = deployable.choose_zone(compute)
        projects = ["testing-project-322415", "testing-project-322416"]
        for project in projects:
            deployable.create_static_ip(compute, project, zone)
            try:
                response = deployable.get_static_ip(compute, project, zone)
            except errors.HttpError:
                assert False, response.get('message')
            deployable.delete_static_IP(compute, project, zone)


if __name__ == '__main__':
    unittest.main(verbosity=2)
