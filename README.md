
# WETRANSFER CRYPTO

Send crypted file to your friends 😉


## Installation

To Install the project you need to execute the command below

```bash
  pip install -r .\requirements.txt
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GOOGLE_APPLICATION_CREDENTIALS` : JSON key of your service account

`BUCKET_NAME` : name of your GCS bucket

`PROJECT_ID` : Your project ID

`FIRESTORE_DATABASE` : The name of your firestore database

`PRIVATE_KEY_PATH` : The key path of your private key



## API Reference

#### Upload data

```http
  POST /upload

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `File` | Send a file to the bucket and store the data in Firestore |
| `from_email` | `String` | Get the link for the user with the email of the sender |
| `to_email` | `String` | Get the link for the user with the email of the receiver  |
| `expiration_date` | `String` | Date expiration of the document |
| `password` | `String` | Password to access file download  |

Uplaod file data to firestore


#### Get from_email

```http
  GET /userLinkFrom/@from_email

```

#### Get to_email

```http
  GET /userLinkTo/@to_email

```


## Tech Stack

**Server:** Python, Flask, cryptography

**Infrastructure:** Google console, Firestore, GCS Bucket


## Authors

- [@LeonardBen](https://github.com/LeonardBen)

