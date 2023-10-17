# pawproject/PawHost



## Pre-requisites
- [python3](https://www.python.org/downloads/)
- [pip3](https://pip.pypa.io/en/stable/installing/)

## Installation
1. Clone the repository
2. Install the dependencies
``` pip3 install -r requirements.txt ``` or ``` ./install.sh ``` on linux or ``` install.cmd ``` on windows

## Running the server
``` python3 main.py ``` or ``` ./run.sh ``` on linux or ``` run.cmd ``` on windows

## Config
The config file is located at ``` config.json ```

- ```FurPass```=> The password for api
- ```data_dir```=> The directory where the database located

## API
- ```/api/health```=> Health check
- ```/api/result/add/ports/custom```=> Add custom port scan result
```
Method: POST
FurPass: md5(FurPass) # md5 hash of password, should be set on 
                      # header or as a get parameter
                      # All api under /api/result
                      # should use password
Content-Type: application/json
{
    "ip": "127.0.0.1",
    "ports": "80",
    "status": "1", # 1 for open, 0 for filtered, -1 for closed
    "banner": "", # when blank, it will be auto grabbed on server
    "note": {
        "origin": "masscan", => origin of the scan
        "orgName": "网易", => org name
        "masscan":{
            "service": "http", => pulgin output
        }
    } # Can keep blank
}
```
------------------------------------
Each api under have those param in common

```limits``` => how much result to return, default is 20

```page``` => which page to return, default is 1

```plain``` => when appeared, only returned format as ```ip:port```, default not

```Use GET Method```
- ```/api/result/query/list/ip``` => List All result in database
- ```/api/result/query/list/ip/<ip>``` => List result of specific ip
- ```/api/result/query/list/port/<port>``` => List result of specific port
- ```/api/result/query/list/status/<status>``` => List result of specific status
- ```/api/result/query/list/banner/<banner>``` => Filiter banner
- ```/api/result/query/list/note/<note>``` => Filiter note


## TODO
1. [ ] Write UI
2. [ ] Integration with [Zmap](https://www.github.com/zmap/zmap), [Masscan](https://www.github.com/robertdavidgraham/masscan), [Nmap](https://www.github.com/nmap/nmap)
3. [ ] Add Web Application Grab/Storage/Analyse API
4. [ ] Add Unauthorized Check