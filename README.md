
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

`PRIVATE_KEY` : The key for encrypt data

`SENDER_EMAIL` : The sending email address

`APP_PASSWORD` : The application password of the email address


## API Reference

#### Upload data

```http
  POST /upload

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `File` | Send a file to the bucket and store the data in Firestore |
| `to_email` | `String` | Get the link for the user with the email of the receiver  |
| `expiration_date` | `String` | Date expiration of the document |
| `password` | `String` | Password to access file download  |

Uplaod file data to firestore


#### Get file_path

```http
  POST /getFilePath/

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `crypted_file_path` | `string` | crypted file path  |
| `password` | `string` | Password for access file |
| `to_email` | `string` | Destination Email |
| `from_email` | `string` | Sender Email |

Get download link from storage

## Tech Stack

**Server:** Python, Flask, cryptography, smtplib

**Infrastructure:** Google console, Firestore, GCS Bucket

## Cryptography

``` load_or_generate_private_key
  return private_key

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |

Generate a key if it does not exist for encrypted data

``` hash_data
  return hashed_data

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `data` | `*` | data to be encrypted  |

Encrypt data

``` generate_key
  return key

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `from_email` | `string` | Sender Email |
| `to_email` | `string` | Destination Email |

Generate key in function of parameters

``` encrypt_url
  return encrypted_url

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `from_email` | `string` | Sender Email |
| `to_email` | `string` | Destination Email |
| `file_path` | `string` | file path |

Generate encrypted url in function of key generated

``` decrypt_url
  return decrypted_url

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `from_email` | `string` | Sender Email |
| `to_email` | `string` | Destination Email |
| `file_path_crypted` | `string` | encrypt file path |

Generate decrypted url in function of key

## Authors
- [@LeonardBen](https://github.com/LeonardBen)
- [@azizPotter](https://github.com/azizPotter)
- [@NicolasDS](https://github.com/SynhPoO)
