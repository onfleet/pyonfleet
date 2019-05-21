import sys
sys.path.append("../onfleet")
import onfleet

import os
import unittest
import re
import json
import requests
from datetime import datetime, timedelta

class TestOnfleet(unittest.TestCase):
    def setUp(self):
        # Input your API key to enable test
        self.api_key = ""
        self.api = onfleet.Onfleet(api_key=self.api_key)

    def test_authenticate(self):
        auth_result = self.api.auth_test()
        org_result = self.api.organization.list()
        match = re.search(r"[a-zA-Z\d]{24}", auth_result["message"])
        self.assertTrue(match.group(0) == org_result["id"])

    def test_datatype(self):
        admins_list = self.api.administrators.list()
        self.assertTrue(isinstance(admins_list, list))
        workers_list = self.api.workers.list()
        self.assertTrue(isinstance(workers_list, list))
        hubs_list = self.api.hubs.list()
        self.assertTrue(isinstance(hubs_list, list))
        teams_list = self.api.teams.list()
        self.assertTrue(isinstance(teams_list, list))
        webhooks_list = self.api.webhooks.list()
        self.assertTrue(isinstance(webhooks_list, list))

    def test_integrated_functions(self):
        # In this test, we test the create, list, update, and delete functions
        old_admin_list_length = len(self.api.administrators.list())
        admin_data = {"name":"Onfleet Tester","email":"ot@onf.lt"}
        new_admin = self.api.administrators.create(body=admin_data)
        new_admin_id = new_admin["id"]
        new_admin_list_length = len(self.api.administrators.list())
        # Length of admin list should increase by 1
        self.assertTrue(old_admin_list_length + 1 == new_admin_list_length)
        updated_result = self.api.administrators.update(id=new_admin_id, body={"name": "Onfleet Testing - Please delete"})
        # Admin name should be updated
        self.assertTrue(updated_result["name"] == "Onfleet Testing - Please delete")
        deletion_result = self.api.administrators.deleteOne(id=new_admin_id)
        deleted_admin_list_length = len(self.api.administrators.list())
        # Deletion should return 200, admin list length should decrease by 1
        self.assertTrue(deletion_result == 200)
        self.assertTrue(deleted_admin_list_length == old_admin_list_length)

    def test_worker_schedule(self):
        worker_list = self.api.workers.list()
        no_match = True
        # Check if there's a duplicate key in worker phone number
        for worker in worker_list:
            if (worker["phone"] == "+16173428853"):
                worker_id = worker["id"]
                no_match = False
            # Get a team ID
            team_id = worker["teams"][0]
        # Create a worker with the example phone number
        if (no_match):
            new_worker_data = {"name":"A Swartz","phone":"617-342-8853","teams": [team_id], "vehicle":{"type":"CAR","description":"Tesla Model 3","licensePlate":"FKNS9A","color":"purple"}}
            new_worker = self.api.workers.create(body=new_worker_data)
            worker_id = new_worker["id"]

        # Create a schedule that is 365 days later in the future
        original_schedule = self.api.workers.getSchedule(id=worker_id)
        original_length_of_schedule = len(original_schedule["entries"])
        future = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        new_schedule_data = {
            "entries":[
                {
                    "date":future,
                    "shifts":[[1500213600000,1500249600000]],
                    "timezone":"America/Los_Angeles"
                }
            ]
        }
        new_schedule_result = self.api.workers.updateSchedule(id=worker_id, body=new_schedule_data)
        # Check that the schedule was updated
        self.assertTrue(len(new_schedule_result) - 1 == original_length_of_schedule)
        reverted_schedule = self.api.workers.updateSchedule(id=worker_id, body=original_schedule)
        # Check that the schedule was reverted
        self.assertTrue(original_length_of_schedule == len(reverted_schedule))

    def test_find_and_query_parameters(self):
        data = {"name":"Boris Foster"}
        search_result = (self.api.recipients.getOne(search=data))
        # Create the recipient if not exist
        if ("id" not in search_result):
            new_recipient_data = {"name":"Boris Foster","phone":"+16505551133","notes":"Always orders our GSC special", "skipPhoneNumberValidation":"true"}
            new_recipient = self.api.recipients.create(body=new_recipient_data)
            recipient_id = new_recipient["id"]
        else:
            recipient_id = search_result["id"]
        search_result_with_query = self.api.recipients.getOne(search=data, queryParams={"skipPhoneNumberValidation":"true"})
        self.assertTrue(search_result_with_query["id"] == recipient_id)


if (__name__ == '__main__'):
    unittest.main()