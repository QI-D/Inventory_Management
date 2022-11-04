docker build -t receiver:latest receiver/
docker build -t storage:latest storage/
docker build -t processing:latest processing/
docker build -t audit_log:latest audit_log/
docker build -t dashboard:latest dashboard-ui/

cd deployment
docker-compose up -d
