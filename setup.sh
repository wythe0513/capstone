curl --request POST \
  --url https://tomascap.jp.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"OYMVmHrMZa0vD9eNinhYvmRMVQ0iU9Oz","client_secret":"OYMVmHrMZa0vD9eNinhYvmRMVQ0iU9Oz","audience":"agency","grant_type":"client_credentials"}'

export DOMAIN="tomascap.jp.auth0.com"
export CLIENT_ID="OYMVmHrMZa0vD9eNinhYvmRMVQ0iU9Oz"
export CLIENT_SECRET="OYMVmHrMZa0vD9eNinhYvmRMVQ0iU9Oz"
