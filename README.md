# Airflow on Docker in EC2 + GitLab's CI/CD

Personal project for simple data pipeline using Airflow. Airflow will be installed inside Docker container, which will be deployed in Amazon's EC2. For continuous integration and continuous deployment (CI/CD), GitLab will be used.

## Steps

1. Set up EC2 server. Choose ubuntu. Download the ssh key (with .pem suffix). Open ports of the EC2 instance, especially port 8080.
2. SSH inside your EC2 server. Install Docker and docker-compose.
3. Create GitLab account. Create new repository on GitLab, and push this repository there.
4. On your GitLab's project page, open Settings > CI/CD > Repository Variables. Configure several variables:<br>
    * _AIRFLOW_WWW_USER_PASSWORD -> Arbitrary password for Airflow (Variable)<br>
    * _AIRFLOW_WWW_USER_USERNAME -> Arbitrary username for Airflow (Variable)<br>
    * EC2_ADDRESS -> IP address of your EC2 host (Variable)<br>
    * GITLAB_PASSWORD -> GitLab password (Variable)<br>
    * GITLAB_USERNAME -> GitLab username (Variable)<br>
    * SSH_KEY_EC2 -> Your SSH key (with .pem suffix that you downloaded earlier) (File)<br>
5. Configure GitLab's runner for CI/CD
6. Open gitlab-ci.yml, change line 25 and 26 with your email (that registered on GitLab) and Name. If your user name in EC2 is not default (ubuntu), change ubuntu in `ubuntu@EC2_ADDRESS` with the correct username
7. Run CI/CD pipeline, check if the code is deployed properly.
8. SSH to the server to inspect if anything goes wrong
9. Open the Airflow UI in browser on EC2_IP_ADDRESS:8080