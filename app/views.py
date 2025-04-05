from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404, redirect
from django.http import JsonResponse
from num2words import num2words
from .models import *
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.utils.timezone import now
import random
import datetime




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
    
    plan = plandetails.objects.filter().last()
    if plan:
        tankerno = plan.tankerno
        drivername=plan.drivername
        From_address = plan.From_address
        To_address = plan.To_address
        tanker_capacity = plan.tanker_capacity
    else:
        tankerno = From_address = To_address = 'Data not available'
    
    if request.method =="POST":
       tankerno  = request.POST['tankerno']
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
       if   AddTrips.objects.filter(tankerno=tankerno, dispatch_time= dispatch_time).exists():
            messages.error(request, 'Trip already exists !!')
            return redirect('addtrip')
       else:
          trip=AddTrips(tankerno=tankerno,From_address=From_address,To_address=To_address,drivername=drivername if drivername else None,tank_capacity=tank_capacity if tank_capacity else None,arrival_time=arrival_time if arrival_time else None,dispatch_time=dispatch_time if dispatch_time else None,reach_time=reach_time if reach_time else None,unload_time=unload_time if unload_time else None,lr_num=lr_num if lr_num else None,lr_date=lr_date if lr_date else None,freight_bill=freight_bill if freight_bill else None,freight_date=freight_date if freight_date else None,loaded_qty=loaded_qty if loaded_qty else None,unload_qty=unload_qty if unload_qty else None,short_qty=short_qty if short_qty else None,short_allow=short_allow if short_allow else None,return_qty=return_qty if return_qty else None,remark=remark if remark else None,)
          trip.save()
          messages.success(request, 'Trip added successfully !!') 
    
    # Pass the values to the template
    context = {
        'tankerno': tankerno,
        'From_address': From_address,
        'To_address': To_address,
        'tanker_capacity': tanker_capacity,
        'drivername':drivername
    }
    return render(request, 'add/add_trip_all.html',context)
   

def updatetrip(request,id):
    uptrip=AddTrips.objects.get(pk=id)
    context={'uptrip':uptrip}
    return render (request,'update-add-trip.html',context)


def do_updatetrip(request,id): 
    tankerno = request.POST.get('tankerno')
    drivername = request.POST.get('drivername')
    From_address = request.POST.get('From_address')
    To_address = request.POST.get('To_address')
    tank_capacity = request.POST.get('tank_capacity')
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
    freight_bill = request.POST.get('freight_bill')
     

    # Fetch the existing plan details to update
    update_t = AddTrips.objects.get(pk=id)

    # Update the fields
    update_t.tankerno = tankerno
    update_t.drivername = drivername
    update_t.From_address = From_address
    update_t.To_address = To_address
    update_t.tank_capacity = tank_capacity
    update_t.dispatch_time = dispatch_time
    update_t.reach_time = reach_time
    update_t.unload_time = unload_time
    update_t.loaded_qty = loaded_qty
    update_t.percent = percent
    update_t.unload_qty = unload_qty
    update_t.short_qty = short_qty
    update_t.short_allow = short_allow
    update_t.return_qty = return_qty
    update_t.lr_num = lr_num
    update_t.return_qty = return_qty
    update_t.freight_bill = freight_bill

    # Save the changes
    update_t.save()

    # Success message
    messages.success(request, 'Trip updated successfully!')

    # Redirect to the showplan page (or wherever you need to redirect)
    return redirect('showtrip')










def Trip_Adani(request):
    plan = plandetails.objects.earliest('tankerno')  
    if plan:
        tankerno = plan.tankerno
        drivername=plan.drivername
        From_address = plan.From_address
        To_address = plan.To_address
        tanker_capacity = plan.tanker_capacity
    else:
        tankerno = From_address = To_address = 'Data not available'
    
    if request.method =="POST":
       tankerno  = request.POST['tankerno']
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
       if   TripAdani.objects.filter(tankerno=tankerno, dispatch_time= dispatch_time).exists():
            messages.error(request, 'Trip already exists !!')
            return redirect('trip-adani')
       else:
          trip=TripAdani(tankerno=tankerno,
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
    context = {
        'tankerno': tankerno,
        'From_address': From_address,
        'To_address': To_address,
        'tanker_capacity': tanker_capacity,
        'drivername':drivername
    }
    return render(request, 'add/add_trip_adani.html',context)

def ShowAdani(request):
    adani=TripAdani.objects.all()
    context={'adani':adani}
    return render(request,'show/show_adani.html',context)



def Trip_Gemini(request):
    plan = plandetails.objects.earliest('tankerno')  
    if plan:
        tankerno = plan.tankerno
        drivername=plan.drivername
        From_address = plan.From_address
        To_address = plan.To_address
        tanker_capacity = plan.tanker_capacity
    else:
        tankerno = From_address = To_address = 'Data not available'
    
    if request.method =="POST":
       tankerno  = request.POST['tankerno']
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
       if   TripGemini.objects.filter(tankerno=tankerno, dispatch_time= dispatch_time).exists():
            messages.error(request, 'Trip already exists !!')
            return redirect('trip-gemini')
       else:
          trip=TripGemini(tankerno=tankerno,
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
                         remark=remark if remark else None
                         )
          trip.save()
          messages.success(request, 'Trip added successfully !!') 
    
    # Pass the values to the template
    context = {
        'tankerno': tankerno,
        'From_address': From_address,
        'To_address': To_address,
        'tanker_capacity': tanker_capacity,
        'drivername':drivername
    }
    return render(request, 'add/add_trip_gemini.html',context)

def Showgemini(request):
    gemeni=TripGemini.objects.all()
    context={'gemeni':gemeni}
    return render(request,'show/show_gemini.html',context)

def showtrip(request):
    show=AddTrips.objects.all()
    context={'show':show}
    return render(request,'show/show-trip.html',context)


def deltrip(request,id):
    deltrips=AddTrips.objects.get(pk=id)
    deltrips.delete()
    return redirect('showtrip')




def aaklocal(request):
    plan = plandetails.objects.earliest('tankerno')  
    if plan:
        tankerno = plan.tankerno
        drivername=plan.drivername
        From_address = plan.From_address
        To_address = plan.To_address
        tanker_capacity = plan.tanker_capacity
    else:
        tankerno = From_address = To_address = 'Data not available'
    
    if request.method =="POST":
       tankerno  = request.POST['tankerno']
       From_address = request.POST['From_address']
       To_address = request.POST['To_address']
    #    drivername = request.POST['drivername']
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
    #    percent = request.POST['percent']
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
       if  AakLocal.objects.filter(tankerno=tankerno, dispatch_time= dispatch_time).exists():
           messages.error(request, 'Trip already exists !!')
           return redirect('aak-local')
       else:
            trip=AakLocal(tankerno=tankerno,
                         From_address=From_address,
                         To_address=To_address,
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
    context = {
        'tankerno': tankerno,
        'From_address': From_address,
        'To_address': To_address,
        'tanker_capacity': tanker_capacity,
        'drivername':drivername}
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
      img = request.POST['img'] 
      
      if NewDriver_Details.objects.filter(adharnumber=adharnumber).exists():
         messages.error(request, 'Aadhar No already exists !!')
         return redirect('adddriver')
      else:
         deriver=NewDriver_Details(name=name,adharnumber=adharnumber,licencenumber=licencenumber,issuedates=issuedates,trdates=trdates,img=img)
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
    d= NewDriver_Details.objects.get(pk=id)
    d.delete()
    return redirect('showdrivers')






# TripExpense

def tripexpense(request):
    if request.method =="POST":
      tankerno = request.POST['tankerno']
      tripdate = request.POST['tripdate']
      tdate = request.POST['tdate']
      drivername = request.POST['drivername']
      fromconsignor = request.POST['fromconsignor']
      toconsignee = request.POST['toconsignee']
      trip_general_expenses = request.POST['trip_general_expenses']
      food_allowance = request.POST['food_allowance']
      bhatta =request.POST['bhatta']
      washing_charges_tank =request.POST['washing_charges_tank']
      total_amount = request.POST['total_amount']

      if TripExpense.objects.filter(tankerno=tankerno,tdate=tdate).exists():
          messages.error(request, 'Trip Expense already exists !!')
          return redirect('trip-expense')
      else:
         res=TripExpense(tankerno=tankerno,tripdate=tripdate,tdate=tdate,drivername=drivername,fromconsignor=fromconsignor,toconsignee=toconsignee,trip_general_d=trip_general_expenses,food_allowance=food_allowance,bhatta=bhatta,washing_charges_tank=washing_charges_tank,total_amount=total_amount)
         res.save()
         messages.success(request, 'Trip expense added successfully !!') 
      
    
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle':vehicle,'company':company,'dname':dname}
    return render(request,'add/add-trip-expense.html',context)





def  showtripexpense(request):
     expense=TripExpense.objects.all()
     context={'expense':expense}
     return render(request,'show-trip-expense.html',context)


def  addtolls(request):
    if request.method =="POST":
      tankerno  = request.POST['tankerno']
      driver_names  = request.POST['driver_names']
      trip_date = request.POST['trip_date']
      date = request.POST['date']
      amount = request.POST['amount']
      toll_name = request.POST['toll_name']
      From_address = request.POST['From_address']
      To_address = request.POST['To_address']
      
      if Toll_Details.objects.filter(tankerno=tankerno,date=date).exists():
         messages.error(request, 'already exists !!')
         return redirect('add-toll')
      else:
         toll=Toll_Details(tankerno=tankerno,driver_names=driver_names,trip_date=trip_date,amount=amount,toll_name=toll_name,From_address=From_address,To_address=To_address)
         toll.save()
         messages.success(request, 'Toll details added successfully !!') 
    vehicle=Add_Vehicle.objects.all()
    company=companydetails.objects.all()
    dname=NewDriver_Details.objects.all()
    context={'vehicle': vehicle,'company':company,'dname':dname}
 
    return render(request,'add/add-toll.html',context)


def  tolldetails(request):
     showtoll=Toll_Details.objects.all()
     context={'showtoll':showtoll}
     return render(request,'show/show-toll.html',context)


def  adddiesel(request):
    if request.method =="POST":
     tankerno_diesel  = request.POST['tankerno_diesel']
     tripdate_diesel  = request.POST['tripdate_diesel']
     date_diesel= request.POST['date_diesel']
     category = request.POST['category']
     subCategory = request.POST['subCategory']
     paid_to = request.POST['paid_to']
     given_amounts_diesel = request.POST['given_amounts_diesel']
     liters = request.POST['liters']
     rate = request.POST['rate']
     total_diesel= request.POST['total_diesel']
      
     if Diesel_detail.objects.filter(tankerno_diesel=tankerno_diesel,date_diesel=date_diesel).exists():
        messages.error(request, 'already exists !!')
        return redirect('add-toll')
     else:
        diesel=Diesel_detail(tankerno_diesel=tankerno_diesel,tripdate_diesel=tripdate_diesel,date_diesel=date_diesel,category=category,subCategory=subCategory,paid_to=paid_to,given_amounts_diesel=given_amounts_diesel,liters=liters,rate=rate,total_diesel=total_diesel)
        diesel.save()
        messages.success(request, 'Diesel details added successfully !!') 
    vehicle=Add_Vehicle.objects.all()
    categories = Category.objects.all()
    dname=NewDriver_Details.objects.all()
    petrol=AddPetrolPump.objects.all()
    context={'categories':categories,'dname':dname,'vehicle':vehicle,'petrol':petrol}
    return render(request,'diesel-details.html',context)


def dieseldetails(request):
    showdiesel=Diesel_detail.objects.all()
    context={'showdiesel':showdiesel}
    return render(request,'show/show-diesel-details.html',context)


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
    vehicle=Add_Vehicle.objects.all()   
    company=companydetails.objects.all()
    context={'vehicle':vehicle,'company':company}    
    return render(request,'driver-salary.html',context)

def  showsalary(request):
    show_s=Driver_salary.objects.all()
    context={'show_s':show_s}
    return render(request,'show/show_salary.html',context)

def  addurea(request):

    if request.method =="POST":
      urea_tanker_no = request.POST['urea_tanker_no']
      From_address = request.POST['From_address']
      To_address  = request.POST['To_address']
      paid_date = request.POST['paid_date']
      bill_date= request.POST['bill_date']
      trip_urea_date = request.POST['trip_urea_date'] 
      urea_liter = request.POST['urea_liter'] 
      urea_rate = request.POST['urea_rate'] 
      urea_total = request.POST['urea_total'] 
    
      if Add_Urea.objects.filter(urea_tanker_no=urea_tanker_no,paid_date=paid_date).exists():
        messages.error(request, 'Urea Details already exists !!')
        return redirect('add-urea')
      else:
        urea_details=Add_Urea(urea_tanker_no=urea_tanker_no,From_address=From_address,To_address=To_address,paid_date=paid_date,bill_date=bill_date,trip_urea_date=trip_urea_date,urea_liter=urea_liter,urea_rate=urea_rate,urea_total=urea_total)
        urea_details.save()
        messages.success(request, 'Urea details added successfully !!') 
    vehicle=Add_Vehicle.objects.all()   
    company=companydetails.objects.all()
    context={'vehicle':vehicle,'company':company}       
    return render(request,'add/add-urea.html',context)
   

def  showurea(request):
    showurea=Add_Urea.objects.all()
    context={'showurea':showurea}
    return render(request,'urea-details.html',context)


def  repairs(request):
    return render(request,'repairs.html')


def report(request):
    trips = Trip.objects.all()
    expenses = Expense.objects.all()
    total_expense_sum = trips.aggregate(Sum('total_expense'))['total_expense__sum']
    combined = zip(trips, expenses)
    context={'combined':combined,'grand_total': total_expense_sum or 0,}  

    return render(request, 'reports.html', context)





def vehicledetails(request):
    if request.method =="POST":
      vehicle_name = request.POST['vehicle_name']
      owner_name = request.POST['owner_name']
      making_year  = request.POST['making_year']
      chassise_no = request.POST['chassise_no']
      engine_no = request.POST['engine_no']
      insurance_date = request.POST['insurance_date'] 
      state_permit = request.POST['state_permit'] 
      national_permit = request.POST['national_permit'] 
      fitness_date = request.POST['fitness_date'] 
      tax_date = request.POST['tax_date'] 
      puc_date = request.POST['puc_date'] 
      vehicle_img = request.POST['vehicle_img'] 

      if Add_Vehicle.objects.filter(vehicle_name=vehicle_name).exists():
          messages.error(request, 'Vehicle No. already exists !!')
          return redirect('addvehicle')
      else:
           vehicle_details=Add_Vehicle(vehicle_name=vehicle_name,owner_name=owner_name,making_year=making_year,chassise_no=chassise_no,engine_no=engine_no,insurance_date=insurance_date,state_permit=state_permit,national_permit=national_permit,fitness_date=fitness_date,tax_date=tax_date,puc_date=puc_date,vehicle_img=vehicle_img)
           vehicle_details.save()
           messages.success(request, 'Vehicle details added successfully !!') 
    # dname=NewDriverDetails.objects.all()
    # context={'dname':dname}
    return render(request,'add/add-vehicle.html')


def show_vehicledetails(request):
    showvehicle=Add_Vehicle.objects.all()
    context={'showvehicle':showvehicle}
    return render(request,'show/show-vehicle-details.html',context)



def company_details(request):
    if request.method =="POST":
      name  = request.POST['name']
      area_name = request.POST['area_name']
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
          cname=companydetails(name=name,area_name=area_name,state=state,city=city,pincode=pincode,gst=gst,pan=pan,contact_no=contact_no)
          cname.save()
          messages.success(request, 'Company details added successfully !!') 
    
    return render(request,'add/add_company.html')


def show_company(request):
    cshow=companydetails.objects.all()
    context={'cshow':cshow}
    return render(request,'show/show_company.html',context)

def all_trip(request):
    if request.method == "POST":
        # Retrieve all data from the POST request
        trip_tanker = request.POST.get('trip_tanker')
        tripdate = request.POST.get('tripdate')
        tdate = request.POST.get('tdate')
        drivername = request.POST.get('drivername')
        From_address = request.POST.get('From_address')
        To_address = request.POST.get('To_address')
        trip_general_expenses = request.POST.get('trip_general_expenses')
        food_allowance = request.POST.get('food_allowance')
        bhatta = request.POST.get('bhatta')
        washing_charges_tank = request.POST.get('washing_charges_tank')
        total_amount = request.POST.get('total_amount')
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        toll_name = request.POST.get('toll_name')
        category = request.POST.get('category')
        subCategory = request.POST.get('subCategory')
        paid_to = request.POST.get('paid_to')
        given_amounts_diesel = request.POST.get('given_amounts_diesel')
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
        end_date = request.POST.get('end_date')

        # Ensure the 'tripdate' field is filled
        if not tripdate or not trip_tanker:
           messages.error(request, 'Please fill in the required fields!')
           return redirect('all-trip')
        
        else:
          # Create and save Trip_Expense instance
            e = Trip_Expense(
            trip_tanker=trip_tanker or None,
            tripdate=tripdate or None,
            tdate = tdate or None,
            drivername=drivername or None,
            From_address=From_address or None,
            To_address=To_address or None,
            trip_general_expenses=trip_general_expenses or None,
            food_allowance=food_allowance or None,
            bhatta=bhatta or None,
            washing_charges_tank=washing_charges_tank or None,
            total_amount=total_amount or None,
            date= date or None,
            amount=amount or None,
            toll_name=toll_name or None,
            category=category or None,
            subCategory=subCategory or None,
            paid_to=paid_to or None,
            given_amounts_diesel=given_amounts_diesel or None,
            liters=liters or None,
            rate=rate or None,
            total_diesel=total_diesel or None,
            paid_date=paid_date or None,
            bill_date=bill_date or None,
            urea_liter=urea_liter or None,
            urea_rate=urea_rate or None,
            urea_total=urea_total or None,
            r_paid_date=r_paid_date or None,
            r_bill_date=r_bill_date or None,
            spare_part=spare_part or None,
            r_amount=r_amount or None,
            part_name=part_name or None,
            no_piece=no_piece or None,
            end_date=end_date or None,
        )
        e.save()
        messages.success(request, 'Trip Expenses Added successfully!!')

    # Fetch data for rendering
    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    categories = Category.objects.all()
    dname = NewDriver_Details.objects.all()
    petrol = AddPetrolPump.objects.all()

    # Return the response
    context = {'categories': categories, 'dname': dname, 'vehicle': vehicle, 'petrol': petrol, 'company': company}
    return render(request, 'trip-expense-all.html', context)






def showallexpense(request):
    allExp=Trip_Expense.objects.all()
    # endTrip=EndTrip.objects.all()
    # Aggregate sums for each field
    all_sum = Trip_Expense.objects.aggregate(Sum('r_amount'))['r_amount__sum']
    u_sum = Trip_Expense.objects.aggregate(Sum('urea_total'))['urea_total__sum']
    d_sum = Trip_Expense.objects.aggregate(Sum('total_diesel'))['total_diesel__sum']
    t_sum = Trip_Expense.objects.aggregate(Sum('total_amount'))['total_amount__sum']
    a_sum = Trip_Expense.objects.aggregate(Sum('amount'))['amount__sum']
    
    # Calculate the total of all sums (if the sum is None, it defaults to 0)
    total_sum = (all_sum or 0) + (u_sum or 0) + (d_sum or 0) + (t_sum or 0) + (a_sum or 0)
    
    # Context to send to the template
    context = {
        'allExp': allExp,
        # 'endTrip':endTrip,
        'all_sum': all_sum,
        'u_sum': u_sum,
        'd_sum': d_sum,
        't_sum': t_sum,
        'a_sum': a_sum,
        'total_sum': total_sum  # total_sum includes the sum of all individual sums
    }
    return render(request,'show/show_all_expense.html',context)




def allexpensedelete(request,id):
    Exp_del=Trip_Expense.objects.get(pk=id)
    Exp_del.delete()
    return redirect('all-expense')




def addEndTrip(request):
    tripend =Trip_Expense.objects.all().last()  
    if tripend: 
        trip_tanker = tripend.trip_tanker
        tripdate = tripend.tripdate
        drivername=tripend.drivername
    else:
        trip_tanker = tripdate =  'Data not available'
    if request.method =="POST":
        tank_ends = request.POST['tank_ends']
        date = request.POST['date']
        driver = request.POST['driver']
        end_Date = request.POST['end_Date']
        
        if End_Trip.objects.filter(tank_ends=tank_ends,end_Date=end_Date).exists():
           messages.error(request, 'Trip End already!!')
           return redirect('add-trip-end')
        else:
           d_end=End_Trip(tank_ends=tank_ends,date=date,driver=driver,end_Date=end_Date)
           d_end.save()
           messages.success(request, 'Trip End successfully !!')

    context = {
        'trip_tanker': trip_tanker,
        'tripdate':  tripdate,
        'drivername':drivername
      
    }       
    return render(request, 'end-trip-date.html',context)
       
    


def showEndTrip(request):
    showend=End_Trip.objects.all()
    context={'showend':showend}
    return render(request,'show-trip-end.html',context)


def all_bill(request):

    return render(request,'all-bills.html')



def generate_bill_no():
    # Generate a simple bill number using the current year and a random number
    year = now().year
    random_number = random.randint(1000, 9999)
    bill_no = f"J.N/{random_number}/{year}"
    return bill_no

def aak_bill(request):
   
    if request.method == "POST":
        # Get the date for the invoice
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')
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

        # Initialize total amount as 0
        total_amount = 0.0
        
        # Get today's date, but exclude the year for the invoice number
        today = datetime.date.today()
        date_str = today.strftime('%m-%y')  # Format as 'MM-DD'

        # Generate the base invoice number (e.g., 'INV-03-25')
        invoice_prefix = f'{date_str}'

        # Generate a random 6-digit number (you can change the length or characters)
        # random_number = ''.join(random.choices(string.digits, k=4))
        # Assume a variable to store the last used number (this would be stored in DB)
        last_used_number = 1000  # You can get this from your database or other storage

        # Increment the counter for the new invoice
        random_number = last_used_number + 1
        last_used_number = random_number  # Save this updated value back to the database

         # Combine the invoice prefix with the new sequential number
        invoice_number = f'{str(random_number)}-{invoice_prefix}'

        # Ensure the invoice number is unique
        while Invoice.objects.filter(invoice_number=invoice_number).exists():
              random_number += 1
              invoice_number = f'J N-{str(random_number)}-{invoice_prefix}'


        # Create the invoice object
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company if company else None,
            gst=gst if gst else None,
            pan=pan if pan else None,
            tanker=tanker if tanker else None,
            tanker_cap=tanker_cap if tanker_cap else None,
            From_add=From_add if  From_add else None,
            To_add=To_add if  To_add else None,
            date_dis=date_dis if  date_dis else None,
            unload=unload if  unload else None,
            short=short if  short else None,
            retn=retn if  retn else None,
            lr_no=lr_no if lr_no else None,
            Fo_date=Fo_date if Fo_date else None,
            To_date=To_date if To_date else None,
            d_rate=d_rate if d_rate else None,
            par_day=par_day if par_day else None,
            total_d=total_d if total_d else None,
            total_amount=total_amount  # This will be updated later
        )

        # Process the items
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # Loop through items and add them to the invoice
        for i in range(len(item_data)):
            quantity = int(quantities[i])
            unit_price = float(unit_prices[i])

            # Calculate the total amount for this item and add it to the invoice
            total_item_cost = quantity * unit_price
            # Define GST rates for SGST and CGST (6% each)
            sgst_rate = 0.06  # 6% SGST
            cgst_rate = 0.06  # 6% CGST
            # Calculate SGST and CGST
            sgst = total_item_cost * sgst_rate
            cgst = total_item_cost * cgst_rate
            # total_amount += int(total_item_cost) + int(total_d)
            total_amount += int(total_item_cost) + int(total_d) + float(sgst) + float(cgst)
            
            
            # Create Item instance and associate it with the invoice
            Item.objects.create(
                invoice=invoice,
                description=item_data[i],
                quantity=quantity,
                unit_price=unit_price
            )
        
        # After processing items, update the invoice's total amount
        invoice.total_amount = total_amount

        # Convert the total amount into words
        total_in_words = num2words(total_amount).title()

        # Save the invoice's total amount in words as well, if needed
        invoice.total_in_words = total_in_words
        invoice.save()

        # Redirect to the invoice detail page
        return redirect('invoice_detail', invoice_id=invoice.id)
    company=companydetails.objects.all()
    context={'company':company}

    return render(request,'bills/aak-india-pvt.html',context)

def Aak_bills(request):
    # bill =.objects.latest('bill_no')
    bill = AAkIndia.objects.filter().last()
    total_sum = bill.total or 0
    total_d_sum = bill.total_d or 0
# Sum of both totals
    total_sum = total_sum + total_d_sum
    total_in_words = num2words(total_sum)
    context = {'bill': bill, 'total_sum': total_sum,'total_in_words': total_in_words}
    return render(request,'bills/akk_india_bill.html',context)
# def generate_bill_no():
#     # Generate a simple bill number using the current year and a random number
#     year = now().year
#     random_number = random.randint(1000, 9999)
#     bill_no = f"J.N/{random_number}/{year}"
#     return bill_no


def gemini_bill(request):
    if request.method == "POST":
        # Get the date for the invoice
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')
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

        # Initialize total amount as 0
        total_amount = 0.0
        
        # Get today's date, but exclude the year for the invoice number
        today = datetime.date.today()
        date_str = today.strftime('%m-%y')  # Format as 'MM-DD'

        # Generate the base invoice number (e.g., 'INV-03-25')
        invoice_prefix = f'{date_str}'

        # Generate a random 6-digit number (you can change the length or characters)
        # random_number = ''.join(random.choices(string.digits, k=4))
        # Assume a variable to store the last used number (this would be stored in DB)
        last_used_number = 1000  # You can get this from your database or other storage

        # Increment the counter for the new invoice
        random_number = last_used_number + 1
        last_used_number = random_number  # Save this updated value back to the database

         # Combine the invoice prefix with the new sequential number
        invoice_number = f'{str(random_number)}-{invoice_prefix}'

        # Ensure the invoice number is unique
        while Invoice.objects.filter(invoice_number=invoice_number).exists():
              random_number += 1
              invoice_number = f'J N-{str(random_number)}-{invoice_prefix}'


        # Create the invoice object
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company if company else None,
            gst=gst if gst else None,
            pan=pan if pan else None,
            tanker=tanker if tanker else None,
            tanker_cap=tanker_cap if tanker_cap else None,
            From_add=From_add if  From_add else None,
            To_add=To_add if  To_add else None,
            date_dis=date_dis if  date_dis else None,
            unload=unload if  unload else None,
            short=short if  short else None,
            retn=retn if  retn else None,
            lr_no=lr_no if lr_no else None,
            Fo_date=Fo_date if  Fo_date else None,
            To_date=To_date if  To_date else None,
            d_rate=d_rate if  d_rate else None,
            par_day=par_day if  par_day else None,
            total_d=total_d if  total_d else None,
            total_amount=total_amount  # This will be updated later
        )

        # Process the items
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # Loop through items and add them to the invoice
        for i in range(len(item_data)):
            quantity = int(quantities[i])
            unit_price = float(unit_prices[i])

            # Calculate the total amount for this item and add it to the invoice
            total_item_cost = quantity * unit_price
            # Define GST rates for SGST and CGST (6% each)
            sgst_rate = 0.06  # 6% SGST
            cgst_rate = 0.06  # 6% CGST
            # Calculate SGST and CGST
            sgst = total_item_cost * sgst_rate
            cgst = total_item_cost * cgst_rate
            # total_amount += int(total_item_cost) + int(total_d)
            total_amount += int(total_item_cost) + int(total_d) + float(sgst) + float(cgst)
            
            
            # Create Item instance and associate it with the invoice
            Item.objects.create(
                invoice=invoice,
                description=item_data[i],
                quantity=quantity,
                unit_price=unit_price
            )
        
        # After processing items, update the invoice's total amount
        invoice.total_amount = total_amount

        # Convert the total amount into words
        total_in_words = num2words(total_amount).title()

        # Save the invoice's total amount in words as well, if needed
        invoice.total_in_words = total_in_words
        invoice.save()

        # Redirect to the invoice detail page
        return redirect('invoice_detail', invoice_id=invoice.id)
    company=companydetails.objects.all()
    context={'company':company}
    return render(request, 'bills/gemini-bill.html', context)




def  geminidetails(request):
     show=Gemini.objects.all()
     context={'show':show}
     return render(request,'bills/show-gemini-bill.html',context)



def bills(request):
    # bill = Gemini.objects.latest('bill_no')
    bill = Gemini.objects.filter().last()
    total_kg_sum = bill.total_kg or 0
    union_charge_sum = bill.union_charge or 0
# Sum of both totals
    total_sum = total_kg_sum + union_charge_sum
    total_in_words = num2words(total_sum)
    context = {'bill': bill, 'total_sum': total_sum,'total_in_words': total_in_words}
    return render(request,'bills/bill.html',context)




def start_trip(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        tanker = request.POST.get('tanker')
        trip_date = request.POST.get('trip_date')
        from_id = request.POST.get('from_id')
        To_id = request.POST.get('To_id')
        
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
                To_id=To_id
            )
            # After creating the trip, redirect to the 'add_expense' page for the newly created trip
            return redirect('add_expense', trip_id=trip.trip_id)
    
    # For a GET request, or after the POST is processed, get the necessary context data
    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    context = {'vehicle': vehicle, 'company': company}
    
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
         
    # Fetch the existing Expense details to update  
    upexpense=Expense.objects.get(pk=id)

    upexpense.trip_general_expenses = trip_general_expenses
    upexpense.food_allowance = food_allowance
    upexpense.bhatta = bhatta
    upexpense.washing_charges_tank = washing_charges_tank
    upexpense.actual_amount= actual_amount
    upexpense.total_amount= total_amount
    upexpense.toll_name= toll_name
    upexpense.toll_amount= toll_amount
    upexpense.category= category
    upexpense.subCategory= subCategory
    upexpense.paid_to= paid_to
    upexpense.amount_given= amount_given
    upexpense.liters= liters
    upexpense.rate= rate
    upexpense.total_diesel= total_diesel
    upexpense.paid_date= paid_date
    upexpense.bill_date= bill_date
    upexpense.urea_liter= urea_liter
    upexpense.urea_rate= urea_rate
    upexpense.urea_total= urea_total
    upexpense.r_paid_date= r_paid_date
    upexpense.r_bill_date= r_bill_date
    upexpense.spare_part= spare_part
    upexpense.r_amount= r_amount
    upexpense.part_name= part_name
    upexpense.no_piece = no_piece 
    upexpense.date = date
    
    upexpense.save()
    messages.success(request, 'Expense Update successfully !!')
    return redirect('start_trip')



def delete_expense(request,id):
    de=Expense.objects.get(pk=id)
    de.delete()
    return redirect('start_trip')



def end_trip(request, trip_id):
    if request.method == 'POST':
        end_time = request.POST.get('end_time')
    # Get the trip object based on trip_id, handle the case of multiple trips
    trips = Trip.objects.filter(trip_id=trip_id)

    if trips.count() == 1:
        trip = trips.first()  # If exactly one trip is found
    elif trips.count() > 1:
        trip = trips.first()  # If multiple trips, select the first one (you can handle it as needed)
    else:
        return render(request, '404.html')  # If no trip found, return 404 or an appropriate response
    
    # Mark the trip as ended
    trip.end_time = timezone.now()  # Set the end time
    trip.is_active = False  # Set is_active to False
    trip.calculate_total_expense()  # Recalculate the total expenses for the trip
    trip.save()

    # Redirect to a page showing the details of the ended trip
    return render(request, 'exp/end_trip.html', {'trip': trip})


def AllTrip(request):
    # Fetch all trip records from the database
    t = Trip.objects.all()

    # Fetch all expense records from the database
    expense = Expense.objects.all()

    # Pass the trip and expense data to the template
    context = {'t': t, 'expense': expense}

    # Render the 'all_trip.html' template with the context data
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
            return redirect('dashboard')  # Redirect to the dashboard page
        else:
            messages.error(request, ' Name and Password is incorrect !!')
            return redirect('log-in') 
    
    return render(request, 'form/login.html')





def Logout_user(request):
    logout(request)
    return redirect('log-in')




def generate_bill_no():
    # Generate a simple bill number using the current year and a random number
    year = now().year
    random_number = random.randint(1000, 9999)
    bill_no = f"J.N/{random_number}/{year}"
    return bill_no


def ashland(request):

    if request.method == "POST":
        # Use .get() to avoid KeyError when fields are missing
        bill_no = request.POST.get('bill_no')
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        kg = request.POST.get('kg')
        rate = request.POST.get('rate')
        total_kg = request.POST.get('total_kg')
        lr_no = request.POST.get('lr_no')
        Fo_date = request.POST.get('Fo_date')
        To_date = request.POST.get('To_date')
        d_rate = request.POST.get('d_rate')
        par_day = request.POST.get('par_day')
        total_d = request.POST.get('total_d')
        tank_c = request.POST.get('tank_c')
        tanker_cap = request.POST.get('tanker_cap')
        
        # If no bill_no is provided, auto-generate one
        if not bill_no:
            bill_no = generate_bill_no()

        # Checking if required fields are not empty
        if not tanker:
           messages.error(request, 'Please fill in the required fields!')
           return redirect('ash-bills')
        else:
            # Create the Gemini instance, only filling non-empty fields
            a = Ashland(
                bill_no=bill_no if bill_no else None,  
                date=date if date else None,  
                company=company if company else None,
                gst=gst if gst else None,
                pan=pan if pan else None,  
                tanker=tanker if tanker else None, 
                From_add=From_add if From_add else None,  
                To_add=To_add if To_add else None,  
                date_dis=date_dis if date_dis else None,  
                tanker_cap=tanker_cap if tanker_cap else None,  
                kg=kg if kg else None,  
                rate=rate if rate else None,  
                total_kg=total_kg if total_kg else None,  
                lr_no=lr_no if lr_no else None,  
                Fo_date=Fo_date if Fo_date else None,  
                To_date=To_date if To_date else None,  
                d_rate=d_rate if d_rate else None, 
                par_day=par_day if par_day else None,  
                total_d=total_d if total_d else None, 
                tank_c=tank_c if tank_c else None, 
            )
            a.save()
            messages.success(request, 'Bill added successfully!')

  
    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    context = {'vehicle': vehicle, 'company': company}
    return render(request,'bills/ashland_india_pvt.html',context)


def Showashland(request):
    show=Ashland.objects.all()
    context={'show':show}
    return render(request,'bills/show_ashland_pvt.html',context)

def Ash_bills(request):
    # bill =.objects.latest('bill_no')
    bill =Ashland.objects.filter().last()
    total_kg_sum = bill.total_kg or 0
    total_d_sum = bill.total_d or 0
    tank_c_sum = bill.tank_c or 0
# Sum of both totals
    total_sum = total_kg_sum + total_d_sum + tank_c_sum 
    total_in_words = num2words(total_sum)
    context = {'bill': bill, 'total_sum': total_sum,'total_in_words': total_in_words}
    return render(request,'bills/ashland_bill.html',context)

def  Cargill(request):
    
    return render(request,'bills/cargill_india.html')


def  Harkaran(request):
    if request.method == "POST":
        # Use .get() to avoid KeyError when fields are missing
        bill = request.POST.get('bill')
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')
        pan = request.POST.get('pan')
        tanker = request.POST.get('tanker')
        From_add = request.POST.get('From_add')
        To_add = request.POST.get('To_add')
        date_dis = request.POST.get('date_dis')
        kg = request.POST.get('kg')
        rate = request.POST.get('rate')
        total_kg = request.POST.get('total_kg')
        lr_no = request.POST.get('lr_no')
        # union_charge = request.POST.get('union_charge')
        
        #   # If no bill_no is provided, auto-generate one
        if not bill:
            bill = generate_bill_no()

        # Checking if required fields are not empty
        if not tanker or not From_add or not To_add or not date_dis or not kg or not rate:
           messages.error(request, 'Please fill in the required fields!')
           return redirect('harkaran')
        else:
            # Create the Gemini instance, only filling non-empty fields
            h = harkaran(
                bill=bill if bill else None,  
                date=date if date else None,  
                company=company if company else None,
                gst=gst if gst else None,
                pan=pan if pan else None,  
                tanker=tanker if tanker else None, 
                From_add=From_add if From_add else None,  
                To_add=To_add if To_add else None,  
                date_dis=date_dis if date_dis else None,  
                kg=kg if kg else None,  
                rate=rate if rate else None,  
                total_kg=total_kg if total_kg else None,  
                lr_no=lr_no if lr_no else None,  
                
            )
            h.save()
            messages.success(request, 'Bill added successfully!')

  
    vehicle = Add_Vehicle.objects.all()
    company = companydetails.objects.all()
    # bill=Gemini.objects.filter().first()
    context = {'vehicle': vehicle, 'company': company}
    return render(request,'bills/Harkaran_dass_ved.html',context)



def create_bill(request):
    if request.method == 'POST':
        # Get the static fields from the POST request
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')
        pan = request.POST.get('pan')

        # Save the Bill object
        bill = Bill.objects.create(
            date=date,
            company=company,
            gst=gst,
            pan=pan
        )

        # Loop through dynamic rows (if any) and save them
        # Assuming each dynamic row has the same naming convention
        tanker_data = []
        for i in range(len(request.POST.getlist('tanker'))):
            tanker = request.POST.getlist('tanker')[i]
            from_address = request.POST.getlist('From_add')[i]
            to_address = request.POST.getlist('To_add')[i]
            dispatch_date = request.POST.getlist('date_dis')[i]
            tanker_capacity = request.POST.getlist('tanker_cap')[i]
            lr_num = request.POST.getlist('lr_num')[i]
            loaded_qty = request.POST.getlist('kg')[i]
            rate_per_kg = request.POST.getlist('rate')[i]
            total_amount = request.POST.getlist('total_kg')[i]

            # Save each dynamic row as TankerDetail
            TankerDetail.objects.create(
                bill=bill,
                tanker=tanker,
                from_address=from_address,
                to_address=to_address,
                dispatch_date=dispatch_date,
                tanker_capacity=tanker_capacity,
                lr_num=lr_num,
                loaded_qty=loaded_qty,
                rate_per_kg=rate_per_kg,
                total_amount=total_amount
            )

        # Save other details such as detention charges
        detention_from_date = request.POST.get('Fo_date')
        detention_to_date = request.POST.get('To_date')
        detention_rate = request.POST.get('d_rate')
        detention_per_day = request.POST.get('par_day')
        total_detention = request.POST.get('total_d')
        tanker_washing_charges = request.POST.get('tank_c')

        # You can save detention charges or tanker washing charges in a similar way

        # After saving, show a success message
        messages.success(request, 'Bill created successfully!')
        return redirect('cargill')

    return render(request, 'bills/cargill.html')


def  VVF(request):
    
    return render(request,'bills/vvf_india.html')

def  Anjani(request):
    
    return render(request,'bills/anjani_agro.html')





#=================Bills ============
def invoice_detail(request, invoice_id):
    # Invoice ko fetch karein
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Invoice ki items ko fetch karein
    items = invoice.items.all()
    # Invoice aur items ko template mein bhejein
    return render(request, 'invoice_detail.html', {'invoice': invoice, 'items': items})






def create_invoice(request):
    if request.method == "POST":
        # Get the date for the invoice
        date = request.POST.get('date')
        company = request.POST.get('company')
        gst = request.POST.get('gst')
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

        # Initialize total amount as 0
        total_amount = 0.0
        
        # Get today's date, but exclude the year for the invoice number
        today = datetime.date.today()
        date_str = today.strftime('%m-%y')  # Format as 'MM-DD'

        # Generate the base invoice number (e.g., 'INV-03-25')
        invoice_prefix = f'{date_str}'

        # Generate a random 6-digit number (you can change the length or characters)
        # random_number = ''.join(random.choices(string.digits, k=4))
        # Assume a variable to store the last used number (this would be stored in DB)
        last_used_number = 1000  # You can get this from your database or other storage

        # Increment the counter for the new invoice
        random_number = last_used_number + 1
        last_used_number = random_number  # Save this updated value back to the database

         # Combine the invoice prefix with the new sequential number
        invoice_number = f'{str(random_number)}-{invoice_prefix}'

        # Ensure the invoice number is unique
        while Invoice.objects.filter(invoice_number=invoice_number).exists():
              random_number += 1
              invoice_number = f'J N-{str(random_number)}-{invoice_prefix}'


        # Create the invoice object
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            date=date,
            company=company if company else None,
            gst=gst if gst else None,
            pan=pan if pan else None,
            tanker=tanker if tanker else None,
            tanker_cap=tanker_cap if tanker_cap else None,
            From_add=From_add if  From_add else None,
            To_add=To_add if  To_add else None,
            date_dis=date_dis if  date_dis else None,
            unload=unload if  unload else None,
            short=short if  short else None,
            retn=retn if  retn else None,
            lr_no=lr_no if lr_no else None,
            Fo_date=Fo_date if  Fo_date else None,
            To_date=To_date if  To_date else None,
            d_rate=d_rate if  d_rate else None,
            par_day=par_day if  par_day else None,
            total_d=total_d if  total_d else None,
            total_amount=total_amount  # This will be updated later
        )

        # Process the items
        item_data = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        unit_prices = request.POST.getlist('item_unit_price')

        # Loop through items and add them to the invoice
        for i in range(len(item_data)):
            quantity = int(quantities[i])
            unit_price = float(unit_prices[i])

            # Calculate the total amount for this item and add it to the invoice
            total_item_cost = quantity * unit_price
            # Define GST rates for SGST and CGST (6% each)
            sgst_rate = 0.06  # 6% SGST
            cgst_rate = 0.06  # 6% CGST
            # Calculate SGST and CGST
            sgst = total_item_cost * sgst_rate
            cgst = total_item_cost * cgst_rate
            # total_amount += int(total_item_cost) + int(total_d)
            total_amount += int(total_item_cost) + int(total_d) + float(sgst) + float(cgst)
            
            
            # Create Item instance and associate it with the invoice
            Item.objects.create(
                invoice=invoice,
                description=item_data[i],
                quantity=quantity,
                unit_price=unit_price
            )
        
        # After processing items, update the invoice's total amount
        invoice.total_amount = total_amount

        # Convert the total amount into words
        total_in_words = num2words(total_amount).title()

        # Save the invoice's total amount in words as well, if needed
        invoice.total_in_words = total_in_words
        invoice.save()

        # Redirect to the invoice detail page
        return redirect('invoice_detail', invoice_id=invoice.id)
    company=companydetails.objects.all()
    context={'company':company}
    return render(request, 'create_invoice.html',context)






# ---------------------Loan-----------------------#
def addloan(request):
    if request.method == "POST":
        name = request.POST.get('name')  # Use .get() to avoid KeyError
        if name:
            bankname = AddBank_Loan.objects.create(name=name)
            bankname.save()
        else:
            # Handle missing name field, e.g., add a message or log the error
            pass

    # Fetch all banks regardless of POST or GET request
    bank = AddBank_Loan.objects.all()

    context = {'bank': bank}

    return render(request, 'loan-details.html', context)







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