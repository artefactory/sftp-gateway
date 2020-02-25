#! /bin/sh

if [ -z "${ENV}" ]; then
  environment=dev
else
  environment=${ENV}
fi

mkdir -p config/

tmpfile=$(mktemp)

cat env/${environment} env/common env/${environment} > $tmpfile
dotenv -f $tmpfile list > config/${environment}
rm -f $tmpfile
