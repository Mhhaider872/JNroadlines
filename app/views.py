from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.utils.timezone import now
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
from num2words import num2words
import os




def userdash(request):
     plan=plandetails.objects.count()
     bill_count = Gemini.objects.count()
     vehicle_c=Add_Vehicle.objects.count()
     dname=NewDriver_Details.objects.count()
     trip=AddTrips.objects.count()
     tripgemini=TripGemini.objects.count()
     tripadani=TripAdani.objects.count()
     triplocal=AakLocal.objects.count()
     trip_exp=Trip.objects.count()
     salary=Driver_salary.objects.count()
     

     context = {
        'plan':plan,
        'bill_count': bill_count,
        'vehicle_c': vehicle_c,
        'dname':dname,
        'trip':trip,
        'trip_exp':trip_exp,
        'salary':salary,
        'tripgemini':tripgemini,
        'tripadani':tripadani,
        'triplocal':triplocal
    }
     return render(request,'userdash.html',context)

def userloan(request):
    
    return render(request,'userloan.html')


# Create your views here.

def dashboard(request):
    plan=plandetails.objects.count()
    bill_count = Gemini.objects.count()
    vehicle_c=Add_Vehicle.objects.count()
    dname=NewDriver_Details.objects.count()
    trip=AddTrips.objects.count()
    tripgemini=TripGemini.objects.count()
    tripadani=TripAdani.objects.count()
    triplocal=AakLocal.objects.count()
    trip_exp=Trip.objects.count()
    salary=Driver_salary.objects.count()

    context = {
        'plan':plan,
        'bill_count': bill_count,
        'vehicle_c': vehicle_c,
        'dname':dname,
        'trip':trip,
        'trip_exp':trip_exp,
        'salary':salary,
        'tripgemini':tripgemini,
        'tripadani':tripadani,
        'triplocal':triplocal
    }
    return render(request,'index.html',context)

def plan(request):
    if request.method =="POST":
      tankerno  = request.POST['tankerno']
      drivername = request.POST['drivername']
      From_address = request.POST['From_address']
      To_address = request.POST['To_address']
      tanker_capacity = request.POST['tanker_capacity']
      dispatch_Date = request.POST['dispatch_Date']
      status = request.POST['status']
      if  plandetails.objects.filter(tankerno=tankerno,dispatch_Date=dispatch_Date).exists():
          messages.error(request, 'Plan already exists !!')
          return redirect('plan')
      else:
          plan=plandetails(tankerno=tankerno,drivername=drivername,From_address=From_address,To_address=To_address,tanker_capacity=tanker_capacity,dispatch_Date=dispatch_Date,status=status)
          plan.save()
          messages.success(request, 'Plan details added successfully !!')
          return redirect('showplan')
    vehicle=Add_Vehicle.objects.all()
    # dname=DriverName.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname}
    return render(request,'add/add-plans.html', context)

def showplan(request):
    showplans=plandetails.objects.all()
    context={'showplans':showplans}
    return render(request,'show/show-plan.html',context)




def updateplan(request,id):
    planupdate=plandetails.objects.get(pk=id)
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    context={'planupdate':planupdate,'vehicle':vehicle,'company':company}
    return render(request,'update-plans.html',context)


def do_updateplan(request, id): 
    tankerno = request.POST.get('tankerno')
    drivername = request.POST.get('drivername')
    From_address = request.POST.get('From_address')
    To_address = request.POST.get('To_address')
    tanker_capacity = request.POST.get('tanker_capacity')
    dispatch_Date = request.POST.get('dispatch_Date')
    status = request.POST.get('status')

    # Fetch the existing plan details to update
    planupdate = plandetails.objects.get(pk=id)

    # Update the fields
    planupdate.tankerno = tankerno
    planupdate.drivername = drivername
    planupdate.From_address = From_address
    planupdate.To_address = To_address
    planupdate.tanker_capacity = tanker_capacity
    planupdate.dispatch_Date = dispatch_Date
    planupdate.status = status

    # Save the changes
    planupdate.save()

    # Success message
    messages.success(request, 'Plan updated successfully!')

    # Redirect to the showplan page (or wherever you need to redirect)
    return redirect('showplan')

                                                                       
def deleteplan(request,id):
    d=plandetails.objects.get(pk=id)
    d.delete()
    return redirect('showplan')




def addtrip(request):
    if request.method == "POST":
        # Get tankerno_id from the form
        tankerno_id = request.POST.get('tankerno')

        if not tankerno_id:
            messages.error(request, 'Please select a tanker.')
            return redirect('addtrip')

        try:
            # Get the selected plan details using tankerno_id
            selected_plan = plandetails.objects.get(id=tankerno_id)
        except plandetails.DoesNotExist:
            messages.error(request, 'Selected tanker does not exist.')
            return redirect('addtrip')

        # Collect other form data
        From_address = request.POST.get('From_address')
        To_address = request.POST.get('To_address')
        drivername = request.POST.get('drivername')
        tank_capacity = request.POST.get('tank_capacity')
        arrival_time = parse_datetime(request.POST.get('arrival_time')) if request.POST.get('arrival_time') else None
        dispatch_time = parse_datetime(request.POST.get('dispatch_time')) if request.POST.get('dispatch_time') else None
        reach_time = parse_datetime(request.POST.get('reach_time')) if request.POST.get('reach_time') else None
        unload_time = parse_datetime(request.POST.get('unload_time')) if request.POST.get('unload_time') else None
        lr_num = request.POST.get('lr_num')
        lr_date = request.POST.get('lr_date')
        freight_bill = request.POST.get('freight_bill')
        freight_date = request.POST.get('freight_date')
        loaded_qty = request.POST.get('loaded_qty')
        unload_qty = request.POST.get('unload_qty')
        percent = request.POST.get('percent')
        short_qty = request.POST.get('short_qty')
        short_allow = request.POST.get('short_allow')
        return_qty = request.POST.get('return_qty')
        remark = request.POST.get('remark')

        # Validate the necessary fields
        if AddTrips.objects.filter(plan=selected_plan, dispatch_time=dispatch_time).exists():
            messages.error(request, 'Trip already exists!')
            return redirect('addtrip')

        # Create a new trip entry
        trip = AddTrips(
            plan=selected_plan,  # Link the selected_plan to the ForeignKey field
            From_address=From_address,
            To_address=To_address,
            drivername=drivername if drivername else None,
            tank_capacity=tank_capacity if tank_capacity else None,
            arrival_time=arrival_time,
            dispatch_time=dispatch_time,
            reach_time=reach_time,
            unload_time=unload_time,
            lr_num=lr_num if lr_num else None,
            lr_date=lr_date if lr_date else None,
            freight_bill=freight_bill if freight_bill else None,
            freight_date=freight_date if freight_date else None,
            loaded_qty=loaded_qty if loaded_qty else None,
            unload_qty=unload_qty if unload_qty else None,
            percent=percent if percent else None,
            short_qty=short_qty if short_qty else None,
            short_allow=short_allow if short_allow else None,
            return_qty=return_qty if return_qty else None,
            remark=remark if remark else None,
        )
        trip.save()  # Save the new trip
        messages.success(request, 'Trip added successfully!')

    # Get the list of plans for the dropdown
    plans = plandetails.objects.all()

    # Return to the template with the plans
    context = {'plans': plans}
    return render(request, 'add/add_trip_all.html', context)



def get_plan_details(request):
    plan_id = request.GET.get('plan_id')
    try:
        plan = plandetails.objects.get(id=plan_id)
        data = {
            'drivername': plan.drivername,
            'From_address': plan.From_address,
            'To_address': plan.To_address,
            'tanker_capacity': plan.tanker_capacity,
            'dispatch_Date': plan.dispatch_Date,
        }
        return JsonResponse(data)
    except plandetails.DoesNotExist:
        return JsonResponse({'error': 'Plan not found'}, status=404)
   
def showtrip(request):
    show=AddTrips.objects.all()
    context={'show':show}
    return render(request,'show/show-trip.html',context)

def updatetrip(request,id):
    uptrip=AddTrips.objects.get(pk=id)
    plans = plandetails.objects.all()
    context={'uptrip':uptrip,'plans':plans}
    return render (request,'update-add-trip.html',context)


def do_updatetrip(request,id): 
    tankerno = request.POST.get('tankerno')
    drivername = request.POST.get('drivername')
    From_address = request.POST.get('From_address')
    To_address = request.POST.get('To_address')
    tank_capacity = request.POST.get('tank_capacity')
    arrival_time = request.POST.get('arrival_time')
    dispatch_time = request.POST.get('dispatch_time')
    reach_time = request.POST.get('reach_time')
    unload_time = request.POST.get('unload_time')
    loaded_qty = request.POST.get('loaded_qty')
    percent = request.POST.get('percent')
    unload_qty = request.POST.get('unload_qty')
    short_qty = request.POST.get('short_qty')
    short_allow = request.POST.get('short_allow')
    return_qty = request.POST.get('return_qty')
    lr_num = request.POST.get('lr_num')
    lr_date = request.POST.get('lr_date')
    freight_bill = request.POST.get('freight_bill')
    freight_date = request.POST.get('freight_date')
     

    # Fetch the existing plan details to update
    update_t = AddTrips.objects.get(pk=id)

    # Update the fields
    update_t.tankerno = tankerno
    update_t.drivername = drivername
    update_t.From_address = From_address
    update_t.To_address = To_address
    update_t.tank_capacity = tank_capacity
    update_t.arrival_time=arrival_time if freight_bill else None
    update_t.dispatch_time = dispatch_time if freight_bill else None
    update_t.reach_time = reach_time if freight_bill else None
    update_t.unload_time = unload_time if freight_bill else None
    update_t.loaded_qty = loaded_qty if freight_bill else 0
    update_t.percent = percent if freight_bill else 0
    update_t.unload_qty = unload_qty if freight_bill else 0
    update_t.short_qty = short_qty if freight_bill else 0
    update_t.short_allow = short_allow if freight_bill else 0
    update_t.return_qty = return_qty if freight_bill else 0
    update_t.lr_num = lr_num if freight_bill else 0
    update_t.return_qty = return_qty if freight_bill else 0
    update_t.freight_bill = freight_bill if freight_bill else 0
    update_t.freight_date = freight_date if freight_date else 0
    update_t.lr_date = lr_date if lr_date else 0

    # Save the changes
    update_t.save()

    # Success message
    messages.success(request, 'Trip updated successfully!')

    # Redirect to the showplan page (or wherever you need to redirect)
    return redirect('showtrip')



def deltrip(request,id):
    deltrips=AddTrips.objects.get(pk=id)
    deltrips.delete()
    return redirect('showtrip')






def Trip_Adani(request):
    # plan = plandetails.objects.earliest('tankerno')  
    # if plan:
    #     tankerno = plan.tankerno
    #     drivername=plan.drivername
    #     From_address = plan.From_address
    #     To_address = plan.To_address
    #     tanker_capacity = plan.tanker_capacity
    # else:
    #     tankerno = From_address = To_address = 'Data not available'
    
    
    if request.method == "POST":
        # Get tankerno_id from the form
        tankerno_id = request.POST.get('tankerno')

        if not tankerno_id:
            messages.error(request, 'Please select a tanker.')
            return redirect('addtrip')

        try:
            # Get the selected plan details using tankerno_id
            selected_plan = plandetails.objects.get(id=tankerno_id)
        except plandetails.DoesNotExist:
            messages.error(request, 'Selected tanker does not exist.')
            return redirect('addtrip')
       
        From_address = request.POST['From_address']
        To_address = request.POST['To_address']
        drivername = request.POST['drivername']
        tank_capacity = request.POST['tank_capacity']
        arrival_time = request.POST['arrival_time']
        dispatch_time = request.POST['dispatch_time']
        reach_time = request.POST['reach_time']
        unload_time = request.POST['unload_time']
        lr_num  = request.POST['lr_num']
        lr_date = request.POST['lr_date']
        freight_bill = request.POST['freight_bill']
        freight_date = request.POST['freight_date']
        loaded_qty = request.POST['loaded_qty']
    #    percent = request.POST['percent']
        unload_qty = request.POST['unload_qty']
        short_qty = request.POST['short_qty']
        short_allow = request.POST['short_allow']
        return_qty = request.POST['return_qty']
        remark = request.POST['remark']
        if   TripAdani.objects.filter(plan=selected_plan, dispatch_time= dispatch_time).exists():
            messages.error(request, 'Trip already exists !!')
            return redirect('trip-adani')
        else:
          trip=TripAdani( plan=selected_plan,
                         tankerno=tankerno_id,
                         From_address=From_address,
                         To_address=To_address,
                         drivername=drivername,
                         tank_capacity=tank_capacity,
                         arrival_time=arrival_time if arrival_time else None,
                         dispatch_time=dispatch_time if dispatch_time else None,
                         reach_time=reach_time if reach_time else None,
                         unload_time=unload_time if unload_time else None,
                         lr_num=lr_num if lr_num else None,
                         lr_date=lr_date if lr_date else None,
                         freight_bill=freight_bill if freight_bill else None,
                         freight_date=freight_date if freight_date else None,
                         loaded_qty=loaded_qty if loaded_qty else None,
                         unload_qty=unload_qty if unload_qty else None,
                         short_qty=short_qty if short_qty else None,
                         short_allow=short_allow if short_allow else None,
                         return_qty=return_qty if return_qty else None,
                         remark=remark if remark else None)
          trip.save()
          messages.success(request, 'Trip added successfully !!') 
          
          
          
    
    # Pass the values to the template
    # Get the list of plans for the dropdown
    plans = plandetails.objects.all()

    # Return to the template with the plans
    context = {'plans': plans}
    return render(request, 'add/add_trip_adani.html',context)

def ShowAdani(request):
    adani=TripAdani.objects.all()
    context={'adani':adani}
    return render(request,'show/show_adani.html',context)

def delatrip(request,id):
    dadani=TripAdani.objects.get(pk=id)
    dadani.delete()
    return redirect('show-adani')

def upadanitrip(request,id):
    up_adani=TripAdani.objects.get(pk=id)
    context={'up_adani':up_adani}
    return render(request,'update_adani.html', context)

def do_upadani(request,id):
    tankerno = request.POST.get('tankerno')
    drivername = request.POST.get('drivername')
    From_address = request.POST.get('From_address')
    To_address = request.POST.get('To_address')
    tank_capacity = request.POST.get('tank_capacity')
    arrival_time = request.POST.get('arrival_time')
    dispatch_time = request.POST.get('dispatch_time')
    reach_time = request.POST.get('reach_time')
    unload_time = request.POST.get('unload_time')
    loaded_qty = request.POST.get('loaded_qty')
    # percent = request.POST.get('percent')
    unload_qty = request.POST.get('unload_qty')
    short_qty = request.POST.get('short_qty')
    short_allow = request.POST.get('short_allow')
    return_qty = request.POST.get('return_qty')
    lr_num = request.POST.get('lr_num')
    lr_date = request.POST.get('lr_date')
    freight_bill = request.POST.get('freight_bill')
    freight_date = request.POST.get('freight_date')
    
    

    up_adani=TripAdani.objects.get(pk=id)

    up_adani.tankerno=tankerno
    up_adani.drivername=drivername
    up_adani.From_address=From_address
    up_adani.To_address=To_address
    up_adani.tank_capacity=tank_capacity
    up_adani.arrival_time=arrival_time
    up_adani.dispatch_time=dispatch_time
    up_adani.reach_time=reach_time
    up_adani.unload_time=unload_time
    up_adani.loaded_qty=loaded_qty
    up_adani.unload_qty=unload_qty
    up_adani.short_qty=short_qty
    up_adani.short_allow=short_allow
    up_adani.return_qty=return_qty
    up_adani.lr_num=lr_num
    up_adani.lr_date=lr_date
    up_adani.freight_bill=freight_bill
    up_adani.freight_date=freight_date

    up_adani.save()

    messages.success(request, 'Adani Trip updated successfully!')
    return redirect('show-adani')



def Trip_Gemini(request):
    # plan = plandetails.objects.earliest('tankerno')  
    # if plan:
    #     tankerno = plan.tankerno
    #     drivername=plan.drivername
    #     From_address = plan.From_address
    #     To_address = plan.To_address
    #     tanker_capacity = plan.tanker_capacity
    # else:
    #     tankerno = From_address = To_address = 'Data not available'
    
    if request.method =="POST":
       if request.method =="POST":
        # Get tankerno_id from the form
        tankerno_id = request.POST.get('tankerno')

        if not tankerno_id:
            messages.error(request, 'Please select a tanker.')
            return redirect('addtrip')

        try:
            # Get the selected plan details using tankerno_id
            selected_plan = plandetails.objects.get(id=tankerno_id)
        except plandetails.DoesNotExist:
            messages.error(request, 'Selected tanker does not exist.')
            return redirect('addtrip')
       
        From_address = request.POST['From_address']
        To_address = request.POST['To_address']
        drivername = request.POST['drivername']
        tank_capacity = request.POST['tank_capacity']
        arrival_time = request.POST['arrival_time']
        dispatch_time = request.POST['dispatch_time']
        reach_time = request.POST['reach_time']
        unload_time = request.POST['unload_time']
        lr_num  = request.POST['lr_num']
        lr_date = request.POST['lr_date']
        freight_bill = request.POST['freight_bill']
        freight_date = request.POST['freight_date']
        loaded_qty = request.POST['loaded_qty']
        # percent = request.POST['percent']
        unload_qty = request.POST['unload_qty']
        short_qty = request.POST['short_qty']
        short_allow = request.POST['short_allow']
        return_qty = request.POST['return_qty']
        remark = request.POST['remark']
        if   TripGemini.objects.filter(plan=selected_plan, dispatch_time= dispatch_time).exists():
            messages.error(request, 'Trip already exists !!')
            return redirect('trip-gemini')
        else:
          trip=TripGemini( plan=selected_plan,
                        tankerno=tankerno_id,
                         From_address=From_address,
                         To_address=To_address,
                         drivername=drivername,
                         tank_capacity=tank_capacity,
                         arrival_time=arrival_time if arrival_time else None,
                         dispatch_time=dispatch_time if dispatch_time else None,
                         reach_time=reach_time if reach_time else None,
                         unload_time=unload_time if unload_time else None,
                         lr_num=lr_num if lr_num else None,
                         lr_date=lr_date if lr_date else None,
                         freight_bill=freight_bill if freight_bill else None,
                         freight_date=freight_date if freight_date else None,
                         loaded_qty=loaded_qty if loaded_qty else None,
                         unload_qty=unload_qty if unload_qty else None,
                        #  percent=percent if percent else None,
                         short_qty=short_qty if short_qty else None,
                         short_allow=short_allow if short_allow else None,
                         return_qty=return_qty if return_qty else None,
                         remark=remark if remark else None
                         )
          trip.save()
          messages.success(request, 'Trip added successfully !!') 
          return redirect('show-gemini-details')
    
    # Get the list of plans for the dropdown
    plans = plandetails.objects.all()

    # Return to the template with the plans
    context = {'plans': plans}
    return render(request, 'add/add_trip_gemini.html',context)

def Showgemini(request):
    gemeni=TripGemini.objects.all()
    context={'gemeni':gemeni}
    return render(request,'show/show_gemini.html',context)


def delgemini(request,id):
    g=TripGemini.objects.get(pk=id)
    g.delete()
    return redirect('show-gemini-details')


def upgemini(request,id):
    geminiup=TripGemini.objects.get(pk=id)
    context={'geminiup':geminiup}
    return render(request,'update_gemini.html',context)


def do_upgemini(request,id):
    tankerno = request.POST.get('tankerno')
    drivername = request.POST.get('drivername')
    From_address = request.POST.get('From_address')
    To_address = request.POST.get('To_address')
    tank_capacity = request.POST.get('tank_capacity')
    arrival_time = request.POST.get('arrival_time')
    dispatch_time = request.POST.get('dispatch_time')
    reach_time = request.POST.get('reach_time')
    unload_time = request.POST.get('unload_time')
    loaded_qty = request.POST.get('loaded_qty')
    # percent = request.POST.get('percent')
    unload_qty = request.POST.get('unload_qty')
    short_qty = request.POST.get('short_qty')
    short_allow = request.POST.get('short_allow')
    return_qty = request.POST.get('return_qty')
    lr_num = request.POST.get('lr_num')
    lr_date = request.POST.get('lr_date')
    freight_bill = request.POST.get('freight_bill')
    freight_date = request.POST.get('freight_date')
    
    

    geminiup=TripGemini.objects.get(pk=id)

    geminiup.tankerno=tankerno
    geminiup.drivername=drivername
    geminiup.From_address=From_address
    geminiup.To_address=To_address
    geminiup.tank_capacity=tank_capacity
    geminiup.arrival_time=arrival_time
    geminiup.dispatch_time=dispatch_time
    geminiup.reach_time=reach_time
    geminiup.unload_time=unload_time
    geminiup.loaded_qty=loaded_qty
    geminiup.unload_qty=unload_qty
    geminiup.short_qty=short_qty
    geminiup.short_allow=short_allow
    geminiup.return_qty=return_qty
    geminiup.lr_num=lr_num
    geminiup.lr_date=lr_date
    geminiup.freight_bill=freight_bill
    geminiup.freight_date=freight_date

    geminiup.save()

    messages.success(request, 'Gemini Trip updated successfully!')
    return redirect('show-gemini-details')




def aaklocal(request):
    
    if request.method =="POST":
        # Get tankerno_id from the form
        tankerno_id = request.POST.get('tankerno')

        if not tankerno_id:
            messages.error(request, 'Please select a tanker.')
            return redirect('addtrip')

        try:
            # Get the selected plan details using tankerno_id
            selected_plan = plandetails.objects.get(id=tankerno_id)
        except plandetails.DoesNotExist:
            messages.error(request, 'Selected tanker does not exist.')
            return redirect('addtrip')
        From_address = request.POST['From_address']
        To_address = request.POST['To_address']
        drivername = request.POST['drivername']
        tank_capacity = request.POST['tank_capacity']
        arrival_time = request.POST['arrival_time']
        dispatch_time = request.POST['dispatch_time']
        reach_time = request.POST['reach_time']
    #    unload_time = request.POST['unload_time']
        lr_num  = request.POST['lr_num']
        lr_date = request.POST['lr_date']
        freight_bill = request.POST['freight_bill']
        freight_date = request.POST['freight_date']
        loaded_qty = request.POST['loaded_qty']
        percent = request.POST['percent']
        unload_qty = request.POST['unload_qty']
        short_qty = request.POST['short_qty']
        short_allow = request.POST['short_allow']
        return_qty = request.POST['return_qty']
        return_qty = request.POST['return_qty']
        return_qty = request.POST['return_qty']
        remark = request.POST['remark']
        time_Loading = request.POST['time_Loading']
        time_Loading_mama = request.POST['time_Loading_mama']
        time_Loading_mama = request.POST['time_Loading_mama']
        unloading_ganesh   = request.POST['unloading_ganesh']
        unloading_mama   = request.POST['unloading_mama']
        returned   = request.POST['returned']
        trip_ganesh   = request.POST['trip_ganesh']
        trip_mama   = request.POST['trip_mama']
        if  AakLocal.objects.filter(plan=selected_plan, dispatch_time= dispatch_time).exists():
           messages.error(request, 'Trip already exists !!')
           return redirect('aak-local')
        else:
            trip=AakLocal(plan=selected_plan,
                         tankerno=selected_plan.tankerno, 
                         From_address=From_address,
                         To_address=To_address,
                         drivername=drivername,
                         tank_capacity=tank_capacity,
                         arrival_time=arrival_time if arrival_time else None,
                         dispatch_time=dispatch_time if dispatch_time else None,
                         reach_time=reach_time if reach_time else None,
                         
                         lr_num=lr_num if lr_num else None,
                         lr_date=lr_date if lr_date else None,
                         freight_bill=freight_bill if freight_bill else None,
                         freight_date=freight_date if freight_date else None,
                         loaded_qty=loaded_qty if loaded_qty else None,
                         unload_qty=unload_qty if unload_qty else None,
                         percent=percent if percent else None,
                         short_qty=short_qty if short_qty else None,
                         short_allow=short_allow if short_allow else None,
                         return_qty=return_qty if return_qty else None,
                         remark=remark if remark else None,
                         time_Loading=time_Loading if time_Loading else None,
                         time_Loading_mama=time_Loading_mama if time_Loading_mama else None,
                         unloading_ganesh=unloading_ganesh if unloading_ganesh else None,
                         unloading_mama=unloading_mama if unloading_mama else None,
                         returned=returned if returned else None,
                         trip_ganesh=trip_ganesh if trip_ganesh else None,
                         trip_mama= trip_mama if  trip_mama else None,
                        )
            trip.save()
            messages.success(request, 'Trip added successfully !!')
     # Get the list of plans for the dropdown
    plans = plandetails.objects.all()

    # Return to the template with the plans
    context = {'plans': plans}
    return render(request,'AAK-india-local.html',context)

def ShowAakLocal(request):
    Aak=AakLocal.objects.all()
    context={'Aak':Aak}
    return render(request,'show/show_Aak_india_local.html',context)


def updateAak(request,id):
    Aak_u=AakLocal.objects.get(pk=id)
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    context={'Aak_u':Aak_u,'company':company,'vehicle':vehicle}
    return render(request,'update_aak_local.html',context)


def doupdateAak(request,id):
    tankerno  = request.POST.get('tankerno')
    From_address = request.POST.get('From_address')
    To_address = request.POST.get('To_address')
    drivername = request.POST.get('drivername')
    tank_capacity = request.POST.get('tank_capacity') 
    arrival_time = request.POST.get('arrival_time')
    dispatch_time = request.POST.get('dispatch_time')
    reach_time = request.POST.get('reach_time')
    lr_num  = request.POST.get('lr_num')
    lr_date = request.POST.get('lr_date')
    freight_bill = request.POST.get('freight_bill')
    freight_date = request.POST.get('freight_date')
    loaded_qty = request.POST.get('loaded_qty')
    unload_qty = request.POST.get('unload_qty')
    short_qty = request.POST.get('short_qty')
    short_allow = request.POST.get('short_allow')
    return_qty = request.POST.get('return_qty')
    
    remark= request.POST.get('remark')
    time_Loading= request.POST.get('time_Loading')
    time_Loading_mama= request.POST.get('time_Loading_mama')
    time_Loading_mama= request.POST.get('time_Loading_mama')
    unloading_ganesh = request.POST.get('unloading_ganesh')
    unloading_mama= request.POST.get('unloading_mama')
    returned= request.POST.get('returned')
    trip_ganesh= request.POST.get('trip_ganesh')
    trip_mama= request.POST.get('trip_mama')
    
    
    Aakupdate=AakLocal.objects.get(pk=id)
    
    Aakupdate.tankerno=tankerno
    Aakupdate.From_address=From_address
    Aakupdate.To_address=To_address
    Aakupdate.drivername=drivername
    Aakupdate.tank_capacity=tank_capacity
    Aakupdate.arrival_time=arrival_time
    Aakupdate.dispatch_time=dispatch_time
    Aakupdate.reach_time=reach_time
    Aakupdate.lr_num=lr_num
    Aakupdate.lr_date=lr_date
    Aakupdate.freight_bill=freight_bill
    Aakupdate.freight_date=freight_date
    Aakupdate.loaded_qty=loaded_qty
    Aakupdate.unload_qty=unload_qty
    Aakupdate.short_qty=short_qty
    Aakupdate.short_allow=short_allow
    Aakupdate.return_qty=return_qty
    Aakupdate.remark=remark
    Aakupdate.time_Loading=time_Loading
    Aakupdate.time_Loading_mama=time_Loading_mama
    Aakupdate.unloading_ganesh=unloading_ganesh
    Aakupdate.unloading_mama=unloading_mama
    Aakupdate.returned=returned
    Aakupdate.trip_ganesh=trip_ganesh
    Aakupdate.trip_mama=trip_mama

    Aakupdate.save()
    messages.success(request, 'Trip updated successfully!')
    return redirect('Aak-Local')



def delete(request,id):
    d=AakLocal.objects.get(pk=id)
    d.delete()
    return redirect('Aak-Local')


def addvehicle(request):
    return render(request,'add/add-vehicle.html')





def adddriver(request):
    if request.method =="POST":
      name = request.POST['name']
      adharnumber = request.POST['adharnumber']
      licencenumber = request.POST['licencenumber']
      issuedates = request.POST['issuedates']
      trdates = request.POST['trdates']
    #   imguploads = request.POST['imguploads'] 
      img = request.FILES.get('img') 
      fname = request.POST['fname']
      
      if NewDriver_Details.objects.filter(adharnumber=adharnumber).exists():
         messages.error(request, 'Driver & Aadhar No already exists !!')
         return redirect('adddriver')
      else:
          deriver=NewDriver_Details(name=name,
                                    adharnumber=adharnumber if adharnumber else None,
                                    licencenumber=licencenumber if licencenumber else None,
                                    issuedates=issuedates if issuedates else None,
                                    trdates=trdates if trdates else None,
                                    img=img if img else None,
                                    fname=fname if fname else None)
          deriver.save()
          messages.success(request, 'Driver details added successfully !!') 
    # dname=NewDriver_Details.objects.all()
    # context={'dname':dname}
    return render(request,'add/add-driver.html')

def showdriver(request):
    showdriver=NewDriver_Details.objects.all()
    context={'showdriver':showdriver}
    return render(request,'show/show-driver-details.html',context)

def deletedriver(request,id):
    driver= NewDriver_Details.objects.get(pk=id)
    if  AddTrips.objects.filter(drivername=driver.name).exists():
          messages.error(request, "Driver cannot be deleted because they have trips assigned.")
          return redirect('showdrivers')
    else:
         driver.delete()
         messages.success(request, "Driver deleted successfully.")

    return redirect('showdrivers')

def driverupdate(request,id):
    updatedriver=NewDriver_Details.objects.get(pk=id)
    context={'updatedriver':updatedriver}
    return render(request,'update-driver.html',context)

def doupdatedriver(request,id):
     name = request.POST.get('name')
     adharnumber = request.POST.get('adharnumber')
     licencenumber = request.POST.get('licencenumber')
     issuedates = request.POST.get('issuedates')
     trdates = request.POST.get('trdates')
     img = request.FILES.get('img') 
     fname = request.POST.get('fname')

     updatedriver=NewDriver_Details.objects.get(pk=id)
     updatedriver.name=name
     updatedriver.adharnumber=adharnumber
     updatedriver.licencenumber=licencenumber
     updatedriver.issuedates=issuedates
     updatedriver.trdates=trdates
     updatedriver.img=img
     updatedriver.fname=fname
     updatedriver.save()
     messages.success(request, "Driver update deleted successfully.")
     return redirect('showdrivers')



# TripExpense

# def tripexpense(request):
#     if request.method =="POST":
#       tankerno = request.POST['tankerno']
#       tripdate = request.POST['tripdate']
#       tdate = request.POST['tdate']
#       drivername = request.POST['drivername']
#       fromconsignor = request.POST['fromconsignor']
#       toconsignee = request.POST['toconsignee']
#       trip_general_expenses = request.POST['trip_general_expenses']
#       food_allowance = request.POST['food_allowance']
#       bhatta =request.POST['bhatta']
#       washing_charges_tank =request.POST['washing_charges_tank']
#       total_amount = request.POST['total_amount']

#       if TripExpense.objects.filter(tankerno=tankerno,tdate=tdate).exists():
#           messages.error(request, 'Trip Expense already exists !!')
#           return redirect('trip-expense')
#       else:
#          res=TripExpense(tankerno=tankerno,tripdate=tripdate,tdate=tdate,drivername=drivername,fromconsignor=fromconsignor,toconsignee=toconsignee,trip_general_d=trip_general_expenses,food_allowance=food_allowance,bhatta=bhatta,washing_charges_tank=washing_charges_tank,total_amount=total_amount)
#          res.save()
#          messages.success(request, 'Trip expense added successfully !!') 
      
    
#     vehicle=Add_Vehicle.objects.all()
#     company=companydetails.objects.all()
#     dname=NewDriver_Details.objects.all()
#     context={'vehicle':vehicle,'company':company,'dname':dname}
#     return render(request,'add/add-trip-expense.html',context)





# def  showtripexpense(request):
#      expense=TripExpense.objects.all()
#      context={'expense':expense}
#      return render(request,'show-trip-expense.html',context)









def get_subcategories(request, category_id):
    # Fetch subcategories based on the selected category
    subcategories = SubCategory.objects.filter(category_id=category_id)
    subcategories_data = [sub.name for sub in subcategories]  # List of subcategory name
    return JsonResponse(subcategories_data, safe=False)

def  addsalary(request):
    if request.method =="POST":
      tankerno = request.POST['tankerno']
      drivername = request.POST['drivername']
      salary_driver  = request.POST['salary_driver']
      f_date = request.POST['f_date']
      t_date= request.POST['t_date']
      p_date = request.POST['p_date'] 
      amount = request.POST['amount'] 
      
    
      if Driver_salary.objects.filter(tankerno=tankerno,p_date=p_date).exists():
        messages.error(request, 'Driver Salar already exists !!')
        return redirect('add-salary')
      else:
        d_salary=Driver_salary(tankerno=tankerno,drivername=drivername,salary_driver=salary_driver,f_date=f_date,t_date=t_date,p_date=p_date,amount=amount)
        d_salary.save()
        messages.success(request, 'Driver Salary added successfully !!')
        return redirect('show-s')
    vehicle=Add_Vehicle.objects.all() 
    dname=NewDriver_Details.objects.all()  
    context={'vehicle':vehicle,'dname':dname}    
    return render(request,'driver-salary.html',context)

def  showsalary(request):
    show_s=Driver_salary.objects.all()
    context={'show_s':show_s}
    return render(request,'show/show_salary.html',context)


def dsalary(request,id):
    d=Driver_salary.objects.get(pk=id)
    d.delete()
    return redirect('show-s')

def usalary(request,id):
    upsalary=Driver_salary.objects.get(pk=id)
    vehicle=Add_Vehicle.objects.all() 
    dname=NewDriver_Details.objects.all()  
    context={'vehicle':vehicle,'dname':dname,'upsalary':upsalary}    
    return render(request,'update_salary.html',context)


def do_update_salary(request,id):
    tankerno = request.POST.get('tankerno')
    drivername = request.POST.get('drivername')
    salary_driver  = request.POST.get('salary_driver')
    f_date = request.POST.get('f_date')
    t_date= request.POST.get('t_date')
    p_date = request.POST.get('p_date')
    amount = request.POST.get('amount')

    upsalary=Driver_salary.objects.get(pk=id)

    upsalary.tankerno=tankerno
    upsalary.drivername=drivername
    upsalary.salary_driver=salary_driver
    upsalary.f_date= f_date
    upsalary.t_date= t_date
    upsalary.p_date= p_date
    upsalary.amount= amount
    upsalary.save()
    messages.success(request, 'Driver Salary Update successfully !!')
    return redirect('show-s')



def report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    trips = Trip.objects.all()

    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            trips = trips.filter(trip_date__range=(from_date_obj, to_date_obj))
        except ValueError:
            pass  # Invalid date format, ignore the filter
    trips = Trip.objects.all()
    expenses = Expense.objects.all()
    total_expense_sum = trips.aggregate(Sum('total_expense'))['total_expense__sum']
    combined = zip(trips, expenses)
    context={'combined':combined,'grand_total': total_expense_sum or 0,}  

    return render(request, 'reports.html', context)







def vehicledetails(request):
    if request.method == "POST":
        vehicle_name = request.POST['vehicle_name']
        tankercap = request.POST['tankercap']
        owner_name = request.POST['owner_name']
        making_year = request.POST['making_year']
        chassise_no = request.POST['chassise_no']
        engine_no = request.POST['engine_no']
        insurance_date = request.POST['insurance_date']
        insurance_img = request.FILES.get('insurance_img') 
        state_permit = request.POST['state_permit']
        state_img = request.FILES.get('state_img') 
        national_permit = request.POST['national_permit']
        national_img = request.FILES.get('national_img')
        fitness_date = request.POST['fitness_date']
        fitness_img = request.FILES.get('fitness_img')
        tax_date = request.POST['tax_date']
        tax_img = request.FILES.get('tax_img')
        puc_date = request.POST['puc_date']
        puc_img = request.FILES.get('puc_img')
        status = request.POST['status']

        # 👇 Replace with actual logged-in user's email if available
        # user_email = 'user@example.com'

        if Add_Vehicle.objects.filter(vehicle_name=vehicle_name).exists():
            messages.error(request, 'Vehicle No. already exists !!')
            return redirect('addvehicle')

        # Save vehicle data
        vehicle_details = Add_Vehicle(
            vehicle_name=vehicle_name if vehicle_name else None,
            tankercap=tankercap if tankercap else None,
            owner_name=owner_name if owner_name else None,
            making_year=making_year if making_year else None,
            chassise_no=chassise_no if chassise_no else None,
            engine_no=engine_no if engine_no else None,
            insurance_date=insurance_date if insurance_date else None,
            insurance_img=insurance_img if insurance_img else None,

            state_permit=state_permit if state_permit else None,
            state_img= state_img if  state_img else None,
            national_permit=national_permit if national_permit else None,
            national_img= national_img if  national_img else None,

            fitness_date=fitness_date if fitness_date else None,
            fitness_img= fitness_img if  fitness_img else None,
            tax_date=tax_date if tax_date else None,
            tax_img= tax_img if  tax_img else None,
            puc_date=puc_date if puc_date else None,
            puc_img= puc_img if puc_img else None,
            status=status if status else None
        )
        vehicle_details.save()
        messages.success(request, 'Vehicle details added successfully!!')
        return redirect('show-vehicle')

        # === Alert generation for near-expiry dates ===
        # alerts = []
        # today = datetime.today().date()
        # threshold = today + timedelta(days=5)

        # date_fields = {
        #     'Insurance': insurance_date,
        #     'State Permit': state_permit,
        #     'National Permit': national_permit,
        #     'Fitness Certificate': fitness_date,
        #     'Road Tax': tax_date,
        #     'PUC': puc_date
        # }

        # for label, date_str in date_fields.items():
        #     try:
        #         exp_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        #         if today <= exp_date <= threshold:
        #             alerts.append(f"🔔 {label} is expiring on {exp_date}")
        #     except ValueError:
        #         alerts.append(f"⚠️ Invalid date for {label}: {date_str}")

        # if alerts:
        #     alert_msg = "\n".join(alerts)

        #     # ✉️ Send email
        #     send_test_email(
        #         subject='Upcoming Vehicle Document Expiry Alerts',
        #         message=alert_msg,
        #         from_email='your@email.com',  # 👈 Replace with real sender
        #         recipient_list=[user_email],
        #         fail_silently=False,
        #     )

        # messages.success(request, 'Vehicle details added successfully (Email sent if any expiry alert) !!')
        # return redirect('show-vehicle')

    return render(request, 'add/add-vehicle.html')


def get_capacity(request):
    vehicle_name = request.GET.get('vehicle_name')
    try:
        tanker = Add_Vehicle.objects.get(vehicle_name=vehicle_name)
        return JsonResponse({'tankercap': tanker.tankercap})
    except Add_Vehicle.DoesNotExist:
        return JsonResponse({'tankercap': None})

def show_vehicledetails(request):
    showvehicle=Add_Vehicle.objects.all()
    context={'showvehicle':showvehicle}
    return render(request,'show/show-vehicle-details.html',context)


def deletevehicle(request,id):
    showvehicle=Add_Vehicle.objects.get(pk=id)
    showvehicle.delete()
    return redirect('show-vehicle')

def updatevehicle(request,id):
    upvehicle=Add_Vehicle.objects.get(pk=id)
    context={'upvehicle':upvehicle}
    return render(request,'update_vehicle.html',context)



def doupdatevehicle(request, id):
    try:
        # Fetch the vehicle by its ID
        upvehicle = Add_Vehicle.objects.get(pk=id)

        if request.method == "POST":
            vehicle_name = request.POST.get('vehicle_name')
            tankercap = request.POST.get('tankercap')
            owner_name = request.POST.get('owner_name')
            making_year = request.POST.get('making_year')
            chassise_no = request.POST.get('chassise_no')
            engine_no = request.POST.get('engine_no')
            insurance_date = request.POST.get('insurance_date')
            insurance_img = request.FILES.get('insurance_img')
            state_permit = request.POST.get('state_permit')
            state_img = request.FILES.get('state_img')
            national_permit = request.POST.get('national_permit')
            national_img = request.FILES.get('national_img')
            fitness_date = request.POST.get('fitness_date')
            fitness_img = request.FILES.get('fitness_img')
            tax_date = request.POST.get('tax_date')
            tax_img = request.FILES.get('tax_img')
            puc_date = request.POST.get('puc_date')
            puc_img = request.FILES.get('puc_img')
            status = request.POST.get('status')

            # Update the fields
            upvehicle.vehicle_name = vehicle_name
            upvehicle.tankercap = tankercap
            upvehicle.owner_name = owner_name
            upvehicle.making_year = making_year
            upvehicle.chassise_no = chassise_no
            upvehicle.engine_no = engine_no
            upvehicle.insurance_date = insurance_date
            if insurance_img:
               upvehicle.insurance_img = insurance_img if insurance_img else None
            upvehicle.state_permit = state_permit
            if state_img:
               upvehicle.state_img = state_img if  state_img else None
            upvehicle.national_permit = national_permit
            if national_img:
               upvehicle.national_img= national_img if  national_img else None

            upvehicle.fitness_date = fitness_date
            if fitness_img:
                upvehicle.fitness_img= fitness_img if  fitness_img else None

            upvehicle.tax_date = tax_date
            if tax_date:
                upvehicle.tax_img= tax_img if  tax_img else None

            upvehicle.puc_date = puc_date
            if puc_date:
                upvehicle.puc_img= puc_img if puc_img else None
            upvehicle.status = status
            # Save the updated vehicle
            upvehicle.save()
            messages.success(request, 'Vehicle details updated successfully!')
            return redirect('show-vehicle')
        
        # If the method is GET, render the update form with current vehicle data
        return render(request, 'update_vehicle.html', {'vehicle': upvehicle})

    except Add_Vehicle.DoesNotExist:
        messages.error(request, 'Vehicle not found!')
        return redirect('show-vehicle')



 


def company_details(request):
    if request.method =="POST":
      name  = request.POST['name']
      area_name = request.POST['area_name']
      short_name = request.POST['short_name']
      state = request.POST['state']
      city = request.POST['city']
      pincode = request.POST['pincode']
      gst = request.POST['gst']
      pan = request.POST['pan']
      contact_no = request.POST['contact_no']

      if  companydetails.objects.filter(name=name,area_name=area_name).exists():
          messages.error(request, 'Company already exists !!')
          return redirect('company-details')
      else:
          cname=companydetails(name=name,area_name=area_name,state=state,city=city if city else None,pincode=pincode if pincode else None,gst=gst if gst else None,pan=pan if pan else None,contact_no=contact_no if contact_no else None,short_name=short_name if short_name else None)
          cname.save()
          messages.success(request, 'Company details added successfully !!') 
          return redirect('s-company')
    city=City.objects.all()
    state=State.objects.all()
    context={'city':city,'state':state}
    return render(request,'add/add_company.html',context)


def show_company(request):
    cshow=companydetails.objects.all()
    context={'cshow':cshow}
    return render(request,'show/show_company.html',context)

def delete_company(request,id):
    dcompany=companydetails.objects.get(pk=id)
    dcompany.delete()
    return redirect('s-company')


def updatecompany(request,id):
    upcompany=companydetails.objects.get(pk=id)
    context={'upcompany':upcompany}
    return render(request,'update_company_details.html',context)

def doupdatecompany(request,id):
      name  = request.POST.get('name')
      area_name = request.POST.get('area_name')
      short_name = request.POST.get('short_name')
      state = request.POST.get('state')
      city = request.POST.get('city')
      pincode = request.POST.get('pincode')
      gst = request.POST.get('gst')
      pan = request.POST.get('pan')
      contact_no = request.POST.get('contact_no')
      
      upcompany=companydetails.objects.get(pk=id)

      upcompany.name=name if name else None
      upcompany.area_name=area_name if area_name else None
      upcompany.short_name=short_name if short_name else None
      upcompany.state=state if state else None
      upcompany.city=city if city else None
      upcompany.pincode=pincode if pincode else None
      upcompany.gst=gst if gst else None
      upcompany.pan=pan if pan else None
      upcompany.contact_no=contact_no if contact_no else None

      upcompany.save()
      messages.success(request, 'Company details update successfully !!')
      return redirect('s-company')








def all_bill(request):

    return render(request,'all-bills.html')






def start_trip(request):
    if request.method == 'POST':
        try:
            # Get data from POST request
            trip_id = request.POST.get('trip_id')
            tanker = request.POST.get('tanker')
            trip_date = request.POST.get('trip_date')
            from_id = request.POST.get('from_id')
            To_id = request.POST.get('To_id')
            drivername = request.POST.get('drivername')
            f_trip = request.POST.get('f_trip')

            # Check if a trip with this trip_id already exists
            existing_trip = Trip.objects.filter(trip_id=trip_id).first()
            if existing_trip:
                # If a trip with the same trip_id exists, redirect to the 'add_expense' page for that trip
                return redirect('add_expense', trip_id=existing_trip.trip_id)

            # If no trip with the same trip_id exists, create a new trip
            if trip_id:
                trip = Trip.objects.create(
                    trip_id=trip_id,
                    tanker=tanker,
                    trip_date=trip_date,
                    from_id=from_id,
                    To_id=To_id,
                    drivername=drivername,
                    f_trip=f_trip if f_trip else None
                )
                # After creating the trip, redirect to the 'add_expense' page for the newly created trip
                return redirect('add_expense', trip_id=trip.trip_id)
        
        except Exception as e:
            # Catch any general exception and show an error message
            messages.error(request, f"Please fill the date fields")
            return redirect('start_trip')  # Redirect to the same page if an error occurs

    # For a GET request, or after the POST is processed, get the necessary context data
    try:
        vehicle = Add_Vehicle.objects.all()
        company = companydetails.objects.all()
        dname = NewDriver_Details.objects.all()
        context = {'vehicle': vehicle, 'company': company, 'dname': dname}
    except Exception as e:
        messages.error(request, f"Error loading data: {str(e)}")
        context = {'vehicle': [], 'company': [], 'dname': []}  # Empty lists if an error occurs

    return render(request, 'exp/start_trip.html', context)





def add_expense(request, trip_id):
    # Get the trip object based on trip_id, handle the case of multiple trips
    trips = Trip.objects.filter(trip_id=trip_id)  # Use filter() instead of get()

    if trips.count() == 1:
        trip = trips.first()  # If exactly one trip is found, use it
    elif trips.count() > 1:
        trip = trips.first()  # For now, we're picking the first one
        

    # Handle the POST request for adding expenses
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        trip_general_expenses = request.POST.get('trip_general_expenses')
        food_allowance = request.POST.get('food_allowance')
        bhatta = request.POST.get('bhatta')
        washing_charges_tank = request.POST.get('washing_charges_tank')
        actual_amount=request.POST.get('actual_amount')
        total_amount = request.POST.get('total_amount')
        toll_date = request.POST.get('toll_date')
        toll_amount = request.POST.get('toll_amount')
        toll_name = request.POST.get('toll_name')
        category = request.POST.get('category')
        subCategory = request.POST.get('subCategory')
        paid_to = request.POST.get('paid_to')
        amount_given = request.POST.get('amount_given')
        liters = request.POST.get('liters')
        rate = request.POST.get('rate')
        total_diesel = request.POST.get('total_diesel')
        paid_date = request.POST.get('paid_date')
        bill_date = request.POST.get('bill_date')
        urea_liter = request.POST.get('urea_liter')
        urea_rate = request.POST.get('urea_rate')
        urea_total = request.POST.get('urea_total')
        r_paid_date = request.POST.get('r_paid_date')
        r_bill_date = request.POST.get('r_bill_date')
        spare_part = request.POST.get('spare_part')
        r_amount = request.POST.get('r_amount')
        part_name = request.POST.get('part_name')
        no_piece = request.POST.get('no_piece')
        from_via = request.POST.get('from_via')
        To_via = request.POST.get('To_via')
        end_date = request.POST.get('end_date')
        

        if amount :
            expense = Expense.objects.create(
                trip=trip, 
                amount=float(amount), 
                description=description,
                date=date if date else None,
                trip_general_expenses=trip_general_expenses if trip_general_expenses else None,
                food_allowance=food_allowance if food_allowance else None,
                bhatta=bhatta if bhatta else None,
                washing_charges_tank=washing_charges_tank if washing_charges_tank else None,
                actual_amount=actual_amount if actual_amount else None,
                total_amount=float(total_amount) if total_amount else None,
                toll_date=toll_date if toll_date else None,
                toll_amount=float(toll_amount) if toll_amount else None,
                toll_name=toll_name if toll_name else None,
                category=category if category else None,
                subCategory=subCategory if subCategory else None,
                paid_to= paid_to if paid_to else None,
                amount_given=amount_given if amount_given else None,
                liters=liters if liters else None,
                rate=rate if rate else None,
                total_diesel=float(total_diesel) if total_diesel else None,
                paid_date=paid_date if paid_date else None,
                bill_date=bill_date if bill_date else None,
                urea_liter=urea_liter if urea_liter else None,
                urea_rate=urea_rate if urea_rate else None,
                urea_total=float(urea_total) if urea_total else None,
                r_paid_date=r_paid_date if r_paid_date else None,
                r_bill_date=r_bill_date if r_bill_date else None,
                spare_part=spare_part if spare_part else None,
                r_amount=r_amount if r_amount else None,
                part_name=part_name if part_name else None, 
                no_piece=no_piece if no_piece else None,
                from_via=from_via if from_via else None,
                To_via= To_via if To_via else None,
                end_date= end_date if end_date else None,

            )
            messages.success(request, 'Trip Add successfully !!')
            trip.calculate_total_expense()  # Recalculate total expense after adding a new expense
            return redirect('add_expense', trip_id=trip.trip_id)
    
    # Get all expenses related to the trip
    expenses = trip.expenses.all()
    categories = Category.objects.all()
    dname = NewDriver_Details.objects.all()
    petrol = AddPetrolPump.objects.all()
    company = companydetails.objects.all()
    # Return the response
    context = {'categories': categories, 'dname': dname, 'petrol': petrol,'trip': trip,
        'expenses': expenses,'company':company}
    return render(request, 'exp/add_expense.html',context)


def update_exp(request,id):
    exp=Expense.objects.get(pk=id)
    categories = Category.objects.all()
    dname = NewDriver_Details.objects.all()
    petrol = AddPetrolPump.objects.all()
    company = companydetails.objects.all()
    context={'exp':exp,'categories': categories, 'dname': dname, 'petrol': petrol,'company':company}
    return render(request,'update_exp.html',context)


def do_update(request,id):
 try:
     trip_general_expenses = request.POST.get('trip_general_expenses')
     food_allowance = request.POST.get('food_allowance')
     bhatta = request.POST.get('bhatta')
     washing_charges_tank = request.POST.get('washing_charges_tank')
     actual_amount = request.POST.get('actual_amount')
     total_amount = request.POST.get('total_amount')
     toll_amount = request.POST.get('toll_amount')
     toll_name = request.POST.get('toll_name')
     category = request.POST.get('category')
     subCategory = request.POST.get('subCategor')
     paid_to = request.POST.get('paid_to')
     amount_given = request.POST.get('amount_given')
     liters = request.POST.get('liters')
     rate = request.POST.get('rate')
     total_diesel = request.POST.get('total_diesel')
     paid_date = request.POST.get('paid_date')
     bill_date = request.POST.get('bill_date')
     urea_liter = request.POST.get('urea_liter')
     urea_rate = request.POST.get('urea_rate')
     urea_total = request.POST.get('urea_total')
     r_paid_date = request.POST.get('r_paid_date')
     r_bill_date = request.POST.get('r_bill_date')
     spare_part = request.POST.get('spare_part')
     r_amount = request.POST.get('r_amount')
     part_name = request.POST.get('part_name')
     no_piece = request.POST.get('no_piece')
     date = request.POST.get('date')
     from_via = request.POST.get('from_via')
     To_via = request.POST.get('To_via')
     amount = request.POST.get('amount')
     end_date = request.POST.get('end_date')
  
     upexpense = Expense.objects.get(pk=id)
     trip_id =upexpense.trip.trip_id

     upexpense.trip_general_expenses = trip_general_expenses or None
     upexpense.food_allowance = food_allowance or None
     upexpense.bhatta = bhatta or None
     upexpense.washing_charges_tank = washing_charges_tank or None
     upexpense.actual_amount = actual_amount or None
     upexpense.total_amount = total_amount or None
     upexpense.toll_name = toll_name or None
     upexpense.toll_amount = toll_amount or None
     upexpense.category = category or None
     upexpense.subCategory = subCategory or None
     upexpense.paid_to = paid_to or None
     upexpense.amount_given = amount_given or None
     upexpense.liters = liters or None
     upexpense.rate = rate or None
     upexpense.total_diesel = total_diesel or None
     upexpense.paid_date = paid_date or None
     upexpense.bill_date = bill_date or None
     upexpense.urea_liter = urea_liter or None
     upexpense.urea_rate = urea_rate or None
     upexpense.urea_total = urea_total or None
     upexpense.r_paid_date = r_paid_date or None
     upexpense.r_bill_date = r_bill_date or None
     upexpense.spare_part = spare_part or None
     upexpense.r_amount = r_amount or None
     upexpense.part_name = part_name or None
     upexpense.no_piece = no_piece or None
     upexpense.date = date or None
     upexpense.amount = amount or None
     upexpense.end_date=end_date or None

     upexpense.save()
     messages.success(request, 'Expense updated successfully!')
     return redirect('add_expense', trip_id=trip_id)

 except Expense.DoesNotExist:
        messages.error(request, 'Expense not found.')
        return redirect('start_trip')

 except Exception as e:
        messages.error(request, f'Error in expense: {str(e)}')
        return redirect('start_trip')
   



# def delete_expense(request,id):
#     de=Expense.objects.get(pk=id)
#     if Expense.objects.filter(date=date).exists(): 
#          messages.error(request, "Trip has already started. Expense cannot be deleted.")
#          return redirect('start_trip')
#     de.delete()
#     return redirect('start_trip')
def delete_expense(request, id):
    # de = get_object_or_404(Expense, pk=id)

    # # Trip already started check based on date
    # if Expense.objects.filter(date=de.date).exists():
    #     messages.error(request, "Trip has already started. Expense cannot be deleted.")
    #     return redirect('start_trip')
    de=Expense.objects.get(pk=id)
    trip_id =de.trip.trip_id
    de.delete()
    messages.success(request, "Expense deleted successfully.")
    return redirect('add_expense', trip_id=trip_id)



# def end_trip(request, trip_id):
#     if request.method == 'POST':
#         end_time = request.POST.get('end_time')
#     # Get the trip object based on trip_id, handle the case of multiple trips
#     trips = Trip.objects.filter(trip_id=trip_id)

#     if trips.count() == 1:
#         trip = trips.first()  # If exactly one trip is found
#     elif trips.count() > 1:
#         trip = trips.first()  # If multiple trips, select the first one (you can handle it as needed)
#     else:
#         return render(request, '404.html')  # If no trip found, return 404 or an appropriate response
    
#     # Mark the trip as ended
#     trip.end_time = timezone.now()  # Set the end time
#     trip.is_active = False  # Set is_active to False
#     trip.calculate_total_expense()  # Recalculate the total expenses for the trip
#     trip.save()

#     # Redirect to a page showing the details of the ended trip
#     return render(request, 'exp/end_trip.html', {'trip': trip})


def AllTrip(request):
    # Fetch all trip records from the database
    t = Trip.objects.all()

    # Fetch all expense records from the database
    expense = Expense.objects.all()
    # Pass the trip, expense, and profit/loss data to the template
    context = {
        't': t,
        'expense': expense,
    }

    return render(request, 'show/all_trip.html', context)



def del_allTrip(request,id):
    d=Trip.objects.get(pk=id)
    d.delete()
    return redirect('trip')


def SignUp(request):
    
    return render(request,'form/signup.html')





def Login(request):
    if request.method == 'POST':  # Make sure the method is POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in

             # Username ke hisaab se redirect
            if user.username == 'haider':
                return redirect('udashboard')  # isko URL me define karo
            elif user.username == 'Pooja':
                return redirect('ldashboard')  # isko bhi define karo
            elif user.username == 'Gemini':
                return redirect('gemini')  # isko bhi define karo
            else:
                return redirect('dashboard')  # Redirect to the dashboard page
        
        else:
            messages.error(request, ' Name and Password is incorrect !!')
            return redirect('log-in') 
    
    return render(request, 'form/login.html')





def Logout_user(request):
    logout(request)
    return redirect('log-in')


# ---------------------Loan-----------------------#
def addbank(request):
    if request.method == "POST":
        name = request.POST.get('name')  # Use .get() to avoid KeyError
        if name:
            bankname = AddBank_Loan.objects.create(name=name)
            bankname.save()
       

    # Fetch all banks regardless of POST or GET request
    bname=AddBank_Loan.objects.all()
    context = {'bname': bname,}

    return render(request, 'add/add_bank_name.html')


def addloan(request):
    if request.method=="POST":
        tankerno=request.POST.get('tankerno')
        loan_contract=request.POST.get('loan_contract')
        finance_by=request.POST.get('finance_by')
        pamount=request.POST.get('pamount')
        iamount=request.POST.get('iamount')
        famount=request.POST.get('famount')
        amount=request.POST.get('amount')
        ddate=request.POST.get('ddate')
        pdate=request.POST.get('pdate')
        days=request.POST.get('days')
        bank=request.POST.get('bank')
        ramount=request.POST.get('ramount')

        if Addloan.objects.filter(tankerno=tankerno,loan_contract=loan_contract).exists():
           messages.error(request, 'Loan already exists!')
           return redirect('loandetails')
        else:
            loan=Addloan.objects.create(tankerno=tankerno,loan_contract=loan_contract,finance_by=finance_by,pamount=pamount,iamount=iamount,famount=famount,amount=amount,ddate=ddate,pdate=pdate,days=days,bank=bank,ramount=ramount)
            loan.save()
            messages.success(request, 'Loan Details added successfully!')
            return redirect('loan-show')
    vehicle=Add_Vehicle.objects.all()
    bname=AddBank_Loan.objects.all()
    context={'vehicle':vehicle,'bname': bname,}
    return render(request,'loan-details.html',context)


def showloan(request):
    loanshow=Addloan.objects.all()
    context={'loanshow':loanshow}
    return render(request,'show/show_loan.html',context)

def ldelete(request,id):
    ldel=Addloan.objects.get(id=id)
    ldel.delete()
    return redirect('loan-show')






def calculate_emi(principal, annual_rate, tenure_months):
    # Convert annual interest rate to monthly interest rate
    monthly_rate = (annual_rate / 100) / 12

    # EMI formula
    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
    return emi

def emi_calculator(request):
    # Default values for the input fields
    principal = 0
    annual_rate = 0
    tenure_months = 0
    emi = 0

    # Check if it's a POST request
    if request.method == 'POST':
        try:
            principal = float(request.POST.get('principal_amount'))
            annual_rate = float(request.POST.get('annual_interest_rate'))
            tenure_months = int(request.POST.get('loan_tenure_months'))

            # Calculate EMI
            emi = calculate_emi(principal, annual_rate, tenure_months)
        except (ValueError, TypeError):
            return HttpResponse("Invalid input. Please enter valid numbers.")

    return render(request, 'emi_calculator.html', {'emi': emi, 'principal': principal, 'annual_rate': annual_rate, 'tenure_months': tenure_months})
   

def AddDriverLoan(request):
    if request.method=='POST':
      tankerno=request.POST['tankerno']
      From_address=request.POST['From_address']
      To_address=request.POST['To_address']
      drivername=request.POST['drivername']
      trip_date=request.POST['trip_date']
      date=request.POST['date']
      load=request.POST['load']
      unload=request.POST['unload']
      short_kg=request.POST['short_kg']
      allow_kg = request.POST['allow_kg']
      actual_short = request.POST['actual_short']
      rate = request.POST['rate']
      short_amount = request.POST['short_amount']
      previous_loan = request.POST['previous_loan']
      loan_amount = request.POST['loan_amount']
      total = request.POST['total']
      if  DriverLoan.objects.filter(tankerno=tankerno,trip_date=trip_date,date=date).exists():
          messages.error(request, 'Driver Loan exists !!')
          return redirect('drivers-loan')
      else:
          d_loan=DriverLoan.objects.create(
          tankerno= tankerno if tankerno else None,
          From_address=From_address if From_address else None,
          To_address=From_address if To_address else None,
          drivername=drivername if drivername else None,
          trip_date=trip_date if trip_date else None,
          date=date if date else None,
          load=load if load else None,
          unload=unload if unload else None,
          short_kg=short_kg if short_kg else None,
          allow_kg=allow_kg if allow_kg else None,
          actual_short=actual_short if actual_short else None,
          rate=rate if rate else None,
          short_amount=short_amount if short_amount else None,
          previous_loan=previous_loan if previous_loan else None,
          loan_amount=loan_amount if loan_amount else None,
          total = total if total else None,
        )
      d_loan.save()
      messages.success(request, 'Driver Loan Add successfully!')

    shortage=Expense.objects.filter().last()
    vehicle=Add_Vehicle.objects.all()
    dname=NewDriver_Details.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname,'shortage':shortage,'company':company}
    return render(request,'add/add_driver_loan.html',context)



def ShowLoan(request):
    Loan=DriverLoan.objects.all()
    return render(request,'show/show_driver_loan.html',{'Loan':Loan})

def deleteloan(request,id):
    d=DriverLoan.objects.get(pk=id)
    d.delete()
    return redirect('show-loan')

def updriverloan(request,id):
    updatedl=DriverLoan.objects.get(pk=id)
    context={'updatedl':updatedl}
    return render(request,'update_driver_loan.html',context)

def do_update_dloan(request,id):
      tankerno=request.POST.get('tankerno')
      From_address=request.POST.get('From_address')
      To_address=request.POST.get('To_address')
      drivername=request.POST.get('drivername')
      trip_date=request.POST.get('trip_date')
      date=request.POST.get('date')
      load=request.POST.get('load')
      unload=request.POST.get('unload')
      short_kg=request.POST.get('short_kg')
      allow_kg = request.POST.get('allow_kg')
      actual_short = request.POST.get('actual_short')
      rate = request.POST.get('rate')
      short_amount = request.POST.get('short_amount')
      previous_loan = request.POST.get('previous_loan')
      loan_amount = request.POST.get('loan_amount')
      total = request.POST.get('total')
      updatedl=DriverLoan.objects.get(pk=id)

      updatedl.tankerno=tankerno
      updatedl.From_address=From_address
      updatedl.To_address=To_address
      updatedl.drivername=drivername
      updatedl.trip_date=trip_date
      updatedl.date=date
      updatedl.load=load
      updatedl.unload=unload
      updatedl.short_kg=short_kg
      updatedl.allow_kg=allow_kg
      updatedl.actual_short=actual_short
      updatedl.rate=rate
      updatedl.short_amount=short_amount
      updatedl.previous_loan=previous_loan
      updatedl.loan_amount=loan_amount
      updatedl.total=total
      updatedl.save()
      messages.success(request, 'Driver Loan Details Update Successfully!')
      return redirect('show-loan')





def generate_bill(request):
    bill = {
        "bill_no": "12345",
        "company": "ABC Corp",
        "gst": "27CMDOM1641J1Z1",
        "date": "2025-03-17",
        "amount": "5000",
        "total_in_words": "Five Thousand Only",
        "union_charge": "200",
        # Add other necessary bill details here
    }

    # Pass the bill object to the template
    return render(request, "invoice_template.html", {"bill": bill})




def tracking(request):
    if request.method == 'POST':
        tanker_no = request.POST['tanker_no']
        location = request.POST['location']
        date = request.POST['date']
        tdate = request.POST['tdate']
        destination = request.POST['destination']
        vehicle_status= request.POST['vehicle_status']
        
        if  Tracking.objects.filter(tanker_no=tanker_no,tdate=tdate).exists():
            messages.error(request, 'Vehicle status already exists !!')
            return redirect('vehicle-track')
        else:
             Tracking.objects.create(
             tanker_no= tanker_no,
             location=location,
             date=date,
             tdate=tdate,
             destination=destination,
             vehicle_status=vehicle_status,)
             messages.success(request, 'Status added successfully !!') 
        # return redirect('vehicle_list')  # ya jo bhi aapka page ho
        
    vehicle=Add_Vehicle.objects.all()
    context={'vehicle':vehicle}
    return render(request, 'add/vehicle_tracking.html',context)



def showtrack(request):
    track=Tracking.objects.all()
    context={'track':track}
    return render(request,'show/show_track.html',context)



def errorpage(request):
    return render(request,'page_404.html')


def addbank(request):
    if request.method=="POST":
        name=request.POST['name']
        if AddBank_Loan.objects.filter(name=name).exists():
           messages.error(request, 'Please enter the Bank Name !!')
           return redirect('add-bank')
        
        else:
            bank=AddBank_Loan.objects.create(name=name)
            bank.save()
            messages.success(request, 'Bank Name add successfully !!')
    return render (request,'add/add_bank_name.html')



def get_cities(request):
    state = request.GET.get('state')
    cities = City.objects.filter(state__statename=state).values_list('cityname', flat=True)
    return JsonResponse({'cities': list(cities)})




def send_test_email(request):
    send_mail(
        subject='Test Email from Django',
        message='Hello bhai! Django se email successfully bhej diya gaya hai.',
        from_email='abc123@gmail.com',  # ← apna Gmail yahan likho
        recipient_list=['kisi.kodost@gmail.com'],  # ← jisko bhejna hai
        fail_silently=False,
    )
    return HttpResponse("Email sent successfully!")



def addtolls(request):
    if request.method =="POST":
      tankerno  = request.POST['tankerno']
      driver_names = request.POST['driver_names']
      From_address = request.POST['From_address']
      To_address = request.POST['To_address']
      trip_date = request.POST['trip_date']
      amount=request.POST['amount']
      status = request.POST['status']
      if  Toll_Details.objects.filter(tankerno=tankerno,trip_date=trip_date).exists():
          messages.error(request, 'Toll already exists !!')
          return redirect('add-toll')
      else:
          toll=Toll_Details(tankerno=tankerno,driver_names=driver_names,trip_date=trip_date,From_address=From_address,To_address=To_address,amount=amount,status=status)
          toll.save()
          messages.success(request, 'Toll details added successfully !!')
          return redirect('toll-details')
    vehicle=Add_Vehicle.objects.all()
    # dname=DriverName.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname}
    return render(request,'add/add-toll.html', context)




def tolldetails(request):
    # Get filters from GET parameters
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    tankerno = request.GET.get('tankerno')
    driver_names = request.GET.get('driver_names')
    from_address = request.GET.get('From_address')
    to_address = request.GET.get('To_address')

    show = Toll_Details.objects.all()

    # Apply filters
    if tankerno:
        show = show.filter(tankerno__icontains=tankerno)

    if driver_names:
        show = show.filter(driver_names__icontains=driver_names)

    if from_address:
        show = show.filter(From_address__icontains=from_address)

    if to_address:
        show = show.filter(To_address__icontains=to_address)

    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            show = show.filter(trip_date__range=(from_date_obj, to_date_obj))
        except ValueError:
            pass  # Invalid date format

    # Calculate total toll amount
    total_toll_sum = show.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'show': show,
        'total_toll_sum': total_toll_sum,
    }
    return render(request, 'show/show-toll.html', context)



def tolldelete(request,id):
    d=Toll_Details.objects.get(pk=id)
    d.delete()
    return redirect('toll-details')


def updatedelete(request,id):
    uptoll=Toll_Details.objects.get(pk=id)
    context={'uptoll':uptoll}
    return render(request,'update_toll.html',context)

def doupdate_toll(request,id):
     tankerno  = request.POST.get('tankerno')
     driver_names = request.POST.get('driver_names')
     From_address = request.POST.get('From_address')
     To_address = request.POST.get('To_address')
     trip_date = request.POST.get('trip_date')
     amount=request.POST.get('amount')
     status = request.POST.get('status')

     uptoll=Toll_Details.objects.get(pk=id)
     uptoll.tankerno=tankerno
     uptoll.driver_names=driver_names
     uptoll.From_address=From_address
     uptoll.To_address=To_address
     uptoll.trip_date=trip_date
     uptoll.amount=amount
     uptoll.status=status
     uptoll.save()
     messages.success(request, 'Toll details Update successfully !!')
     return redirect('toll-details')

    


def AddPetrolp(request):
    if request.method=="POST":
        name=request.POST['name']
        if AddPetrolPump.objects.filter(name=name).exists():
           messages.error(request, 'Petrol Pump already exists !!')
           return redirect('add-petrol') 
        else:
            pname=AddPetrolPump(name=name)
            pname.save()
            messages.success(request, 'Petrol Pump added successfully !!')
    return render(request,'add/add_petrol_pump.html')


def showpertol(request):
    showpump=AddPetrolPump.objects.all()
    context={'showpump':showpump}
    return render(request,'show/petrol_pump.html',context)
    

def dpertol(request,id):
    dpump=AddPetrolPump.objects.get(pk=id)
    dpump.delete()
    return redirect('s-petrol')
    

##================Client Dashborad===================

def cgemini(request):
    showg = Clientgemini.objects.all().order_by('-create_date')[:3]
    context={'showg':showg}
    return render(request,'client/gemini.html',context)


def ordergemini(request):
    return render(request,'client/gemini_form.html')
    



def generate_order_id():
    date = datetime.now().strftime("%Y")
    serial_file = f"serial_{date}.txt"  # Year-wise file

    if os.path.exists(serial_file):
        with open(serial_file, "r") as file:
            serial = int(file.read().strip()) + 1
    else:
        serial = 1  # Start from 1 if file for this year doesn't exist

    with open(serial_file, "w") as file:
        file.write(str(serial))

    serial_str = str(serial).zfill(3)  # Pad with zeros to make 3 digits
    return f"GEM-{serial_str}{date}"

def geminiorder(request):
    if request.method == "POST":
       
       
        # Auto-generate order ID
        order_id = generate_order_id()

        # Other form fields
        tanker_type = request.POST['tanker_type']
        tanker_cpa = request.POST['tanker_cpa']
        fadd = request.POST['fadd']
        tadd = request.POST['tadd']
        ddate = request.POST['ddate']

        # Check uniqueness
        if  Clientgemini.objects.filter(fadd=fadd,tadd=tadd,ddate=ddate).exists():
            messages.error(request, 'Order already exists !!')
            return redirect('order-gemini')
        else:
         # Save order
            gorder = Clientgemini(
            order_id=order_id,
            tanker_type=tanker_type,
            tanker_cpa=tanker_cpa,
            fadd=fadd,
            tadd=tadd,
            ddate=ddate
        )
        gorder.save()
        messages.success(request, f'Order-: {order_id} add successfully! ')
        return redirect('order-show')

    return render(request, 'client/gemini_form.html')


def gorder(request):
    gshow=Clientgemini.objects.all()
    context={'gshow':gshow}
    return render (request,'client/show.html',context)


def companyorder(request):
    return render (request,'fresh_order.html')


#=====================Fresh Order By Companies======================


def freshgemini(request):
    fshow=Clientgemini.objects.all()
    context={'fshow':fshow}
    return render(request,'fresh_order/gemini_order.html',context)

def plangemini(request):
    return render(request,'fresh_order/plan_gemini.html')


# def create_bill(request):
#     if request.method == 'POST':
#         customer_name = request.POST.get('customer_name')
#         descriptions = request.POST.getlist('description')
#         quantities = request.POST.getlist('quantity')
#         rates = request.POST.getlist('rate')

#         total = 0
#         for q, r in zip(quantities, rates):
#             total += int(q) * float(r)

#         bill = Bills.objects.create(customer_name=customer_name, total_amount=total)

#         for desc, qty, rate in zip(descriptions, quantities, rates):
#             BillItem.objects.create(
#                 bill=bill,
#                 description=desc,
#                 quantity=int(qty),
#                 rate=float(rate)
#             )
#         return redirect('bill_list')

#     return render(request, 'create_bill.html')


# def bill_list(request):
#     bills = Bills.objects.all()
#     return render(request, 'bill_list.html', {'bills': bills})


# def bill_detail(request, bill_id):
#     bill = get_object_or_404(Bills, id=bill_id)
#     return render(request, 'bill_detail.html', {'bill': bill})



#================Billing System===============================

def Billing(request):
    adani=Invoice.objects.count()
    gemini=GInvoice.objects.count()
    akkinword=Aak_in_Invoice.objects.count()
    context={'adani':adani,'gemini':gemini,'akkinword':akkinword}
    return render(request,'billing.html',context)





#========================ADANI BILL====================================================
def generate_bill_no():
    now = datetime.now()  
    month = f"{now.month:02d}"  
    year = now.year
    random_number = random.randint(1000, 9999)  # 4-digit random


    if now.month >= 4:  # April se new financial year
        fy_start = str(year)[-2:]
        fy_end = str(year + 1)[-2:]
    else:
        fy_start = str(year - 1)[-2:]
        fy_end = str(year)[-2:]

    financial_year = f"{fy_start}-{fy_end}"

    # Final bill number
    bill_no = f"{random_number}/JN/{month}/{financial_year}"
    return bill_no


def extract_gst_code(gst_number):
    return gst_number[:2] if gst_number and isinstance(gst_number, str) and len(gst_number) >= 2 else ''


def extract_state(address):
    try:
        return address.split(',')[-1].strip().lower()
    except:
        return ''




def adani_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        unload = request.POST.get('unload')
        short = request.POST.get('short')
        retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            unload=unload,
            short=short,
            retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)

            # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)
        



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('invoice_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/adani.html', context)


def invoice_list(request):
    invoices = Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'invoice_list.html', {'invoices': invoices})


def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = Item.objects.filter(invoice=invoice)
    return render(request, 'invoice_detail.html', {'invoice': invoice, 'items': items})


#========================GEMINI BILL====================================================
def gemini_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        # unload = request.POST.get('unload')
        # short = request.POST.get('short')
        # retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if GInvoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = GInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            # tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            # unload=unload,
            # short=short,
            # retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price + 1500
                subtotal += line_total
                

                GItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)
       # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('ginvoice_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/gemini.html', context)


def Ginvoice_list(request):
    ginvoice = GInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/gemini_list.html', {'ginvoice': ginvoice})


def Ginvoice_detail(request, invoice_id):
    invoice = get_object_or_404(GInvoice, id=invoice_id)
    items = GItem.objects.filter(invoice=invoice)
    return render(request, 'bills/gemini_details.html', {'invoice': invoice, 'items': items})


#========================Ashland BILL====================================================
def ashland_bill(request):

    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        # unload = request.POST.get('unload')
        # short = request.POST.get('short')
        # retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        t_rate = request.POST.get('t_rate')
        tpar_day = request.POST.get('tpar_day')
        total_t = request.POST.get('total_t')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')
        tcharges = request.POST.get('tcharges')
        thsac = request.POST.get('thsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if AInvoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = AInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            # tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            # unload=unload,
            # short=short,
            # retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if charges else None,
            hsac=hsac if hsac else 0,
            tcharges=tcharges if tcharges else None,
            thsac=thsac if thsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if d_rate else 0,
            par_day=par_day if par_day else None,
            total_d=total_d if total_d else 0,
            t_rate=t_rate if t_rate else 0,
            tpar_day=tpar_day if tpar_day else None,
            total_t=total_t if total_t else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price + 0
                subtotal += line_total

                AItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = grand_total
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('ainvoice_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Ashland/ashland.html', context)


def Ainvoice_list(request):
    ainvoice = AInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Ashland/ashland_list.html', {'ainvoice': ainvoice})


def Ainvoice_detail(request, invoice_id):
    invoice = get_object_or_404(AInvoice, id=invoice_id)
    items = AItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Ashland/ashland_details.html', {'invoice': invoice, 'items': items})


#========================CARGILL BILL====================================================



#========================AAK INWORD BILL====================================================

def aakin_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        unload = request.POST.get('unload')
        short = request.POST.get('short')
        retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if Aak_in_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = Aak_in_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            unload=unload,
            short=short,
            retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                Aak_in_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)

            # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)
        



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('Aak_Inword_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Aak_Inword/aak_india.html', context)


def aakin_list(request):
    invoices = Aak_in_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Aak_Inword/aakin_list.html', {'invoices': invoices})


def aakin_detail(request, invoice_id):
    invoice = get_object_or_404(Aak_in_Invoice, id=invoice_id)
    items = Aak_in_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Aak_Inword/aakin_detail.html', {'invoice': invoice, 'items': items})



#========================VVF TALOJA BILL====================================================
def generate_bills_no():
    now = datetime.now()  # <-- correct function call
    month = f"{now.month:02d}"  # Zero-padded month (e.g., 05)
    year = now.year
    random_number = random.randint(1000, 9999)  # 4-digit random

    # Financial year logic
    if now.month >= 4:  # April se new financial year
        fy_start = str(year)[-2:]
        fy_end = str(year + 1)[-2:]
    else:
        fy_start = str(year - 1)[-2:]
        fy_end = str(year)[-2:]

    financial_year = f"{fy_start}-{fy_end}"

    # Final bill number
    bill_no = f"{random_number}/JN/{month}/{financial_year}"
    return bill_no


def extract_gst_code(gst_number):
    return gst_number[:2] if gst_number and isinstance(gst_number, str) and len(gst_number) >= 2 else ''


def extract_state(address):
    try:
        return address.split(',')[-1].strip().lower()
    except:
        return ''

def vvft_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        # unload = request.POST.get('unload')
        # short = request.POST.get('short')
        # retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bills_no()
        

        if vvft_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = vvft_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            # tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            # unload=unload,
            # short=short,
            # retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total
                

                vvft_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)
       # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('vvft_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Vvf_Taloja/vvf_t.html', context)


def vvftinvoice_list(request):
    vvfinvoice = vvft_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Vvf_Taloja/vvf_t_list.html', {'vvfinvoice': vvfinvoice})


def vvft_detail(request, invoice_id):
    invoice = get_object_or_404(vvft_Invoice, id=invoice_id)
    items = vvft_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Vvf_Taloja/vvf_t_detail.html', {'invoice': invoice, 'items': items})


#==============================TASTY BITE EATABLES LTD===========================================
def tasty_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        unload = request.POST.get('unload')
        short = request.POST.get('short')
        retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if TB_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = TB_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            unload=unload,
            short=short,
            retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                TB_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)

            # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)
        



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('tasty_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Tasty_Bite/Tasty_bite.html', context)


def tasty_list(request):
    tbnvoices = TB_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Tasty_Bite/Tasty_list.html', {'tbnvoices': tbnvoices})


def tasty_detail(request, invoice_id):
    invoice = get_object_or_404(TB_Invoice, id=invoice_id)
    items = TB_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Tasty_Bite/Tasty_detail.html', {'invoice': invoice, 'items': items})



#============================VISWAAT CHEMICALS LTD ======================================
def viswaat_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        # unload = request.POST.get('unload')
        # short = request.POST.get('short')
        # retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if VC_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = VC_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            # tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            # unload=unload,
            # short=short,
            # retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total
                

                VC_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)
       # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('vs_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Viswaat_Chemicals/viswaat.html', context)


def viswaat_list(request):
    vinvoice = VC_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Viswaat_Chemicals/viswaat_list.html', {'vinvoice': vinvoice})


def viswaat_detail(request, invoice_id):
    invoice = get_object_or_404(VC_Invoice, id=invoice_id)
    items = VC_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Viswaat_Chemicals/viswaat_detail.html', {'invoice': invoice, 'items': items})




#========================AAK OUTWORD BILL====================================================

def aakout_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        unload = request.POST.get('unload')
        short = request.POST.get('short')
        retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if AO_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = AO_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            unload=unload,
            short=short,
            retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                AO_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)

            # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)
        



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('Aak_outword_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Aak_Outword/aak_outword.html', context)


def aakout_list(request):
    invoices = AO_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Aak_Outword/aak_outword_list.html', {'invoices': invoices})


def aakout_detail(request, invoice_id):
    invoice = get_object_or_404(AO_Invoice, id=invoice_id)
    items = AO_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Aak_Outword/aak_outword_detail.html', {'invoice': invoice, 'items': items})



#============================KND BUSINESS  ======================================
def knd_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        # unload = request.POST.get('unload')
        # short = request.POST.get('short')
        # retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if KND_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = KND_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            # tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            # unload=unload,
            # short=short,
            # retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total
                

                KND_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)
       # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('KND_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/KND/knd.html', context)


def knd_list(request):
    vinvoice = KND_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/KND/knd_list.html', {'vinvoice': vinvoice})


def knd_detail(request, invoice_id):
    invoice = get_object_or_404(KND_Invoice, id=invoice_id)
    items = KND_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/KND/knd_detail.html', {'invoice': invoice, 'items': items})


#========================SHRI RISHABH INDIA BILL====================================================
def generate_billno():
    now = datetime.now()  # <-- correct function call
    month = f"{now.month:02d}"  # Zero-padded month (e.g., 05)
    year = now.year
    random_number = random.randint(1000, 9999)  # 4-digit random

    # Financial year logic
    if now.month >= 4:  # April se new financial year
        fy_start = str(year)[-2:]
        fy_end = str(year + 1)[-2:]
    else:
        fy_start = str(year - 1)[-2:]
        fy_end = str(year)[-2:]

    financial_year = f"{fy_start}-{fy_end}"

    # Final bill number
    bill_no = f"{random_number}/I/{month}/{financial_year}"
    return bill_no


def extract_gst_code(gst_number):
    return gst_number[:2] if gst_number and isinstance(gst_number, str) and len(gst_number) >= 2 else ''


def extract_state(address):
    try:
        return address.split(',')[-1].strip().lower()
    except:
        return ''
    

def shri_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        unload = request.POST.get('unload')
        short = request.POST.get('short')
        retn = request.POST.get('retn')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_billno()
        

        if SR_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = SR_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            tanker_cap=tanker_cap,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            unload=unload,
            short=short,
            retn=retn,
            lr_no=lr_no,
            sac=sac if sac else 0,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                SR_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        #Step 5: Calculate tax
        cgst_r = 0.09
        sgst_r = 0.09
        igst_r = 0.18

        # GST-based logic
        company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            c_gst = round(g_amount * cgst_r, 2)
            s_gst = round(g_amount * sgst_r, 2)
            i_gst = 0.0
        else:
            # Inter-state
            c_gst = 0.0
            s_gst = 0.0
            i_gst = round(g_amount * igst_r, 2)

        g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        

        basic_amount = subtotal 

        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount * cgst_rate, 2)
            sgst = round(basic_amount * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst + g_total, 2)

            # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)
        



        # Step 6: Save tax and total
        invoice.c_gst = c_gst
        invoice.s_gst = s_gst
        invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('sr_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Shri_Rishabh/shri.html', context)


def shri_list(request):
    tbnvoices = SR_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Shri_Rishabh/shri_list.html', {'tbnvoices': tbnvoices})


def shri_detail(request, invoice_id):
    invoice = get_object_or_404(SR_Invoice, id=invoice_id)
    items = SR_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Shri_Rishabh/shri_detail.html', {'invoice': invoice, 'items': items})