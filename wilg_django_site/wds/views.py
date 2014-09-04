# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.views.generic.list import ListView

from slideshow.models import Slideshow

#homepage 
def index(request):
    return render_to_response('index/index.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('about/index.html', context_instance=RequestContext(request, {
                'about_slideshow':Slideshow.objects.get(name='about_page')
                }))

def rush(request):
    return render_to_response('rush/index.html', context_instance=RequestContext(request))

def house(request):
    return render_to_response('house/index.html', context_instance=RequestContext(request, {
                'house_slideshow':Slideshow.objects.get(name='house_tour')
                }))

def alumnae(request):
    return render_to_response('alumnae/index.html', context_instance=RequestContext(request))

def _exec(request):
    return render_to_response('exec/index.html', context_instance=RequestContext(request))

def events(request):
    return render_to_response('events/index.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact/index.html', context_instance=RequestContext(request))

def _members(request):
    return render_to_response('members/index2.html', context_instance=RequestContext(request))

def resources(request):
    return render_to_response('resources/index.html', context_instance=RequestContext(request))

def getSequence(request):
    seq = Sequence.objects.order_by('?')[0]
    js = serializers.serialize("json",[seq])
    return HttpResponse(js, mimetype='application/json')

def initTrial(request):
    '''
    initialize a trial with a new trial ID an a new random sequence
    '''
    sequence = Sequence.objects.order_by('?')[0]
    conf_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    while(conf_code in Trial.objects.values('conf_code')):
        # ensure uniqueness
        conf_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    js = serializers.serialize("json", [sequence])

    # a hack to get the confirmation code into json
    js_dict = json.loads(js)
    js_dict.append({'conf_code':conf_code})
    js = json.dumps(js_dict)

    return HttpResponse(js, mimetype='application/json')

def submitSamples(request):
    samples = request.GET.get('samples')
    guess_arr = request.GET.get('guess')
    try:
        trial_obj = Trial.objects.get(conf_code = request.GET.get('conf'))
    except:
        trial_obj = Trial(sequence_id = request.GET.get('seq_id'))
        trial_obj.save()
        trial_obj.conf_code = request.GET.get('conf')
    guess_obj = Guess(numbers=guess_arr)
    guess_obj.save()
    trial_obj.guesses.add(guess_obj)
    trial_obj.save()
    js = serializers.serialize("json",[])
    return HttpResponse(js, mimetype='application/json')

