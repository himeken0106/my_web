from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

# boto3セッション作成、認証情報取得
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

region = 'us-west-2'
service = 'aoss'

auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token
)

#host = 'znhxqss7jbvjmbcf4tzi.us-west-2.aoss.amazonaws.com'
host = '7zfwbb45303vdhztt4ah.us-west-2.aoss.amazonaws.com'

client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=10
)

try:
    indices = client.cat.indices(format="json")
    print("Available indices:")
    for idx in indices:
        print(f" - {idx['index']}")
except Exception as e:
    print("Error:", e)
