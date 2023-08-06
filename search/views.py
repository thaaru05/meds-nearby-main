from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests
import json

from .forms import SearchForm,CoordForm
# Create your views here.
def sort_by_distance(result):
    length=len(result)
    i=0
    while i<length:
        pharma=result[i]
        j=i-1
        while j>=0:
            if result[j]['distance']>pharma['distance']:
                temp=result[j]
                result[j]=pharma
                result[j+1]=temp
            j-=1
        i+=1
    '''print('in sbd',result)'''
    return result
    '''template='api_handling/result.html'
    data={'form':form,'result':result}
    return render(request,template,data)'''

def sort_By_price(result):
    length=len(result)
    i=0
    while i<length:
        pharma=result[i]
        j=i-1
        while j>=0:
            if result[j]['price']>pharma['price']:
                temp=result[j]
                result[j]=pharma
                result[j+1]=temp
            j-=1
        i+=1
    '''print(result)'''
    return result
def get_result(pharmacies,medicine_name):
    '''print('get_result')'''
    place_id=dict()
    i=0
    for pharma in pharmacies:
        place_id[i]=pharma['place_id']
        i+=1
    place_id=json.dumps(place_id)
    api=f"http://127.0.0.1:8000/api/pharmacies/?pharmacy_id={place_id}&medicine_name={medicine_name}"
    res=requests.get(api)
    result=json.loads(res.json())
    for result_pharma in result:
        for pharma in pharmacies:
            if result_pharma['place_id']==pharma['place_id']:
                result_pharma['distance']=pharma['distance']
                result_pharma['lat']=pharma['lat']
                result_pharma['lon']=pharma['lon']
    return result

def get_pharmacies(lon,lat,medicine_name,radius):
    '''print('get_phar')'''
    api=f'https://api.geoapify.com/v2/places?bias=proximity:{lon},{lat}&categories=healthcare.pharmacy&filter=circle:76.9843304,11.0629428,{radius}&limit=50&apiKey=d0f637b5187e487196dd3d9504742ecf'
    res=requests.get(api)
    dict_res=res.json()
    '''print('type',type(dict_res))'''
    features=dict_res['features']
    '''print('type feat',type(features),'\nfeatures len\n',len(features))'''
    pharmacy_details=[]
    for places in features:
        properties =places['properties']
        if 'name' in properties.keys():
            pharmacy_details.append({'name':properties['name'],'distance':properties['distance'],'place_id':properties['place_id'],'lat':properties['lat'],'lon':properties['lon']})
    '''print('phar len',len(pharmacy_details))
    print('details')'''
    '''for pharma in pharmacy_details:
        print(pharma['name'],pharma['distance'],pharma['place_id'],pharma['lat'],pharma['lon'])'''
    result=get_result(pharmacy_details,medicine_name)
    return result
def get_coord_api(request):
    if request.method=='GET':
        form=SearchForm()
        template='search/search.html'
        data={'form':form,'result':None}
        return render(request,template,data)
    if request.method=='POST':
        '''print(request.POST)'''
        form=SearchForm(request.POST)
        medicine_name=request.POST['medicine']
        radius=request.POST['search_radius_in_meter']
        sort_by=request.POST['sortby']
        api='https://api.geoapify.com/v1/geocode/search?postcode={}&format=json&apiKey=d0f637b5187e487196dd3d9504742ecf'.format(request.POST['postal_code'])
        res=requests.get(api)
        dict_res=res.json()
        lat=dict_res['results'][0]['lat']
        lon=dict_res['results'][0]['lon']
        '''print(lat,lon)'''
        result=get_pharmacies(lon,lat,medicine_name,radius)
        print('result:\n',result)
        if sort_by=='d':
            result=sort_by_distance(result)
        else:
            result=sort_By_price(result)
        print('r:\n',result)
        if len(result)==0:
            messages.warning(request,"Couldn't find any pharmacies in the specified radius that sell the searched medicine! please try increasing the search radius!")
        template='search/search.html'
        for r in result:
            value_={'to_lat':r['lat'],'to_lon':r['lon'],'frm_lat':lat,'frm_lon':lon}
            r['coord']=CoordForm(value_)
            print('r',r['coord'].is_valid())
        data={'form':form,'result':result,'medicine_name':medicine_name}
        return render(request,template,data)
        

