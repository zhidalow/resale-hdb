import requests
import json
import time

class IngestDatasets():
    def __init__(
        self,
        apiKey:str =None,
        rate_limit:int =24
    ):
        '''
        Args:
        apiKey: data.gov apiKey if any. will pass in to avoid downtime for rest api ingestion
        rate_limit: max number of requests allowed to be made per minute
        '''

        self.apiKey = apiKey
        self.headers = None
        if apiKey:
            self.headers = {"x-api-key": self.apiKey}
        self.rate_limit=rate_limit
        self.last_request_time = 0

    def rate_limit_wait(
        self
    ):
        # Implement rate limiting
        min_interval = 60.0 / self.rate_limit # seconds between requests
        elapsed = time.time() - self.last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()
 
    def make_get_request(
        self,
        url: str,
        body: dict = None
    ):

        self.rate_limit_wait()
        if body:
            body = json.dumps(body)
        response = requests.get(
            url,
            headers=self.headers,
            data=body
        )

        response.raise_for_status()

        return response

    def download_dataset(
        self,
        dataset_id:str,
        filename:str
    ):

        # send download initiate request first 
        download_request = self.make_get_request(url=f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/initiate-download")
        print(f"Download request sent for dataset_id {dataset_id}.")

        for attempt in range(3):
        # poll for completion
            poll_for_completion = self.make_get_request(url=f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download")
            poll_for_completion = poll_for_completion.json()
            if poll_for_completion["data"]["status"] == "DOWNLOAD_SUCCESS":
                print(f"dataset_id {dataset_id} ready for download.")
                break
            print(f"Try {attempt+1}, dataset not ready, polling again in 5s...")
            time.sleep(5)

        # download dataset
        response = self.make_get_request(url=poll_for_completion["data"]["url"])
        save_location = f"raw/{filename}.csv"

        with open(save_location, "wb") as f:
            f.write(response.content)
        print(f"======Dataset {dataset_id} saved to {save_location}.======")