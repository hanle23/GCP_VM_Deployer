from deployable import access, deploy_instance, student_data
import unittest

compute, service = access.authorize()
assert compute != None
assert service != None


class DeployTestCase(unittest.TestCase):
    def test_list_projects(self):
        projects = deploy_instance.list_projects(service)
        self.assertIsInstance(projects, list)
        self.assertIsNotNone(projects)

    def test_choose_zone(self):
        zone = deploy_instance.choose_zone(compute)
        self.assertTrue(zone.startswith("us-east"))

    def test_namevalid(self):
        name = "bda-123456789"
        self.assertTrue(deploy_instance.namevalid(name))

    def test_get_student_txt(self):
        student_list = student_data.data.get_student_id_txt("test_file.txt")
        self.assertTrue(student_list)
        self.assertIsNotNone(student_list)

    def test_create_instance(self):
        zone = deploy_instance.choose_zone(compute)
        projects = ["testing-project-322415", "testing-project-322416"]
        for project in projects:
            deploy_instance.create_instance(compute, project, zone)
            names = deploy_instance.get_instance_names(compute, project)
            self.assertIn("bda-db-1", names)
            deploy_instance.delete_instance(compute, project, zone)


if __name__ == '__main__':
    unittest.main(verbosity=2)
