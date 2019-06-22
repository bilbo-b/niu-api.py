#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import requests
import json
from requests.exceptions import ConnectionError
# import time
# from prometheus_client import start_http_server
# from prometheus_client import Counter, Gauge

API_BASE_URL = 'https://app-api.niu.com'
ACCOUNT_BASE_URL = 'https://account.niu.com'
NIU_EMAIL = os.environ['NIU_EMAIL']
NIU_PASSWORD = os.environ['NIU_PASSWORD']
NIU_COUNTRYCODE = os.environ['NIU_COUNTRYCODE']


def get_token(email=NIU_EMAIL, password=NIU_PASSWORD, cc=NIU_COUNTRYCODE):
    url = ACCOUNT_BASE_URL + '/appv2/login'
    data = {'account': email, 'countryCode': cc, 'password': password}
    try:
        r = requests.post(url, data=data)
    except BaseException as e:
        print (e)
        return False
    data = json.loads(r.content.decode())
    return data['data']['token']


def get_vehicles(token):

    url = API_BASE_URL + '/motoinfo/list'
    headers = {'token': token, 'Accept-Language': 'en-US'}
    try:
        r = requests.post(url, headers=headers, data=[])
    except ConnectionError as e:
        print("Caught Error")
        print(e)
        return False
    if r.status_code != 200:
        return False
    data = json.loads(r.content.decode())
    return data['data'][0]['sn']
# übergebe nur die erste Seriennr. zu erweitern,
# wenn man mehr als 1 Roller mit dem Account verbunden hat


def get_info(path, sn, token):
    url = API_BASE_URL + path
#    print (url)
    params = {'sn': sn}
    headers = {'token': token, 'Accept-Language': 'en-US'}
    try:
        r = requests.get(url, headers=headers, params=params)
#        print (r.content)
#        print (r.status_code)
    except ConnectionError as e:
        print("Caught Error")
        print(e)
        return False
    if r.status_code != 200:
        return False
    data = json.loads(r.content.decode())
    if data['status'] != 0:
        print (data)
        return False
#    data = data['data']['batteries']['compartmentA']
#    del data['items']
    return data


def post_info(path, sn, token):
    url = API_BASE_URL + path
#    print (url)
    params = {}
    headers = {'token': token, 'Accept-Language': 'en-US'}
    try:
        r = requests.post(url, headers=headers, params=params, data={'sn':sn})
#        print (r.content)
#        print (r.status_code)
    except ConnectionError as e:
        print("Caught Error")
        print(e)
        return False
    if r.status_code != 200:
        return False
    data = json.loads(r.content.decode())
    if data['status'] != 0:
        print (data)
        return False
#    data = data['data']['batteries']['compartmentA']
#    del data['items']
    return data

if __name__ == "__main__":
    token = get_token()
    sn = get_vehicles(token)
    data = get_info('/v3/motor_data/battery_info', sn, token)
    batteryInfo = data['data']['batteries']['compartmentA']
    """
    print ('Output von batteryInfo')
    del batteryInfo['items']
    print (batteryInfo)
    # {'isConnected': True, 'chargedTimes': '10', 'temperature': 23,
    'energyConsumedTody': 0, 'totalPoint': 480, 'temperatureDesc': 'normal',
    'bmsId': 'BN1GPC2B40400386', 'batteryCharging': 49, 'gradeBattery': '99'}
    """
    print ('Battery Info:')
    print ('BMS-Id:        ', batteryInfo['bmsId'])
    print ('BatteryCharge: ', batteryInfo['batteryCharging'])
    print ('Is connected:  ', batteryInfo['isConnected'])
    print ('Times charged: ', batteryInfo['chargedTimes'])
    print ('Temperature:   ', batteryInfo['temperature'])
    print ('Battery Grade: ', batteryInfo['gradeBattery'])

    motorInfo = get_info('/v3/motor_data/index_info', sn, token)

    print ('Motor Info:')
    print ('exp. range:    ', motorInfo['data']['estimatedMileage'])
    print ('current speed: ', motorInfo['data']['nowSpeed'])
    print ('is connected:  ', motorInfo['data']['isConnected'])
    print ('is charging:   ', motorInfo['data']['isCharging'])
    print ('is locked:     ', motorInfo['data']['lockStatus'])
    print ('gsm signal:    ', motorInfo['data']['gsm'])
    print ('gps signal:    ', motorInfo['data']['gps'])
    print ('Time left:     ', motorInfo['data']['leftTime'])
    print ('centreCtrlBatt:', motorInfo['data']['centreCtrlBattery'])
    print ('Position lat:  ', motorInfo['data']['postion']['lat'])
    print ('Position lng:  ', motorInfo['data']['postion']['lng'])
    if (len(motorInfo['data']['lastTrack'])) != 0:
        print ('Last Track:  ')
        print ('  Timestamp:   ', motorInfo['data']['lastTrack']['time'])
        print ('  Distance:    ', motorInfo['data']['lastTrack']['distance'])
        print ('  Riding Time: ', motorInfo['data']['lastTrack']['ridingTime'])
    """
    print ('Last Track:  ')
    print ('  Timestamp:   ', motorInfo['data']['lastTrack']['time'])
    print ('  Distance:    ', motorInfo['data']['lastTrack']['distance'])
    print ('  Riding Time: ', motorInfo['data']['lastTrack']['ridingTime'])
    print (motorInfo)
    {'trace': '成功', 'status': 0, 'desc': '成功', 'data': {'ss_protocol_ver': 2,
    'nowSpeed': 0, 'isAccOn': '', 'isConnected': True, 'infoTimestamp':
    1561015942946, 'leftTime': '17.0', 'isCharging': 0, 'hdop': 0, 'gsm': 24,
    'gps': 3, 'centreCtrlBattery': 100, 'gpsTimestamp': 1560976555998,
    'batteryDetail': True, 'lockStatus': 0, 'isFortificationOn': '',
    'batteries': {'compartmentA': {'batteryCharging': 49, 'bmsId':
    'BN1GPC2B40400386', 'isConnected': True, 'gradeBattery': '99'}},
    'time': 1561015942946, 'ss_online_sta': '1', 'lastTrack': {'time':
    1560976555998, 'distance': 7755, 'ridingTime': 1066},
    'postion': {'lng': 8.703397, 'lat': 50.105606}, 'estimatedMileage': 28}}
    """

    overallTally = post_info('/motoinfo/overallTally', sn, token)
    # print (overallTally)
    print ('Total km:      ', overallTally['data']['totalMileage'])
    print ('Total km since:', overallTally['data']['bindDaysCount'], 'days')

    batteryHealth = get_info('/v3/motor_data/battery_info/health', sn, token)
    """
    # fand ich überwiegend als info nicht spannend
    print (batteryHealth)
    # {'desc': '成功', 'trace': '成功', 'data': {'isDoubleBattery': False,
    'batteries': {'compartmentA': {'healthRecords': [{'time': 1561017242842,
    'chargeCount': '10', 'name': '电池循环 * 10', 'color': '#878787',
    'result': '-1'}], 'faults': [], 'isConnected': True, 'gradeBattery': '99',
    'bmsId': 'BN1GPC2B40400386'}}}, 'status': 0}
    """
    print ('is double batt:', batteryHealth['data']['isDoubleBattery'])
    # firmwareInfo = get_info('/motorota/getfirmwareversion', sn, token)
    # print (firmwareInfo)
