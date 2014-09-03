# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from chat.models import Message, Feedback

import json
import uuid

class Custom:
    def __init__(self, name, phone):
        self.id = uuid.uuid1()
        self.name = name
        self.phone = phone

class TempMessage:
    def __init__(self, type, content, time):
        self.type = type
        self.content = content
        self.time = time

def customInitialization(request):
    try:
        custom = request.session['custom']
        messages = []
        for item in Message.objects.filter(customID = custom.id):
            messages.append(TempMessage('custom', item.content, item.time))
        for item in Feedback.objects.filter(customID = custom.id, isDisplay = True):
            messages.append(TempMessage('server', item.content, item.time))
        messages = sorted(messages, key = lambda x : x.time)
    except:
        custom = None
        messages = []
    return { 'messages': messages, 'custom': custom }

def serverInitialization(request):
    items = []
    result = []
    messages = Message.objects.all().order_by('-time')
    for item in messages:
        if item.customID not in items:
            result.append(item)
            items.append(item.customID)
    return { 'messages': result[:10] }

def getDemo(request, type, templateName):
    if type == 'custom':
        return render_to_response(templateName, {
            }, context_instance = RequestContext(request,
                processors = [customInitialization]))
    else:
        return render_to_response(templateName, {
            }, context_instance = RequestContext(request,
                processors = [serverInitialization]))

def getServerMessage(request, templateName):
    messages = []
    customID = ''
    if request.method == 'GET':
        customID = request.GET.get('customID', None)
        for item in Message.objects.filter(customID = customID, isDisplay = True):
            messages.append(TempMessage('custom', item.content, item.time))
        for item in Feedback.objects.filter(customID = customID):
            messages.append(TempMessage('server', item.content, item.time))
        messages = sorted(messages, key = lambda x : x.time)
    return render_to_response(templateName, {
        'messages': messages,
        'customID': customID,
        })

def getSessionList(request, templateName):
    items = []
    result = []
    messages = Message.objects.all().order_by('-time')
    for item in messages:
        if item.customID not in items:
            result.append(item)
            items.append(item.customID)
    return render_to_response(templateName, {
        'messages': result,
        })

def getNewMessage(request, type, templateName):
    messages = []
    if request.method == 'GET':
        if type == 'custom':
            if request.session['custom']:
                customID = request.session['custom'].id
                messages = Feedback.objects.filter(customID = customID,
                    isDisplay = False)
        elif type == 'server':
            customID = request.GET.get('customID', None)
            if customID:
                messages = Message.objects.filter(isDisplay = False,
                    customID = customID)
        for item in messages:
            item.isDisplay = True
            item.save()
    return render_to_response(templateName, {
        'messages': messages,
        }, context_instance = RequestContext(request))

@csrf_exempt
def createNewMessage(request, type):
    success = False
    wrong = ''
    if request.method == 'POST':
        content = request.POST.get('content', None)
        if content:
            if type == 'custom':
                if request.session['custom']:
                    custom = request.session['custom']
                    Message.objects.create(
                        customID = custom.id,
                        name = custom.name,
                        phone = custom.phone,
                        content = content,
                        )
                    success = True
                else:
                    wrong = '操作时间过长,用户已失效'
            elif type == 'server':
                customID = request.POST.get('customID', None)
                if customID:
                    Feedback.objects.create(
                        content = content,
                        customID = customID,
                        )
                    success = True
                else:
                    wrong = '操作失败'
            else:
                wrong = '请不要乱输url'
        else:
            wrong = '内容不能为空'
    return HttpResponse(json.dumps({
        'success': success,
        'wrong': wrong,
        }))

@csrf_exempt
def getCustomID(request, templateName):
    custom = None
    try:
        custom = request.session['custom']
    except:
        name = request.POST.get('name', None)
        phone = request.POST.get('phone', None)
        if name and phone:
            request.session['custom'] = Custom(name, phone)
            custom = request.session['custom']
    return render_to_response(templateName, {
        'custom': custom,
        })
