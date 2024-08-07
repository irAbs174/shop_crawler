# WOOCOMMERCE SHOP CRAWLER

**Version:** 0.0.2  
**Developer:** UNIQUE174

## INSTALLATION

### Using Python Virtual Environment

To set up the project using a Python virtual environment, follow these steps:

```bash
sudo apt install python3 python3-pip python3-venv &&
python3 -m venv env &&
source env/bin/activate &&
pip install --upgrade pip &&
pip install -r requirements.txt &&
python3 app/main.py --help
```
### Using Docker
If you don't have Docker installed, follow these steps to install it:
Update your package list and install necessary packages:
```
sudo apt update &&
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
Add Docker’s official GPG key:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
Set up the stable repository:
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
Install Docker Engine:
```
sudo apt update &&
sudo apt install docker-ce docker-ce-cli containerd.io
```
Verify that Docker is installed correctly by running the hello-world image:
```
sudo docker run hello-world
```
Build and Run the Docker Image
To set up the project using Docker, follow these steps:

Build the Docker image:
```
docker build -t woocommerce-shop-crawler .
```
Run the Docker container:
```
docker run -it --rm woocommerce-shop-crawler --help
```
love
