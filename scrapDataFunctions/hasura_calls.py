import aiohttp
from aiohttp import ClientConnectionError, ClientError
from gql import gql
from requests.exceptions import HTTPError
from tenacity import retry, stop_after_attempt, wait_exponential

headers = {'content-type': 'application/json',
             'x-hasura-admin-secret': 'ahFsQwjyqg2UFjVGT3L786keKu7089kDC856PmO5486BV0sp5U3aHqL0FuB40Slw'}

hasura_url = 'https://engaged-puma-42.hasura.app/v1/graphql'


@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def insert_employer_info(emp_name, noc_id, job_location_province, job, emp_url, email, latitude, longitude,
                               job_location_address):
    try:
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

        async with aiohttp.ClientSession() as session:
            async with session.post(url=hasura_url,headers=headers, json={'query': str(query), 'variables': param}) as response:
                status_code = response.status
                result = await response.json()
        print(status_code)
        print(result)
        # If status code = 200 then print("Employer data inserted") run and check if its int or string
        # de-seralize result and return id of employer

        return param
    except (HTTPError, TimeoutError, ClientConnectionError, ClientError) as e:
        print("Error occurred while inserting employer info: " + e)
        raise e
