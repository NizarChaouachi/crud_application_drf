from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import NoteSerializer
from .models import NoteModel
import math
from datetime import datetime 

# Create your views here.

class Notes(generics.GenericAPIView):
    serializer_class=NoteSerializer
    queryset=NoteModel.objects.all()
    
    def get(self,request):
        page_num=int(request.GET.get('page',1))
        limit_num=int(request.GET.get("limit",10))
        start_num=(page_num-1)*limit_num
        end_num=limit_num*page_num
        search_param=request.GET.get('search')
        notes=NoteModel.objects.all()
        total_notes=notes.count()
        if search_param:
            notes=notes.filter(title__icontains=search_param)
        serializer=self.serializer_class(notes[start_num:end_num],many=True)
        return Response(
            {
                "status":"success",
                "total":total_notes,
                "page_num":page_num,
                "last_page":math.ceil(total_notes/limit_num),
                "notes":serializer.data
             }
            )
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( {"status":"success","note":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"fail","message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
class NotesDetail(generics.GenericAPIView):
    queryset=NoteModel.objects.all()
    serializer_class=NoteSerializer
    
    def get_note(self,pk):
        try :
            return NoteModel.objects.get(pk=pk)
        except:
            return None
        
    def get(self,request,pk):
        notes=self.get_note(pk=pk)
        if not notes:
            return Response({"status":"fail","message":f"Note with Id: {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(notes)
        return Response({"status":"succes","notes":serializer.data})
    def patch(self,request,pk):
        notes=self.get_note(pk=pk)
        if not notes:
            return Response({"status":"fail","message":f"Note with Id: {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(notes,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.validated_data['updateAt']=datetime.now()
            serializer.save()
            return Response({"status":"succes","notes":serializer.data})
        return Response({"status":"fail","message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        notes=self.get_note(pk=pk)
        if not notes:
            return Response({"status":"fail","message":f"Note with Id: {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        notes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        