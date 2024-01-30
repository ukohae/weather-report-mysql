# Weather Report with MySQL and Python

```
git clone https://github.com/ukohae/weather-report-mysql.git
```
## Terraform Virtual Environment Configuration - WSL-Ubuntu (Optional)
- Configure virtual environment on `Ubuntu WSL`
```
sudo ln -sf $(which python3) /usr/bin/python && sudo apt install python3-venv -y && sudo apt install unzip -y
```

```
python -m venv venv && source venv/bin/activate
```

- Terraform Installation
    - Run the `install-terraform.sh` script
```
./scripts/install-terraform.sh 
```
```
source venv/bin/activate
```


## Deploy MySQL to AWS
- Terraform version must be `v1.3.0` and above
```
terraform init && terraform apply --auto-approve
```
- Give it `4 minutes` to provision the `MySQL Server`.

- After `4 minutes`, `SSH` into the `MySQL Server` and run the `weather.py` script
```
python3 weather.py
```

## Destroy all resources
- Exit out of the database
```
\q
```
- Destroy the resources
```
terraform destroy --auto-approve
```

- To clean up your environment after `destroying resources` run:
```
./scripts/clean.sh
```