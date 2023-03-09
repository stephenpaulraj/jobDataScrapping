import json
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import log as requests_logger

transport = AIOHTTPTransport(
    url='https://engaged-puma-42.hasura.app/v1/graphql',
    headers={'content-type': 'application/json',
             'x-hasura-admin-secret': 'ahFsQwjyqg2UFjVGT3L786keKu7089kDC856PmO5486BV0sp5U3aHqL0FuB40Slw'}
)

client = Client(transport=transport, fetch_schema_from_transport=True)


async def insert_employer_info(emp_name, noc_id, job_location_province, job, emp_url, email, latitude, longitude,
                               job_location_address):
    query = gql(
        """
        mutation insertEmployerInfo($employer_name: String = "", $employer_noc_id: bigint = "", $employer_province: String = "", $employer_region: String = "", $employer_url: String = "", $employer_email_address: String = "", $latitude: float8 = "", $longitude: float8 = "", $employer_address: String = "") {
        insert_employers(objects: {employer_name: $employer_name, employer_noc_id: $employer_noc_id, employer_province: $employer_province, employer_region: $employer_region, employer_url: $employer_url, employer_email_address: $employer_email_address, latitude: $latitude, longitude: $longitude, employer_address: $employer_address}) {
        returning {
              id
            }
          }
        }
        """
    )

    param = {"employer_name": emp_name, "employer_noc_id": noc_id, "employer_province": job_location_province,
             "employer_region": job, "employer_url": emp_url, "employer_email_address": email, "latitude": latitude,
             "longitude": longitude, "employer_address": job_location_address}

    print(param)

    # result = await client.execute_async(query, variable_values=param)
    # print(result)
    #
    # employer_id = result['insert_employers']['returning'][0]['id']
    # print(employer_id)

    return param
