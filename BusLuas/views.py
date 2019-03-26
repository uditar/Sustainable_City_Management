from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from BusLuas.models import BusLuas as IrishRail
from django.http import JsonResponse
from APIHandling import DublinBusAPI


def index(request):
    template = loader.get_template('BusLuas/IrishRail.html')
    return HttpResponse(template.render())


def irishrail_data(request):
    template = loader.get_template('IrishRail.html')
    return HttpResponse(template.render())


def IrishRailData(request):
    # vsar data=CityEvents.objects.values_list('nametext', 'startutc', named=True)
    queryset = list(IrishRail.objects.filter().values())
    #print(queryset)
    return JsonResponse(queryset, safe=False)

def DublinBusData(request):
    print('Testthe----------------')
    test=DublinBusAPI.getAllDublinBusStandInfo()
    queryset = list(IrishRail.objects.filter().values())
    #print(queryset)
    return JsonResponse(queryset, safe=False)

def RealTimeBusData(stopnumber):
    print('test')
    stopid = request.form['stopid']
    print(stopid)



    url = "http://rtpi.dublinbus.ie/DublinBusRTPIService.asmx"

    querystring = {"WSDL":""}

    payload = "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:dub=\"http://dublinbus.ie/\">\r\n   <soap:Header/>\r\n   <soap:Body>\r\n      <dub:GetRealTimeStopData>\r\n         <dub:stopId>"+ str(stopid)+"</dub:stopId>\r\n      </dub:GetRealTimeStopData>\r\n   </soap:Body>\r\n</soap:Envelope>"
    headers = {
        'Content-Type': "text/xml",
        'cache-control': "no-cache",
        'Postman-Token': "618820e6-6411-40c5-805a-9846f9812b55"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    # print(response.text)
    stopDataRealTime=jsonResponse(response.text)


    # dblink = 'http://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid=' + str(stopid)+ '&format=json'
    # r = requests.get(dblink)
    # print(r)

    fileName=str(stopid)+ '.json'
    with open(fileName, 'w') as outfile:
        json.dump(stopDataRealTime, outfile)
    
    # jsondata = json.loads(r.text)
    # jsonpath = 'dbapp/static/json_data/stop' + str(stopid)+ '.json'
    # dir = os.path.dirname(jsonpath)
    # if not os.path.exists(dir):
    #     os.makedirs(dir)
    # with open(jsonpath, 'w') as f:
    #     json.dump(jsondata, f)
    return render_template('search.html', stopid = stopid)


def jsonResponse(xmlText):
    print('recieved')

    o = xmltodict.parse(xmlText)
    print(type(dict(o)))
    response=json.loads(json.dumps(o['soap:Envelope']["soap:Body"]["GetRealTimeStopDataResponse"]["GetRealTimeStopDataResult"]["diffgr:diffgram"]["DocumentElement"]["StopData"]))
    stopDataRealTime=json.loads(json.dumps(o['soap:Envelope']["soap:Body"]["GetRealTimeStopDataResponse"]["GetRealTimeStopDataResult"]["diffgr:diffgram"]["DocumentElement"]["StopData"]))
    print(stopDataRealTime)
    for element in stopDataRealTime:
        # print(json.dumps(element))
        print(element['MonitoredCall_ExpectedDepartureTime'])
    # print(stopDataRealTime)
    # print(type(response['soap:Envelope']["soap:Body"]["GetRealTimeStopDataResponse"]["GetRealTimeStopDataResult"]["diffgr:diffgram"]["DocumentElement"]["StopData"]))
    return stopDataRealTime


# def BusDashBoard(request):
#     template = loader.get_template('DublinBus.html')
#     return HttpResponse(template.render())