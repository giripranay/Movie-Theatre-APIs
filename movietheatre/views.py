# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.http import HttpResponse
from .models import Screen,Row,Seat
import json
from movietheatre.serializers import UserSerializer,ScreenSerializer,RowSerializer,SeatSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import Http404

def index(request):
    request = {"name":"inox","seatInfo":{"A":{"numberOfSeats":10,"aisleSeats":[0,5,6,9]}}}
    #entry = Screen(screen_name = request.name)
    #entry.save()
    #screen = Screen.objects.get(screen_name = request.name)
    screen_name = request['name']
    
    row = request['seatInfo'].keys()
    
    for i in row:
        row_name = i
        seat_number=request['seatInfo'][i]['numberOfSeats']
        aisle_seats=request['seatInfo'][i]['aisleSeats']
    

    return HttpResponse(row_name)

class Screens(APIView):
    def post(self,request,format=None):
        serializer = ScreenSerializer(data = {'screen_name':request.data['name']})
        if serializer.is_valid():
            serializer.save()
            row = request.data['seatInfo'].keys()
            for i in row:
                screen = serializer.data['id']
                row_name = i
                number_of_seats=request.data['seatInfo'][i]['numberOfSeats']
                string = ""
                for seat in request.data['seatInfo'][i]['aisleSeats']:
                    string += str(seat)
                aisle_seats=string
                Data = {'screen':screen,'row_name':row_name,'number_of_seats':number_of_seats,'aisle_seats':aisle_seats}
                rowserializer = RowSerializer(data = Data)
                if rowserializer.is_valid():
                    rowserializer.save()
            rows = Row.objects.filter(screen=serializer.data['id'])
            rowserializer = RowSerializer(rows, many = True)
            serializer_data = serializer.data
            serializer_data.pop('id')
            serializer_data['seatInfo'] = rowserializer.data
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Reserve(APIView):
    def post(self,request,screen_name,format=None):
        seat = request.data['seats'].keys()  
        try:
            screen_obj = Screen.objects.get(screen_name=screen_name)
            for i in seat:
                screen = screen_obj.id
                try:
                    row_obj = Row.objects.get(Q(screen=screen_obj.id) & Q(row_name=i))
                    row = row_obj.id
                    for num in request.data['seats'][i]:
                        Data = {'screen':screen,'row':row,'seat_number':num,'is_reserved':True}
                        serializer = SeatSerializer(data = Data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Row.DoesNotExist:
                    return Response({"Error":"Row "+i+ " doesn't exist"}, status = status.HTTP_400_BAD_REQUEST)
            seats = Seat.objects.filter(screen=screen)
            seatserializer = SeatSerializer(seats,many = True)
            return Response(seatserializer.data, status = status.HTTP_201_CREATED)
        except Screen.DoesNotExist:
            return Response({"Error":"Screen with name " +screen_name + " doesn't exist"}, status = status.HTTP_400_BAD_REQUEST)

class ShowSeats(APIView):
    def get(self,request,screen_name):
        if request.GET['status']=='unreserved':
            try:
                rows = Row.objects.filter(screen__screen_name = screen_name)
                dic = {"seats":{}}
                for row in rows:
                    seats = Seat.objects.filter(Q(screen__screen_name = screen_name) & Q(row__row_name = row.row_name))
                    l=range(1,row.number_of_seats+1)
                    for seat in seats:
                        l.remove(seat.seat_number)
                    dic['seats'][row.row_name] = l
                return Response(dic,status = status.HTTP_201_CREATED)    
            except Seat.DoesNotExist:
                return Response({"Error":"error"},status = status.HTTP_400_BAD_REQUEST)

        elif request.GET['status']=='reserved':
            try:
                rows = Row.objects.filter(screen__screen_name = screen_name)
                dic = {"seats":{}}
                for row in rows:
                    seats = Seat.objects.filter(Q(screen__screen_name = screen_name) & Q(row__row_name = row.row_name))
                    l=[]
                    for seat in seats:
                        l.append(seat.seat_number)
                    dic['seats'][row.row_name] = l
                return Response(dic,status = status.HTTP_201_CREATED)    
            except Seat.DoesNotExist:
                return Response({"Error":"error"},status = status.HTTP_400_BAD_REQUEST)
            




class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
       # return HttpResponse("Hello world")
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
