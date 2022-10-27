docker build -t receiver:latest receiver/
docker build -t storage:latest storage/
docker build -t processing:latest processing/
docker build -t audit_log:latest audit_log/

cd deployment
docker-compose up -d
