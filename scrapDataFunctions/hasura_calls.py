import aiohttp
from aiohttp import ClientConnectionError, ClientError
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from requests.exceptions import HTTPError
from tenacity import retry, stop_after_attempt, wait_exponential

transport = AIOHTTPTransport(
    url='https://engaged-puma-42.hasura.app/v1/graphql',
    headers={'content-type': 'application/json',
             'x-hasura-admin-secret': 'ahFsQwjyqg2UFjVGT3L786keKu7089kDC856PmO5486BV0sp5U3aHqL0FuB40Slw'}
)
client = Client(transport=transport, fetch_schema_from_transport=True)


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

        param = {"employer_name": emp_name, "employer_noc_id": str(noc_id), "employer_province": job_location_province,
                 "employer_region": job, "employer_url": emp_url, "employer_email_address": email,
                 "latitude": str(latitude),
                 "longitude": str(longitude), "employer_address": job_location_address}

        result = await client.execute_async(query, variable_values=param)
        employer_id = result['insert_employers']['returning'][0]['id']

        return employer_id
    except (HTTPError, TimeoutError, ClientConnectionError, ClientError) as e:
        print("Error occurred while inserting employer info: " + e)
        raise e


@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def insert_job_basic_info(e_id, title, base_salary, work_hour, location, posted_at):
    try:
        query = gql(
            """
            mutation insert_job_basic_info($employer_id: bigint = "", $job_base_salary: String = "", $job_location: String = "", $job_posted_at: timestamp = "", $job_title: String = "", $job_work_hours: String = "") {
              insert_job_basic_information(objects: {employer_id: $employer_id, job_base_salary: $job_base_salary, job_location: $job_location, job_posted_at: $job_posted_at, job_title: $job_title, job_work_hours: $job_work_hours}) {
                returning {
                  id
                }
              }
            }

            """
        )
        param = {"employer_id": e_id, "job_base_salary": base_salary, "job_location": location,
                 "job_posted_at": posted_at, "job_title": title, "job_work_hours": work_hour}

        result = await client.execute_async(query, variable_values=param)

        job_id = result['insert_job_basic_information']['returning'][0]['id']
        return job_id

    except (HTTPError, TimeoutError, ClientConnectionError, ClientError) as e:
        print("Error occurred while inserting employer info: " + e)
        raise e



@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def insert_job_details_info(j_id, employment, commitment, start_date, benefits, vacancy, job_type):
    try:
        query_1 = gql(
            """
            mutation insert_job_details($job_basic_info_id: bigint = "", $job_benefits: String = "", $job_type: String = "", $special_commitment: String = "", $start_date: String = "", $term_of_employment: String = "", $total_vacancies: String = "") {
              insert_job_details(objects: {job_basic_info_id: $job_basic_info_id, job_benefits: $job_benefits, job_type: $job_type, special_commitment: $special_commitment, start_date: $start_date, term_of_employment: $term_of_employment, total_vacancies: $total_vacancies}) {
                returning {
                  id
                }
              }
            }

            """
        )
        param_1 = {"job_basic_info_id": j_id, "job_benefits": benefits, "job_type": job_type,
                   "special_commitment": commitment, "start_date": start_date, "term_of_employment": employment,
                   "total_vacancies": vacancy}

        result = await client.execute_async(query_1, variable_values=param_1)
        job_details_id = result['insert_job_details']['returning'][0]['id']

        return job_details_id

    except (HTTPError, TimeoutError, ClientConnectionError, ClientError) as e:
        print("Error occurred while inserting employer info: " + e)
        raise e



@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def insert_job_additional_info(j_id, data):
    try:
        query_1 = gql(
            """
            mutation insert_job_additional($job_additional_info_content: String = "", $job_additional_info_sub_topic: String = "", $job_additional_info_topic: String = "", $job_basic_info_id: bigint = "") {
              insert_job_additional_details(objects: {job_additional_info_content: $job_additional_info_content, job_additional_info_sub_topic: $job_additional_info_sub_topic, job_additional_info_topic: $job_additional_info_topic, job_basic_info_id: $job_basic_info_id}) {
                returning {
                  id
                }
              }
            }

            """
        )
        param_1 = {"job_additional_info_content": data[2], "job_additional_info_sub_topic": data[1],
                 "job_additional_info_topic": data[0], "job_basic_info_id": j_id}

        result = await client.execute_async(query_1, variable_values=param_1)

        return result

    except (HTTPError, TimeoutError, ClientConnectionError, ClientError) as e:
        print("Error occurred while inserting employer info: " + e)
        raise e
