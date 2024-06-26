# Warehouse Digital Twin Data Layer APIs

- Host: https://digital-twin.expangea.com
- Required request header: **X-API-KEY**

## Warehouse API
- Endpoint: ``` /warehouse/```
- Method: POST

## Warehouse Details API
- Endpoint: ``` /warehouse/<warehouse_code>/```
- Method: POST

## Rack List API
- Endpoint: ``` /rack/<warehouse_code>/```
- Method: POST

## Rack Details API
- Endpoint: ``` /rack/<warehouse_code>/<rack_no>/```
- Method: POST

## Rack Location Details API
- Endpoint: ``` /rack-location/<location_id>/```
- Method: POST

## Pallet Details API
- Endpoint: ``` /pallet/<pallet_id>/```
- Method: POST

## Pallet History API
- Endpoint: ``` /pallet/<pallet_id>/<days>/```
- Method: POST

## Device Location API
- Endpoint: ``` /device/<device-name>/```
- Method: POST

## Device Location History API
- Endpoint: ``` /device/<device-name>/<days>/```
- Method: POST

## Device Location Upload API
- Endpoint: ``` /device/```
- Method: POST
