import pandas as pd
import boto3
#from sagemaker import get_execution_role
#import dask.dataframe as dd
from pyathena import connect

class connect_athena():
    def __init__(self, client, bucket):
        self.client =client
        self.bucket = bucket
    def run_query(self, query, database, s3_output):
        """
        s3_output -> 'output_sql'
        """


        full_s3_output = 's3://{0}/{1}/'.format(self.bucket, s3_output)

        client = self.client['athena']
        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
                },
            ResultConfiguration={
            'OutputLocation': full_s3_output,
            }
        )
        print('Execution ID: ' + response['QueryExecutionId'])
        return response

    def query_to_df(self, query, s3_output, ):
        """
        s3_output -> 'output_sql'
        """


        s3_output = 's3://{}/{}/'.format(self.bucket, s3_output)

        key, secret_ = self.client['s3']

        conn = connect(aws_access_key_id=key,
               aws_secret_access_key=secret_,
               s3_staging_dir=s3_output,
               region_name=self.region)

        df = pd.read_sql(query, conn)

        return df