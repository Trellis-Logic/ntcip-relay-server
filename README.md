# ntcip-relay-server

This continer is used to convert POST http requests to actions on an NTCIP
Server.

Given this config.json:
```
{
    "ntcip_controller_ip": "192.168.88.1",
    "ntcip_controller_port": "501",
    "ntcip_community": "administrator",
    "ntcip_version": 1,
    "http_server_port": 8080
}
```
The resulting POST curl invocations on the pedcall endpoint on the local server at port 8080
will result in NTCIP/SNMP set commands on the NTCIP controller at IP address 192.168.88.1
and port 5501.

Operations will be performed on the oid specified at "1.2.3.4".  A curl command formatted like this:
```
curl -X POST http://localhost:8080/pedcall/ \
  -H 'Content-Type: application/json' \
  -d '{ "activate" : true, "phase_control_group" : 1, "phase" : 1, "mib" : "1.3.6.1.4.1.1206.4.2.1.1.5.1.7" }'
```
will result in an integer 1 value (phase bit 1) set on the mib at 1.3.6.1.4.1.1206.4.2.1.1.5.1.7.1, and a command formatted like this:
```
curl -X POST http://localhost:8080/pedcall/ \
  -H 'Content-Type: application/json' \
  -d '{ "activate" : false, "phase_control_group" : 1, "phase" : 1, "mib" : "1.3.6.1.4.1.1206.4.2.1.1.5.1.7" }'
```
will result in an cleared phase phase bit 1 value on the mib at 1.3.6.1.4.1.1206.4.2.1.1.5.1.7.1

To verify, you may query with a command like this:
```
snmpwalk -v2c -c administrator localhost:501 1.3.6.1.4.1.1206.4.2.1.1.5.1.7.1
```

## Building and running with docker

Run `./docker/build.sh` to build followed by `./docker/run.sh`

## Integrating with Services

The [docker/service](docker/service) directory is intended for integrating with the [services](https://github.com/sighthoundinc/services)
repository.  See the example documentation there for further information.

