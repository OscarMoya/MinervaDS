# MinervaDS

Distributed Storage Minerva use-case main repository

## Deploying

First, configure the `deploy_config.py` file with proper IPs, password and port to access your machines.

```
cd tools
python deploy.py {start|stop|shutdown}
```

## Uploading

```
cd distributed/storage/src/main
python run_client.py upload <path_to_file>
```
The client will return a file identifier to be used during the download.

## Downloading

```
python run_client.py download <file_id>
```
