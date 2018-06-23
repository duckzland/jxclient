# JXClient

Python script for controlling [ JXMiner ](https://github.com/duckzland/jxminer) via CLI.

![Alt text](docs/jxminer.png?raw=true "JXMiner Screenshot")

## Requirement
- JXMiner installed and running


## Installation (Ubuntu)       
1. Install python dependencies via requirement.txt:
```bash
    sudo pip install -r requirement.txt  
```
    
3. Install the deb
```bash
    sudo dpkg -i python-jxclient-VERSION.deb
```
    


## Usage

```bash
    jxclient -a|-h|-s|-p|-v {options}
```

Valid options for the client :
```bash
    -a {action}
        monitor:miner:cpu          Retrieving CPU miner log entry'
        monitor:miner:gpu:x        Retrieving CPU miner x (0|1) log entry'
        monitor:server             Retrieving Full server logs in json format'
        server:status              Checking server status'
        server:shutdown            Shuts down the server'
        server:reboot              Rebooting server instance'
        server:update              Updating server loaded configuration'
    -s Insert the server host ip address, default to 127.0.0.1'
    -p Insert the server port number, default is 8129'
    -h Prints this help message'
    -v Prints version'
```



## Authors

* **Jason Xie** - *Initial work* - [VicTheme.com](https://victheme.com)



## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details
