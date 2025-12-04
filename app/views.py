from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.utils.timezone import now
import random
from datetime import datetime,time
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
from num2words import num2words
import os
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth 
from django.db.models import Count 
from django.db.models import Q
from datetime import date

@login_required(login_url="log-in")
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
@login_required(login_url="log-in")
def dashboard(request):
    plan = plandetails.objects.count()
    bill_count = Gemini.objects.count()
    vehicle_c = Add_Vehicle.objects.count()
    dname = NewDriver_Details.objects.count()
    trip = AddTrips.objects.count()
    tripgemini = TripGemini.objects.count()
    tripadani = TripAdani.objects.count()
    triplocal = AakLocal.objects.count()
    trip_exp = Trip.objects.count()
    salary = Driver_salary.objects.count()
    company = companydetails.objects.count()
    driver = NewDriver_Details.objects.count()
    driverl = DriverL.objects.values('drivername').distinct().count()

    # Monthly trips for chart (all months)
    data = (
        AddTrips.objects.filter(dispatch_time__isnull=False)
        .annotate(month=ExtractMonth("dispatch_time"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    trips_dict = {i:0 for i in range(1,13)}
    for row in data:
        trips_dict[row["month"]] = row["total"]

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    trips_monthly = [trips_dict[i] for i in range(1,13)]

    context = {
        'plan': plan,
        'bill_count': bill_count,
        'vehicle_c': vehicle_c,
        'dname': dname,
        'trip': trip,
        'trip_exp': trip_exp,
        'salary': salary,
        'tripgemini': tripgemini,
        'tripadani': tripadani,
        'triplocal': triplocal,
        'company': company,
        'driver': driver,
        'months': months,
        'trips_monthly': trips_monthly,
        'driverl':driverl
    }

    return render(request,'index.html',context)


@login_required(login_url="log-in")
def plan(request):
    if request.method =="POST":
      tankerno  = request.POST['tankerno']
      drivername = request.POST['drivername']
      ddriver = request.POST['ddriver']
      From_address = request.POST['From_address']
      To_address = request.POST['To_address']
      tanker_capacity = request.POST['tanker_capacity']
      dispatch_Date = request.POST['dispatch_Date']
      status = request.POST['status']
      if  plandetails.objects.filter(tankerno=tankerno,dispatch_Date=dispatch_Date).exists():
          messages.error(request, 'Plan already exists !!')
          return redirect('plan')
      else:
          plan=plandetails(tankerno=tankerno,drivername=drivername,ddriver=ddriver if ddriver else "",From_address=From_address,To_address=To_address,tanker_capacity=tanker_capacity,dispatch_Date=dispatch_Date,status=status)
          plan.save()
          messages.success(request, 'Plan details added successfully !!')
          return redirect('showplan')
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname}
    return render(request,'add/add-plans.html', context)


def showplan(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search = request.GET.get('search')

    showplans = plandetails.objects.all().order_by('-dispatch_Date')

    # Filter by date range if provided
    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            showplans = showplans.filter(dispatch_Date__range=(from_date_obj, to_date_obj))
        except ValueError:
            pass  # Invalid date format, ignore filtering

    # Filter by tanker number or driver name
    if search:
        showplans = showplans.filter(
            Q(tankerno__icontains=search) |
            Q(drivername__icontains=search)  # adjust field name
        )

    context = {'showplans': showplans}
    return render(request, 'show/show-plan.html', context)


def updateplan(request,id):
    planupdate=plandetails.objects.get(pk=id)
    vehicle=Add_Vehicle.objects.all()
    dname=NewDriver_Details.objects.all()
    company=companydetails.objects.all()
    context={'planupdate':planupdate,'vehicle':vehicle,'company':company,'dname':dname}
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



@login_required(login_url="log-in")
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
        ddriver = request.POST.get('ddriver')
        tank_capacity = request.POST.get('tank_capacity')
        arrival_time = parse_datetime(request.POST.get('arrival_time')) if request.POST.get('arrival_time') else None
        dispatch_time = parse_datetime(request.POST.get('dispatch_time')) if request.POST.get('dispatch_time') else None
        reach_time = parse_datetime(request.POST.get('reach_time')) if request.POST.get('reach_time') else None
        unload_time = parse_datetime(request.POST.get('unload_time')) if request.POST.get('unload_time') else None
        lr_num = request.POST.get('lr_num')
        dolr_num = request.POST.get('dolr_num')
        lr_date = request.POST.get('lr_date')
        dolr_date = request.POST.get('dolr_date')
        freight_bill = request.POST.get('freight_bill')
        dofreight_bill = request.POST.get('dofreight_bill')
        freight_date = request.POST.get('freight_date')
        dofreight_date = request.POST.get('dofreight_date')
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
            ddriver=ddriver if ddriver else "",
            tank_capacity=tank_capacity if tank_capacity else None,
            arrival_time=arrival_time,
            dispatch_time=dispatch_time,
            reach_time=reach_time,
            unload_time=unload_time,
            lr_num=lr_num if lr_num else None,
            dolr_num=dolr_num if dolr_num else None,
            lr_date=lr_date if lr_date else None,
            dolr_date=dolr_date if dolr_date else None,
            freight_bill=freight_bill if freight_bill else None,
            dofreight_bill=dofreight_bill if dofreight_bill else None,
            freight_date=freight_date if freight_date else None,
            dofreight_date=dofreight_date if dofreight_date else None,
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
    
    # STEP: Get saved tanker IDs (that are already in trips)
    saved_plan_ids = AddTrips.objects.values_list('plan_id', flat=True)
    # Return to the template with the plans
    context = {'plans': plans, 'saved_plan_ids': list(saved_plan_ids),}
    return render(request, 'add/add_trip_all.html', context)



def get_plan_details(request):
    plan_id = request.GET.get('plan_id')
    try:
        plan = plandetails.objects.get(id=plan_id)
        data = {
            'drivername': plan.drivername,
            'ddriver': plan.ddriver,
            'From_address': plan.From_address,
            'To_address': plan.To_address,
            'tanker_capacity': plan.tanker_capacity,
            'dispatch_Date': plan.dispatch_Date,
        }
        return JsonResponse(data)
    except plandetails.DoesNotExist:
        return JsonResponse({'error': 'Plan not found'}, status=404)
   
def showtrip(request):
    from datetime import datetime, time
    from django.db.models import Q

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search = request.GET.get('search')

    show = AddTrips.objects.all()

    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

            from_datetime = datetime.combine(from_date_obj.date(), time.min)
            to_datetime = datetime.combine(to_date_obj.date(), time.max)

            show = show.filter(dispatch_time__range=(from_datetime, to_datetime))
        except ValueError:
            pass

    if search:
        show = show.filter(
            Q(plan__tankerno__icontains=search) |
            Q(drivername__icontains=search)
        )

    # 👇 Order by dispatch_time descending
    show = show.order_by('-dispatch_time')

    context = {'show': show}
    return render(request, 'show/show-trip.html', context)


def updatetrip(request,id):
    uptrip=AddTrips.objects.get(pk=id)
    plans = plandetails.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'uptrip':uptrip,'plans':plans,'company':company,'dname':dname}
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
    dolr_num = request.POST.get('dolr_num')
    lr_date = request.POST.get('lr_date')
    dolr_date = request.POST.get('dolr_date')
    freight_bill = request.POST.get('freight_bill')
    dofreight_bill = request.POST.get('dofreight_bill')
    freight_date = request.POST.get('freight_date')
    dofreight_date = request.POST.get('dofreight_date')
    remark = request.POST.get('remark')
     

    # Fetch the existing plan details to update
    update_t = AddTrips.objects.get(pk=id)

 
    update_t.tankerno = tankerno
    update_t.drivername = drivername
    update_t.From_address = From_address
    update_t.To_address = To_address
    update_t.tank_capacity = tank_capacity
    update_t.arrival_time = arrival_time if arrival_time else None
    update_t.dispatch_time = dispatch_time if dispatch_time else None
    update_t.reach_time = reach_time if reach_time else None
    update_t.unload_time = unload_time if unload_time else None
    update_t.loaded_qty = loaded_qty if loaded_qty else 0
    update_t.percent = percent if percent else 0
    update_t.unload_qty = unload_qty if unload_qty else 0
    update_t.short_qty = short_qty if short_qty else 0
    update_t.short_allow = short_allow if short_allow else 0
    update_t.return_qty = return_qty if return_qty else 0
    update_t.lr_num = lr_num if lr_num else ""
    update_t.dolr_num = dolr_num if dolr_num else ""
    update_t.lr_date = lr_date if lr_date else None
    update_t.dolr_date = dolr_date if dolr_date else None
    update_t.freight_bill = freight_bill if freight_bill else ""
    update_t.dofreight_bill = dofreight_bill if dofreight_bill else ""
    update_t.freight_date = freight_date if freight_date else None
    update_t.dofreight_date = dofreight_date if dofreight_date else None
    update_t.remark = remark if remark else ""

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





@login_required(login_url="log-in")
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
          messages.success(request, 'Adani Trip added successfully !!') 
          
          
          
    
    # Pass the values to the template
    # Get the list of plans for the dropdown
    plans = plandetails.objects.all()
    
    saved_plan_ids = AddTrips.objects.values_list('plan_id', flat=True)
    # Return to the template with the plans
    context = {'plans': plans,'saved_plan_ids':saved_plan_ids}
    return render(request, 'add/add_trip_adani.html',context)

def ShowAdani(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    adani=TripAdani.objects.all()

    if from_date and to_date:
        try:
            # Sirf date mil raha hai: "2025-09-11"
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

            # Din ki starting aur ending time set karo:
            from_datetime = datetime.combine(from_date_obj.date(), time.min)  # 00:00:00
            to_datetime = datetime.combine(to_date_obj.date(), time.max)      # 23:59:59.999999

            # Filter karo dispatch_time ke range par
            adani = adani.filter(dispatch_time__range=(from_datetime, to_datetime))
        except ValueError:
            pass  # Agar galat format ho to skip karo
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
    up_adani.arrival_time=arrival_time  if arrival_time else None
    up_adani.dispatch_time=dispatch_time  if dispatch_time else None
    up_adani.reach_time=reach_time if reach_time else None
    up_adani.unload_time=unload_time if unload_time else None
    up_adani.loaded_qty=loaded_qty if loaded_qty else 0
    up_adani.unload_qty=unload_qty if unload_qty else 0
    up_adani.short_qty=short_qty if short_qty else 0
    up_adani.short_allow=short_allow if short_allow else 0
    up_adani.return_qty=return_qty if return_qty else 0
    up_adani.lr_num=lr_num  if lr_num else 0
    up_adani.lr_date=lr_date if lr_date else None
    up_adani.freight_bill=freight_bill  if freight_bill else 0
    up_adani.freight_date=freight_date if freight_date else None

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
          messages.success(request, 'Gemini Trip added successfully !!') 
          return redirect('show-gemini-details')
    
    # Get the list of plans for the dropdown
    plans = plandetails.objects.all()

    saved_plan_ids = AddTrips.objects.values_list('plan_id', flat=True)

    # Return to the template with the plans
    context = {'plans': plans,'saved_plan_ids':saved_plan_ids}
    return render(request, 'add/add_trip_gemini.html',context)

def Showgemini(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    gemeni=TripGemini.objects.all()

    if from_date and to_date:
        try:
            # Sirf date mil raha hai: "2025-09-11"
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

            # Din ki starting aur ending time set karo:
            from_datetime = datetime.combine(from_date_obj.date(), time.min)  # 00:00:00
            to_datetime = datetime.combine(to_date_obj.date(), time.max)      # 23:59:59.999999

            # Filter karo dispatch_time ke range par
            gemeni =  gemeni.filter(dispatch_time__range=(from_datetime, to_datetime))
        except ValueError:
            pass  # Agar galat format ho to skip karo
    
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
    geminiup.arrival_time=arrival_time if arrival_time else None
    geminiup.dispatch_time=dispatch_time if dispatch_time else None
    geminiup.reach_time=reach_time if reach_time else None
    geminiup.unload_time=unload_time if unload_time else None
    geminiup.loaded_qty=loaded_qty if loaded_qty else 0
    
    geminiup.unload_qty=unload_qty if unload_qty else 0
    geminiup.short_qty=short_qty if short_qty else 0
    geminiup.short_allow=short_allow if short_allow else 0
    geminiup.return_qty=return_qty if return_qty else 0
    geminiup.lr_num=lr_num if lr_num else 0
    geminiup.lr_date=lr_date if lr_date else None
    geminiup.freight_bill=freight_bill if freight_bill else 0
    geminiup.freight_date=freight_date if freight_date else None

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
            messages.success(request, 'Trip Aak India Local added successfully !!')
     # Get the list of plans for the dropdown
    plans = plandetails.objects.all()

    saved_plan_ids = AddTrips.objects.values_list('plan_id', flat=True)

    # Return to the template with the plans
    context = {'plans': plans,'saved_plan_ids':saved_plan_ids}
    return render(request,'AAK-india-local.html',context)

def ShowAakLocal(request):
    
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    Aak=AakLocal.objects.all()

    if from_date and to_date:
        try:
            # Sirf date mil raha hai: "2025-09-11"
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

            # Din ki starting aur ending time set karo:
            from_datetime = datetime.combine(from_date_obj.date(), time.min)  # 00:00:00
            to_datetime = datetime.combine(to_date_obj.date(), time.max)      # 23:59:59.999999

            # Filter karo dispatch_time ke range par
            Aak =Aak.filter(dispatch_time__range=(from_datetime, to_datetime))
        except ValueError:
            pass  # Agar galat format ho to skip karo
    
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
    percent= request.POST.get('percent')
    
    
    Aakupdate=AakLocal.objects.get(pk=id)
    
    Aakupdate.tankerno=tankerno
    Aakupdate.From_address=From_address
    Aakupdate.To_address=To_address
    Aakupdate.drivername=drivername
    Aakupdate.tank_capacity=tank_capacity
    Aakupdate.arrival_time=arrival_time if arrival_time else None
    Aakupdate.dispatch_time=dispatch_time if dispatch_time else None
    Aakupdate.reach_time=reach_time if reach_time else None
    Aakupdate.lr_num=lr_num if lr_num else 0
    Aakupdate.lr_date=lr_date if lr_date else None
    Aakupdate.freight_bill=freight_bill if freight_bill else 0
    Aakupdate.freight_date=freight_date if freight_date else None
    Aakupdate.loaded_qty=loaded_qty if loaded_qty else 0
    Aakupdate.unload_qty=unload_qty if unload_qty else 0
    Aakupdate.short_qty=short_qty if short_qty else 0
    Aakupdate.short_allow=short_allow if short_allow else 0
    Aakupdate.return_qty=return_qty if return_qty else 0
    Aakupdate.remark=remark if remark else None
    Aakupdate.time_Loading=time_Loading if time_Loading else None
    Aakupdate.time_Loading_mama=time_Loading_mama if unloading_ganesh else None
    Aakupdate.unloading_ganesh=unloading_ganesh if unloading_ganesh else 0
    Aakupdate.unloading_mama=unloading_mama if unloading_mama else 0
    Aakupdate.returned=returned if returned else None
    Aakupdate.trip_ganesh=trip_ganesh if trip_ganesh else None
    Aakupdate.trip_mama=trip_mama if trip_mama else None
    Aakupdate.percent=percent if percent else 0

    Aakupdate.save()
    messages.success(request, 'Trip Aak India Local updated successfully!')
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
     if img:
        updatedriver.img=img
     updatedriver.fname=fname
     updatedriver.save()
     messages.success(request, "Driver Update successfully.")
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

    # Do NOT overwrite the filtered trips
    expenses = Expense.objects.all()
    total_expense_sum = trips.aggregate(Sum('total_expense'))['total_expense__sum']
    combined = zip(trips, expenses)
    
    context = {
        'combined': combined,
        'grand_total': total_expense_sum or 0,
    }

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
            upvehicle.insurance_date = insurance_date if insurance_date else None
            if insurance_img:
               upvehicle.insurance_img = insurance_img if insurance_img else None
            upvehicle.state_permit = state_permit if state_permit else None
            if state_img:
               upvehicle.state_img = state_img if  state_img else None
            upvehicle.national_permit = national_permit if national_permit else None
            if national_img:
               upvehicle.national_img= national_img if  national_img else None

            upvehicle.fitness_date = fitness_date if fitness_date else None
            if fitness_img:
                upvehicle.fitness_img= fitness_img if  fitness_img else None

            upvehicle.tax_date = tax_date if tax_date else None
            if tax_date:
                upvehicle.tax_img= tax_img if  tax_img else None

            upvehicle.puc_date = puc_date if puc_date else None
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
          cname=companydetails(name=name,area_name=area_name,state=state if state else None,city=city if city else None,pincode=pincode if pincode else None,gst=gst if gst else None,pan=pan if pan else None,contact_no=contact_no if contact_no else None,short_name=short_name if short_name else None)
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
            pending_trip = request.POST.get('pending_trip')

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
                    trip_date=trip_date if trip_date else None,
                    from_id=from_id,
                    To_id=To_id,
                    drivername=drivername,
                    f_trip=f_trip if f_trip else None,
                    pending_trip=pending_trip if pending_trip else 'Actual trip'
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


def update_trip(request, trip_id):
    # trip = get_object_or_404(Trip, trip_id=trip_id)
    trip = Trip.objects.get(id=trip_id)

    if request.method == 'POST':
        try:
            trip.tanker = request.POST.get('tanker')
            trip.trip_date = request.POST.get('trip_date')
            trip.from_id = request.POST.get('from_id')
            trip.To_id = request.POST.get('To_id')
            trip.drivername = request.POST.get('drivername')
            trip.f_trip = request.POST.get('f_trip') or None
            trip.pending_trip = request.POST.get('pending_trip') 
            trip.save()

            messages.success(request, 'Trip updated successfully.')
            return redirect('trip')

        except Exception as e:
            messages.error(request, f"Update failed: {str(e)}")
            return redirect('trip')
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname,'trip': trip}
    return render(request, 'update_starttrip.html',context)




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
        drname = request.POST.get('drname')
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
                To_via = To_via if To_via else None,
                drname  = drname if drname else "",
                end_date= end_date if end_date else None,

            )
            messages.success(request, 'Trip Expense Add successfully !!')
            trip.calculate_total_expense()  # Recalculate total expense after adding a new expense
            return redirect('add_expense', trip_id=trip.trip_id)
        
    food_allowance_sum = trip.expenses.aggregate(Sum('food_allowance'))['food_allowance__sum'] or 0
    bhatta_sum = trip.expenses.aggregate(Sum('bhatta'))['bhatta__sum'] or 0
    toll_amount_sum = trip.expenses.aggregate(Sum('toll_amount'))['toll_amount__sum'] or 0
    total_diesel_sum = trip.expenses.aggregate(Sum('total_diesel'))['total_diesel__sum'] or 0
    urea_total_sum = trip.expenses.aggregate(Sum('urea_total'))['urea_total__sum'] or 0
    r_amount_sum = trip.expenses.aggregate(Sum('r_amount'))['r_amount__sum'] or 0

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search = request.GET.get('search')

    showplans = trip.expenses.all()

     # Apply date filter
    if from_date and to_date:
       try:
         from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
         to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
         showplans = showplans.filter(dispatch_Date__range=(from_date_obj, to_date_obj))
       except ValueError:
            pass

    # Apply search filter
    if search:
        showplans = showplans.filter(
         Q(tankerno__icontains=search) |
         Q(drivername__icontains=search)
    )
    # Get all expenses related to the trip
    expenses = trip.expenses.all()
    categories = Category.objects.all()
    dname = NewDriver_Details.objects.all()
    petrol = AddPetrolPump.objects.all()
    company = companydetails.objects.all()
    # Return the response

    context = {'categories': categories, 'dname': dname, 'petrol': petrol,'trip': trip,
        'expenses': expenses,'company':company,'food_allowance_sum':food_allowance_sum,'bhatta_sum':bhatta_sum,'toll_amount_sum':toll_amount_sum,'total_diesel_sum':total_diesel_sum,'urea_total_sum':urea_total_sum,'r_amount_sum':r_amount_sum,'showplans': showplans}
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
     upexpense.from_via = from_via or None
     upexpense.To_via = To_via or None
     upexpense.end_date=end_date or None

     upexpense.save()
     upexpense.trip.calculate_total_expense() 
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


#===================Start Modify file================================
def end_trip(request, trip_id):
    if request.method == 'POST':
        end_time = request.POST.get('end_time')
    trips = Trip.objects.filter(trip_id=trip_id)

    if trips.count() == 1:
        trip = trips.first() 
    elif trips.count() > 1:
        trip = trips.first()  
    else:
        return render(request, '404.html')  
    # Mark the trip as ended
    trip.end_time = timezone.now() 
    trip.is_active = False  
    trip.calculate_total_expense()  
    trip.save()

   
    return render(request, 'exp/end_trip.html', {'trip': trip})
#===================End Modify file================================

def AllTrip(request):
    t = Trip.objects.all().order_by('-id')

    trip_data = []

    for trip in t:
        # Latest expense ke end_date fetch karo
        latest_expense = trip.expenses.order_by('-end_date').first()  # related_name "expenses" use kiya
        trip_data.append({
            'trip': trip,
            'end_date': latest_expense.end_date if latest_expense else None
            
        })

    context = {
        't': trip_data,
    }

    return render(request, 'show/all_trip.html', context)




def del_allTrip(request,id):
    d=Trip.objects.get(pk=id)
    d.delete()
    return redirect('trip')


def SignUp(request):
    
    return render(request,'form/signup.html')



#=========================LOGIN SYSTEM=========================================

def Login(request):
    if request.method == 'POST':  # Make sure the method is POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in

             # Username ke hisaab se redirect
            if user.username == 'Mhaider':
                return redirect('inventory-dashboard')  # isko URL me define karo
            elif user.username == 'Pratiksha':
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
      driverloan=request.POST['driverloan']
      total = request.POST['total']
      repayment = request.POST['repayment']
      short_allow_rate  = request.POST['short_allow_rate']
      name = request.POST.get('name')
      rdate = request.POST.get('rdate')
      amount = request.POST.get('amount')
      driverid = request.POST.get('driverid')
      tanker = request.POST.get('tanker')

      if  DriverL.objects.filter(date=date,drivername=drivername).exists():
          messages.error(request, 'Driver Loan exists !!')
          return redirect('drivers-loan')
      else:
          d_loan=DriverL.objects.create(
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
          driverloan=driverloan if driverloan else None,
          total = total if total else None,
          short_allow_rate = short_allow_rate  if short_allow_rate else None,
          repayment = repayment if repayment else None,
          name = name if name else None,
          rdate = rdate if rdate else None,
          amount = amount if amount else None,
          driverid = driverid if driverid else None,
          tanker = tanker if tanker else None,
        )
      d_loan.save()
      messages.success(request, 'Driver Loan Add successfully!')

    shortage=Expense.objects.filter().last()
    vehicle=Add_Vehicle.objects.all()
    dname=NewDriver_Details.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    trip = Trip.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname,'shortage':shortage,'company':company,'trip':trip}
    return render(request,'add/add_driver_loan.html',context)



def ShowLoan(request):
    Loan=DriverL.objects.all()
    return render(request,'show/show_driver_loan.html',{'Loan':Loan})

def deleteloan(request,id):
    d=DriverL.objects.get(pk=id)
    d.delete()
    return redirect('show-loan')

def updriverloan(request,id):
    updatedl=DriverL.objects.get(pk=id)
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
      updatedl=DriverL.objects.get(pk=id)

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


# def get_driver_shortage(request):
#     driver_name = request.GET.get('driver_name')
#     shortage_amount = 0

#     if driver_name:
#         # Filter latest shortage for this driver
#         latest_loan = DriverL.objects.filter(drivername=driver_name).order_by('-id').first()
#         if latest_loan:
#             shortage_amount = latest_loan.total or 0

#     return JsonResponse({'shortage': shortage_amount})

def get_driver_shortage(request):
    driver_name = request.GET.get('driver_name')
    shortage_amount = 0

    if driver_name:
        # Total loan amount for the driver
        total_loan = DriverL.objects.filter(drivername__iexact=driver_name).aggregate(
            total=Sum('loan_amount')
        )['total'] or 0

        # Total repayment amount for the driver
        total_repayment = DriverL.objects.filter(drivername__iexact=driver_name).aggregate(
            total=Sum('repayment')
        )['total'] or 0

        # Net shortage = loan - repayment
        shortage_amount = total_loan - total_repayment

    return JsonResponse({'shortage': float(shortage_amount)})

#========================END DRIVER LOAN===================================


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


def Multi_bill(request):
    # adani=Invoice.objects.count()
    # gemini=GInvoice.objects.count()
    # akkinword=Aak_in_Invoice.objects.count()
    # context={'adani':adani,'gemini':gemini,'akkinword':akkinword}
    return render(request,'multi_bill.html')

def detention_bill(request):
    # adani=Invoice.objects.count()
    # gemini=GInvoice.objects.count()
    # akkinword=Aak_in_Invoice.objects.count()
    # context={'adani':adani,'gemini':gemini,'akkinword':akkinword}
    return render(request,'detention_bill.html')





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


#====================ADANI BILL====================================

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
#=============================ADANI KAKINADA BILL=====================================
def adk_bill(request):
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
           return redirect('adaniK-bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = AKInvioce.objects.create(
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

                AKItem.objects.create(
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

        return redirect('adaniK_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Adani_kakinada/kakinada.html', context)


def adk_list(request):
    invoices = AKInvioce.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Adani_kakinada/kakinada_list.html', {'invoices': invoices})


def adk_detail(request, invoice_id):
    invoice = get_object_or_404(AKInvioce, id=invoice_id)
    items = AKItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Adani_kakinada/kakinada_details.html', {'invoice': invoice, 'items': items})

#=============================ADANI MUNDRA BILL=====================================
def amundra_bill(request):
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
        # Fo_date = request.POST.get('Fo_date')
        # To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        # charges = request.POST.get('charges')
        # hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if ADMInvioce.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('adm_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = ADMInvioce.objects.create(
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
            # charges=charges if total_d else None,
            # hsac=hsac if hsac else 0,
            # Fo_date=Fo_date if Fo_date else None,
            # To_date=To_date if Fo_date else None,
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

                ADMItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d)  # or Decimal(total_d)

        basic_amount = subtotal - float(total_d)

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
            sgst = round(basic_amount   * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount + cgst + sgst + igst, 2)
        grand_total = round(basic_amount + cgst + sgst + igst , 2)

            # Check decimal part
        decimal_part = grand_total - int(grand_total)

        # Add 1 rupee if decimal part > 0.50
        if decimal_part > 0.50:
          grand_total = int(grand_total) + 1
        else:
            grand_total = int(grand_total)

        #  final output looks like 1000.00 format
        formatted_total = "{:.2f}".format(grand_total)
        



        #Step 6: Save tax and total
        invoice.total_amount = basic_amount 
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('adm_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Adani/mundra.html', context)


def amundra_list(request):
    invoices = ADMInvioce.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Adani/mundra_list.html', {'invoices': invoices})


def amundra_detail(request, invoice_id):
    invoice = get_object_or_404(ADMInvioce, id=invoice_id)
    items = ADMItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Adani/mundra_details.html', {'invoice': invoice, 'items': items})



#=================================GEMINI BILL====================================================
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
        # tanker_cap = request.POST.get('tanker_cap')
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
        tmsid=request.POST.get('tmsid')
        unloadcharge = request.POST.get('unloadcharge')
        unloadrate = request.POST.get('unloadrate')
        

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if ASL_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('ainvoice_list')
        else:
          
        # Step 3: Create empty invoice
         invoice = ASL_Invoice.objects.create(
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
            tmsid=tmsid,
            sac=sac if sac else 0,
            unloadcharge=unloadcharge if total_d else None,
            unloadrate=unloadrate if total_d else None,
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

                ASL_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d or 0) + float(unloadrate or 0)  # or Decimal(total_d)

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
        invoice.g_amount = g_amount
        invoice.total_d = total_d 
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('ainvoice_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Ashland/ashland.html', context)


def Ainvoice_list(request):
    ainvoice = ASL_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Ashland/ashland_list.html', {'ainvoice': ainvoice})


def Ainvoice_detail(request, invoice_id):
    invoice = get_object_or_404(ASL_Invoice, id=invoice_id)
    items = ASL_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Ashland/ashland_details.html', {'invoice': invoice, 'items': items})


#========================CARGILL BILL====================================================
def generate_billc_no():
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
    bill_no = f"{random_number}/CD/{month}/{financial_year}"
    return bill_no


def extract_gst_code(gst_number):
    return gst_number[:2] if gst_number and isinstance(gst_number, str) and len(gst_number) >= 2 else ''


def extract_state(address):
    try:
        return address.split(',')[-1].strip().lower()
    except:
        return ''


def cargill_bill(request):
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
        # Fo_date = request.POST.get('Fo_date')
        # To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')

        # Step 2: Generate invoice number
        invoice_number = generate_billc_no()
        

        if CRInvoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('cinvoice_list')
        else:
          
        # Step 3: Create empty invoice
         invoice = CRInvoice.objects.create(
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
            # Fo_date=Fo_date if Fo_date else None,
            # To_date=To_date if Fo_date else None,
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

                CRItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        # g_amount = float(total_d)  # or Decimal(total_d)

        # #Step 5: Calculate tax
        # cgst_r = 0.09
        # sgst_r = 0.09
        # igst_r = 0.18

        # # GST-based logic
        # company_gst = "27XXXXX0000Z5A"  # Set your own company's GST number here (hardcoded or from DB)
        # from_gst_code = extract_gst_code(company_gst)  # Your GST
        # to_gst_code = extract_gst_code(gst)  # Customer GST

        # if from_gst_code == '27' and to_gst_code == '27':
        #     # Intra-state (Maharashtra)
        #     c_gst = round(g_amount * cgst_r, 2)
        #     s_gst = round(g_amount * sgst_r, 2)
        #     i_gst = 0.0
        # else:
        #     # Inter-state
        #     c_gst = 0.0
        #     s_gst = 0.0
        #     i_gst = round(g_amount * igst_r, 2)

        # g_total = round(g_amount + c_gst + s_gst + i_gst, 2)
     

        
        g_amount=float(total_d)
        basic_amount = subtotal + g_amount
       
        cgst_rate = 0.06
        sgst_rate = 0.06
        igst_rate = 0.12

        # GST-based logic
        company_gst = "27XXXXX0000Z5A" 
        from_gst_code = extract_gst_code(company_gst)  # Your GST
        to_gst_code = extract_gst_code(gst)  # Customer GST

        if from_gst_code == '27' and to_gst_code == '27':
            # Intra-state (Maharashtra)
            cgst = round(basic_amount  * cgst_rate, 2)
            sgst = round(basic_amount  * sgst_rate, 2)
            igst = 0.0
        else:
            # Inter-state
            cgst = 0.0
            sgst = 0.0
            igst = round(basic_amount * igst_rate, 2)

        fright_total = round(basic_amount  + cgst + sgst + igst , 2)
        grand_total = round(basic_amount  + cgst + sgst + igst, 2)

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
        # invoice.c_gst = c_gst
        # invoice.s_gst = s_gst
        # invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d
        # invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('cinvoice_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Cargill/cargill.html', context)


def cargill_list(request):
    invoices = CRInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Cargill/cargill_list.html', {'invoices': invoices})


def cargill_detail(request, invoice_id):
    invoice = get_object_or_404(CRInvoice, id=invoice_id)
    items = CRItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Cargill/cargill_details.html', {'invoice': invoice, 'items': items})







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

#=========================AAK INDIA RAIPUR BILL ====================================================
def generate_billR_no():
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
    bill_no = f"{random_number}/R/{month}/{financial_year}"
    return bill_no


def raipur_bill(request):
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
        invoice_number = generate_billR_no()
        

        if AAKR_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('raipur_list')
        else:
          
        # Step 3: Create empty invoice
         invoice = AAKR_Invoice.objects.create(
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

                AAKR_Item.objects.create(
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

        return redirect('raipur_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/AAK_INDIA/raipur.html', context)


def raipur_list(request):
    tbnvoices = AAKR_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/AAK_INDIA/raipur_list.html', {'tbnvoices': tbnvoices})


def raipur_detail(request, invoice_id):
    invoice = get_object_or_404(AAKR_Invoice, id=invoice_id)
    items = AAKR_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/AAK_INDIA/raipur_details.html', {'invoice': invoice, 'items': items})


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
#========================VINAY ENTERPRISES BILL====================================================
def vinay_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tan = request.POST.get('tan')
        fassi = request.POST.get('fassi')
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
        

        if VE_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = VE_Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tan=tan,
            fassi=fassi,
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

                VE_Item.objects.create(
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

        return redirect('vin_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Vinay/vinay.html', context)


def vinay_list(request):
    tbnvoices = VE_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Vinay/vinay_list.html', {'tbnvoices': tbnvoices})


def vinay_detail(request, invoice_id):
    invoice = get_object_or_404(VE_Invoice, id=invoice_id)
    items = VE_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Vinay/vinay_detail.html', {'invoice': invoice, 'items': items})






#========================SUNDER AGRO INDUSTRIES BILL====================================================
def sun_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if SAInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('create_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = SAInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                SAItem.objects.create(
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

        return redirect('sagro_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Sunder/sunder.html', context)


def sunder_list(request):
    ginvoice = SAInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Sunder/sunder_list.html', {'ginvoice': ginvoice})


def sunder_detail(request, invoice_id):
    invoice = get_object_or_404(SAInvoice, id=invoice_id)
    items = SAItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Sunder/sunder_detail.html', {'invoice': invoice, 'items': items})


#========================RION REFOIL BILL====================================================
def rion_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if RRInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('rion_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = RRInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                RRItem.objects.create(
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

        return redirect('sagro_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Rion_Refoil/Rion.html', context)



def rion_list(request):
    rinvoice = RRInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Rion_Refoil/Rion_list.html', {'rinvoice': rinvoice})

def rion_detail(request, invoice_id):
    invoice = get_object_or_404(RRInvoice, id=invoice_id)
    items = RRItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Rion_Refoil/rion_details.html', {'invoice': invoice, 'items': items})

#========================NHT & COMPANY BILL====================================================
def NHT_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if NHTInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('NHT_list')
        else:
          
        # Step 3: Create empty invoice
         invoice = NHTInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                NHTItem.objects.create(
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

        return redirect('NHT_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/NHT/NHT.html', context)



def NHT_list(request):
    nhtinvoice = NHTInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/NHT/NHT_list.html', {'nhtinvoice': nhtinvoice})

def NHT_detail(request, invoice_id):
    invoice = get_object_or_404(NHTInvoice, id=invoice_id)
    items = NHTItem.objects.filter(invoice=invoice)
    return render(request, 'bills/NHT/NHT_details.html', {'invoice': invoice, 'items': items})

#========================MURLIWALA  BILL====================================================
def murli_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if MUInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('murli_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = MUInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                MUItem.objects.create(
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

        return redirect('murli_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/MURLIWALA/murli.html', context)


def murli_list(request):
    invoices = MUInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/MURLIWALA/murli_list.html',{'invoices': invoices})


def murli_detail(request, invoice_id):
    invoice = get_object_or_404(MUInvoice, id=invoice_id)
    items = MUItem.objects.filter(invoice=invoice)
    return render(request, 'bills/MURLIWALA/murli_details.html', {'invoice': invoice, 'items': items})

#========================MALANI TRADING CO BILL====================================================
def malani_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if MAInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('malani_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = MAInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                MAItem.objects.create(
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

        return redirect('manali_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Malani/malani.html', context)


def malani_list(request):
    ginvoice = MAInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Malani/malani_list.html', {'ginvoice': ginvoice})


def malani_detail(request, invoice_id):
    invoice = get_object_or_404(MAInvoice, id=invoice_id)
    items = MAItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Malani/malani_details.html', {'invoice': invoice, 'items': items})


#=========================PATEL TRADERS BILL ====================================================
def patel_bill(request):
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
        

        if PT_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('patel_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = PT_Invoice.objects.create(
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

                PT_Item.objects.create(
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

        return redirect('patel_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Patel_traders/patel.html', context)


def patel_list(request):
    tbnvoices = PT_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Patel_traders/patel_list.html', {'tbnvoices': tbnvoices})


def patel_detail(request, invoice_id):
    invoice = get_object_or_404(PT_Invoice, id=invoice_id)
    items = PT_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Patel_traders/patel_details.html', {'invoice': invoice, 'items': items})

#=========================KOP Agro BILL ====================================================
def KOP_bill(request):
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
        

        if KOP_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('KOP_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = KOP_Invoice.objects.create(
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

                KOP_Item.objects.create(
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

        return redirect('KOP_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/KOP/kop.html', context)


def KOP_list(request):
    tbnvoices = KOP_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/KOP/KOP_list.html', {'tbnvoices': tbnvoices})


def KOP_detail(request, invoice_id):
    invoice = get_object_or_404(KOP_Invoice, id=invoice_id)
    items = KOP_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/KOP/KOP_details.html', {'invoice': invoice, 'items': items})


#==============================DHANLAXMI EDIBLES PVT LIMITED====================================
def dhan_bill(request):
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
        unloadcharge = request.POST.get('unloadcharge')
        unloadrate = request.POST.get('unloadrate')
        

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if DE_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('dhanlaxmi_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = DE_Invoice.objects.create(
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
            unloadcharge=unloadcharge if total_d else None,
            unloadrate=unloadrate if total_d else None,
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

                DE_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d or 0) + float(unloadrate or 0)  # or Decimal(total_d)

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
        invoice.g_amount = g_amount
        invoice.total_d = total_d 
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('dhanlaxmi_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Dhanlaxmi/dhanlaxmi.html', context)


def dhan_list(request):
    Dnvoices = DE_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Dhanlaxmi/dhanlaxmi_list.html', {'Dnvoices': Dnvoices})


def dhan_detail(request, invoice_id):
    invoice = get_object_or_404(DE_Invoice, id=invoice_id)
    items = DE_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Dhanlaxmi/dhanlaxmi_details.html', {'invoice': invoice, 'items': items})

#==============================BARRY CALLEBAUT PVT LIMITED====================================
def barry_bill(request):
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
        unloadcharge = request.POST.get('unloadcharge')
        unloadrate = request.POST.get('unloadrate')
        

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if BC_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('barry_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = BC_Invoice.objects.create(
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
            unloadcharge=unloadcharge if total_d else None,
            unloadrate=unloadrate if total_d else None,
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

                BC_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d or 0) + float(unloadrate or 0)  # or Decimal(total_d)

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
        invoice.g_amount = g_amount
        invoice.total_d = total_d 
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('barry_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Barry/barry.html', context)


def barry_list(request):
    bnvoices = BC_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Barry/barry_list.html', {'bnvoices': bnvoices})


def barry_detail(request, invoice_id):
    invoice = get_object_or_404(BC_Invoice, id=invoice_id)
    items = BC_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Barry/barry_details.html', {'invoice': invoice, 'items': items})
#=========================CARGILL DAVANGERE BILL ====================================================
def generate_bill():
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
    bill_no = f"{random_number}/CD/{month}/{financial_year}"
    return bill_no

def davan_bill(request):
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
        invoice_number = generate_bill()
        

        if CD_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('davan_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = CD_Invoice.objects.create(
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

                CD_Item.objects.create(
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

        return redirect('davan_lists')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Cargill_Davn/davangere.html', context)


def davan_list(request):
    cdnvoices = CD_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Cargill_Davn/davangere_list.html', {'cdnvoices': cdnvoices})


def davan_detail(request, invoice_id):
    invoice = get_object_or_404(CD_Invoice, id=invoice_id)
    items = CD_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Cargill_Davn/davangere_details.html', {'invoice': invoice, 'items': items})

#=========================CARGILL BHIMASAR BILL ====================================================
def bhima_bill(request):
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
        

        if CB_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('KOP_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = CB_Invoice.objects.create(
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

                CB_Item.objects.create(
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

        return redirect('KOP_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Cargill_Bhima/bhimasar.html', context)


def bhima_list(request):
    tbnvoices = CB_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Cargill_Bhima/bhimasar_list.html', {'tbnvoices': tbnvoices})


def bhima_detail(request, invoice_id):
    invoice = get_object_or_404(CB_Invoice, id=invoice_id)
    items = CB_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Cargill_Bhima/bhimasar_details.html', {'invoice': invoice, 'items': items})

#=========================CARGILL KURKUMBH BILL ====================================================
def kurkm_bill(request):
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
        

        if CK_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('KOP_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = CK_Invoice.objects.create(
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

                CK_Item.objects.create(
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

        return redirect('kurkumbh_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Cargill_kum/kurkumbh.html', context)


def  kurkm_list(request):
    CKnvoices = CK_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Cargill_kum/kurkumbh_list.html', {'CKnvoices': CKnvoices})


def  kurkm_detail(request, invoice_id):
    invoice = get_object_or_404(CK_Invoice, id=invoice_id)
    items = CK_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Cargill_kum/kurkumbh_details.html', {'invoice': invoice, 'items': items})


#=========================BUNGE INDIA PVT LTD BILL ====================================================
def bunge_bill(request):
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
        

        if BU_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('KOP_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = BU_Invoice.objects.create(
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
        quantities = request.POST.getlist('tanker_cap')
        unit_prices = request.POST.getlist('item_unit_price')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                BU_Item.objects.create(
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

        return redirect('bunge_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Bunge/bunge.html', context)


def bunge_list(request):
    tbnvoices = BU_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Bunge/bunge_list.html', {'tbnvoices': tbnvoices})


def bunge_detail(request, invoice_id):
    invoice = get_object_or_404(BU_Invoice, id=invoice_id)
    items = BU_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/Bunge/bunge_details.html', {'invoice': invoice, 'items': items})


#=========================M/S AKM INTERNATIONAL BILL ====================================================
def akm_bill(request):
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
        

        if AKM_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('akm_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = AKM_Invoice.objects.create(
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
            unload=unload if unload else None,
            short=short if short else None,
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

                AKM_Item.objects.create(
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

        return redirect('akm_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/AKM_INT/akm.html', context)


def akm_list(request):
    tbnvoices = AKM_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/AKM_INT/akm_list.html', {'tbnvoices': tbnvoices})


def akm_detail(request, invoice_id):
    invoice = get_object_or_404(AKM_Invoice, id=invoice_id)
    items = AKM_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/AKM_INT/akm_details.html', {'invoice': invoice, 'items': items})

#========================ANJANI AGRO INDUSTRIES BILL====================================================
def anjani_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if ANGInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('anjani_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = ANGInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                ANGItem.objects.create(
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

        return redirect('anjani_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/ANJANI/anjani.html', context)


def anjani_list(request):
    ginvoice = ANGInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/ANJANI/anjani_list.html', {'ginvoice': ginvoice})


def anjani_detail(request, invoice_id):
    invoice = get_object_or_404(ANGInvoice, id=invoice_id)
    items = ANGItem.objects.filter(invoice=invoice)
    return render(request, 'bills/ANJANI/anjani_details.html', {'invoice': invoice, 'items': items})


#========================SIDDHIVINAYAK DATA PVT LTD BILL====================================================
def siddhi_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if SVDInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('anjani_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = SVDInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                SVDItem.objects.create(
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

        return redirect('siddhi_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/SIDDHI/shiddhi.html', context)


def siddhi_list(request):
    ginvoice = SVDInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/SIDDHI/shiddhi_list.html', {'ginvoice': ginvoice})


def siddhi_detail(request, invoice_id):
    invoice = get_object_or_404(SVDInvoice, id=invoice_id)
    items = SVDItem.objects.filter(invoice=invoice)
    return render(request, 'bills/SIDDHI/shiddhi_details.html', {'invoice': invoice, 'items': items})



#========================VISWAAT CHEMICAL (AMBERNATH) PVT LTD BILL====================================================
def viswaa_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if VCLInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('viswaa_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = VCLInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                VCLItem.objects.create(
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

        return redirect('viswaa_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/VISWAAT/viswaat.html', context)


def viswaa_list(request):
    vclinvoice = VCLInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/VISWAAT/viswaat_list.html', {'vclinvoice': vclinvoice})


def viswaa_detail(request, invoice_id):
    invoice = get_object_or_404(VCLInvoice, id=invoice_id)
    items = VCLItem.objects.filter(invoice=invoice)
    return render(request, 'bills/VISWAAT/viswaat_details.html', {'invoice': invoice, 'items': items})


#================================GRANUELS INDIA BILL====================================================
def granuels_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
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
        if GRNInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('granuel_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = GRNInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
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
                

                GRNItem.objects.create(
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

        return redirect('granuel_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/GRANUELS/granuels.html', context)


def granuels_list(request):
    ginvoice = GRNInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/GRANUELS/granuels_list.html', {'ginvoice': ginvoice})


def granuels_detail(request, invoice_id):
    invoice = get_object_or_404(GRNInvoice, id=invoice_id)
    items = GRNItem.objects.filter(invoice=invoice)
    return render(request, 'bills/GRANUELS/granuels_details.html', {'invoice': invoice, 'items': items})


#=================================HABHIT WELLNESS PVT LTD BILL====================================================
def habhit_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        tanker_cap = request.POST.get('tanker_cap')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')
        total_kg = request.POST.get('total_kg')

         # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        if HInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('habit_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = HInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            From_add=From_add,
            To_add=To_add,
            date_dis=date_dis,
            lr_no=lr_no,
            total_kg=total_kg,
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
                

                HItem.objects.create(
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

        return redirect('habit_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/Habit_welness/Habhit.html', context)


def habhit_list(request):
    HBinvoice = HInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/Habit_welness/Habhit_list.html', {'HBinvoice': HBinvoice})


def habhit_detail(request, invoice_id):
    invoice = get_object_or_404(HInvoice, id=invoice_id)
    items = HItem.objects.filter(invoice=invoice)
    return render(request, 'bills/Habit_welness/Habhit_details.html', {'invoice': invoice, 'items': items})

#================================= MULTI BILL================================
#========================VVF INDIA (BADDI) LTD====================================================
def generate_bill_VB():
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
    bill_no = f"{random_number}/VB/{month}/{financial_year}"
    return bill_no


def vvfbaddi_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        # tanker = request.POST.get('tanker')
        # From_add = request.POST.get('From_add')
        # To_add = request.POST.get('To_add')
        # date_dis = request.POST.get('date_dis')
        # lr_no = request.POST.get('lr_no')
        sac = request.POST.get('sac')
        

         # Step 2: Generate invoice number
        invoice_number = generate_bill_VB()
        if VVFMInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('baddi_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = VVFMInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            # tanker=tanker,
            # From_add=From_add,
            # To_add=To_add,
            # date_dis=date_dis,
            # lr_no=lr_no,
            sac=sac if sac else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # New: tanker, lr_no, from_add, to_add per item
        tanker_list = request.POST.getlist('item_tanker')
        lr_no_list = request.POST.getlist('item_lr_no')
        from_add_list = request.POST.getlist('item_From_add')
        to_add_list = request.POST.getlist('item_To_add')
        to_date_dis =request.POST.getlist('item_date_dis')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price 
                subtotal += line_total
                

                VVFMItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price,
                    tanker=tanker_list[i] if i < len(tanker_list) else '',
                    lr_no=lr_no_list[i] if i < len(lr_no_list) else '',
                    From_add=from_add_list[i] if i < len(from_add_list) else '',
                    To_add=to_add_list[i] if i < len(to_add_list) else '',
                    date_dis=to_date_dis[i] if i < len(to_date_dis) else '',
                )
            except (ValueError, IndexError):
                continue
        

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
        grand_total = round(basic_amount + cgst + sgst + igst, 2)
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
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('vvf_baddi_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/VVF_Baddi/baddi.html', context)


def vvfbaddi_list(request):
    ginvoice = VVFMInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/VVF_Baddi/baddi_list.html', {'ginvoice': ginvoice})


def vvfbaddi_detail(request, invoice_id):
    invoice = get_object_or_404(VVFMInvoice, id=invoice_id)
    items = VVFMItem.objects.filter(invoice=invoice)
    return render(request, 'bills/VVF_Baddi/baddi_details.html', {'invoice': invoice, 'items': items})

#========================VVF INDIA (TALOJA) LTD MULTI BILL====================================================
# def generate_bill_VB():
#     now = datetime.now()  
#     month = f"{now.month:02d}"  
#     year = now.year
#     random_number = random.randint(1000, 9999)  # 4-digit random


#     if now.month >= 4:  # April se new financial year
#         fy_start = str(year)[-2:]
#         fy_end = str(year + 1)[-2:]
#     else:
#         fy_start = str(year - 1)[-2:]
#         fy_end = str(year)[-2:]

#     financial_year = f"{fy_start}-{fy_end}"

#     # Final bill number
#     bill_no = f"{random_number}/VB/{month}/{financial_year}"
#     return bill_no


# def vvfbaddi_bill(request):
#     if request.method == "POST":
#         date = request.POST.get('date')
#         company = request.POST.get('company')
#         gst = request.POST.get('gst')  # This is buyer GST (To GST)
#         pan = request.POST.get('pan')
#         # tanker = request.POST.get('tanker')
#         # From_add = request.POST.get('From_add')
#         # To_add = request.POST.get('To_add')
#         # date_dis = request.POST.get('date_dis')
#         # lr_no = request.POST.get('lr_no')
#         sac = request.POST.get('sac')
        

#          # Step 2: Generate invoice number
#         invoice_number = generate_bill_VB()
#         if VVFMInvoice.objects.filter(date=date,company=company).exists():
#             messages.error(request, 'Bill already Exists!!')
#             return redirect('baddi_bill')
#         else:
          
#         # Step 3: Create empty invoice
#          invoice = VVFMInvoice.objects.create(
#             invoice_number=invoice_number,
#             date=date,
#             company=company,
#             gst=gst,
#             pan=pan,
#             # tanker=tanker,
#             # From_add=From_add,
#             # To_add=To_add,
#             # date_dis=date_dis,
#             # lr_no=lr_no,
#             sac=sac if sac else 0,
#             total_amount=0.0
#         )

#         # Step 4: Handle item data
#         item_data = request.POST.getlist('item_description')
#         quantities = request.POST.getlist('item_quantity')
#         unit_prices = request.POST.getlist('item_unit_price')

#         # New: tanker, lr_no, from_add, to_add per item
#         tanker_list = request.POST.getlist('item_tanker')
#         lr_no_list = request.POST.getlist('item_lr_no')
#         from_add_list = request.POST.getlist('item_From_add')
#         to_add_list = request.POST.getlist('item_To_add')
#         to_date_dis =request.POST.getlist('item_date_dis')

#         subtotal = 0.0

#         for i in range(len(item_data)):
#             try:
#                 quantity = int(quantities[i])
#                 unit_price = float(unit_prices[i])
#                 line_total = quantity * unit_price 
#                 subtotal += line_total
                

#                 VVFMItem.objects.create(
#                     invoice=invoice,
#                     description=item_data[i],
#                     quantity=quantity,
#                     unit_price=unit_price,
#                     tanker=tanker_list[i] if i < len(tanker_list) else '',
#                     lr_no=lr_no_list[i] if i < len(lr_no_list) else '',
#                     From_add=from_add_list[i] if i < len(from_add_list) else '',
#                     To_add=to_add_list[i] if i < len(to_add_list) else '',
#                     date_dis=to_date_dis[i] if i < len(to_date_dis) else '',
#                 )
#             except (ValueError, IndexError):
#                 continue
        

#         basic_amount = subtotal 

#         cgst_rate = 0.06
#         sgst_rate = 0.06
#         igst_rate = 0.12

#         # GST-based logic
#         company_gst = "27XXXXX0000Z5A" 
#         from_gst_code = extract_gst_code(company_gst)  # Your GST
#         to_gst_code = extract_gst_code(gst)  # Customer GST

#         if from_gst_code == '27' and to_gst_code == '27':
#             # Intra-state (Maharashtra)
#             cgst = round(basic_amount * cgst_rate, 2)
#             sgst = round(basic_amount * sgst_rate, 2)
#             igst = 0.0
#         else:
#             # Inter-state
#             cgst = 0.0
#             sgst = 0.0
#             igst = round(basic_amount * igst_rate, 2)

#         fright_total = round(basic_amount + cgst + sgst + igst, 2)
#         grand_total = round(basic_amount + cgst + sgst + igst, 2)
#        # Check decimal part
#         decimal_part = grand_total - int(grand_total)

#         # Add 1 rupee if decimal part > 0.50
#         if decimal_part > 0.50:
#           grand_total = int(grand_total) + 1
#         else:
#             grand_total = int(grand_total)

#         #  final output looks like 1000.00 format
#         formatted_total = "{:.2f}".format(grand_total)



#         # Step 6: Save tax and total
#         invoice.total_amount = basic_amount
#         invoice.cgst = cgst
#         invoice.sgst = sgst
#         invoice.igst = igst
#         invoice.fright_total = fright_total 
#         invoice.grand_total = formatted_total
#         invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
#         invoice.save()
#         messages.success(request, 'Bill generate successfully !!')

#         return redirect('vvf_baddi_list')

#     vehicle = Add_Vehicle.objects.all()
#     company = companydetails.objects.all()
#     dname = NewDriver_Details.objects.all()
#     context = {'vehicle': vehicle, 'company': company, 'dname': dname}

#     return render(request, 'bills/VVF_Baddi/baddi.html', context)


# def vvfbaddi_list(request):
#     ginvoice = VVFMInvoice.objects.all().order_by('date')  # Latest invoice first
#     return render(request, 'bills/VVF_Baddi/baddi_list.html', {'ginvoice': ginvoice})


# def vvfbaddi_detail(request, invoice_id):
#     invoice = get_object_or_404(VVFMInvoice, id=invoice_id)
#     items = VVFMItem.objects.filter(invoice=invoice)
#     return render(request, 'bills/VVF_Baddi/baddi_details.html', {'invoice': invoice, 'items': items})

#====================================VERTEX SALES PVT  LTD MULTI BILL====================================================
# def generate_bill_V():
#     now = datetime.now()  
#     month = f"{now.month:02d}"  
#     year = now.year
#     random_number = random.randint(1000, 9999)  # 4-digit random


#     if now.month >= 4:  # April se new financial year
#         fy_start = str(year)[-2:]
#         fy_end = str(year + 1)[-2:]
#     else:
#         fy_start = str(year - 1)[-2:]
#         fy_end = str(year)[-2:]

#     financial_year = f"{fy_start}-{fy_end}"

#     # Final bill number
#     bill_no = f"{random_number}/VB/{month}/{financial_year}"
#     return bill_no


def vertex_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        # tanker = request.POST.get('tanker')
        # From_add = request.POST.get('From_add')
        # To_add = request.POST.get('To_add')
        # date_dis = request.POST.get('date_dis')
        # lr_no = request.POST.get('lr_no')
        sac = request.POST.get('sac')
        

         # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        if VERTEXInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('vertex_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = VERTEXInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            # tanker=tanker,
            # From_add=From_add,
            # To_add=To_add,
            # date_dis=date_dis,
            # lr_no=lr_no,
            sac=sac if sac else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # New: tanker, lr_no, from_add, to_add per item
        tanker_list = request.POST.getlist('item_tanker')
        lr_no_list = request.POST.getlist('item_lr_no')
        from_add_list = request.POST.getlist('item_From_add')
        to_add_list = request.POST.getlist('item_To_add')
        to_date_dis =request.POST.getlist('item_date_dis')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price 
                subtotal += line_total
                

                VERTEXItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price,
                    tanker=tanker_list[i] if i < len(tanker_list) else '',
                    lr_no=lr_no_list[i] if i < len(lr_no_list) else '',
                    From_add=from_add_list[i] if i < len(from_add_list) else '',
                    To_add=to_add_list[i] if i < len(to_add_list) else '',
                    date_dis=to_date_dis[i] if i < len(to_date_dis) else '',
                )
            except (ValueError, IndexError):
                continue
        

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
        grand_total = round(basic_amount + cgst + sgst + igst, 2)
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
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('vertex_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/VERTEX/vertex.html', context)


def vertex_list(request):
    ginvoice = VERTEXInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/VERTEX/vertex_list.html', {'ginvoice': ginvoice})


def vertex_detail(request, invoice_id):
    invoice = get_object_or_404(VERTEXInvoice, id=invoice_id)
    items = VERTEXItem.objects.filter(invoice=invoice)
    return render(request, 'bills/VERTEX/vertex_details.html', {'invoice': invoice, 'items': items})

#====================================ALLANA PVT LTD.MULTI BILL====================================================
def generate_bill_AL():
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
    bill_no = f"{random_number}/F/{month}/{financial_year}"
    return bill_no


def allana_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        # tanker = request.POST.get('tanker')
        # From_add = request.POST.get('From_add')
        # To_add = request.POST.get('To_add')
        # date_dis = request.POST.get('date_dis')
        # lr_no = request.POST.get('lr_no')
        sac = request.POST.get('sac')
        

         # Step 2: Generate invoice number
        invoice_number = generate_bill_AL()
        if ALLANAInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('allana_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = ALLANAInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            # tanker=tanker,
            # From_add=From_add,
            # To_add=To_add,
            # date_dis=date_dis,
            # lr_no=lr_no,
            sac=sac if sac else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # New: tanker, lr_no, from_add, to_add per item
        tanker_list = request.POST.getlist('item_tanker')
        lr_no_list = request.POST.getlist('item_lr_no')
        from_add_list = request.POST.getlist('item_From_add')
        to_add_list = request.POST.getlist('item_To_add')
        to_date_dis =request.POST.getlist('item_date_dis')
        to_load_list=request.POST.getlist('item_load')
        to_unload_list=request.POST.getlist('item_unload')
        to_short_list=request.POST.getlist('item_short')
        to_retn_list=request.POST.getlist('item_retn')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price 
                subtotal += line_total
                

                ALLANAItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price,
                    tanker=tanker_list[i] if i < len(tanker_list) else '',
                    lr_no=lr_no_list[i] if i < len(lr_no_list) else '',
                    From_add=from_add_list[i] if i < len(from_add_list) else '',
                    To_add=to_add_list[i] if i < len(to_add_list) else '',
                    date_dis = to_date_dis[i] if i < len(to_date_dis) and to_date_dis[i] else None,
                    load=float(to_load_list[i]) if i < len(to_load_list) and to_load_list[i] else 0,
                    unload=float(to_unload_list[i]) if i < len(to_unload_list) and to_unload_list[i] else 0,
                    short=float(to_short_list[i]) if i < len(to_short_list) and to_short_list[i] else 0,
                    retn=float(to_retn_list[i]) if i < len(to_retn_list) and to_retn_list[i] else 0,

                )
            except (ValueError, IndexError):
                continue
        

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
        grand_total = round(basic_amount + cgst + sgst + igst, 2)
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
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('allanalist')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/ALLANA_KHOP/allana.html', context)


def allana_list(request):
    ainvoice = ALLANAInvoice.objects.all().order_by('date')
    return render(request, 'bills/ALLANA_KHOP/allana_list.html', {'ainvoice': ainvoice})



def allana_detail(request, invoice_id):
    invoice = get_object_or_404(ALLANAInvoice, id=invoice_id)
    items = ALLANAItem.objects.filter(invoice=invoice)
    return render(request, 'bills/ALLANA_KHOP/allana_details.html', {'invoice': invoice, 'items': items})


#===================================AAK INDIA DETENTION BILL====================================
def AAKdetention_bill(request):
    if request.method == "POST":
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        # tanker = request.POST.get('tanker')
        # From_add = request.POST.get('From_add')
        # To_add = request.POST.get('To_add')
        # date_dis = request.POST.get('date_dis')
        # lr_no = request.POST.get('lr_no')
        sac = request.POST.get('sac')
        

         # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        if AAKDEInvoice.objects.filter(date=date,company=company).exists():
            messages.error(request, 'Bill already Exists!!')
            return redirect('aakdt_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = AAKDEInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            # tanker=tanker,
            # From_add=From_add,
            # To_add=To_add,
            # date_dis=date_dis,
            # lr_no=lr_no,
            sac=sac if sac else 0,
            total_amount=0.0
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # New: tanker, lr_no, from_add, to_add per item
        tanker_list = request.POST.getlist('item_tanker')
        lr_no_list = request.POST.getlist('item_lr_no')
        from_add_list = request.POST.getlist('item_From_add')
        to_add_list = request.POST.getlist('item_To_add')
        to_date_dis =request.POST.getlist('item_date_dis')
        to_load_list=request.POST.getlist('item_load')
        to_unload_list=request.POST.getlist('item_unload')
        to_short_list=request.POST.getlist('item_short')
        to_retn_list=request.POST.getlist('item_retn')
        to_rate_list=request.POST.getlist('item_rate')
        to_qty_list=request.POST.getlist('item_qty')
        to_fo_date_list=request.POST.getlist('item_Fo_date')
        to_to_date_list=request.POST.getlist('item_To_date')
        to_charges_list=request.POST.getlist('item_charges')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price 
                subtotal += line_total
                

                AAKDEItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price,
                    tanker=tanker_list[i] if i < len(tanker_list) else '0',
                    lr_no=lr_no_list[i] if i < len(lr_no_list) else '0',
                    From_add=from_add_list[i] if i < len(from_add_list) else '',
                    To_add=to_add_list[i] if i < len(to_add_list) else '',
                    date_dis = to_date_dis[i] if i < len(to_date_dis) and to_date_dis[i] else None,
                    load=float(to_load_list[i]) if i < len(to_load_list) and to_load_list[i] else 0,
                    unload=float(to_unload_list[i]) if i < len(to_unload_list) and to_unload_list[i] else 0,
                    short=float(to_short_list[i]) if i < len(to_short_list) and to_short_list[i] else 0,
                    retn=float(to_retn_list[i]) if i < len(to_retn_list) and to_retn_list[i] else 0,
                    rate=to_rate_list[i] if i < len(to_rate_list) and to_rate_list[i] else 0,
                    qty=to_qty_list[i] if i < len(to_qty_list) and to_qty_list[i] else 0,
                    Fo_date=to_fo_date_list[i] if i < len(to_fo_date_list) and to_fo_date_list[i] else 0,
                    To_date=to_to_date_list[i] if i < len(to_to_date_list) and to_to_date_list[i] else 0,
                    charges=to_charges_list[i] if i < len(to_charges_list) and to_charges_list[i] else 0,

                )
            except (ValueError, IndexError):
                continue
        

        basic_amount = subtotal 

        cgst_rate = 0.09
        sgst_rate = 0.09
        igst_rate = 0.18

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
        grand_total = round(basic_amount + cgst + sgst + igst, 2)
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
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('aakdt_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/AAK_DETENTION/detention.html', context)


def AAKdetention_list(request):
    aainvoice = AAKDEInvoice.objects.all().order_by('date')
    return render(request, 'bills/AAK_DETENTION/detention_list.html', {'aainvoice': aainvoice})



def AAKdetention_detail(request, invoice_id):
    invoice = get_object_or_404(AAKDEInvoice, id=invoice_id)
    items = AAKDEItem.objects.filter(invoice=invoice)
    return render(request, 'bills/AAK_DETENTION/detention_details.html', {'invoice': invoice, 'items': items})




#===================================MORDE FOODS PVT LTD====================================================
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None
def morde_bill(request):
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
        unloadcharge = request.POST.get('unloadcharge')
        unloadrate = request.POST.get('unloadrate')

        Fo_dateD = parse_date(request.POST.get('Fo_dateD'))
        To_dateD = parse_date(request.POST.get('To_dateD'))
        d_rateD = request.POST.get('d_rateD')
        par_dayD = request.POST.get('par_dayD')
        totalD = request.POST.get('totalD')
        sacD = request.POST.get('sacD')
        charges_D = request.POST.get('charges_D')
        

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if MOR_Invoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('morde_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = MOR_Invoice.objects.create(
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
            unloadcharge=unloadcharge if total_d else None,
            unloadrate=unloadrate if total_d else None,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if Fo_date else None,
            d_rate=d_rate if total_d else 0,
            par_day=par_day if total_d else 0,
            total_d=total_d if total_d else 0,
            total_amount=0.0,
            sacD=sacD if sacD else 0,
            Fo_dateD=Fo_dateD if Fo_dateD else 0,
            To_dateD=To_dateD if To_dateD else 0,
            d_rateD=d_rateD if d_rateD else 0,
            par_dayD=par_dayD if par_dayD else 0,
            totalD=totalD if totalD else 0,
            charges_D=charges_D if charges_D else 0,
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

                MOR_Item.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price
                )
            except (ValueError, IndexError):
                continue
        
        g_amount = float(total_d or 0) + float( totalD or 0)  # or Decimal(total_d)

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
        invoice.g_amount = g_amount
        invoice.total_d = total_d 
        invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('morde_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/MORDE/morde.html', context)


def morde_list(request):
    Dnvoices = MOR_Invoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/MORDE/morde_list.html', {'Dnvoices': Dnvoices})


def morde_detail(request, invoice_id):
    invoice = get_object_or_404(MOR_Invoice, id=invoice_id)
    items = MOR_Item.objects.filter(invoice=invoice)
    return render(request, 'bills/MORDE/morde_details.html', {'invoice': invoice, 'items': items})


#===================================AAK INDIA (REIMBURESEMENT ) BILL==================
def aakreim_bill(request):
    return render(request,'bills/AAK_REIMBURES/aak_india.html')

def AAKREM_bill(request):
    if request.method == "POST":
        # Step 1: Extract invoice data
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')  # This is buyer GST (To GST)
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
       
        Fo_date = request.POST.get('Fo_date')
        total_mt = request.POST.get('total_mt')
        f_total = request.POST.get('f_total')
        
        # d_rate = request.POST.get('d_rate')
        # par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        sac = request.POST.get('sac')
        charges = request.POST.get('charges')
        hsac = request.POST.get('hsac')
        Scharges = request.POST.get('Scharges')
        Stotal_d = request.POST.get('Stotal_d')
        Shsac = request.POST.get('Shsac')
        SFo_date = request.POST.get('SFo_date')

        # Fo_dateD = parse_date(request.POST.get('Fo_dateD'))
        # To_dateD = parse_date(request.POST.get('To_dateD'))
        # d_rateD = request.POST.get('d_rateD')
        # par_dayD = request.POST.get('par_dayD')
        # totalD = request.POST.get('totalD')
        # sacD = request.POST.get('sacD')
        # charges_D = request.POST.get('charges_D')
        

        # Step 2: Generate invoice number
        invoice_number = generate_bill_no()
        

        if AAKRMInvoice.objects.filter(date=date,company=company).exists():
           messages.error(request, 'Bill already Exists!!')
           return redirect('AAK_reimbures_bill')
        else:
          
        # Step 3: Create empty invoice
         invoice = AAKRMInvoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company,
            gst=gst,
            pan=pan,
            tanker=tanker,
            sac=sac if sac else 0,
            total_mt=total_mt if total_mt else 0,
            f_total=f_total if f_total else 0,
            # unloadcharge=unloadcharge if total_d else None,
            # unloadrate=unloadrate if total_d else None,
            charges=charges if total_d else None,
            hsac=hsac if hsac else 0,
            Fo_date=Fo_date if Fo_date else None,
            total_d=total_d if total_d else 0,
            total_amount=0.0,
            date_from= date_from if  date_from else 0,
            date_to= date_to if  date_to else 0,
            Scharges=Scharges if Scharges else 0,
            Stotal_d=Stotal_d if Stotal_d else 0,
            Shsac=Shsac if Shsac else 0,
            SFo_date=SFo_date if SFo_date else 0,
            # par_dayD=par_dayD if par_dayD else 0,
            # totalD=totalD if totalD else 0,
            #  date_from= date_from if  date_from else 0,
        )

        # Step 4: Handle item data
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        tanker_no_list = request.POST.getlist('item_tanker_no')
        date_list = request.POST.getlist('item_date')
        from_add_list = request.POST.getlist('item_From_add')
        to_add_list = request.POST.getlist('item_To_add')
        to_lrno_list =request.POST.getlist('item_lrno')
        to_totalkm_list=request.POST.getlist('item_totalkm')
        to_diesel_list=request.POST.getlist('item_diesel')
        to_dieselrate_list=request.POST.getlist('item_dieselrate')
        to_dieselamount_list=request.POST.getlist('item_dieselamount')
        to_urearate_list=request.POST.getlist('item_urearate')
        to_ureaamount_list=request.POST.getlist('item_ureaamount')
        to_toll_list=request.POST.getlist('item_toll')
        to_totalamount_list=request.POST.getlist('item_totalamount')

        subtotal = 0.0

        for i in range(len(item_data)):
            try:
                quantity = int(quantities[i])
                unit_price = float(unit_prices[i])
                line_total = quantity * unit_price
                subtotal += line_total

                AAKRMItem.objects.create(
                    invoice=invoice,
                    description=item_data[i],
                    quantity=quantity,
                    unit_price=unit_price,
                    tanker_no=tanker_no_list[i] if i < len(tanker_no_list) else '',
                    date=date_list[i] if i < len(date_list) else None,
                    From_add=from_add_list[i] if i < len(from_add_list) else '',
                    To_add=to_add_list[i] if i < len(to_add_list) else '',
                    lrno = to_lrno_list[i] if i < len(to_lrno_list) and to_lrno_list[i] else None,
                    totalkm=float(to_totalkm_list[i]) if i < len(to_totalkm_list) and to_totalkm_list[i] else 0,
                    diesel=float(to_diesel_list[i]) if i < len(to_diesel_list) and to_diesel_list[i] else 0,
                    dieselrate=float(to_dieselrate_list[i]) if i < len(to_dieselrate_list) and to_dieselrate_list[i] else 0,
                    dieselamount=float(to_dieselamount_list[i]) if i < len(to_dieselamount_list) and to_dieselamount_list[i] else 0,
                    urearate=float(to_urearate_list[i]) if i < len(to_urearate_list) and to_urearate_list[i] else 0,
                    ureaamount=float(to_ureaamount_list[i]) if i < len(to_ureaamount_list) and to_ureaamount_list[i] else 0,
                    toll=float(to_toll_list[i]) if i < len(to_toll_list) and to_toll_list[i] else 0,
                    totalamount=float(to_totalamount_list[i]) if i < len(to_totalamount_list) and to_totalamount_list[i] else 0,

                )
            except (ValueError, IndexError):
                continue
        # Step 5: Calculate items' totalamount sum
        items_total_sum = AAKRMItem.objects.filter(invoice=invoice).aggregate(
        Sum('totalamount')
        )['totalamount__sum'] or 0

        # Optional: round it up like before
        items_integer_part = int(items_total_sum)
        items_decimal_part = items_total_sum - items_integer_part

        if items_decimal_part > 0.50:
            items_total_sum = items_integer_part + 1
        else:
            items_total_sum = items_integer_part

        g_amount = float(total_d or 0)  # or Decimal(total_d)   + float( totalD or 0)

        freight=float(f_total or 0) + float(Stotal_d or 0)
        basic_amount = freight + float(total_d or 0) 

        cgst_rate = 0.09
        sgst_rate = 0.09
        igst_rate = 0.18

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
        grand_total = round(basic_amount + cgst + sgst + igst + items_total_sum, 2)


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
        # invoice.c_gst = c_gst
        # invoice.s_gst = s_gst
        # invoice.i_gst = i_gst
        invoice.total_amount = basic_amount
        invoice.cgst = cgst
        invoice.sgst = sgst
        invoice.igst = igst
        invoice.total_d = total_d 
        # invoice.g_total = g_total
        invoice.fright_total = fright_total 
        invoice.grand_total = formatted_total
        # invoice. total_in_words = num2words(formatted_total)
        invoice. total_in_words =num2words(formatted_total, lang='en_IN').title().replace(",", "")+ " " + "ONLY"
        invoice.save()
        messages.success(request, 'Bill generate successfully !!')

        return redirect('AAK_reimbures_list')

    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'vehicle': vehicle, 'company': company, 'dname': dname}

    return render(request, 'bills/AAK_REIMBURES/AAK.html', context)



def AAKREM_list(request):
    ARinvoice = AAKRMInvoice.objects.all().order_by('date')  # Latest invoice first
    return render(request, 'bills/AAK_REIMBURES/AAK_list.html', {'ARinvoice': ARinvoice})


def AAKREM_detail(request, invoice_id):
    invoice = get_object_or_404(AAKRMInvoice, id=invoice_id)
    items = AAKRMItem.objects.filter(invoice=invoice)
    total_sum = items.aggregate(Sum('totalamount'))['totalamount__sum'] or 0
    integer_part = int(total_sum)
    decimal_part = total_sum - integer_part

    if decimal_part > 0.50:
        total_sum = integer_part + 1
    else:
        total_sum = integer_part
    return render(request, 'bills/AAK_REIMBURES/AAK_details.html', {'invoice': invoice, 'items': items,'total_sum':total_sum})

#=======================INVENTORY MANAGEMENT SYSTEM=============================================

def inventroy_system(request):
    items=Items.objects.count()
    useitem=UsedItem.objects.count()
    tool=Tools.objects.count()
    usetool=Usetool.objects.count()
    context={'items':items,'useitem':useitem,'tool':tool,'usetool':usetool}
    
    return render(request, 'Inventory/dashboard.html',context)


#======================ADD ITEM ITEM FORM===========================

def inventroy_form(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        item_qty = request.POST.get('item_qty')
        item_date = request.POST.get('item_date')  
        vendor_name = request.POST.get('vendor_name')
        item=Items.objects.create(item_name=item_name,item_qty=item_qty,item_date=item_date,vendor_name=vendor_name if vendor_name else None)
        item.save()
        return redirect('show-item')
    return render(request, 'Inventory/inventory.html')



def show_item(request):
     item_name = request.GET.get(' item_name')
     vendor_name = request.GET.get('vendor_name')
     item_date = request.GET.get('item_date')
    
     showitem=Items.objects.all()

     if item_name:
        showitem = showitem.filter(item_name__icontains=item_name)

     if vendor_name:
        showitem = showitem.filter(vendor_name__icontains=vendor_name)

     if item_date:
        showitem = showitem.filter(item_date__icontains=item_date)

     context={'showitem':showitem}
     return render(request,'Inventory/show_item.html',context)



def delete_item(request,id):
    itemdelete=Items.objects.get(pk=id)
    itemdelete.delete()
    return redirect('show-item')

def update_tool(request,id):
    updateitem=Items.objects.get(pk=id)
    context={'updateitem':updateitem}
    return render(request,'Inventory/update_item.html',context)


#====================== USED ITEM FORM===========================



def service_form(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        tanker = request.POST.get('tanker')
        person_name= request.POST.get('person_name')
        used_on= request.POST.get('used_on')

        try:
            item = Items.objects.get(id=item_id)

            if item.item_qty >= quantity:
                # Create UsedItem entry
                UsedItem.objects.create(item=item, quantity=quantity,tanker=tanker,person_name=person_name,used_on=used_on)
                # Update store quantity
                item.item_qty -= quantity
                item.save()
                messages.success(request, 'Item used successfully!')
            else:
                messages.error(request, 'Not enough quantity in store.')

        except Item.DoesNotExist:
            messages.error(request, 'Item not found.')

        return redirect('show-useitem')  # Replace with your view name or URL

    else:
        vehicle=Add_Vehicle.objects.all()
        item=Items.objects.all()
        context={'vehicle':vehicle,'item':item}
        return render(request, 'Inventory/service.html',context)


def show_useitem(request):
    itemused=UsedItem.objects.all()
    context={'itemused':itemused}
    return render(request, 'Inventory/show_useitem.html',context)
    
def delete_useite(request,id):
    dell=UsedItem.objects.get(pk=id)
    dell.delete()
    return redirect('show-useitem')


#======================TOOLS FORM===========================

def tools_form(request):
    if request.method == "POST":
        tool_name = request.POST.get('tool_name')
        tool_qty = request.POST.get('tool_qty')
        tool_date = request.POST.get('tool_date')  
        vendor_name = request.POST.get('vendor_name')
        tool=Tools.objects.create(tool_name=tool_name,tool_qty=tool_qty,tool_date=tool_date,vendor_name=vendor_name if vendor_name else None)
        tool.save()
        messages.success(request,"Tool Add Successfuly !")
        return redirect('tools-show')
    return render(request, 'Inventory/tool.html')



def tools_show(request):
     item_name = request.GET.get(' item_name')
     vendor_name = request.GET.get('vendor_name')
     item_date = request.GET.get('item_date')
    
     showtool=Tools.objects.all()

     if item_name:
        showitem = showitem.filter(item_name__icontains=item_name)

     if vendor_name:
        showitem = showitem.filter(vendor_name__icontains=vendor_name)

     if item_date:
        showitem = showitem.filter(item_date__icontains=item_date)

     context={'showtool':showtool}
     return render(request,'Inventory/show_tool.html',context)


def delete_tool(request,id):
    deltools=Tools.objects.get(pk=id)
    deltools.delete()
    return redirect('tools-show')
#======================USED TOOLS FORM===========================
def use_tool(request):
    if request.method == "POST":
        try:
            tool_id = request.POST.get('tool_id')
            person_name = request.POST.get('person_name')
            tool_condition = request.POST.get('tool_condition')
            tool_take = request.POST.get('tool_take')
            tool_return = request.POST.get('tool_return')
            issue = request.POST.get('issue')
            use_of = request.POST.get('use_of')
            qty_str = request.POST.get('qty')


            try:
                qty = Decimal(qty_str)
            except (InvalidOperation, TypeError):
                messages.error(request, "Invalid quantity.")
                return redirect('tool-show')

            tool = Tools.objects.get(id=int(tool_id))

            if tool.tool_qty >= qty:
                Usetool.objects.create(
                    tool=tool,
                    person_name=person_name,
                    tool_condition=tool_condition,
                    tool_take=tool_take,
                    tool_return=tool_return,
                    issue=issue,
                    use_of=use_of,
                    qty=qty
                )
                tool.tool_qty-= qty
                tool.save()
                messages.success(request, "Used Tool added successfully!")
            else:
                messages.error(request, "Not enough tool quantity available.")

        except Tools.DoesNotExist:
            messages.error(request, "Tool not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('tool-show')

    tool_name =Tools.objects.all()
    context = {'tool_name': tool_name}
    return render(request, 'Inventory/use_tools.html', context)

def usetool_show(request):
     item_name = request.GET.get(' item_name')
     vendor_name = request.GET.get('vendor_name')
     item_date = request.GET.get('item_date')
    
     usetool=Usetool.objects.all()

     if item_name:
        showitem = showitem.filter(item_name__icontains=item_name)

     if vendor_name:
        showitem = showitem.filter(vendor_name__icontains=vendor_name)

     if item_date:
        showitem = showitem.filter(item_date__icontains=item_date)

     context={'usetool':usetool}
     return render(request,'Inventory/show_usetools.html',context)

def delete_usetool(request,id):
    deltools=Usetool.objects.get(pk=id)
    deltools.delete()
    return redirect('tool-show')


#======================VEHICLE INOUT TIME===========================



def inout_form(request):
    if request.method == "POST":
        tanke = request.POST.get('tanke')
        driver = request.POST.get('driver')
        tankertype = request.POST.get('tankertype')
        tankercapacity = request.POST.get('tankercapacity')
        tankercondition = request.POST.get('tankercondition')
        entry = request.POST.get('entry')
        fire = request.POST.get('fire')
        kit = request.POST.get('kit')
        intitme = request.POST.get('intitme')  
        outtitme = request.POST.get('outtitme')
        tool=Inout.objects.create(tanke=tanke,driver=driver,tankertype=tankertype,tankercapacity=tankercapacity,tankercondition=tankercondition,entry=entry,fire=fire,kit=kit,intitme=intitme,outtitme=outtitme if outtitme else None)
        tool.save()
        messages.success(request,"Tanker Entry Date & Time Add Successfuly !")
        return redirect('Inout-show')
    
    return render(request, 'Inventory/Vehicle_Inout.html')



def tankertime_show(request):
     item_name = request.GET.get(' item_name')
     vendor_name = request.GET.get('vendor_name')
     item_date = request.GET.get('item_date')
    
     showtool=Inout.objects.all()

     if item_name:
        showitem = showitem.filter(item_name__icontains=item_name)

     if vendor_name:
        showitem = showitem.filter(vendor_name__icontains=vendor_name)

     if item_date:
        showitem = showitem.filter(item_date__icontains=item_date)

     context={'showtool':showtool}
     return render(request,'Inventory/show_tanketime.html',context)

def delete_tanktime(request,id):
    deltools=Inout.objects.get(pk=id)
    deltools.delete()
    return redirect('Inout-show')

#====================TANKER SERVICES =================================

def tanker_service(request):
    if request.method == "POST":
        tanke = request.POST.get('tanke')
        owner_name = request.POST.get('owner_name')
        type = request.POST.get('type')
        date = request.POST.get('date')
        remark = request.POST.get('remark')
     
        service=Service.objects.create(tanke=tanke,owner_name=owner_name,type=type,date=date,remark=remark)
        service.save()
        messages.success(request,"Tanker Service Add Successfuly !")
        return redirect('show-service')
    
    return render(request, 'Inventory/tanker_service.html')


def show_service(request):
    showservice=Service.objects.all()
    context={'showservice':showservice}
    return render(request, 'Inventory/service_show.html',context)


def delete_service(request,id):
    deltools=Service.objects.get(pk=id)
    deltools.delete()
    return redirect('show-service')

#======================SHOW CHECK LIST=====================
def check_list(request):

    return render(request, 'Inventory/vehicle_check.html')


def show_list(request):

    return render(request, 'Inventory/show_checklist.html')


def gate_pass(request):

    return render(request, 'Inventory/gate_pass.html')


#=========================PROFIT & LOSS===========================================
def profit(request):
    if request.method=="POST":
      tanker=request.POST.get("tanker")
      from_add=request.POST.get("from_add")
      to_add=request.POST.get("to_add")
      trip=request.POST.get("trip")
      bill=request.POST.get("bill")
      company=request.POST.get("company")
      expese=request.POST.get("expese")
      bill_amount=request.POST.get("bill_amount")
      total=request.POST.get("total")

      profit=Profit.objects.create(tanker=tanker,from_add=from_add,to_add=to_add,trip=trip,bill=bill,company=company,expese=expese,bill_amount=bill_amount,total=total)
      profit.save()
      messages.success(request,"Data Add Successfuly !")
      return redirect('show_pro')
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    context={'vehicle':vehicle,'company':company}
    return render(request, 'profit_loss.html',context)

def Showprofit(request):
    showprofit=Profit.objects.all()
    context={'showprofit':showprofit}
    return render(request,'show_profit.html',context)



def tally(request):
    return render(request,'Tally_bill.html')



#====================================DRIVER LOCATION =====================================================
def reached_view(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    return render(request, 'reached.html', {'driver': driver})

def submit_location(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        
        driver = get_object_or_404(Driver, id=driver_id)
        LocationLog.objects.create(driver=driver, latitude=lat, longitude=lon)
        return JsonResponse({'status': 'success'})
    
def track_driver_view(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    latest_log = LocationLog.objects.filter(driver=driver).order_by('-timestamp').first()
    context = {
        'driver': driver,
        'latest_log': latest_log
    }
    return render(request, 'track_driver.html', context)



def vouchar(request):
    if request.method=="POST":
      tankerno=request.POST.get("tankerno")
      from_add=request.POST.get("from_add")
      To=request.POST.get("To")
      loadingdate=request.POST.get("loadingdate")
      cashname=request.POST.get("cashname")
      cashdate=request.POST.get("cashdate")
      cashamount=request.POST.get("cashamount")
      remark=request.POST.get("remark")
   
      cash=CashVoucher.objects.create(tankerno=tankerno,from_add=from_add,To=To if To else "",loadingdate=loadingdate if loadingdate else None,cashname=cashname,cashdate=cashdate,cashamount=cashamount,remark=remark if remark else "")
      cash.save()
      messages.success(request,"Cash Voucher Add Successfuly !")
      return redirect('show_voucher')
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname}
    return render(request, 'cash_vouchar.html',context)



def showvouchar(request):
    voucher=CashVoucher.objects.all()
    context={'voucher':voucher}
    return render(request, 'show_vouchar.html',context)


def deletevouchar(request,id):
    voucher=CashVoucher.objects.get(pk=id)
    voucher.delete()
    return redirect('show_voucher')


def get_subcategories(request, category_id):
    subcategories = SubCategory.objects.filter(category_id=category_id).values_list('name', flat=True)
    return JsonResponse(list(subcategories), safe=False)




def repayment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        amount = request.POST.get("amount")
        driverid = request.POST.get("driverid")
        tanker = request.POST.get("tanker")

        # Check if payment already exists
        if Payment.objects.filter(date=date, name=name).exists():
            messages.error(request, 'Repayment already exists !!')
            return redirect('payment_cash')
        else:
            # Create and save new payment
            payment = Payment.objects.create(tanker=tanker,driverid=driverid,name=name, date=date, amount=amount if amount else 0)
            messages.success(request, "Repayment added successfully!")

    # Fetch data to show in the form/page
    trip = Trip.objects.all()
    dname = NewDriver_Details.objects.all()
    context = {'dname': dname,'trip':trip}
    return render(request, 'repayment.html', context)


def get_payment(request):
    name = request.GET.get('name')
    if not name:
        return JsonResponse({'amount': 0})

    # last payment of driver (date ke hisaab se latest)
    last_payment = Payment.objects.filter(name=name).order_by('-id').first()

    if last_payment:
        return JsonResponse({'amount': last_payment.amount})
    else:
        return JsonResponse({'amount': 0})
    


def showrepayment(request):
    payment=Payment.objects.all()
    context={'payment':payment}
    return render(request,'show_repayment.html',context)


def deletepayment(request,id):
    pay=Payment.objects.get(pk=id)
    pay.delete()
    return redirect('show_payment')

    
def get_trip_details(request):
    trip_id = request.GET.get('trip_id')
    if trip_id:
        try:
            trip = Trip.objects.get(trip_id=trip_id)
            data = {
                'date': trip.trip_date.strftime('%Y-%m-%d'),  # ya desired format
                'driver_name': trip.drivername,
                'tanker' :trip.tanker, # model field adjust karein
            }
            return JsonResponse(data)
        except Trip.DoesNotExist:
            return JsonResponse({'error': 'Trip not found'}, status=404)
    return JsonResponse({'error': 'No trip ID provided'}, status=400)



import requests

def vehicle_data_view(request):
    try:
        response = requests.get("http://track.ansitindia.com/webservice?token=getLiveData&user=jnr&pass=jnr123&format=json")
        response.raise_for_status()  # Raises exception for HTTP errors
        data = response.json()
        vehicles = data.get("root", {}).get("VehicleData", [])
    except Exception as e:
        print("Error fetching data:", e)
        vehicles = []

    return render(request, "gps.html", {"vehicles": vehicles})



#===================================
# New Planning Page
#===================================

def party_list(request):
    parties = Party.objects.all()
    return render(request, "party_list.html", {"parties": parties})


def add_multiple_trips(request, party_id):
    party = get_object_or_404(Party, id=party_id)
    
    if request.method == "POST":
        dates = request.POST.getlist('date')
        tankers = request.POST.getlist('tanker_no')
        drivers = request.POST.getlist('driver')
        loads = request.POST.getlist('load_mt')
        statuses = request.POST.getlist('status')
        
        for i in range(len(dates)):
            PlanTrip.objects.create(
                party=party,
                date=dates[i],
                tanker_no=tankers[i],
                driver=drivers[i],
                load_mt=loads[i],
                status=statuses[i]
            )
        return redirect('trip_list', party_id=party.id)

    return render(request, "add_multiple_trips.html", {"party": party, "today": date.today()})



def trip_list(request, party_id):
    party = get_object_or_404(Party, id=party_id)
    trips = PlanTrip.objects.filter(party=party).order_by('-date')
    return render(request, "trip_list.html", {"party": party, "trips": trips})



def confirm_trip(request, trip_id):
    trip = get_object_or_404(PlanTrip, id=trip_id)
    trip.status = "confirm"  
    trip.save()
    return redirect("trip_list", party_id=trip.party.id)












#=====================================
# Profit & Loss 
#=====================================


def tanker_wise_expense(request):
    tankers = Trip.objects.values('tanker').distinct()

    result = []

    for t in tankers:
        tanker_no = t['tanker']
        total_exp = Expense.objects.filter(trip__tanker=tanker_no)\
                                   .aggregate(total=Sum('total_amount'))['total'] or 0

        result.append({
            'tanker': tanker_no,
            'expense': total_exp
        })

    return render(request, "tanker_wise_expense.html", {'result': result})


from django.db.models.functions import TruncMonth
def monthly_expense(request):
    report = (
        Expense.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('-month')
    )

    return render(request, "monthly_expense.html", {'report': report})



def driver_wise_expense(request):
    report = (
        Expense.objects
        .values('trip__drivername')  # Trip model से drivername
        .annotate(total=Sum('total_amount'))
        .order_by('-total')
    )
    for r in report:
        r['drivername'] = r.pop('trip__drivername')  
    return render(request, "driver_wise_expense.html", {'report': report})



def income_expense_chart(request):
    trips = Trip.objects.all().order_by('trip_id')
    labels = []
    income = []
    expense = []
    trip_data = []

    for trip in trips:
        labels.append(str(trip.trip_id))

        # Income calculation from all bill models
        trip_income = 0
        # ADANI KAKINADA
        trip_income += AKInvioce.objects.filter(tanker=trip.tanker).aggregate(total=Sum('grand_total'))['total'] or 0
        # ADANI MUNDRA
        trip_income += ADMInvioce.objects.filter(tanker=trip.tanker).aggregate(total=Sum('grand_total'))['total'] or 0
        # ASHLAND
        trip_income += ASL_Invoice.objects.filter(tanker=trip.tanker).aggregate(total=Sum('grand_total'))['total'] or 0
        # CARGILL
        trip_income += CRInvoice.objects.filter(tanker=trip.tanker).aggregate(total=Sum('grand_total'))['total'] or 0
        # AAK OUT WORD
        trip_income += Aak_in_Invoice.objects.filter(tanker=trip.tanker).aggregate(total=Sum('grand_total'))['total'] or 0
        # Expense calculation
        total_exp = trip.expenses.aggregate(total=Sum('total_amount'))['total'] or 0

        # Profit calculation
        trip_profit = float(trip_income) - float(total_exp)

        income.append(float(trip_income))
        expense.append(float(total_exp))

         # Add trip data including profit
        trip_data.append((trip.trip_id, float(trip_income), float(total_exp), trip_profit))


    context = {
        'labels': labels,
        'income': income,
        'expense': expense,
        'trip_data': trip_data
    }

    return render(request, "income_expense_chart.html", context)

