from django.contrib import admin
from django.urls import path
from app import views 


urlpatterns =[
    path('admin/', admin.site.urls),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('plan/',views.plan,name='plan'),
    path('show_plan/',views.showplan,name='showplan'),
    path('update_plan/<int:id>',views.updateplan,name='update-plan'),
    path('do_updateplan/<int:id>',views. do_updateplan,name='do-updateplan'),
    path('deleteplan/<int:id>',views.deleteplan,name='delete-plan'),
    
    path('add_trip/',views.addtrip,name='addtrip'),
    path('add_trip_adani/',views.Trip_Adani,name='trip-adani'),
    path('show_adani_trip/',views.ShowAdani,name='show-adani'),

    path('add_track/',views.tracking,name='vehicle-track'),
    path('show_track/',views.showtrack,name='show-track'),
    

    
    path('aak_india_local/',views.aaklocal,name='aak-local'),
    path('show_aak_local/',views.ShowAakLocal,name='Aak-Local'),
    path('update_aak_local/<int:id>/',views.updateAak,name='update-Local'),
    path('do_update_aak_local/<int:id>',views.doupdateAak,name='doLocal'),
    path('del_aak_local/<int:id>',views.delete,name='delete-local'),

    path('add_trip_gemini/',views.Trip_Gemini,name='trip-gemini'),
    path('show_gemini_trip/',views.Showgemini,name='show-gemini-details'),
    path('show_trip/',views.showtrip,name='showtrip'),
    path('delete/<int:id>/',views.deltrip,name='del-trip'),
    path('update/<int:id>/',views.updatetrip,name='update-trip'),
    path('do_updatetrip/<int:id>/',views.do_updatetrip,name='updatetrip'),

    
    
    path('add_vehicle/',views.vehicledetails,name='addvehicle'),
    path('show_vehicle/',views.show_vehicledetails,name='show-vehicle'),   

    path('company_details/',views.company_details,name='company-details'),  
    path('show_company_details/',views.show_company,name='s-company'), 
    
    path('add_driver/',views.adddriver,name='adddriver'),
    path('show_driver/',views.showdriver,name='showdrivers'),
    path('driverdelete/<int:id>',views.deletedriver,name='deletedriver'),

    path('add_salary/', views.addsalary, name='add-salary'),
    path('show_salary/', views.showsalary, name='show-s'),
    
    path('loan_details/',views.addloan,name='loandetails'),
    
    path('trip_expense/',views.tripexpense,name='trip-expense'),
    path('show_expense/',views.showtripexpense,name='show-expense'),
    path('add_toll/',views.addtolls,name='add-toll'),
    path('toll_details/',views.tolldetails,name='toll-details'),
    path('diesel_details/', views.adddiesel, name='diesel-details'),
    path('show_diesel_details/', views.dieseldetails, name='show-diesel'),
    path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    
    path('add_urea/', views.addurea, name='add-urea'),
    path('show_urea_details/', views.showurea, name='urea-details'),
    path('add_repairs/', views.repairs, name='add-repairs'),
    path('reports/', views.report, name='report-show'),
    path('all_expense/', views.all_trip, name='all-trip'),
    path('show_all_expense/', views.showallexpense, name='all-expense'),
    path('delete_expense/<int:id>', views.allexpensedelete, name='del-expense'),
    # path('update_expense/<int:id>',views.updatExpense,name='update-expense'),
    # path('start-trip/', views.start_trip, name='start_trip'),
    # path('end-trip/<int:trip_id>/', views.end_trip, name='end_trip'),
    #  path('tanker-detail/<int:tanker_id>/', views.tanker_detail, name='tanker_details'),
    path('addendtrip',views.addEndTrip,name='add-trip-end'),
    path('showendtrip',views.showEndTrip,name='show-trip-end'),
    
    path('driver_loan',views.AddDriverLoan,name='drivers-loan'),
    path('show_driver_loan',views.ShowLoan,name='show-loan'),
   
   
    path('all_bills/',views.all_bill,name='all-bill'),
    path('aak_india_bills/',views.aak_bill,name='aak-bills'),
    path('aak_bill/',views.Aak_bills,name='aak-bill'),
    path('ashland_india/',views.ashland,name='ash-bills'),
    path('show_ashland/',views.Showashland,name='show-ashland'),
    path('ashland_bill/',views.Ash_bills,name='ash-bill'),
    path('cargill_india/',views.Cargill,name='cargill'),
    path('harkaran_dass/',views.Harkaran,name='harkaran'),
    path('vvf_india/',views.VVF,name='vvf-india'),
    path('anjani_agro/',views.Anjani,name='anjani'),
    path('cargill/',views.create_bill,name='cargill'),

    

    
    path('gemini_bills/',views.gemini_bill,name='gemini-bills'),
    path('bill_details_ge/',views.geminidetails,name='gemini-show'),

    path('bill/',views.bills,name='bills-show'),
  


    path('start/', views.start_trip, name='start_trip'),

    path('add_expense/<str:trip_id>/', views.add_expense, name='add_expense'),
    path('update_expense/<int:id>/',views.update_exp,name='update-exp'),
    path('do_update_expense/<int:id>/',views.do_update,name='do-exp-update'),
    path('delete_exp/<int:id>',views.delete_expense,name='delete-exp'),


    path('end_trip/<str:trip_id>/', views.end_trip, name='end_trip'),



    path('signup/', views.SignUp, name='sign-up'),
    path('', views.Login, name='log-in'),
    path('logout/', views.Logout_user, name='logout'),


    path('all_trip/', views.AllTrip, name='trip'),
    path('delete_all_trip/<int:id>', views.del_allTrip, name='delete-trip'),

    path('create-invoice/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),



    path('emi_calculator/', views.emi_calculator, name='emi_calculator'),
]






