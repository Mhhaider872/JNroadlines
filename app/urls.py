from django.contrib import admin
from django.urls import path
from app import views 


urlpatterns =[
    path('admin/', admin.site.urls),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/haider/',views.userdash,name='udashboard'),
    path('dashboard/pooja/',views.userloan,name='ldashboard'),
    
    
    
    path('plan/',views.plan,name='plan'),
    path('get_capacity/', views.get_capacity, name='get_capacity'),
    path('show_plan/',views.showplan,name='showplan'),
    path('update_plan/<int:id>',views.updateplan,name='update-plan'),
    path('do_updateplan/<int:id>',views. do_updateplan,name='do-updateplan'),
    path('deleteplan/<int:id>',views.deleteplan,name='delete-plan'),
    
    path('add_trip/',views.addtrip,name='addtrip'),
    path('show_trip/',views.showtrip,name='showtrip'),
    path('get_plan_details/', views.get_plan_details, name='get_plan_details'),
    path('delete/<int:id>/',views.deltrip,name='del-trip'),
    path('update/<int:id>/',views.updatetrip,name='update-trip'),
    path('do_updatetrip/<int:id>/',views.do_updatetrip,name='updatetrip'),



    path('add_trip_adani/',views.Trip_Adani,name='trip-adani'),
    path('show_adani_trip/',views.ShowAdani,name='show-adani'),
    path('delete_adani/<int:id>',views.delatrip,name='del-adani'),
    path('update_adani/<int:id>',views.upadanitrip,name='up-adani'),
    path('doupdate/<int:id>',views.do_upadani,name='do_up_adani'),




   
    

    
    path('aak_india_local/',views.aaklocal,name='aak-local'),
    path('show_aak_local/',views.ShowAakLocal,name='Aak-Local'),
    path('update_aak_local/<int:id>/',views.updateAak,name='update-Local'),
    path('do_update_aak_local/<int:id>',views.doupdateAak,name='doLocal'),
    path('del_aak_local/<int:id>',views.delete,name='delete-local'),

    path('add_trip_gemini/',views.Trip_Gemini,name='trip-gemini'),
    path('show_gemini_trip/',views.Showgemini,name='show-gemini-details'),
    path('delete_gemini_trip/<int:id>',views.delgemini,name='g-delete'),
    path('update_gemini_trip/<int:id>',views.upgemini,name='gemini-update'),
    path('do_update_gemini/<int:id>',views.do_upgemini,name='do-gemini-update'),




    

    
    
    path('add_vehicle/',views.vehicledetails,name='addvehicle'),
    path('show_vehicle/',views.show_vehicledetails,name='show-vehicle'),   
    path('delete_vehicle/<int:id>',views.deletevehicle,name='d-vehicle'), 
    path('update_vehicle/<int:id>',views.updatevehicle,name='up-vehicle'),
    path('update/<int:id>',views.doupdatevehicle,name='update-vehicledetails'),

    path('company_details/',views.company_details,name='company-details'),  
    path('show_company_details/',views.show_company,name='s-company'), 
    path('delete/<int:id>',views.delete_company,name='de-company'),
    path('update_company/<int:id>',views.updatecompany,name='update-company'),
    path('company_details_update/<int:id>',views.doupdatecompany,name='company-update'),
    
    path('add_driver/',views.adddriver,name='adddriver'),
    path('show_driver/',views.showdriver,name='showdrivers'),
    path('driverdelete/<int:id>',views.deletedriver,name='d-driver'),
    path('update_driver/<int:id>',views.driverupdate,name='updates-driver'),
    path('drivers_update/<int:id>',views.doupdatedriver,name='drivers-updated'),

    path('add_salary/', views.addsalary, name='add-salary'),
    path('show_salary/', views.showsalary, name='show-s'),
    path('delete_salary/<int:id>', views.dsalary, name='delete-s'),
    path('update_salary/<int:id>', views.usalary, name='update-s'),
    path('do_salary/<int:id>', views.do_update_salary, name='do-update'),
    
    path('bank_details/',views.addbank,name='bank-details'),
    path('loan_details/',views.addloan,name='loandetails'),
    path('show_loan_details/',views.showloan,name='loan-show'),
    path('delete_loan/<int:id>',views.ldelete,name='delete_l'),
    
    # path('trip_expense/',views.tripexpense,name='trip-expense'),
    # path('show_expense/',views.showtripexpense,name='show-expense'),
    path('add_toll/',views.addtolls,name='add-toll'),
    path('toll_details/',views.tolldetails,name='toll-details'),
    path('toll_delete/<int:id>', views.tolldelete, name='toll-d'),
    path('toll_update/<int:id>', views.updatedelete, name='toll-update'),
    path('dotoll_update/<int:id>', views.doupdate_toll, name='toll-doupdate'),
    # path('show_diesel_details/', views.dieseldetails, name='show-diesel'),
    path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    
    # path('add_urea/', views.addurea, name='add-urea'),
    # path('show_urea_details/', views.showurea, name='urea-details'),
    # path('add_repairs/', views.repairs, name='add-repairs'),
    path('reports/', views.report, name='report-show'),
    # path('all_expense/', views.all_trip, name='all-trip'),
    # path('show_all_expense/', views.showallexpense, name='all-expense'),
    # path('delete_expense/<int:id>', views.allexpensedelete, name='del-expense'),
    # path('update_expense/<int:id>',views.updatExpense,name='update-expense'),
    # path('start-trip/', views.start_trip, name='start_trip'),
    # path('end-trip/<int:trip_id>/', views.end_trip, name='end_trip'),
    #  path('tanker-detail/<int:tanker_id>/', views.tanker_detail, name='tanker_details'),
    # path('addendtrip',views.addEndTrip,name='add-trip-end'),
    # path('showendtrip',views.showEndTrip,name='show-trip-end'),
    
    path('driver_loan',views.AddDriverLoan,name='drivers-loan'),
    path('show_driver_loan',views.ShowLoan,name='show-loan'),
    path('loan_delete/<int:id>',views.deleteloan,name='loan-delete'),
    path('driverloan_update/<int:id>',views.updriverloan,name='update-dloan'),
    path('dloan_update/<int:id>',views.do_update_dloan,name='updatedloan'),
   
   
    path('all_bills/',views.all_bill,name='all-bill'),
    # path('aak_india_bills/',views.aak_bill,name='aak-bills'),
    # path('aak_bill/',views.Aak_bills,name='aak-bill'),
    # path('ashland_india/',views.ashland,name='ash-bills'),
    # path('show_ashland/',views.Showashland,name='show-ashland'),
    # path('ashland_bill/',views.Ash_bills,name='ash-bill'),
    # path('cargill_india/',views.Cargill,name='cargill'),
    # path('harkaran_dass/',views.Harkaran,name='harkaran'),
    # path('vvf_india/',views.VVF,name='vvf-india'),
    # path('anjani_agro/',views.Anjani,name='anjani'),
    # path('cargill/',views.create_bill,name='cargill'),

    

    
    # path('gemini_bills/',views.gemini_bill,name='gemini-bills'),
    # path('bill_details_ge/',views.geminidetails,name='gemini-show'),

    # path('bill/',views.bills,name='bills-show'),
  


    path('start/', views.start_trip, name='start_trip'),

    path('add_expense/<str:trip_id>/', views.add_expense, name='add_expense'),
    path('update_expense/<int:id>/',views.update_exp,name='update-exp'),
    path('do_update_expense/<int:id>/',views.do_update,name='do-exp-update'),
    path('delete_exp/<int:id>',views.delete_expense,name='delete-exp'),


    # path('end_trip/<str:trip_id>/', views.end_trip, name='end_trip'),



    path('signup/', views.SignUp, name='sign-up'),
    path('', views.Login, name='log-in'),
    path('logout/', views.Logout_user, name='logout'),


    path('all_trip/', views.AllTrip, name='trip'),
    path('delete_all_trip/<int:id>', views.del_allTrip, name='delete-trip'),

    # path('create-invoice/', views.create_invoice, name='create_invoice'),
    # path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),


    path('add_petrol_pump/', views.AddPetrolp, name='add-petrol'),
    path('show_petrol_pump/', views.showpertol, name='s-petrol'),
    path('delete_petrol_pump/<int:id>', views.dpertol, name='d-petrol'),
    path('add_bank/', views.addbank, name='add-bank'),
    path('404_page', views.errorpage, name='404-page'),
    path('get-cities/', views.get_cities, name='get_cities'),
    
    path('add_track/',views.tracking,name='vehicle-track'),
    path('show_track/',views.showtrack,name='show-track'),
    # path('test-email/', views.send_test_email, name='test_email'),

    #=================Client Dashboard Url=========
    path('gemini/gemini/', views.cgemini, name='gemini'),
    path('add_order/gemini/', views.geminiorder, name='order-gemini'),
    path('show_order/gemini/', views.gorder, name='order-show'),
    path('order_by_company/', views.companyorder, name='com-order'),


    #=================Fresh Order Url===============
    path('order_by_gemini/', views.freshgemini, name='fresh-ogemini'),
    path('plan_gemini/', views.plangemini, name='plan-ogemini'),
    
    


    #======================Billing ULRs===========================================
    path('Billing_page/', views.Billing, name='bill-page'),


    #=======================Adani Bill=============================================
    path('create-bill/', views.adani_bill, name='create_bill'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),

    #=======================Gemini Bill=============================================
    path('gemini-bill/', views.gemini_bill, name='create_bill_gemini'),
    path('gemini_invoices/', views.Ginvoice_list, name='ginvoice_list'),
    path('gemini/<int:invoice_id>/', views.Ginvoice_detail, name='ginvoice_detail'),

     #=======================Gemini Bill=============================================
    path('ashland-bill/', views.ashland_bill, name='create_bill_ashland'),
    path('ashland_invoices/', views.Ainvoice_list, name='ainvoice_list'),
    path('ashland/<int:invoice_id>/', views.Ainvoice_detail, name='ainvoice_detail'),
    #=======================Cargill Bill=============================================
    # path('cargill-bill/', views.cargill_bill, name='create_bill_cargill'),
    # path('cargill_invoices/', views.cainvoice_list, name='cinvoice_list'),
    # path('cargill/<int:invoice_id>/', views.cainvoice_detail, name='cinvoice_detail'),


      #=======================Aak India INword Bill=============================================
    path('Aak_Inword-bill/', views.aakin_bill, name='create_bill_Aak_Inword'),
    path('Aak_Inword_invoices/', views.aakin_list, name='Aak_Inword_list'),
    path('Aak_Inword/<int:invoice_id>/', views.aakin_detail, name='Aak_Inword_detail'),


       #=======================VVF TALOJA Bill=============================================
    path('Vvf-taloja-bill/', views.vvft_bill, name='create_vvf_taloja'),
    path('vvft_invoices/', views.vvftinvoice_list, name='vvft_list'),
    path('vvf_t/<int:invoice_id>/', views.vvft_detail, name='vvft_detail'),

  
]






