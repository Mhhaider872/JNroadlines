from django.db import models

# Create your models here.


    

class TankerCapacity(models.Model):
    name=models.CharField(max_length=200)


    

class companydetails(models.Model):
     name=models.CharField(max_length=200)
     area_name=models.CharField(max_length=200,blank=True,null=True)
     short_name=models.CharField(max_length=200,blank=True,null=True)
     city=models.CharField(max_length=200,blank=True,null=True)
     state=models.CharField(max_length=200,blank=True,null=True)
     pincode=models.IntegerField(blank=True,null=True)
     gst=models.CharField(max_length=200,blank=True,null=True)
     pan=models.CharField(max_length=200,blank=True,null=True)
     
     contact_no=models.IntegerField(blank=True,null=True)


     def __str__(self):
        return self.name
    

class NewDriver_Details(models.Model):
    name=models.CharField(max_length=200, null=True)
    adharnumber=models.BigIntegerField(null=False, blank=False)
    licencenumber=models.CharField(max_length=20, null=False,blank=False)
    issuedates=models.DateField(null=False, blank=False)
    trdates=models.DateField(null=False, blank=False)
    # imguploads=models.FileField(upload_to='img/')
    # imguploads= models.FileField(upload_to='pdfs/')
    img= models.FileField(upload_to='img/',null=True)
    is_deleted = models.BooleanField(default=False)
    fname=models.CharField(max_length=200, null=True, blank=True)
   
   
    def __str__(self):
        return self.name

class plandetails(models.Model):
  
    tankerno = models.CharField(max_length=200)
    drivername=models.CharField(max_length=200, null=True)
    # driver = models.ForeignKey(NewDriver_Details, on_delete=models.CASCADE, null=True)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    tanker_capacity=models.CharField(max_length=200)
    dispatch_Date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=100)


    def save(self, *args, **kwargs):
        self.From_address = self.From_address.title()
        self.To_address = self.To_address.title()
        super().save(*args, **kwargs)



class AddTrips(models.Model):
    plan = models.ForeignKey(plandetails, on_delete=models.CASCADE, null=True)
    tankerno=models.CharField(max_length=100, null=True)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    drivername=models.CharField(max_length=100)
    tank_capacity=models.CharField(max_length=100)
    arrival_time=models.DateTimeField(null=True, blank=True)
    dispatch_time=models.DateTimeField(null=True, blank=True)
    reach_time=models.DateTimeField(null=True, blank=True)
    unload_time=models.DateTimeField(null=True, blank=True)
    lr_num=models.CharField(max_length=200, null=True, blank=True)
    lr_date=models.DateField(null=True, blank=True)
    freight_bill=models.CharField(max_length=200, null=True, blank=True)
    freight_date=models.DateField(null=True, blank=True)
    loaded_qty=models.IntegerField(null=True, blank=True)
    unload_qty=models.IntegerField(null=True, blank=True)
    percent=models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    short_qty=models.IntegerField(null=True, blank=True)
    short_allow=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    return_qty=models.IntegerField(null=True, blank=True)
    remark=models.CharField(max_length=200, null=True, blank=True)


class AakLocal(models.Model):
    plan = models.ForeignKey(plandetails, on_delete=models.CASCADE, null=True)
    tankerno=models.CharField(max_length=100)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    drivername=models.CharField(max_length=100, null=True, blank=True)
    tank_capacity=models.CharField(max_length=100)
    arrival_time=models.DateTimeField(null=True, blank=True)
    dispatch_time=models.DateTimeField(null=True, blank=True)
    reach_time=models.DateTimeField(null=True, blank=True)
    # unload_time=models.DateTimeField(null=True, blank=True)
    lr_num=models.CharField(max_length=200, null=True, blank=True)
    lr_date=models.DateField(null=True, blank=True)
    freight_bill=models.CharField(max_length=200, null=True, blank=True)
    freight_date=models.DateField(null=True, blank=True)
    loaded_qty=models.IntegerField(null=True, blank=True)
    unload_qty=models.IntegerField(null=True, blank=True)
    percent=models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    short_qty=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_allow=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    return_qty=models.IntegerField(null=True, blank=True)
    remark=models.CharField(max_length=200, null=True, blank=True)
    time_Loading=models.IntegerField(null=True, blank=True)
    time_Loading_mama=models.IntegerField(null=True, blank=True)
    unloading_ganesh=models.IntegerField(null=True, blank=True)
    unloading_mama=models.IntegerField(null=True, blank=True)
    returned=models.DateTimeField(null=True, blank=True)
    trip_ganesh=models.IntegerField(null=True, blank=True)
    trip_mama=models.IntegerField(null=True, blank=True)



class TripGemini(models.Model):
    plan = models.ForeignKey(plandetails, on_delete=models.CASCADE, null=True)
    tankerno=models.CharField(max_length=100)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    drivername=models.CharField(max_length=100)
    tank_capacity=models.CharField(max_length=100)
    arrival_time=models.DateTimeField(null=True, blank=True)
    dispatch_time=models.DateTimeField(null=True, blank=True)
    reach_time=models.DateTimeField(null=True, blank=True)
    unload_time=models.DateTimeField(null=True, blank=True)
    lr_num=models.CharField(max_length=200, null=True, blank=True)
    lr_date=models.DateField(null=True, blank=True)
    freight_bill=models.CharField(max_length=200, null=True, blank=True)
    freight_date=models.DateField(null=True, blank=True)
    loaded_qty=models.IntegerField(null=True, blank=True)
    unload_qty=models.IntegerField(null=True, blank=True)
    short_qty=models.IntegerField(null=True, blank=True)
    short_allow=models.IntegerField(null=True, blank=True)
    return_qty=models.IntegerField(null=True, blank=True)
    remark=models.CharField(max_length=200)
    

class TripAdani(models.Model):
    plan = models.ForeignKey(plandetails, on_delete=models.CASCADE, null=True)
    tankerno=models.CharField(max_length=100)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    drivername=models.CharField(max_length=100)
    tank_capacity=models.CharField(max_length=100)
    arrival_time=models.DateTimeField(null=True, blank=True)
    dispatch_time=models.DateTimeField(null=True, blank=True)
    reach_time=models.DateTimeField(null=True, blank=True)
    unload_time=models.DateTimeField(null=True, blank=True)
    lr_num=models.CharField(max_length=200, null=True, blank=True)
    lr_date=models.DateField(null=True, blank=True)
    freight_bill=models.CharField(max_length=200, null=True, blank=True)
    freight_date=models.DateField(null=True, blank=True)
    loaded_qty=models.IntegerField(null=True, blank=True)
    unload_qty=models.IntegerField(null=True, blank=True)
    short_qty=models.IntegerField(null=True, blank=True)
    short_allow=models.IntegerField(null=True, blank=True)
    return_qty=models.IntegerField(null=True, blank=True)
    remark=models.CharField(max_length=200, null=True, blank=True)



    


class TripExpense(models.Model):
    tankerno=models.CharField(max_length=100)
    tripdate=models.DateField(null=True, blank=False)
    tdate=models.DateField(null=True, blank=False)
    drivername=models.CharField(max_length=100)
    fromconsignor=models.CharField(max_length=200)
    toconsignee=models.CharField(max_length=200)
    trip_general_expenses=models.IntegerField(null=True)
    food_allowance=models.IntegerField()
    bhatta=models.IntegerField()
    washing_charges_tank=models.IntegerField()
    total_amount=models.IntegerField(null=False)
    
    def __str__(self):
        return self.tankerno
    


    



class Driver_salary(models.Model):
    
     tankerno=models.CharField(max_length=100)
     salary_driver=models.CharField(max_length=100)
     f_date =models.DateField(null=True, blank=True)
     t_date =models.DateField(null=True, blank=True)
     p_date =models.DateField(null=True, blank=True)
     drivername=models.CharField(max_length=100)
     amount = models.DecimalField(max_digits=10, decimal_places=2)
   
   
     def __str__(self):
        return self.drivername













    


class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to category
    name = models.CharField(max_length=100)  # Name of the subcategory

    def __str__(self):
        return self.name
    



class Toll_Details(models.Model):
    tankerno=models.CharField(max_length=200)
    driver_names=models.CharField(max_length=200)
    trip_date = models.DateField(null=True, blank=False)
    date = models.DateField(null=True, blank=False,)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=200)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)




class Diesel_detail(models.Model):
    tankerno_diesel=models.CharField(max_length=200)
    tripdate_diesel=models.DateField(null=True,blank=False)
    date_diesel=models.DateField(null=True,blank=False)
    category=models.CharField(max_length=200)
    subCategory=models.CharField(max_length=200)
    paid_to=models.CharField(max_length=200)
    given_amounts_diesel=models.DecimalField(max_digits=10, decimal_places=2)
    liters=models.IntegerField()
    rate=models.DecimalField(max_digits=10, decimal_places=2)
    total_diesel=models.DecimalField(max_digits=10, decimal_places=2)





class Add_Vehicle(models.Model):
    vehicle_name=models.CharField(max_length=200)
    tankercap=models.CharField(max_length=200, null=True, blank=True)
    owner_name=models.CharField(max_length=200)
    making_year = models.DateField(null=True, blank=False)
    chassise_no = models.CharField(max_length=200, null=True, blank=False)
    engine_no = models.CharField(max_length=200, null=True, blank=False)
    insurance_date = models.DateField(null=True, blank=False)
    insurance_img= models.FileField(upload_to='insurance/',null=True)
    state_permit = models.DateField(null=True, blank=False)
    state_img= models.FileField(upload_to='state/',null=True)
    national_permit = models.DateField(null=True, blank=False)
    national_img= models.FileField(upload_to='national/',null=True)
    fitness_date = models.DateField(null=True, blank=False)
    fitness_img= models.FileField(upload_to='fitness/',null=True)
    tax_date = models.DateField(null=True, blank=False)
    tax_img= models.FileField(upload_to='tax/',null=True)
    puc_date = models.DateField(null=True, blank=False)
    puc_img= models.FileField(upload_to='puc/',null=True)
    # vehicle_img=models.FileField(upload_to='vehicle_image/')
    status=models.CharField(max_length=200, null=True, blank=True)




class Add_Urea(models.Model):
    urea_tanker_no=models.CharField(max_length=200)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    paid_date= models.DateField(null=True, blank=False)
    bill_date= models.DateField(null=True, blank=False)
    trip_urea_date= models.DateField(null=True, blank=False)
    urea_liter=models.IntegerField()
    urea_rate=models.DecimalField(max_digits=10, decimal_places=4)
    urea_total=models.DecimalField(max_digits=10, decimal_places=4)






class AddPetrolPump(models.Model):
    name=models.CharField(max_length=200)













class Trip_Expense(models.Model):
    trip_tanker=models.CharField(max_length=100, null=True, blank=True)
    tripdate=models.DateField(null=True,blank=True)
    tdate=models.DateField(null=True,blank=True)
    drivername=models.CharField(max_length=100, null=True, blank=True)
    From_address=models.CharField(max_length=200, null=True, blank=True)
    To_address=models.CharField(max_length=200, null=True, blank=True)
    trip_general_expenses=models.IntegerField(null=True, blank=True)
    food_allowance=models.IntegerField(null=True, blank=True)
    bhatta=models.IntegerField(null=True, blank=True)
    washing_charges_tank=models.IntegerField(null=True, blank=True)
    total_amount=models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    amount=models.IntegerField(null=True, blank=True)
    toll_name=models.CharField(max_length=200,null=True, blank=True)
    category=models.CharField(max_length=200, null=True, blank=True)
    subCategory=models.CharField(max_length=200, null=True, blank=True)
    # paid_by=models.CharField(max_length=200)
    paid_to=models.CharField(max_length=200 ,null=True, blank=True)
    given_amounts_diesel=models.IntegerField(null=True, blank=True)
    liters=models.IntegerField(null=True, blank=True)
    rate=models.IntegerField(null=True, blank=True)
    total_diesel=models.IntegerField(null=True, blank=True)
    paid_date= models.DateField(null=True,blank=True)
    bill_date= models.DateField(null=True,blank=True)
    # trip_urea_date= models.DateField(null=True, blank=False)
    urea_liter=models.IntegerField(null=True, blank=True)
    urea_rate=models.IntegerField(null=True, blank=True)
    urea_total=models.IntegerField(null=True, blank=True)
    r_paid_date= models.DateField(null=True,blank=True)
    r_bill_date= models.DateField(null=True,blank=True)
    spare_part=models.IntegerField(null=True, blank=True)
    r_amount=models.IntegerField(null=True, blank=True)
    part_name=models.CharField(max_length=200, null=True, blank=True)
    no_piece = models.IntegerField(null=True, blank=True)
    end_date = models.DateField(null=True,blank=True)












class End_Trip(models.Model):
    tank_ends=models.CharField(max_length=200,null=True)
    driver=models.CharField(max_length=200,null=True)
    date=models.DateField(null=False, blank=False)
    end_Date = models.DateField(null=True, blank=False)




class Gemini(models.Model):
     bill_no=models.CharField(max_length=100, unique=True)
     date=models.DateField(null=True, blank=True)
     company=models.CharField(max_length=300, null=True, blank=True)
     gst=models.CharField(max_length=300, null=True, blank=True)
     pan=models.CharField(max_length=300, null=True, blank=True)
     tanker=models.CharField(max_length=200,null=True)
     From_add=models.CharField(max_length=200,null=True)
     To_add=models.CharField(max_length=200,null=True)
     date_dis=models.DateField(null=True, blank=True)
     bill_no=models.IntegerField(null=True, blank=True)
     kg=models.DecimalField(max_digits=10, decimal_places=2)
     rate=models.DecimalField(max_digits=10, decimal_places=2)
     total_kg=models.DecimalField(max_digits=10, decimal_places=2)
     lr_no=models.IntegerField(null=True, blank=True)
     union_charge=models.IntegerField(null=True, blank=True)
     




class AAkIndia(models.Model):
     bill_no=models.CharField(max_length=100, null=True, blank=True, unique=True)
     date=models.DateField(null=True, blank=True)
     company=models.CharField(max_length=300, null=True, blank=True)
     gst=models.CharField(max_length=300, null=True, blank=True)
     pan=models.CharField(max_length=300, null=True, blank=True)
     tanker=models.CharField(max_length=200, null=True, blank=True)
     tanker_cap=models.CharField(max_length=200, null=True, blank=True)
     From_add=models.CharField(max_length=200, null=True, blank=True)
     To_add=models.CharField(max_length=200,null=True, blank=True)
     date_dis=models.DateField(null=True, blank=True)
     load=models.IntegerField(null=True, blank=True)
     rate_kg=models.IntegerField(null=True, blank=True)
     unload=models.IntegerField(null=True, blank=True)
     short=models.IntegerField(null=True, blank=True)
     retn=models.IntegerField(null=True, blank=True)
     total=models.DecimalField(max_digits=10, decimal_places=2)
     lr_no=models.IntegerField(null=True, blank=True)
     Fo_date=models.DateField(null=True, blank=True)
     To_date=models.DateField(null=True, blank=True)
     d_rate=models.IntegerField(null=True, blank=True)
     par_day=models.IntegerField(null=True, blank=True)
     total_d=models.IntegerField(null=True, blank=True)
      


class Ashland(models.Model):
     bill_no=models.CharField(max_length=100, null=True, blank=True, unique=True)
     date=models.DateField(null=True, blank=True)
     company=models.CharField(max_length=300, null=True, blank=True)
     gst=models.CharField(max_length=300, null=True, blank=True)
     pan=models.CharField(max_length=300, null=True, blank=True)
     tanker=models.CharField(max_length=200, null=True, blank=True)
     tanker_cap=models.CharField(max_length=200, null=True, blank=True)
     From_add=models.CharField(max_length=200, null=True, blank=True)
     To_add=models.CharField(max_length=200,null=True, blank=True)
     date_dis=models.DateField(null=True, blank=True)
     kg=models.IntegerField(null=True, blank=True)
     rate=models.IntegerField(null=True, blank=True)
     total_kg = models.IntegerField(null=True, blank=True)
     lr_no=models.IntegerField(null=True, blank=True)
     Fo_date=models.DateField(null=True, blank=True)
     To_date=models.DateField(null=True, blank=True)
     d_rate=models.IntegerField(null=True, blank=True)
     par_day=models.IntegerField(null=True, blank=True)
     total_d=models.IntegerField(null=True, blank=True)
     tank_c=models.IntegerField(null=True, blank=True)


    




class harkaran(models.Model):
     bill=models.CharField(max_length=200, null=True, blank=True, unique=True)
     date=models.DateField(null=True, blank=True)
     company=models.CharField(max_length=300, null=True, blank=True)
     gst=models.CharField(max_length=300, null=True, blank=True)
     pan=models.CharField(max_length=300, null=True, blank=True)
     tanker=models.CharField(max_length=200,null=True)
     From_add=models.CharField(max_length=200,null=True)
     To_add=models.CharField(max_length=200,null=True)
     date_dis=models.DateField(null=True, blank=True)
     kg=models.DecimalField(max_digits=10, decimal_places=2)
     rate=models.DecimalField(max_digits=10, decimal_places=2)
     total_kg=models.DecimalField(max_digits=10, decimal_places=2)
     lr_no=models.IntegerField(null=True, blank=True)



   

















class Trip(models.Model):
    trip_id = models.CharField(max_length=50, unique=True)
    tanker= models.CharField(max_length=50, null=True, blank=True)
    trip_date=models.DateField(null=True, blank=True)
    from_id = models.CharField(max_length=50, null=True, blank=True )
    To_id = models.CharField(max_length=50, null=True, blank=True )
    drivername = models.CharField(max_length=50, null=True, blank=True )
    f_trip =models.IntegerField(null=True, blank=True)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # start_time = models.DateTimeField(auto_now_add=True)
    # end_time = models.DateField(null=True, blank=True)
    # total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Trip {self.trip_id}"

    def calculate_total_expense(self):
        expenses = self.expenses.all()  # Use 'expenses' instead of 'expense_set'
        self.total_expense = sum([expense.amount for expense in expenses])
        self.save()

class Expense(models.Model):
    trip = models.ForeignKey(Trip, related_name="expenses", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    trip_general_expenses=models.IntegerField(null=True, blank=True)
    food_allowance=models.IntegerField(null=True, blank=True)
    bhatta=models.IntegerField(null=True, blank=True)
    washing_charges_tank=models.IntegerField(null=True, blank=True)
    actual_amount=models.IntegerField(null=True, blank=True)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    toll_date = models.DateField(null=True,blank=True)
    toll_amount=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    toll_name=models.CharField(max_length=200,null=True, blank=True)
    category=models.CharField(max_length=200, null=True, blank=True)
    subCategory=models.CharField(max_length=200, null=True, blank=True)
    # paid_by=models.CharField(max_length=200)
    paid_to=models.CharField(max_length=200 ,null=True, blank=True)
    amount_given=models.IntegerField(null=True, blank=True)
    liters=models.IntegerField(null=True, blank=True)
    rate=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_diesel=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_date= models.DateField(null=True,blank=True)
    bill_date= models.DateField(null=True,blank=True)
    # trip_urea_date= models.DateField(null=True, blank=False)
    urea_liter=models.IntegerField(null=True, blank=True)
    urea_rate=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    urea_total=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    r_paid_date= models.DateField(null=True,blank=True)
    r_bill_date= models.DateField(null=True,blank=True)
    spare_part=models.IntegerField(null=True, blank=True)
    r_amount=models.IntegerField(null=True, blank=True)
    part_name=models.CharField(max_length=200, null=True, blank=True)
    no_piece = models.IntegerField(null=True, blank=True)
    from_via = models.CharField(max_length=50, null=True, blank=True )
    To_via = models.CharField(max_length=50, null=True, blank=True )
    end_date= models.DateField(null=True,blank=True)

    def __str__(self):
        return f"Expense {self.id} for Trip {self.trip.trip_id}"


#==========================ADANI BILLING SYSTEM===================================

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    unload=models.IntegerField(null=True, blank=True)
    short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.IntegerField(null=True, blank=True) 
    cgst = models.FloatField(default=0.0,null=True, blank=True)
    sgst = models.FloatField(default=0.0,null=True, blank=True)
    igst = models.FloatField(default=0.0,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.FloatField(default=0.0,null=True, blank=True)


    def __str__(self):
        return self.invoice_number
    



class Item(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    



    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    



class Bill(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=255)
    gst = models.CharField(max_length=255)
    pan = models.CharField(max_length=255)
    # Other fields like static information

class TankerDetail(models.Model):
    bill = models.ForeignKey(Bill, related_name='tanker_details', on_delete=models.CASCADE)
    tanker = models.CharField(max_length=255)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    dispatch_date = models.DateField()
    tanker_capacity = models.IntegerField()
    lr_num = models.IntegerField()
    loaded_qty = models.IntegerField()
    rate_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)






class  AddBank_Loan(models.Model):
    name= models.CharField(max_length=255, null=True, blank=True)
    




class Loan(models.Model):
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_tenure_months = models.IntegerField()

    def __str__(self):
        return f"Loan of {self.principal_amount} for {self.loan_tenure_months} months"

class Addloan(models.Model):
    tankerno=models.CharField(max_length=255,null=True, blank=True)
    loan_contract=models.CharField(max_length=255,null=True, blank=True)
    finance_by=models.CharField(max_length=255,null=True, blank=True)
    pamount=models.DecimalField(max_digits=12, decimal_places=2)
    iamount=models.DecimalField(max_digits=10, decimal_places=2)
    famount=models.DecimalField(max_digits=15, decimal_places=2)
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    ddate=models.DateField(blank=True,null=True)
    pdate=models.DateField(blank=True,null=True)
    days=models.CharField(max_length=150, blank=True,null=True)
    bank=models.CharField(max_length=150, blank=True,null=True)
    ramount=models.DecimalField(max_digits=15, decimal_places=2)



class DriverLoan(models.Model):
    tankerno=models.CharField(max_length=100)
    From_address=models.CharField(max_length=200)
    To_address=models.CharField(max_length=200)
    drivername=models.CharField(max_length=100)
    trip_date=models.DateField(null=True, blank=True)
    date=models.DateField(null=True, blank=True)
    load=models.IntegerField(null=True, blank=True)
    unload=models.IntegerField(null=True, blank=True)
    short_kg=models.IntegerField(null=True, blank=True)
    allow_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_short = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True )
    short_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True )
    previous_loan = models.IntegerField(null=True, blank=True)
    loan_amount = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)



class Tracking(models.Model):
    tanker_no = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField(max_length=15)
    tdate = models.DateField(max_length=255)
    destination = models.CharField(max_length=255)
    vehicle_status = models.CharField(max_length=100, null=True,blank=True)
       


class State(models.Model):
    statename = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.statename

class City(models.Model):
    cityname = models.CharField(max_length=200, null=True, blank=True)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cityname}, {self.state.statename}"
    

#===================Client Side View====================



class Clientgemini(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    tanker_type=models.CharField(max_length=200, null=True,blank=True)
    tanker_cpa=models.CharField(max_length=200, null=True,blank=True)
    fadd=models.CharField(max_length=200, null=True,blank=True)
    tadd=models.CharField(max_length=200, null=True,blank=True)
    ddate=models.DateField(null=False,blank=False)
    create_date=models.DateTimeField(auto_now_add=True)

    
# models.py
class Bills(models.Model):
    customer_name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class BillItem(models.Model):
    bill = models.ForeignKey(Bills, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)




#=======================ASHLAND BILLING SYSTEM ==================================
class AInvoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    # tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    # unload=models.IntegerField(null=True, blank=True)
    # short=models.IntegerField(null=True, blank=True)
    # retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    t_rate=models.IntegerField(null=True, blank=True)
    tpar_day=models.IntegerField(null=True, blank=True)
    total_t=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    thsac=models.IntegerField(null=True, blank=True)
    tcharges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.invoice_number
    



class AItem(models.Model):
    invoice = models.ForeignKey(AInvoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    

#==========================CARGILL BILLING SYSTEM===================================




#==========================AAK OUT WORD BILLING SYSTEM===================================

class Aak_in_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    unload=models.IntegerField(null=True, blank=True)
    short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.IntegerField(null=True, blank=True) 
    cgst = models.FloatField(default=0.0,null=True, blank=True)
    sgst = models.FloatField(default=0.0,null=True, blank=True)
    igst = models.FloatField(default=0.0,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.FloatField(default=0.0,null=True, blank=True)


    def __str__(self):
        return self.invoice_number
    



class Aak_in_Item(models.Model):
    invoice = models.ForeignKey(Aak_in_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    


    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description


#=======================GEMINI BILLING SYSTEM ==================================


class GInvoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    # tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    # unload=models.IntegerField(null=True, blank=True)
    # short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.invoice_number
    



class GItem(models.Model):
    invoice = models.ForeignKey(GInvoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    




#=======================VVF TALOJA BILLING SYSTEM ==================================
class vvft_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    # tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    # unload=models.IntegerField(null=True, blank=True)
    # short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.invoice_number
    



class vvft_Item(models.Model):
    invoice = models.ForeignKey(vvft_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    




#=======================VISWAAT CHEMICALS SYSTEM ==================================
class VC_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    # tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    # unload=models.IntegerField(null=True, blank=True)
    # short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.invoice_number
    



class VC_Item(models.Model):
    invoice = models.ForeignKey(VC_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    







#=======================TEASTY BITE SYSTEM ==================================
class TB_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    unload=models.IntegerField(null=True, blank=True)
    short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.IntegerField(null=True, blank=True) 
    cgst = models.FloatField(default=0.0,null=True, blank=True)
    sgst = models.FloatField(default=0.0,null=True, blank=True)
    igst = models.FloatField(default=0.0,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.FloatField(default=0.0,null=True, blank=True)


    def __str__(self):
        return self.invoice_number
    



class TB_Item(models.Model):
    invoice = models.ForeignKey(TB_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    



    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    

#=======================AAK INDIA OUT WORD SYSTEM ==================================
class AO_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    unload=models.IntegerField(null=True, blank=True)
    short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.IntegerField(null=True, blank=True) 
    cgst = models.FloatField(default=0.0,null=True, blank=True)
    sgst = models.FloatField(default=0.0,null=True, blank=True)
    igst = models.FloatField(default=0.0,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.FloatField(default=0.0,null=True, blank=True)


    def __str__(self):
        return self.invoice_number
    



class AO_Item(models.Model):
    invoice = models.ForeignKey(AO_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    



    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    


#=======================KND BUSINESS SYSTEM ==================================
class  KND_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    # tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    # unload=models.IntegerField(null=True, blank=True)
    # short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.invoice_number
    



class KND_Item(models.Model):
    invoice = models.ForeignKey( KND_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    

#=======================SHRI RISHABH INDIA BITE SYSTEM ==================================
class SR_Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    company=models.CharField(max_length=300, null=True, blank=True)
    gst=models.CharField(max_length=300, null=True, blank=True)
    pan=models.CharField(max_length=300, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_in_words = models.CharField(max_length=255, blank=True)
    tanker=models.CharField(max_length=200, null=True, blank=True)
    tanker_cap=models.IntegerField(null=True, blank=True)
    From_add=models.CharField(max_length=200, null=True, blank=True)
    To_add=models.CharField(max_length=200,null=True, blank=True)
    date_dis=models.DateField(null=True, blank=True)
    # load=models.IntegerField(null=True, blank=True)
    # rate_kg=models.IntegerField(null=True, blank=True)
    unload=models.IntegerField(null=True, blank=True)
    short=models.IntegerField(null=True, blank=True)
    retn=models.IntegerField(null=True, blank=True)
    lr_no=models.CharField(max_length=200, null=True, blank=True)
    sac=models.IntegerField(null=True, blank=True)
    Fo_date=models.DateField(null=True, blank=True)
    To_date=models.DateField(null=True, blank=True)
    d_rate=models.IntegerField(null=True, blank=True)
    par_day=models.IntegerField(null=True, blank=True)
    total_d=models.IntegerField(null=True, blank=True) 
    cgst = models.FloatField(default=0.0,null=True, blank=True)
    sgst = models.FloatField(default=0.0,null=True, blank=True)
    igst = models.FloatField(default=0.0,null=True, blank=True)
    fright_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hsac=models.IntegerField(null=True, blank=True)
    charges=models.CharField(max_length=300, null=True, blank=True)
    c_gst = models.FloatField(default=0.0,null=True, blank=True)
    s_gst = models.FloatField(default=0.0,null=True, blank=True)
    i_gst = models.FloatField(default=0.0,null=True, blank=True)
    g_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.FloatField(default=0.0,null=True, blank=True)


    def __str__(self):
        return self.invoice_number
    



class SR_Item(models.Model):
    invoice = models.ForeignKey(SR_Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    



    def save(self, *args, **kwargs):
        # Calculate total price for the item
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
    