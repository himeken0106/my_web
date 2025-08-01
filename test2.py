from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

# boto3で認証情報取得（環境変数や aws configure の情報を使う）
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

region = 'us-west-2'
service = 'aoss'  # OpenSearch Serverless用サービス名

auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token
)

#host = 'znhxqss7jbvjmbcf4tzi.us-west-2.aoss.amazonaws.com'  # あなたのOpenSearch Serverlessエンドポイント
host = '7zfwbb45303vdhztt4ah.us-west-2.aoss.amazonaws.com'
#index_name = 'kb-01k1d2natkm6jz660373'
index_name = 'bedrock-knowledge-base-default-index'

client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30
)

query = {
    "size": 20,
    "query": {
        "match_all": {}
    }
}

try:
    res = client.search(index=index_name, body=query)
    for hit in res['hits']['hits']:
        print("======Chunk content:")
        print(hit['_source'].get('AMAZON_BEDROCK_TEXT_CHUNK'))
except Exception as e:
    print("Error:", e)
