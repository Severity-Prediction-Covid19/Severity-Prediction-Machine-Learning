# Severity Prediction Machine Learning (Sure Health) By C22-PS273 Capstone Project Bangkit 2022

## Overview
SureHealth is an app which has the purpose to optimize the self-diagnosis to be more accurate, especially to know about severity prediction covid-19

## Credits
The dataset that we use for built model prediction is from kaggle [[Dataset]](https://www.kaggle.com/code/corneliustantius/covid-severity-prediction/data)

Then our reference of the model is also from kaggle [[Reference]](https://www.kaggle.com/code/maragarcagirn/covid-19-recognition)

These are some of the references we use Deploying an ML Model on Google Compute Engine by alara dirik [[Deployment To VM]](https://towardsdatascience.com/deploying-a-custom-ml-prediction-service-on-google-cloud-ae3be7e6d38f)

## Making Prediction Model
From the dataset there are 316800 row data and for this model we use 11 features in the form of symptoms and later will produce the output which is like severity categories in the form of none, mild, moderate and severe. For the general step is we do the preprocessing data which is to split data for training and validation of the model. In this model we use 202752 samples for training and 50688 for validation.  After that we built the model with keras and tensorflow. Then the model will generate the new folder which has shown the variable that it can use in load_model and produce the output of prediction. After that we make a flask that is used as web server to try the prediction model in a way upload the validation data and will give the result of prediction. Then, we make main.py script is for use as API that can be access by Cloud Computing path. Machine Learning path use Jupyter Lab for built the model and pre-deploy process.

## Step Deploy To GCP 
1. First Go to VPC Network > Firewall Rules > Ip Ranges Source 0.0.0.0/0 > Set Target tags > Set specifed protocols and port on TCP 5000 (Because we set flask running on port 5000)
2. Go to VM instance in Google Compute Engine (GCE) We are using Ubuntu 18.04 LTS > allow the HTTP traffic > Click Networking > Put your Network Tags 
3. Open the VM using SSH.
4. After that, we will prepare the dependencies and the virtual environment. On the terminal run:
```bash
# Clone This Repository On Github
git clone https://github.com/Severity-Prediction-Covid19/Severity-Prediction-Machine-Learning.git

# update system packages, install the required packages, and miniconda
sudo apt-get update
sudo apt-get install bzip2 libxml2-dev libsm6 libxrender1 libfontconfig1
wget https://repo.anaconda.com/miniconda/Miniconda3-4.7.10-Linux-x86_64.sh
bash Miniconda3-4.7.10-Linux-x86_64.sh

# make conda executable
export PATH=/home/<Google Cloud name>/miniconda3/bin:$PATH
rm Miniconda3-4.7.10-Linux-x86_64.sh

# create and activate a new virtual environment
conda create -n sure-health python=3.7
conda activate sure-health
```
5. Next step install the dependencies from requirements.txt and gunicorn in the virtual environment and start running the **main.py** script:
```bash
# Change directory 
cd Severity-Prediction-Machine-Learning

# Install all requirements
pip install -r requirements.txt
pip install gunicorn

# Test run main.py
python main.py
```
6. Use Nginx and gunicorn to make the VM can handle HTTP requests, because Flask itself can not handle them. We need to install Nginx in VM
```bash
# Install nginx
cd ..
sudo apt-get install nginx-full
sudo /etc/init.d/nginx start
```
7. Configure Nginx
```bash
# remove default configuration file
sudo rm /etc/nginx/sites-enabled/default

# create a new site configuration file
sudo touch /etc/nginx/sites-available/sure-health-project
sudo ln -s /etc/nginx/sites-available/sure-health-project /etc/nginx/sites-enabled/sure-health-project
```
8. Next edit file configuration
```bash
sudo nano /etc/nginx/sites-enabled/sure-health-project
```
Copy and Paste the code bellow and save
```bash
server {
    client_max_body_size 100M;
    location / {
        proxy_pass http://0.0.0.0:5000;
    }
```
9. Next Restart the Nginx Server
```bash
sudo /etc/init.d/nginx restart
```
10. Change directory to folder repo and bind the Flask model **main.py** to the Gunicorn server.
```bash
cd Severity-Prediction-Machine-Learning
gunicorn --bind 0.0.0.0:5000 main:app
```

11. Now u can use this API Model, use the external IP Address on VM Instance for Run

## Postman Test
You can use Request GET Mehod and url '/' go to http://34.101.40.253/ and this result is C22-PS273 and You can request with Method POST and url '/predict' request to body with key 'data_file' and select file **validation_data.csv** for check this result go to http://34.101.40.253/predict. 
![Postman test](https://user-images.githubusercontent.com/99069985/172362060-8930055a-3ebb-4344-a0e0-bfa8d0f67521.jpg)

