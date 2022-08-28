from main import (
    practiceQueues,
    isChat,
    importing_chats_metadata,
    download_chats_metadata_in_df,
    find_geolocation_from_ip_addresses,
    handler,
    find_unique_ip_addresses,
)
from vr_ip_chat_research import *
import pytest
import lh3.api

client = lh3.api.Client()

import ipinfo

access_token = "9c2fc435da6c9cs"
handler = ipinfo.getHandler(access_token)

import glob
import os


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method."""
    files = glob.glob("./*.xlsx")
    for i in files:
        os.remove(i)


class TestResearchPoster:
    @pytest.fixture(autouse=True, scope="class")
    def state(self):
        return {"chats": client.chats().list_day(2019, 9, 9, "2019-09-10")}

    @pytest.fixture(autouse=True, scope="class")
    def research(self):
        return {"df": download_chats_metadata_in_df()}

    def test_if_number_of_chats_is_390_for_these_two_days(self, state):
        assert len(state["chats"]) == 360

    def test_the_function_practiceQueues(self, state):
        chats = state["chats"]
        chats_without_practice_queue = list(filter(practiceQueues, chats))
        assert len(chats_without_practice_queue) == 359

    def test_the_function_isChat(self, state):
        chats = state["chats"]
        chats = list(filter(practiceQueues, chats))
        chats = list(filter(isChat, chats))
        assert len(chats) == 341

    def test_the_function_download_chats_metadata_in_df(self, research):
        assert len(research["df"]) == 47775

    def test_the_function_find_unique_ip_addresses(self, research):
        ip_unique = find_unique_ip_addresses(research["df"])
        assert len(ip_unique) == 29817

    def test_find_the_function_geolocation_from_ip_addresses(self, research):
        ip_unique = find_unique_ip_addresses(research["df"])
        details = handler.getDetails(ip_unique[256])
        assert details.country == "CA"
        assert details.city == "Niagara Falls"
        assert details.postal == "L2H"

    def test_find_the_function_geolocation_from_ip_addresses_outside_canada(
        self, research
    ):
        ip_unique = find_unique_ip_addresses(research["df"])
        details = handler.getDetails(ip_unique[29389])
        assert details.country == "NA"

    def test_find_the_function_geolocation_from_ip_addresses_with_error(self, research):
        ip_unique = find_unique_ip_addresses(research["df"])
        details = handler.getDetails(ip_unique[6299])
        assert details.country == "ZW"
        assert details.city == "Harare"

    def test_exception(self, research):
        with pytest.raises(Exception) as e_info:
            x = 1 / 0
            assert details.postal == None
