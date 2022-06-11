# importing standard module
import glob
from uuid import uuid4
from pprint import pprint as print
from random import randint
import sys
import timeit
import traceback
import logging

# installed  package
from dotenv import dotenv_values
import lh3.api

client = lh3.api.Client()
import pandas as pd

import ipinfo


config = dotenv_values(".env")
access_token = config.get('ipinfokey', "no_api_key_found")
handler = ipinfo.getHandler(access_token)

# excecution time
start = timeit.default_timer()

# Logger
logging.basicConfig(
    filename="./error.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


# ==================================================================
# ==================================================================
# Functions


def practiceQueues(chat):
    return chat["queue"] not in (
        "practice-webinars",
        "practice-webinars-txt",
        "practice-webinars-fr",
    )


def isChat(chat):
    return chat["protocol"] != "twilio"


def find_geolocation_from_ip_addresses(ip_unique):
    print("Starting retrieving geolocation")
    metadata = list()
    counter = 0
    for ip in ip_unique:
        try:
            if ";" in ip:
                raise ValueError("Represents a hidden bug, catch this")
            print("Total chats left: {0}".format(len(ip_unique) - counter))
            counter = counter + 1
            details = handler.getDetails(ip)
            try:
                city = details.city
            except:
                city = None
            try:
                country = details.country
            except:
                country = None
            try:
                latitude = details.latitude
            except:
                latitude = None
            try:
                longitude = details.longitude
            except:
                longitude = None
            try:
                timezone = details.timezone
            except:
                timezone = None
            try:
                postal = details.postal
            except:
                postal = None
            try:
                locations = details.loc
            except:
                locations = None
            metadata.append(
                {
                    "uuid": str(uuid4())[0:8],
                    "ip": ip,
                    "city": city,
                    "country": country,
                    "locations": locations,
                    "latitude": latitude,
                    "longitude": longitude,
                    "timezone": timezone,
                    "postal": postal,
                }
            )
        except Exception as err:
            print("Error for this IP {0}".format(ip))
            traceback.print_exc()
            logger.error(err)
            pass
    new_df = pd.DataFrame(metadata)
    new_df.to_excel("geolocation_for_unique_ip_fall_2019-2021.xlsx", index=False)
    return new_df


def importing_chats_metadata(query=None):
    chats = query
    chats = list(filter(practiceQueues, chats))
    chats = list(filter(isChat, chats))
    data = pd.DataFrame(chats)
    print(len(chats))
    return data


def download_chats_metadata_in_df():
    data2019 = importing_chats_metadata(
        query=client.chats().list_day(2019, 9, 9, "2019-12-06")
    )
    data2020 = importing_chats_metadata(
        query=client.chats().list_day(2020, 9, 8, "2020-12-11")
    )
    data2021 = importing_chats_metadata(
        query=client.chats().list_day(2021, 9, 7, "2021-12-10")
    )

    print("Contatenating DataFrames")
    df = pd.concat([data2019, data2020, data2021], ignore_index=True)

    # change column format to timestamps
    df["started"] = df["started"].astype("datetime64[ns]")
    df["year"] = df["started"].dt.year

    # safe backup
    df.to_excel("chats_fall_2019-2021.xlsx", index=False)
    return df


def find_unique_ip_addresses(df):
    # Unique IP addresses
    df_ip = pd.DataFrame(df.ip.unique(), columns=["ip"])
    ip_unique = df.ip.unique()
    return ip_unique


def find_execution_time():
    stop = timeit.default_timer()
    total_time = stop - start

    # output running time in a nice format.
    mins, secs = divmod(total_time, 60)
    hours, mins = divmod(mins, 60)

    sys.stdout.write("Total running time: %d:%d:%d.\n" % (hours, mins, secs))


if __name__ == "__main__":
    df = download_chats_metadata_in_df()
    ip_unique = find_unique_ip_addresses(df)
    ip_df = find_geolocation_from_ip_addresses(ip_unique)
    # MERGE df and ip_df ON "ip" field
    print("Merging DataFrame")
    final_df = pd.merge(df, ip_df, on="ip", how="outer")
    cf = pd.read_excel("list_of_countries.xlsx")
    final = pd.merge(final_df, cf, on="country", how="left")
    final_df.to_excel("research_data_fall_2019-2021.xlsx", index=False)
    print(final_df.size)
    find_execution_time()
