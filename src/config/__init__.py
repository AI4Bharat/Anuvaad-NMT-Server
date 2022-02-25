from .kafka_topics import kafka_topic, bootstrap_server_boolean, bootstrap_server
import os

## app configuration variables
DEBUG = False
API_URL_PREFIX = ""
HOST = "0.0.0.0"
PORT = 5001

ENABLE_CORS = True

## application base path
APP_BASE_PATH = "src/"

## Module name
MODULE_NAME = "/aai4b-nmt-inference"

## fetch model details
FETCH_MODEL_CONFG = os.path.join(APP_BASE_PATH, "config/fetch_models.json")

## truncation limit for sentence length
trunc_limit = 200

## max number of input sentences per batch (for inference service, specific to GPU type)
translation_batch_limit = os.environ.get('TRANSLATION_BATCH_LIMIT', 75)
if isinstance(translation_batch_limit, str):
    translation_batch_limit = eval(translation_batch_limit)

## supported languages
supported_languages = ['en','hi','ta','te','kn','pa','mr','as','or','ml','gu','bn']

## loaded model ('indic-en' OR 'en-indic' OR 'indic-indic')
model_to_load = os.environ.get('MODEL_NAME', 'indic-indic') # loads all three models 

redis_server_host = os.environ.get('REDIS_URL', 'localhost')
redis_server_pass = os.environ.get('REDIS_PASS', 'mypassword')
redis_server_port = os.environ.get('REDIS_PORT', 6380)
if isinstance(redis_server_port, str):
    redis_server_port = eval(redis_server_port)

redis_db = os.environ.get('TRANSLATION_REDIS_DB', 0)
if isinstance(redis_db, str):
    redis_db = eval(redis_db)

record_expiry_in_sec = os.environ.get('TRANSLATION_REDIS_EXPIRY', 86400)
if isinstance(record_expiry_in_sec, str):
    record_expiry_in_sec = eval(record_expiry_in_sec)

nmt_cron_interval_sec = os.environ.get('NMT_CRON_INTERVAL_SEC', 1)
if isinstance(nmt_cron_interval_sec, str):
    nmt_cron_interval_sec = eval(nmt_cron_interval_sec)

poll_api_interval_sec = os.environ.get('POLL_API_INTERVAL_SEC', 0.1)
if isinstance(poll_api_interval_sec, str):
    poll_api_interval_sec = eval(poll_api_interval_sec)